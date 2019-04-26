
from GUI.setupWindow import *
from modules.CustomSlots import CustomSlots
from modules.CaptureManager import CaptureManager
from PyQt4.QtCore import QThread
import time


class SetupInterface(Ui_SetupWindow):
    def __init__(self, captureManager=CaptureManager(0)):
        super(SetupInterface, self).__init__()
        self.frame=None
        self.capture = True
        self.captureManager = captureManager
        self.setupWindow = CustomSlots(self)
        self.setupUi(self.setupWindow)
        self.setupWindow.show()
        self.refresher = refreshFrameThread(self, self.setupWindow)
        self.liveStream()
        QtCore.QObject.connect(self.refresher, QtCore.SIGNAL('refreshFrame()'), self.refreshFrame)

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



class refreshFrameThread(QThread):

    def __init__(self,interface,window):
        super(refreshFrameThread, self).__init__()
        self.interface=interface
        self.window=window

    def run(self):

        while self.interface.capture:
            self.emit(QtCore.SIGNAL('refreshFrame()'))
            print("sent")
            time.sleep(0.4)
        print("end send")

