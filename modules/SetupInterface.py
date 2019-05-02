from modules.CaptureManager import CaptureManager


from GUI.setupWindow import *
from modules.CustomSlots import CustomSlots
from modules.ProcessingTools import ProcessingTools
from modules.ToolSettingsInterface import ToolSettingsInterface
from PyQt4.QtCore import QThread
import time



class SetupInterface(Ui_SetupWindow):
    def __init__(self, captureManager):
        super(SetupInterface, self).__init__()
        self.frame = None
        self.capture = True
        self.captureManager = captureManager
        self.ColorThresh=[None]*4
        self.setupWindow = CustomSlots(self)
        self.setupUi(self.setupWindow)
        self.setupWindow.show()
        self.refresher = refreshFrameThread(self, self.setupWindow)
        if self.captureManager.isMasterExist():
            self.frame = captureManager.loadFrame('./Masters/MasterImage'+str(self.captureManager.programNumber)+'.jpg')
            self.setImagePreview(self.frame)
        else:
            self.liveStream()
        QtCore.QObject.connect(self.refresher, QtCore.SIGNAL('refreshFrame()'), self.refreshFrame)
        self.ToolsListSetup.hide()

        QtCore.QObject.connect(self.ThreshSlider1, QtCore.SIGNAL("sliderPressed()"),
                               self.setToolIndex1)
        QtCore.QObject.connect(self.ThreshSlider2, QtCore.SIGNAL("sliderPressed()"),
                               self.setToolIndex2)
        QtCore.QObject.connect(self.ThreshSlider3, QtCore.SIGNAL("sliderPressed()"),
                               self.setToolIndex3)
        QtCore.QObject.connect(self.ThreshSlider4, QtCore.SIGNAL("sliderPressed()"),
                               self.setToolIndex4)

        self.processingTools = ProcessingTools()
        self.defaultDoubleClick=self.ImagePreview.mouseDoubleClickEvent
        self.defaultMousePress=self.ImagePreview.mousePressEvent
        self.defaultMouseRelease = self.ImagePreview.mouseReleaseEvent
        self.defaultMouseMove=self.ImagePreview.mouseMoveEvent

        self.ImagePreview.mouseDoubleClickEvent = self.DoNothing
        self.ImagePreview.mousePressEvent = self.DoNothing
        self.ImagePreview.mouseReleaseEvent = self.DoNothing
        self.ImagePreview.mouseMoveEvent = self.DoNothing


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
        self.capture=True
        self.refresher.start()

    def saveMaster(self):

        name = QtGui.QFileDialog.getSaveFileName(self.setupWindow, 'Save File', 'MasterImage' +
                                                 str(self.captureManager.getProgramNumber)+'.jpg')
        if name.endswith(('/.png', '/.jpg', '/.jpeg')):
            self.saveMaster()

        elif name.endswith(('.png', '.jpg', '.jpeg')):
            print(name)
            self.captureManager.saveImage(self.frame, name)

    def showToolSettings(self,ToolIndex):
        self.captureManager.toolIndex=ToolIndex

        self.toolSettingsUi = ToolSettingsInterface(self.captureManager,self)

    def setImagePreview(self,frame):
        temp = self.captureManager.makePixmap(frame)
        self.ImagePreview.setPixmap(QtGui.QPixmap(temp))

    def countColorPixels(self):
        self.enable('doubleClick')
        if self.captureManager.pixelColor[self.captureManager.toolIndex] is not None and \
                self.ColorThresh[self.captureManager.toolIndex] is not None and \
                self.ColorThresh[self.captureManager.toolIndex].isEnabled():
            pixels, frame = self.processingTools.countColorPixel(self.frame, self.captureManager.pixelColor[self.captureManager.toolIndex],
                                                                 int(self.ColorThresh[self.captureManager.toolIndex].value()))
            self.setImagePreview(frame)
            print(pixels)
        else:
            self.setImagePreview(self.frame)


    def getPixel(self, event):

        x = event.pos().x()
        y = event.pos().y()
        self.captureManager.pixelColor[self.captureManager.toolIndex] = self.frame[y, x]
        self.countColorPixels()

    def measureDistance(self):
        self.enable('removePixel')
        xdistance, ydistance, edgedMeasure = self.processingTools.measure(self.edged,self.measurementThresh.value(),True,True)
        self.setImagePreview(edgedMeasure)



    def startIgnoring(self, event):
        x = event.pos().x()
        y = event.pos().y()

        self.startPoint=x, y
        self.ImagePreview.mouseMoveEvent=self.drawIgnored

    def drawIgnored(self,event):
        x = event.pos().x()
        y = event.pos().y()
        edged=self.processingTools.gray2BGR(self.edged)
        self.captureManager.drawRectangle(edged, (x, y), self.startPoint, (0, 0, 255))
        self.setImagePreview(edged)


    def stopIgnoring(self, event):

        self.ImagePreview.mouseMoveEvent = self.defaultMouseMove
        x = event.pos().x()
        y = event.pos().y()

        if (x,y)==self.startPoint:
            x+=1
            y+=1

        self.edged = self.processingTools.ignoreEdge(self.edged, self.startPoint[0], self.startPoint[1],
                                                     (y-self.startPoint[1]), (x-self.startPoint[0]))
        edged=self.processingTools.gray2BGR(self.edged)
        self.captureManager.drawRectangle(edged,(x,y),self.startPoint,(0,0,255))
        self.setImagePreview(edged)


    def coloredPixel(self):

        self.setImagePreview(self.frame)
        if self.captureManager.toolIndex==1:
            self.ColorThresh[self.captureManager.toolIndex]=self.ThreshSlider1
            toolName=self.ToolName1
        elif self.captureManager.toolIndex==2:
            self.ColorThresh[self.captureManager.toolIndex]=self.ThreshSlider2
            toolName = self.ToolName2
        elif self.captureManager.toolIndex == 3:
            toolName = self.ToolName3
            self.ColorThresh[self.captureManager.toolIndex] = self.ThreshSlider3
        elif self.captureManager.toolIndex == 4:
            self.ColorThresh[self.captureManager.toolIndex] = self.ThreshSlider4
            toolName = self.ToolName4
        self.ColorThresh[self.captureManager.toolIndex].setMaximum(255)
        toolName.setText("Color Pixel Tool")
        QtCore.QObject.connect(self.ColorThresh[self.captureManager.toolIndex], QtCore.SIGNAL("valueChanged(int)"),
                               self.countColorPixels)
        QtCore.QObject.connect(self.ColorThresh[self.captureManager.toolIndex], QtCore.SIGNAL("sliderPressed()"),
                               self.countColorPixels)

        self.enable('doubleClick')

    def measurement(self):

        if self.captureManager.toolIndex==1:
            self.measurementThresh=self.ThreshSlider1
            toolName=self.ToolName1
        elif self.captureManager.toolIndex==2:
            self.measurementThresh=self.ThreshSlider2
            toolName = self.ToolName2
        elif self.captureManager.toolIndex == 3:
            toolName = self.ToolName3
            self.measurementThresh = self.ThreshSlider3
        elif self.captureManager.toolIndex == 4:
            self.measurementThresh = self.ThreshSlider4
            toolName = self.ToolName4
        toolName.setText("measurement Tool")
        self.measurementThresh.setMaximum(max(self.frame.shape))
        self.edged = self.processingTools.detectEdges(self.frame)


        self.setImagePreview(self.edged)
        QtCore.QObject.connect(self.measurementThresh, QtCore.SIGNAL("valueChanged(int)"),
                               self.measureDistance)
        QtCore.QObject.connect(self.measurementThresh, QtCore.SIGNAL("sliderPressed()"),
                               self.measureDistance)

        self.enable('removePixel')

    def enable(self,command):
        if command=='removePixel':
            self.ImagePreview.mouseDoubleClickEvent = self.defaultDoubleClick
            self.ImagePreview.mousePressEvent = self.startIgnoring
            self.ImagePreview.mouseReleaseEvent = self.stopIgnoring
        elif command=='doubleClick':
            self.ImagePreview.mouseDoubleClickEvent = self.getPixel
            self.ImagePreview.mousePressEvent = self.defaultMousePress
            self.ImagePreview.mouseReleaseEvent = self.defaultMouseRelease
        else:
            self.ImagePreview.mouseDoubleClickEvent = self.defaultDoubleClick
            self.ImagePreview.mousePressEvent = self.defaultMousePress
            self.ImagePreview.mouseReleaseEvent = self.defaultMouseRelease




class refreshFrameThread(QThread):

    def __init__(self, interface, window):
        super(refreshFrameThread, self).__init__()
        self.interface=interface
        self.window=window

    def run(self):

        while self.interface.capture:
            self.emit(QtCore.SIGNAL('refreshFrame()'))

            time.sleep(0.4)


