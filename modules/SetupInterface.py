
from GUI.setupWindow import *
from modules.CustomSlots import CustomSlots
from modules.CaptureManager import CaptureManager
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
        self.ColorThresh=None
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

        self.processingTools=ProcessingTools()



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

        name = QtGui.QFileDialog.getSaveFileName(self.setupWindow, 'Save File', 'MasterImage'+str(self.captureManager.getProgramNumber)+'.jpg')
        if name.endswith(('/.png', '/.jpg', '/.jpeg')):
            self.saveMaster()

        elif name.endswith(('.png', '.jpg', '.jpeg')):
            print(name)
            self.captureManager.saveImage(self.frame, name)

    def showToolSettings(self,ToolIndex):
        self.captureManager.toolIndex=ToolIndex
        if ToolIndex == 1:
            self.toolSettingsUi1 = ToolSettingsInterface(self.captureManager,self)

        elif ToolIndex == 2:
            self.toolSettingsUi2 = ToolSettingsInterface(self.captureManager,self)

        elif ToolIndex == 3:
            self.toolSettingsUi3 = ToolSettingsInterface(self.captureManager,self)

        elif ToolIndex == 4:
            self.toolSettingsUi4 = ToolSettingsInterface(self.captureManager,self)

    def setImagePreview(self,frame):
        temp = self.captureManager.makePixmap(frame)
        self.ImagePreview.setPixmap(QtGui.QPixmap(temp))

    def countColorPixels(self):

        if self.captureManager.pixelColor is not None and self.ColorThresh is not None:
            pixels, frame = self.processingTools.countColorPixel(self.frame, self.captureManager.pixelColor,
                                                                 int(self.ColorThresh.value()))
            self.setImagePreview(frame)
            print(pixels)

    def getPixel(self, event):

        x = event.pos().x()
        y = event.pos().y()
        self.captureManager.pixelColor = self.frame[y, x]
        self.countColorPixels()


    def coloredPixel(self):
        self.ImagePreview.mouseDoubleClickEvent = self.getPixel

        if self.captureManager.toolIndex==1:
            self.ColorThresh=self.ThreshSlider1
            toolName=self.ToolName1
        elif self.captureManager.toolIndex==2:
            self.ColorThresh=self.ThreshSlider2
            toolName = self.ToolName2
        elif self.captureManager.toolIndex == 3:
            toolName = self.ToolName3
            self.ColorThresh = self.ThreshSlider3
        elif self.captureManager.toolIndex == 4:
            self.ColorThresh = self.ThreshSlider4
            toolName = self.ToolName4
        self.ColorThresh.setMaximum(255)
        toolName.setText("Color Pixel Tool")
        # self.ColorThresh.connect()
        QtCore.QObject.connect(self.ColorThresh, QtCore.SIGNAL("valueChanged(int)"),
                               self.countColorPixels)









class refreshFrameThread(QThread):

    def __init__(self, interface, window):
        super(refreshFrameThread, self).__init__()
        self.interface=interface
        self.window=window

    def run(self):

        while self.interface.capture:
            self.emit(QtCore.SIGNAL('refreshFrame()'))

            time.sleep(0.4)


