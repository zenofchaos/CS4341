#Genetic Algorithm code for Assignment 2 of CS 4341, AI
import random
import optimize

#Calibration settings for GA search
POPULATION_SIZE = 100
ELITISM_DECIMAL = 0.1
MUTATION_DECIMAL = 0.01


class member():

        def __init__(arr):
                self.add_subb_bin = arr[0:len(arr)//3]
                self.position_bin = arr[len(arr)//3: 2*len(arr)//3]
                self.prime_bin = arr[2*len(arr)//3:len(arr)]
                self.score = scoreBins(self.add_subb_bin, self.position_bin, self.prime_bin)

#Runs a genetic algorithm on the given bins to maximize
#the score returned by scoreBins
#       Parameter: arr - an array of input integers in [-9,9] to be sorted
def geneticAlg(arr):
        

