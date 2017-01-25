# Imports
import argparse
import sys

#global constants
HEURISTIC = 1

class Node:
    
    def __init__(self,p,x,y,g,goalNode):
        self.parent = p
        self.xPos = x
        self.yPos = y
        self.g_cost = g
        self.h_cost = self.calcH(goalNode)

    def equals(self,toCheck):
        return ((self.xPos == toCheck.xPos) and (self.yPos == toCheck.yPos))

    def calcH(self,goalNode):
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
            startNode = Node(None,j,i,1,None)
        elif (arr[i][j] == 'G'):
            goalNode = Node(None,j,i,1,None)
        else:
            continue

for i in range(0, len(arr)):
	print (arr[i])

print (goalNode.parent,goalNode.xPos,goalNode.yPos,goalNode.g_cost)
#----------------------------------------------------------------------------

#init the open list
openList = [startNode]
closedList = []

##while (len.openList != 0):
##    #get the lowest cost node (last in list)
##    toExpand = openList.pop()
##    neighbors = toExpand.getNeighbors()
##
##    for k in range(0,len(neighbors)):
##        if (neighbors[k].equals(goalNode)):
##            path = createPath(neighbors[k])
##            printResults(path)
##            return
        


