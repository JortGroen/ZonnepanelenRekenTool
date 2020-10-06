#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct  5 10:42:28 2020

@author: djoghurt
"""

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
import sys

app = QApplication(sys.argv)
screen_resolution = app.desktop().screenGeometry()
scale = 0.75
width, height = int(screen_resolution.width()*scale), int(screen_resolution.height()*scale)
xpos, ypos = int(screen_resolution.width()/2-width/2), int(screen_resolution.height()/2-height/2)

class MyWindow(QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        self.setGeometry(xpos, ypos, width, height)
        self.setWindowTitle("tool")
        self.initUI()
        
    def initUI(self):
        self.label = QtWidgets.QLabel(self)
        self.label.setText("label1")
        self.label.move(50,50)
        
        self.b1 = QtWidgets.QPushButton(self)
        self.b1.setText("button 1")
        self.b1.clicked.connect(self.clicked)
        
    def clicked(self):
        self.label.setText("you pressed button1")
        self.update()
        
    def update(self):
        self.label.adjustSize()
        

def clicked():
    print("clicked")

def Window():
    win = MyWindow()  
    win.show()
    sys.exit(app.exec_())
    
Window()





