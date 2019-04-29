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

    def showToolSettings1(self):
        self._interface.showToolSettings(1)


    def showToolSettings2(self):
        self._interface.showToolSettings(2)


    def showToolSettings3(self):
        self._interface.showToolSettings(3)


    def showToolSettings4(self):
        self._interface.showToolSettings(4)

    def saveMasterFrame(self):

        self.snapshot()
        self._interface.saveMaster()
