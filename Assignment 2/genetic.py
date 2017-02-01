#Genetic Algorithm code for Assignment 2 of CS 4341, AI
import random
import optimize


#Calibration settings for GA search
POP_SIZE = 100
ELITISM_DECIMAL = 0.1
MUTATION_DECIMAL = 0.01

class Member():

        def __init__(self,args,arr):
                self.add_sub_bin = arr[0:len(arr)//3]
                self.position_bin = arr[len(arr)//3: 2*len(arr)//3]
                self.prime_bin = arr[2*len(arr)//3:len(arr)]
                self.score = optimize.scoreBins(args, self.add_sub_bin, self.position_bin, self.prime_bin)

#Returns the count of each number [-9,9] in the given array
def getNumNums(arr):
        numCount = []
        for i in range(-9,10):
                count = 0;
                for j in range(0,len(arr)):
                        if i == arr[j]:
                                count += 1
                numCount[i] = count
        return numCount

#Runs a genetic algorithm on the given bins to maximize
#the score returned by scoreBins
#       Parameter: arr - an array of input integers in [-9,9] to be sorted
def geneticAlg(args,arr):
        if(args.debug):
                print("In genetic alg")

        #generate a list of the number of each number in arr
        #will be used to determine if a member is valid
        nuNums = getNumNums(arr)
        
        #initialize the populations
        presentPop = []
        futurePop = []

        #fill the initial population
        for i in range(0,POP_SIZE):
                presentPop.append(Member(args,random.shuffle(arr)))
                
        #save elites
        numElites = int(POP_SIZE * ELITISM_DECIMAL)
        

        #generate probabilities

        #for (POP_SIZE - #elites) iterations
        
                #select two members

                #add random cut

                #combine to form two new members

                #verify valid member

                #implement mutation (randomly switch two numbers)

                #add to new population
        

