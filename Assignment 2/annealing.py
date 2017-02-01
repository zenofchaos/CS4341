# Import
import optimize
import random
import time

def annealClimb(args, arr, score):
	round = 0
	iteration = 0
	topScore = score
	START = time.time()
	
	
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

		newScore =optimize.scoreBins(args, add_sub_bin,position_bin,prime_bin, False)
		
		if(topScore >= newScore):
			arr[binChoice2],arr[binChoice1] = arr[binChoice1],arr[binChoice2]
			round += 1
		else:
			if (args.debug):
				print ("Top score of",topScore,"was beat by",newScore,"on round",round,"of iteration",iteration)

			round = 0
			topScore = newScore

		if (round == 100 and time.time() - START <= args.time):
			round = 0
			random.shuffle(arr)
			iteration += 1
		
	print ("\nFinal Hil Climbing Results:")
	print ("Bin #1:", add_sub_bin)
	print ("Bin #2:", position_bin)
	print ("Bin #3:", prime_bin)
	print ("Final Score:", topScore)
	return topScore