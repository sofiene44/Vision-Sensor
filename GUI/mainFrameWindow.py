# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainFrameWindow.ui'
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

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.setWindowModality(QtCore.Qt.ApplicationModal)
        MainWindow.setEnabled(True)
        MainWindow.resize(1080, 600)
        MainWindow.setMinimumSize(QtCore.QSize(1080, 600))
        MainWindow.setBaseSize(QtCore.QSize(1080, 600))
        MainWindow.setTabShape(QtGui.QTabWidget.Rounded)
        self.background = QtGui.QWidget(MainWindow)
        self.background.setObjectName(_fromUtf8("background"))
        self.gridLayout = QtGui.QGridLayout(self.background)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.horizontalLayout_5 = QtGui.QHBoxLayout()
        self.horizontalLayout_5.setObjectName(_fromUtf8("horizontalLayout_5"))
        self.ManualTrigger = QtGui.QPushButton(self.background)
        self.ManualTrigger.setObjectName(_fromUtf8("ManualTrigger"))
        self.horizontalLayout_5.addWidget(self.ManualTrigger)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem)
        self.pushButton = QtGui.QPushButton(self.background)
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.horizontalLayout_5.addWidget(self.pushButton)
        self.gridLayout.addLayout(self.horizontalLayout_5, 1, 0, 1, 1)
        self.ToolsList = QtGui.QVBoxLayout()
        self.ToolsList.setObjectName(_fromUtf8("ToolsList"))
        self.Tool1 = QtGui.QHBoxLayout()
        self.Tool1.setObjectName(_fromUtf8("Tool1"))
        self.ToolName1 = QtGui.QLabel(self.background)
        self.ToolName1.setEnabled(False)
        self.ToolName1.setObjectName(_fromUtf8("ToolName1"))
        self.Tool1.addWidget(self.ToolName1)
        self.gridLayout_6 = QtGui.QGridLayout()
        self.gridLayout_6.setObjectName(_fromUtf8("gridLayout_6"))
        self.ThreshSlider1 = QtGui.QSlider(self.background)
        self.ThreshSlider1.setEnabled(False)
        self.ThreshSlider1.setMaximum(100)
        self.ThreshSlider1.setOrientation(QtCore.Qt.Horizontal)
        self.ThreshSlider1.setInvertedAppearance(False)
        self.ThreshSlider1.setInvertedControls(False)
        self.ThreshSlider1.setObjectName(_fromUtf8("ThreshSlider1"))
        self.gridLayout_6.addWidget(self.ThreshSlider1, 2, 0, 1, 1)
        self.horizontalLayout_10 = QtGui.QHBoxLayout()
        self.horizontalLayout_10.setObjectName(_fromUtf8("horizontalLayout_10"))
        self.ThreshValue1 = QtGui.QLabel(self.background)
        self.ThreshValue1.setMaximumSize(QtCore.QSize(50, 50))
        self.ThreshValue1.setTextFormat(QtCore.Qt.PlainText)
        self.ThreshValue1.setScaledContents(False)
        self.ThreshValue1.setAlignment(QtCore.Qt.AlignCenter)
        self.ThreshValue1.setObjectName(_fromUtf8("ThreshValue1"))
        self.horizontalLayout_10.addWidget(self.ThreshValue1)
        self.gridLayout_6.addLayout(self.horizontalLayout_10, 1, 0, 1, 1)
        self.Tool1.addLayout(self.gridLayout_6)
        self.Enable1 = QtGui.QCheckBox(self.background)
        self.Enable1.setObjectName(_fromUtf8("Enable1"))
        self.Tool1.addWidget(self.Enable1)
        self.ToolSettings1 = QtGui.QToolButton(self.background)
        self.ToolSettings1.setEnabled(False)
        self.ToolSettings1.setObjectName(_fromUtf8("ToolSettings1"))
        self.Tool1.addWidget(self.ToolSettings1)
        self.ToolsList.addLayout(self.Tool1)
        self.Tool2 = QtGui.QHBoxLayout()
        self.Tool2.setObjectName(_fromUtf8("Tool2"))
        self.ToolName2 = QtGui.QLabel(self.background)
        self.ToolName2.setEnabled(False)
        self.ToolName2.setObjectName(_fromUtf8("ToolName2"))
        self.Tool2.addWidget(self.ToolName2)
        self.gridLayout_9 = QtGui.QGridLayout()
        self.gridLayout_9.setObjectName(_fromUtf8("gridLayout_9"))
        self.ThreshSlider2 = QtGui.QSlider(self.background)
        self.ThreshSlider2.setEnabled(False)
        self.ThreshSlider2.setMaximum(100)
        self.ThreshSlider2.setOrientation(QtCore.Qt.Horizontal)
        self.ThreshSlider2.setInvertedAppearance(False)
        self.ThreshSlider2.setInvertedControls(False)
        self.ThreshSlider2.setObjectName(_fromUtf8("ThreshSlider2"))
        self.gridLayout_9.addWidget(self.ThreshSlider2, 2, 0, 1, 1)
        self.horizontalLayout_12 = QtGui.QHBoxLayout()
        self.horizontalLayout_12.setObjectName(_fromUtf8("horizontalLayout_12"))
        self.ThreshValue2 = QtGui.QLabel(self.background)
        self.ThreshValue2.setMaximumSize(QtCore.QSize(50, 50))
        self.ThreshValue2.setTextFormat(QtCore.Qt.PlainText)
        self.ThreshValue2.setScaledContents(False)
        self.ThreshValue2.setAlignment(QtCore.Qt.AlignCenter)
        self.ThreshValue2.setObjectName(_fromUtf8("ThreshValue2"))
        self.horizontalLayout_12.addWidget(self.ThreshValue2)
        self.gridLayout_9.addLayout(self.horizontalLayout_12, 1, 0, 1, 1)
        self.Tool2.addLayout(self.gridLayout_9)
        self.Enable2 = QtGui.QCheckBox(self.background)
        self.Enable2.setObjectName(_fromUtf8("Enable2"))
        self.Tool2.addWidget(self.Enable2)
        self.ToolSettings2 = QtGui.QToolButton(self.background)
        self.ToolSettings2.setEnabled(False)
        self.ToolSettings2.setObjectName(_fromUtf8("ToolSettings2"))
        self.Tool2.addWidget(self.ToolSettings2)
        self.ToolsList.addLayout(self.Tool2)
        self.Tool3 = QtGui.QHBoxLayout()
        self.Tool3.setObjectName(_fromUtf8("Tool3"))
        self.ToolName3 = QtGui.QLabel(self.background)
        self.ToolName3.setEnabled(False)
        self.ToolName3.setObjectName(_fromUtf8("ToolName3"))
        self.Tool3.addWidget(self.ToolName3)
        self.gridLayout_8 = QtGui.QGridLayout()
        self.gridLayout_8.setObjectName(_fromUtf8("gridLayout_8"))
        self.ThreshSlider3 = QtGui.QSlider(self.background)
        self.ThreshSlider3.setEnabled(False)
        self.ThreshSlider3.setMaximum(100)
        self.ThreshSlider3.setOrientation(QtCore.Qt.Horizontal)
        self.ThreshSlider3.setInvertedAppearance(False)
        self.ThreshSlider3.setInvertedControls(False)
        self.ThreshSlider3.setObjectName(_fromUtf8("ThreshSlider3"))
        self.gridLayout_8.addWidget(self.ThreshSlider3, 2, 0, 1, 1)
        self.horizontalLayout_11 = QtGui.QHBoxLayout()
        self.horizontalLayout_11.setObjectName(_fromUtf8("horizontalLayout_11"))
        self.ThreshValue3 = QtGui.QLabel(self.background)
        self.ThreshValue3.setMaximumSize(QtCore.QSize(50, 50))
        self.ThreshValue3.setTextFormat(QtCore.Qt.PlainText)
        self.ThreshValue3.setScaledContents(False)
        self.ThreshValue3.setAlignment(QtCore.Qt.AlignCenter)
        self.ThreshValue3.setObjectName(_fromUtf8("ThreshValue3"))
        self.horizontalLayout_11.addWidget(self.ThreshValue3)
        self.gridLayout_8.addLayout(self.horizontalLayout_11, 1, 0, 1, 1)
        self.Tool3.addLayout(self.gridLayout_8)
        self.Enable3 = QtGui.QCheckBox(self.background)
        self.Enable3.setObjectName(_fromUtf8("Enable3"))
        self.Tool3.addWidget(self.Enable3)
        self.ToolSettings3 = QtGui.QToolButton(self.background)
        self.ToolSettings3.setEnabled(False)
        self.ToolSettings3.setObjectName(_fromUtf8("ToolSettings3"))
        self.Tool3.addWidget(self.ToolSettings3)
        self.ToolsList.addLayout(self.Tool3)
        self.Tool4 = QtGui.QHBoxLayout()
        self.Tool4.setObjectName(_fromUtf8("Tool4"))
        self.ToolName4 = QtGui.QLabel(self.background)
        self.ToolName4.setEnabled(False)
        self.ToolName4.setObjectName(_fromUtf8("ToolName4"))
        self.Tool4.addWidget(self.ToolName4)
        self.gridLayout_10 = QtGui.QGridLayout()
        self.gridLayout_10.setObjectName(_fromUtf8("gridLayout_10"))
        self.ThreshSlider4 = QtGui.QSlider(self.background)
        self.ThreshSlider4.setEnabled(False)
        self.ThreshSlider4.setMaximum(100)
        self.ThreshSlider4.setOrientation(QtCore.Qt.Horizontal)
        self.ThreshSlider4.setInvertedAppearance(False)
        self.ThreshSlider4.setInvertedControls(False)
        self.ThreshSlider4.setObjectName(_fromUtf8("ThreshSlider4"))
        self.gridLayout_10.addWidget(self.ThreshSlider4, 2, 0, 1, 1)
        self.horizontalLayout_13 = QtGui.QHBoxLayout()
        self.horizontalLayout_13.setObjectName(_fromUtf8("horizontalLayout_13"))
        self.ThreshValue4 = QtGui.QLabel(self.background)
        self.ThreshValue4.setMaximumSize(QtCore.QSize(50, 50))
        self.ThreshValue4.setTextFormat(QtCore.Qt.PlainText)
        self.ThreshValue4.setScaledContents(False)
        self.ThreshValue4.setAlignment(QtCore.Qt.AlignCenter)
        self.ThreshValue4.setObjectName(_fromUtf8("ThreshValue4"))
        self.horizontalLayout_13.addWidget(self.ThreshValue4)
        self.gridLayout_10.addLayout(self.horizontalLayout_13, 1, 0, 1, 1)
        self.Tool4.addLayout(self.gridLayout_10)
        self.Enable4 = QtGui.QCheckBox(self.background)
        self.Enable4.setObjectName(_fromUtf8("Enable4"))
        self.Tool4.addWidget(self.Enable4)
        self.ToolSettings4 = QtGui.QToolButton(self.background)
        self.ToolSettings4.setEnabled(False)
        self.ToolSettings4.setObjectName(_fromUtf8("ToolSettings4"))
        self.Tool4.addWidget(self.ToolSettings4)
        self.ToolsList.addLayout(self.Tool4)
        self.gridLayout.addLayout(self.ToolsList, 2, 1, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem1, 3, 0, 1, 1)
        self.ImagePreview = QtGui.QLabel(self.background)
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
        self.gridLayout.addWidget(self.ImagePreview, 2, 0, 1, 1)
        self.horizontalLayout_14 = QtGui.QHBoxLayout()
        self.horizontalLayout_14.setObjectName(_fromUtf8("horizontalLayout_14"))
        self.programsList = QtGui.QComboBox(self.background)
        self.programsList.setObjectName(_fromUtf8("programsList"))
        self.programsList.addItem(_fromUtf8(""))
        self.programsList.addItem(_fromUtf8(""))
        self.programsList.addItem(_fromUtf8(""))
        self.programsList.addItem(_fromUtf8(""))
        self.programsList.addItem(_fromUtf8(""))
        self.programsList.addItem(_fromUtf8(""))
        self.horizontalLayout_14.addWidget(self.programsList)
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_14.addItem(spacerItem2)
        self.gridLayout.addLayout(self.horizontalLayout_14, 1, 1, 1, 1)
        MainWindow.setCentralWidget(self.background)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1080, 25))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QObject.connect(self.Enable1, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.ThreshSlider1.setEnabled)
        QtCore.QObject.connect(self.Enable1, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.ToolSettings1.setEnabled)
        QtCore.QObject.connect(self.ThreshSlider1, QtCore.SIGNAL(_fromUtf8("valueChanged(int)")), self.ThreshValue1.setNum)
        QtCore.QObject.connect(self.Enable1, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.ToolName1.setEnabled)
        QtCore.QObject.connect(self.Enable2, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.ThreshSlider2.setEnabled)
        QtCore.QObject.connect(self.Enable2, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.ToolName2.setEnabled)
        QtCore.QObject.connect(self.Enable2, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.ToolSettings2.setEnabled)
        QtCore.QObject.connect(self.ThreshSlider2, QtCore.SIGNAL(_fromUtf8("valueChanged(int)")), self.ThreshValue2.setNum)
        QtCore.QObject.connect(self.Enable3, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.ToolName3.setEnabled)
        QtCore.QObject.connect(self.Enable4, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.ToolName4.setEnabled)
        QtCore.QObject.connect(self.Enable3, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.ToolSettings3.setEnabled)
        QtCore.QObject.connect(self.Enable4, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.ToolSettings4.setEnabled)
        QtCore.QObject.connect(self.Enable4, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.ThreshSlider4.setEnabled)
        QtCore.QObject.connect(self.Enable3, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.ThreshSlider3.setEnabled)
        QtCore.QObject.connect(self.ThreshSlider3, QtCore.SIGNAL(_fromUtf8("valueChanged(int)")), self.ThreshValue3.setNum)
        QtCore.QObject.connect(self.ThreshSlider4, QtCore.SIGNAL(_fromUtf8("valueChanged(int)")), self.ThreshValue4.setNum)
        QtCore.QObject.connect(self.ManualTrigger, QtCore.SIGNAL(_fromUtf8("clicked()")), MainWindow.refreshFrame)
        QtCore.QObject.connect(self.ToolSettings1, QtCore.SIGNAL(_fromUtf8("clicked()")), MainWindow.showToolSettings)
        QtCore.QObject.connect(self.pushButton, QtCore.SIGNAL(_fromUtf8("clicked()")), MainWindow.showSetup)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        MainWindow.setTabOrder(self.ManualTrigger, self.programsList)
        MainWindow.setTabOrder(self.programsList, self.Enable1)
        MainWindow.setTabOrder(self.Enable1, self.ToolSettings1)
        MainWindow.setTabOrder(self.ToolSettings1, self.ThreshSlider1)
        MainWindow.setTabOrder(self.ThreshSlider1, self.Enable2)
        MainWindow.setTabOrder(self.Enable2, self.ToolSettings2)
        MainWindow.setTabOrder(self.ToolSettings2, self.ThreshSlider2)
        MainWindow.setTabOrder(self.ThreshSlider2, self.Enable3)
        MainWindow.setTabOrder(self.Enable3, self.ToolSettings3)
        MainWindow.setTabOrder(self.ToolSettings3, self.ThreshSlider3)
        MainWindow.setTabOrder(self.ThreshSlider3, self.Enable4)
        MainWindow.setTabOrder(self.Enable4, self.ToolSettings4)
        MainWindow.setTabOrder(self.ToolSettings4, self.ThreshSlider4)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.ManualTrigger.setText(_translate("MainWindow", "manual Trigger", None))
        self.pushButton.setText(_translate("MainWindow", "Setup", None))
        self.ToolName1.setText(_translate("MainWindow", "Tool 1", None))
        self.ThreshValue1.setText(_translate("MainWindow", "0", None))
        self.Enable1.setText(_translate("MainWindow", "Enable", None))
        self.ToolSettings1.setText(_translate("MainWindow", "...", None))
        self.ToolName2.setText(_translate("MainWindow", "Tool 2 ", None))
        self.ThreshValue2.setText(_translate("MainWindow", "0", None))
        self.Enable2.setText(_translate("MainWindow", "Enable", None))
        self.ToolSettings2.setText(_translate("MainWindow", "...", None))
        self.ToolName3.setText(_translate("MainWindow", "Tool 3 ", None))
        self.ThreshValue3.setText(_translate("MainWindow", "0", None))
        self.Enable3.setText(_translate("MainWindow", "Enable", None))
        self.ToolSettings3.setText(_translate("MainWindow", "...", None))
        self.ToolName4.setText(_translate("MainWindow", "Tool 4 ", None))
        self.ThreshValue4.setText(_translate("MainWindow", "0", None))
        self.Enable4.setText(_translate("MainWindow", "Enable", None))
        self.ToolSettings4.setText(_translate("MainWindow", "...", None))
        self.programsList.setItemText(0, _translate("MainWindow", "P0", None))
        self.programsList.setItemText(1, _translate("MainWindow", "P1", None))
        self.programsList.setItemText(2, _translate("MainWindow", "P2", None))
        self.programsList.setItemText(3, _translate("MainWindow", "P3", None))
        self.programsList.setItemText(4, _translate("MainWindow", "P4", None))
        self.programsList.setItemText(5, _translate("MainWindow", "P5", None))
