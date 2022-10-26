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

#CheckingArray = (GoalState == InitialState).all()
#print (CheckingArray) these can be used to check if its the goal state


class nodes:
    def __init__(self,array) -> None:
        self.array = array
        #self.children = children
        #self.parents = parents
        pass

def AStar(StartingState, QueueingFunction):
    failure = False
    QueueingFunction = PriorityQueue(0)
    StartNode = nodes(StartingState)
    QueueingFunction.put((1,StartNode))
    while not failure:
        if QueueingFunction.empty():
            failure = True
        else:
            print('we made it through')
            failure = True

Q = PriorityQueue(0)
AStar(InitialState,Q)

    

#       we now have a way to check if something is the goal state
#       we can use a priority queue as our queuing function since we are expanding the least cost anyway

#