# Imports
import argparse
import sys

#global constants
HEURISTIC = 1

#global variable
pathNotFound = True

class Node:
    
    def __init__(self,p,y,x,g,goalNode):
        self.parent = p
        self.xPos = x
        self.yPos = y
        self.g_cost = g
        self.h_cost = self.calcH(goalNode)
        self.f_cost = 32767

    def __eq__(self,toCheck):
        try:
            return ((self.xPos == toCheck.xPos) and (self.yPos == toCheck.yPos))
        except AttributeError:
            try:
                self.xPos
                return False
            except AttributeError:
                try:
                    toCheck.xPos
                    return False
                except AttributeError:
                    return True
        

    def __lt__(self,toCheck):
        return (self.f_cost < toCheck.f_cost)

    def __le__(self,toCheck):
        return (self.f_cost <= toCheck.f_cost)

    def __ne__(self,toCheck):
        return not (self == toCheck)

    def __gt__(self,toCheck):
        return (self.f_cost > toCheck.f_cost)

    def __ge__(self,toCheck):
        return (self.f_cost >= toCheck.f_cost)

    def calcH(self,goalNode):
        if (goalNode == None):
            return 0
        else:

            vertDif = abs(goalNode.yPos - self.yPos)
            horizDif = abs(goalNode.xPos - self.xPos)

            # Heuristic 1: 0
            if(HEURISTIC == 1):
                return 0
            # Heuristic 2: Min(vertical, horizontal)
            elif(HEURISTIC == 2):
                return min(vertDif, horizDif)
            # Heuristic 3: Max(vertical, horizontal)
            elif(HEURISTIC == 3):
                return max(vertDif, horizDif)
            # Heuristic 4: vertical + horizontal
            elif(HEURISTIC == 4):
                return (vertDif + horizDif)
            # Heuristic 5: vertical + horizontal + turns required
            elif(HEURISTIC == 5):
                return (vertDif + horizDif + self.calcTurns(self.calcDir(), goalNode))
            # Heuristic 6: Heuristic 5 * 3
            elif(HEURISTIC == 6):
                return ((vertDif + horizDif + self.calcTurns(self.calcDir(), goalNode))*3)
            else:
                print("Error in calcH: Heuristic outside of [1,6]")
                return -1

    #returns a list of the valid neighbors of this node
    #assumes this node has valid x and y positions
    def getNeighbors(self,boardArray,goal):
        neighbors = []

        if (args.debug):
            print("\nSelf: (",self.yPos,",",self.xPos,").")
        #neighbor south
        neighborX = self.xPos
        neighborY = self.yPos + 1
        if(neighborY < len(boardArray)):
            if(boardArray[neighborY][neighborX] != '#'):
                #The neighbor is valid, so add it to the list
                neighbors.append(Node(self,neighborY,neighborX,32767,goal))

                if (args.debug):
                    print ("South neighbor made at (", neighborY,",",neighborX,"). Terrain cost is",boardArray[neighborY][neighborX],".")
        #neighbor north
        neighborX = self.xPos
        neighborY = self.yPos - 1
        if(neighborY >= 0):
            if(boardArray[neighborY][neighborX] != '#'):
                #The neighbor is valid, so add it to the list
                neighbors.append(Node(self,neighborY,neighborX,32767,goal))
                if (args.debug):
                    print ("North neighbor made at (", neighborY,",",neighborX,"). Terrain cost is",boardArray[neighborY][neighborX],".")
        #neighbor west
        neighborX = self.xPos - 1
        neighborY = self.yPos
        if(neighborX >= 0):
            if (boardArray[neighborY][neighborX] != '#'):
                #The neighbor is valid, so add it to the list
                neighbors.append(Node(self,neighborY,neighborX,32767,goal))
                if (args.debug):
                    print ("West neighbor made at (", neighborY,",",neighborX,"). Terrain cost is",boardArray[neighborY][neighborX],".")
        #neighbor east
        neighborX = self.xPos + 1
        neighborY = self.yPos
        if(neighborX < len(boardArray[neighborY])):
            if(boardArray[neighborY][neighborX] != '#'):
                #The neighbor is valid, so add it to the list
                neighbors.append(Node(self,neighborY,neighborX,32767,goal))
                if (args.debug):
                    print ("East neighbor made at (", neighborY,",",neighborX,"). Terrain cost is",boardArray[neighborY][neighborX],".")
        #leap north
        neighborX = self.xPos
        neighborY = self.yPos - 3
        if(neighborY >= 0):
            if(boardArray[neighborY][neighborX] != '#'):
                #The neighbor is valid, so add it to the list
                neighbors.append(Node(self,neighborY,neighborX,32767,goal))
                if (args.debug):
                    print ("Leap North neighbor made at (", neighborY,",",neighborX,"). Terrain cost is",boardArray[neighborY][neighborX],".")
        #leap south
        neighborX = self.xPos
        neighborY = self.yPos + 3
        if(neighborY < len(boardArray)):
            if(boardArray[neighborY][neighborX] != '#'):
                #The neighbor is valid, so add it to the list
                neighbors.append(Node(self,neighborY,neighborX,32767,goal))
                if (args.debug):
                    print ("Leap South neighbor made at (", neighborY,",",neighborX,"). Terrain cost is",boardArray[neighborY][neighborX],".")
        #leap west
        neighborX = self.xPos - 3
        neighborY = self.yPos
        if(neighborX >= 0):
            if(boardArray[neighborY][neighborX] != '#'):
                #The neighbor is valid, so add it to the list
                neighbors.append(Node(self,neighborY,neighborX,32767,goal))
                if (args.debug):
                    print ("Leap West neighbor made at (", neighborY,",",neighborX,"). Terrain cost is",boardArray[neighborY][neighborX],".")
        #leap right
        neighborX = self.xPos + 3
        neighborY = self.yPos
        if(neighborX < len(boardArray[neighborY])):
            if(boardArray[neighborY][neighborX] != '#'):
                #The neighbor is valid, so add it to the list
                neighbors.append(Node(self,neighborY,neighborX,32767,goal))
                if (args.debug):
                    print ("Leap East neighbor made at (", neighborY,",",neighborX,"). Terrain cost is",boardArray[neighborY][neighborX],".")

        return neighbors

    def calcDir(self):

        # Next determine the ending direction.
        # If the parent of this node's parent is None, then it's the start. Starting direction is north.
        if (self.parent == None):
            direction = 1
        # If the node has a smaller y-value that its parent, then the direction is north.
        elif (self.yPos < self.parent.yPos):
            direction = 1
        # If the node has a larger x-value that its parent, then the direction is east.
        elif (self.xPos > self.parent.xPos):
            direction = 2
        # If the node has a larger y-value that its parent, then the direction is south.
        elif (self.yPos > self.parent.yPos):
            direction = 3
        # If the node has a smaller x-value that its parent, then the direction is west.
        elif (self.xPos < self.parent.xPos):
            direction = 4
        return direction

        
    def turnCost(self):

        # If the parent of this node's parent is None, then it's the start. Starting direction is north.
        if (self.parent == None):
            startDir = 1
        else:   
            # Runs calcDir() to find the starting direction and ending direction.
            startDir = self.parent.calcDir()
        endDir = self.calcDir()

        # Calculates the cost of a turn based on the directions provided.
        # If they're the same direction, there's no turn cost.
        turn = abs(startDir - endDir)

        # The directions were the same, no turn.
        if (turn == 0):
            return 0
        # The directions resulted in a 90 degree turn.
        elif (turn % 2 == 1):
            return arr[self.parent.yPos][self.parent.xPos] / 3
        else:
            return 2 * arr[self.parent.yPos][self.parent.xPos] / 3

    def calcTurns(self, dirFacing, goalNode):

        # First, fill an array with the 1-2 directions the robot
        # needs to head towards in order to reach the goal
        dirToGoal = []
        # If the node has a smaller y-value than the goal, one of the directions to face is South
        if (self.yPos < goalNode.yPos):
            dirToGoal.append(3)
        # If the node has a greater y-value than the goal, one of the directions to face is North
        if (self.yPos > goalNode.yPos):
            dirToGoal.append(1)
        # If the node has a smaller x-value than the goal, one of the directions to face is East
        if (self.xPos < goalNode.xPos):
            dirToGoal.append(2)
        # If the node has a greater x-value than the goal, one of the directions to face is West
        if (self.xPos > goalNode.xPos):
            dirToGoal.append(4)

        # Fill an array with the difference in facing-direction and desired-directions
        dirDif = [abs(dirFacing-item) for item in dirToGoal]

        # If 3, change to 1 because it means it's going from West to North or vice versa
        for idx,item in enumerate(dirDif):
            if item == 3:
                item = 1
                dirDif[idx] = item
            if (args.debug):
                print(dirDif)
     
        # Return minimum number of turns needed to arrive at the goal
        if dirDif:
            if (args.debug):
                print(max(dirDif)/3)
            return (max(dirDif)/3)
        return 0

    def calcG(self):

        if (args.debug):
            print ("Now calculating the g cost for the node at (",self.yPos,",",self.xPos,"), which has a terrain cost of ",arr[self.yPos][self.xPos],".")

        # Store the difference bettwen the vertical and horizontal positions.
        vert = abs(self.parent.yPos - self.yPos)
        hor = abs(self.parent.xPos - self.xPos)
        
        # Calculate the turn cost and store it.
        cost = self.parent.turnCost();

        # Store g as a large number, in case of invalid nodes.
        g = 10000

        # If the move is a leap, calculate with that in mind. 20 for leap + turn cost + parent's g cost.
        if(vert >= 3 or hor >= 3):
            g = (self.parent.g_cost + 20 + cost)
        
        # If the move is normal, calculate the normal g cost. Terrain cost + turn cost + parent's g cost.
        g = arr[self.yPos][self.xPos] + self.parent.g_cost + cost

        if (args.debug):
            print ("The g_cost of Node (",self.yPos,",",self.xPos,") is",g,"time.")
        
        # Set this node's g_cost to the newly calcualted g.
        self.g_cost = g
        return g
#----------------------------------------------------------------------------
def createPath(currentNode):
    path = []
    while(currentNode.parent != None):
        path.append(currentNode)
        currentNode = currentNode.parent
    path.append(startNode)
    path.reverse()
    return path
#----------------------------------------------------------------------------
def printResults(path):

    # Note that print path was reached.
    if (args.debug):
        print ("\nCreating the path now.")

    # First, print the score of the path.
    print ("\nScore:",500 - path[len(path) - 1].g_cost)

    # Next, determine the number of actions taken.
    actionNum = 0
    actionList = []

    for i in range(0, len(path) - 1):

        # Just a forward move. Add forward to the actionList.
        if (path[i].calcDir() == 1):
            if (path[i + 1].calcDir() == 1):
                actionNum += 1
            elif (path[i + 1].calcDir() == 2):
                actionList.append("Turn Right")
                actionNum += 2
            elif (path[i + 1].calcDir() == 4):
                actionList.append("Turn Left")
                actionNum += 2
            elif (path[i + 1].calcDir() == 3):
                actionList.append("Turn Right")
                actionList.append("Turn Right")
                actionNum += 3
        elif (path[i].calcDir() == 2):
            if (path[i + 1].calcDir() == 2):
                actionNum += 1
            elif (path[i + 1].calcDir() == 3):
                actionList.append("Turn Right")
                actionNum += 2
            elif (path[i + 1].calcDir() == 1):
                actionList.append("Turn Left")
                actionNum += 2
            elif (path[i + 1].calcDir() == 4):
                actionList.append("Turn Right")
                actionList.append("Turn Right")
                actionNum += 3
        elif (path[i].calcDir() == 3):
            if (path[i + 1].calcDir() == 3):
                actionNum += 1
            elif (path[i + 1].calcDir() == 4):
                actionList.append("Turn Right")
                actionNum += 2
            elif (path[i + 1].calcDir() == 2):
                actionList.append("Turn Left")
                actionNum += 2
            elif (path[i + 1].calcDir() == 1):
                actionList.append("Turn Right")
                actionList.append("Turn Right")
                actionNum += 3
        elif (path[i].calcDir() == 4):
            if (path[i + 1].calcDir() == 4):
                actionNum += 1
            elif (path[i + 1].calcDir() == 1):
                actionList.append("Turn Right")
                actionNum += 2
            elif (path[i + 1].calcDir() == 3):
                actionList.append("Turn Left")
                actionNum += 2
            elif (path[i + 1].calcDir() == 2):
                actionList.append("Turn Right")
                actionList.append("Turn Right")
                actionNum += 3

        if (abs(path[i].yPos - path[i + 1].yPos) == 3 or abs(path[i].xPos - path[i + 1].xPos) == 3):
            actionList.append("Leap Forward")
        else:
          actionList.append("Forward")

    print ("Number of Actions:",actionNum)



    # Third, print the number of nodes expanded. (Nodes in the closed list)
    print("Nodes Expanded:",len(closedList))

    # Then, print the estimated branching factor.
    print("Estimated Branching Factor:")

    # Finally, print the series of actions.
    for i in range(0,len(actionList)):
        print (actionList[i])

    while(path):
        print("yPos:",path[0].yPos,"xPos:",path[0].xPos)
        path.pop(0)
#----------------------------------------------------------------------------
# Create the argument parser.
parser = argparse.ArgumentParser(description="Read in a map and run A* on it.")

# Add arguments to the parser.
parser.add_argument("--debug", "-d", help="Print the debug version of the program.", action="store_true")
parser.add_argument("map", help="Path to the map file.")
parser.add_argument("heuristic", help="Which heuristic to use.", type = int, choices = [1,2,3,4,5,6])

# Parses the arguments.
args = parser.parse_args()

# Set the huristic to use
HEURISTIC = args.heuristic

# Note whether the program is in debug mode or not.
if (args.debug):
    print ("\nPrinting in debug mode.\n")

# Open the file.
with open(args.map, 'r') as f:
    arr = [line.strip('\n').split('\t') for line in f]

#DONT FORGET: arrays are -> arr[y][x]
for i in range(0,len(arr)):
    for j in range(0,len(arr[i])):
        if (arr[i][j] == 'S'):
            startNode = Node(None,i,j,0,None)
            arr[i][j] = 1
        elif (arr[i][j] == 'G'):
            goalNode = Node(None,i,j,0,None)
            arr[i][j] = 1
        else:
            if (arr[i][j] != "#"):
                arr[i][j] = int(arr[i][j])
if (args.debug):
    for i in range(0, len(arr)):
        print (arr[i])
#----------------------------------------------------------------------------
#init the open list
openList = [startNode]
closedList = []

while (len(openList) != 0):

    if (args.debug):
        print("\nThe openList contains:")
        for i in range(0,len(openList)):
            print("Node (",openList[i].yPos,",",openList[i].xPos,")")

    #get the lowest cost node (last in list)
    toExpand = openList.pop(0)

    if (args.debug):
        print("\nThe node toExpand is now Node (",toExpand.yPos,",",toExpand.xPos,").")

    if (toExpand == goalNode):

        if (args.debug):
            print ("The node toExpand is the goalNode!")
        pathNotFound = False
        path = createPath(toExpand)
        printResults(path)
        break
    neighbors = toExpand.getNeighbors(arr,goalNode)

    for k in range(0,len(neighbors)):
        neighbors[k].calcG()
        f_cost = neighbors[k].g_cost + neighbors[k].h_cost

        if (neighbors[k] in openList):
            prev = openList.index(neighbors[k])
            if (neighbors[k].f_cost < openList[prev].f_cost):
                openList[prev] = neighbors[k]
        elif (neighbors[k] in closedList):
            prev = closedList.index(neighbors[k])
            if (neighbors[k].f_cost < closedList[prev].f_cost):
                closedList[prev] = neighbors[k]
        else:
            openList.append(neighbors[k])
            openList.sort()

            if (args.debug):
                print("Adding Node at (",neighbors[k].yPos,",",neighbors[k].xPos,") to the openList.")

    closedList.append(toExpand)

if (pathNotFound):
    print("\nPath not found!")
