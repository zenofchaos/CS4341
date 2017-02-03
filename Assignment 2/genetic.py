#Genetic Algorithm code for Assignment 2 of CS 4341, AI
import random
import optimize

#Calibration settings for GA search
POP_SIZE = 100
ELITISM_DECIMAL = 0.1
MUTATION_DECIMAL = 0.01
GENERATIONS = 3

VALUES_ARRAY = []

class Member():

        def __init__(self,args,arr):
                self.arr = convertToValues(arr)
                self.score = self.calcScore(args,False)

        def __eq__(self,toCheck):
                return (self.arr == toCheck.arr)
        
        def __lt__(self,toCheck):
                return (self.score < toCheck.score)

        def __le__(self,toCheck):
                return (self.score <= toCheck.score)

        def __ne__(self,toCheck):
                return not (self == toCheck)

        def __gt__(self,toCheck):
                return (self.score > toCheck.score)

        def __ge__(self,toCheck):
                return (self.score >= toCheck.score)
        
        def __str__(self):
                return "Array: " + str(self.arr) + " Score: " + str(self.score)

        #Calculates the score of this member
        def calcScore(self,args,to_print):
                #Convert the positions in arr to values
                arrValues = []
                for i in range(0,len(arr)):
                        arrValues[i] = VALUES_ARRAY[arr[i]]

                #Split the array into the 3 bins
                add_sub_bin = arrValues[0:len(arrValues)//3]
                position_bin = arrValues[len(arrValues)//3: 2*len(arrValues)//3]
                prime_bin = arrValues[2*len(arrValues)//3:len(arrValues)]

                #calculate the score of the bins
                optimize.scoreBins(args, add_sub_bin, position_bin, prime_bin,False)

        #mutates this member based on the mutation chance MUTATION_DECIMAL
        def mutate(self,args):
                return self

#Returns a weighted random Member from a population
################################################
#    Title: A weighted version of random.choice
#    Author: Ned Batchelder
#    Date: 11/9/2010
#    Code version: Python 
#    Availability: http://stackoverflow.com/questions/3679694/a-weighted-version-of-random-choice
################################################
def weighted_choice(population):
    total = sum(Member.score for Member in population)
    r = random.uniform(0, total)
    upto = 0
    for Member in population:
        if upto + Member.score >= r:
            return Member
        upto += Member.score
    assert False, "Shouldn't get here"

#returns the given member with invalid components changed to make them valid
def makeValid(member)
        toAdd = []
        toRemoveIndex = [][]
        toRemoveValue = []
        for i in range(0,len(member.arr)):
                if (i in member.arr):
                        #check if double counted
                        if (member.arr.count(i) > 1):
                                toRemoveValue.append(i)
                                firstIndex = member.arr.index(i)
                                secondIndex = member.arr.index(i,firstIndex + 1)
                                indexList = [firstIndex,secondIndex]
                                toRemoveIndex.append(indexList)
                        #end if(member.arr.count(i)...)
                else:
                        toAdd.append(i)
        #end for i...

#Runs a genetic algorithm on the given bins to maximize
#the score returned by scoreBins
#       Parameter: arr - an array of input integers in [-9,9] to be sorted
def geneticAlg(args,arr):
    if(args.debug):
        print("In genetic alg")

    #save array values and original array to be used later
    VALUES_ARRAY = arr
    originalMem = Member(args,arr)

    #convert arr to an array of positions
    for h in range(0,len(arr)):
        arr[i] = i
        
    #initialize the populations
    presentPop = []
    futurePop = []

    #fill the initial population
    for i in range(0,POP_SIZE):
        presentPop.append(Member(args,random.shuffle(arr)))

    # Start timer
    START = time.time()
    
    generationsCreated = 0
    #for GENERATIONS iterations, or until the timer runs out
    # TODO possibly get rid of generations?
    while (generationsCreated <= GENERATIONS and time.time() - START <= args.time):

        #sort the population so the best fit members are at the lowest index
        presentPop.sort()
        presentPop.reverse()
        
        #save elites - assumes presentPop is sorted most fit to least fit
        numElites = int(POP_SIZE * ELITISM_DECIMAL)
        for j in range(0,numElites):
            futurePop[j] = presentPop[j]

        numNewMembers = 0
        #for (POP_SIZE - #elites) iterations
        while (numNewMembers < (POP_SIZE - numElites)):
            if(args.debug):
                print("Creating new members")

            #select two members
            firstMember = weighted_choice(presentPop)
            secondMember = weighted_choice(presentPop)
            while (secondMember == firstMember):
                secondMember = weighted_choice(presentPop)

            #create a random cutline
            cutline = random.randint(1,len(firstMember.arr) - 1)

            #add random cut and form new members
            mem1FirstHalf = firstMember.arr[0:cutLine]
            mem1SecondHalf = firstMember.arr[cutLine:len(firstMember.arr)]
            mem2FirstHalf = secondMember.arr[0:cutLine]
            mem2SecondHalf = secondMember.arr[cutLine,len(firstMember.arr)]
            newMem1 = Member(args,mem1FirstHalf + mem2SecondHalf)
            newMem2 = Member(args,mem1FirstHalf + mem2SecondHalf)

            #convert to a valid member if it's not
            newMem1 = makeValid(newMem1)
            newMem2 = makeValie(newMem1)
            
            #implement mutation
            newMem1.mutate(args)
            newMem2.mutate(args)
                
            #add to new population
            futurePop.append(newMem1)
            futurePop.append(newMem2)
            numNewMembers += 2
        #end while(numNewMembers...)

        #reinitialize populations
        presentPop = futurePop
        futurePop = []

        #increment generations
        generationsCreated += 1
    #end while(generationsCreated....
    
    #sort the population so the best fit members are at the lowest index
    presentPop.sort()
    presentPop.reverse()
    

    #analysis
    print("Elitism: ", ELITISM_DECIMAL*100, "%")
    print("Population Size: ", POP_SIZE)
    print("Number of Generations Created: ", generationsCreated)
    print("Original Score: ", originalMem.calcScore)
    print("Best Score: ", presentPop[0].calcScore)

    

