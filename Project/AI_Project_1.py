#from gettext import npgettext
#from multiprocessing import dummy
#from queue import PriorityQueue
#import heapq
#from tabnanny import check
from typing import List
#from xml.dom.minidom import Childless
import numpy as np
import time
#from dataclasses import dataclass, field
#from typing import Any

#@dataclass(order=True)
class PrioritizedItem:
    #priority: int
    #item: Any=field(compare=False)
    def __init__(self, priority, data) -> None:
        self.priority = priority
        self.data = data
        pass

    def getPriority(self):
        return self.priority

    def getData(self):
        return self.data


#print ('hello world')

#   https://www.codingem.com/numpy-compare-arrays/#:~:text=The%20easiest%20way%20to%20compare,if%20the%20elements%20are%20True. help for comparing arrays
#   https://docs.python.org/3/library/queue.html The Queues
#   function general-search(problem, QUEUEING-FUNCTION)
#       nodes = MAKE-QUEUE(MAKE_NODE(problem.INITIAL-STATE))
#       loop do
#           if EMPTY(nodes) then return "failure"
#           node = REMOVE-FRONT(nodes)
#           if problme.GOAL-TEST(node.STATE) succeeds then return node
#           nodes = QUEUEING-FUNCTION(nodes, EXPAND(nod,problem.OPERATORS))
#   end
#
#                      GENERAL SEARCH ALGORITHM
#
#                   8-puzzle game
#                   Goals [1,2,3]
#                         [4,5,6]
#                         [7,8,0]
#                   where 0 is considered the placeholder for the empty space
#                   need to implement, Uniform cost search (A* with h(n)=0), Misplaced tile hueristic, manhattan distance hueristic
#                   A* works with f(n) = g(n) + h(n) where g(n) is distance from initial to current and g(n) is estimated distance from current to goal
#           Things we need for search algorithms:
#           Start state, Operators, goal state
#
         
GoalState = np.array([[1,2,3],[4,5,6],[7,8,0]])
#lets make an arbitrary initial state for now
#                 Initial [1,2,3]
#                         [4,0,5]
#                         [7,8,6]
#later on, make a function that'll randomize the initial state
#InitialState = np.array([[1,2,3],[4,5,6],[0,7,8]]) #Depth 2
#InitialState = np.array([[1,2,3],[5,0,6],[4,7,8]]) #Depth 4
#InitialState = np.array([[1,3,6],[5,0,2],[4,7,8]]) #Depth 8
#InitialState = np.array([[1,3,6],[5,0,7],[4,8,2]]) #Depth 12
#InitialState = np.array([[1,6,7],[5,0,3],[4,8,2]]) #Depth 16
#InitialState = np.array([[7,1,2],[4,8,5],[6,3,0]]) #Depth 20
InitialState = np.array([[0,7,2],[4,6,1],[3,5,8]]) #Depth 24

class nodes:
    def __init__(self,Array):
        self.Array = Array
        self.Gn = 1 #depth
        self.Hn = 0 #estimated cost to goal
        #self.children = children
        #self.parents = parents
        self.ChildList=list(())
        self.ChildCount = 0
        tmp = np.where(Array == 0)
        self.BlankRow = tmp[0][0] #would output as an array with a single element, get the value byt doing BlankRow[0]
        self.BlankColumn = tmp[1][0]#find location of blank (0)
    def getArray(self):
        return self.Array    
    def printValue(self):
        print(self.Array)
    def setParent(self, parent):
        self.parent = parent   
    def getParent(self):
        return self.parent
    def getChildCount(self):
        return self.ChildCount   
    def createChildren(self): #create new arrays
        #self.ChildArray=np.array([])
        #currChild = 0
        if (self.BlankRow)-1 >=0: #we can go up
            temporary = np.copy(self.Array) # Normal equals doesn't work, it just a pass by reference
            number = temporary[self.BlankRow-1][self.BlankColumn]
            temporary[self.BlankRow-1][self.BlankColumn] = 0
            temporary[self.BlankRow][self.BlankColumn] = number
            checkParent = (temporary == self.parent.getArray()).all()
            if not checkParent:
                tmp = nodes(temporary)
                tmp.setParent(self)
                tmp.Gn = self.Gn + 1
                self.ChildList.append(tmp)
                #np.append(self.ChildArray,tmp)
                #np.insert(self.ChildArray,currChild,tmp)
                #currChild+=1
                #print("we can go up")
                self.ChildCount+=1           

        if (self.BlankRow)+1 <=2: #we can go down
            temporary = np.copy(self.Array)
            number = temporary[self.BlankRow+1][self.BlankColumn]
            temporary[self.BlankRow+1][self.BlankColumn] = 0
            temporary[self.BlankRow][self.BlankColumn] = number
            checkParent = (temporary == self.parent.getArray()).all()
            if not checkParent:
                tmp = nodes(temporary)
                tmp.setParent(self)
                tmp.Gn = self.Gn + 1
                self.ChildList.append(tmp)
                #np.append(self.ChildArray,tmp)
                #np.insert(self.ChildArray,currChild,tmp)
                #currChild+=1
                #print("we can go down")
                self.ChildCount+=1   
            
        if (self.BlankColumn)-1 >=0: #we can go Left
            temporary = np.copy(self.Array)
            number = temporary[self.BlankRow][self.BlankColumn-1]
            temporary[self.BlankRow][self.BlankColumn-1] = 0
            temporary[self.BlankRow][self.BlankColumn] = number
            checkParent = (temporary == self.parent.getArray()).all()
            if not checkParent:
                tmp = nodes(temporary)
                tmp.setParent(self)
                tmp.Gn = self.Gn + 1
                self.ChildList.append(tmp)
                #np.append(self.ChildArray,tmp)
                #np.insert(self.ChildArray,currChild,tmp)
                #currChild+=1
                #print("we can go left")
                self.ChildCount+=1   
            
        if (self.BlankColumn)+1 <=2: #we can go Right
            temporary = np.copy(self.Array)
            number = temporary[self.BlankRow][self.BlankColumn+1]
            temporary[self.BlankRow][self.BlankColumn+1] = 0
            temporary[self.BlankRow][self.BlankColumn] = number
            checkParent = (temporary == self.parent.getArray()).all()
            if not checkParent:
                tmp = nodes(temporary)
                tmp.setParent(self)
                tmp.Gn = self.Gn + 1
                self.ChildList.append(tmp)
                #np.append(self.ChildArray,tmp)
                #np.insert(self.ChildArray,currChild,tmp)
                #currChild+=1
                #print("we can go Right")
                self.ChildCount+=1   
    def getChild(self, number):
        return self.ChildList[number]
    def printChild(self, number):
        self.ChildList[number].printValue()

def UniformCS(StartingState, QueueingFunction, Goal): #function general-search(problem, QUEUEING-FUNCTION)
    failure = False
    priority = 1 #this is essentially the f(n)
    #QueueingFunction = PriorityQueue(0)
    StartNode = nodes(StartingState)        #
    StartNode.setParent(StartNode)
    QueueingFunction.append(PrioritizedItem(priority,StartNode))
    #np.append(QueueingFunction, PrioritizedItem(priority,StartNode), axis=0)     #nodes = MAKE-QUEUE(MAKE_NODE(problem.INITIAL-STATE))
    UniqueList = list(())
    UniqueList.append(PrioritizedItem(priority,StartNode))
    while not failure:                      #loop do
        if len(QueueingFunction)==0:        #if EMPTY(nodes) then return "failure"
            failure = True
            #print("not a searchable state \n")
            return False                            
        #print('. . .')
        #print(QueueingFunction)

        index = 0
        for N in range(len(QueueingFunction)):
            if(int(QueueingFunction[N].getPriority())<int(QueueingFunction[index].getPriority())):
                print("found a smaller value")
                index = N
        temp = QueueingFunction[index]                              #node = REMOVE-FRONT(nodes)
        #print("looking through node with: " + str(QueueingFunction[index].getPriority()) + " Priority")    
        QueueingFunction.pop(index)
        #np.delete(QueueingFunction,N, axis=0)
        #QueueingFunction.task_done
        #print(temp.getData())
        CheckingArray = (Goal == temp.getData().getArray()).all()     
        if(CheckingArray ==True):           #if problem.GOAL-TEST(node.STATE) succeeds then return node
            print("found it")
            return temp.getData()
        else:
            priority+=1
            temp.getData().createChildren()           #nodes = QUEUEING-FUNCTION(nodes, EXPAND(nod,problem.OPERATORS))
            for x in range(temp.getData().getChildCount()):
                #temp[1].printChild(x)
                #print(x)
                
                dummy = PrioritizedItem(priority, temp.getData().getChild(x))
                isUnique = True
                for j in range(len(UniqueList)):
                    chkArray = (UniqueList[j].getData().getArray() == temp.getData().getChild(x).getArray()).all()
                    if(chkArray == True):
                        isUnique = False
                if(isUnique):
                    QueueingFunction.append(dummy)
                      
def AStarMisplacedTile(StartingState, QueueingFunction, Goal): #same as uniform but 
    failure = False
    priority = 1                                                #this is essentially the f(n)
    StartNode = nodes(StartingState)        #
    StartNode.setParent(StartNode)
    QueueingFunction.append(PrioritizedItem(priority,StartNode))
    UniqueList = list(())
    UniqueList.append(PrioritizedItem(priority,StartNode))
    while not failure:                                          #loop do
        if len(QueueingFunction)==0:                            #if EMPTY(nodes) then return "failure"
            failure = True
            print("not a searchable state \n")
            return False      
        #print('. . .')                      
        index = 0
        for N in range(len(QueueingFunction)):
            if(int(QueueingFunction[N].getPriority())<int(QueueingFunction[index].getPriority())):
                #print("found a smaller value")
                index = N
        temp = QueueingFunction[index]                              #node = REMOVE-FRONT(nodes)
        #print("looking through node with: " + str(QueueingFunction[index].getPriority()) + " Priority")    
        QueueingFunction.pop(index)
        CheckingArray = (Goal == temp.getData().getArray()).all()     
        if(CheckingArray ==True):                               #if problem.GOAL-TEST(node.STATE) succeeds then return node
            print("found it")
            return temp.getData()
        else:
            priority+=1
            Hn = 0                                         
            temp.getData().createChildren()                     #nodes = QUEUEING-FUNCTION(nodes, EXPAND(nod,problem.OPERATORS))
            for x in range(temp.getData().getChildCount()):
                for i in range(1, 9):#can change to arbitrary puzzle  ******THE MAIN CHANGE, CALCULATE H(N)**************
                    checkTile = np.where(Goal == i)
                    checkTile2 = np.where(temp.getData().getChild(x).getArray() == i)
                    if not (checkTile == checkTile2):
                        Hn+=1
                childPriority = priority+Hn
                dummy = PrioritizedItem(childPriority, temp.getData().getChild(x))
                isUnique = True
                for j in range(len(UniqueList)):
                    chkArray = (UniqueList[j].getData().getArray() == temp.getData().getChild(x).getArray()).all()
                    if(chkArray == True):
                        isUnique = False
                if(isUnique):
                    QueueingFunction.append(dummy)
                Hn = 0

def AStarManHatDist(StartingState, QueueingFunction, Goal): #majority same as previous
    failure = False
    #priority = 1                                                #this is essentially the f(n)
    StartNode = nodes(StartingState)        #
    StartNode.setParent(StartNode)
    QueueingFunction.append(PrioritizedItem(StartNode.Gn,StartNode))
    UniqueList = list(())
    UniqueList.append(PrioritizedItem(StartNode.Gn,StartNode))
    while not failure:                                          #loop do
        if len(QueueingFunction)==0:                            #if EMPTY(nodes) then return "failure"
            failure = True
            print("not a searchable state \n")
            return False      
        #print('. . .')                      
        index = 0
        #for C in range(len(QueueingFunction)):
        #    print(str(QueueingFunction[C].getPriority), end='')
        #print()
        for N in range(len(QueueingFunction)):
            if(int(QueueingFunction[N].getPriority())<int(QueueingFunction[index].getPriority())):
                #print("found a smaller value")
                index = N
        temp = QueueingFunction[index]                              #node = REMOVE-FRONT(nodes)
        #print("looking through node with: " + str(QueueingFunction[index].getPriority()) + " Priority")    
        QueueingFunction.pop(index)
        CheckingArray = (Goal == temp.getData().getArray()).all()     
        if(CheckingArray ==True):                               #if problem.GOAL-TEST(node.STATE) succeeds then return node
            print("found it")
            return temp.getData()
        else:
            #priority+=1
            Hntmp = 0                                         
            temp.getData().createChildren()                     #nodes = QUEUEING-FUNCTION(nodes, EXPAND(nod,problem.OPERATORS))
            for x in range(temp.getData().getChildCount()):
                for i in range(1,9):#can change to arbitrary puzzle  ******THE MAIN CHANGE, CALCULATE H(N)**************
                    checkTile = np.where(Goal == i)
                    checkTile2 = np.where(temp.getData().getChild(x).getArray() == i)
                    if not (checkTile == checkTile2):
                        tile1Row = checkTile[0][0] #would output as an array with a single element, get the value byt doing BlankRow[0]
                        #print(tile1Row)
                        tile1Column = checkTile[1][0]#find location of element
                        #print(tile1Column)
                        tile2Row = checkTile2[0][0] #would output as an array with a single element, get the value byt doing BlankRow[0]
                        #print(tile2Row)
                        tile2Column = checkTile2[1][0]#find location of element
                        #print(tile2Column)
                        row = abs(tile1Row - tile2Row)
                        column = abs(tile1Column - tile2Column)
                        Hntmp = Hntmp + row + column
                temp.getData().getChild(x).Hn = Hntmp
                childPriority = temp.getData().getChild(x).Gn + Hntmp
                print("creating child with: " + str(childPriority) + "priority, where Gn is: " + str(temp.getData().getChild(x).Gn) + " and Hn is " + str(temp.getData().getChild(x).Hn))
                dummy = PrioritizedItem(childPriority, temp.getData().getChild(x))
                isUnique = True
                for j in range(len(UniqueList)):
                    chkArray = (UniqueList[j].getData().getArray() == temp.getData().getChild(x).getArray()).all()
                    if(chkArray == True):
                        isUnique = False
                if(isUnique):
                    QueueingFunction.append(dummy)
                Hntmp = 0

startTime = time.time()
Q = list(())
#answer = AStarMisplacedTile(InitialState,Q,GoalState)
answer = AStarManHatDist(InitialState,Q,GoalState)
answer.printValue()
print()
while not((answer.getArray() == InitialState).all()):
    intermidiary = answer.getParent()
    intermidiary.printValue()
    print()
    answer = answer.getParent()
endTime = time.time()
resultsInSeconds = (endTime - startTime)
resultsInMinutes = ((endTime - startTime)/60)
print("This took: " + str(resultsInSeconds) + " Seconds to run")
print("This took: " + str(resultsInMinutes) + " minutes to run")

    

#       we now have a way to check if something is the goal state
#       we can use a priority queue as our queuing function since we are expanding the least cost anyway

#