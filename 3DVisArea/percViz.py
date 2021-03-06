#!/usr/bin/env python

import sys
from PyQt4 import QtGui, QtCore
import pyqtgraph.examples
import pyqtgraph as pg
import pyqtgraph.opengl as gl
from numpy import *
from matplotlib.cm import *
import itertools
#import MainWindow
from MainWindow import *
from worker import Worker, clearBox


class percViz(QtGui.QWidget):

    mysignal = QtCore.pyqtSignal(list, bool)

    def __init__(self):
        super(percViz, self).__init__()
        # main = MainWindow.MainWindow()

    def loadPercFile(self, percChargeIdCB, plotWidget):
        self.__init__()

        self.plotWidget = plotWidget
        self.percChargeIdCB = percChargeIdCB
        percFileName = QtGui.QFileDialog.getOpenFileName(
            self, 'Load Perc File', '.')
        if ".perc" not in percFileName:
            QtGui.QMessageBox.about(self, "Error",
                                    "Not a .perc File or is currupted")
            return

        self.worker = Worker(percFileName, self.mysignal, ".perc")
        self.worker.start()
        self.mysignal.connect(self.printData)

        # try:
        #     with open(percFileName) as percFile:
        #         percData = percFile.readlines()
        # except IOError:
        #     return

        # if ".perc" not in percFileName:
        #     QtGui.QMessageBox.about(self, "Error", "Not a Perc File")
        #     return

    def printData(self, percData, mybool):
        if not mybool:
            QtGui.QMessageBox.about(self, "Error",
                                    "Not a .perc File or is currupted")
            return
        dataLen = len(percData)

        self.pos = empty((dataLen, 3))
        self.size = empty((dataLen))
        self.color = empty((dataLen, 4))

        chargeIdColorCode = {
            0: (1, 0, 0, 1),  # Red
            1: (1, .5, 0, 1),  # Orange
            2: (1, 1, 0, 1),  # Yellow
            3: (.5, 1, 0, 1),  # Spring Green
            4: (0, 1, 0, 1),  # Green
            5: (0, 1, .5, 1),  # Turquoise
            6: (0, 1, 1, 1),  # Cyan
            7: (0, .5, 1, 1),  # Ocean
            8: (0, 0, 1, 1),  # Blue
            9: (.5, 0, 1, 1),  # Violet
            10: (1, 0, 1, 1),  # Magenta
            11: (1, 0, .5, 1),  # Raspberry
        }

        idList = []
        self.chargeIdDic = {}
        self.percDataDic = {}
        self.plotDic = {}

        for i, j in enumerate(percData):
            temp = percData[i].split(' ')

            if (len(temp) == 2):
                currentKey = temp[0]
                self.percDataDic.setdefault(temp[0], [])
                if currentKey not in idList:
                    idList.append(currentKey)
            else:
                self.percDataDic[currentKey].append(temp)

        for k, v in iter(self.percDataDic.items()):

            dataLen = len(v)

            self.pos = empty((dataLen, 3))
            self.size = empty((dataLen))
            self.color = empty((dataLen, 4))

            for i, j in enumerate(v):

                self.pos[i] = tuple(v[i][0:3])
                self.size[i] = .5
                self.color[i] = chargeIdColorCode[int(k)%len(chargeIdColorCode)]

            self.plotDic[k] = gl.GLLinePlotItem(
                pos=self.pos, color=self.color)

        idList.sort()
        self.percChargeIdCB.setEnabled(True)
        self.percChargeIdCB.addItems(["View All"])
        self.percChargeIdCB.addItems(idList)
        self.percChargeIdCB.setCurrentIndex(0)

        maxPos = self.pos[dataLen - 1]

        xMaxPos = int(maxPos[0])
        yMaxPos = int(maxPos[1])
        zMaxPos = int(maxPos[2])

        # for k, v in iter(self.plotDic.items()):
        #     self.plotWidget.addItem(self.plotDic[k])

        self.plotAlreadyThere = True
        self.previousDataSize = dataLen

    def selectPercChargeID(self, plotWidget):

        chargeID = str(self.percChargeIdCB.currentText())

        for k, v in iter(self.plotDic.items()):
            try:
                plotWidget.removeItem(self.plotDic[k])
                print("removed: ", k, self.plotDic[k])
            except ValueError:
                pass

        if chargeID == "View All":
            for k, v in iter(self.plotDic.items()):
                print("added:", k, self.plotDic[k])
                plotWidget.addItem(self.plotDic[k])
        else:
            for k, v in iter(self.plotDic.items()):
                if k == chargeID:
                    print("added:", k, self.plotDic[k])
                    plotWidget.addItem(self.plotDic[k])

        """

        if chargeID == "View All":
            for i in range(0, len(self.pos)):
                self.size[i] = .5
        else:
            chargeID = int(chargeID)

            for i in range(0, len(self.pos)):
                self.size[i] = 0



            for k, v in self.chargeIdDic.iteritems():
                for i in range(0, len(self.pos)):
                    if chargeID == k:
                        self.size[v] = .5

        """
