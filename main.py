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

        return 1

        if (goalNode == None):
            return 0
        else:
            if(HEURISTIC == 1):
                print ()
            elif(HEURISTIC == 2):
                print ()
            elif(HEURISTIC == 3):
                print ()
            elif(HEURISTIC == 4):
                print ()
            elif(HEURISTIC == 5):
                print ()
            elif(HEURISTIC == 6):
                print ()
            else:
                print("Error in calcH: Heuristic outside of [1,6]")
                return -1
    def calcG():
        return
        #somewhere in here we need calcDir()

    def calcDir(self):

        # First, determine the starting direction.
        # Guide to directions. North is 1, East is 2, South is 3, and West is 4.
        # If the parent of this node's parent is None, then it's the start. Starting direction is north.
        if (self.parent.parent == None):
            startDir = 1
            print ("Grandparent is start.")
        # If the parent has a smaller y-value that its parent, then the direction is north.
        elif (self.parent.yPos < self.parent.parent.yPos):
            startDir = 1
        # If the parent has a larger x-value that its parent, then the direction is east.
        elif (self.parent.xPos > self.parent.parent.xPos):
            startDir = 2
        # If the parent has a larger y-value that its parent, then the direction is south.
        elif (self.parent.yPos > self.parent.parent.yPos):
            startDir = 3
        # If the parent has a smaller x-value that its parent, then the direction is west.
        elif (self.parent.xPos < self.parent.parent.xPos):
            startDir = 4

        # Next determine the ending direction.
        # If the node has a smaller y-value that its parent, then the direction is north.
        if (self.yPos < self.parent.yPos):
            endDir = 1
        # If the node has a larger x-value that its parent, then the direction is east.
        elif (self.xPos > self.parent.xPos):
            endDir = 2
        # If the node has a larger y-value that its parent, then the direction is south.
        elif (self.yPos > self.parent.yPos):
            endDir = 3
        # If the node has a smaller x-value that its parent, then the direction is west.
        elif (self.xPos < self.parent.xPos):
            endDir = 4

        # Now determine the cost accosiated with the turn.
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

# while (len(openList) != 0):
#     #get the lowest cost node (last in list)
#     toExpand = openList.pop(0)
#     if (toExpand == goalNode):
#             path = createPath(toExpand)
#             printResults(path)
#             return
#     neighbors = toExpand.getNeighbors(toExpand)

#     for k in range(0,len(neighbors)):
#         neighbors[k].calcG()
#         f_cost = neighbors[k].g_cost + neighbors[k].h_cost

#         if (neighbors[k] in openList):
#             prev = openList.index(neighbors[k])
#             if (neighbors[k].f_cost < openList[prev].f_cost):
#                 openList[prev] = neighbors[k]
#         elif (neighbors[k] in closedList):
#             prev = closedList.index(neighbors[k])
#             if (neighbors[k].f_cost < closedList[prev].f_cost):
#                 closedList[prev] = neighbors[k]
#         else:
#             openList.append(neighbors[k])
#             openList.sort()

#     closedList.append(toExpand)
