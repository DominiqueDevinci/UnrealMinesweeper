from Util import choose

class ProbProcessor:
    
    def __init__(self, boardController):
        self.board=boardController
        
    def getSurroundingUnknown(self, id):
        for i in self.board.getSurroundingIndexes(id):
            if(self.board.itemsState[i]==-1):
                yield i #return square id if it is concerned by the number of mines

    def getSurroundingFlagged(self, id):        
        for i in self.board.getSurroundingIndexes(id):
            if(self.board.itemsState[i]==-2):
                yield i #return square id if it is concerned by the number of mines
            
    def computeProbabilities(self, level=1): #compute probabilities omiting their inter-coupling
        
        sumpProbabilities=[0]*self.board.length #sum of probablities
        couplingNumber=[0]*self.board.length #number of added probablities (to make a average with sumProbabilities)
        trivialPatternsFound=0
        confirmedResult=[None]*self.board.length
        
        for knowId, nbMines in self.board.knownId():
            surroundingUnknown=frozenset(self.getSurroundingUnknown(knowId)) #get static constraints
            surroundingFlagged=frozenset(self.getSurroundingFlagged(knowId))
            
            nbUnknownNeighbour=len(surroundingUnknown)

            mineConfirmed=False #if we are sure that all neighbour are mined
            allSafe=False #if we are sure that all neighboor are safe
            
            #print "id="+str(knowId)+" & nbUnknownNeighbour = "+str(nbUnknownNeighbour)+" & nbMines = "+str(nbMines)
            
            if nbUnknownNeighbour==(nbMines-len(surroundingFlagged)):
                '''print str(knowId)+" condition 1 filled ("+str(nbUnknownNeighbour)+", "+str(nbMines)+", "+str(len(surroundingFlagged))+")"
                for ii in self.board.getSurroundingIndexes(knowId):
                    print str(ii)+" => "+str(self.board.itemsState[ii])'''
                mineConfirmed=True
            elif (nbMines-len(surroundingFlagged))<=0:
                #print str(knowId)+" condition 2 filled ("+str(nbUnknownNeighbour)+", "+str(nbMines)+")"
                allSafe=True
                                 
            for id in surroundingUnknown:
                if mineConfirmed:
                    confirmedResult[id]=True
                elif allSafe:
                    confirmedResult[id]=False
                else:
                    if(level>0): #if level is 0, don"t compute intermediate probabilities.
                        sumpProbabilities[id]+=(nbMines-len(surroundingFlagged))/float(nbUnknownNeighbour)
                        couplingNumber[id]+=1
                
        
        for i in xrange(0, self.board.length):
            if confirmedResult[i] is not None:
                trivialPatternsFound+=1
                if confirmedResult[i]:
                    self.board.setProbability(i, 1.0)
                else:
                    self.board.setProbability(i, 0.0)
            elif couplingNumber[i]>0:
                if(int(sumpProbabilities[i]/couplingNumber[i]*100)==100):
                    self.board.setProbability(i, 0.99) 
                else:
                    if sumpProbabilities[i]/couplingNumber[i]>1:
                        print "uncoherent probability : "+str(sumProbabilities[i])+" / "+str(couplingNumber[i])
                    self.board.setProbability(i, sumpProbabilities[i]/couplingNumber[i]) 
                
        return trivialPatternsFound
        
        