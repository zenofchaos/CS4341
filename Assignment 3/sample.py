# Imports
import argparse
import copy
import probDicts
import random
import sys
import time

# Constants
NODE_LIST = ["humidity", "temp", "icy", "snow", "day", "cloudy", "exams", "stress"]

# Object for the environment.
class Environment:
	
	def __init__(self):
		self.query_node = None
		self.humidity = None
		self.temp = None
		self.icy = None
		self.snow = None
		self.day = None
		self.cloudy = None
		self.exams = None
		self.stress = None

	def __str__(self):
		return "\nQuerying Node: " + str(self.query_node) + "\n\nHumdity: " + str(self.humidity) + "\nTemp: " + str(self.temp) + "\nIcy: " + str(self.icy) + "\nSnow: " + str(self.snow) + "\nDay: " + str(self.day) + "\nCloudy: " + str(self.cloudy)+ "\nExams: " + str(self.exams)+ "\nStress: " + str(self.stress)

	def setNodeByArg(self, arg_string):

		# Split the string and make it lowercase.
		arg_split = arg_string.lower().split("=")

		# Search through the whole node list.
		for i in range(0, len(NODE_LIST)):

			# Is the argument provided this node.
			if (NODE_LIST[i] == arg_split[0]):

				# Error check the string.
				if (len(arg_split) < 2):
					print("\nError: No value given for this node.")
					return

				# Is the argument humidity?
				if (i == 0):
					# Is the correct value being set?
					if (arg_split[1] in ["low", "medium", "high"]):
						if (self.humidity == None):
							self.humidity = arg_split[1]
							if (self.query_node == None):
								self.query_node = arg_split[0]
						else:
							print ("\nError: Second instance of humidity found. Continuing without this node.")
					else:
						print("\nError:",arg_split[1],"is not a valid value for humidity (Low, Medium, High). Continuing without this node.")
					return
				
				# Is the argument temp?
				if (i == 1):
					# Is the correct value being set?
					if (arg_split[1] in ["warm", "mild", "cold"]):
						if (self.temp == None):
							self.temp = arg_split[1]
							if (self.query_node == None):
								self.query_node = arg_split[0]
						else:
							print ("\nError: Second instance of temp found. Continuing without this node.")
					else:
						print("\nError:",arg_split[1],"is not a valid value for temp (Warm, Mild, Cold). Continuing without this node.")
					return

				# Is the argument icy?
				if (i == 2):
					# Is the correct value being set?
					if (arg_split[1] in ["true", "false"]):
						if (self.icy == None):
							self.icy = arg_split[1]
							if (self.query_node == None):
								self.query_node = arg_split[0]
						else:
							print ("\nError: Second instance of icy found. Continuing without this node.")
					else:
						print("\nError:",arg_split[1],"is not a valid value for icy (True or False). Continuing without this node.")
					return

				# Is the argument snow?
				if (i == 3):
					# Is the correct value being set?
					if (arg_split[1] in ["true", "false"]):
						if (self.snow == None):
							self.snow = arg_split[1]
							if (self.query_node == None):
								self.query_node = arg_split[0]
						else:
							print ("\nError: Second instance of snow found. Continuing without this node.")
					else:
						print("\nError:",arg_split[1],"is not a valid value for snow (True or False). Continuing without this node.")
					return

				# Is the argument day?
				if (i == 4):
					# Is the correct value being set?
					if (arg_split[1] in ["weekend", "weekday"]):
						if (self.day == None):
							self.day = arg_split[1]
							if (self.query_node == None):
								self.query_node = arg_split[0]
						else:
							print ("\nError: Second instance of day found. Continuing without this node.")
					else:
						print("\nError:",arg_split[1],"is not a valid value for day (Weekday or Weekend). Continuing without this node.")
					return

				# Is the argument cloudy?
				if (i == 5):
					# Is the correct value being set?
					if (arg_split[1] in ["true", "false"]):
						if (self.cloudy == None):
							self.cloudy = arg_split[1]
							if (self.query_node == None):
								self.query_node = arg_split[0]
						else:
							print ("\nError: Second instance of cloudy found. Continuing without this node.")
					else:
						print("\nError:",arg_split,"is not a valid value for cloudy (True or False). Continuing without this node.")
					return

				# Is the argument exams?
				if (i == 6):
					# Is the correct value being set?
					if (arg_split[1] in ["true", "false"]):
						if (self.exams == None):
							self.exams = arg_split[1]
							if (self.query_node == None):
								self.query_node = arg_split[0]
						else:
							print ("\nError: Second instance of exams found. Continuing without this node.")
					else:
						print("\nError:",arg_split[1],"is not a valid value for exams (True or False). Continuing without this node.")
					return

				# Is the argument stress?
				if (i == 7):
					# Is the correct value being set?
					if (arg_split[1] in ["high", "low"]):
						if (self.stress == None):
							self.stress = arg_split[1]
							if (self.query_node == None):
								self.query_node = arg_split[0]
						else:
							print ("\nError: Second instance of stress found. Continuing without this node.")
					else:
						print("\nError:",arg_split[1],"is not a valid value for stress (High or Low). Continuing without this node.")
					return

		# Argument is not a node.
		print("\nError:", arg_split[0],"is not a valid node. Continuing without this node.")
		return

	# Fill the environment with random values.
	def fillEnvironment(self):

		# Set all the top nodes.
		self.humidity = humidityRandomChance()
		self.temp = tempRandomChance()
		self.day = dayRandomChance()

		# Set the icy value.
		self.icy = calcProb(probDicts.pIcy(self.humidity, self.temp))

		# Set the snow value.
		self.snow = calcProb(probDicts.pSnow(self.humidity, self.temp))

		# Set the cloudy value.
		self.cloudy = calcProb(probDicts.pCloudy(self.snow))

		# Set the exams value.
		self.exams = calcProb(probDicts.pExams(self.snow, self.day))

		# Set the stress value.
		if (calcProb(probDicts.pStress(self.snow, self.exams)) == "true"):
			self.stress = "high"
		else:
			self.stress = "low"

	# Reject an environment if anything, but the query node, doesn't match.
	def reject(self, testEnviro):

		for i in range(0, len(NODE_LIST)):

			# Is the argument humidity?
			if (i == 0):
				if ((self.query_node == "humidity") or (self.humidity == None)):
					continue
				if (self.humidity != testEnviro.humidity):
					return True

			# Is the argument temp?
			if (i == 1):
				if ((self.query_node == "temp") or (self.temp == None)):
					continue
				if (self.temp != testEnviro.temp):
					return True

			# Is the argument icy?
			if (i == 2):
				if ((self.query_node == "icy") or (self.icy == None)):
					continue
				if (self.icy != testEnviro.icy):
					return True

			# Is the argument snow?
			if (i == 3):
				if ((self.query_node == "snow") or (self.snow == None)):
					continue
				if (self.snow != testEnviro.snow):
					return True

			# Is the argument day?
			if (i == 4):
				if ((self.query_node == "day") or (self.day == None)):
					continue
				if (self.day != testEnviro.day):
					return True

			# Is the argument cloudy?
			if (i == 5):
				if ((self.query_node == "cloudy") or (self.cloudy == None)):
					continue
				if (self.cloudy != testEnviro.cloudy):
					return True

			# Is the argument exams?
			if (i == 6):
				if ((self.query_node == "exams") or (self.exams == None)):
					continue
				if (self.exams != testEnviro.exams):
					return True			

			# Is the argument stress?
			if (i == 7):
				if ((self.query_node == "stress") or (self.stress == None)):
					continue
				if (self.stress != testEnviro.stress):
					return True		
		return False

	def checkSuccess(self, testEnviro):

		if (self.query_node == "humidity"):
			if(self.humidity == testEnviro.humidity):
				return True
			else:
				return False
		if (self.query_node == "temp"):
			if(self.temp == testEnviro.temp):
				return True
			else:
				return False
		if (self.query_node == "day"):
			if(self.day == testEnviro.day):
				return True
			else:
				return False
		if (self.query_node == "icy"):
			if(self.icy == testEnviro.icy):
				return True
			else:
				return False
		if (self.query_node == "snow"):
			if(self.snow == testEnviro.snow):
				return True
			else:
				return False
		if (self.query_node == "cloudy"):
			if(self.cloudy == testEnviro.cloudy):
				return True
			else:
				return False
		if (self.query_node == "exams"):
			if(self.exams == testEnviro.exams):
				return True
			else:
				return False
		if (self.query_node == "stress"):
			if(self.stress == testEnviro.stress):
				return True
			else:
				return False


# Humidity helper function.
def humidityRandomChance():
	choice = random.random()
	if(choice < .2 ):
		return "low"
	elif(choice > .2 and choice < .7):
		return "medium"
	elif(choice > .7):
		return "high"
	
# Temprature helper function.
def tempRandomChance():
	choice = random.random()
	if(choice < .1 ):
		return "warm"
	elif(choice > .1 and choice < .5):
		return "mild"
	elif(choice > .5):
		return "cold"

# Day helper function.
def dayRandomChance():
	choice = random.random()
	if(choice < .2 ):
		return "weekend"
	elif(choice > .2):
		return "weekday"
		
def calcProb(value):
	choice = random.random()
	
	if(choice <= value):
		return "true"
	else:
		return "false"

# Checks if this is main. Allows storing everything in other files.
if __name__ == "__main__":

	# Create the timer.
	start_time = time.time()

	# Create the argument parser.
	parser = argparse.ArgumentParser(description="Runs rejection sampling on the tree provided for assignment 3.")

	# Add arguments to the parser.
	parser.add_argument("--debug", "-d", help="Print the debug version of the program.", action="store_true")
	parser.add_argument("query_node", help="The query node that will be accepted.", type=str)
	parser.add_argument("iterations", help="Number of iterations to execute.", type = int)
	parser.add_argument("observed_nodes", help="Other nodes that have been observed.", type=str, nargs="*")

	# Parses the arguments.
	args = parser.parse_args()

	#Rounds to compute
	rounds = args.iterations
	
	# Create the environment.
	enviro = Environment()
	
	# Store the query node.
	enviro.setNodeByArg(args.query_node)

	# Verify the query node was set.
	if (enviro.query_node == None):
		print ("\nError: Query node invalid. Stopping sampling.")
		sys.exit()

	# Store the other nodes.
	for i in range(0, len(args.observed_nodes)):
		enviro.setNodeByArg(args.observed_nodes[i])
	
	# Variable for the number of rejected samples.
	rejected_rounds = 0
	success_rounds = 0

	# Begin the rounds.
	for x in range(0, rounds):

		# Create and fill a test environment.
		testEnviro = Environment()
		testEnviro.fillEnvironment()

		if (args.debug):
			print(testEnviro)

		# Reject the environment or accept it depending on nodes.
		if(enviro.reject(testEnviro)):
			rejected_rounds += 1
			continue

		# Check if this was a success.
		if(enviro.checkSuccess(testEnviro)):
			success_rounds += 1

	end_time = time.time()

	# Final print statement.
	print("\nFinal Print:")
	print("\nTotal Samples:", args.iterations)
	print("Non-Rejected Samples:",(args.iterations - rejected_rounds))
	print("Estimated Probability:",success_rounds/(args.iterations - rejected_rounds))
	print("Time Taken:", (end_time - start_time), "seconds")
#end if(__name__...)