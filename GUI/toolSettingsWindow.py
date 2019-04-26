# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'toolSettingsWindow.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_ToolSettingsWindow(object):
    def setupUi(self, ToolSettingsWindow):
        ToolSettingsWindow.setObjectName(_fromUtf8("ToolSettingsWindow"))
        ToolSettingsWindow.setWindowModality(QtCore.Qt.ApplicationModal)
        ToolSettingsWindow.resize(750, 400)
        ToolSettingsWindow.setMinimumSize(QtCore.QSize(750, 400))
        ToolSettingsWindow.setUnifiedTitleAndToolBarOnMac(False)
        self.centralwidget = QtGui.QWidget(ToolSettingsWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.gridLayout = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 1, 0, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 1, 2, 1, 1)
        spacerItem2 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem2, 0, 1, 1, 1)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.label = QtGui.QLabel(self.centralwidget)
        self.label.setText(_fromUtf8(""))
        self.label.setPixmap(QtGui.QPixmap(_fromUtf8("../icons/icon---color-pixel.png")))
        self.label.setScaledContents(True)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setWordWrap(False)
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout.addWidget(self.label)
        self.ColoredPixelButton = QtGui.QPushButton(self.centralwidget)
        self.ColoredPixelButton.setMinimumSize(QtCore.QSize(200, 0))
        self.ColoredPixelButton.setObjectName(_fromUtf8("ColoredPixelButton"))
        self.verticalLayout.addWidget(self.ColoredPixelButton)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.verticalLayout_3 = QtGui.QVBoxLayout()
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.label_4 = QtGui.QLabel(self.centralwidget)
        self.label_4.setText(_fromUtf8(""))
        self.label_4.setPixmap(QtGui.QPixmap(_fromUtf8("../icons/icon---measurement.png")))
        self.label_4.setScaledContents(True)
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setWordWrap(False)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.verticalLayout_3.addWidget(self.label_4)
        self.measurementButton = QtGui.QPushButton(self.centralwidget)
        self.measurementButton.setMinimumSize(QtCore.QSize(200, 0))
        self.measurementButton.setObjectName(_fromUtf8("measurementButton"))
        self.verticalLayout_3.addWidget(self.measurementButton)
        self.horizontalLayout.addLayout(self.verticalLayout_3)
        self.verticalLayout_4 = QtGui.QVBoxLayout()
        self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
        self.label_5 = QtGui.QLabel(self.centralwidget)
        self.label_5.setText(_fromUtf8(""))
        self.label_5.setPixmap(QtGui.QPixmap(_fromUtf8("../icons/icon---pattern.png")))
        self.label_5.setScaledContents(True)
        self.label_5.setAlignment(QtCore.Qt.AlignCenter)
        self.label_5.setWordWrap(False)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.verticalLayout_4.addWidget(self.label_5)
        self.patternDetectionButton = QtGui.QPushButton(self.centralwidget)
        self.patternDetectionButton.setMinimumSize(QtCore.QSize(200, 0))
        self.patternDetectionButton.setObjectName(_fromUtf8("patternDetectionButton"))
        self.verticalLayout_4.addWidget(self.patternDetectionButton)
        self.horizontalLayout.addLayout(self.verticalLayout_4)
        self.gridLayout.addLayout(self.horizontalLayout, 1, 1, 1, 1)
        spacerItem3 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem3, 2, 1, 1, 1)
        ToolSettingsWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(ToolSettingsWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 750, 25))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        ToolSettingsWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(ToolSettingsWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        ToolSettingsWindow.setStatusBar(self.statusbar)

        self.retranslateUi(ToolSettingsWindow)
        QtCore.QObject.connect(self.ColoredPixelButton, QtCore.SIGNAL(_fromUtf8("clicked()")), ToolSettingsWindow.ColorePixelSelected)
        QtCore.QObject.connect(self.measurementButton, QtCore.SIGNAL(_fromUtf8("clicked()")), ToolSettingsWindow.measurementSelected)
        QtCore.QObject.connect(self.patternDetectionButton, QtCore.SIGNAL(_fromUtf8("clicked()")), ToolSettingsWindow.patternDetectionSelected)
        QtCore.QMetaObject.connectSlotsByName(ToolSettingsWindow)
        ToolSettingsWindow.setTabOrder(self.ColoredPixelButton, self.measurementButton)
        ToolSettingsWindow.setTabOrder(self.measurementButton, self.patternDetectionButton)

    def retranslateUi(self, ToolSettingsWindow):
        ToolSettingsWindow.setWindowTitle(_translate("ToolSettingsWindow", "Tool Settings", None))
        self.ColoredPixelButton.setText(_translate("ToolSettingsWindow", "Colored pixel count", None))
        self.measurementButton.setText(_translate("ToolSettingsWindow", "measurement", None))
        self.patternDetectionButton.setText(_translate("ToolSettingsWindow", "pattern detection", None))

