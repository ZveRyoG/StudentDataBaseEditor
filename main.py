#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys, sqlite3
from PyQt4 import QtCore, QtGui, uic
app = QtGui.QApplication(sys.argv)

class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        uic.loadUi('main.ui', self)
        self.connect(self.openFile, QtCore.SIGNAL('triggered()'), self.openDB)
        #self.openFile.clicked.connect(self.openDB)
        self.cursorDB = None

    def openDB(self):
        file = QtGui.QFileDialog.getOpenFileName(None, u"Выберите БД")
        conn = sqlite3.connect(file)
        self.cursorDB = conn.cursor()

    def saveDB(self):
        file = QtGui.QFileDialog.getSaveFileName(None, u"Сохранить...")

    def addRecord(self):
        pass

    def removeRecord(self):
        pass





mw = MainWindow()
mw.show()
app.exec_()
