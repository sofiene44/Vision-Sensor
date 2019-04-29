
from GUI.setupWindow import *
from modules.CustomSlots import CustomSlots
from modules.CaptureManager import CaptureManager
from modules.ToolSettingsInterface import ToolSettingsInterface
from PyQt4.QtCore import QThread
import time


class SetupInterface(Ui_SetupWindow):
    def __init__(self, captureManager=CaptureManager(0)):
        super(SetupInterface, self).__init__()
        self.frame = None
        self.capture = True
        self.captureManager = captureManager
        self.setupWindow = CustomSlots(self)
        self.setupUi(self.setupWindow)
        self.setupWindow.show()
        self.refresher = refreshFrameThread(self, self.setupWindow)
        self.liveStream()
        QtCore.QObject.connect(self.refresher, QtCore.SIGNAL('refreshFrame()'), self.refreshFrame)
        self.ToolsListSetup.hide()

    def refreshFrame(self):
        if self.setupWindow.isVisible():
            print("refresh")
            self.captureManager.setCamera(0)
            self.frame = self.captureManager.readFrame()
            temp = self.captureManager.makePixmap(self.frame)
            self.ImagePreview.setPixmap(QtGui.QPixmap(temp))
            self.captureManager.cameraRelease()
        else:
            self.capture = False

    def liveStream(self):
        self.capture=True
        self.refresher.start()
        print("start")

    def saveMaster(self):

        name = QtGui.QFileDialog.getSaveFileName(self.setupWindow, 'Save File', 'Master.jpg')
        if name.endswith(('/.png', '/.jpg', '/.jpeg')):
            self.saveMaster()

        elif name.endswith(('.png', '.jpg', '.jpeg')):
            print(name)
            self.captureManager.saveImage(self.frame, name)

    def showToolSettings(self,ToolIndex):

        if ToolIndex == 1:
            self.toolSettingsUi1 = ToolSettingsInterface()

        elif ToolIndex == 2:
            self.toolSettingsUi2 = ToolSettingsInterface()

        elif ToolIndex == 3:
            self.toolSettingsUi3 = ToolSettingsInterface()

        elif ToolIndex == 4:
            self.toolSettingsUi4 = ToolSettingsInterface()

class refreshFrameThread(QThread):

    def __init__(self, interface, window):
        super(refreshFrameThread, self).__init__()
        self.interface=interface
        self.window=window

    def run(self):

        while self.interface.capture:
            self.emit(QtCore.SIGNAL('refreshFrame()'))
            print("sent")
            time.sleep(0.4)
        print("end send")

