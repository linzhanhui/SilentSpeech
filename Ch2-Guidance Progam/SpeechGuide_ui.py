# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'speech_guide.ui'
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
        MainWindow.resize(1437, 1111)
        sizePolicy = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy1)
        self.verticalLayout_8 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.verticalLayout_7 = QVBoxLayout()
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.verticalLayout_9 = QVBoxLayout()
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.horizontalLayout_20 = QHBoxLayout()
        self.horizontalLayout_20.setObjectName(u"horizontalLayout_20")
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label_3 = QLabel(self.centralwidget)
        self.label_3.setObjectName(u"label_3")
        font = QFont()
        font.setBold(True)
        self.label_3.setFont(font)

        self.horizontalLayout_3.addWidget(self.label_3)

        self.CurrentGroup = QLineEdit(self.centralwidget)
        self.CurrentGroup.setObjectName(u"CurrentGroup")
        font1 = QFont()
        font1.setFamily(u"Times New Roman")
        self.CurrentGroup.setFont(font1)

        self.horizontalLayout_3.addWidget(self.CurrentGroup)


        self.horizontalLayout_20.addLayout(self.horizontalLayout_3)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.label_11 = QLabel(self.centralwidget)
        self.label_11.setObjectName(u"label_11")
        self.label_11.setFont(font)

        self.horizontalLayout_6.addWidget(self.label_11)

        self.SpeechMode = QComboBox(self.centralwidget)
        self.SpeechMode.addItem("")
        self.SpeechMode.addItem("")
        self.SpeechMode.setObjectName(u"SpeechMode")

        self.horizontalLayout_6.addWidget(self.SpeechMode)

        self.horizontalLayout_6.setStretch(0, 1)
        self.horizontalLayout_6.setStretch(1, 4)

        self.horizontalLayout_20.addLayout(self.horizontalLayout_6)

        self.horizontalLayout_19 = QHBoxLayout()
        self.horizontalLayout_19.setObjectName(u"horizontalLayout_19")
        self.label_18 = QLabel(self.centralwidget)
        self.label_18.setObjectName(u"label_18")
        self.label_18.setFont(font)

        self.horizontalLayout_19.addWidget(self.label_18)

        self.GainType = QComboBox(self.centralwidget)
        self.GainType.addItem("")
        self.GainType.addItem("")
        self.GainType.addItem("")
        self.GainType.addItem("")
        self.GainType.addItem("")
        self.GainType.addItem("")
        self.GainType.addItem("")
        self.GainType.setObjectName(u"GainType")

        self.horizontalLayout_19.addWidget(self.GainType)


        self.horizontalLayout_20.addLayout(self.horizontalLayout_19)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_20.addItem(self.horizontalSpacer)

        self.LossCheckOn = QCheckBox(self.centralwidget)
        self.LossCheckOn.setObjectName(u"LossCheckOn")
        self.LossCheckOn.setFont(font)
        self.LossCheckOn.setLayoutDirection(Qt.RightToLeft)
        self.LossCheckOn.setChecked(True)

        self.horizontalLayout_20.addWidget(self.LossCheckOn)

        self.horizontalLayout_14 = QHBoxLayout()
        self.horizontalLayout_14.setObjectName(u"horizontalLayout_14")
        self.horizontalSpacer_9 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_14.addItem(self.horizontalSpacer_9)

        self.label_4 = QLabel(self.centralwidget)
        self.label_4.setObjectName(u"label_4")
        sizePolicy2 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy2)
        self.label_4.setFont(font)

        self.horizontalLayout_14.addWidget(self.label_4)

        self.BatteryLevel = QProgressBar(self.centralwidget)
        self.BatteryLevel.setObjectName(u"BatteryLevel")
        font2 = QFont()
        font2.setFamily(u"Times New Roman")
        font2.setPointSize(13)
        font2.setBold(False)
        font2.setItalic(False)
        self.BatteryLevel.setFont(font2)
        self.BatteryLevel.setStyleSheet(u"QProgressBar{\n"
"	font: 13pt \"Times New Roman\";\n"
"	border-radius:5px;\n"
"	text-align:center;\n"
"	border:1px solid #E8EDF2;\n"
"	background-color: transparent;\n"
"	border-color: rgb(180, 180, 180);\n"
"	color: black\n"
"\n"
"}\n"
"QProgressBar:chunk{\n"
"	border-radius:5px;\n"
"	background-color:green;\n"
"}")
        self.BatteryLevel.setValue(100)
        self.BatteryLevel.setInvertedAppearance(False)

        self.horizontalLayout_14.addWidget(self.BatteryLevel)

        self.horizontalLayout_14.setStretch(2, 1)

        self.horizontalLayout_20.addLayout(self.horizontalLayout_14)

        self.LEDLayout = QHBoxLayout()
        self.LEDLayout.setObjectName(u"LEDLayout")

        self.horizontalLayout_20.addLayout(self.LEDLayout)

        self.horizontalLayout_20.setStretch(0, 2)
        self.horizontalLayout_20.setStretch(1, 2)
        self.horizontalLayout_20.setStretch(2, 1)
        self.horizontalLayout_20.setStretch(3, 3)
        self.horizontalLayout_20.setStretch(5, 2)
        self.horizontalLayout_20.setStretch(6, 1)

        self.verticalLayout_9.addLayout(self.horizontalLayout_20)


        self.verticalLayout_7.addLayout(self.verticalLayout_9)

        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.horizontalLayout_16 = QHBoxLayout()
        self.horizontalLayout_16.setObjectName(u"horizontalLayout_16")
        self.horizontalLayout_16.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.horizontalSpacer_7 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_16.addItem(self.horizontalSpacer_7)

        self.verticalLayout_6 = QVBoxLayout()
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.verticalLayout_6.setSizeConstraint(QLayout.SetFixedSize)
        self.CurrentFig = QLabel(self.centralwidget)
        self.CurrentFig.setObjectName(u"CurrentFig")
        sizePolicy3 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.CurrentFig.sizePolicy().hasHeightForWidth())
        self.CurrentFig.setSizePolicy(sizePolicy3)
        self.CurrentFig.setMinimumSize(QSize(400, 400))
        self.CurrentFig.setMaximumSize(QSize(400, 400))
        self.CurrentFig.setScaledContents(True)

        self.verticalLayout_6.addWidget(self.CurrentFig)

        self.horizontalLayout_22 = QHBoxLayout()
        self.horizontalLayout_22.setObjectName(u"horizontalLayout_22")
        self.horizontalLayout_22.setContentsMargins(-1, 9, -1, 9)
        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Preferred, QSizePolicy.Minimum)

        self.horizontalLayout_22.addItem(self.horizontalSpacer_2)

        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        sizePolicy1.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy1)
        self.label.setMinimumSize(QSize(90, 20))
        self.label.setMaximumSize(QSize(1000, 1000))
        font3 = QFont()
        font3.setPointSize(17)
        font3.setBold(True)
        self.label.setFont(font3)

        self.horizontalLayout_22.addWidget(self.label)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Preferred, QSizePolicy.Minimum)

        self.horizontalLayout_22.addItem(self.horizontalSpacer_3)

        self.horizontalLayout_22.setStretch(0, 1)
        self.horizontalLayout_22.setStretch(2, 1)

        self.verticalLayout_6.addLayout(self.horizontalLayout_22)

        self.verticalLayout_6.setStretch(0, 10)

        self.horizontalLayout_16.addLayout(self.verticalLayout_6)

        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_16.addItem(self.horizontalSpacer_6)

        self.verticalLayout_5 = QVBoxLayout()
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.NextFig = QLabel(self.centralwidget)
        self.NextFig.setObjectName(u"NextFig")
        sizePolicy3.setHeightForWidth(self.NextFig.sizePolicy().hasHeightForWidth())
        self.NextFig.setSizePolicy(sizePolicy3)
        self.NextFig.setMinimumSize(QSize(400, 400))
        self.NextFig.setMaximumSize(QSize(400, 400))
        self.NextFig.setScaledContents(True)

        self.verticalLayout_5.addWidget(self.NextFig)

        self.horizontalLayout_23 = QHBoxLayout()
        self.horizontalLayout_23.setObjectName(u"horizontalLayout_23")
        self.horizontalLayout_23.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.horizontalLayout_23.setContentsMargins(-1, 9, -1, 9)
        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Preferred, QSizePolicy.Minimum)

        self.horizontalLayout_23.addItem(self.horizontalSpacer_4)

        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")
        sizePolicy1.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy1)
        self.label_2.setMinimumSize(QSize(20, 20))
        self.label_2.setMaximumSize(QSize(1000, 1000))
        self.label_2.setFont(font3)

        self.horizontalLayout_23.addWidget(self.label_2)

        self.horizontalSpacer_5 = QSpacerItem(40, 10, QSizePolicy.Preferred, QSizePolicy.Minimum)

        self.horizontalLayout_23.addItem(self.horizontalSpacer_5)

        self.horizontalLayout_23.setStretch(0, 1)
        self.horizontalLayout_23.setStretch(2, 1)

        self.verticalLayout_5.addLayout(self.horizontalLayout_23)


        self.horizontalLayout_16.addLayout(self.verticalLayout_5)

        self.horizontalSpacer_8 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_16.addItem(self.horizontalSpacer_8)

        self.horizontalLayout_16.setStretch(0, 1)
        self.horizontalLayout_16.setStretch(2, 1)
        self.horizontalLayout_16.setStretch(4, 1)

        self.gridLayout.addLayout(self.horizontalLayout_16, 0, 0, 1, 1)

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

        self.horizontalLayout_18 = QHBoxLayout()
        self.horizontalLayout_18.setObjectName(u"horizontalLayout_18")
        self.SetFilter = QPushButton(self.centralwidget)
        self.SetFilter.setObjectName(u"SetFilter")
        self.SetFilter.setMinimumSize(QSize(0, 50))
        self.SetFilter.setFont(font)

        self.horizontalLayout_18.addWidget(self.SetFilter)


        self.verticalLayout.addLayout(self.horizontalLayout_18)


        self.gridLayout.addLayout(self.verticalLayout, 1, 1, 1, 1)

        self.EMGPlotLayout = QHBoxLayout()
        self.EMGPlotLayout.setObjectName(u"EMGPlotLayout")
        self.EMGPlotLayout.setSizeConstraint(QLayout.SetDefaultConstraint)

        self.gridLayout.addLayout(self.EMGPlotLayout, 1, 0, 1, 1)

        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setSpacing(6)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label_5 = QLabel(self.centralwidget)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setFont(font)

        self.horizontalLayout.addWidget(self.label_5)

        self.SubjectID = QLineEdit(self.centralwidget)
        self.SubjectID.setObjectName(u"SubjectID")
        self.SubjectID.setFont(font1)

        self.horizontalLayout.addWidget(self.SubjectID)


        self.verticalLayout_4.addLayout(self.horizontalLayout)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.label_9 = QLabel(self.centralwidget)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setFont(font)

        self.horizontalLayout_5.addWidget(self.label_9)

        self.CurrentIndex = QLineEdit(self.centralwidget)
        self.CurrentIndex.setObjectName(u"CurrentIndex")
        self.CurrentIndex.setFont(font1)

        self.horizontalLayout_5.addWidget(self.CurrentIndex)

        self.label_10 = QLabel(self.centralwidget)
        self.label_10.setObjectName(u"label_10")

        self.horizontalLayout_5.addWidget(self.label_10)

        self.TotalIndex = QLineEdit(self.centralwidget)
        self.TotalIndex.setObjectName(u"TotalIndex")
        self.TotalIndex.setFont(font1)

        self.horizontalLayout_5.addWidget(self.TotalIndex)


        self.verticalLayout_4.addLayout(self.horizontalLayout_5)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.label_7 = QLabel(self.centralwidget)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setFont(font)

        self.horizontalLayout_4.addWidget(self.label_7)

        self.CurrentTrial = QLineEdit(self.centralwidget)
        self.CurrentTrial.setObjectName(u"CurrentTrial")
        self.CurrentTrial.setFont(font1)

        self.horizontalLayout_4.addWidget(self.CurrentTrial)

        self.label_8 = QLabel(self.centralwidget)
        self.label_8.setObjectName(u"label_8")

        self.horizontalLayout_4.addWidget(self.label_8)

        self.TotalTrial = QLineEdit(self.centralwidget)
        self.TotalTrial.setObjectName(u"TotalTrial")
        self.TotalTrial.setFont(font1)

        self.horizontalLayout_4.addWidget(self.TotalTrial)


        self.verticalLayout_4.addLayout(self.horizontalLayout_4)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label_6 = QLabel(self.centralwidget)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setFont(font)

        self.horizontalLayout_2.addWidget(self.label_6)

        self.MissionTimer = QLineEdit(self.centralwidget)
        self.MissionTimer.setObjectName(u"MissionTimer")
        self.MissionTimer.setFont(font1)

        self.horizontalLayout_2.addWidget(self.MissionTimer)


        self.verticalLayout_4.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_13 = QHBoxLayout()
        self.horizontalLayout_13.setObjectName(u"horizontalLayout_13")
        self.PauseButton = QPushButton(self.centralwidget)
        self.PauseButton.setObjectName(u"PauseButton")
        self.PauseButton.setMinimumSize(QSize(0, 40))
        self.PauseButton.setFont(font)

        self.horizontalLayout_13.addWidget(self.PauseButton)

        self.ContinueButton = QPushButton(self.centralwidget)
        self.ContinueButton.setObjectName(u"ContinueButton")
        self.ContinueButton.setMinimumSize(QSize(0, 40))
        self.ContinueButton.setFont(font)

        self.horizontalLayout_13.addWidget(self.ContinueButton)


        self.verticalLayout_4.addLayout(self.horizontalLayout_13)

        self.horizontalLayout_15 = QHBoxLayout()
        self.horizontalLayout_15.setObjectName(u"horizontalLayout_15")
        self.StartButton = QPushButton(self.centralwidget)
        self.StartButton.setObjectName(u"StartButton")
        self.StartButton.setMinimumSize(QSize(0, 60))
        self.StartButton.setFont(font)

        self.horizontalLayout_15.addWidget(self.StartButton)


        self.verticalLayout_4.addLayout(self.horizontalLayout_15)

        self.verticalLayout_4.setStretch(0, 1)
        self.verticalLayout_4.setStretch(1, 1)
        self.verticalLayout_4.setStretch(2, 1)
        self.verticalLayout_4.setStretch(3, 1)
        self.verticalLayout_4.setStretch(4, 1)
        self.verticalLayout_4.setStretch(5, 1)

        self.gridLayout.addLayout(self.verticalLayout_4, 0, 1, 1, 1)

        self.gridLayout.setRowStretch(1, 1)
        self.gridLayout.setColumnStretch(0, 10)
        self.gridLayout.setColumnStretch(1, 1)

        self.verticalLayout_7.addLayout(self.gridLayout)

        self.verticalLayout_7.setStretch(0, 1)
        self.verticalLayout_7.setStretch(1, 12)

        self.verticalLayout_8.addLayout(self.verticalLayout_7)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1437, 28))
        MainWindow.setMenuBar(self.menubar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"\u5f53\u524d\u53d1\u97f3\u7ec4", None))
        self.label_11.setText(QCoreApplication.translate("MainWindow", u"\u53d1\u58f0\u6a21\u5f0f", None))
        self.SpeechMode.setItemText(0, QCoreApplication.translate("MainWindow", u"\u65e0\u58f0", None))
        self.SpeechMode.setItemText(1, QCoreApplication.translate("MainWindow", u"\u6709\u58f0", None))

        self.label_18.setText(QCoreApplication.translate("MainWindow", u"\u589e\u76ca", None))
        self.GainType.setItemText(0, QCoreApplication.translate("MainWindow", u"6", None))
        self.GainType.setItemText(1, QCoreApplication.translate("MainWindow", u"1", None))
        self.GainType.setItemText(2, QCoreApplication.translate("MainWindow", u"2", None))
        self.GainType.setItemText(3, QCoreApplication.translate("MainWindow", u"3", None))
        self.GainType.setItemText(4, QCoreApplication.translate("MainWindow", u"4", None))
        self.GainType.setItemText(5, QCoreApplication.translate("MainWindow", u"8", None))
        self.GainType.setItemText(6, QCoreApplication.translate("MainWindow", u"12", None))

        self.LossCheckOn.setText(QCoreApplication.translate("MainWindow", u"\u4e22\u5305\u68c0\u6d4b", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"\u7535\u91cf", None))
        self.CurrentFig.setText("")
        self.label.setText(QCoreApplication.translate("MainWindow", u" \u5f53\u524d\u53d1\u97f3", None))
        self.NextFig.setText("")
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"\u4e0b\u6b21\u53d1\u97f3", None))
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
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"\u53d7\u8bd5ID", None))
        self.label_9.setText(QCoreApplication.translate("MainWindow", u"\u53d1\u97f3\u5e8f\u53f7", None))
        self.label_10.setText(QCoreApplication.translate("MainWindow", u"/ ", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"\u8bd5\u9a8c\u6b21\u6570", None))
        self.label_8.setText(QCoreApplication.translate("MainWindow", u"/", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"\u4efb\u52a1\u8ba1\u65f6\u5668", None))
        self.PauseButton.setText(QCoreApplication.translate("MainWindow", u"\u6682\u505c\u5b9e\u9a8c", None))
        self.ContinueButton.setText(QCoreApplication.translate("MainWindow", u"\u7ee7\u7eed\u5b9e\u9a8c", None))
        self.StartButton.setText(QCoreApplication.translate("MainWindow", u"\u5f00\u59cb\u5b9e\u9a8c", None))
    # retranslateUi

