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

        self.masterPattern = None
        self.passThresh = [0] * 5
        self.mixedFrame = [None] * 5
        self.measurementPoints = [None] * 5
        self.areaOfInterest = [None] * 5
        self.MainWindow = CustomSlots(self)
        self.setupUi(self.MainWindow)
        self.MainWindow.show()
        self.frame = None
        self.captureManager = captureManager
        self.config = ConfigParser()
        self.processingTools = ProcessingTools()

        self.threshValue = [None] * 5
        self.ColorThresh = [None] * 5
        self.pixelColor = [None] * 5
        self.measurementThresh = [None] * 5
        self.patternThresh = [None] * 5
        self.toolList = [None] * 5
        self.ignoredPixels = [None] * 5
        self.Results = [None] * 5
        self.NewResults = [0] * 5
        self.edged = [None] * 5

        self.loadConfig()
        self.captureManager.toolIndex = None

        QtCore.QObject.connect(self.ThreshSlider1, QtCore.SIGNAL("valueChanged(int)"),
                               self.setToolIndex1)
        QtCore.QObject.connect(self.ThreshSlider1, QtCore.SIGNAL("sliderPressed()"),
                               self.setToolIndex1)
        QtCore.QObject.connect(self.ThreshSlider2, QtCore.SIGNAL("valueChanged(int)"),
                               self.setToolIndex2)
        QtCore.QObject.connect(self.ThreshSlider2, QtCore.SIGNAL("sliderPressed()"),
                               self.setToolIndex2)
        QtCore.QObject.connect(self.ThreshSlider3, QtCore.SIGNAL("valueChanged(int)"),
                               self.setToolIndex3)
        QtCore.QObject.connect(self.ThreshSlider3, QtCore.SIGNAL("sliderPressed()"),
                               self.setToolIndex3)
        QtCore.QObject.connect(self.ThreshSlider4, QtCore.SIGNAL("valueChanged(int)"),
                               self.setToolIndex4)
        QtCore.QObject.connect(self.ThreshSlider4, QtCore.SIGNAL("sliderPressed()"),
                               self.setToolIndex4)

    def setToolIndex1(self):
        self.captureManager.toolIndex = 1
        self.savePassThresh(1, self.ThreshSlider1.value())

    def setToolIndex2(self):
        self.captureManager.toolIndex = 2
        self.savePassThresh(2, self.ThreshSlider2.value())

    def setToolIndex3(self):
        self.captureManager.toolIndex = 3
        self.savePassThresh(3, self.ThreshSlider3.value())

    def setToolIndex4(self):
        self.captureManager.toolIndex = 4
        self.savePassThresh(4, self.ThreshSlider4.value())

    # load an existing frame, takes Frame path as argument,default frame is replaced by the read frame

    def refreshFrame(self):

        self.captureManager.setCamera()
        self.frame = self.captureManager.readFrame()
        self.setImagePreview(self.frame)
        self.captureManager.cameraRelease()
        if self.captureManager.toolIndex is None:
            return
        if self.config.get("Tool" + str(self.captureManager.toolIndex) + "_Settings",
                           "tool name") == 'Color Pixel Tool':
            self.coloredPixel()

        elif self.config.get("Tool" + str(self.captureManager.toolIndex) + "_Settings",
                             "tool name") == 'measurement Tool':
            self.measurement()

        elif self.config.get("Tool" + str(self.captureManager.toolIndex) + "_Settings",
                             "tool name") == 'Pattern Detection Tool':
            self.patternDetection()

    # show frame in specific window ,default frame and window name are shown if not specified
    def setImagePreview(self, frame):
        temp = self.captureManager.makePixmap(frame)
        self.ImagePreview.setPixmap(QtGui.QPixmap(temp))

    def showSetup(self):
        self.SetupInterface = SetupInterface(self.captureManager)

    def loadConfig(self):
        self.config.read('config/config' + str(self.captureManager.programNumber) + '.ini')

        self.threshValue = [None] * 5
        self.ColorThresh = [None] * 5
        self.pixelColor = [None] * 5
        self.measurementThresh = [None] * 5
        self.patternThresh = [None] * 5
        self.toolList = [None] * 5
        self.areaOfInterest = [None] * 5
        self.measurementPoints = [None] * 5
        self.ignoredPixels = [None] * 5
        self.Results = [None] * 5
        self.passThresh = [0] * 5

        self.ToolName1.setText(self.config.get("Tool1_Settings", "tool name"))
        self.ToolName2.setText(self.config.get("Tool2_Settings", "tool name"))
        self.ToolName3.setText(self.config.get("Tool3_Settings", "tool name"))
        self.ToolName4.setText(self.config.get("Tool4_Settings", "tool name"))

        self.validation1.setText("")
        self.validation2.setText("")
        self.validation3.setText("")
        self.validation4.setText("")

        if self.config.get("Tool1_Settings", "tool name") == 'Tool1':
            self.Enable1.setChecked(False)
            self.Enable1.setCheckable(False)
            self.ThreshSlider1.setValue(0)

        else:

            self.Enable1.setChecked(True)
            self.Enable1.setCheckable(False)
            self.ThreshSlider1.setValue(int(self.config.get("Tool1_Settings", "pass thresh")))
            self.passThresh[1] = self.ThreshSlider1.value()

        if self.config.get("Tool2_Settings", "tool name") == 'Tool2':
            self.Enable2.setCheckable(False)
            self.Enable2.setChecked(False)
            self.ThreshSlider2.setValue(0)

        else:
            self.Enable2.setChecked(True)
            self.Enable2.setCheckable(False)
            self.ThreshSlider2.setValue(int(self.config.get("Tool2_Settings", "pass thresh")))
            self.passThresh[2] = self.ThreshSlider2.value()

        if self.config.get("Tool3_Settings", "tool name") == 'Tool3':
            self.Enable3.setChecked(False)
            self.Enable3.setCheckable(False)
            self.ThreshSlider3.setValue(0)
        else:
            self.Enable3.setChecked(True)
            self.Enable3.setCheckable(False)
            self.ThreshSlider3.setValue(int(self.config.get("Tool3_Settings", "pass thresh")))
            self.passThresh[3] = self.ThreshSlider3.value()

        if self.config.get("Tool4_Settings", "tool name") == 'Tool4':
            self.Enable4.setChecked(False)
            self.Enable4.setCheckable(False)
            self.ThreshSlider4.setValue(0)

        else:
            self.Enable4.setChecked(True)
            self.Enable4.setCheckable(False)
            self.ThreshSlider4.setValue(int(self.config.get("Tool4_Settings", "pass thresh")))
            self.passThresh[4] = self.ThreshSlider4.value()

        for toolIndex in range(1, 5):
            self.captureManager.toolIndex = toolIndex
            tool = "Tool" + str(toolIndex) + "_Settings"
            self.toolList[toolIndex] = self.config.get(tool, "tool name")
            if self.config.get(tool, "tool name") == 'Color Pixel Tool':
                pixelColor = self.config.get(tool, "pixel color")
                self.pixelColor[toolIndex] = [int(e.strip('[],')) for e in pixelColor.split(' ')]
                self.Results[toolIndex] = int(self.config.get(tool, "result"))
                self.threshValue[toolIndex] = int(self.config.get(tool, 'tool thresh'))
                self.coloredPixel()

            elif self.config.get(tool, "tool name") == 'measurement Tool':
                self.areaOfInterest[toolIndex] = ast.literal_eval(self.config.get(tool, "area of interest"))
                self.Results[toolIndex] = ast.literal_eval(self.config.get(tool, "result"))
                self.threshValue[toolIndex] = int(self.config.get(tool, 'tool thresh'))
                self.measurementPoints[toolIndex] = ast.literal_eval(self.config.get(tool, "measurement points"))
                self.measurement()

            elif self.config.get(tool, "tool name") == 'Pattern Detection Tool':
                self.threshValue[toolIndex] = int(self.config.get(tool, 'tool thresh'))
                self.Results[toolIndex] = int(self.config.get(tool, "result"))
                self.patternDetection()

    def countColorPixels(self):
        if self.frame is None:
            return

        self.compare()

        if self.pixelColor[self.captureManager.toolIndex] is not None:
            pixels, frame = self.processingTools.countColorPixel(self.frame, self.pixelColor[
                self.captureManager.toolIndex], self.threshValue[self.captureManager.toolIndex])

            self.setImagePreview(frame)

            self.NewResults[self.captureManager.toolIndex] = pixels
        else:
            self.setImagePreview(self.frame)

    def measureDistance(self):
        if self.frame is None:
            return

        # xdistance, ydistance, edgedMeasure = self.processingTools.measure(
        #     self.edged[self.captureManager.toolIndex], self.threshValue[self.captureManager.toolIndex], True, True)
        # self.setImagePreview(edgedMeasure)
        # self.NewResults[self.captureManager.toolIndex] = (xdistance, ydistance)
        startPoint = self.areaOfInterest[self.captureManager.toolIndex][0]
        endPoint = self.areaOfInterest[self.captureManager.toolIndex][1]

        frame = self.frame.copy()
        self.cropped = self.processingTools.cropFrame(self.frame, startPoint[0], startPoint[1],
                                                      (endPoint[1] - startPoint[1]), (endPoint[0] - startPoint[0]))
        self.edged[self.captureManager.toolIndex] = self.processingTools.detectEdges(self.cropped, self.threshValue[
            self.captureManager.toolIndex] / 100)

        edged3ch = self.processingTools.gray2BGR(self.edged[self.captureManager.toolIndex])
        self.mixedFrame[self.captureManager.toolIndex] = self.processingTools.replacePartFrame(frame, edged3ch,
                                                                                               min(endPoint[0],
                                                                                                   startPoint[0]),
                                                                                               min(endPoint[1],
                                                                                                   startPoint[1]))

        firstMeasurePoint = self.measurementPoints[self.captureManager.toolIndex][0]
        secondMeasurePoint = self.measurementPoints[self.captureManager.toolIndex][1]

        xedged = firstMeasurePoint[0] - startPoint[0]
        yedged = firstMeasurePoint[1] - startPoint[1]
        xedged, yedged = self.processingTools.getNearestPos(self.edged[self.captureManager.toolIndex], (xedged, yedged))
        if xedged is None or yedged is None:
            xedged=100000000
            yedged=100000000
            print("edge not found")

        firstMeasurePoint = (xedged + startPoint[0], yedged + startPoint[1])
        # firstMeasurePoint[0] = xedged + startPoint[0]
        # firstMeasurePoint[1] = yedged + startPoint[1]

        xedged = secondMeasurePoint[0] - startPoint[0]
        yedged = secondMeasurePoint[1] - startPoint[1]
        xedged, yedged = self.processingTools.getNearestPos(self.edged[self.captureManager.toolIndex], (xedged, yedged))

        if xedged is None or yedged is None:
            xedged=100000000
            yedged=100000000
            print("edge not found")

        secondMeasurePoint = (xedged + startPoint[0], yedged + startPoint[1])
        # secondMeasurePoint[0] = xedged + startPoint[0]
        # secondMeasurePoint[1] = yedged + startPoint[1]

        xdistance = abs(firstMeasurePoint[0] - secondMeasurePoint[0])
        ydistance = abs(firstMeasurePoint[1] - secondMeasurePoint[1])
        distance = (xdistance ** 2 + ydistance ** 2) ** (1 / 2)

        frame = self.mixedFrame[self.captureManager.toolIndex].copy()
        self.captureManager.drawArrow(frame, firstMeasurePoint, secondMeasurePoint)
        self.captureManager.drawArrow(frame, firstMeasurePoint,
                                      (secondMeasurePoint[0], firstMeasurePoint[1]), (0, 0, 255))
        self.captureManager.drawArrow(frame, secondMeasurePoint,
                                      (secondMeasurePoint[0], firstMeasurePoint[1]), (0, 255, 0))

        self.setImagePreview(frame)
        self.NewResults[self.captureManager.toolIndex] = (xdistance, ydistance, distance)

    def detectPattern(self):
        if self.frame is None:
            return

        self.compare()

        self.setImagePreview(self.frame)

        # maxThresh = self.patternThresh[self.captureManager.toolIndex].maximum()
        pos, pattern = self.processingTools.detectPattern(
            self.frame, self.masterPattern,
            (100 - self.threshValue[self.captureManager.toolIndex]) / 100,
            True)
        self.setImagePreview(pattern)

        self.NewResults[self.captureManager.toolIndex] = len(pos)

    def coloredPixel(self):
        if self.frame is not None:
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

        self.measureDistance()
        if self.frame is not None:
            self.compare()

        QtCore.QObject.connect(self.measurementThresh[self.captureManager.toolIndex],
                               QtCore.SIGNAL("valueChanged(int)"),
                               self.compare)

        QtCore.QObject.connect(self.measurementThresh[self.captureManager.toolIndex], QtCore.SIGNAL("sliderPressed()"),
                               self.measureDistance)

    def patternDetection(self):
        try:
            self.masterPattern = self.captureManager.loadFrame('./MasterPatterns/MasterPattern' +
                                                               str(self.captureManager.programNumber) + '.jpg')

        except Exception:
            print("error loading master pattern")

        if self.masterPattern is None:
            return

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

        threshSensible = [0, self.ThreshSlider1.value(), self.ThreshSlider2.value(), self.ThreshSlider3.value(),
                          self.ThreshSlider4.value()]
        validationLabel = [None, self.validation1, self.validation2, self.validation3, self.validation4]
        sensibility = threshSensible[self.captureManager.toolIndex]
        valid = validationLabel[self.captureManager.toolIndex]

        oldResult = self.Results[self.captureManager.toolIndex]
        newResult = self.NewResults[self.captureManager.toolIndex]
        print(self.toolList[self.captureManager.toolIndex])
        if type(oldResult) is int:
            print("new ", newResult, " old ", oldResult)
            if oldResult - sensibility * oldResult * 0.01 < newResult < oldResult + sensibility * oldResult * 0.01:
                valid.setText("OK")
                valid.setStyleSheet("color: green")
                return
            else:
                valid.setText("NOT OK")
                valid.setStyleSheet("color: red")
                return
        else:
            ok = True
            for i in range(0, len(oldResult)):
                print("new ", newResult[i], " old ", oldResult[i])
                if not oldResult[i] - sensibility * oldResult[i] * 0.01 < newResult[i] < oldResult[i] + sensibility * \
                       oldResult[i] * 0.01:
                    ok = False
            if ok:
                valid.setText("OK")
                valid.setStyleSheet("color: green")
                return
            else:
                valid.setText("NOT OK")
                valid.setStyleSheet("color: red")
                return

    def savePassThresh(self, toolIndex, passThresh):
        tool = "Tool" + str(toolIndex) + "_Settings"
        self.config.set(tool, "pass thresh", str(passThresh))

        with open('config/config' + str(self.captureManager.programNumber) + '.ini', 'w') as configfile:
            self.config.write(configfile)
