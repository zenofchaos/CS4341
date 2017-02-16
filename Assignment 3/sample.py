# Imports
import argparse
import sys

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


# Checks if this is main. Allows storing everything in other files.
if __name__ == "__main__":

	# Create the argument parser.
	parser = argparse.ArgumentParser(description="Runs rejection sampling on the tree provided for assignment 3.")

	# Add arguments to the parser.
	parser.add_argument("--debug", "-d", help="Print the debug version of the program.", action="store_true")
	parser.add_argument("query_node", help="The query node that will be accepted.", type=str)
	parser.add_argument("iterations", help="Number of iterations to execute.", type = int)
	parser.add_argument("observed_nodes", help="Other nodes that have been observed.", type=str, nargs="*")

	# Parses the arguments.
	args = parser.parse_args()

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

	# Print the environment if debugging.
	if (args.debug):
		print(enviro)

#end if(__name__...)