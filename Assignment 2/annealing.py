# Import
import math
import optimize
import random
import time

# Global Constants
HEAT_VALUE = 5

def probabilty(args, topScore, newScore, heat):

	if newScore > topScore:
		return 1.0
	else:
		prob = math.exp((newScore - topScore - 1) / heat)
		return prob

def cooldown(args, heat):
	if (heat > 0.01):
		return (heat - 0.01)
	else:
		return heat


def annealClimb(args, arr, score):
	round = 0
	iteration = 0
	bestIteration = 0
	topScore = score
	topOverallScore = -1000000
	START = time.time()
	heat = HEAT_VALUE;
	tempbin1,tempbin2,tempbin3 = [],[],[]
	roundTotal = 0

	if (args.debug):
		print ("\nStarting Iteration:", iteration)
	
	while(round <= 100 and time.time() - START <= args.time):

		# pick 2 random numbers in the array to swap
		binChoice1 = random.randint(0,len(arr)-1)
		binChoice2 = random.randint(0,len(arr)-1)
		
		# checking if same choice for swapping
		if(binChoice1 == binChoice2):
			if(binChoice2 == 0):
				binChoice2 += 1
			else:
				binChoice2 -= 1
		
		#performs the swap on the array of numbers
		arr[binChoice1],arr[binChoice2] = arr[binChoice2],arr[binChoice1]
			
		# recreat the bins
		add_sub_bin = arr[0:len(arr)//3]
		position_bin = arr[len(arr)//3: 2*len(arr)//3]
		prime_bin = arr[2*len(arr)//3:len(arr)]

		# Score the move
		newScore =optimize.scoreBins(args, add_sub_bin,position_bin,prime_bin, False)

		chance = random.random()
		if (probabilty(args, topScore, newScore, heat) > chance):
			round = 0
			topScore = newScore
			
		else:
			arr[binChoice2],arr[binChoice1] = arr[binChoice1],arr[binChoice2]
			round += 1
			roundTotal += 1

			
		# if 100th round and still have time. Reset to a random start position
		if (round == 100 and time.time() - START <= args.time):

			if (args.debug):
				print ("Bin #1:", add_sub_bin)
				print ("Bin #2:", position_bin)
				print ("Bin #3:", prime_bin)
				print ("Iteration Score:", topScore)

			# Store the best overall score and its bins
			if (topScore > topOverallScore):
				topOverallScore = topScore
				bestIteration = iteration
				tempbin1 = add_sub_bin
				tempbin2 = position_bin
				tempbin3 = prime_bin

			round = 0
			
			# Shuffle and make new bins.
			random.shuffle(arr)
			add_sub_bin = arr[0:len(arr)//3]
			position_bin = arr[len(arr)//3: 2*len(arr)//3]
			prime_bin = arr[2*len(arr)//3:len(arr)]

			# New iteration. Reset rounds and scores.
			iteration += 1
			topScore = optimize.scoreBins(args, add_sub_bin,position_bin,prime_bin, False)
			round = 0
			heat = HEAT_VALUE

			# Print the start of the next iteration!
			if (args.debug):
				print("\nIteration",iteration,"has started!")
			
		heat = cooldown(args, heat)

	if (args.debug):
		print ("Iteration",iteration,"ran out of time!")
		print ("Bin #1:", add_sub_bin)
		print ("Bin #2:", position_bin)
		print ("Bin #3:", prime_bin)
		print ("Iteration Score:", topScore)
	# Store the best overall score and its bins
	if (topScore > topOverallScore):
		topOverallScore = topScore
		bestIteration = iteration
		tempbin1 = add_sub_bin
		tempbin2 = position_bin
		tempbin3 = prime_bin

	print ("\nFinal Simulated Annealing Results:")
	print ("Bin #1:", tempbin1)
	print ("Bin #2:", tempbin2)
	print ("Bin #3:", tempbin3)
	print ("Final Score:", topOverallScore)
	print ("Best Iteration:", bestIteration)
	print ("Total Iterations:", iteration)
	print ("Total Rounds:", roundTotal)
	return topOverallScore