# Imports
import argparse
import sys

class Node:
    
    def __init__(self,p,x,y,c):
        self.parent = p
        self.xPos = x
        self.yPos = y
        self.cost = c
    
#----------------------------------------------------------------------------
# Create the argument parser.
parser = argparse.ArgumentParser(description="Read in a map and run A* on it.")

# Add arguments to the parser.
parser.add_argument("map", help="Path to the map file.")

# Parses the arguments.
args = parser.parse_args()

# Open the file.
with open(args.map, 'r') as f:
    arr = [line.strip('\n').split('\t') for line in f]

#DONT FORGET: arrays are -> arr[y][x]
for i in range(0,len(arr)):
    for j in range(0,len(arr[i])):
        if (arr[i][j] == 'S'):
            startNode = Node(None,j,i,1)
        elif (arr[i][j] == 'G'):
            goalNode = Node(None,j,i,1)
        else:
            continue

for i in range(0, len(arr)):
	print (arr[i])

print (goalNode.parent,goalNode.xPos,goalNode.yPos,goalNode.cost)
#----------------------------------------------------------------------------

#init the open list

#while (len.openList != 0)
    
