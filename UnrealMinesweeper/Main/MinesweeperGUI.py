import sys

from PyQt4.QtGui import *
from PyQt4.QtCore import *

from ImageLoader import ImageLoader
from BoardController import BoardController
from Util import choose

import Solver

class MinesweeperGUI(QMainWindow):
    def __init__(self, parent = None):
        super(MinesweeperGUI, self).__init__(parent)
        

        
        self.setCentralWidget(QWidget(self))
        self.setWindowTitle(" Unreal Minesweeper ")
        
        #Menu
        menubar = self.menuBar()
        benchmarkProbasV1=QAction(" Benchmark probabilistic algorithm v1", self)
        benchmarkProbasV1.triggered.connect(self.runBenchmarkProbasV1)
        
        
        benchMenu = menubar.addMenu(' Run a benchmark ')        
        benchMenu.addAction(benchmarkProbasV1)
        
      
        
        layout = QVBoxLayout(self.centralWidget())
        layout.addStretch()
        layout.setMargin(0)
        layout.setSpacing(0)
    
        layout.addWidget(QPushButton(" Probabilistic solver : next step"))
        layout.addWidget(QPushButton(" Probabilistic solver : auto-solve"))
        
        layout.addWidget(QPushButton(" CSP Solver : next step "))
        layout.addWidget(QPushButton(" CSP Solver : auto-solve "))
        
        self.mainLayout=layout;
        
        ImageLoader.init();       
    
        self.setStatus(" Ready to play !");

    def setStatus(self, str):    
        self.statusBar().showMessage(str)
        
    def runBenchmarkProbasV1(self):
        print "run benchmark"   
         
    def initBoard(self, height, width, boardController):
        self.height=height
        self.width=width
        self.length=height*width;
        
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
        .QPushButton{
            margin-top: 5px;
            margin-bottom: 5px;
            height: 50px;
        }
        """);
        
        
    def updateItems(self, updatedItems): #updatedItems is a frozenset containing modified item. The value is -1 if unknow, 0 if mi
        return
     