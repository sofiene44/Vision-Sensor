from RPiSim.GPIO import GPIO
from modules.ProcessingTools import ProcessingTools
from modules.CaptureManager import CaptureManager
from configparser import ConfigParser


class VisionSensor:

    def __init__(self):


        # GPIO setup
        GPIO.setmode(GPIO.BCM)

        # Program Number
        GPIO.setup(2, GPIO.IN)
        GPIO.setup(3, GPIO.IN)
        GPIO.setup(4, GPIO.IN)
        GPIO.add_event_detect(2,GPIO.BOTH)

        # VisionSensor setup
        self.frame = None
        self.captureManager = CaptureManager(0)
        self.processingTools = ProcessingTools()
        self.config = ConfigParser()
        self.captureManager.programNumber=self.getProgramNumber()
        print(self.captureManager.programNumber)



    def getProgramNumber(self):
        return int(str(int(GPIO.input(2)))+str(int(GPIO.input(3)))+str(int(GPIO.input(4))),2)

    def loadConfig(self):
        pass


VisionSensor=VisionSensor()