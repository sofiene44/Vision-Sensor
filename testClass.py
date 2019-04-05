from CaptureManager import CaptureManager
from ProcessingTools import ProcessingTools
from trackbar import Trackbar


import cv2



class TestClass(object):

    def __init__(self):
        self._captureManager = CaptureManager()
        self._processingTools = ProcessingTools()
        self._edgeTrackBar = Trackbar()

    def runGetFrame(self):
        trigger=True
        _edgeThreshold=0
        cv2.namedWindow("window 1")
        self._edgeTrackBar.addBar("edge", "window 1", 100, _edgeThreshold)

        while True:
            if trigger:
                trigger = False
                self._captureManager.readFrame()

            #self._captureManager.setFrame(cv2.imread("piece-mecanique.jpg"))
            self._captureManager.showFrame()


            key=cv2.waitKey(1)& 0xff
            if key== 27:    #escape
                break
            elif key==32:   #space
                trigger=True   #refresh frame
            elif key==9:    #tab
                #path= input("enter path ")
                #print("\n")
                imageName=input("enter file name ")
                print("\n")
                self._captureManager.saveImage(imageName=imageName+'.jpg')

            elif key==ord("e"):

                _edgeThreshold = self._edgeTrackBar.getBar

                frame=self._captureManager.getFrame
                edges=self._processingTools.detectEdges(frame,1-float(_edgeThreshold/100))
                self._captureManager.showFrame("edges", edges)



        self._captureManager.cameraRelease()



if __name__ == "__main__":
    TestClass().runGetFrame()
