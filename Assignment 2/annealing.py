# Import
import optimize
import random
import time

def annealClimb(args, arr, score):
	round = 0
	iteration = 0
	topScore = score
	START = time.time()
	heat = .6;
	tempbin1,tempbin2,tempbin3 = [],[],[]
	
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
		
		# if new state is better increment rounds, and revert the swap
		if(topScore >= newScore):
			chance = random.random()
			# chance depending on heat to increment and take a worse move
			if(chance > heat):
				arr[binChoice2],arr[binChoice1] = arr[binChoice1],arr[binChoice2]
				round += 1
			else:
				#Heat high enough. Take the worse move
				round = 0
				topScore = newScore
			
		else:
			if (args.debug):
				print ("Top score of",topScore,"was beat by",newScore,"on round",round,"of iteration",iteration)

			# reset round limit
			round = 0
			topScore = newScore
			
		# if 100th round and still have time. Reset to a random start position
		if (round == 200 and time.time() - START <= args.time):
			round = 0
			tempbin1 = add_sub_bin
			tempbin2 = position_bin
			tempbin3 = prime_bin
			
			random.shuffle(arr)
			iteration += 1
			
		# at end of every cycle decrease heat if not 0
		if(heat > 0):
			heat -= .0005
		
	print ("\nFinal Hil Climbing Results:")
	if(iteration > 0):
		print ("Bin #1:", tempbin1)
		print ("Bin #2:", tempbin2)
		print ("Bin #3:", tempbin3)
	else:
		print("Bin #1:", add_sub_bin)
		print ("Bin #2:", position_bin)
		print ("Bin #3:", prime_bin)
	print ("Final Score:", topScore)
	print ("Heat reduced to:", heat)
	print ("Iteration is:", iteration)
	return topScore