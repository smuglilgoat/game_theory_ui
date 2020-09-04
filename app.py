import sys
import numpy as np
import pandas as pd
import itertools
import tkinter as tk
from tkinter import filedialog

from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QApplication, QDialog, QMainWindow, QPushButton
from PyQt5.uic import loadUi

numPlayers = 2
StratList = np.array([2, 2])
stratInputs = []
data = None

class Window(QMainWindow):
    """Main window."""
    def __init__(self, parent=None):
        """Initializer."""
        super().__init__(parent)
        # Load the main GUI
        loadUi("main.ui", self)
        self.setWindowIcon(QtGui.QIcon("numpy.png"))
        # Connecting buttons with there function
        self.actionNGPure.triggered.connect(self.onNGPureActnTrggrd)
        self.actionRPure.triggered.connect(self.onRPureActnTrggrd)
        self.actionNGMixed.triggered.connect(self.onNGMixedActnTrggrd)
        self.actionRMixed.triggered.connect(self.onRMixedActnTrggrd)

    # Create a slot for launching the player strategies dialog
    def onNGPureActnTrggrd(self):
        """Launch the player strat dialog."""
        dlg = PlayerStarts(self)
        dlg.exec()

    def onNGMixedActnTrggrd(self):
        """Launch the player strat dialog."""
        dlg = PlayerStartsMixed(self)
        dlg.exec()

    def onRPureActnTrggrd(self):
        root = tk.Tk()
        root.withdraw()

        file_path = filedialog.askopenfilename()
        print("# Reading file:", file_path)
        dlg = CSVAnalysis(self)
        dlg.fileHandler(file_path)
        dlg.exec()

    def onRMixedActnTrggrd(self):
        root = tk.Tk()
        root.withdraw()

        file_path = filedialog.askopenfilename()
        print("# Reading file:", file_path)
        dlg = CSVAnalysisMixed(self)
        dlg.fileHandler(file_path)
        dlg.exec()

class PandasModel(QtCore.QAbstractTableModel):
    """
    Class to populate a table view with a pandas dataframe
    """
    def __init__(self, data, parent=None):
        QtCore.QAbstractTableModel.__init__(self, parent)
        self._data = data

    def rowCount(self, parent=None):
        return len(self._data.values)

    def columnCount(self, parent=None):
        return self._data.columns.size

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if index.isValid():
            if role == QtCore.Qt.DisplayRole:
                return str(self._data.values[index.row()][index.column()])
        return None

    def headerData(self, col, orientation, role):
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            return self._data.columns[col]
        return None

class CSVAnalysisMixed(QDialog):
    """CSVAnalysis dialog."""
    def __init__(self, parent=None):
        super().__init__(parent)
        # Load the dialog's GUI
        loadUi("csvreaderMixed.ui", self)

    def fileHandler(self, file_path):
        global  data
        self.textBrowser.append("# Reading file: " + file_path)
        data = pd.read_csv(file_path)
        print(data)
        model = PandasModel(data)
        self.tableView.setModel(model)

class CSVAnalysis(QDialog):
    """CSVAnalysis dialog."""
    def __init__(self, parent=None):
        super().__init__(parent)
        # Load the dialog's GUI
        loadUi("csvreader.ui", self)
        # Connecting buttons with there function
        self.StrictDomButton.clicked.connect(self.onStrictDomBtnClicked)
        self.FaibleDomButton.clicked.connect(self.onFaibleDomBtnClicked)
        self.ElimStrictDomButton.clicked.connect(self.onElimStrictDomBtnClicked)
        self.ElimFaibleDomButton.clicked.connect(self.onElimFaibleDomBtnClicked)
        self.NashButton.clicked.connect(self.onNashBtnClicked)
        self.ParetoButton.clicked.connect(self.onParetoBtnClicked)
        self.SecurityButton.clicked.connect(self.onSecurityLevelBtnClicked)

    def fileHandler(self, file_path):
        global  data
        self.textBrowser.append("# Reading file: " + file_path)
        data = pd.read_csv(file_path)
        print(data)
        model = PandasModel(data)
        self.tableView.setModel(model)

    def onStrictDomBtnClicked(self):
        global  data

        print("# Recherche des Strategies Strictement Dominantes")
        self.textBrowser.append("# Recherche des Strategies Strictement Dominantes")
        headers = list(data.head())
        playersArr = headers[0:(len(headers) // 2)]
        print("Players: ", playersArr)
        self.textBrowser.append("Players: " + str(playersArr))
        playerStrats = {}
        for e in playersArr:
            playerStrats[e] = np.unique(list(data[e]))
        print("Strategies: ", playerStrats)
        self.textBrowser.append("Strategies: " + str(playerStrats))
        playerGains = {}
        for e in playersArr:
            playerGains[e] = []
            for s in playerStrats[e]:
                print("Player ", e, "Strategie ", s)
                interDF = data[data[e] == int(s)]
                print(interDF)
                playerGains[e].append(list(interDF["Gain " + e]))
                print("#############################")
        print("Gains: ", playerGains)
        self.textBrowser.append("Gains: " + str(playerGains))
        for p in playerGains:
            for s in playerGains[p]:
                print("Player ", p, "Strategie ", s)
                self.textBrowser.append("Player " + str(p) + " Strategie " + str(s))
                otherStrats = playerGains[p].copy()
                currentStrat = otherStrats.pop(otherStrats.index(s))
                print("currentStrat: ", currentStrat)
                self.textBrowser.append("currentStrat: " + str(currentStrat))
                print("otherStrats: ", otherStrats)
                self.textBrowser.append("otherStrats: " + str(otherStrats))
                dom = True
                for e in otherStrats:
                    for i in range(len(currentStrat)):
                        if e[i] >= currentStrat[i]:
                            dom = False
                    if dom == True:
                        self.textBrowser.append("La Strategie: " + str(currentStrat) + "(" + str(playerGains[p].index(
                            s)) + ") domine la Strategie: " + str(e) + "(" + str(playerGains[p].index(
                            e)) + ")")
                        print("La Strategie: ", currentStrat, "(", playerGains[p].index(s), ") domine la Strategie: ", e,"(", playerGains[p].index(
                            e), ")")
                if dom == True:
                    self.textBrowser.append("La Strategie: " + str(currentStrat) + "(" + str(playerGains[p].index(s)) + ")" + " est une strategie strictement dominante pour le Joueur " + str(p))
                    print("La Strategie: ", currentStrat, "(", playerGains[p].index(s), ")", " est un strategie strictement dominante pour le Joueur ", p)
                print("#############################")
                self.textBrowser.append("#############################")

    def onFaibleDomBtnClicked(self):
        global data

        print("# Recherche des Strategies Faiblement Dominantes")
        self.textBrowser.append("# Recherche des Strategies Faiblement Dominantes")
        headers = list(data.head())
        playersArr = headers[0:(len(headers) // 2)]
        print("Players: ", playersArr)
        self.textBrowser.append("Players: " + str(playersArr))
        playerStrats = {}
        for e in playersArr:
            playerStrats[e] = np.unique(list(data[e]))
        print("Strategies: ", playerStrats)
        self.textBrowser.append("Strategies: " + str(playerStrats))
        playerGains = {}
        for e in playersArr:
            playerGains[e] = []
            for s in playerStrats[e]:
                print("Player ", e, "Strategie ", s)
                interDF = data[data[e] == int(s)]
                print(interDF)
                playerGains[e].append(list(interDF["Gain " + e]))
                print("#############################")
        print("Gains: ", playerGains)
        self.textBrowser.append("Gains: " + str(playerGains))
        for p in playerGains:
            for s in playerGains[p]:
                print("Player ", p, "Strategie ", s)
                self.textBrowser.append("Player " + str(p) + " Strategie " + str(s))
                copyGains = playerGains[p].copy()
                currentStrat = copyGains.pop(copyGains.index(s))
                print("currentStrat: ", currentStrat)
                self.textBrowser.append("currentStrat: " + str(currentStrat))
                print("copyGains: ", copyGains)
                self.textBrowser.append("copyGains: " + str(copyGains))
                dom = True
                for e in copyGains:
                    for i in range(len(currentStrat)):
                        if e[i] > currentStrat[i]:
                            dom = False
                    if dom == True:
                        self.textBrowser.append("La Strategie: " + str(currentStrat) + "(" + str(playerGains[p].index(
                            s)) + ") domine la Strategie: " + str(e) + "(" + str(playerGains[p].index(
                            e)) + ")")
                        print("La Strategie: ", currentStrat, "(", playerGains[p].index(s), ") domine la Strategie: ", e,"(", playerGains[p].index(
                            e), ")")
                if dom == True:
                    self.textBrowser.append("La Strategie: " + str(currentStrat) + "(" + str(playerGains[p].index(s)) + ")" + " est une strategie faiblement dominante pour le Joueur " + str(p))
                    print("La Strategie: ", currentStrat, "(", playerGains[p].index(s), ")", "est un strategie faiblement dominante pour le Joueur ", p)
                print("#############################")
                self.textBrowser.append("#############################")

    def onElimStrictDomBtnClicked(self):
        print("onElimStrictDomBtnClicked")
        self.textBrowser.append("onElimStrictDomBtnClicked")

    def onElimFaibleDomBtnClicked(self):
        print("onElimFaibleDomBtnClicked")
        self.textBrowser.append("onElimFaibleDomBtnClicked")

    def onNashBtnClicked(self):
        global data

        print("# Recherche de l'Equilibre de Nash")
        self.textBrowser.append("# Recherche de l'Equilibre de Nash")
        headers = list(data.head())
        playersArr = headers[0:(len(headers) // 2)]
        print("Players: ", playersArr)
        self.textBrowser.append("Players: " + str(playersArr))
        playerStrats = {}
        for e in playersArr:
            playerStrats[e] = np.unique(list(data[e]))
        print("Strategies: ", playerStrats)
        self.textBrowser.append("Strategies: " + str(playerStrats))
        playerStratsDataFrame = {}
        for p in playersArr:
            playerStratsDataFrame[p] = []
            for s in playerStrats[p]:
                playerStratsDataFrame[p].append(data[data[p] == s].to_numpy())
        print(playerStratsDataFrame)
        self.textBrowser.append("Strategies de Chq Joueurs: " + str(playerStratsDataFrame))
        bestMoves = {}
        bestMovesStr = {}
        for p in playerStratsDataFrame:
            bestMoves[p] = []
            bestMovesStr[p] = []
            for i in range(len(playerStratsDataFrame[p][0])):
                maxGain = playerStratsDataFrame[p][0][i][len(playersArr) + int(p)]
                strats = playerStratsDataFrame[p][0][i][0:len(playersArr)]
                for df in playerStratsDataFrame[p]:
                    if df[i][len(playersArr) + int(p)] > maxGain:
                        maxGain = df[i][len(playersArr) + int(p)]
                        strats = df[i][0:len(playersArr)]
                for df in playerStratsDataFrame[p]:
                    if df[i][len(playersArr) + int(p)] == maxGain:
                        bestMoves[p].append(list(df[i][0:len(playersArr)]))
                        bestMovesStr[p].append(''.join(map(str, list(df[i][0:len(playersArr)]))))
                print("Player ", p, "Line ", i, "maxGain ", maxGain, " | Played ", strats)
                self.textBrowser.append("Joueur " + str(p) + " maxGain pour le profile " + str(strats) + "=" + str(maxGain))
                bestMoves[p].append(list(strats))
                bestMovesStr[p].append(''.join(map(str, list(strats))))
            print("#################################")
            self.textBrowser.append("###################################")
        print("Best Moves: ", np.unique(bestMovesStr))
        self.textBrowser.append("Meilleurs Réponses: ")
        for e in bestMovesStr:
            self.textBrowser.append("Joueur: " + str(e))
            self.textBrowser.append("Reponses: " + str(np.unique(bestMovesStr[e])))
            self.textBrowser.append("###################################")

        nashEquilb = []
        for i in range(len(bestMovesStr['0'])):
            isNash = True
            strat = bestMovesStr['0'][i]
            for p in range(1, len(bestMovesStr)):
                print(np.intersect1d(strat, bestMovesStr[str(p)]))
                if np.intersect1d(strat, bestMovesStr[str(p)]).size == 0:
                    isNash = False
            if isNash:
                nashEquilb.append(strat)
        nashEquilb = np.unique(nashEquilb)
        print("nashEquilb: ", nashEquilb)
        self.textBrowser.append("Equilibres de Nash: " + str(nashEquilb))

    def onParetoBtnClicked(self):
        def ifBetterProfile(profile1, profile2):
            isBetter = False
            for i in range(len(profile1)):
                if profile1[i] < profile2[i]:
                    return False
                elif profile1[i] > profile2[i]:
                    isBetter = True
            return isBetter

        global data

        print("# Recherche des Optimums de Pareto")
        self.textBrowser.append("# Recherche des Optimums de Pareto")
        headers = list(data.head())
        playersArr = headers[0:(len(headers) // 2)]
        print("Players: ", playersArr)
        self.textBrowser.append("Players: " + str(playersArr))
        playerStrats = {}
        for e in playersArr:
            playerStrats[e] = np.unique(list(data[e]))
        print("Strategies: ", playerStrats)
        self.textBrowser.append("Strategies: " + str(playerStrats))
        dataNPArray = data.to_numpy()
        paretoEfficiency = []
        for i in range(len(dataNPArray)):
            isParetoDom = True
            for j in range(len(dataNPArray)):
                if ifBetterProfile(dataNPArray[j][len(playersArr):], dataNPArray[i][len(playersArr):]):
                    isParetoDom = False
            if isParetoDom:
                paretoEfficiency.append(list(dataNPArray[i][0:len(playersArr)]))
        print("paretoEfficiency: ", paretoEfficiency)
        self.textBrowser.append("Optimum de Pareto: " + str(paretoEfficiency))

    def onSecurityLevelBtnClicked(self):
        global data

        print("# Recherche des Niveaux de Securité")
        self.textBrowser.append("# Recherche des Niveaux de Securité")
        headers = list(data.head())
        playersArr = headers[0:(len(headers) // 2)]
        print("Players: ", playersArr)
        self.textBrowser.append("Players: " + str(playersArr))
        playerStrats = {}
        for e in playersArr:
            playerStrats[e] = np.unique(list(data[e]))
        print("Strategies: ", playerStrats)
        self.textBrowser.append("Strategies: " + str(playerStrats))
        playerStratsDataFrame = {}
        for p in playersArr:
            playerStratsDataFrame[p] = []
            for s in playerStrats[p]:
                playerStratsDataFrame[p].append(data[data[p] == s])
        print(playerStratsDataFrame)
        self.textBrowser.append("Strategies de Chq Joueurs: " + str(playerStratsDataFrame))
        for p in playerStratsDataFrame:
            for s in playerStratsDataFrame[p]:
                print("Player ", p, "Strategy ", np.unique(s[p].to_numpy()), "Security Level ", np.amin(s['Gain ' + p].to_numpy()))
                self.textBrowser.append("Player " + str(p) + " Strategy " + str(np.unique(s[p].to_numpy())) + " Security Level " + str(np.amin(s['Gain ' + p].to_numpy())))
            print("##########################")
            self.textBrowser.append("##########################")

class PlayerStarts(QDialog):
    """PlayerStrat dialog."""
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
        global StratList

        winWidth = self.frameGeometry().width()
        winHeight = self.frameGeometry().height()
        numPlayers = numPlayers + 1
        print("#    Adding players... ", "(Total =", numPlayers, ")")
        StratList = np.append(StratList, 2)
        print("playersStrats = ", StratList)
        self.newLabel = QtWidgets.QLabel()
        self.newLabel.setObjectName(("label_" + str(numPlayers + 1)))
        self.newLabel.setText("Player " + str(numPlayers))
        self.newPlayerStrat = QtWidgets.QLineEdit()
        self.newPlayerStrat.setObjectName("playerStrats_" + str(numPlayers))
        self.newPlayerStrat.setText('2')
        self.formLayout.addRow(self.newLabel, self.newPlayerStrat)
        stratInputs.append(self.newPlayerStrat)
        self.generateButton.setGeometry(QtCore.QRect(11, self.generateButton.y() + 22, 151, 28))
        self.addPlayerButton.setGeometry(QtCore.QRect(11, self.addPlayerButton.y() + 22, 151, 28))
        self.line_2.setGeometry(QtCore.QRect(11, self.line_2.y() + 22, 151, 20))
        self.layoutWidget.setGeometry(QtCore.QRect(10, 50, 151, self.layoutWidget.height() + 22))
        self.resize(self.width(), self.height() + 22)

    def onGenerateCSVBtnClicked(self):
        global StratList
        global numPlayers
        global stratInputs

        StratList = []
        for i in range(len(stratInputs)):
            StratList.append(stratInputs[i].text())
        StratList = np.array(StratList).astype(int)

        print("#    Generating...")
        print("numPlayers = ", numPlayers)
        print("playersStrats = ", StratList)

        profiles = []
        for i in StratList:
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
        global StratList
        global numPlayers
        global stratInputs
        numPlayers = 2
        StratList = np.array([2, 2])
        stratInputs = []

class PlayerStartsMixed(QDialog):
    """PlayerStartsMixed dialog."""
    def __init__(self, parent=None):
        super().__init__(parent)
        # Load the dialog's GUI
        loadUi("inputFormMixed.ui", self)
        # Connecting buttons with there function
        self.generateButton.clicked.connect(self.onGenerateCSVBtnClicked)
        # Inits
        stratInputs.append(self.playerStrats_1)
        stratInputs.append(self.playerStrats_2)

    def onGenerateCSVBtnClicked(self):
        global StratList
        global numPlayers
        global stratInputs

        StratList = []
        for i in range(len(stratInputs)):
            StratList.append(stratInputs[i].text())
        StratList = np.array(StratList).astype(int)

        print("#    Generating...")
        print("numPlayers = ", numPlayers)
        print("playersStrats = ", StratList)

        profiles = []
        for i in StratList:
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
        resultsDataFrame.to_csv("fileMixed.csv", index=None)

    def closeEvent(self, event):
        global StratList
        global numPlayers
        global stratInputs
        numPlayers = 2
        StratList = np.array([2, 2])
        stratInputs = []

if __name__ == "__main__":
    # Create the application
    app = QApplication(sys.argv)
    # Create and show the application's main window
    win = Window()
    win.show()
    # Run the application's main loop
    sys.exit(app.exec())