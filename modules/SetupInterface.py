from modules.CaptureManager import CaptureManager

from configparser import ConfigParser


from GUI.setupWindow import *
from modules.CustomSlots import CustomSlots
from modules.ProcessingTools import ProcessingTools
from modules.ToolSettingsInterface import ToolSettingsInterface
from PyQt4.QtCore import QThread
import time


class SetupInterface(Ui_SetupWindow):
    def __init__(self, captureManager):
        super(SetupInterface, self).__init__()
        self.config = ConfigParser()
        self.frame = None
        self.capture = True
        self.captureManager = captureManager
        self.edged = [None] * 5
        self.ColorThresh = [None] * 5
        self.pixelColor = [None] * 5
        self.measurementThresh = [None] * 5
        self.patternThresh = [None] * 5
        self.toolList = [None] * 5
        self.ignoredPixels = [None] * 5
        self.Results = [None] * 5
        self.setupWindow = CustomSlots(self)
        self.setupUi(self.setupWindow)
        self.setupWindow.show()
        self.refresher = refreshFrameThread(self, self.setupWindow)
        self.config.read('config/config'+str(self.captureManager.programNumber)+'.ini')
        if self.captureManager.isMasterExist():
            self.frame = captureManager.loadFrame(
                './Masters/MasterImage' + str(self.captureManager.programNumber) + '.jpg')
            self.setImagePreview(self.frame)
        else:
            self.liveStream()
        QtCore.QObject.connect(self.refresher, QtCore.SIGNAL('refreshFrame()'), self.refreshFrame)
        self.ToolsListSetup.hide()

        QtCore.QObject.connect(self.ThreshSlider1, QtCore.SIGNAL("sliderPressed()"),
                               self.setToolIndex1)
        QtCore.QObject.connect(self.ThreshSlider1, QtCore.SIGNAL("valueChanged(int)"),
                               self.setToolIndex1)
        QtCore.QObject.connect(self.ThreshSlider2, QtCore.SIGNAL("sliderPressed()"),
                               self.setToolIndex2)
        QtCore.QObject.connect(self.ThreshSlider2, QtCore.SIGNAL("valueChanged(int)"),
                               self.setToolIndex2)
        QtCore.QObject.connect(self.ThreshSlider3, QtCore.SIGNAL("sliderPressed()"),
                               self.setToolIndex3)
        QtCore.QObject.connect(self.ThreshSlider3, QtCore.SIGNAL("valueChanged(int)"),
                               self.setToolIndex3)
        QtCore.QObject.connect(self.ThreshSlider4, QtCore.SIGNAL("sliderPressed()"),
                               self.setToolIndex4)
        QtCore.QObject.connect(self.ThreshSlider4, QtCore.SIGNAL("valueChanged(int)"),
                               self.setToolIndex4)

        self.processingTools = ProcessingTools()
        self.defaultDoubleClick = self.ImagePreview.mouseDoubleClickEvent
        self.defaultMousePress = self.ImagePreview.mousePressEvent
        self.defaultMouseRelease = self.ImagePreview.mouseReleaseEvent
        self.defaultMouseMove = self.ImagePreview.mouseMoveEvent
        self.defaultKeyPressed = self.setupWindow.keyPressEvent

        self.ImagePreview.mouseDoubleClickEvent = self.DoNothing
        self.ImagePreview.mousePressEvent = self.DoNothing
        self.ImagePreview.mouseReleaseEvent = self.DoNothing
        self.ImagePreview.mouseMoveEvent = self.DoNothing
        self.setupWindow.keyPressEvent = self.DoNothing

    def setToolIndex1(self):
        self.captureManager.toolIndex = 1

    def setToolIndex2(self):
        self.captureManager.toolIndex = 2

    def setToolIndex3(self):
        self.captureManager.toolIndex = 3

    def setToolIndex4(self):
        self.captureManager.toolIndex = 4

    def DoNothing(self, event):
        return

    def refreshFrame(self):
        if self.setupWindow.isVisible():

            self.captureManager.setCamera(0)
            self.frame = self.captureManager.readFrame()
            self.setImagePreview(self.frame)
            self.captureManager.cameraRelease()

        else:
            self.capture = False

    def liveStream(self):
        self.capture = True
        self.refresher.start()

    def saveMaster(self):

        name = QtGui.QFileDialog.getSaveFileName(self.setupWindow, 'Save File', 'MasterImage' +
                                                 str(self.captureManager.getProgramNumber) + '.jpg')
        if name.endswith(('/.png', '/.jpg', '/.jpeg')):
            self.saveMaster()

        elif name.endswith(('.png', '.jpg', '.jpeg')):
            print(name)
            self.captureManager.saveImage(self.frame, name)

    def showToolSettings(self, ToolIndex):
        self.captureManager.toolIndex = ToolIndex

        self.toolSettingsUi = ToolSettingsInterface(self.captureManager, self)

    def setImagePreview(self, frame):
        temp = self.captureManager.makePixmap(frame)
        self.ImagePreview.setPixmap(QtGui.QPixmap(temp))

    def countColorPixels(self):
        self.enable('doubleClick')

        if self.pixelColor[self.captureManager.toolIndex] is not None and \
                self.ColorThresh[self.captureManager.toolIndex] is not None and \
                self.ColorThresh[self.captureManager.toolIndex].isEnabled():
            pixels, frame = self.processingTools.countColorPixel(self.frame, self.pixelColor[
                self.captureManager.toolIndex],int(self.ColorThresh[self.captureManager.toolIndex].value()))

            self.setImagePreview(frame)
            print(pixels)
            self.Results[self.captureManager.toolIndex] = pixels
        else:
            self.setImagePreview(self.frame)
            self.Results[self.captureManager.toolIndex] = None

    def getPixel(self, event):

        x = event.pos().x()
        y = event.pos().y()
        self.pixelColor[self.captureManager.toolIndex] = self.frame[y, x]
        self.countColorPixels()

    def measureDistance(self):
        self.enable('removePixel')
        xdistance, ydistance, edgedMeasure = self.processingTools.measure(
            self.edged[self.captureManager.toolIndex], self.measurementThresh[self.captureManager.toolIndex].value(), True, True)
        self.setImagePreview(edgedMeasure)
        self.Results[self.captureManager.toolIndex] = (xdistance, ydistance)


    def detectPattern(self):
        if self.masterPattern is None:
            self.statusbar.showMessage("no reference found please select a new reference")
            self.enable('cropArea')
        else:
            self.enable('')
        self.setImagePreview(self.frame)
        if self.masterPattern is None:
            return
        maxThresh = self.patternThresh[self.captureManager.toolIndex].maximum()
        pos, pattern = self.processingTools.detectPattern(
            self.frame, self.masterPattern,
            (maxThresh - self.patternThresh[self.captureManager.toolIndex].value()) / 100,
            True)
        self.setImagePreview(pattern)
        print("detected patterns= ", len(pos))
        self.Results[self.captureManager.toolIndex] = len(pos)

    def startIgnoring(self, event):
        x = event.pos().x()
        y = event.pos().y()
        self.dragging = True
        self.startPoint = x, y
        self.ImagePreview.mouseMoveEvent = self.drawIgnored

    def drawIgnored(self, event):
        x = event.pos().x()
        y = event.pos().y()
        self.setupWindow.keyPressEvent = self.KeyboardEscapePressed
        if self.dragging:
            edged = self.processingTools.gray2BGR(self.edged[self.captureManager.toolIndex])
            self.captureManager.drawRectangle(edged, (x, y), self.startPoint, (0, 0, 255))
            self.setImagePreview(edged)
        else:
            self.setImagePreview(self.edged[self.captureManager.toolIndex])

    def stopIgnoring(self, event):

        self.ImagePreview.mouseMoveEvent = self.defaultMouseMove
        x = event.pos().x()
        y = event.pos().y()

        if (x, y) == self.startPoint:
            # x += 1
            # y += 1
            self.dragging=False

        if self.dragging:
            self.edged[self.captureManager.toolIndex] = self.processingTools.ignoreEdge(self.edged[self.captureManager.toolIndex], self.startPoint[0], self.startPoint[1],
                                                         (y - self.startPoint[1]), (x - self.startPoint[0]))
            edged = self.processingTools.gray2BGR(self.edged[self.captureManager.toolIndex])
            self.captureManager.drawRectangle(edged, (x, y), self.startPoint, (0, 0, 255))
            self.ignoredPixels[self.captureManager.toolIndex].append([(x,y),self.startPoint])
            print("tool",self.captureManager.toolIndex)
            print(self.ignoredPixels[self.captureManager.toolIndex])

        else:
            edged = self.edged[self.captureManager.toolIndex]
        self.setImagePreview(edged)

    def startCropping(self, event):
        x = event.pos().x()
        y = event.pos().y()
        self.dragging = True
        self.startPoint = x, y
        self.ImagePreview.mouseMoveEvent = self.drawCropped

    def drawCropped(self, event):
        x = event.pos().x()
        y = event.pos().y()
        self.setupWindow.keyPressEvent = self.KeyboardEscapePressed
        if self.dragging:
            frame = self.frame.copy()
            self.captureManager.drawRectangle(frame, (x, y), self.startPoint, (0, 0, 255))
            self.setImagePreview(frame)
        else:
            self.setImagePreview(self.frame)

    def stopCropping(self, event):

        self.ImagePreview.mouseMoveEvent = self.defaultMouseMove
        x = event.pos().x()
        y = event.pos().y()
        frame = self.frame.copy()
        if (x, y) == self.startPoint:
            return
        if self.dragging:
            self.cropped = self.processingTools.cropFrame(self.frame, self.startPoint[0], self.startPoint[1],
                                                          (y - self.startPoint[1]), (x - self.startPoint[0]))
            self.captureManager.drawRectangle(frame, (x, y), self.startPoint, (0, 0, 255))
        self.masterPattern = self.cropped
        self.setImagePreview(self.frame)

    def coloredPixel(self):

        self.setImagePreview(self.frame)
        if self.captureManager.toolIndex == 1:
            self.ColorThresh[self.captureManager.toolIndex] = self.ThreshSlider1
            toolName = self.ToolName1
        elif self.captureManager.toolIndex == 2:
            self.ColorThresh[self.captureManager.toolIndex] = self.ThreshSlider2
            toolName = self.ToolName2
        elif self.captureManager.toolIndex == 3:
            self.ColorThresh[self.captureManager.toolIndex] = self.ThreshSlider3
            toolName = self.ToolName3
        elif self.captureManager.toolIndex == 4:
            self.ColorThresh[self.captureManager.toolIndex] = self.ThreshSlider4
            toolName = self.ToolName4
        self.ColorThresh[self.captureManager.toolIndex].setMaximum(255)
        toolName.setText("Color Pixel Tool")
        self.toolList[self.captureManager.toolIndex]="Color Pixel Tool"
        QtCore.QObject.connect(self.ColorThresh[self.captureManager.toolIndex], QtCore.SIGNAL("valueChanged(int)"),
                               self.countColorPixels)
        QtCore.QObject.connect(self.ColorThresh[self.captureManager.toolIndex], QtCore.SIGNAL("sliderPressed()"),
                               self.countColorPixels)

        self.enable('doubleClick')

    def measurement(self):

        if self.captureManager.toolIndex == 1:
            self.measurementThresh[self.captureManager.toolIndex] = self.ThreshSlider1
            toolName = self.ToolName1
        elif self.captureManager.toolIndex == 2:
            self.measurementThresh[self.captureManager.toolIndex] = self.ThreshSlider2
            toolName = self.ToolName2
        elif self.captureManager.toolIndex == 3:
            self.measurementThresh[self.captureManager.toolIndex] = self.ThreshSlider3
            toolName = self.ToolName3
        elif self.captureManager.toolIndex == 4:
            self.measurementThresh[self.captureManager.toolIndex] = self.ThreshSlider4
            toolName = self.ToolName4
        toolName.setText("measurement Tool")
        self.ignoredPixels[self.captureManager.toolIndex]=[]
        self.toolList[self.captureManager.toolIndex] = "measurement Tool"
        self.measurementThresh[self.captureManager.toolIndex].setMaximum(max(self.frame.shape))
        self.edged[self.captureManager.toolIndex] = self.processingTools.detectEdges(self.frame)

        self.setImagePreview(self.edged[self.captureManager.toolIndex])
        QtCore.QObject.connect(self.measurementThresh[self.captureManager.toolIndex],
                               QtCore.SIGNAL("valueChanged(int)"),
                               self.measureDistance)
        QtCore.QObject.connect(self.measurementThresh[self.captureManager.toolIndex], QtCore.SIGNAL("sliderPressed()"),
                               self.measureDistance)

        self.enable('removePixel')

    def patternDetection(self):
        try:
            self.masterPattern = self.captureManager.loadFrame('./Masters/MasterPattern' +
                                                               str(self.captureManager.programNumber) + '.jpg')
        except Exception:
            pass
        if self.masterPattern is None:
            self.statusbar.showMessage("no reference found please select a new reference")
            self.enable('cropArea')

        if self.captureManager.toolIndex == 1:
            self.patternThresh[self.captureManager.toolIndex] = self.ThreshSlider1
            toolName = self.ToolName1
        elif self.captureManager.toolIndex == 2:
            self.patternThresh[self.captureManager.toolIndex] = self.ThreshSlider2
            toolName = self.ToolName2
        elif self.captureManager.toolIndex == 3:
            self.patternThresh[self.captureManager.toolIndex] = self.ThreshSlider3
            toolName = self.ToolName3
        elif self.captureManager.toolIndex == 4:
            self.patternThresh[self.captureManager.toolIndex] = self.ThreshSlider4
            toolName = self.ToolName4
        else:
            toolName=None
        self.patternThresh[self.captureManager.toolIndex].setMaximum(100)
        toolName.setText("Pattern Detection Tool")
        self.toolList[self.captureManager.toolIndex] = "Pattern Detection Tool"
        self.detectPattern()
        QtCore.QObject.connect(self.patternThresh[self.captureManager.toolIndex], QtCore.SIGNAL("valueChanged(int)"),
                               self.detectPattern)
        QtCore.QObject.connect(self.patternThresh[self.captureManager.toolIndex], QtCore.SIGNAL("sliderPressed()"),
                               self.detectPattern)

    def enable(self, command):
        if command == 'removePixel':
            self.ImagePreview.mouseMoveEvent = self.defaultMouseMove
            self.ImagePreview.mouseDoubleClickEvent = self.defaultDoubleClick
            self.ImagePreview.mousePressEvent = self.startIgnoring
            self.ImagePreview.mouseReleaseEvent = self.stopIgnoring
            self.statusbar.showMessage("right click + drag to select filtred area"
                                       " --- "
                                       "escape to cancel selection")
        elif command == 'doubleClick':
            self.ImagePreview.mouseMoveEvent = self.defaultMouseMove
            self.ImagePreview.mouseDoubleClickEvent = self.getPixel
            self.ImagePreview.mousePressEvent = self.defaultMousePress
            self.ImagePreview.mouseReleaseEvent = self.defaultMouseRelease
            self.statusbar.showMessage("select color using the mouse right button double click")
        elif command == 'cropArea':
            print(command)
            self.ImagePreview.mouseMoveEvent = self.defaultMouseMove
            self.ImagePreview.mouseDoubleClickEvent = self.defaultDoubleClick
            self.ImagePreview.mousePressEvent = self.startCropping
            self.ImagePreview.mouseReleaseEvent = self.stopCropping
            self.statusbar.showMessage("select the master pattern using the mouse right button")
        else:
            self.ImagePreview.mouseMoveEvent = self.defaultMouseMove
            self.ImagePreview.mouseDoubleClickEvent = self.defaultDoubleClick
            self.ImagePreview.mousePressEvent = self.defaultMousePress
            self.ImagePreview.mouseReleaseEvent = self.defaultMouseRelease

    def KeyboardEscapePressed(self, event):
        if event.key() == QtCore.Qt.Key_Escape:
            self.dragging = False

    def nextPressedOnce(self):
        self.ToolsListSetup.show()
        self.saveMasterImageButton.setEnabled(False)
        self.RetakeImageButton.setEnabled(False)
        self.SnapshotButton.setEnabled(False)
        self.NextStepButton.clicked.disconnect()
        self.NextStepButton.clicked.connect(self.nextPressedTwice)
        self.PreviousStepButton.clicked.disconnect()
        self.PreviousStepButton.clicked.connect(self.PreviousPressedOnce)

    def nextPressedTwice(self):
        self.saveSettings()
        self.setupWindow.close()
        print("Save settings")
        print(self.toolList)

    def PreviousPressedOnce(self):
        self.ToolsListSetup.hide()
        self.setImagePreview(self.frame)
        self.saveMasterImageButton.setEnabled(True)
        self.RetakeImageButton.setEnabled(True)
        self.SnapshotButton.setEnabled(True)
        self.NextStepButton.clicked.disconnect()
        self.NextStepButton.clicked.connect(self.nextPressedOnce)
        self.PreviousStepButton.clicked.disconnect()
        self.PreviousStepButton.clicked.connect(self.setupWindow.close)

    def saveSettings(self):

        for toolIndex in range(1, 5):
            tool = "Tool" + str(toolIndex) + "_Settings"
            self.config.set(tool, "tool name",str(self.toolList[toolIndex]))

            if self.toolList[toolIndex] == 'Color Pixel Tool' and self.ColorThresh[toolIndex].isEnabled():

                self.config.set(tool, "tool thresh", str(self.ColorThresh[toolIndex].value()))
                self.config.set(tool, "pixel color", str(self.pixelColor[toolIndex]))
                self.config.set(tool, "ignored pixels", "None")
                self.config.set(tool, "Result", str(self.Results[toolIndex]))

            elif self.toolList[toolIndex] == 'measurement Tool' and self.measurementThresh[toolIndex].isEnabled():

                self.config.set(tool, "tool thresh", str(self.measurementThresh[toolIndex].value()))
                self.config.set(tool, "pixel color", "None")
                self.config.set(tool, "ignored pixels", str(self.ignoredPixels[toolIndex]))
                self.config.set(tool, "Result", str(self.Results[toolIndex]))

            elif self.toolList[toolIndex] == 'Pattern Detection Tool' and self.patternThresh[toolIndex].isEnabled():

                self.config.set(tool, "tool thresh", str(self.patternThresh[toolIndex].value()))
                self.config.set(tool, "pixel color", "None")
                self.config.set(tool, "ignored pixels", "None")
                self.config.set(tool, "Result", str(self.Results[toolIndex]))

            else:
                self.config.set(tool, "tool thresh", str(0))
                self.config.set(tool, "pixel color", "None")
                self.config.set(tool, "ignored pixels", "None")
                self.config.set(tool, "tool name", "None")
                self.config.set(tool, "Result", "Tool"+str(toolIndex))

        with open('config/config'+str(self.captureManager.programNumber)+'.ini', 'w') as configfile:
            self.config.write(configfile)


class refreshFrameThread(QThread):

    def __init__(self, interface, window):
        super(refreshFrameThread, self).__init__()
        self.interface = interface
        self.window = window

    def run(self):
        while self.interface.capture:
            self.emit(QtCore.SIGNAL('refreshFrame()'))

            time.sleep(0.4)
