# Imports
import argparse
import random
import genetic

# Global Constants
PRIME_LIST = [3, 5, 7]
COMPOSITE_LIST = [0, 1, 2, 4, 6, 8, 9]

# Bin scoring function.
def scoreBins(args,add_sub_bin, position_bin, prime_bin):

	# Notify the user where they are in the code, if they're debugging.
	if (args.debug):
		print("\nRunning the scoring system.")

	# Calculate the first bin's score.
	add_sub_score = add_sub_bin[0]
	for i in range (1, len(add_sub_bin)):
		add_sub_score += (-(-1) ** i) * add_sub_bin[i]
	print ("Bin #1 Score:", add_sub_score)

	# Calculate the second bin's score.
	position_score = 0
	for i in range (0, len(position_bin) - 1):
		if (position_bin[i] < position_bin[i + 1]):
			position_score += 3
		elif (position_bin[i] == position_bin[i + 1]):
			position_score += 5
		else:
			position_score -= 10
	print ("Bin #2 Score:", position_score)

	# Calculate the third bin's score.
	prime_score = 0

	for i in range(0, len(prime_bin)):

		# If this is the list's first half.
		if (i < len(prime_bin)//2):
			
			if (prime_bin[i] in PRIME_LIST):
				prime_score += 4
			elif (prime_bin[i] in COMPOSITE_LIST):
				prime_score -= prime_bin[i]
			else:
				prime_score -= 2

		# Ignore the middle if it's an odd length set.
		elif (i == len(prime_bin)//2 and len(prime_bin) % 2):
			continue

		# If this is the list's second half.
		else:

			if (prime_bin[i] in PRIME_LIST):
				prime_score -= 4
			elif (prime_bin[i] in COMPOSITE_LIST):
				prime_score += prime_bin[i]
			else:
				prime_score += 2
	print ("Bin #3 Score:", prime_score)



	# Program success.
	return 0
#end scoreBins()

if __name__ == "__main__":

        # Create the argument parser.
        parser = argparse.ArgumentParser(description="Reads in a list of intergers between [-9,9], splits them into bins, sorts them as well as possible, and scores them.")

        # Add arguments to the parser.
        parser.add_argument("--debug", "-d", help="Print the debug version of the program.", action="store_true")
        parser.add_argument("search", help="Which search type to use.", type = str, choices = ["hill", "annealing", "ga"])
        parser.add_argument("ints", help="Path to the integer list's file.", type = str)
        parser.add_argument("time", help="Time in seconds that the program is allowed to run for.", type = float)


        # Parses the arguments.
        args = parser.parse_args()

        # Notify the user that they're in debugging mode.
        if (args.debug):
                print ("\nProgram started in debug mode.")

         # Open the file and store the integers in a single array.
        with open(args.ints) as f:

                arr = []

                for line in f:
                        line = line.split(" ")

                for i in range(0, len(line)):
                        arr.append(int(line[i]))

        # Print the newly imported list.
        if (args.debug):
                print(arr)

        # Randomize the list.
        random.shuffle(arr)

        # Print the newly shuffled list.
        if (args.debug):
                print (arr)

        # Split the now random list.
        add_sub_bin = arr[0:len(arr)//3]
        position_bin = arr[len(arr)//3: 2*len(arr)//3]
        prime_bin = arr[2*len(arr)//3:len(arr)]

        # Print the new lists.
        if (args.debug):
                print (add_sub_bin,position_bin,prime_bin)

        # Run the scoring system.
        scoreBins(args,add_sub_bin, position_bin, prime_bin)

        genetic.geneticAlg(args,arr)

#end if(__name__...)
