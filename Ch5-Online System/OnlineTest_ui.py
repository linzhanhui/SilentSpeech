# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'online_test.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1436, 1093)
        MainWindow.setAutoFillBackground(False)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout_6 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.verticalLayout_5 = QVBoxLayout()
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label_6 = QLabel(self.centralwidget)
        self.label_6.setObjectName(u"label_6")
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_6.sizePolicy().hasHeightForWidth())
        self.label_6.setSizePolicy(sizePolicy)
        self.label_6.setMinimumSize(QSize(55, 26))
        font = QFont()
        font.setBold(True)
        self.label_6.setFont(font)

        self.horizontalLayout_2.addWidget(self.label_6)

        self.DetectionMode = QComboBox(self.centralwidget)
        self.DetectionMode.addItem("")
        self.DetectionMode.addItem("")
        self.DetectionMode.addItem("")
        self.DetectionMode.setObjectName(u"DetectionMode")

        self.horizontalLayout_2.addWidget(self.DetectionMode)

        self.BeginButton = QPushButton(self.centralwidget)
        self.BeginButton.setObjectName(u"BeginButton")
        self.BeginButton.setFont(font)

        self.horizontalLayout_2.addWidget(self.BeginButton)


        self.horizontalLayout_6.addLayout(self.horizontalLayout_2)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_6.addItem(self.horizontalSpacer)

        self.label_3 = QLabel(self.centralwidget)
        self.label_3.setObjectName(u"label_3")
        font1 = QFont()
        font1.setFamily(u"Songti SC")
        font1.setPointSize(20)
        font1.setBold(True)
        self.label_3.setFont(font1)

        self.horizontalLayout_6.addWidget(self.label_3)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_6.addItem(self.horizontalSpacer_2)

        self.IndicatorLayout = QHBoxLayout()
        self.IndicatorLayout.setObjectName(u"IndicatorLayout")

        self.horizontalLayout_6.addLayout(self.IndicatorLayout)

        self.horizontalLayout_6.setStretch(0, 3)
        self.horizontalLayout_6.setStretch(1, 2)
        self.horizontalLayout_6.setStretch(2, 1)
        self.horizontalLayout_6.setStretch(3, 4)
        self.horizontalLayout_6.setStretch(4, 1)

        self.verticalLayout_5.addLayout(self.horizontalLayout_6)

        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setVerticalSpacing(4)
        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setSpacing(9)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.label_8 = QLabel(self.centralwidget)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setFont(font)

        self.horizontalLayout_4.addWidget(self.label_8)

        self.Threshold = QSlider(self.centralwidget)
        self.Threshold.setObjectName(u"Threshold")
        self.Threshold.setMinimum(1)
        self.Threshold.setMaximum(20)
        self.Threshold.setSingleStep(1)
        self.Threshold.setPageStep(5)
        self.Threshold.setValue(10)
        self.Threshold.setOrientation(Qt.Horizontal)
        self.Threshold.setInvertedAppearance(False)
        self.Threshold.setInvertedControls(False)

        self.horizontalLayout_4.addWidget(self.Threshold)


        self.verticalLayout_4.addLayout(self.horizontalLayout_4)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setFont(font)

        self.horizontalLayout_5.addWidget(self.label_2)

        self.FilterOn = QCheckBox(self.centralwidget)
        self.FilterOn.setObjectName(u"FilterOn")
        self.FilterOn.setLayoutDirection(Qt.RightToLeft)
        self.FilterOn.setChecked(True)

        self.horizontalLayout_5.addWidget(self.FilterOn)


        self.verticalLayout_4.addLayout(self.horizontalLayout_5)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label_7 = QLabel(self.centralwidget)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setFont(font)

        self.horizontalLayout_3.addWidget(self.label_7)

        self.Sensitivity = QSlider(self.centralwidget)
        self.Sensitivity.setObjectName(u"Sensitivity")
        self.Sensitivity.setMinimum(1)
        self.Sensitivity.setMaximum(64)
        self.Sensitivity.setValue(32)
        self.Sensitivity.setOrientation(Qt.Horizontal)
        self.Sensitivity.setInvertedAppearance(False)
        self.Sensitivity.setInvertedControls(False)

        self.horizontalLayout_3.addWidget(self.Sensitivity)


        self.verticalLayout_4.addLayout(self.horizontalLayout_3)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label_5 = QLabel(self.centralwidget)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setFont(font)

        self.horizontalLayout.addWidget(self.label_5)

        self.SubjectID = QLineEdit(self.centralwidget)
        self.SubjectID.setObjectName(u"SubjectID")
        font2 = QFont()
        font2.setFamily(u"Times New Roman")
        self.SubjectID.setFont(font2)

        self.horizontalLayout.addWidget(self.SubjectID)


        self.verticalLayout_4.addLayout(self.horizontalLayout)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setSpacing(9)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(-1, 0, -1, 0)
        self.StartButton = QPushButton(self.centralwidget)
        self.StartButton.setObjectName(u"StartButton")
        self.StartButton.setMinimumSize(QSize(5, 60))
        self.StartButton.setFont(font)

        self.verticalLayout_2.addWidget(self.StartButton)

        self.StopButton = QPushButton(self.centralwidget)
        self.StopButton.setObjectName(u"StopButton")
        self.StopButton.setMinimumSize(QSize(0, 60))
        self.StopButton.setFont(font)

        self.verticalLayout_2.addWidget(self.StopButton)

        self.verticalLayout_2.setStretch(0, 1)

        self.verticalLayout_4.addLayout(self.verticalLayout_2)

        self.verticalLayout_4.setStretch(0, 1)
        self.verticalLayout_4.setStretch(1, 1)
        self.verticalLayout_4.setStretch(2, 1)
        self.verticalLayout_4.setStretch(3, 1)
        self.verticalLayout_4.setStretch(4, 4)

        self.gridLayout.addLayout(self.verticalLayout_4, 0, 1, 1, 1)

        self.horizontalLayout_16 = QHBoxLayout()
        self.horizontalLayout_16.setObjectName(u"horizontalLayout_16")
        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_16.addItem(self.horizontalSpacer_6)

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(-1, 0, -1, 7)
        self.PredResult = QLabel(self.centralwidget)
        self.PredResult.setObjectName(u"PredResult")
        sizePolicy.setHeightForWidth(self.PredResult.sizePolicy().hasHeightForWidth())
        self.PredResult.setSizePolicy(sizePolicy)
        self.PredResult.setMinimumSize(QSize(400, 400))
        self.PredResult.setMaximumSize(QSize(400, 400))

        self.verticalLayout_3.addWidget(self.PredResult)

        self.horizontalLayout_13 = QHBoxLayout()
        self.horizontalLayout_13.setSpacing(0)
        self.horizontalLayout_13.setObjectName(u"horizontalLayout_13")
        self.horizontalLayout_13.setContentsMargins(-1, 9, -1, 9)
        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Preferred, QSizePolicy.Minimum)

        self.horizontalLayout_13.addItem(self.horizontalSpacer_3)

        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy1)
        self.label.setMinimumSize(QSize(68, 24))
        font3 = QFont()
        font3.setFamily(u"Songti SC")
        font3.setPointSize(17)
        font3.setBold(True)
        self.label.setFont(font3)

        self.horizontalLayout_13.addWidget(self.label)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Preferred, QSizePolicy.Minimum)

        self.horizontalLayout_13.addItem(self.horizontalSpacer_4)

        self.horizontalLayout_13.setStretch(0, 1)
        self.horizontalLayout_13.setStretch(2, 1)

        self.verticalLayout_3.addLayout(self.horizontalLayout_13)

        self.verticalLayout_3.setStretch(1, 1)

        self.horizontalLayout_16.addLayout(self.verticalLayout_3)

        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_16.addItem(self.horizontalSpacer_5)

        self.horizontalLayout_16.setStretch(0, 1)
        self.horizontalLayout_16.setStretch(2, 1)

        self.gridLayout.addLayout(self.horizontalLayout_16, 0, 0, 1, 1)

        self.EMGPlotLayout = QHBoxLayout()
        self.EMGPlotLayout.setObjectName(u"EMGPlotLayout")

        self.gridLayout.addLayout(self.EMGPlotLayout, 1, 0, 1, 1)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.label_12 = QLabel(self.centralwidget)
        self.label_12.setObjectName(u"label_12")
        self.label_12.setFont(font)

        self.horizontalLayout_7.addWidget(self.label_12)

        self.RangePlusButton = QPushButton(self.centralwidget)
        self.RangePlusButton.setObjectName(u"RangePlusButton")

        self.horizontalLayout_7.addWidget(self.RangePlusButton)

        self.RangeMinusButton = QPushButton(self.centralwidget)
        self.RangeMinusButton.setObjectName(u"RangeMinusButton")

        self.horizontalLayout_7.addWidget(self.RangeMinusButton)


        self.verticalLayout.addLayout(self.horizontalLayout_7)

        self.horizontalLayout_9 = QHBoxLayout()
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.label_14 = QLabel(self.centralwidget)
        self.label_14.setObjectName(u"label_14")
        self.label_14.setFont(font)

        self.horizontalLayout_9.addWidget(self.label_14)

        self.WindowLen = QComboBox(self.centralwidget)
        self.WindowLen.addItem("")
        self.WindowLen.addItem("")
        self.WindowLen.addItem("")
        self.WindowLen.setObjectName(u"WindowLen")

        self.horizontalLayout_9.addWidget(self.WindowLen)


        self.verticalLayout.addLayout(self.horizontalLayout_9)

        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.label_13 = QLabel(self.centralwidget)
        self.label_13.setObjectName(u"label_13")
        self.label_13.setFont(font)

        self.horizontalLayout_8.addWidget(self.label_13)

        self.FilterSelect = QComboBox(self.centralwidget)
        self.FilterSelect.addItem("")
        self.FilterSelect.addItem("")
        self.FilterSelect.addItem("")
        self.FilterSelect.addItem("")
        self.FilterSelect.setObjectName(u"FilterSelect")

        self.horizontalLayout_8.addWidget(self.FilterSelect)


        self.verticalLayout.addLayout(self.horizontalLayout_8)

        self.horizontalLayout_10 = QHBoxLayout()
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.label_15 = QLabel(self.centralwidget)
        self.label_15.setObjectName(u"label_15")
        self.label_15.setFont(font)

        self.horizontalLayout_10.addWidget(self.label_15)

        self.FilterOrderSelect = QComboBox(self.centralwidget)
        self.FilterOrderSelect.addItem("")
        self.FilterOrderSelect.addItem("")
        self.FilterOrderSelect.addItem("")
        self.FilterOrderSelect.addItem("")
        self.FilterOrderSelect.addItem("")
        self.FilterOrderSelect.addItem("")
        self.FilterOrderSelect.addItem("")
        self.FilterOrderSelect.addItem("")
        self.FilterOrderSelect.addItem("")
        self.FilterOrderSelect.addItem("")
        self.FilterOrderSelect.setObjectName(u"FilterOrderSelect")
        self.FilterOrderSelect.setMaxVisibleItems(5)

        self.horizontalLayout_10.addWidget(self.FilterOrderSelect)


        self.verticalLayout.addLayout(self.horizontalLayout_10)

        self.horizontalLayout_11 = QHBoxLayout()
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.label_16 = QLabel(self.centralwidget)
        self.label_16.setObjectName(u"label_16")
        self.label_16.setFont(font)

        self.horizontalLayout_11.addWidget(self.label_16)

        self.CutoffLow = QLineEdit(self.centralwidget)
        self.CutoffLow.setObjectName(u"CutoffLow")

        self.horizontalLayout_11.addWidget(self.CutoffLow)

        self.CutoffHigh = QLineEdit(self.centralwidget)
        self.CutoffHigh.setObjectName(u"CutoffHigh")

        self.horizontalLayout_11.addWidget(self.CutoffHigh)


        self.verticalLayout.addLayout(self.horizontalLayout_11)

        self.horizontalLayout_12 = QHBoxLayout()
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.label_17 = QLabel(self.centralwidget)
        self.label_17.setObjectName(u"label_17")
        self.label_17.setFont(font)

        self.horizontalLayout_12.addWidget(self.label_17)

        self.NotchOn = QCheckBox(self.centralwidget)
        self.NotchOn.setObjectName(u"NotchOn")
        self.NotchOn.setChecked(True)

        self.horizontalLayout_12.addWidget(self.NotchOn)


        self.verticalLayout.addLayout(self.horizontalLayout_12)

        self.SetFilter = QPushButton(self.centralwidget)
        self.SetFilter.setObjectName(u"SetFilter")
        self.SetFilter.setMinimumSize(QSize(0, 50))
        self.SetFilter.setFont(font)

        self.verticalLayout.addWidget(self.SetFilter)


        self.gridLayout.addLayout(self.verticalLayout, 1, 1, 1, 1)

        self.gridLayout.setRowStretch(1, 1)
        self.gridLayout.setColumnStretch(0, 10)
        self.gridLayout.setColumnStretch(1, 1)

        self.verticalLayout_5.addLayout(self.gridLayout)


        self.verticalLayout_6.addLayout(self.verticalLayout_5)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1436, 28))
        MainWindow.setMenuBar(self.menubar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"\u68c0\u6d4b\u6a21\u5f0f", None))
        self.DetectionMode.setItemText(0, QCoreApplication.translate("MainWindow", u"Threshold", None))
        self.DetectionMode.setItemText(1, QCoreApplication.translate("MainWindow", u"Button", None))
        self.DetectionMode.setItemText(2, QCoreApplication.translate("MainWindow", u"Model", None))

        self.BeginButton.setText(QCoreApplication.translate("MainWindow", u"Begin", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"\u5728\u7ebf\u6d4b\u8bd5\u7a0b\u5e8f", None))
        self.label_8.setText(QCoreApplication.translate("MainWindow", u"\u9608\u503c", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"\u542f\u7528\u6ee4\u6ce2", None))
        self.FilterOn.setText("")
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"\u7075\u654f\u5ea6", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"\u53d7\u8bd5ID", None))
        self.SubjectID.setText(QCoreApplication.translate("MainWindow", u"1", None))
        self.StartButton.setText(QCoreApplication.translate("MainWindow", u"\u5f00\u59cb\u6d4b\u8bd5", None))
        self.StopButton.setText(QCoreApplication.translate("MainWindow", u"\u7ed3\u675f\u6d4b\u8bd5", None))
        self.PredResult.setText("")
        self.label.setText(QCoreApplication.translate("MainWindow", u"\u9884\u6d4b\u53d1\u97f3", None))
        self.label_12.setText(QCoreApplication.translate("MainWindow", u"Scale", None))
        self.RangePlusButton.setText(QCoreApplication.translate("MainWindow", u"+", None))
        self.RangeMinusButton.setText(QCoreApplication.translate("MainWindow", u"-", None))
        self.label_14.setText(QCoreApplication.translate("MainWindow", u"\u7a97\u53e3\u957f\u5ea6", None))
        self.WindowLen.setItemText(0, QCoreApplication.translate("MainWindow", u"0.1s", None))
        self.WindowLen.setItemText(1, QCoreApplication.translate("MainWindow", u"1s", None))
        self.WindowLen.setItemText(2, QCoreApplication.translate("MainWindow", u"10s", None))

        self.WindowLen.setCurrentText(QCoreApplication.translate("MainWindow", u"0.1s", None))
        self.label_13.setText(QCoreApplication.translate("MainWindow", u"\u6ee4\u6ce2\u5668", None))
        self.FilterSelect.setItemText(0, QCoreApplication.translate("MainWindow", u"\u4e0d\u6ee4\u6ce2", None))
        self.FilterSelect.setItemText(1, QCoreApplication.translate("MainWindow", u"lowpass", None))
        self.FilterSelect.setItemText(2, QCoreApplication.translate("MainWindow", u"highpass", None))
        self.FilterSelect.setItemText(3, QCoreApplication.translate("MainWindow", u"bandpass", None))

        self.FilterSelect.setCurrentText(QCoreApplication.translate("MainWindow", u"\u4e0d\u6ee4\u6ce2", None))
        self.label_15.setText(QCoreApplication.translate("MainWindow", u"\u9636\u6570", None))
        self.FilterOrderSelect.setItemText(0, QCoreApplication.translate("MainWindow", u"1", None))
        self.FilterOrderSelect.setItemText(1, QCoreApplication.translate("MainWindow", u"2", None))
        self.FilterOrderSelect.setItemText(2, QCoreApplication.translate("MainWindow", u"3", None))
        self.FilterOrderSelect.setItemText(3, QCoreApplication.translate("MainWindow", u"4", None))
        self.FilterOrderSelect.setItemText(4, QCoreApplication.translate("MainWindow", u"5", None))
        self.FilterOrderSelect.setItemText(5, QCoreApplication.translate("MainWindow", u"6", None))
        self.FilterOrderSelect.setItemText(6, QCoreApplication.translate("MainWindow", u"7", None))
        self.FilterOrderSelect.setItemText(7, QCoreApplication.translate("MainWindow", u"8", None))
        self.FilterOrderSelect.setItemText(8, QCoreApplication.translate("MainWindow", u"9", None))
        self.FilterOrderSelect.setItemText(9, QCoreApplication.translate("MainWindow", u"10", None))

        self.FilterOrderSelect.setCurrentText(QCoreApplication.translate("MainWindow", u"1", None))
        self.label_16.setText(QCoreApplication.translate("MainWindow", u"\u622a\u6b62\u9891\u7387", None))
        self.CutoffLow.setText(QCoreApplication.translate("MainWindow", u"10", None))
        self.CutoffHigh.setText(QCoreApplication.translate("MainWindow", u"499.5", None))
        self.label_17.setText(QCoreApplication.translate("MainWindow", u"\u542f\u752850Hz Notch", None))
        self.NotchOn.setText("")
        self.SetFilter.setText(QCoreApplication.translate("MainWindow", u"Set", None))
    # retranslateUi

