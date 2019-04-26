

from GUI.mainFrameWindow import *
from modules.CaptureManager import CaptureManager
from modules.ToolSettingsInterface import ToolSettingsInterface
from modules.SetupInterface import SetupInterface


class MainWindowUi(Ui_MainWindow):

    # Initialise the class to default values ; default camera index corresponds to the computer's default camera

    def __init__(self, captureManager=CaptureManager(0)):
        super(MainWindowUi, self).__init__()
        self.frame=None
        self.MainWindow = None
        self.captureManager = captureManager
        self.captureManager.setActiveWindow("MainWindow")

    # load an existing frame, takes Frame path as argument,default frame is replaced by the read frame

    def refreshFrame(self):
        self.captureManager.setCamera()
        self.frame = self.captureManager.readFrame()
        self.showFrame(self.frame)
        self.captureManager.cameraRelease()

    # show frame in specific window ,default frame and window name are shown if not specified
    def showFrame(self, frame):
        temp = self.captureManager.makePixmap(frame)
        self.ImagePreview.setPixmap(QtGui.QPixmap(temp))



    def showToolSettings(self):

        self.toolSettingsUi = ToolSettingsInterface()


    def showSetup(self):
        self.setupUi = SetupInterface()
