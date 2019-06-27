from RPi import GPIO
import ast

from modules.ProcessingTools import ProcessingTools
from modules.CaptureManager import CaptureManager
from configparser import ConfigParser

programNumber = [4, 5, 6]
trigger = 7

busy=25
ready = 27
validTest = 21
validTools = [17,18,19]

class VisionSensor(object):

    def __init__(self):

        # GPIO setup
        GPIO.setmode(GPIO.BCM)

        # Program Number
        for i in programNumber:
            GPIO.setup(i, GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
            GPIO.add_event_detect(i, GPIO.BOTH)

        # trigger
        GPIO.setup(trigger, GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
        GPIO.add_event_detect(trigger, GPIO.RISING)

        # results
        for i in validTools:
            GPIO.setup(i, GPIO.OUT, initial=GPIO.LOW)

        GPIO.setup(ready, GPIO.OUT, initial=GPIO.LOW)
        
        GPIO.setup(busy, GPIO.OUT, initial=GPIO.LOW)
        
        GPIO.setup(validTest, GPIO.OUT, initial=GPIO.LOW)

        # VisionSensor setup
        self.frame = None
        self.captureManager = CaptureManager()
        self.processingTools = ProcessingTools()
        self.config = ConfigParser()
        self.captureManager.programNumber = self.getProgramNumber()
        print(self.captureManager.programNumber)

    def getProgramNumber(self):
        temp = str(int(GPIO.input(programNumber[0]))) + str(int(GPIO.input(programNumber[1]))) + \
               str(int(GPIO.input(programNumber[2])))
        return int(temp, 2)

    def resetEvent(self, pins, GPIOevent=GPIO.RISING):
        if type(pins) is int:
            GPIO.remove_event_detect(pins)
            GPIO.add_event_detect(pins, GPIOevent)
        else:
            for i in pins:
                GPIO.remove_event_detect(i)
                GPIO.add_event_detect(i, GPIOevent)

    def loadConfig(self):
        if self.captureManager.programNumber > 5:
            print("failed to load program ", self.captureManager.programNumber)
            return False

        print('loadConfig ', self.captureManager.programNumber)
        self.config.read('config/config' + str(self.captureManager.programNumber) + '.ini')

        self.threshValue = [0] * 5
        self.ColorThresh = [None] * 5
        self.pixelColor = [None] * 5
        self.measurementThresh = [None] * 5
        self.patternThresh = [None] * 5
        self.toolList = [None] * 5
        self.areaOfInterest = [None] * 5
        self.measurementPoints = [None] * 5
        self.ignoredPixels = [None] * 5
        self.Results = [None] * 5
        self.edged = [None] * 5
        self.passThresh = [0] * 5
        self.NewResults = [0] * 5

        for toolIndex in range(1, 5):
            self.captureManager.toolIndex = toolIndex
            tool = "Tool" + str(toolIndex) + "_Settings"
            self.toolList[toolIndex] = self.config.get(tool, "tool name")
            if self.config.get(tool, "tool name") == 'Color Pixel Tool':
                pixelColor = self.config.get(tool, "pixel color")
                self.pixelColor[toolIndex] = [int(e.strip('[],')) for e in pixelColor.split(' ')]
                self.Results[toolIndex] = int(self.config.get(tool, "result"))
                self.threshValue[toolIndex] = int(self.config.get(tool, 'tool thresh'))
                self.passThresh[toolIndex] = int(self.config.get(tool, 'pass thresh'))

            elif self.config.get(tool, "tool name") == 'measurement Tool':
                self.areaOfInterest[toolIndex] = ast.literal_eval(self.config.get(tool, "area of interest"))
                self.Results[toolIndex] = ast.literal_eval(self.config.get(tool, "result"))
                self.threshValue[toolIndex] = int(self.config.get(tool, 'tool thresh'))
                self.measurementPoints[toolIndex] = ast.literal_eval(self.config.get(tool, "measurement points"))
                self.passThresh[toolIndex] = int(self.config.get(tool, 'pass thresh'))

            elif self.config.get(tool, "tool name") == 'Pattern Detection Tool':
                self.threshValue[toolIndex] = int(self.config.get(tool, 'tool thresh'))
                self.Results[toolIndex] = int(self.config.get(tool, "result"))
                self.passThresh[toolIndex] = int(self.config.get(tool, 'pass thresh'))

        return True

    def readFrame(self):
        # self.frame = self.captureManager.readFrameSmartphone()
        self.frame = self.captureManager.readFrame()
        print(self.frame)

    def countColorPixels(self, toolIndex):
        if self.frame is None:
            return

        if self.pixelColor[toolIndex] is not None:
            pixels, frame = self.processingTools.countColorPixel(self.frame, self.pixelColor[
                toolIndex], self.threshValue[toolIndex])
            self.NewResults[toolIndex] = pixels

    def measureDistance(self, toolIndex):
        if self.frame is None:
            return

        xdistance = 0
        ydistance = 0
        distance= 0
        
        startPoint = self.areaOfInterest[toolIndex][0]
        endPoint = self.areaOfInterest[toolIndex][1]

        self.cropped = self.processingTools.cropFrame(self.frame, startPoint[0], startPoint[1],
                                                      (endPoint[1] - startPoint[1]), (endPoint[0] - startPoint[0]))
        self.edged[toolIndex] = self.processingTools.detectEdges(self.cropped, self.threshValue[toolIndex] / 100)

        firstMeasurePoint = self.measurementPoints[toolIndex][0]
        secondMeasurePoint = self.measurementPoints[toolIndex][1]

        xedged = firstMeasurePoint[0] - startPoint[0]
        yedged = firstMeasurePoint[1] - startPoint[1]
        xedged, yedged = self.processingTools.getNearestPos(self.edged[toolIndex], (xedged, yedged))
        if xedged is None or yedged is None:
            xedged = 100000000
            yedged = 100000000
            print("edge not found")

        firstMeasurePoint = (xedged + startPoint[0], yedged + startPoint[1])

        xedged = secondMeasurePoint[0] - startPoint[0]
        yedged = secondMeasurePoint[1] - startPoint[1]
        xedged, yedged = self.processingTools.getNearestPos(self.edged[toolIndex], (xedged, yedged))

        if xedged is None or yedged is None:
            xedged = 100000000
            yedged = 100000000
            print("edge not found")

        secondMeasurePoint = (xedged + startPoint[0], yedged + startPoint[1])

        xdistance = abs(firstMeasurePoint[0] - secondMeasurePoint[0])
        ydistance = abs(firstMeasurePoint[1] - secondMeasurePoint[1])
        distance = (xdistance ** 2 + ydistance ** 2) ** (1 / 2)

        self.NewResults[toolIndex] = (xdistance, ydistance, distance)

    def detectPattern(self, toolIndex):

        if self.frame is None:
            return
        self.masterPattern = self.captureManager.loadFrame('./MasterPatterns/MasterPattern' +
                                                           str(self.captureManager.programNumber) + '.jpg')

        pos, pattern = self.processingTools.detectPattern(
            self.frame, self.masterPattern,
            (100 - self.threshValue[toolIndex]) / 100,
            True)

        self.NewResults[toolIndex] = len(pos)

    def compare(self, toolIndex):

        sensibility = self.passThresh[toolIndex]

        oldResult = self.Results[toolIndex]
        newResult = self.NewResults[toolIndex]
        print(self.toolList[toolIndex])

        if type(oldResult) is int:
            print("new ", newResult, " old ", oldResult)
            if oldResult - sensibility * oldResult * 0.01 < newResult < oldResult + sensibility * oldResult * 0.01:
                GPIO.output(validTools[toolIndex - 1], GPIO.HIGH)
                print("Pass")
                return True


            else:
                GPIO.output(validTools[toolIndex - 1], GPIO.LOW)
                print("Fail")
                return False
        elif type(oldResult) is not int:
            
            ok = True
            for i in range(0, len(oldResult)):
                print("new ", newResult[i], " old ", oldResult[i])
                if not oldResult[i] - sensibility * oldResult[i] * 0.01 < newResult[i] < oldResult[i] + sensibility * \
                       oldResult[i] * 0.01:
                    ok = False

            if ok:
                GPIO.output(validTools[toolIndex - 1], GPIO.HIGH)
                print("Pass")
                return True
            else:
                GPIO.output(validTools[toolIndex - 1], GPIO.LOW)
                print("Fail")
                return False

    def run(self):
        loaded = self.loadConfig()
        GPIO.output(ready, GPIO.HIGH)
        while True:

            self.test = [True] * 5
            if GPIO.event_detected(programNumber[0]) or GPIO.event_detected(programNumber[1]) or \
                    GPIO.event_detected(programNumber[2]):
                visionSensor.resetEvent(programNumber, GPIO.BOTH)
                visionSensor.captureManager.programNumber = visionSensor.getProgramNumber()
                loaded = visionSensor.loadConfig()
            elif GPIO.event_detected(trigger) and loaded:
                print("=========================================")
                
                for i in validTools:
                    GPIO.output(i, GPIO.LOW)
                GPIO.output(validTest, GPIO.LOW)
                
                GPIO.output(busy, GPIO.HIGH)
                
                GPIO.output(ready, GPIO.LOW)
                GPIO.output(validTest, GPIO.LOW)
                visionSensor.resetEvent(trigger, GPIO.RISING)
                print("execute tools")
                self.readFrame()
                for toolIndex in range(1, 5):
                    print("--------------------")
                    if self.toolList[toolIndex] == "Color Pixel Tool":
                        self.countColorPixels(toolIndex)
                        self.test[toolIndex] = self.compare(toolIndex)
                    elif self.toolList[toolIndex] == "measurement Tool":
                        self.measureDistance(toolIndex)
                        self.test[toolIndex] = self.compare(toolIndex)
                    elif self.toolList[toolIndex] == "Pattern Detection Tool":
                        self.detectPattern(toolIndex)
                        self.test[toolIndex] = self.compare(toolIndex)
                    else:
                        pass
                GPIO.output(busy, GPIO.LOW)
                GPIO.output(ready, GPIO.HIGH)
                if self.test == [True] * 5:
                    GPIO.output(validTest, GPIO.HIGH)

            # else:
            #     print("waiting for command signal")


if __name__ == "__main__":
    visionSensor = VisionSensor()
    visionSensor.run()
