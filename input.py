# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'input.ui'
#
# Created by: PyQt5 UI code generator 5.15.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
import numpy as np
import pandas as pd
import itertools

numPlayers = 2
playersStrats = np.array([2, 2])
stratInputs = []

class Ui_playerInputWindow(object):
    def setupUi(self, playerInputWindow):
        global stratInputs

        playerInputWindow.setObjectName("playerInputWindow")
        playerInputWindow.resize(459, 187)
        self.centralwidget = QtWidgets.QWidget(playerInputWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(10, 10, 441, 166))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 3, 0, 1, 1)
        self.playerStrats2 = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.playerStrats2.setObjectName("playerStrats2")
        self.gridLayout.addWidget(self.playerStrats2, 3, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 2, 0, 1, 1)
        self.playerStrats1 = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.playerStrats1.setObjectName("playerStrats1")
        self.gridLayout.addWidget(self.playerStrats1, 2, 1, 1, 1)
        self.line = QtWidgets.QFrame(self.gridLayoutWidget)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.gridLayout.addWidget(self.line, 1, 0, 1, 2)
        self.label_3 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 0, 1, 1, 1)
        self.line_2 = QtWidgets.QFrame(self.gridLayoutWidget)
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.gridLayout.addWidget(self.line_2, 4, 0, 1, 2)
        self.addPlayerButton = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.addPlayerButton.setObjectName("addPlayerButton")
        self.gridLayout.addWidget(self.addPlayerButton, 5, 0, 1, 2)
        self.generateButton = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.generateButton.setObjectName("generateButton")
        self.gridLayout.addWidget(self.generateButton, 6, 0, 1, 2)
        playerInputWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(playerInputWindow)
        QtCore.QMetaObject.connectSlotsByName(playerInputWindow)

        stratInputs.append(self.playerStrats1)
        stratInputs.append(self.playerStrats2)


    def retranslateUi(self, playerInputWindow):
        _translate = QtCore.QCoreApplication.translate
        playerInputWindow.setWindowTitle(_translate("playerInputWindow", "Enter data to generate matrix"))
        self.label.setText(_translate("playerInputWindow", "Player 2"))
        self.label_2.setText(_translate("playerInputWindow", "Player 1"))
        self.label_3.setText(_translate("playerInputWindow", "Strategies"))
        self.addPlayerButton.setText(_translate("playerInputWindow", "Add +"))
        self.generateButton.setText(_translate("playerInputWindow", "Generate CSV"))

    def addPlayer():
        global numPlayers
        global playersStrats

        numPlayers = numPlayers + 1
        print("#    Adding players... ", "(Total =", numPlayers, ")")
        playersStrats = np.append(playersStrats, 2)
        print("playersStrats = ", playersStrats)

    def generateCSV():
        global playersStrats
        global numPlayers
        global stratInputs

        playersStrats = []
        for i in range(len(stratInputs)):
            playersStrats.append(stratInputs[i].text())
        playersStrats = np.array(playersStrats).astype(int)

        print("#    Generating...")
        print("numPlayers = ", numPlayers)
        print("playersStrats = ", playersStrats)

        profiles = []
        for i in playersStrats:
            a = np.arange(i)
            profiles.append(a)
        result = []
        for element in itertools.product(*profiles):
            result.append(element)
        print(np.array(result))
        headerList = np.arange(numPlayers)
        headerList = np.array(headerList).astype(str).tolist()
        print(headerList)
        for i in range(len(headerList)):
            headerList[i] = "Gain " + headerList[i]
        print(headerList)
        resultsDataFrame = pd.DataFrame(result)
        print(resultsDataFrame)
        resultsDataFrame = resultsDataFrame.reindex(columns=resultsDataFrame.columns.tolist() + headerList)
        print(resultsDataFrame)
        resultsDataFrame.to_csv("file.csv", index=None)

if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    playerInputWindow = QtWidgets.QMainWindow()
    ui = Ui_playerInputWindow()
    ui.setupUi(playerInputWindow)

    ui.addPlayerButton.clicked.connect(Ui_playerInputWindow.addPlayer)
    ui.generateButton.clicked.connect(Ui_playerInputWindow.generateCSV)

    playerInputWindow.show()
    sys.exit(app.exec_())
