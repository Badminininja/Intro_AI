import numpy as np
class PrioritizedItem: #made a simple class for tuples where the first element is the cost and the second is the node

    def __init__(self, priority, data) -> None:
        self.priority = priority
        self.data = data
        pass

    def getPriority(self):
        return self.priority

    def getData(self):
        return self.data

maxQueSize = 0
nodesExpanded = 0
GoalState = np.array([[1,2,3],[4,5,6],[7,8,0]])

class nodes:                            #class where I can have my state's contain their own individual information
    def __init__(self,Array):
        self.Array = Array
        self.Gn = 0                     #essentially the depth in this scenerio
        self.Hn = 0                     #estimated cost to goal, The heuristic cost
        self.ChildList=list(())         #list to hold the children
        self.ChildCount = 0             #Basic record of the amount of children
        tmp = np.where(Array == 0)      #find location of blank (0)
        self.BlankRow = tmp[0][0]       #and record it's row 
        self.BlankColumn = tmp[1][0]    #and record it's column
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
    def createChildren(self): #create new children arrays
        if (self.BlankRow)-1 >=0: #we can go up
            temporary = np.copy(self.Array)                             # Normal equals doesn't work, it just a pass by reference
            number = temporary[self.BlankRow-1][self.BlankColumn]       #switching the element we want the blank to move to with each other
            temporary[self.BlankRow-1][self.BlankColumn] = 0
            temporary[self.BlankRow][self.BlankColumn] = number
            checkParent = (temporary == self.parent.getArray()).all()   #check that the movement doesn't create a copy of its parent 
            if not checkParent:                                         #(make sure it doesn't just go up and down repeatedly forever)
                tmp = nodes(temporary)              #turn the array into a node object so it follows suit
                tmp.setParent(self)                 #set the parent
                tmp.Gn = self.Gn + 1                #increment the depth
                self.ChildList.append(tmp)          #append the child to the child list
                self.ChildCount+=1                  #increment the child count as we have created a new child

        if (self.BlankRow)+1 <=2: #we can go down, Same logic as previous but for different movement
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
            
        if (self.BlankColumn)-1 >=0: #we can go Left, Same logic as previous but for different movement
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
            
        if (self.BlankColumn)+1 <=2: #we can go Right, Same logic as previous but for different movement
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
    failure = False                                                 #this isn't that useful, but it makes sure that the loop won't continue if we ever find that it's not a valid puzzle
    global maxQueSize                                               
    global nodesExpanded                                            
    StartNode = nodes(StartingState)                                #create the first node
    StartNode.setParent(StartNode)
    QueueingFunction.append(PrioritizedItem(StartNode.Gn,StartNode))#append the first node to start the queueing function
    UniqueList = list(())                                           #create a list to record unique states so that we don't repeat any states
    UniqueList.append(PrioritizedItem(StartNode.Gn,StartNode))
    while not failure:                                              #loop do
        if len(QueueingFunction)==0:                                #if EMPTY(nodes) then return "failure"
            failure = True
            print("not a searchable state \n")
            return False                            
        if len(QueueingFunction)>maxQueSize:                        #if the max queue size got bigger, record it
            maxQueSize = len(QueueingFunction)
        index = 0
        for N in range(len(QueueingFunction)):                      #choosing the node with the lowest cost/priority
            if(int(QueueingFunction[N].getPriority())<int(QueueingFunction[index].getPriority())):
                index = N
        temp = QueueingFunction[index]                              #node = REMOVE-FRONT(nodes)
        QueueingFunction.pop(index)
        CheckingArray = (Goal == temp.getData().getArray()).all()     
        if(CheckingArray ==True):                                   #if problem.GOAL-TEST(node.STATE) succeeds then return node
            return temp.getData()
        else:
            temp.getData().createChildren()                         #nodes = QUEUEING-FUNCTION(nodes, EXPAND(nod,problem.OPERATORS))
            for x in range(temp.getData().getChildCount()):         #loop through the children list of the node
                dummy = PrioritizedItem(temp.getData().getChild(x).Gn, temp.getData().getChild(x))
                isUnique = True
                for j in range(len(UniqueList)):                    #make sure the new children nodes are not repeated states
                    chkArray = (UniqueList[j].getData().getArray() == temp.getData().getChild(x).getArray()).all()
                    if(chkArray == True):
                        isUnique = False
                if(isUnique):                                       #
                    nodesExpanded+=1                                #if they are unique, increment nodesExpanded
                    QueueingFunction.append(dummy)                  #add the child node to the queue and repeat the loop
                      
def AStarMisplacedTile(StartingState, QueueingFunction, Goal): #same as uniform but with new g(n)
    failure = False
    global maxQueSize
    global nodesExpanded
    StartNode = nodes(StartingState)        
    StartNode.setParent(StartNode)
    QueueingFunction.append(PrioritizedItem(StartNode.Gn,StartNode))
    UniqueList = list(())
    UniqueList.append(PrioritizedItem(StartNode.Gn,StartNode))
    while not failure:                                          
        if len(QueueingFunction)==0:                            
            failure = True
            print("not a searchable state \n")
            return False        
        if len(QueueingFunction)>maxQueSize:
            maxQueSize = len(QueueingFunction)               
        index = 0
        for N in range(len(QueueingFunction)):
            if(int(QueueingFunction[N].getPriority())<int(QueueingFunction[index].getPriority())):
                index = N
        temp = QueueingFunction[index]                                
        QueueingFunction.pop(index)
        CheckingArray = (Goal == temp.getData().getArray()).all()     
        if(CheckingArray ==True):                               
            return temp.getData()
        else:
            Hntmp = 0                                           #set h(n) to 0 
            temp.getData().createChildren()                     
            for x in range(temp.getData().getChildCount()):
                for i in range(1, 9):                           #can change to arbitrary puzzle  ******THE MAIN CHANGE, CALCULATE H(N)**************
                    checkTile = np.where(Goal == i)                                     #loop through all the numbers and find where that number is for the goal
                    checkTile2 = np.where(temp.getData().getChild(x).getArray() == i)   #and for the new child being created
                    if not (checkTile == checkTile2):                                   #if its a misplaced tile
                        Hntmp+=1                                                        #   increment the h(n) and loop through the rest of the numbers
                temp.getData().getChild(x).Hn = Hntmp
                childPriority = temp.getData().getChild(x).Gn + Hntmp                   #add the g(n)/depth to the h(n) as a single number priority/cost
                dummy = PrioritizedItem(childPriority, temp.getData().getChild(x))      #create a tuple for the queue with that cost and child
                isUnique = True
                for j in range(len(UniqueList)):
                    chkArray = (UniqueList[j].getData().getArray() == temp.getData().getChild(x).getArray()).all()
                    if(chkArray == True):
                        isUnique = False
                if(isUnique):
                    nodesExpanded+=1
                    QueueingFunction.append(dummy)
                Hntmp = 0                                       #reset h(n) to 0 for next possible child

def AStarManHatDist(StartingState, QueueingFunction, Goal): #same as misplaced but with more calculation on g(n)
    failure = False
    global maxQueSize
    global nodesExpanded
    StartNode = nodes(StartingState)        
    StartNode.setParent(StartNode)
    QueueingFunction.append(PrioritizedItem(StartNode.Gn,StartNode))
    UniqueList = list(())
    UniqueList.append(PrioritizedItem(StartNode.Gn,StartNode))
    while not failure:                                          
        if len(QueueingFunction)==0:                            
            failure = True
            print("not a searchable state \n")
            return False
        if len(QueueingFunction)>maxQueSize:
            maxQueSize = len(QueueingFunction)
                                  
        index = 0
        for N in range(len(QueueingFunction)):
            if(int(QueueingFunction[N].getPriority())<int(QueueingFunction[index].getPriority())):
                index = N
        temp = QueueingFunction[index]                              
        QueueingFunction.pop(index)
        CheckingArray = (Goal == temp.getData().getArray()).all()     
        if(CheckingArray ==True):                               
            return temp.getData()
        else:
            Hntmp = 0                                         
            temp.getData().createChildren()                     
            for x in range(temp.getData().getChildCount()):
                for i in range(1,9):    
                    checkTile = np.where(Goal == i)
                    checkTile2 = np.where(temp.getData().getChild(x).getArray() == i)
                    if not (checkTile == checkTile2):                               #*****THE CHANGE FROM MISPLACED TILES*****
                        tile1Row = checkTile[0][0]                                  #instead of simply incrementing the h(n) cost for each misplaced tile
                        tile1Column = checkTile[1][0]                               #I find the exact row and column of that number for both the goal state
                        tile2Row = checkTile2[0][0]                                 #and the new child state
                        tile2Column = checkTile2[1][0]
                        row = abs(tile1Row - tile2Row)                              #find how far that element needs to travel to get to the element in the goal state
                        column = abs(tile1Column - tile2Column)
                        Hntmp = Hntmp + row + column                                #then add those totals to the h(n) and repeat for all the other elements in the puzzle
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
    print("Enter your puzzle where the 0 is considered the blank space and delimit your numbers with a comma only. Use only valid 8-puzzles otherwise it will take a while to go through the entire search space")
    createdArray1 = input("enter the first row: ")
    first = int(createdArray1[0])
    second = int(createdArray1[2])
    third = int(createdArray1[4])
    createdArray2 = input("enter the second row: ")
    fourth = int(createdArray2[0])
    fifth = int(createdArray2[2])
    sixth = int(createdArray2[4])
    createdArray3 = input("enter the third row: ")
    seventh = int(createdArray3[0])
    eighth = int(createdArray3[2])
    ninth = int(createdArray3[4])
    InitialState = np.array([[first,second,third],[fourth,fifth,sixth],[seventh,eighth,ninth]])

algo = input("Now please enter the number for the algorithm you want to use to solve it with. Uniform Cost Search with (1), A* with Misplaced Tile Heuristic with (2), or A* with Manhattan Distance Heuristic with (3)\n")
match algo:
    case '1':
        answer = UniformCS(InitialState,Q,GoalState)
    case '2':
        answer = AStarMisplacedTile(InitialState, Q, GoalState)
    case '3':
        answer = AStarManHatDist(InitialState,Q,GoalState)
    case _:
        print("ERROR, not one of the given algorithms. Exiting. . .")
        quit()
depth = answer.Gn
outputList = list(())
outputList.append(answer)
print()
while not((answer.getArray() == InitialState).all()):   #create an output list and append the outputs to it
    intermidiary = answer.getParent()                   #we can trace the route of the algorithm by going backwards
    outputList.append(intermidiary)                     #and looking through the parents of the nodes until we hit the initial state
    answer = answer.getParent()

for i in reversed(outputList):                          #output the list in reverse to see the list in proper order from top to bottom
    print("The best state to expand with a g(n) = " + str(i.Gn) + " and h(n) = " + str(i.Hn) + " is?")
    i.printValue()
    print()
print("Goal state!")
print("Solution depth was: " + str(depth))
print("Number of nodes expanded: " + str(nodesExpanded))
print("Max Queue size: " + str(maxQueSize))