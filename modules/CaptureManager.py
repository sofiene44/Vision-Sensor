import cv2
import os

from modules.ProcessingTools import ProcessingTools
from PyQt4 import QtGui




class CaptureManager(object):
    def __init__(self, cameraIndex=None):
            self._activeWindow = None
            self._cameraIndex = cameraIndex
            self._camera = None
            self._frame = None
            self.programNumber=0

    def loadFrame(self, path):

        self._frame = cv2.imread(path)
        return self._frame

    def readFrame(self):
        if self._camera is not None:
            _, self._frame = self._camera.read()
            return self._frame

    def saveImage(self, frame=None, path="./", imageName=''):

        if frame is None:
            frame = self._frame

        cv2.imwrite(path + imageName, frame)
        print('image successfully saved in "' + path + imageName + '"')


    def makePixmap(self, frame):
        if frame is None:
            return None
        if len(frame.shape) < 3:
            temp = ProcessingTools.gray2BGR(frame)
        else:
            temp = frame
        height, width, channel = temp.shape
        bytesPerLine = 3 * width
        qImg = QtGui.QImage(temp.data, width, height, bytesPerLine, QtGui.QImage.Format_RGB888).rgbSwapped()
        return qImg

    def addtext(self, frame, pos, text, color=(255,255,255)):
        cv2.putText(frame, text, pos, cv2.FONT_HERSHEY_SIMPLEX, 1.0, color)

    @property
    def getFrame(self):
        return self._frame

    def setFrame(self, frame):
        self._frame = frame

    @property
    def getActiveWindow(self):
        return self._activeWindow

    def setActiveWindow(self,activeWindow):
        self._activeWindow=activeWindow

    @property
    def getProgramNumber(self):
        return self.programNumber

    def cameraRelease(self):
        if self._camera is not None:
            self._camera.release()
            self._camera=None

    def setCamera(self, cameraIndex=None):

        if cameraIndex is None:
            self.cameraRelease()
            self._camera = cv2.VideoCapture(self._cameraIndex)
        else:
            self.cameraRelease()
            self._camera = cv2.VideoCapture(cameraIndex)







#
# class Interactions(object):
#
#     def __init__(self):
#         self._mousePos = (0, 0)
#         self.drag_start = None
#         self.selected = (0, 0, 0, 0)
#         self.frame = None
#         self.windowName = None
#         self.height = None
#         self.width = None
#
#     def keyPressed(self, delay=1):
#         return cv2.waitKey(delay) & 0xff
#
#     def getMouseDbclick(self, windowName):
#
#         cv2.setMouseCallback(windowName, self.mouseDbClicked)
#         return self._mousePos
#
#     def mouseDbClicked(self, event, x, y, flags, param):
#         if event == cv2.EVENT_LBUTTONDBLCLK:
#             self._mousePos = y, x
#
#     def selectArea(self, windowName, frame):
#         self.frame = frame.copy()
#         self.windowName = windowName
#         self.height, self.width, _ = self.frame.shape
#
#         cv2.setMouseCallback(windowName, self.mouseDragged)
#         if self.selected[2] != 0 and self.selected[3] != 0:
#
#             return self.selected
#         else:
#
#             return 0, 0, self.width, self.height
#
#     def mouseDragged(self, event, x, y, flags, param):
#
#         if event == cv2.EVENT_LBUTTONDOWN:
#             self.drag_start = x, y
#             self.selected = (0, 0, 0, 0)
#
#         elif event == cv2.EVENT_LBUTTONUP:
#             self.drag_start = None
#
#         elif self.drag_start:
#
#             if flags & cv2.EVENT_FLAG_LBUTTON:
#                 x, y = max(x, 0), max(y, 0)
#                 minpos = min(self.drag_start[0], x), min(self.drag_start[1], y)
#                 maxpos = max(self.drag_start[0], x), max(self.drag_start[1], y)
#                 self.selected = (minpos[0], minpos[1], maxpos[0], maxpos[1])
#                 cv2.rectangle(self.frame, (self.selected[0], self.selected[1]), (self.selected[2], self.selected[3]),
#                               (0, 255, 255), 1)
#                 cv2.imshow(self.windowName, self.frame)
#
#             else:
#                 self.drag_start = None
#
#
# # this class is responsible for creating and getting values from Trackbars for sensibility testing

#
# class Trackbar(object):
#
#     def __init__(self):
#         self._val = 0
#         self._max = 0
#
#     # function executed when the bar value is changed, save the current value to the default value
#     def on_trackbar(self, val):
#         self._val = val
#
#     # create a trackbar in a specific window
#     def addBar(self, trackName, maxValue, value, windowName='default window'):
#         self._max = maxValue
#         cv2.createTrackbar(trackName, windowName, value, self._max, self.on_trackbar)
#
#     # getter for the saved value of the trackbar
#     @property
#     def getBar(self):
#         return self._val

#
# if __name__ == "__main__":
#     import sys
#
#     app = QtGui.QApplication(sys.argv)
#     ui = CaptureManager(0)
#     MainWindow = CustomSlots(ui)
#
#     ui.setupUi(MainWindow)
#     MainWindow.show()
#
#     sys.exit(app.exec_())
