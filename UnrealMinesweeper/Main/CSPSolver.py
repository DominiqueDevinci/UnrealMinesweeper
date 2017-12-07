# -*- coding: utf-8 -*-

import sys
from Util import choose


class ConstraintSet:
    def __init__(self, id, states): # a constraint set is defined by this id, and its constraints are dynamically computed from states
        self.id=id
        self.states=states
        
   

class CSPSolver:
    
    def __init__(self, itemsState, width, height): #build set constraints
        self.states=list(itemsState)
        self.width=width
        self.height=height
        self.length=width*height
        
        assert (len(itemsState)==self.length), "width*height is not equals to states.length !"
    
    def recurUndermineArea(self, freeArea, nbLeftingMine): #recursive function to undermine K suare among N free squre    
        if nbLeftingMine>0:
            for freeId in freeArea.copy():
                if self.states[freeId]==-1:
                    self.states[freeId]=-2 #consider this square is mined (=> flag it)
                    if nbLeftingMine>1:
                        freeArea.remove(freeId) #because we search all combinations WITHOUT DUPLICATES ( binomial_factor and no factorial_factor)
                        for x in self.recurUndermineArea(freeArea, nbLeftingMine-1): #in Python 3.3 there is syntax "yield from". Not in python 2.7 ...
                            yield x
                    else:
                        #if we have land the last lefting mine, "lock" another squares to "free" (value : -4) to forbid other constraint to modify that
                        yield True    
                    self.states[freeId]=-1 #after yield, cancel the flag
        
                    
        yield False
        
    def solve(self):
        for i in xrange(0, self.length):
           
            if self.states[i]>=0: #if squarre is not unknow, we have associated constraints
               

                self.computeTree(i, set())
                
    
    def computeTree(self, id, constraintTree):        
        if id not in constraintTree: #to avoid cycles
            constraintTree.add(id)
            print "deep="+str(len(constraintTree)    )   
            print "browsing constraint trees from square "+str(id)
            
            for b in self.nextConsistentConfig(id):
                
                if b is True:
                    t=True
                    for connectedId in self.browseConnectedConstraints(id, constraintTree):
                        print "check matches with constraint set no"+str(connectedId)
                        c=self.computeTree(connectedId, constraintTree)
                        t=False
                    if not t:
                        sys.stdout.write("End of tree (deep="+str(len(constraintTree))+". Config available : ")
                        print self.states
           
    def browseConnectedConstraints(self, id, constraintTree): #constraintTree est un set qui contient les id des ensembles de contraintes parcourus (pour éviter de provoquer un "cycle" dans l'arbre)
        for i in self.getSurroundingIndexes(id):
            if self.states[i]>=0 and i not in constraintTree:
                yield i
                
        
        
    def nextConsistentConfig(self, id):
        unknownArea=set()
        F=0 #nb flags
        N=0 #nb of  neighbors
        K=self.states[id] #nb mines
        val=0
        for i in self.getSurroundingIndexes(id):
            val=self.states[i]
            if(val<0):
                N+=1
                
                if val==-2:
                    F+=1
                else:
                    unknownArea.add(i) #add this unknown neighbor to unknown area
        
        print str(N)+" unknown neighbors, but "+str(F)+" re flagged, len(unknownArea)="+str(len(unknownArea))+" and nb mines = "+str(K)
        
        if F==K:
            print "F==K, nothing to do !"
            yield True
        elif F>K:
            print "F>K, not possible !"
            yield False
        else:        
            for i in self.recurUndermineArea(unknownArea, K-F):
                if i:
                    #sys.stdout.write("Configuration possible : ")
                    #print self.states;
                    yield True
        
            yield False
                
        
    
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
                

def test():    
    states=[-1, 2, -1, 2, -1, -1, -1, 1, -1]
    print states
    solver=CSPSolver(states, 3, 3)
    solver.solve()
    
test()    
    