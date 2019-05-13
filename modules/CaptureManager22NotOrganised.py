import cv2
import os
import time

from GUI.mainFrameWindow import *
from GUI.toolSettingsWindow import *
from GUI.setupWindow import *
from modules.ProcessingTools import ProcessingTools
from PyQt4.QtCore import QThread
from PyQt4 import QtCore, QtGui


# this class is responsible for reading frames from the camera, creating windows, loading existing frames


class CaptureManager(Ui_MainWindow):

    # Initialise the class to default values ; default camera index corresponds to the computer's default camera

    def __init__(self, cameraIndex=None):
        super(CaptureManager, self).__init__()
        self.MainWindow=None
        self._cameraIndex=cameraIndex
        #self._camera = cv2.VideoCapture(cameraIndex)
        self._camera=None
        self._frame = None
        self._path = './'
        self._imageName = 'noName.jpg'
        self._windowName = 'default window'

    # create a named window with default name if not specified
    def createWindow(self, windowName=None):
        if windowName is None:
            windowName = self._windowName
        cv2.namedWindow(windowName)

    # load an existing frame, takes Frame path as argument,default frame is replaced by the read frame
    def loadFrame(self, path):

        self._frame = cv2.imread(path)
        return self._frame


    # read and return current frame from the camera, default frame is replaced by read frame
    def readFrame(self):
        if self._camera is not None:

            _, self._frame = self._camera.read()
            return self._frame



    def refreshFrame(self):
        self.setCamera()
        frame = self.readFrame()
        temp = self.makePixmap(frame)
        self.ImagePreview.setPixmap(QtGui.QPixmap(temp))
        self.cameraRelease()


    # show frame in specific window ,default frame and window name are shown if not specified
    def showFrame(self, windowName=None, frame=None):
        if frame is None:
            frame = self._frame
        if windowName is None:
            windowName = self._windowName

        # try:
        cv2.imshow(windowName, frame)
        # except:
        #     sys.exit("Error showing Frame ")

    # wait for pressed key while frame is shown

    # save image to specific path, default values are used if arguments are not specified
    def saveImage(self, frame=None, path=None, imageName=None):

        if path is None:
            path = self._path

        if imageName is None:
            imageName = self._imageName

        if frame is None:
            frame = self._frame

        if not os.path.exists(path + imageName):
            try:
                cv2.imwrite(path + imageName, frame)
                print('image successfully saved in "' + path + imageName + '"')
            except:
                print("Error saving file")
        else:
            print('this name already exists')

    def makePixmap(self, frame):
        if len(frame.shape) < 3:
            temp = ProcessingTools.gray2BGR()
        else:
            temp = frame
        height, width, channel = temp.shape
        bytesPerLine = 3 * width
        qImg = QtGui.QImage(temp.data, width, height, bytesPerLine, QtGui.QImage.Format_RGB888).rgbSwapped()
        return qImg

    def addtext(self, frame, pos, text):
        cv2.putText(frame, text, pos, cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255))

    # getters and setters for the default values

    @property
    def getFrame(self):
        return self._frame

    def setFrame(self, frame):
        self._frame = frame

    @property
    def getWindowName(self):
        return self._windowName

    def setPath(self, path):
        self._path = path

    def setImageName(self, name):
        self._imageName = name

    # release camera and destroy shown windows
    def destroyWindow(self, windowName=None):
        if windowName is None:
            cv2.destroyAllWindows()
        else:
            cv2.destroyWindow(windowName)

    def cameraRelease(self):
        if self._camera is not None:
            self._camera.release()

    def setCamera(self,cameraIndex=None):

        if cameraIndex is None:
            self._camera=cv2.VideoCapture(self._cameraIndex)
        else:
            self._camera=cv2.VideoCapture(cameraIndex)

    def showToolSettings(self):

        self.toolSettingsUi = ToolSettingsInterface()
        self.toolSettingsWindow = CustomSlots(self.toolSettingsUi)
        self.toolSettingsUi.setupUi(self.toolSettingsWindow)
        self.toolSettingsWindow.show()

    def showSetup(self):
        self.setupUi = SetupInterface()
        self.setupWindow = CustomSlots(self.setupUi)
        self.setupUi.setupUi(self.setupWindow)
        self.setupWindow.show()
        self.refresher=SecondThread(self.setupUi,self.setupWindow)
        self.refresher.start()
        QtCore.QObject.connect(self.refresher,QtCore.SIGNAL('refreshFrame()'),self.setupUi.refreshFrame)



class SecondThread(QThread):

    def __init__(self,interface,window):
        super(SecondThread, self).__init__()
        self.interface=interface
        self.window=window
    def run(self):
        while self.interface.capture:
            self.emit(QtCore.SIGNAL('refreshFrame()'))
            time.sleep(0.2)





class ToolSettingsInterface(Ui_ToolSettingsWindow):

    def __init__(self):
        super(ToolSettingsInterface, self).__init__()

    def ColorePixelSelected(self):

        print("ColorPixel")

    def measurementSelected(self):
        print("measurement")

    def patternDetectionSelected(self):
        print("patternDetection")


class SetupInterface(Ui_SetupWindow):
    def __init__(self):
        super(SetupInterface, self).__init__()
        self.capture = True
        self.camera=CaptureManager(0)


    def refreshFrame(self):
        print("ok")

        self.camera.setCamera(0)
        frame = self.camera.readFrame()
        temp = self.camera.makePixmap(frame)
        self.ImagePreview.setPixmap(QtGui.QPixmap(temp))
        self.camera.cameraRelease()





class CustomSlots(QtGui.QMainWindow):

    def __init__(self,interface):
        super(CustomSlots, self).__init__()
        self._interface = interface

    def refreshFrame(self):

        self._interface.refreshFrame()

    def showToolSettings(self):

        self._interface.showToolSettings()

    def showSetup(self):
        self._interface.showSetup()



    def ColorePixelSelected(self):

        self._interface.ColorePixelSelected()
        self.deleteLater()

    def measurementSelected(self):
        self._interface.measurementSelected()
        self.deleteLater()

    def patternDetectionSelected(self):
        self._interface.patternDetectionSelected()
        self.deleteLater()

    def snapshot(self):
        self._interface.capture=False



class Interactions(object):

    def __init__(self):
        self._mousePos = (0, 0)
        self.drag_start = None
        self.selected = (0, 0, 0, 0)
        self.frame = None
        self.windowName = None
        self.height = None
        self.width = None

    def keyPressed(self, delay=1):
        return cv2.waitKey(delay) & 0xff

    def getMouseDbclick(self, windowName):

        cv2.setMouseCallback(windowName, self.mouseDbClicked)
        return self._mousePos

    def mouseDbClicked(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDBLCLK:
            self._mousePos = y, x

    def selectArea(self, windowName, frame):
        self.frame = frame.copy()
        self.windowName = windowName
        self.height, self.width, _ = self.frame.shape

        cv2.setMouseCallback(windowName, self.mouseDragged)
        if self.selected[2] != 0 and self.selected[3] != 0:

            return self.selected
        else:

            return 0, 0, self.width, self.height

    def mouseDragged(self, event, x, y, flags, param):

        if event == cv2.EVENT_LBUTTONDOWN:
            self.drag_start = x, y
            self.selected = (0, 0, 0, 0)

        elif event == cv2.EVENT_LBUTTONUP:
            self.drag_start = None

        elif self.drag_start:

            if flags & cv2.EVENT_FLAG_LBUTTON:
                x, y = max(x, 0), max(y, 0)
                minpos = min(self.drag_start[0], x), min(self.drag_start[1], y)
                maxpos = max(self.drag_start[0], x), max(self.drag_start[1], y)
                self.selected = (minpos[0], minpos[1], maxpos[0], maxpos[1])
                cv2.rectangle(self.frame, (self.selected[0], self.selected[1]), (self.selected[2], self.selected[3]),
                              (0, 255, 255), 1)
                cv2.imshow(self.windowName, self.frame)

            else:
                self.drag_start = None


# this class is responsible for creating and getting values from Trackbars for sensibility testing


class Trackbar(object):

    def __init__(self):
        self._val = 0
        self._max = 0

    # function executed when the bar value is changed, save the current value to the default value
    def on_trackbar(self, val):
        self._val = val

    # create a trackbar in a specific window
    def addBar(self, trackName, maxValue, value, windowName='default window'):
        self._max = maxValue
        cv2.createTrackbar(trackName, windowName, value, self._max, self.on_trackbar)

    # getter for the saved value of the trackbar
    @property
    def getBar(self):
        return self._val

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
