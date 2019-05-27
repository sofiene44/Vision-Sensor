#from RPiSim.GPIO import GPIO
from RPi import GPIO


from modules.ProcessingTools import ProcessingTools
from modules.CaptureManager import CaptureManager
from configparser import ConfigParser


programNumber=[2,3,4]
trigger=14

class VisionSensor:

    def __init__(self):

        # GPIO setup
        GPIO.setmode(GPIO.BCM)

        # Program Number
        for i in programNumber:
            GPIO.setup(i, GPIO.IN)
            GPIO.add_event_detect(i,GPIO.BOTH)


        # trigger
        GPIO.setup(trigger, GPIO.IN)
        GPIO.add_event_detect(trigger,GPIO.RISING)

        # VisionSensor setup
        self.frame = None
        self.captureManager = CaptureManager(0)
        self.processingTools = ProcessingTools()
        self.config = ConfigParser()
        self.captureManager.programNumber=self.getProgramNumber()
        print(self.captureManager.programNumber)


    def getProgramNumber(self):
        temp=str(int(GPIO.input(programNumber[0])))+str(int(GPIO.input(programNumber[1])))+\
             str(int(GPIO.input(programNumber[2])))
        return int(temp,2)

    def resetEvent(self, pins,GPIOevent = GPIO.RISING):
        if type(pins) is int:
            GPIO.remove_event_detect(pins)
            GPIO.add_event_detect(pins, GPIOevent)
        else:
            for i in pins:
                GPIO.remove_event_detect(i)
                GPIO.add_event_detect(i, GPIOevent)

    def loadConfig(self):
        print('loadConfig ', self.captureManager.programNumber)
        pass

    def run(self):
        while True:
            if GPIO.event_detected(programNumber[0]) or GPIO.event_detected(programNumber[1]) or \
                    GPIO.event_detected(programNumber[2]):
                visionSensor.resetEvent(programNumber, GPIO.BOTH)
                visionSensor.captureManager.programNumber = visionSensor.getProgramNumber()
                print(visionSensor.getProgramNumber())
                visionSensor.loadConfig()
            elif GPIO.event_detected(trigger):
                visionSensor.resetEvent(trigger, GPIO.RISING)
                print("execute tools")


visionSensor = VisionSensor()
visionSensor.run()


        




