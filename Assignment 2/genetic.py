#Genetic Algorithm code for Assignment 2 of CS 4341, AI
import random
import optimize
import time
import copy

#Calibration settings for GA search
POP_SIZE = 150
ELITISM_DECIMAL = 0.15
MUTATION_DECIMAL = 0.3
COUNTER = 50

class Member():

        def __init__(self,args,arr):
                self.arr = arr
                self.score = self.calcScore(args,False)
                self.args = args

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
                for i in range(0,len(self.arr)):
                        a = self.arr[i]
                        b = VALUES_ARRAY[a]
                        arrValues.append(b)

                #Split the array into the 3 bins
                add_sub_bin = arrValues[0:len(arrValues)//3]
                position_bin = arrValues[len(arrValues)//3: 2*len(arrValues)//3]
                prime_bin = arrValues[2*len(arrValues)//3:len(arrValues)]
                #calculate the score of the bins
                return optimize.scoreBins(args, add_sub_bin, position_bin, prime_bin, to_print)

        #mutates this member based on the mutation chance MUTATION_DECIMAL
        def mutate(self,args):
                if(args.debug):
                        print("MUTATION HAPPENED")
                toSwap1 = random.randint(0,len(self.arr)-1)
                toSwap2 = random.randint(0,len(self.arr)-1)

                if(toSwap1 == toSwap2):
                        if(toSwap2 == 0):
                                toSwap2 += 1
                        else:
                                toSwap2 -= 1

                self.arr[toSwap1],self.arr[toSwap2] = self.arr[toSwap2],self.arr[toSwap1]

                #recalculate score
                self.score = self.calcScore(self.args, False)
                

        #alters the given member such that invalid components are replaced with valid components
        def makeValid(self):
                locArr = self.arr
                gluttons = []
                starving = []
                countArr = [0]*len(locArr)
                repeatExists = False
                
                for i in range(0,len(locArr)):
                        countArr[locArr[i]] += 1
                        if (countArr[locArr[i]] == 2):
                                repeatExists = True
                                gluttons.append(i)
                if (repeatExists):
                        for j in range(0,len(locArr)):
                                if (countArr[j] == 0):
                                        starving.append(j)
                        for k in range(0,len(starving)):
                                self.arr[gluttons[k]] = starving[k]

                #recalculate score
                self.score = self.calcScore(self.args, False)


#Returns a weighted random Member from a population
################################################
#    Title: A weighted version of random.choice
#    Author: Ned Batchelder
#    Date: 11/9/2010
#    Code version: Python 
#    Availability: http://stackoverflow.com/questions/3679694/a-weighted-version-of-random-choice
################################################
def weighted_choice(population):
        minScore = abs(min(population).score) + 1
        total = sum((Member.score + minScore) for Member in population)
        r = random.uniform(0, total)
        upto = 0
        for Member in population:
                if ((upto + (Member.score + minScore)) >= r):
                        return Member
                upto += (Member.score + minScore)
        assert False, "Shouldn't get here"

#Runs a genetic algorithm on the given bins to maximize
#the score returned by scoreBins
#       Parameter: arr - an array of input integers in [-9,9] to be sorted
def geneticAlg(args,arr):
        if(args.debug):
                print("In genetic alg")
                
        #save array values to be used later
        global VALUES_ARRAY
        VALUES_ARRAY = list(arr)
        
        
        #convert arr to an array of positions
        for h in range(0,len(arr)):
                arr[h] = h

        originalMem = Member(args, list(arr))

        #initialize the populations
        presentPop = []
        futurePop = []
        
        #fill the initial population
        for i in range(0,POP_SIZE):
                random.shuffle(arr)
                temp = list(arr)
                m = Member(args,temp)
                presentPop.append(m)
        
        # Start timer
        START = time.time()
    
        generationsCreated = 0
        #for GENERATIONS iterations, or until the timer runs out
        # TODO possibly get rid of generations?
        while (time.time() - START <= args.time):
                if (args.debug):
                        print("NEW GENERATION")
                
                #sort the population so the best fit members are at the lowest index
                presentPop.sort()
                presentPop.reverse()
                
                #save elites - assumes presentPop is sorted most fit to least fit
                numElites = int(POP_SIZE * ELITISM_DECIMAL)
                for j in range(0,numElites):
                        futurePop.append(presentPop[j])
                        
                numNewMembers = 0
                #for (POP_SIZE - #elites) iterations
                while (numNewMembers < (POP_SIZE - numElites)):
                        if(args.debug):
                                print("New members", time.time() - START)
                                
                        #select two members
                        firstMember = weighted_choice(presentPop)
                        secondMember = weighted_choice(presentPop)
                        numEqLoops = 0
                        while (secondMember == firstMember and numEqLoops < COUNTER):
                                if (args.debug):
                                        print("2nd mem invalid - must choose other")
                                secondMember = weighted_choice(presentPop)      
                                numEqLoops += 1

                        if (numEqLoops == COUNTER):
                                #if(args.debug):
                                print("got stuck in equality loop")
                                break
                                
                        if(args.debug):
                                print("Members Chosen", time.time() - START)
                                
                        #create a random cutline
                        cutLine = random.randint(1,len(firstMember.arr) - 1)
                        
                        #add random cut and form new members
                        mem1FirstHalf = list(firstMember.arr[0:cutLine])
                        mem1SecondHalf = list(firstMember.arr[cutLine:len(firstMember.arr)])
                        mem2FirstHalf = list(secondMember.arr[0:cutLine])
                        mem2SecondHalf = list(secondMember.arr[cutLine:len(firstMember.arr)])

                        newMem1 = Member(args,mem1FirstHalf + mem2SecondHalf)
                        newMem2 = Member(args,mem2FirstHalf + mem1SecondHalf)

                        if(args.debug):
                                print("Members combined", time.time() - START)

                        #convert to a valid member if it's not
                        newMem1.makeValid()
                        newMem2.makeValid()
                        if(args.debug):
                                print("Members valid", time.time() - START)
                                
                        #implement mutation
                        if (random.random() <= MUTATION_DECIMAL):
                                newMem1.mutate(args)
                                if(args.debug):
                                        print("Mutation implemented on 1")
                        if (random.random() <= MUTATION_DECIMAL):
                                newMem2.mutate(args)
                                if(args.debug):
                                        print("Mutation implemented on 2")

                        #add to new population
                        futurePop.append(newMem1)
                        numNewMembers += 1
                        if (numNewMembers >= (POP_SIZE - numElites)):
                                break;
                        futurePop.append(newMem2)
                        numNewMembers += 1
                        if(args.debug):
                                print("Members Added", time.time() - START)
                #end while(numNewMembers...)

                #if the equality loop in the previous while loop runs 15 times
                #it's safe to say that the best solution has been found since
                #all population members are virtually identical
                if (numEqLoops == COUNTER):
                        print("Generations stagnated - best possible solution found")
                        break

                if (args.debug):
                        print("Reinitialize populations")
                #reinitialize populations
                for i in range(0,len(futurePop)):
                        presentPop[i] = futurePop[i]
                futurePop = []

                #increment generations
                generationsCreated += 1
        #end while(generationsCreated....
    
        #sort the population so the best fit members are at the lowest index
        presentPop.sort()
        presentPop.reverse()
        
        #analysis
        print("Elitism:                      ", ELITISM_DECIMAL*100, "%")
        print("Population Size:              ", POP_SIZE)
        print("Number of Generations Created:", generationsCreated)
        print("Original Score:               ", originalMem.score)
        print("Original Score:               ", originalMem.calcScore(originalMem.args, False))
        print("Best Score:                   ", presentPop[0].score)          
        #for p in range(0,len(presentPop)):
        #        print(presentPop[p])
        print("------------------------------------------------------------------------------------")
        #print()
        #for p in range(0,len(futurePop)):
        #        print(futurePop[p])

