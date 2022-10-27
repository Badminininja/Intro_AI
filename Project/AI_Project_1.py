from gettext import npgettext
#from multiprocessing import dummy
from queue import PriorityQueue
import heapq
from tabnanny import check
from typing import List
from xml.dom.minidom import Childless
import numpy as np
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
#InitialState = np.array([[1,2,3],[0,5,6],[4,7,8]])
InitialState = np.array([[1,2,3],[4,0,5],[7,8,6]]) #later on, make a function that'll randomize the initial state



#{x = np.where(InitialState == 0)       # random work to find out where the 0 is in the state
#print(x)
#row = x[0]
#column = x[1]

#print(InitialState[row[0]][column[0]])
#actualRow = x[0][0]
#print(actualRow)
#actualColoumn = x[1][0]
#print(actualColoumn)
#print(InitialState[actualRow][actualColoumn])
#CheckingArray = (GoalState == InitialState).all()
#print (CheckingArray) these can be used to check if its the goal state
#       Failed numpy array is differnet from normal array
#for row in InitialState:
#    for element in row:
#        if(element == 0):
#            BlankRow = row
#            BlankColoumn = element
#print(InitialState.index(BlankRow))
#print(BlankRow.index(0))}

class nodes:
    def __init__(self,Array):
        self.Array = Array
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

        

def AStar(StartingState, QueueingFunction, Goal): #function general-search(problem, QUEUEING-FUNCTION)
    failure = False
    priority = 1 #this is essentially the f(n)
    #QueueingFunction = PriorityQueue(0)
    StartNode = nodes(StartingState)        #
    StartNode.setParent(StartNode)
    QueueingFunction.append(PrioritizedItem(priority,StartNode))
    #np.append(QueueingFunction, PrioritizedItem(priority,StartNode), axis=0)     #nodes = MAKE-QUEUE(MAKE_NODE(problem.INITIAL-STATE))
    while not failure:                      #loop do
        if len(QueueingFunction)==0:        #if EMPTY(nodes) then return "failure"
            failure = True
            print("not a searchable state \n")
            return False                            
        #print('we made it through')
        #print(QueueingFunction)

        index = 0
        for N in range(len(QueueingFunction)):
            if(QueueingFunction[N].getPriority()<index):
                index = N


        temp = QueueingFunction[N]       #node = REMOVE-FRONT(nodes)    temp[1].printValue() this is how we can print the values
        QueueingFunction.pop(N)
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
                QueueingFunction.append(dummy)
                #np.append(QueueingFunction,dummy)
                #QueueingFunction.put((priority,dummy))
                #QueueingFunction.task_done
                #print(QueueingFunction.queue)
            


#Q = PriorityQueue(0)
#Q = np.array([])
Q = list(())
answer = AStar(InitialState,Q,GoalState)
answer.printValue()
print()
while not((answer.getArray() == InitialState).all()):
    intermidiary = answer.getParent()
    intermidiary.printValue()
    print()
    answer = answer.getParent()


    

#       we now have a way to check if something is the goal state
#       we can use a priority queue as our queuing function since we are expanding the least cost anyway

#