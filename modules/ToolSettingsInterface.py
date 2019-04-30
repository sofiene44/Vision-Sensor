
from GUI.toolSettingsWindow import *
from modules.CustomSlots import CustomSlots
from modules.CaptureManager import CaptureManager


class ToolSettingsInterface(Ui_ToolSettingsWindow):

    def __init__(self, captureManager,parent):

        super(ToolSettingsInterface, self).__init__()
        self.toolIndex = captureManager.toolIndex
        self.captureManager = captureManager
        self.parent=parent
        self.frame=self.captureManager.loadFrame("Masters/MasterImage"+str(captureManager.programNumber)+".jpg")
        self.toolSettingsWindow = CustomSlots(self)
        self.setupUi(self.toolSettingsWindow)
        self.toolSettingsWindow.show()

    def ColorePixelSelected(self):

        print("ColorPixel")

        self.parent.coloredPixel()

    def measurementSelected(self):

        print("measurement")
        self.parent.measurement()

    def patternDetectionSelected(self):

        print("patternDetection")
        self.parent.patternDetection()
