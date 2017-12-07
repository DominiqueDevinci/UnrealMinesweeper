import sys

from PyQt4.QtGui import *
from PyQt4.QtCore import *

from ImageLoader import ImageLoader
from BoardController import BoardController
from Util import choose

import Solver

class QPushButtonCustom(QPushButton):
    rightClick=pyqtSignal()
    
    def mousePressEvent (self, event):
        QPushButton.mousePressEvent(self, event)
        if event.button() == Qt.RightButton :
            self.rightClick.emit()
    
    def __init__(self, id):
        super(QPushButtonCustom, self).__init__()
        self.id=id  
        self.setFixedSize(45, 45)
        self.surroundingMines=-1 # -1 = number of surrounding mines unknown, -2 = flagged, -3 = mine hited (game over !)
        self.updateView()
        
    def setProbability(self, p, verboseDisplay):
        if self.surroundingMines>=-1 or verboseDisplay:
            self.setText(str(int(p*100))+"%")
        else:
           self.setText("");
     
        
    def getId(self):
        return self.id
    
    def setFlag(self, flagged): #must be called by controller and not directly by a right click
        if(flagged):
            self.setIcon(ImageLoader.iconFlag)
            self.surroundingMines=-2
        else:
            self.setIcon(QIcon())
            self.surroundingMines=-1  
        self.updateView()
        
        
        
        
    def setSurroundingMines(self, nb):
        self.surroundingMines=nb #set surrounding mines = case is known
        self.updateView()
        
    def setState(self, nb):
        if(nb==-3):
            self.surroundingMines=nb
            #self.setText("")
            self.setIcon(ImageLoader.iconMine)
            
        
    def updateView(self):
        if self.surroundingMines>-1: # case known
            self.setFlat(True)
            if self.surroundingMines==0:   
                self.setStyleSheet("border: 1px solid grey; background-color: rgb(224, 224, 224); ")                           
                self.setText("")                
            else:
                self.setText(str(self.surroundingMines))
                
            if(self.surroundingMines==1):
                self.setStyleSheet("border: 1px solid grey; background-color: rgb(224, 224, 224); color: blue;") 
            elif(self.surroundingMines==2):
                self.setStyleSheet("border: 1px solid grey; background-color: rgb(224, 224, 224); color: green;") 
            elif(self.surroundingMines>=3):
                self.setStyleSheet("border: 1px solid grey; background-color: rgb(224, 224, 224); color: red;") 
        else:
            if self.surroundingMines==-2:
                self.setIcon(ImageLoader.iconFlag)
            
         
