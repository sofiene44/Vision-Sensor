import cv2
import os
import sys



class CaptureManager(object):

    def __init__(self, camera=cv2.VideoCapture(0)):
        self._camera = camera
        self._frame = None
        self._path = './'
        self._imageName = '0.jpg'
        self._windowName ='window 1'


    def createwindow(self,windowName=None):
        if windowName is None:
            windowName=self._windowName
        cv2.namedWindow(windowName)

    def readFrame(self):
        try:
            _, self._frame = self._camera.read()
            return self._frame

        except:
            self._frame = None
            sys.exit("Error reading frame from sensor")

    @property
    def getFrame(self):
        return self._frame

    def setFrame(self, frame):
        self._frame = frame

    def showFrame(self, windowName= None, frame=None):
        if frame is None:
            frame = self._frame
        if windowName is None:
            windowName = self._windowName

        try:
            cv2.imshow(windowName, frame)
        except:
            sys.exit("Error showing Frame ")

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
            print('this name already existes')

    def setPath(self, path):
        self._path = path

    def setImageName(self, name):
        self._imageName = name

    def cameraRelease(self):
        self._camera.release()
        cv2.destroyAllWindows()
