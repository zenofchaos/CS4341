#Genetic Algorithm code for Assignment 2 of CS 4341, AI
import random
import optimize


#Calibration settings for GA search
POP_SIZE = 100
ELITISM_DECIMAL = 0.1
MUTATION_DECIMAL = 0.01

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
                arrOfValues = #TODO - Convert to array of values
        
                add_sub_bin = arrOfValues[0:len(arrOfValues)//3]
                position_bin = arrOfValues[len(arrOfValues)//3: 2*len(arrOfValues)//3]
                prime_bin = arrOfValues[2*len(arrOfValues)//3:len(arrOfValues)]
                optimize.scoreBins(args, add_sub_bin, position_bin, prime_bin,False)

        #mutates this member based on the mutation chance MUTATION_DECIMAL
        def mutate(self,args):
                return self

#Returns a weighted random Member from a population
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
        #TODO - fill in function


#Runs a genetic algorithm on the given bins to maximize
#the score returned by scoreBins
#       Parameter: arr - an array of input integers in [-9,9] to be sorted
def geneticAlg(args,arr):
        if(args.debug):
                print("In genetic alg")

        #generate a hash table of 0 -> arr[0]
        #TODO

        #convert arr to an array of positions
        for h in range(0,len(arr)):
                arr[i] = i
        
        #initialize the populations
        presentPop = []
        futurePop = []

        #fill the initial population
        for i in range(0,POP_SIZE):
                presentPop.append(Member(args,random.shuffle(arr)))

        #sort the population so the best fit members are at the lowest index
        arr.sort() #TODO - will this work? is the syntax right?
        
        #save elites - assumes presentPop is sorted most fit to least fit
        numElites = int(POP_SIZE * ELITISM_DECIMAL)
        for j in range(0,numElites):
                futurePop[j] = presentPop[j]

        #TODO: Currently only iterates once, generating 1 new population from the original and stopping
        #       Need to add another loop that is linked with a timer
        
        numNewMembers = 0
        #for (POP_SIZE - #elites) iterations
        while (numNewMembers < (POP_SIZE - numElites)):
                #select two members - TODO
                firstMember = weighted_choice(presentPop)
                secondMember = weighted_choice(presentPop)
                while (secondMember == firstMember):
                        secondMember = weighted_choice(presentPop)
                        
                #add random cut and form new members
                mem1FirstHalf = firstMember.arr[0:cutLine]
                mem1SecondHalf = firstMember.arr[cutLine:len(firstMember.arr)]
                mem2FirstHalf = secondMember.arr[0:cutLine]
                mem2SecondHalf = secondMember.arr[cutLine,len(firstMember.arr)]

                newMem1 = Member(args,mem1FirstHalf + Mem2SecondHalf)
                newMem2 = Member(args,mem1FirstHalf + Mem2SecondHalf)

                #convert to a valid member if it's not
                newMem1 = makeValid(newMem1)
                newMem2 = makeValie(newMem1)
                
                #implement mutation
                newMem1.mutate(args)
                newMem2.mutate(args)
                
                #add to new population
                futurePop.append(newMem1)
                futurePop.append(newMem1)
                numNewMembers += 2
        #end while(numNewMembers...)

