# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'setupWindow.ui'
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

class Ui_SetupWindow(object):
    def setupUi(self, SetupWindow):
        SetupWindow.setObjectName(_fromUtf8("SetupWindow"))
        SetupWindow.setWindowModality(QtCore.Qt.WindowModal)
        SetupWindow.resize(1085, 630)
        SetupWindow.setFocusPolicy(QtCore.Qt.NoFocus)
        self.centralwidget = QtGui.QWidget(SetupWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.gridLayout = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.ImagePreview = QtGui.QLabel(self.centralwidget)
        self.ImagePreview.setMinimumSize(QtCore.QSize(600, 400))
        self.ImagePreview.setBaseSize(QtCore.QSize(600, 400))
        self.ImagePreview.setMouseTracking(True)
        self.ImagePreview.setFrameShape(QtGui.QFrame.Box)
        self.ImagePreview.setFrameShadow(QtGui.QFrame.Plain)
        self.ImagePreview.setText(_fromUtf8(""))
        self.ImagePreview.setTextFormat(QtCore.Qt.AutoText)
        self.ImagePreview.setPixmap(QtGui.QPixmap(_fromUtf8("../pictures/ADDIXO.png")))
        self.ImagePreview.setScaledContents(True)
        self.ImagePreview.setAlignment(QtCore.Qt.AlignCenter)
        self.ImagePreview.setWordWrap(False)
        self.ImagePreview.setObjectName(_fromUtf8("ImagePreview"))
        self.gridLayout.addWidget(self.ImagePreview, 1, 0, 1, 1)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.saveMasterImage = QtGui.QPushButton(self.centralwidget)
        self.saveMasterImage.setObjectName(_fromUtf8("saveMasterImage"))
        self.horizontalLayout.addWidget(self.saveMasterImage)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.pushButton = QtGui.QPushButton(self.centralwidget)
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.horizontalLayout.addWidget(self.pushButton)
        self.saveMasterImage_2 = QtGui.QPushButton(self.centralwidget)
        self.saveMasterImage_2.setObjectName(_fromUtf8("saveMasterImage_2"))
        self.horizontalLayout.addWidget(self.saveMasterImage_2)
        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(116, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 1, 4, 1, 1)
        spacerItem2 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem2, 2, 0, 1, 1)
        SetupWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(SetupWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1085, 25))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        SetupWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(SetupWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        SetupWindow.setStatusBar(self.statusbar)

        self.retranslateUi(SetupWindow)
        QtCore.QObject.connect(self.saveMasterImage_2, QtCore.SIGNAL(_fromUtf8("clicked()")), SetupWindow.snapshot)
        QtCore.QObject.connect(self.saveMasterImage, QtCore.SIGNAL(_fromUtf8("clicked()")), SetupWindow.saveMasterFrame)
        QtCore.QObject.connect(self.pushButton, QtCore.SIGNAL(_fromUtf8("clicked()")), SetupWindow.liveStream)
        QtCore.QMetaObject.connectSlotsByName(SetupWindow)

    def retranslateUi(self, SetupWindow):
        SetupWindow.setWindowTitle(_translate("SetupWindow", "Setup", None))
        self.saveMasterImage.setText(_translate("SetupWindow", "Save Master Image", None))
        self.pushButton.setText(_translate("SetupWindow", "Retake Image", None))
        self.saveMasterImage_2.setText(_translate("SetupWindow", "snapshot Image", None))

