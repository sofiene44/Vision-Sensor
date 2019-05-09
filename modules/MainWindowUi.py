

from GUI.mainFrameWindow import *
from modules.CaptureManager import CaptureManager
from modules.ToolSettingsInterface import ToolSettingsInterface
from modules.SetupInterface import SetupInterface
from configparser import ConfigParser
from modules.CustomSlots import CustomSlots
import ast


class MainWindowUi(Ui_MainWindow):

    # Initialise the class to default values ; default camera index corresponds to the computer's default camera

    def __init__(self, captureManager):
        super(MainWindowUi, self).__init__()
        self.MainWindow = CustomSlots(self)
        self.setupUi(self.MainWindow)
        self.MainWindow.show()
        self.frame=None
        self.captureManager = captureManager
        self.config=ConfigParser()

        self.ColorThresh = [None] * 5
        self.pixelColor = [None] * 5
        self.measurementThresh = [None] * 5
        self.patternThresh = [None] * 5
        self.toolList = [None] * 5
        self.ignoredPixels = [None] * 5
        self.Results = [None] * 5

        self.loadConfig()



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


    def showSetup(self):
        self.SetupInterface = SetupInterface(self.captureManager)

    def loadConfig(self):
        self.config.read('config/config' + str(self.captureManager.programNumber) + '.ini')

        self.pixelColor=[None] * 5
        self.Results=[None] * 5
        self.ignoredPixels=[None] * 5

        self.ToolName1.setText(self.config.get("Tool1_Settings", "tool name"))
        self.ToolName2.setText(self.config.get("Tool2_Settings", "tool name"))
        self.ToolName3.setText(self.config.get("Tool3_Settings", "tool name"))
        self.ToolName4.setText(self.config.get("Tool4_Settings", "tool name"))

        if self.config.get("Tool1_Settings", "tool name") == 'Tool1':
            self.Enable1.setChecked(False)
            self.Enable1.setCheckable(False)

        else:
            self.Enable1.setCheckable(True)
            self.Enable1.setChecked(True)

        if self.config.get("Tool2_Settings", "tool name") == 'Tool2':
            self.Enable2.setChecked(False)
            self.Enable2.setCheckable(False)

        else:
            self.Enable2.setCheckable(True)
            self.Enable2.setChecked(True)

        if self.config.get("Tool3_Settings", "tool name") == 'Tool3':
            self.Enable3.setChecked(False)
            self.Enable3.setCheckable(False)

        else:
            self.Enable3.setCheckable(True)
            self.Enable3.setChecked(True)

        if self.config.get("Tool4_Settings", "tool name") == 'Tool4':
            self.Enable4.setChecked(False)
            self.Enable4.setCheckable(False)

        else:
            self.Enable4.setCheckable(True)
            self.Enable4.setChecked(True)

        for toolIndex in range(1, 5):
            tool="Tool"+str(toolIndex)+"_Settings"
            if self.config.get(tool,"tool name") == 'Color Pixel Tool':
                pixelColor = self.config.get(tool,"pixel color")
                self.pixelColor[toolIndex] = [int(e.strip('[]')) for e in pixelColor.split(' ')]
                self.Results[toolIndex] = int(self.config.get(tool, "result"))

            elif self.config.get(tool, "tool name") == 'measurement Tool':
                self.ignoredPixels[toolIndex]=ast.literal_eval(self.config.get(tool, "ignored pixels"))
                self.Results[toolIndex] = ast.literal_eval(self.config.get(tool, "result"))

            elif self.config.get(tool, "tool name") == 'Pattern Detection Tool':

                self.Results[toolIndex] = int(self.config.get(tool, "result"))





