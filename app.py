import sys
import numpy as np
import pandas as pd
import itertools

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QApplication, QDialog, QMainWindow, QPushButton
from PyQt5.uic import loadUi

numPlayers = 2
playersStrats = np.array([2, 2])
stratInputs = []

class Window(QMainWindow):
    """Main window."""
    def __init__(self, parent=None):
        """Initializer."""
        super().__init__(parent)
        # Load the main GUI
        loadUi("main.ui", self)
        # Connecting buttons with there function
        self.actionNGPure.triggered.connect(self.onNGPureActnTrggrd)

    # Create a slot for launching the player strategies dialog
    def onNGPureActnTrggrd(self):
        """Launch the player strat dialog."""
        dlg = PlayerStarts(self)
        dlg.exec()


class PlayerStarts(QDialog):
    """Employee dialog."""
    def __init__(self, parent=None):
        super().__init__(parent)
        # Load the dialog's GUI
        loadUi("inputForm.ui", self)
        # Connecting buttons with there function
        self.addPlayerButton.clicked.connect(self.onAddPlayerBtnClicked)
        self.generateButton.clicked.connect(self.onGenerateCSVBtnClicked)
        # Inits
        stratInputs.append(self.playerStrats_1)
        stratInputs.append(self.playerStrats_2)

    def onAddPlayerBtnClicked(self):
        global numPlayers
        global playersStrats

        numPlayers = numPlayers + 1
        print("#    Adding players... ", "(Total =", numPlayers, ")")
        playersStrats = np.append(playersStrats, 2)
        print("playersStrats = ", playersStrats)
        self.newLabel = QtWidgets.QLabel(self.gridLayoutWidget)
        self.newLabel.setObjectName(("label_" + str(numPlayers + 1)))
        self.newLabel.setText("Player " + str(numPlayers))
        self.newPlayerStrat = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.newPlayerStrat.setObjectName("playerStrats_" + str(numPlayers))
        self.newPlayerStrat.setText('2')
        self.formLayout.addRow(self.newLabel, self.newPlayerStrat)
        stratInputs.append(self.newPlayerStrat)

    def onGenerateCSVBtnClicked(self):
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

    def closeEvent(self, event):
        global playersStrats
        global numPlayers
        global stratInputs
        numPlayers = 2
        playersStrats = np.array([2, 2])
        stratInputs = []

if __name__ == "__main__":
    # Create the application
    app = QApplication(sys.argv)
    # Create and show the application's main window
    win = Window()
    win.show()
    # Run the application's main loop
    sys.exit(app.exec())