from PyQt4 import QtGui



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

    def liveStream(self):

        self._interface.liveStream()


    def saveMasterFrame(self):
        masterName=("MasterImage"+ str(self._interface.captureManager.getProgramNumber)+".jpg")
        print(masterName)
        self._interface.captureManager.saveImage(self._interface.frame,"./Masters/",masterName)
