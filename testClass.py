from CaptureManager import CaptureManager
from ProcessingTools import ProcessingTools
from trackbar import Trackbar
import time

import cv2


class TestClass(object):

    def __init__(self):
        self._startTime = None
        self._captureManager = CaptureManager()
        self._processingTools = ProcessingTools()
        self._edgeTrackBar = Trackbar()
        self._endTime = None

    def runGetFrame(self):

        trigger = True
        _edgeThreshold = 0
        self._captureManager.createwindow()
        self._edgeTrackBar.addBar("edge", "window 1", 100, _edgeThreshold)

        while True:
            self._startTime = time.time()
            if trigger:
                trigger = False
                self._captureManager.readFrame()

            # self._captureManager.setFrame(cv2.imread("mario.png"))
            self._captureManager.showFrame()
            _frame = self._captureManager.getFrame
            key = cv2.waitKey(1) & 0xff

            if key == 27:  # escape
                break
            elif key == 32:  # space
                trigger = True  # refresh frame
            elif key == 9:  # tab
                # path= input("enter path ")
                # print("\n")
                imageName = input("enter file name ")
                print("\n")
                self._captureManager.saveImage(imageName=imageName + '.jpg')

            elif key == ord("e") or True:  # apply edge detection

                _edgeThreshold = self._edgeTrackBar.getBar
                edges = self._processingTools.detectEdges(_frame, float(_edgeThreshold / 100))
                self._captureManager.showFrame("edges", edges)
            elif key == ord("c"):
                cropped = self._processingTools.cropFrame(_frame, 0, 0, 200, 200)
                self._captureManager.showFrame("cropped", cropped)

            # test execution time for a single test
            if self._endTime is None:
                self._endTime = time.time()
                print("time =  ", self._endTime - self._startTime)

        self._captureManager.cameraRelease()


if __name__ == "__main__":
    TestClass().runGetFrame()
