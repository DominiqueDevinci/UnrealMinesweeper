from PyQt4.QtGui import *
from PyQt4.QtCore import *
from array import array
from random import randint
from ConstraintManager import ConstraintManager

class BoardController:
    
    def __init__(self, view, width, height, mines):
        
        if((width*height)/float(mines)<2):
            print "You have too much mines (>50%)"
            return
        
        self.constraintManager=ConstraintManager(self)
        self.width=width
        self.height=height
        self.length=height*width
        self.helper=0 #default = no helper selected
        self.view=view
        self.itemsView=[None]*(width*height)
        self.itemsState=[-1]*(width*height) #state : -3 = mine hited (game over), -2 = flagged, -1=unknown, >=0 = number of surrounding mines
        #default state : unknown
        self.itemsValue=[False]*(width*height)
        self.verboseDisplay=False;
        
        minesLanded=0;
        while(minesLanded<mines):
            i=randint(0, (width*height)-1)
            if self.itemsValue[i] is not True:
                print str(i)+" mined !"
                self.itemsValue[i]=True
                minesLanded+=1
        
        
        
        
    def addItemView(self, index, pushButton): #argument expected: QPushButtonCustom
        self.itemsView[index]=pushButton
        pushButton.connect(pushButton, SIGNAL("clicked()"), lambda: self.itemClicked(pushButton.id))
        pushButton.connect(pushButton, SIGNAL("rightClick()"), lambda: self.itemRightClicked(pushButton.id))
        
    def gameOver(self):
        for i, val in enumerate(self.itemsValue):
            if(val):
                self.itemsView[i].setState(-3)
        self.view.setStatus("Game over !")
        
    def itemClicked(self, id, updateView=True, updateHelper=True):
        if(self.itemsState[id]==-1):
            if(self.itemsValue[id]!=-2):    #else, do nothing
                if(self.itemsValue[id]):
                    self.itemsState[id]=-3 #lost
                    self.gameOver()
                else:
                    surroundingMines=0           
                    for i in self.getSurroundingIndexes(id):
                        if(self.itemsValue[i]):
                            surroundingMines+=1
                            
                    self.itemsState[id]=surroundingMines
                    
                    if surroundingMines==0: #uncover free surrounding spaces
                        for i in self.getSurroundingIndexes(id):
                            self.itemClicked(i, updateView, False) #don't update helper recursively ... just calculate it at the end !
                    
                    if updateView: #
                        self.itemsView[id].setSurroundingMines(surroundingMines)
                        self.runHelper()    
    
    def setVerboseDisplay(self, vd):
        self.verboseDisplay=vd
        self.runHelper() #update helper
            
    def runHelper(self):
        if(self.helper==1): #proba helper
            self.constraintManager.computeProbabilities()
        elif(self.helper==2):
            return;
        
    def cleanHelper(self):        
        for i in xrange(0, self.length):
                if self.itemsState[i]<0: # if uncovered case, remove probability from button text
                    self.itemsView[i].setText("")
                    
    def setHelper(self, idHelper):
        if(idHelper==1 or idHelper==2):
            self.helper=idHelper
            self.runHelper()
        else:
            self.helper=0
            self.cleanHelper()
                    
    def itemRightClicked(self, id):
        if(self.itemsState[id]==-1):
            self.setFlag(id, True)
        elif(self.itemsState[id]==-2):
            self.setFlag(id, False)
            
        #else do nothing
    
    def setFlag(self, id, flagged):        
        if flagged is True:
            self.itemsState[id]=-2
        else:
            self.itemsState[id]=-1
            
        self.itemsView[id].setFlag(flagged)
        
            
                
    def knownId(self): #iterate for associating each id with nb of mines surrounding this suqare
        for id in xrange(0, self.length):
            if(self.itemsState[id]>=0):
                yield id, self.itemsState[id]
            
    def setProbability(self, id, p):
        if self.itemsState[id]==-1: #dont display probability if square is known
            self.itemsView[id].setProbability(p, self.verboseDisplay)
            
            
    def getSurroundingIndexesOld(self, id):
        listIndex=list()
        
        
        leftBoundOffset=1         
        if id%self.width==0: #bord left
            leftBoundOffset=0
            
        rightBoundOffset=1
        if id%self.width==(self.width-1): #bord left
            rightBoundOffset=0

        if id>=self.width: #if it's not first line            
            for i in range(id-self.width-(1*leftBoundOffset), id-self.width+(1*rightBoundOffset) +1):
                 listIndex.append(i)
                
        for i in range(id-1, id+2):
            listIndex.append(i)
        
        if id<self.width*(self.height-1): #if it's not last line
            for i in range(id+self.width-(1*leftBoundOffset), id+self.width+(1*rightBoundOffset) +1):
                listIndex.append(i)
                        
        return listIndex
            
    def getSurroundingIndexes(self, id): #iterable version of getSurroundingIndex (best performances)
        
        leftBoundOffset=1         
        if id%self.width==0: #bord left
            leftBoundOffset=0
            
        rightBoundOffset=1
        if id%self.width==(self.width-1): #bord left
            rightBoundOffset=0

        if id>=self.width: #if it's not first line            
            for i in range(id-self.width-(1*leftBoundOffset), id-self.width+(1*rightBoundOffset) +1):
                 yield i
                
        for i in range(id-(1*leftBoundOffset), id+1*rightBoundOffset +1):
            yield i
        
        if id<self.width*(self.height-1): #if it's not last line
            for i in range(id+self.width-(1*leftBoundOffset), id+self.width+(1*rightBoundOffset) +1):
                yield i
  
        