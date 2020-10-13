#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct  5 10:42:28 2020

@author: djoghurt
"""

from PyQt5 import QtCore, QtGui, QtWidgets
import sys

from mainWindow import Ui_TabWidget
import zonneEngine

class MyWindow(QtWidgets.QTabWidget):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.ui = Ui_TabWidget()
        self.ui.setupUi(self)
        
        self.ui.pushButton_bereken.clicked.connect(self.buttonClick_bereken)
        self.ui.pushButton_verdeel.clicked.connect(self.buttonClick_verdeel)

    def buttonClick_bereken(self):
        print("bereken klik")
        zonneEngine.bereken_uit_UI(self.ui)
    
    def buttonClick_verdeel(self):
        print("verdeel klik")    
        totaal = float(self.ui.lineEdit_verbruikTotaal.text())
        
        verdeel = [0.0638, 0.1804, 0.2617, 0.3729, 0.44, 0.4033, 0.4058, 0.3508, 0.2638, 0.1838, 0.0938, 0.0513]
        if self.ui.checkBox_gelijkeMaanden.isChecked():
            verdeel = [0.083, 0.083, 0.083, 0.083, 0.083, 0.083, 0.083, 0.083, 0.083, 0.083, 0.083, 0.083]
        
        self.ui.lineEdit_verbruikJan.setText(str(round(totaal*verdeel[0],2)))
        self.ui.lineEdit_verbruikFeb.setText(str(round(totaal*verdeel[1],2)))
        self.ui.lineEdit_verbruikMaart.setText(str(round(totaal*verdeel[2],2)))
        self.ui.lineEdit_verbruikApr.setText(str(round(totaal*verdeel[3],2)))
        self.ui.lineEdit_verbruikMei.setText(str(round(totaal*verdeel[4],2)))
        self.ui.lineEdit_verbruikJun.setText(str(round(totaal*verdeel[5],2)))
        self.ui.lineEdit_verbruikJul.setText(str(round(totaal*verdeel[6],2)))
        self.ui.lineEdit_verbruikAug.setText(str(round(totaal*verdeel[7],2)))
        self.ui.lineEdit_verbruikSep.setText(str(round(totaal*verdeel[8],2)))
        self.ui.lineEdit_verbruikOkt.setText(str(round(totaal*verdeel[9],2)))
        self.ui.lineEdit_verbruikNov.setText(str(round(totaal*verdeel[10],2)))
        self.ui.lineEdit_verbruikDec.setText(str(round(totaal*verdeel[11],2)))


app = QtWidgets.QApplication(sys.argv)
TabWidget = MyWindow()
TabWidget.show()
sys.exit(app.exec_())





