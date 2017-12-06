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
        
        self.firstClick=True;
        self.constraintManager=ConstraintManager(self)
        self.width=width
        self.height=height
        self.nbMines=mines;
        self.length=height*width
        self.helper=0 #default = no helper selected
        self.view=view
        self.endGame=None #True = victory, false = lost
        
        self.itemsView=[None]*(width*height)
        self.itemsState=[-1]*(width*height) # -2 = flagged, -1=unknown, >=0 = number of surrounding mines
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
        self.endGame=False
    
    def doFirstClick(self, id, updateView):

        minePlaced=False
        while not minePlaced:
            i=randint(0, self.length)
            if not self.itemsValue[i]:
                minePlaced=True
                self.itemsValue[i]=True
                print "first click ("+str(id)+") was mined, moving this mine at index "+str(i)
        self.itemsValue[id]=False
        self.itemClicked(id, updateView, False)   
        
        
        
    def itemClicked(self, id, updateView=True, updateHelper=True):
        if(self.itemsState[id]==-1):
            if(self.itemsValue[id]!=-2):    #else, do nothing
                if(self.itemsValue[id]):
                    if not self.firstClick:
                        self.gameOver()
                    else:
                        self.doFirstClick(id, updateView)
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
                        self.updateStatus()
                        self.runHelper() 
                           
        self.firstClick=False
        
        
    def setVerboseDisplay(self, vd):
        self.verboseDisplay=vd
        self.runHelper() #update helper
        for i in self.getSurroundingIndexes(63):
            print i
            
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
           
        self.runHelper()
        self.updateStatus()
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
            self.itemsView[id].setProbability(p, self.verboseDisplay)
            
            
    def updateStatus(self):
        unknowCase=0
        for i in xrange(0, self.length):
            if self.itemsState[i]==-1:
                unknowCase+=1   
                
        #no suqare lefting and the user have not exploded !             
        if unknowCase==0 and self.endGame is None:
            self.endGame=True
        
        if self.endGame is None:
            count=0
            for i in xrange(0, self.length):
                if self.itemsState[i]==-2:
                    count+=1
            self.view.setStatus("Mines flagged : "+str(count)+"/"+str(self.nbMines)+". "+str(unknowCase)+" unknown squares.")
        elif self.endGame is True:
            self.view.setStatus(" You win !!! ")
            return True
        else: 
            self.view.setStatus(" Game over ! :( ")
            
        return False
        #all other case is not a win (so return false, but it not means "defeat"
            
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
        
        if leftBoundOffset!=0:
            yield id-1
                    
        if rightBoundOffset!=0:
            yield id+1
        
        if id<self.width*(self.height-1): #if it's not last line
            for i in range(id+self.width-(1*leftBoundOffset), id+self.width+(1*rightBoundOffset) +1):
                yield i
  
        