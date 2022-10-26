from gettext import npgettext
from queue import PriorityQueue
import numpy as np

print ('hello world')

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
#                 Initial [1,0,3]
#                         [4,2,5]
#                         [7,8,6]
InitialState = np.array([[1,0,3],[4,2,5],[7,8,6]]) #later on, make a function that'll randomize the initial state

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
    def __init__(self,array):
        self.array = array
        #self.children = children
        #self.parents = parents
        self.ChildCount = 0
        tmp = np.where(array == 0)
        self.BlankRow = tmp[0][0] #would output as an array with a single element, get the value byt doing BlankRow[0]
        self.BlankColumn = tmp[1][0]
        #find location of blank (0)

        
    def getValue(self):
        print(self.array)

        
    def createChildren(self):
        if (self.BlankRow)-1 >=0: #we can go up
            print("we can go up")
            self.ChildCount+=1
        if (self.BlankRow)+1 <=2: #we can go down
            print("we can go down")
            self.ChildCount+=1
        if (self.BlankColumn)-1 >=0: #we can go Left
            print("we can go Left")
            self.ChildCount+=1
        if (self.BlankColumn)+1 <=2: #we can go Right
            print("we can go Right")
            self.ChildCount+=1
        print("we can have " + str(self.ChildCount) + " children")

        

def AStar(StartingState, QueueingFunction, Goal): #function general-search(problem, QUEUEING-FUNCTION)
    failure = False
    priority = 1
    QueueingFunction = PriorityQueue(0)
    StartNode = nodes(StartingState)        #
    QueueingFunction.put((priority,StartNode))     #nodes = MAKE-QUEUE(MAKE_NODE(problem.INITIAL-STATE))
    while not failure:                      #loop do
        if QueueingFunction.empty():        #if EMPTY(nodes) then return "failure"
            failure = True
            print("not a searchable state \n")
            return False                            
        print('we made it through')     
        temp = QueueingFunction.get()       #node = REMOVE-FRONT(nodes)    temp[1].getValue() this is how we can print the values
        CheckingArray = (Goal == temp[1]).all()     
        if(CheckingArray ==True):           #if problem.GOAL-TEST(node.STATE) succeeds then return node
            return temp
        else:
            temp[1].createChildren()           #nodes = QUEUEING-FUNCTION(nodes, EXPAND(nod,problem.OPERATORS))
            


Q = PriorityQueue(0)
AStar(InitialState,Q,GoalState)

    

#       we now have a way to check if something is the goal state
#       we can use a priority queue as our queuing function since we are expanding the least cost anyway

#