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
        
        self.constraints=ConstraintManager(self)
        self.width=width
        self.height=height
        self.length=height*width
        self.view=view
        self.itemsView=[None]*(width*height)
        self.itemsState=[-1]*(width*height) #state : -3 = mine hited (game over), -2 = flagged, -1=unknown, >=0 = number of surrounding mines
        #default state : unknown
        self.itemsValue=[False]*(width*height)
        
        minesLanded=0;
        while(minesLanded<mines):
            i=randint(0, (width*height)-1)
            if self.itemsValue[i] is not True:
                print str(i)+" mined !"
                self.itemsValue[i]=True
                minesLanded+=1
        
        
        
        
    def addItemView(self, index, pushButton): #argument expected: QPushButtonCustom
        self.itemsView[index]=pushButton
        pushButton.connect(pushButton, SIGNAL("clicked()"), lambda: self.itemClicked(pushButton))
        
    def gameOver(self):
        for i, val in enumerate(self.itemsValue):
            if(val):
                self.itemsView[i].setState(-3)
        
    def itemClicked(self, button):
        id=button.id
        if(self.itemsValue[id]):
            self.gameOver()
        else:
            surroundingMines=0;            
        
            for i in self.getSurroundingIndexes(id):
                if(self.itemsValue[i]):
                    surroundingMines+=1
                    
            self.itemsState[id]=surroundingMines
            button.setSurroundingMines(surroundingMines)
            print "printing constraints ..."
            for c in self.constraints.getConstraintsById(id):
                print c
                
    def knownId(self): #iterate for associating each id with nb of mines surrounding this suqare
        for id in xrange(0, length):
            if(itemsState[id]>=0):
                yield id, itemState[id]
            
    def setProbability(self, id, p):
        itemsView[id].setProbability(p)
            
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
                
        for i in range(id-1, id+2):
            yield i
        
        if id<self.width*(self.height-1): #if it's not last line
            for i in range(id+self.width-(1*leftBoundOffset), id+self.width+(1*rightBoundOffset) +1):
                yield i
  
        