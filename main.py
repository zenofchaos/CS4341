# Imports
import argparse
import sys

#global constants
HEURISTIC = 1

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
        return (self.f_cost != toCheck.f_cost)

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
                return (vertDif + horizDif + calcTurns(calcDir(), goalNode))
            # Heuristic 6: Heuristic 5 * 3
            elif(HEURISTIC == 6):
                return ((vertDif + horizDif + calcTurns(calcDir(), goalNode))*3)
            else:
                print("Error in calcH: Heuristic outside of [1,6]")
                return -1

    #returns a list of the valid neighbors of this node
    #assumes this node has valid x and y positions
    def getNeighbors(self,boardArray,goal):
        neighbors = []

        print("Self: ",self.xPos,self.yPos)
        #neighbor south
        neighborX = self.xPos
        neighborY = self.yPos + 1
        if(neighborY < len(boardArray)):
            if(boardArray[neighborY][neighborX] != '#'):
                #The neighbor is valid, so add it to the list
                neighbors.append(Node(self,neighborX,neighborY,32767,goal))
        #neighbor north
        neighborX = self.xPos
        neighborY = self.yPos - 1
        if(neighborY >= 0):
            if(boardArray[neighborY][neighborX] != '#'):
                #The neighbor is valid, so add it to the list
                neighbors.append(Node(self,neighborX,neighborY,32767,goal))
        #neighbor west
        neighborX = self.xPos - 1
        neighborY = self.yPos
        if(neighborX >= 0):
            if (boardArray[neighborY][neighborX] != '#'):
                #The neighbor is valid, so add it to the list
                neighbors.append(Node(self,neighborX,neighborY,32767,goal))
        #neighbor east
        neighborX = self.xPos + 1
        neighborY = self.yPos
        if(neighborX < len(boardArray[neighborY])):
            if(boardArray[neighborY][neighborX] != '#'):
                #The neighbor is valid, so add it to the list
                neighbors.append(Node(self,neighborX,neighborY,32767,goal))
        #leap north
        neighborX = self.xPos
        neighborY = self.yPos - 3
        if(neighborY >= 0):
            if(boardArray[neighborY][neighborX] != '#'):
                #The neighbor is valid, so add it to the list
                neighbors.append(Node(self,neighborX,neighborY,32767,goal))
        #leap south
        neighborX = self.xPos
        neighborY = self.yPos + 3
        if(neighborY < len(boardArray)):
            if(boardArray[neighborY][neighborX] != '#'):
                #The neighbor is valid, so add it to the list
                neighbors.append(Node(self,neighborX,neighborY,32767,goal))
        #leap west
        neighborX = self.xPos - 3
        neighborY = self.yPos
        if(neighborX >= 0):
            if(boardArray[neighborY][neighborX] != '#'):
                #The neighbor is valid, so add it to the list
                neighbors.append(Node(self,neighborX,neighborY,32767,goal))
        #leap right
        neighborX = self.xPos + 3
        neighborY = self.yPos
        if(neighborX < len(boardArray[neighborY])):
            if(boardArray[neighborY][neighborX] != '#'):
                #The neighbor is valid, so add it to the list
                neighbors.append(Node(self,neighborX,neighborY,32767,goal))

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
            print(dirDif)
     
        # Return minimum number of turns needed to arrive at the goal
        print(max(dirDif)/3)
        return (max(dirDif)/3)

    def calcG(self):

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
        print ("\nTerrain cost: ",arr[self.yPos][self.xPos], "\nParent G Cost: ", self.parent.g_cost, "\nTurn Cost: ", cost)
        g = arr[self.yPos][self.xPos] + self.parent.g_cost + cost
        
        return g
#----------------------------------------------------------------------------
def createPath(currentNode):
    path = []
    while(currentNode.parent != None):
        path.append(currentNode)
        currentNode = currentNode.parent
    return path.reverse()
#----------------------------------------------------------------------------
def printResults(path):
    while(not path):
        print("xPos: ",path[0].xPos," yPos: ",path[0].yPos)
        path.pop(0)
#----------------------------------------------------------------------------
# Create the argument parser.
parser = argparse.ArgumentParser(description="Read in a map and run A* on it.")

# Add arguments to the parser.
parser.add_argument("map", help="Path to the map file.")
parser.add_argument("heuristic", help="Which heuristic to use.", type = int, choices = [1,2,3,4,5,6])

# Parses the arguments.
args = parser.parse_args()

# Set the huristic to use
HEURISTIC = args.heuristic

# Open the file.
with open(args.map, 'r') as f:
    arr = [line.strip('\n').split('\t') for line in f]

#DONT FORGET: arrays are -> arr[y][x]
for i in range(0,len(arr)):
    for j in range(0,len(arr[i])):
        if (arr[i][j] == 'S'):
            startNode = Node(None,i,j,1,None)
            arr[i][j] = 1
        elif (arr[i][j] == 'G'):
            goalNode = Node(None,i,j,1,None)
            arr[i][j] = 1
        else:
            if (arr[i][j] != "#"):
                arr[i][j] = int(arr[i][j])

for i in range(0, len(arr)):
    print (arr[i])
#----------------------------------------------------------------------------
#init the open list
openList = [startNode]
closedList = []

while (len(openList) != 0):
    #get the lowest cost node (last in list)
    toExpand = openList.pop(0)
    if (toExpand == goalNode):
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

    closedList.append(toExpand)
print("Path not found")
