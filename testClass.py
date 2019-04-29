from modules.CaptureManager import CaptureManager
from modules.MainWindowUi import MainWindowUi
from modules.CustomSlots import CustomSlots
from modules.ProcessingTools import ProcessingTools
from PyQt4 import QtGui

import time


# this class is a test case class responsible for testing the different classes
# it will be executed as the main class
#
# class TestClass(object):
#
#     def __init__(self):
#         self._startTime = None
#         self._captureManager = CaptureManager(0)
#         self._processingTools = ProcessingTools()
#         self._edgeTrackBar = Trackbar()
#         self._coloredPixelCount = Trackbar()
#         self._interactions = Interactions()
#         self._endTime = None
#
#     def runGetFrame(self):
#         toggleColorOn = False
#         toggleEdgeOn = False
#         toggleCroppOn = False
#         trigger = True
#         _edgeThreshold = 0
#         _colorPixelThreshold = 0
#         self._captureManager.createWindow()
#         self._edgeTrackBar.addBar("edge", 100, _edgeThreshold)
#         self._coloredPixelCount.addBar("colored pixel", 255, _colorPixelThreshold)
#         #self._captureManager.loadFrame("pictures/color-pixel-count.jpg")
#         while True:
#             self._startTime = time.time()
#             if trigger:
#                 #trigger = False
#                 self._captureManager.readFrame()
#             _frame = self._captureManager.getFrame
#             self._captureManager.showFrame()
#             key = self._interactions.keyPressed()
#             if key == 27:  # escape
#                 break
#             elif key == 32:  # space
#                 trigger = True  # refresh frame
#             elif key == 9:  # tab
#                 # path= input("enter path ")
#                 # print("\n")
#                 imageName = input("enter file name ")
#                 print("\n")
#                 self._captureManager.saveImage(imageName=imageName + '.jpg')
#
#             elif key == ord("e") or toggleEdgeOn:  # apply edge detection
#                 toggleEdgeOn = True
#                 _edgeThreshold = self._edgeTrackBar.getBar
#                 edges = self._processingTools.detectEdges(_frame, float(_edgeThreshold / 100))
#                 self._captureManager.showFrame("edges", edges)
#                 if key == 8:
#                     self._captureManager.destroyWindow("edges")
#                     toggleEdgeOn = False
#             elif key == ord("a") or toggleCroppOn:
#                 toggleCroppOn = True
#                 selected = self._interactions.selectArea(self._captureManager.getWindowName, _frame)
#                 selected = selected[0], selected[1], max(abs(selected[2] - selected[0]), 1), \
#                            max(abs(selected[3] - selected[1]), 1)
#                 cropped = self._processingTools.cropFrame(_frame, selected[0], selected[1], selected[2], selected[3])
#                 self._captureManager.showFrame("cropped", cropped)
#                 if key == 8:
#                     self._captureManager.destroyWindow("cropped")
#                     toggleCroppOn = False
#             elif key == ord("z") or toggleColorOn:
#                 toggleColorOn = True
#                 pos = self._interactions.getMouseDbclick(self._captureManager.getWindowName)
#                 _colorPixelThreshold = self._coloredPixelCount.getBar
#                 _, detectedColor = self._processingTools.countColorPixel(_frame, _frame[pos], _colorPixelThreshold)
#                 self._captureManager.showFrame("detected color", detectedColor)
#                 if key == 8:
#                     self._captureManager.destroyWindow("detected color")
#                     toggleColorOn = False
#
#
#
#             # test execution time for a single test
#             if self._endTime is None:
#                 self._endTime = time.time()
#                 print("execution time =  ", self._endTime - self._startTime)
#
#         self._captureManager.cameraRelease()
#         self._captureManager.destroyWindow()
#


#if __name__ == "__main__":
#    TestClass().runGetFrame()


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    captureManager = CaptureManager(0)
    mainWindowUi = MainWindowUi()
    mainWindowUi.MainWindow = CustomSlots(mainWindowUi)
    mainWindowUi.setupUi(mainWindowUi.MainWindow)
    mainWindowUi.MainWindow.show()

    sys.exit(app.exec_())

