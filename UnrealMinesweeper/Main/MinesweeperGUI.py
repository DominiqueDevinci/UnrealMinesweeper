import sys

from PyQt4.QtGui import *
from PyQt4.QtCore import *

from ImageLoader import ImageLoader
from BoardController import BoardController
from Util import choose
from QPushButtonCustom import QPushButtonCustom
from time import sleep

import Solver

class MinesweeperGUI(QMainWindow):
    def __init__(self, parent = None):
        super(MinesweeperGUI, self).__init__(parent)       
        self.benchmarking=False
        
        self.setCentralWidget(QWidget(self))
        self.setWindowTitle(" Unreal Minesweeper ")
        
        
        
        #Menu
        menubar = self.menuBar()
        benchMenu = menubar.addMenu(" Benchmark ")  
        newGameMenu=menubar.addMenu(" Game ")   
        helperMenu=menubar.addMenu(" Helper ") 
        solverMenu=menubar.addMenu(" Solver ") 
        debugMenu=menubar.addMenu(" Debug ") 
        
        ''' 
                Benchmark menu
        '''
        benchmarkProbasV1=QAction(" Benchmark probabilistic algorithm v1", self)
        benchmarkProbasV1.triggered.connect(self.runBenchmarkProbasV1)                
  
        benchMenu.addAction(benchmarkProbasV1)
        
        ''' 
                Game menu
        '''
        newGameEasy=QAction(" Easy (8x8  + 10 mines) ", self)
        newGameIntermediate=QAction(" Easy (16x16  + 40 mines) ", self)
        newGameHard=QAction(" Easy (30x16  + 99 mines) ", self)
        
        newGameEasy.triggered.connect(lambda: self.newGame(8, 8, 10))
        newGameIntermediate.triggered.connect(lambda: self.newGame(16, 16, 40))
        newGameHard.triggered.connect(lambda: self.newGame(30, 16, 99))
        
        newGameMenu.addAction(newGameEasy)
        newGameMenu.addAction(newGameIntermediate)
        newGameMenu.addAction(newGameHard)      
    
        '''layout.addWidget(QPushButton(" Probabilistic solver : next step"))
        layout.addWidget(QPushButton(" Probabilistic solver : auto-solve"))
        
        layout.addWidget(QPushButton(" CSP Solver : next step "))
        layout.addWidget(QPushButton(" CSP Solver : auto-solve "))'''

        ''' 
                Helper menu
        '''
        
        helpers=QActionGroup(self, exclusive=True)
        
        self.helperNone=helpers.addAction(QAction(" No helper ! ", self, checkable=True, checked=True))
        self.helperNone.triggered.connect(self.setHelper)        
        helperMenu.addAction(self.helperNone)
        
        self.helperProba=helpers.addAction(QAction(" Probabilistic approach ", self, checkable=True))
        self.helperProba.triggered.connect(self.setHelper)        
        helperMenu.addAction(self.helperProba)
        
        self.helperCSP=helpers.addAction(QAction(" CSP approach ", self, checkable=True))
        self.helperCSP.triggered.connect(self.setHelper)        
        helperMenu.addAction(self.helperCSP)
        
        ''' 
                Helper menu
        '''
        self.verboseDisplay=QAction(" Verbose display ", self, checkable=True)
        self.verboseDisplay.triggered.connect(self.setDebug)
        debugMenu.addAction(self.verboseDisplay)
        
        ImageLoader.init();      
        self.mainLayout=None
        self.setStatus(" Ready to play ! ");
        
        
    def setDebug(self):
        self.boardController.setVerboseDisplay(self.verboseDisplay.isChecked())

    def setHelper(self):
        if self.helperProba.isChecked():
            self.boardController.setHelper(1)
        elif self.helperCSP.isChecked():
            self.boardController.setHelper(2)
        else:
            self.boardController.setHelper(0)
  
    def setStatus(self, str, force=False):
        if not self.benchmarking or force:    
            self.statusBar().showMessage(str)
        
    def runBenchmarkProbasV1(self):
        self.benchmarking=True
        victory=0
        defeat=0
        
        width=16
        height=16
        mines=40
        
        for i in xrange(0, 1000+1):
            sleep(1)
            self.newGame(width, height, mines, True)
            rs=self.boardController.autoSolve(True) #disable updateView
            if rs is None or rs is True:
                if rs is True:
                    victory+=1
                    break
                else:
                    break
            else:
                defeat+=1
                
            nb=victory+defeat
            
            if i%50==0:
                self.setStatus(str(nb)+" battles. Winrate : "+str(victory/float(nb)*100)+"% ("+str(victory)+"/"+str(defeat)+"). Config : "+str(width)+"x"+str(height)+" with "+str(mines)+" mines (density : "+str(float(mines)/(width*height)*100)+"% )", True)
        
        self.boardController.repaintView()   
        sleep(5)
        self.benchmarking=False
    def initBoard(self):        
        count=0
        #init empty board
        for l in range(0, self.height):
            tmpLayout=QHBoxLayout()
            tmpLayout.setMargin(0)
            tmpLayout.setSpacing(0)
            tmpLayout.addStretch()
            for c in range(0, self.width):                
                button=QPushButtonCustom(count)
                self.boardController.addItemView(count, button)               
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

                 
    def newGame(self, width, height, mines, withView=True):
        
        #if self.mainLayout is not None:
        #    self.clearLayout(self.mainLayout)
       
        if withView:
            oldWidget=self.centralWidget()
            oldWidget.deleteLater()
            
            
            self.setCentralWidget(QWidget())
            layout = QVBoxLayout(self.centralWidget())
            layout.addStretch()
            layout.setMargin(0)
            layout.setSpacing(0)
            self.mainLayout=layout;
            
            
            self.height=height
            self.width=width
            self.length=height*width
            self.mines=mines
            
        self.boardController=BoardController(self, width, height, mines)
        
        if withView:
            self.initBoard() 
            
        self.setHelper()
        self.setStatus(" ready to play ! ")

     