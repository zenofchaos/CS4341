# Imports
import argparse
import random
import sys

# Create the argument parser.
parser = argparse.ArgumentParser(description="Create maps that can be traversed by main.py (A*).")

# Add arguments to the parser.
parser.add_argument("width", help="Width of the file. Minimum 2, maximum 100.", type = int, choices = range(2,100))
parser.add_argument("length", help="Length of the file. Minimum 2, maximum 100.", type = int, choices = range(2,100))

# Parses the arguments.
args = parser.parse_args()

# List of all possible terrain types. (Double chance for each number when compared to a wall.
terrain = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "1", "2", "3", "4", "5", "6", "7", "8", "9", "#"]

# Empty map.
map = []

# For loop that places each integer.
for i in range (0, args.width):

	# Line list declared to an empty list.
	line = []

	for j in range (0, args.length):

		# Add this the line list.
		line.append(random.choice(terrain))

		# Add the line to the map if the line is done.
		if (j == args.length - 1):
			map.append(line)

start = [] 
goal = []

# Guarentee the start and goal aren't the same.
while (start == goal):

	# Random start and end locations.
	start = [random.randrange(0, args.width), random.randrange(0, args.length)]
	goal = [random.randrange(0, args.width), random.randrange(0, args.length)]

map[start[0]][start[1]] = "S"
map[goal[0]][goal[1]] = "G"

for i in range (0, len(map)):
	print ("\t".join(map[i]))