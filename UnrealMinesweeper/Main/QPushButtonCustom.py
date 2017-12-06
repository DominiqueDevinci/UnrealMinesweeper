import sys

from PyQt4.QtGui import *
from PyQt4.QtCore import *

from ImageLoader import ImageLoader
from BoardController import BoardController
from Util import choose
from MinesweeperGUI import MinesweeperGUI

import Solver

class QPushButtonCustom(QPushButton):
    def __init__(self, id):
        super(QPushButtonCustom, self).__init__()
        self.id=id
        self.flagged=False;        
        self.setFixedSize(45, 45)
        self.surroundingMines=-1 # -1 = number of surrounding mines unknown
        self.updateView()
        
    def setProbability(self, p):
        if self.surroundingMines!=-3 or True:
            self.setText(str(int(p*100))+"%")
        else:
           self.setText("");
     
        
    def getId(self):
        return self.id
    
    def setFlagged(self, flagged): #must be called by controller and not directly by a right click
        self.flagged=flagged
        updateView()
        
    def setSurroundingMines(self, nb):
        self.surroundingMines=nb #set surrounding mines = case is known
        self.updateView()
        
    def setState(self, nb):
        if(nb==-3):
            self.surroundingMines=nb
            #self.setText("")
            self.setIcon(ImageLoader.iconMine)
            
        
    def updateView(self):
        if self.flagged:
            self.setIcon(ImageLoader.iconFlag)
            self.setObjectName("flagged")
        elif self.surroundingMines>-1: # case known
            self.setFlat(True)
            self.setIcon(QIcon())
            self.setStyleSheet("border: 1px solid grey; background-color: rgb(224, 224, 224); color: red;") 
            
            if self.surroundingMines==0:                             
                self.setText("")
            else:
                self.setText(str(self.surroundingMines))
         
