

from GUI.mainFrameWindow import *
from modules.CaptureManager import CaptureManager
from modules.ToolSettingsInterface import ToolSettingsInterface
from modules.SetupInterface import SetupInterface
from configparser import ConfigParser
from modules.CustomSlots import CustomSlots
from modules.ProcessingTools import ProcessingTools
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
        self.processingTools = ProcessingTools()

        self.threshValue = [None] * 5
        self.ColorThresh = [None] * 5
        self.pixelColor = [None] * 5
        self.measurementThresh = [None] * 5
        self.patternThresh = [None] * 5
        self.toolList = [None] * 5
        self.ignoredPixels = [None] * 5
        self.Results = [None] * 5
        self.NewResults = [None] * 5
        self.edged = [None] * 5

        self.loadConfig()
        self.captureManager.toolIndex = None

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

    def setToolIndex1(self):
        self.captureManager.toolIndex = 1

    def setToolIndex2(self):
        self.captureManager.toolIndex = 2

    def setToolIndex3(self):
        self.captureManager.toolIndex = 3

    def setToolIndex4(self):
        self.captureManager.toolIndex = 4






    # load an existing frame, takes Frame path as argument,default frame is replaced by the read frame

    def refreshFrame(self):

        self.captureManager.setCamera()
        self.frame = self.captureManager.readFrame()
        self.setImagePreview(self.frame)
        self.captureManager.cameraRelease()
        if self.captureManager.toolIndex is None:
            return
        if self.config.get("Tool"+str(self.captureManager.toolIndex)+"_Settings", "tool name") == 'Color Pixel Tool':
            self.coloredPixel()

        elif self.config.get("Tool"+str(self.captureManager.toolIndex)+"_Settings", "tool name") == 'measurement Tool':
            self.measurement()

        elif self.config.get("Tool"+str(self.captureManager.toolIndex)+"_Settings", "tool name") == 'Pattern Detection Tool':
            self.patternDetection()


    # show frame in specific window ,default frame and window name are shown if not specified
    def setImagePreview(self, frame):
        temp = self.captureManager.makePixmap(frame)
        self.ImagePreview.setPixmap(QtGui.QPixmap(temp))



    def showSetup(self):
        self.SetupInterface = SetupInterface(self.captureManager)

    def loadConfig(self):
        self.config.read('config/config' + str(self.captureManager.programNumber) + '.ini')

        self.threshValue=[None] * 5
        self.ColorThresh = [None] * 5
        self.pixelColor = [None] * 5
        self.measurementThresh = [None] * 5
        self.patternThresh = [None] * 5
        self.toolList = [None] * 5
        self.ignoredPixels = [None] * 5
        self.Results = [None] * 5

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
                self.pixelColor[toolIndex] = [int(e.strip('[],')) for e in pixelColor.split(' ')]
                self.Results[toolIndex] = int(self.config.get(tool, "result"))
                self.threshValue[toolIndex]=int(self.config.get(tool, 'tool thresh'))

            elif self.config.get(tool, "tool name") == 'measurement Tool':
                self.ignoredPixels[toolIndex]=ast.literal_eval(self.config.get(tool, "ignored pixels"))
                self.Results[toolIndex] = ast.literal_eval(self.config.get(tool, "result"))
                self.threshValue[toolIndex] = int(self.config.get(tool, 'tool thresh'))

            elif self.config.get(tool, "tool name") == 'Pattern Detection Tool':
                self.threshValue[toolIndex] = int(self.config.get(tool, 'tool thresh'))
                self.Results[toolIndex] = int(self.config.get(tool, "result"))


    def countColorPixels(self):

        if self.pixelColor[self.captureManager.toolIndex] is not None:
            pixels, frame = self.processingTools.countColorPixel(self.frame, self.pixelColor[
                self.captureManager.toolIndex],  self.threshValue[self.captureManager.toolIndex])

            self.setImagePreview(frame)
            print(pixels)
            self.NewResults[self.captureManager.toolIndex] = pixels
        else:
            self.setImagePreview(self.frame)


    def measureDistance(self):

        xdistance, ydistance, edgedMeasure = self.processingTools.measure(
            self.edged[self.captureManager.toolIndex], self.threshValue[self.captureManager.toolIndex], True, True)
        self.setImagePreview(edgedMeasure)
        self.NewResults[self.captureManager.toolIndex] = (xdistance, ydistance)


    def detectPattern(self):
        self.setImagePreview(self.frame)

        maxThresh = self.patternThresh[self.captureManager.toolIndex].maximum()
        pos, pattern = self.processingTools.detectPattern(
            self.frame, self.masterPattern,
            (maxThresh - self.patternThresh[self.captureManager.toolIndex].value()) / 100,
            True)
        self.setImagePreview(pattern)
        print("detected patterns= ", len(pos))
        self.NewResults[self.captureManager.toolIndex] = len(pos)


    def coloredPixel(self):

        self.setImagePreview(self.frame)
        if self.captureManager.toolIndex == 1:
            self.ColorThresh[self.captureManager.toolIndex] = self.ThreshSlider1
        elif self.captureManager.toolIndex == 2:
            self.ColorThresh[self.captureManager.toolIndex] = self.ThreshSlider2
        elif self.captureManager.toolIndex == 3:
            self.ColorThresh[self.captureManager.toolIndex] = self.ThreshSlider3
        elif self.captureManager.toolIndex == 4:
            self.ColorThresh[self.captureManager.toolIndex] = self.ThreshSlider4
        self.countColorPixels()
        QtCore.QObject.connect(self.ColorThresh[self.captureManager.toolIndex], QtCore.SIGNAL("valueChanged(int)"),
                               self.compare)
        QtCore.QObject.connect(self.ColorThresh[self.captureManager.toolIndex], QtCore.SIGNAL("sliderPressed()"),
                               self.countColorPixels)

    def measurement(self):

        if self.captureManager.toolIndex == 1:
            self.measurementThresh[self.captureManager.toolIndex] = self.ThreshSlider1
        elif self.captureManager.toolIndex == 2:
            self.measurementThresh[self.captureManager.toolIndex] = self.ThreshSlider2
        elif self.captureManager.toolIndex == 3:
            self.measurementThresh[self.captureManager.toolIndex] = self.ThreshSlider3
        elif self.captureManager.toolIndex == 4:
            self.measurementThresh[self.captureManager.toolIndex] = self.ThreshSlider4
        self.edged[self.captureManager.toolIndex] = self.processingTools.detectEdges(self.frame)

        self.setImagePreview(self.edged[self.captureManager.toolIndex])
        self.measureDistance()
        QtCore.QObject.connect(self.measurementThresh[self.captureManager.toolIndex],
                               QtCore.SIGNAL("valueChanged(int)"),
                               self.compare)
        QtCore.QObject.connect(self.measurementThresh[self.captureManager.toolIndex], QtCore.SIGNAL("sliderPressed()"),
                               self.measureDistance)



    def patternDetection(self):
        try:
            self.masterPattern = self.captureManager.loadFrame('./Masters/MasterPattern' +
                                                               str(self.captureManager.programNumber) + '.jpg')

        except Exception:
            print("error loading master pattern")

        if self.captureManager.toolIndex == 1:
            self.patternThresh[self.captureManager.toolIndex] = self.ThreshSlider1
        elif self.captureManager.toolIndex == 2:
            self.patternThresh[self.captureManager.toolIndex] = self.ThreshSlider2
        elif self.captureManager.toolIndex == 3:
            self.patternThresh[self.captureManager.toolIndex] = self.ThreshSlider3
        elif self.captureManager.toolIndex == 4:
            self.patternThresh[self.captureManager.toolIndex] = self.ThreshSlider4

        self.detectPattern()
        QtCore.QObject.connect(self.patternThresh[self.captureManager.toolIndex], QtCore.SIGNAL("valueChanged(int)"),
                               self.compare)
        QtCore.QObject.connect(self.patternThresh[self.captureManager.toolIndex], QtCore.SIGNAL("sliderPressed()"),
                               self.detectPattern)


    def compare(self):
        oldResult=self.Results[self.captureManager.toolIndex]
        newResult=self.NewResults[self.captureManager.toolIndex]
        if type(newResult) is int:
            print("new ", newResult, " old ", oldResult)
        else:
            for i in range(0,len(newResult)):
                print("new ",newResult[i]," old ",oldResult[i])







