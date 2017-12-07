from PyQt4.QtGui import *
from PyQt4.QtCore import *
from array import array
from random import randint
from ConstraintManager import ConstraintManager
from time import sleep


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
        self.probabilties=[-1.0]*self.length
        self.itemsView=[None]*self.length
        self.itemsState=[-1]*self.length # -2 = flagged, -1=unknown, >=0 = number of surrounding mines
        #default state : unknown
        self.itemsValue=[False]*(width*height)
        self.verboseDisplay=False
        self.updateView=True
        
        minesLanded=0;
        while(minesLanded<mines):
            i=randint(0, (width*height)-1)
            if self.itemsValue[i] is not True:
                self.itemsValue[i]=True
                minesLanded+=1
        
        
        
        
    def addItemView(self, index, pushButton): #argument expected: QPushButtonCustom
        self.itemsView[index]=pushButton
        pushButton.connect(pushButton, SIGNAL("clicked()"), lambda: self.itemClicked(pushButton.id))
        pushButton.connect(pushButton, SIGNAL("rightClick()"), lambda: self.itemRightClicked(pushButton.id))
        
    def gameOver(self):
        if self.updateView:
            for i, val in enumerate(self.itemsValue):
                if(val):
                    self.itemsView[i].setState(-3)
            self.view.setStatus("Game over !")
        self.endGame=False
    
    def doFirstClick(self, id, updateView):
        minePlaced=False
        while not minePlaced:
            i=randint(0, self.length-1)
            if not self.itemsValue[i]:
                minePlaced=True
                self.itemsValue[i]=True
                print "first click ("+str(id)+") was mined, moving this mine at index "+str(i)
        self.itemsValue[id]=False
        self.itemClicked(id, updateView, False)   
        
    
    def browseProbZero(self):
        for i in xrange(0, self.length):
            if self.itemsState[i]==-1 and int(self.probabilties[i]*100)==0:
                yield i
                
    def browseProb100(self):
        for i in xrange(0, self.length):
            if self.itemsState[i]==-1 and int(self.probabilties[i]*100)==100:
                yield i
                
    def browseProbUnknow(self):
        for i in xrange(0, self.length):
            if self.itemsState[i]==-1 and self.probabilties[i]<0:
                yield i
                
    def getLowestProb(self):
        id_lowest=-1
        for i in xrange(0, self.length):
            if self.itemsState[i]==-1 and self.probabilties[i]>=0.0:
                if id_lowest==-1:
                    id_lowest=i
                elif self.probabilties[i]<self.probabilties[id_lowest]:
                    id_lowest=i
        return id_lowest, self.probabilties[id_lowest]
                
    def getRandomUnknown(self):
        tmp=list(self.browseProbUnknow())
        nb=len(tmp)
        if nb>0: #if there are still some unknown prob squares ...
            randId=tmp[randint(0, nb-1)]
            return randId, self.probabilties[randId]
        else: #no unknown square lefting ...
            #print "Huuh ... it's crap shoot !"
            return self.getLowestProb()
        
    def autoSolve(self, updateView=True):        
        self.updateView=updateView
        limit=0
        flagged=0    
        self.runHelper()
        clicked=True
        while clicked:
            clicked=False
            while self.endGame is None and limit<=self.length:
                sleep(0.1)

                #compute random percent
                cr=0
                for i in xrange(0, self.length):
                    if self.itemsState[i]==-1:
                        cr+=1
                
                if self.nbMines-flagged==0:
                    self.endGame=True
                    break
                else:
                    percent=(self.nbMines-flagged)/float(cr)
                    
                #print "percent ="+str(percent*100)+"%"

                limit+=1
                
                '''
                Clicking on safe squares 
                '''
                
                for safeId in self.browseProbZero():
                    self.itemClicked(safeId, updateView, True) #no view, helper activated
                    clicked=True
                    
                if clicked:
                    break; #if action is done, relooping to take account of modifications
                
                
                '''
                Flagging  squares with p=100% 
                '''
                clicked=False   
                for minedId in self.browseProb100():
                    #print "flagging ..."
                    self.setFlag(minedId, True, False) #no view, helper activated
                    flagged+=1
                    clicked=True
                    
                if clicked:
                    break;
                
    
                '''
                Clicking on square with lowest probability (if p<20% )
                '''
                
                id, prob=self.getLowestProb()
                if id>=0 and 0.0 <= prob*100<percent:
                    #print "clicking on "+str(id)+" which have p="+str(prob)
                    self.itemClicked(id, False, True)
                else:
                    #print "Lowest prob is "+str(prob)+". Click on random case (wich prob is unknow), or if not exists on lowest possible prob ..."
                    id, prob=self.getRandomUnknown()
                    #print "clicking on "+str(id)+" (prob="+str(prob)  
                    self.itemClicked(id, False, True)
                    
        #print "end ! limit = "+str(limit)+" and endGame = "+str(self.endGame)+" & clicked = "+str(clicked)
        self.updateView=True
        return self.endGame;
    def itemClicked(self, id, updateView=True, updateHelper=True):
        if(self.itemsState[id]==-1):
            if(self.itemsValue[id]!=-2):    #else, do nothing
                if(self.itemsValue[id]):
                    if not self.firstClick:
                        print "clicked on mine "+str(id)+", game over ..."
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
                    
    def itemRightClicked(self, id, updateView=True):
        
        if(self.itemsState[id]==-1):
            self.setFlag(id, True)
        elif(self.itemsState[id]==-2):
            self.setFlag(id, False)
           
        self.runHelper()
        if updateView:
            self.updateStatus()
        #else do nothing
    
    def setFlag(self, id, flagged, updateView=True):        
        if flagged is True:
            self.itemsState[id]=-2
        else:
            self.itemsState[id]=-1
            
        if updateView:
            self.itemsView[id].setFlag(flagged)
        
            
                
    def knownId(self): #iterate for associating each id with nb of mines surrounding this suqare
        for id in xrange(0, self.length):
            if(self.itemsState[id]>=0):
                yield id, self.itemsState[id]
            
    def setProbability(self, id, p):
            self.probabilties[id]=p
            if self.updateView:
                self.itemsView[id].setProbability(p, self.verboseDisplay)
                
    def repaintView(self):
        for i in xrange(0, self.length):
            self.itemsView[i].setSurroundingMines(self.itemsState[i])
            
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
  
        