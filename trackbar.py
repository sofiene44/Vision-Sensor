import cv2 as cv


class Trackbar(object):
    def __init__(self):
        self._val = 0

    def on_trackbar(self, val):
        self._val = val


    def addBar(self, trackName, windowName, max,value):
        self._max = max
        cv.createTrackbar(trackName, windowName, value, self._max, self.on_trackbar)

    @property
    def getBar(self):
        return self._val


