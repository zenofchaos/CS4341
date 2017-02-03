# Import
import optimize
import random
import time

def firstClimb(args, arr, score):
	round = 0
	iteration = 0
	topScore = score
	topOverallScore = -1000000
	START = time.time()
	tempbin1,tempbin2,tempbin3 = [],[],[]
	roundTotal = 0
	
	if (args.debug):
		print ("\nStarting Iteration:", iteration)

	while(round <= 100 and time.time() - START <= args.time):

		binChoice1 = random.randint(0,len(arr)-1)
		binChoice2 = random.randint(0,len(arr)-1)
		
		if(binChoice1 == binChoice2):
			if(binChoice2 == 0):
				binChoice2 += 1
			else:
				binChoice2 -= 1
	
		arr[binChoice1],arr[binChoice2] = arr[binChoice2],arr[binChoice1]
		
		add_sub_bin = arr[0:len(arr)//3]
		position_bin = arr[len(arr)//3: 2*len(arr)//3]
		prime_bin = arr[2*len(arr)//3:len(arr)]

		newScore = optimize.scoreBins(args, add_sub_bin,position_bin,prime_bin, False)
		
		if(topScore >= newScore):
			arr[binChoice2],arr[binChoice1] = arr[binChoice1],arr[binChoice2]
			round += 1
			roundTotal += 1
		else:
			round = 0
			topScore = newScore

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

			# Shuffle and make new bins.
			random.shuffle(arr)
			add_sub_bin = arr[0:len(arr)//3]
			position_bin = arr[len(arr)//3: 2*len(arr)//3]
			prime_bin = arr[2*len(arr)//3:len(arr)]

			# New iteration. Reset rounds and scores.
			iteration += 1
			topScore = optimize.scoreBins(args, add_sub_bin,position_bin,prime_bin, False)
			round = 0

			# Print the start of the next iteration!
			if (args.debug):
				print("\nIteration",iteration,"has started!")
	
	if (args.debug):
		print ("Iteration",iteration,"ran out of time!")
	print ("\nFinal Hill Climbing Results:")
	print ("Bin #1:", tempbin1)
	print ("Bin #2:", tempbin2)
	print ("Bin #3:", tempbin3)
	print ("Final Score:", topOverallScore)
	print ("Best Iteration:", bestIteration)
	print ("Total Iterations:", iteration)
	print ("Total Rounds:", roundTotal)
	return topOverallScore