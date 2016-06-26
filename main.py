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
        self.connect(self.addRecord, QtCore.SIGNAL('triggered()'), self.recordAdd)
        self.connect(self.saveFile, QtCore.SIGNAL('triggered()'), self.saveDB)
        self.connect(self.deleteRecord, QtCore.SIGNAL('triggered()'), self.removeRecord)
        self.connect(self.actionExit, QtCore.SIGNAL('triggered()'), app.exit)
        #self.openFile.clicked.connect(self.openDB)
        self.cursorDB = None

    def openDB(self):
        file = QtGui.QFileDialog.getOpenFileName(None, u"Выберите БД")

        if (file is not None):
            self.conn = sqlite3.connect(str(file))
            self.cursorDB = self.conn.cursor()
            self.cursorDB.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='Students';")
            res = self.cursorDB.fetchone()
            if res is None or res[0]!="Students":
                if QtGui.QMessageBox(u"Вопрос",u"Не найдена таблица студентов.\nСоздать новую таблицу?",QtGui.QMessageBox.Question,QtGui.QMessageBox.Yes,QtGui.QMessageBox.No,0).exec_()==QtGui.QMessageBox.Yes:
                    self.cursorDB.execute('''CREATE TABLE `Students` (
	                    `ID`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                    	`First_Name`	TEXT NOT NULL,
                    	`Second_Name`	TEXT NOT NULL,
	                    `Group_Num`	INTEGER NOT NULL
);''')
            elif res[0]=="Students":
                self.addRecord.setEnabled(True)
                self.saveFile.setEnabled(True)
                self.deleteRecord.setEnabled(True)
                #headers = ['ID','First_Name','Second_name','Group_Num']


    def saveDB(self):
        #file = QtGui.QFileDialog.getSaveFileName(None, u"Сохранить...")
        self.conn.commit()


    def recordAdd(self):
        addRecDialog = addRec(self)
        if addRecDialog.exec_():
            FrName = addRecDialog.FirstName.toPlainText()
            ScName = addRecDialog.SecondName.toPlainText()
            Group = addRecDialog.GroupName.toPlainText()
            if FrName is not None and ScName is not None and Group is not None:
                self.cursorDB.execute("INSERT INTO 'Students' ('First_Name','Second_Name','Group_Num') VALUES('"+str(FrName)+"','"+str(ScName)+"','"+str(Group)+"')")
        #self.conn.commit()


    def removeRecord(self):
        self.cursorDB.execute("SELECT * FROM Students")
        if self.cursorDB.fetchall() is not None:
            print self.cursorDB.fetchall()


class addRec(QtGui.QDialog):
    def __init__(self,parent=None):
        QtGui.QDialog.__init__(self,parent)
        uic.loadUi('addRecord.ui', self)

mw = MainWindow()
mw.show()
app.exec_()
