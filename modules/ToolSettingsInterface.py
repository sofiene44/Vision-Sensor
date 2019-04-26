
from GUI.toolSettingsWindow import *
from modules.CustomSlots import CustomSlots


class ToolSettingsInterface(Ui_ToolSettingsWindow):

    def __init__(self):
        super(ToolSettingsInterface, self).__init__()
        self.frame=None
        self.toolSettingsWindow = CustomSlots(self)
        self.setupUi(self.toolSettingsWindow)
        self.toolSettingsWindow.show()

    def ColorePixelSelected(self):

        print("ColorPixel")

    def measurementSelected(self):
        print("measurement")

    def patternDetectionSelected(self):
        print("patternDetection")
