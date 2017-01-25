# Imports
import argparse
import sys

# Create the argument parser.
parser = argparse.ArgumentParser(description="Read in a map and run A* on it.")

# Add arguments to the parser.
parser.add_argument("map", help="Path to the map file.")

# Parses the arguments.
args = parser.parse_args()

# Open the file.
with open(args.map, 'r') as f:
    arr = [line.strip('\n').split('\t') for line in f]

for i in range(0,len(arr)):
    for j in range(0,len(arr[i])):
        arr[i][j] = (arr[i][j])

for i in range(0, len(arr)):
	print (arr[i])