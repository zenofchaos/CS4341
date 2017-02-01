#Genetic Algorithm code for Assignment 2 of CS 4341, AI
import random
import optimize


#Calibration settings for GA search
POP_SIZE = 100
ELITISM_DECIMAL = 0.1
MUTATION_DECIMAL = 0.01

class Member():

        def __init__(self,args,arr):
                self.arr = arr
                self.add_sub_bin = arr[0:len(arr)//3]
                self.position_bin = arr[len(arr)//3: 2*len(arr)//3]
                self.prime_bin = arr[2*len(arr)//3:len(arr)]
                self.score = optimize.scoreBins(args, self.add_sub_bin, self.position_bin, self.prime_bin)

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

#Runs a genetic algorithm on the given bins to maximize
#the score returned by scoreBins
#       Parameter: arr - an array of input integers in [-9,9] to be sorted
def geneticAlg(args,arr):
        if(args.debug):
                print("In genetic alg")

        #generate a list of the number of each number in arr
        #will be used to determine if a member is valid
        validNumNums = getNumNums(arr)
        
        #initialize the populations
        presentPop = []
        futurePop = []

        #fill the initial population
        for i in range(0,POP_SIZE):
                presentPop.append(Member(args,random.shuffle(arr)))
                
        #save elites - assumes presentPop is sorted most fit to least fit
        numElites = int(POP_SIZE * ELITISM_DECIMAL)
        for j in range(0,numElites):
                futurePop[j] = presentPop[j]

        numNewMembers = 0
        #for (POP_SIZE - #elites) iterations
        while (numNewMembers < (POP_SIZE - numElites)):
                #select two members - TODO
                firstMember = weighted_choice(presentPop)
                secondMember = weighted_choice(presentPop)
                while (secondMember == firstMember):
                        secondMember = weighted_choice(presentPop)
                        
                #add random cut and form new members
                cutLine = random.randint(1,len(arr)-1)
                mem1FirstHalf = firstMember.arr[0:cutLine]
                mem1SecondHalf = firstMember.arr[cutLine:len(firstMember.arr)]
                mem2FirstHalf = secondMember.arr[0:cutLine]
                mem2SecondHalf = secondMember.arr[cutLine,len(firstMember.arr)]

                newMem1 = Member(args,mem1FirstHalf + Mem2SecondHalf)
                newMem2 = Member(args,mem1FirstHalf + Mem2SecondHalf)

                #if valid member
                mem1NumNums = getNumNums(newMem1.arr)
                if (mem1NumNums == validNumNums):
                        #implement mutation (randomly switch two numbers)
                        if (random.random() <= MUTATION_DECIMAL):
                                newMem1.mutate()
                        #add to new population
                        futurePop.append(newMem1)
                        numNewMembers += 1
                if (mem2NumNums == validNumNums):
                        #implement mutation (randomly switch two numbers)
                        if (random.random() <= MUTATION_DECIMAL):
                                newMem1.mutate()
                        #add to new population
                        futurePop.append(newMem1)
                        numNewMembers += 1

