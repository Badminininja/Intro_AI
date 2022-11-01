from typing import List
import numpy as np
import time

class PrioritizedItem:

    def __init__(self, priority, data) -> None:
        self.priority = priority
        self.data = data
        pass

    def getPriority(self):
        return self.priority

    def getData(self):
        return self.data
#   https://www.codingem.com/numpy-compare-arrays/#:~:text=The%20easiest%20way%20to%20compare,if%20the%20elements%20are%20True. help for comparing arrays
#   https://docs.python.org/3/library/queue.html The Queues

maxQueSize = 0
nodesExpanded = 0
GoalState = np.array([[1,2,3],[4,5,6],[7,8,0]])

#later on, make a function that'll randomize the initial state


class nodes:
    def __init__(self,Array):
        self.Array = Array
        self.Gn = 0 #depth
        self.Hn = 0 #estimated cost to goal
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
                self.ChildCount+=1   
    def getChild(self, number):
        return self.ChildList[number]
    def printChild(self, number):
        self.ChildList[number].printValue()

def UniformCS(StartingState, QueueingFunction, Goal): #function general-search(problem, QUEUEING-FUNCTION)
    failure = False
    global maxQueSize
    global nodesExpanded
    StartNode = nodes(StartingState)        #
    StartNode.setParent(StartNode)
    QueueingFunction.append(PrioritizedItem(StartNode.Gn,StartNode))
    UniqueList = list(())
    UniqueList.append(PrioritizedItem(StartNode.Gn,StartNode))
    while not failure:                                              #loop do
        if len(QueueingFunction)==0:                                #if EMPTY(nodes) then return "failure"
            failure = True
            print("not a searchable state \n")
            return False                            
        if len(QueueingFunction)>maxQueSize:
            maxQueSize = len(QueueingFunction)
        index = 0
        for N in range(len(QueueingFunction)):
            if(int(QueueingFunction[N].getPriority())<int(QueueingFunction[index].getPriority())):
                index = N
        temp = QueueingFunction[index]                              #node = REMOVE-FRONT(nodes)
        QueueingFunction.pop(index)
        CheckingArray = (Goal == temp.getData().getArray()).all()     
        if(CheckingArray ==True):                                   #if problem.GOAL-TEST(node.STATE) succeeds then return node
            return temp.getData()
        else:
            temp.getData().createChildren()                         #nodes = QUEUEING-FUNCTION(nodes, EXPAND(nod,problem.OPERATORS))
            for x in range(temp.getData().getChildCount()):
                dummy = PrioritizedItem(temp.getData().getChild(x).Gn, temp.getData().getChild(x))
                isUnique = True
                for j in range(len(UniqueList)):
                    chkArray = (UniqueList[j].getData().getArray() == temp.getData().getChild(x).getArray()).all()
                    if(chkArray == True):
                        isUnique = False
                if(isUnique):
                    nodesExpanded+=1
                    QueueingFunction.append(dummy)
                      
def AStarMisplacedTile(StartingState, QueueingFunction, Goal): #same as uniform but with new g(n)
    failure = False
    global maxQueSize
    global nodesExpanded
    StartNode = nodes(StartingState)        
    StartNode.setParent(StartNode)
    QueueingFunction.append(PrioritizedItem(StartNode.Gn,StartNode))
    UniqueList = list(())
    UniqueList.append(PrioritizedItem(StartNode.Gn,StartNode))
    while not failure:                                          #loop do
        if len(QueueingFunction)==0:                            #if EMPTY(nodes) then return "failure"
            failure = True
            print("not a searchable state \n")
            return False        
        if len(QueueingFunction)>maxQueSize:
            maxQueSize = len(QueueingFunction)               
        index = 0
        for N in range(len(QueueingFunction)):
            if(int(QueueingFunction[N].getPriority())<int(QueueingFunction[index].getPriority())):
                index = N
        temp = QueueingFunction[index]                              #node = REMOVE-FRONT(nodes)  
        QueueingFunction.pop(index)
        CheckingArray = (Goal == temp.getData().getArray()).all()     
        if(CheckingArray ==True):                               #if problem.GOAL-TEST(node.STATE) succeeds then return node
            return temp.getData()
        else:
            Hntmp = 0                                         
            temp.getData().createChildren()                     #nodes = QUEUEING-FUNCTION(nodes, EXPAND(nod,problem.OPERATORS))
            for x in range(temp.getData().getChildCount()):
                for i in range(1, 9):                           #can change to arbitrary puzzle  ******THE MAIN CHANGE, CALCULATE H(N)**************
                    checkTile = np.where(Goal == i)
                    checkTile2 = np.where(temp.getData().getChild(x).getArray() == i)
                    if not (checkTile == checkTile2):
                        Hntmp+=1
                temp.getData().getChild(x).Hn = Hntmp
                childPriority = temp.getData().getChild(x).Gn + Hntmp
                dummy = PrioritizedItem(childPriority, temp.getData().getChild(x))
                isUnique = True
                for j in range(len(UniqueList)):
                    chkArray = (UniqueList[j].getData().getArray() == temp.getData().getChild(x).getArray()).all()
                    if(chkArray == True):
                        isUnique = False
                if(isUnique):
                    nodesExpanded+=1
                    QueueingFunction.append(dummy)
                Hntmp = 0

def AStarManHatDist(StartingState, QueueingFunction, Goal): #majority same as previous
    failure = False
    global maxQueSize
    global nodesExpanded
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
        if len(QueueingFunction)>maxQueSize:
            maxQueSize = len(QueueingFunction)
                                  
        index = 0
        for N in range(len(QueueingFunction)):
            if(int(QueueingFunction[N].getPriority())<int(QueueingFunction[index].getPriority())):
                index = N
        temp = QueueingFunction[index]                              #node = REMOVE-FRONT(nodes)
        QueueingFunction.pop(index)
        CheckingArray = (Goal == temp.getData().getArray()).all()     
        if(CheckingArray ==True):                               #if problem.GOAL-TEST(node.STATE) succeeds then return node
            return temp.getData()
        else:
            Hntmp = 0                                         
            temp.getData().createChildren()                     #nodes = QUEUEING-FUNCTION(nodes, EXPAND(nod,problem.OPERATORS))
            for x in range(temp.getData().getChildCount()):
                for i in range(1,9):    
                    checkTile = np.where(Goal == i)
                    checkTile2 = np.where(temp.getData().getChild(x).getArray() == i)
                    if not (checkTile == checkTile2):
                        tile1Row = checkTile[0][0] 
                        tile1Column = checkTile[1][0]
                        tile2Row = checkTile2[0][0]
                        tile2Column = checkTile2[1][0]
                        row = abs(tile1Row - tile2Row)
                        column = abs(tile1Column - tile2Column)
                        Hntmp = Hntmp + row + column
                temp.getData().getChild(x).Hn = Hntmp
                childPriority = temp.getData().getChild(x).Gn + Hntmp
                dummy = PrioritizedItem(childPriority, temp.getData().getChild(x))
                isUnique = True
                for j in range(len(UniqueList)):
                    chkArray = (UniqueList[j].getData().getArray() == temp.getData().getChild(x).getArray()).all()
                    if(chkArray == True):
                        isUnique = False
                if(isUnique):
                    nodesExpanded+=1
                    QueueingFunction.append(dummy)
                Hntmp = 0

startTime = time.time()
depth = 0
Q = list(())
menu = input("Welcome to Joseph's 8-puzzle solver. Type '1' for a hard-coded puzzle, or '2' to create you're own\n") #this looks similar to the example shown on the project example for simplicity and clarity
if(menu == '1'):
    InitialState1 = np.array([[1,2,3],[4,5,6],[0,7,8]]) #Depth 2
    print("Problem 1: depth 2")
    print(InitialState1)
    InitialState2 = np.array([[1,2,3],[5,0,6],[4,7,8]]) #Depth 4
    print("Problem 2: depth 4")
    print(InitialState2)
    InitialState3 = np.array([[1,3,6],[5,0,2],[4,7,8]]) #Depth 8
    print("Problem 3: depth 8")
    print(InitialState3)
    InitialState4 = np.array([[1,3,6],[5,0,7],[4,8,2]]) #Depth 12
    print("Problem 4: depth 12")
    print(InitialState4)
    InitialState5 = np.array([[1,6,7],[5,0,3],[4,8,2]]) #Depth 16
    print("Problem 5: depth 16")
    print(InitialState5)
    InitialState6 = np.array([[7,1,2],[4,8,5],[6,3,0]]) #Depth 20
    print("Problem 6: depth 20")
    print(InitialState6)
    InitialState7 = np.array([[0,7,2],[4,6,1],[3,5,8]]) #Depth 24
    print("Problem 7: depth 24")
    print(InitialState7)
    codedP = input("These are EK's hard coded examples, please type the problem number for which one you'd like to run. Not the depth\n")
    match codedP:
        case '1':
            InitialState = InitialState1
        case '2':
            InitialState = InitialState2
        case '3':
            InitialState = InitialState3
        case '4':
            InitialState = InitialState4
        case '5':
            InitialState = InitialState5
        case '6':
            InitialState = InitialState6
        case '7':
            InitialState = InitialState7
elif(menu == '2'):
    print("type the puzzle")
answer = AStarMisplacedTile(InitialState,Q,GoalState)
depth = answer.Gn
outputList = list(())
outputList.append(answer)
print()
while not((answer.getArray() == InitialState).all()):
    intermidiary = answer.getParent()
    outputList.append(intermidiary)
    answer = answer.getParent()

for i in reversed(outputList):
    print("The best state to expand with a g(n) = " + str(i.Gn) + " and h(n) = " + str(i.Hn) + " is?")
    i.printValue()
    print()
print("Goal state!")
print("Solution depth was: " + str(depth))
print("Number of nodes expanded: " + str(nodesExpanded))
print("Max Queue size: " + str(maxQueSize))