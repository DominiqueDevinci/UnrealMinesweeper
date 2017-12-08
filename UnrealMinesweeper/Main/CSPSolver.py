# -*- coding: utf-8 -*-

import sys
from Util import choose


class ConstraintSet:
    def __init__(self, id, states): # a constraint set is defined by this id, and its constraints are dynamically computed from states
        self.id=id
        self.states=states
        
   

class CSPSolver:
    
    def __init__(self, itemsState, width, height): #build set constraints
        self.frozenStates=list(itemsState)
        self.width=width
        self.height=height
        self.length=width*height
        
        assert (len(itemsState)==self.length), "width*height is not equals to states.length !"
        
        self.buildEdges()
    
    
    def recurUndermineArea(self, freeArea, nbLeftingMine): #recursive function to undermine K suare among N free squre    
        if nbLeftingMine>0:
            #print "free area :"+str(len(freeArea))
            for freeId in freeArea.copy():
                if self.states[freeId]==-1:
                    self.states[freeId]=-2 #consider this square is mined (=> flag it)
                    if nbLeftingMine>1:                        
                        freeArea.remove(freeId) #because we search all combinations WITHOUT DUPLICATES ( binomial_factor and no factorial_factor)
                        for x in self.recurUndermineArea(freeArea, nbLeftingMine-1): #in Python 3.3 there is syntax "yield from". Not in python 2.7 ...
                            yield x
                        
                    else:
                        #if we have land the last lefting mine, "lock" another squares to "safe" (value : -4) to forbid other constraint to modify that
                        for j in freeArea:
                            if self.states[j]==-1:
                                self.states[j]=-4
                                
                        yield True    
                        
                    self.states[freeId]=-4 #after consdiering all cases where freeID is flagged, it is free in other cases
                    for j in freeArea: #and reset free area
                            if self.states[j]==-4:
                                self.states[j]=-1
                    
        yield False
        
    def solve(self):
        
        self.results=[-1]*self.length #contains tuples: first is nb of configurations available, second tab is nb of mined configurations
        self.beginResults()
        self.states=list(self.frozenStates); #copy list
        for i in xrange(0, self.length):
           
            if self.states[i]>=0: #if squarre is not unknow, we have associated constraints        
                
                self.computeTree(i, set())
                self.states=list(self.frozenStates); #reinit original stats after each main edge

                
    def beginResults(self):
        for i in xrange(0, self.length):
            self.results[i]=[0, 0]
        
    def commitResults(self):
        val=0
        for i in xrange(0, self.length):
            val=self.states[i]
            if val==-2: #flag (considered as mined)
                self.results[i][0]+=1
                self.results[i][1]+=1 #considered as mined
            elif val==-4:
                self.results[i][0]+=1
                # considered as safe, so we don't increment counter of mined configs
                
    def computeProbabilities(self):
        probs=[-1]*self.length
        for i in xrange(0, self.length):
            if self.results[i][0]>0: #this suqare appear in some configs ...
                if self.results[i][1]==0: #square always considred as safe
                    probs[i]=0.01
                else:
                    probs[i]=self.results[i][1]/float(self.results[i][0])
        return probs
                
    
    def computeTree(self, id, constraintTree):        
        if id not in constraintTree: #to avoid cycles
            constraintTree.add(id)
            #print "deep="+str(len(constraintTree)    )   
            #print "browsing constraint trees from square "+str(id)
            
            for b in self.nextConsistentConfig(id):
                
                if b is True:
                    
                    for connectedId in self.browseConnectedConstraints(id, constraintTree):
                        #print "check matches with constraint set no"+str(connectedId)
                        c=self.computeTree(connectedId, constraintTree)
                    
                    #sys.stdout.write("End of tree - no more constraints. (deep="+str(len(constraintTree))+". Config available : ")
                    #print self.states
                    self.commitResults() #register results
           
    def browseConnectedConstraints(self, id, constraintTree): #constraintTree est un set qui contient les id des ensembles de contraintes parcourus (pour éviter de provoquer un "cycle" dans l'arbre)
        for i in self.edges[id]:
            if self.states[i]>=0 and i not in constraintTree:
                yield i
                
        
        
    def nextConsistentConfig(self, id):
        unknownArea=set()
        F=0 #nb flags
        N=0 #nb of  neighbors
        S=0 # nb of squares locked as "safe"
        K=self.states[id] #nb mines
        val=0
        for i in self.getSurroundingIndexes(id):
            val=self.states[i]
            if(val<0):
                N+=1
                
                if val==-2:
                    F+=1
                elif val==-4:
                    S+=1
                else:
                    unknownArea.add(i) #add this unknown neighbor to unknown area
        
        #print str(N)+" unknown neighbors, but "+str(F)+" are flagged and "+str(S)+" a locked as 'safe', len(unknownArea)="+str(len(unknownArea))+" and nb mines = "+str(K)
        
        if len(unknownArea)<(K-F): #if unknwon area is smaller than surrounding mine lefting, this config is inconsistent
            #print "inconcistent config !"
            yield False
        if F==K:
            #print "F==K, nothing to do !"
            yield True
        elif F>K:
            #print "F>K, not possible !"
            yield False
        else:        
            for i in self.recurUndermineArea(unknownArea, K-F):
                if i:
                    #sys.stdout.write("Configuration possible : ")
                    #print self.states;
                    yield True
            
            yield False
                
    def buildEdges(self): #preprocess connections between consraint domains
        self.edges=[None]*self.length
        for i in xrange(0, self.length):
            connectedDomains=set()
            if self.frozenStates[i]>=0:
                for j in self.getSurroundingIndexes(i):
                     
                    if self.frozenStates[j]>=0: #All known square surrounding current square is connected 
                        connectedDomains.add(j)
                   
                    for j2 in self.getSurroundingIndexes(j): # But squares wich are surrounding the last square is also connected (okay, this is bad perfs method) '''
                        if self.frozenStates[j2]>=0:
                            connectedDomains.add(j2)    # i think to totally change this part using intersects and matrix with numpy '''
                        
                                                         #the perfs of this sofwatre is not a priority, the winrate is at once the priority
            self.edges[i]=connectedDomains
        
    
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
    #states=[-1, 2, -1, 2, -1, -1, -1, 1, -1]
    states=[2, -1, -1,
            -1, -1, -1,
            -1, 2, -1,
            -1, -1, -1]
    print states
    solver=CSPSolver(states, 3,4)
    solver.solve()
    
test()    
    