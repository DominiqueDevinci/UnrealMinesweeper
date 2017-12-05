import sys

from PyQt4.QtGui import *
from PyQt4.QtCore import *

from ImageLoader import ImageLoader
from BoardController import BoardController

import Solver


class QPushButtonCustom(QPushButton):
    def __init__(self, id):
        super(QPushButtonCustom, self).__init__()
        self.id=id
        self.flagged=False;        
        self.setFixedSize(35, 35)
        self.surroundingMines=-1 # -1 = number of surrounding mines unknown
        self.updateView()
        
        
    def getId(self):
        return self.id
    
    def setFlagged(self, flagged):
        self.flagged=flagged
        updateView()
        
    def toggleFlag(self):
        self.flagged=(not self.flagged)
        updateView()
        
    def setSurroundingMines(self, nb):
        print nb
        self.surroundingMines=nb #set surrounding mines = case is known
        self.updateView()
        
    def setState(self, nb):
        if(nb==-3):
            self.setObjectName("exploded")
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
         

       
class MinesweeperGUI(QMainWindow):
    def __init__(self, width, height, parent = None):
        super(MinesweeperGUI, self).__init__(parent)
        
        self.height=height
        self.width=width
        
        self.setCentralWidget(QWidget(self))
        self.setWindowTitle(" Unreal Minesweeper ")
        
        layout = QVBoxLayout(self.centralWidget())
        layout.addStretch()
        layout.setMargin(0)
        layout.setSpacing(0)
        layout.addWidget(QPushButton(" New Game ... "))        
        layout.addWidget(QPushButton(" Solve (basic solver) "))
        layout.addWidget(QPushButton(" Solve (with dynamic propagation constraint) "))
        
        self.mainLayout=layout;
        
        ImageLoader.init();
        
       
        
        
        
    def initBoard(self, boardController):
       
        count=0
        #init empty board
        for l in range(0, self.height):
            tmpLayout=QHBoxLayout()
            tmpLayout.setMargin(0)
            tmpLayout.setSpacing(0)
            tmpLayout.addStretch()
            for c in range(0, self.width):                
                button=QPushButtonCustom(count)
                boardController.addItemView(count, button)               
                tmpLayout.addWidget(button)                
                count+=1
                
            tmpLayout.addStretch()
            self.mainLayout.addLayout(tmpLayout)
        self.mainLayout.addStretch()  
        
        self.setStyleSheet("""
        
        /*.QPushButtonCustom#known0 {
            background-color: rgb(224, 224, 224);
            border: 1px inset grey;
            color: red;
            font-weight: bold;
        }
        .QPushButtonCustom#known1 {
            background-color: rgb(224, 224, 224);
            border: 1px inset grey;
            color: blue;
            font-weight: bold;
        }
        QPushButtonCustom#known2 {
            background-color: rgb(224, 224, 224);
            border: 1px inset grey;
            color: green;
            font-weight: bold;
        }
        .QPushButtonCustom#known3 {
            background-color: rgb(224, 224, 224);
            border: 1px inset grey;
            color: rgb(229, 141, 0);
            font-weight: bold;
        }
        .QPushButtonCustom#known4 {
            background-color: rgb(224, 224, 224);
            border: 1px inset grey;
            color: red;
            font-weight: bold;
        }
        
        .QPushButtonCustom#exploded {
            background-color: rgb(224, 224, 224);
            border: 1px inset red;
        }*/
        
        .QPushButton{
            margin-bottom: 10px;
            height: 50px;
        }
        """);
        
        
    def updateItems(self, updatedItems): #updatedItems is a frozenset containing modified item. The value is -1 if unknow, 0 if mi
        return
        

def main():
   app = QApplication(sys.argv)
   
   view = MinesweeperGUI(10, 10)
   boardController=BoardController(view, 10, 10, 20)
   view.initBoard(boardController)
   print choose(8, 2)
   view.show()
   sys.exit(app.exec_())
    
if __name__ == '__main__':
   main()