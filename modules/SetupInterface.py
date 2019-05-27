from modules.CaptureManager import CaptureManager

from configparser import ConfigParser
import ast
from cv2 import findNonZero

from GUI.setupWindow import *
from modules.CustomSlots import CustomSlots
from modules.ProcessingTools import ProcessingTools
from modules.ToolSettingsInterface import ToolSettingsInterface
from PyQt4.QtCore import QThread
import time


class SetupInterface(Ui_SetupWindow):
    def __init__(self, captureManager):
        super(SetupInterface, self).__init__()
        self.measurePoints = ((0, 0), (0, 0))
        self.config = ConfigParser()
        self.frame = None
        self.capture = True
        self.captureManager = captureManager
        self.edged = [None] * 5
        self.edgedPos = [None] * 5
        self.mixedFrame = [None] * 5
        self.firstMeasurePoint = (0, 0)
        self.secondMeasurePoint = (0, 0)
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
        self.config.read('config/config' + str(self.captureManager.programNumber) + '.ini')
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

        self.cropped = self.frame
        self.loadConfig()
        self.setImagePreview(self.frame)
        self.statusbar.showMessage("")

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
                self.captureManager.toolIndex], int(self.ColorThresh[self.captureManager.toolIndex].value()))

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
        self.stopCropping()
        self.setImagePreview(self.frame)
        self.enable('cropArea')
        # xdistance, ydistance, edgedMeasure = self.processingTools.measure(
        #     self.edged[self.captureManager.toolIndex], self.measurementThresh[self.captureManager.toolIndex].value(),
        #     True, True)
        if self.mixedFrame[self.captureManager.toolIndex] is None:
            return

        xdistance = abs(self.firstMeasurePoint[0] - self.secondMeasurePoint[0])
        ydistance = abs(self.firstMeasurePoint[1] - self.secondMeasurePoint[1])
        distance = (xdistance ** 2 + ydistance ** 2) ** (1 / 2)
        print(xdistance, ydistance, distance)

        frame = self.mixedFrame[self.captureManager.toolIndex].copy()
        self.captureManager.drawArrow(frame, self.firstMeasurePoint, self.secondMeasurePoint)
        self.captureManager.drawArrow(frame, self.firstMeasurePoint,
                                      (self.secondMeasurePoint[0], self.firstMeasurePoint[1]), (0, 0, 255))
        self.captureManager.drawArrow(frame, self.secondMeasurePoint,
                                      (self.secondMeasurePoint[0], self.firstMeasurePoint[1]), (0, 255, 0))

        # frame=self.processingTools.replacePartFrame(self.frame,self.edged[self.captureManager.toolIndex], self.edgedPos[self.captureManager.toolIndex][0][0],self.edgedPos[self.captureManager.toolIndex][0][1])
        # frame=self.processingTools.replacePartFrame(self.frame,edgedMeasure, self.edgedPos[self.captureManager.toolIndex][0][0],self.edgedPos[self.captureManager.toolIndex][0][1])
        self.setImagePreview(frame)
        self.Results[self.captureManager.toolIndex] = (xdistance, ydistance, distance)

    def detectPattern(self):
        if self.masterPattern is None:
            self.statusbar.showMessage("no reference found please select a new reference")
            self.enable('selectPattern')
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
            self.dragging = False

        if self.dragging:
            self.edged[self.captureManager.toolIndex] = self.processingTools.ignoreEdge(
                self.edged[self.captureManager.toolIndex], self.startPoint[0], self.startPoint[1],
                (y - self.startPoint[1]), (x - self.startPoint[0]))
            edged = self.processingTools.gray2BGR(self.edged[self.captureManager.toolIndex])
            self.captureManager.drawRectangle(edged, (x, y), self.startPoint, (0, 0, 255))
            self.ignoredPixels[self.captureManager.toolIndex].append([(x, y), self.startPoint])


        else:
            edged = self.edged[self.captureManager.toolIndex]
        self.setImagePreview(edged)

    def startSelectingPattern(self, event):
        x = event.pos().x()
        y = event.pos().y()
        self.dragging = True
        self.startPoint = x, y
        self.ImagePreview.mouseMoveEvent = self.drawSelection

    def drawSelection(self, event):
        x = event.pos().x()
        y = event.pos().y()
        self.setupWindow.keyPressEvent = self.KeyboardEscapePressed
        if self.dragging:
            frame = self.frame.copy()
            self.captureManager.drawRectangle(frame, (x, y), self.startPoint, (0, 0, 255))
            self.setImagePreview(frame)
        else:
            self.setImagePreview(self.frame)

    def stopSelectingPattern(self, event):

        self.ImagePreview.mouseMoveEvent = self.defaultMouseMove
        x = event.pos().x()
        y = event.pos().y()
        frame = self.frame.copy()
        if (x, y) == self.startPoint:
            return
        if self.dragging:
            self.masterPattern = self.processingTools.cropFrame(self.frame, self.startPoint[0], self.startPoint[1],
                                                                (y - self.startPoint[1]), (x - self.startPoint[0]))
            self.captureManager.drawRectangle(frame, (x, y), self.startPoint, (0, 0, 255))
            name = QtGui.QFileDialog.getSaveFileName(self.setupWindow, 'Save File', 'MasterPattern' +
                                                     str(self.captureManager.getProgramNumber) + '.jpg')

            if name.endswith(('.png', '.jpg', '.jpeg')):
                print(name)
                self.captureManager.saveImage(self.masterPattern, name)
        self.setImagePreview(self.frame)

    def startCropping(self, event=None):

        if self.edgedPos[self.captureManager.toolIndex] is not None and event is None:
            self.enable('measure')
            (self.firstMeasurePoint, self.secondMeasurePoint) = self.measurePoints
            self.startPoint = self.edgedPos[self.captureManager.toolIndex][0]
            self.dragging = True
            self.stopCropping()
            return

        if event is None:
            return

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

    def stopCropping(self, event=None):

        self.ImagePreview.mouseMoveEvent = self.defaultMouseMove
        if event is not None:
            x = event.pos().x()
            y = event.pos().y()
        else:
            x = self.edgedPos[self.captureManager.toolIndex][1][0]
            y = self.edgedPos[self.captureManager.toolIndex][1][1]

        frame = self.frame.copy()

        if (x, y) == self.startPoint:
            return
        if self.dragging:
            self.cropped = self.processingTools.cropFrame(self.frame, self.startPoint[0], self.startPoint[1],
                                                          (y - self.startPoint[1]), (x - self.startPoint[0]))

            # self.captureManager.drawRectangle(frame, (x, y), self.startPoint, (0, 0, 255))
            if self.measurementThresh[self.captureManager.toolIndex] is not None:
                self.measurementThreshValue[self.captureManager.toolIndex] = self.measurementThresh[self.captureManager.toolIndex].value()
                print(self.measurementThreshValue[self.captureManager.toolIndex])



            self.edged[self.captureManager.toolIndex] = self.processingTools.detectEdges(self.cropped,self.measurementThreshValue[self.captureManager.toolIndex]/100)
            print(self.measurementThreshValue[self.captureManager.toolIndex]/100)
            edged3ch = self.processingTools.gray2BGR(self.edged[self.captureManager.toolIndex])
            self.mixedFrame[self.captureManager.toolIndex] = self.processingTools.replacePartFrame(frame, edged3ch,
                                                                                                   min(x,
                                                                                                       self.startPoint[
                                                                                                           0]), min(y,
                                                                                                                    self.startPoint[
                                                                                                                        1]))
            self.edgedPos[self.captureManager.toolIndex] = ((min(x, self.startPoint[0]), min(y, self.startPoint[1])),
                                                            (max(x, self.startPoint[0]), max(y, self.startPoint[1])))
            frame = self.mixedFrame[self.captureManager.toolIndex]
            self.enable('measure')

            if findNonZero(self.edged[self.captureManager.toolIndex]) is None:
                self.resetCrop()
                return

        self.setImagePreview(frame)

    def selectMeasurePointFirst(self, event):

        x = event.pos().x()
        y = event.pos().y()

        if x < self.edgedPos[self.captureManager.toolIndex][0][0] or x > \
                self.edgedPos[self.captureManager.toolIndex][1][0] or y < \
                self.edgedPos[self.captureManager.toolIndex][0][1] or y > \
                self.edgedPos[self.captureManager.toolIndex][1][1]:
            self.dragging = False
            self.enable('measure')
            return

        # add approximation function
        xedged = x - self.edgedPos[self.captureManager.toolIndex][0][0]
        yedged = y - self.edgedPos[self.captureManager.toolIndex][0][1]
        xedged, yedged = self.processingTools.getNearestPos(self.edged[self.captureManager.toolIndex], (xedged, yedged))

        x = xedged + self.edgedPos[self.captureManager.toolIndex][0][0]
        y = yedged + self.edgedPos[self.captureManager.toolIndex][0][1]

        self.dragging = True
        self.firstMeasurePoint = (x, y)

        self.ImagePreview.mouseMoveEvent = self.drawArrow
        self.ImagePreview.mousePressEvent = self.selectMeasurePointSecond

    def drawArrow(self, event):

        self.statusbar.showMessage("select the second point of measurement")
        x = event.pos().x()
        y = event.pos().y()

        self.setupWindow.keyPressEvent = self.KeyboardEscapePressed
        if self.dragging:
            frame = self.mixedFrame[self.captureManager.toolIndex].copy()
            self.captureManager.drawArrow(frame, self.firstMeasurePoint, (x, y))
            self.setImagePreview(frame)
        else:
            self.setImagePreview(self.mixedFrame[self.captureManager.toolIndex])

    def selectMeasurePointSecond(self, event=None):
        if event is not None:
            x = event.pos().x()
            y = event.pos().y()
        else:
            x=self.secondMeasurePoint[0]
            y=self.secondMeasurePoint[1]
        if x < self.edgedPos[self.captureManager.toolIndex][0][0] or x > \
                self.edgedPos[self.captureManager.toolIndex][1][0] or y < \
                self.edgedPos[self.captureManager.toolIndex][0][1] or y > \
                self.edgedPos[self.captureManager.toolIndex][1][1]:
            return

        # add approximation function
        xedged = x - self.edgedPos[self.captureManager.toolIndex][0][0]
        yedged = y - self.edgedPos[self.captureManager.toolIndex][0][1]
        xedged, yedged = self.processingTools.getNearestPos(self.edged[self.captureManager.toolIndex], (xedged, yedged))
        x = xedged + self.edgedPos[self.captureManager.toolIndex][0][0]
        y = yedged + self.edgedPos[self.captureManager.toolIndex][0][1]

        self.secondMeasurePoint = (x, y)
        frame = self.mixedFrame[self.captureManager.toolIndex].copy()
        self.captureManager.drawArrow(frame, self.firstMeasurePoint, (x, y))
        self.setImagePreview(frame)
        self.measureDistance()
        self.enable('measure')

    def resetCrop(self, event=None):
        print("reset")
        self.edgedPos[self.captureManager.toolIndex] = None
        self.setImagePreview(self.frame)
        self.measurement()

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
        self.toolList[self.captureManager.toolIndex] = "Color Pixel Tool"
        QtCore.QObject.connect(self.ColorThresh[self.captureManager.toolIndex], QtCore.SIGNAL("valueChanged(int)"),
                               self.countColorPixels)
        QtCore.QObject.connect(self.ColorThresh[self.captureManager.toolIndex], QtCore.SIGNAL("sliderPressed()"),
                               self.countColorPixels)

        self.enable('doubleClick')

    def measurement(self):

        self.enable('cropArea')
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
        self.ignoredPixels[self.captureManager.toolIndex] = []
        self.toolList[self.captureManager.toolIndex] = "measurement Tool"
        self.measurementThresh[self.captureManager.toolIndex].setMaximum(100)

        self.setImagePreview(self.frame)
        QtCore.QObject.connect(self.measurementThresh[self.captureManager.toolIndex],
                               QtCore.SIGNAL("valueChanged(int)"),
                               self.measureDistance)
        QtCore.QObject.connect(self.measurementThresh[self.captureManager.toolIndex], QtCore.SIGNAL("sliderPressed()"),
                               self.measureDistance)

        # self.enable('removePixel')

    def patternDetection(self):
        self.statusbar.showMessage("")

        try:
            self.masterPattern = self.captureManager.loadFrame('./Masters/MasterPattern' +
                                                               str(self.captureManager.programNumber) + '.jpg')
        except Exception:
            pass
        if self.masterPattern is None:
            self.statusbar.showMessage("no reference found please select a new reference")
            self.enable('selectPattern')

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
            toolName = None
        self.patternThresh[self.captureManager.toolIndex].setMaximum(100)
        toolName.setText("Pattern Detection Tool")
        self.toolList[self.captureManager.toolIndex] = "Pattern Detection Tool"
        self.detectPattern()
        QtCore.QObject.connect(self.patternThresh[self.captureManager.toolIndex], QtCore.SIGNAL("valueChanged(int)"),
                               self.detectPattern)
        QtCore.QObject.connect(self.patternThresh[self.captureManager.toolIndex], QtCore.SIGNAL("sliderPressed()"),
                               self.detectPattern)

    def enable(self, command=''):
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
        elif command == 'selectPattern':

            self.ImagePreview.mouseMoveEvent = self.defaultMouseMove
            self.ImagePreview.mouseDoubleClickEvent = self.defaultDoubleClick
            self.ImagePreview.mousePressEvent = self.startSelectingPattern
            self.ImagePreview.mouseReleaseEvent = self.stopSelectingPattern
            self.statusbar.showMessage("select the master pattern using the mouse right button")

        elif command == 'cropArea':

            self.ImagePreview.mouseMoveEvent = self.defaultMouseMove
            self.ImagePreview.mouseDoubleClickEvent = self.defaultDoubleClick
            self.ImagePreview.mousePressEvent = self.startCropping
            self.ImagePreview.mouseReleaseEvent = self.stopCropping
            self.statusbar.showMessage("select the area of interest using the mouse right button")

        elif command == 'measure':

            self.ImagePreview.mouseMoveEvent = self.defaultMouseMove
            self.ImagePreview.mouseDoubleClickEvent = self.resetCrop
            self.ImagePreview.mousePressEvent = self.selectMeasurePointFirst
            self.ImagePreview.mouseReleaseEvent = self.defaultMouseRelease
            self.statusbar.showMessage("select the first point of measurement")

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
            self.config.set(tool, "tool name", str(self.toolList[toolIndex]))

            if self.toolList[toolIndex] == 'Color Pixel Tool' and self.ColorThresh[toolIndex].isEnabled():

                self.config.set(tool, "tool thresh", str(self.ColorThresh[toolIndex].value()))
                self.config.set(tool, "pixel color", str(self.pixelColor[toolIndex]))
                self.config.set(tool, "area of interest", "None")
                self.config.set(tool, "measurement points", str(None))
                self.config.set(tool, "Result", str(self.Results[toolIndex]))

            elif self.toolList[toolIndex] == 'measurement Tool' and self.measurementThresh[toolIndex].isEnabled():

                self.config.set(tool, "tool thresh", str(self.measurementThresh[toolIndex].value()))
                self.config.set(tool, "pixel color", "None")
                self.config.set(tool, "area of interest", str(self.edgedPos[toolIndex]))
                self.config.set(tool, "measurement points", str((self.firstMeasurePoint, self.secondMeasurePoint)))
                self.config.set(tool, "Result", str(self.Results[toolIndex]))

            elif self.toolList[toolIndex] == 'Pattern Detection Tool' and self.patternThresh[toolIndex].isEnabled():

                self.config.set(tool, "tool thresh", str(self.patternThresh[toolIndex].value()))
                self.config.set(tool, "pixel color", "None")
                self.config.set(tool, "area of interest", "None")
                self.config.set(tool, "measurement points", str(None))
                self.config.set(tool, "Result", str(self.Results[toolIndex]))

            else:
                self.config.set(tool, "tool name", 'Tool' + str(toolIndex))
                self.config.set(tool, "tool thresh", str(0))
                self.config.set(tool, "pixel color", "None")
                self.config.set(tool, "area of interest", "None")
                self.config.set(tool, "measurement points", str(None))
                self.config.set(tool, "Result", "None")

        with open('config/config' + str(self.captureManager.programNumber) + '.ini', 'w') as configfile:
            self.config.write(configfile)

    def loadConfig(self):
        self.config.read('config/config' + str(self.captureManager.programNumber) + '.ini')

        self.pixelColor = [None] * 5
        self.ColorThreshValue = [None] * 5
        self.measurementThreshValue = [None] * 5
        self.patternThreshValue = [None] * 5
        self.toolList = [None] * 5
        self.ignoredPixels = [None] * 5
        self.Results = [None] * 5

        self.ToolName1.setText(self.config.get("Tool1_Settings", "tool name"))
        self.ToolName2.setText(self.config.get("Tool2_Settings", "tool name"))
        self.ToolName3.setText(self.config.get("Tool3_Settings", "tool name"))
        self.ToolName4.setText(self.config.get("Tool4_Settings", "tool name"))

        if self.config.get("Tool1_Settings", "tool name") == 'Tool1':
            self.Enable1.setChecked(False)

        else:
            self.Enable1.setChecked(True)
            self.ThreshSlider1.setValue(int(self.config.get("Tool1_Settings", "tool thresh")))

        if self.config.get("Tool2_Settings", "tool name") == 'Tool2':
            self.Enable2.setChecked(False)

        else:
            self.Enable2.setChecked(True)
            self.ThreshSlider2.setValue(int(self.config.get("Tool2_Settings", "tool thresh")))

        if self.config.get("Tool3_Settings", "tool name") == 'Tool3':
            self.Enable3.setChecked(False)

        else:
            self.Enable3.setChecked(True)
            self.ThreshSlider3.setValue(int(self.config.get("Tool3_Settings", "tool thresh")))

        if self.config.get("Tool4_Settings", "tool name") == 'Tool4':
            self.Enable4.setChecked(False)

        else:
            self.Enable4.setChecked(True)
            self.ThreshSlider4.setValue(int(self.config.get("Tool4_Settings", "tool thresh")))

        for toolIndex in range(1, 5):
            tool = "Tool" + str(toolIndex) + "_Settings"
            if self.config.get(tool, "tool name") == 'Color Pixel Tool':
                pixelColor = self.config.get(tool, "pixel color")
                self.pixelColor[toolIndex] = [int(e.strip('[],')) for e in pixelColor.split(' ')]
                self.Results[toolIndex] = int(self.config.get(tool, "result"))
                self.ColorThreshValue[toolIndex] = int(self.config.get(tool, 'tool thresh'))
                self.captureManager.toolIndex = toolIndex
                self.coloredPixel()

            elif self.config.get(tool, "tool name") == 'measurement Tool':
                self.edgedPos[toolIndex] = ast.literal_eval(self.config.get(tool, "area of interest"))
                self.measurePoints = ast.literal_eval(self.config.get(tool, "measurement points"))
                self.Results[toolIndex] = ast.literal_eval(self.config.get(tool, "result"))
                self.measurementThreshValue[toolIndex] = int(self.config.get(tool, 'tool thresh'))
                self.captureManager.toolIndex = toolIndex
                self.startCropping()
                self.measurement()

            elif self.config.get(tool, "tool name") == 'Pattern Detection Tool':
                self.patternThreshValue[toolIndex] = int(self.config.get(tool, 'tool thresh'))
                self.Results[toolIndex] = int(self.config.get(tool, "result"))
                self.captureManager.toolIndex = toolIndex
                self.patternDetection()


class refreshFrameThread(QThread):

    def __init__(self, interface, window):
        super(refreshFrameThread, self).__init__()
        self.interface = interface
        self.window = window

    def run(self):
        while self.interface.capture:
            self.emit(QtCore.SIGNAL('refreshFrame()'))

            time.sleep(0.4)
