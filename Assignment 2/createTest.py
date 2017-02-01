# Imports
import argparse
import random

# Global Constants
POSSIBLE_INTEGERS = ["-9", "-8", "-7", "-6", "-5", "-4", "-3", "-2", "-1", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]

# Create the argument parser.
parser = argparse.ArgumentParser(description="Reads in a number between.")

# Add arguments to the parser.
parser.add_argument("ints", help="Number of ints in the output list.", type = int, choices = range(3, 10000), metavar= "integer in the range of [3,9999]")

# Parses the arguments.
args = parser.parse_args()

# Verify the user gave proper input.
int_list_length = args.ints//3 * 3

# List for integers.
int_list = []

# Loop through and append all of the integers.
for i in range(0, int_list_length):
	int_list.append(random.choice(POSSIBLE_INTEGERS))

# Print the final list.
print(" ".join(int_list))