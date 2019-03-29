from CaptureManager import CaptureManager
import cv2

class TestClass(object):

    def __init__(self):
        self._captureManager = CaptureManager()


    def runGetFrame(self):

        self._captureManager.readFrame()
        while 1:
            self._captureManager.showFrame()
            key=cv2.waitKey(1)& 0xff
            if key== 27:    #escape
                break
            elif key==32:   #space
                self._captureManager.readFrame()    #refresh frame
            elif key==9:    #tab
                #path= input("enter path ")
                #print("\n")
                imageName=input("enter file name ")
                print("\n")
                self._captureManager.saveImage(None, None, imageName+'.jpg')


TestClass=TestClass()

if __name__ == "__main__":
    TestClass.runGetFrame()
