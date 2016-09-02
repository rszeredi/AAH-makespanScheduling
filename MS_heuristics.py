# AAH 2016 Group Assignment: Lotte, Ken, Ria

# This file contains:
# Heuristics (GLS, VDS, *our heuristic*)
# All auxiliary functions for heuristics

# FORMATTING:
# instance: 1 array (p1,p2,...,p_n,m)
# solution (x): 1xm list of sets (each entry i is a set of activities to be run on machine i)
# OR might it be easier if x is a 1xn array specifying the machine each job is assigned to?
# -> See below for methods for converting between the two

#----------------------------------------------------------------------------------------#
# HEURISTICS

# input: instance (see above); initial solution (list of sets); k-exchange value
# output: local optimum found from greedy local search; makespan of local optimum;
# runtime (not including calculation of makespan)
def GLS(instance, initSol, k):
	start = time.time()

	# methods to use:
	# findInitialFeasibleSolution
	# findBestNeighbour_jump
	# OR findBestNeighbour_jumpSwap
	# getMakespan

	end = time.time()
	runtime = end - start

	makespan = getMakespan(x_star)

	return x_star, makespan, runtime

# input: instance (see above); initial solution (list of sets); k-exchange value
# output: local optimum found using variable depth search; makespan of local optimum;
# runtime (not including calculation of makespan)
def VDS(instance, initSol, k):
	start = time.time()

	# methods to use:
	# findInitialFeasibleSolution
	# findBestNeighbour_jump
	# OR findBestNeighbour_jumpSwap
	# getMakespan


	end = time.time()
	runtime = end - start

	makespan = getMakespan(x_star)

	return x_star, makespan, runtime

# todo!
# input:
# output: 
def ourHeuristic(instance, initSol, k):
	start = time.time()


	end = time.time()
	runtime = end - start

	makespan = getMakespan(x_star)

	return x_star, makespan, runtime

#----------------------------------------------------------------------------------------#
# AUXILIARY FUNCTIONS FOR HEURISTICS

# input: instance (defined by array of durations and number of machines as last entry)
# output: a feasible solution
def findInitialFeasibleSolution(instance):

	# need to decide how to do this
	# Ideas:
	# Assign all jobs to first machine
	# Assign jobs to different machines in order of input

	return x

# input: a feasible solution x (which format?)
# output: the best feasible solution after performing a k-jump on x
def findBestNeighbour_jump(x, k):
	
	# methods to use:
	# getMakespan

	return x, cost

# input: a feasible solution x (which format?)
# output: the best feasible solution after performing a k-jump-swap on x
def findBestNeighbour_jumpSwap(x, k):

	# methods to use:
	# getMakespan

	# For now, I assume x is in the form x = [1,2,1,2], and do k=1 and ONLY jump.
	
	numMachines = max(x)
	makespan = getMakespan(x)
	cost = [] # cost is a list with sublists [new_makespan,new_x] that stores all jumps.

	for item in range(len(x)): # for all jobs
		for jumps in range(numMachines): # for all machines 
			if jumps+1 != x[item]: # only consider jumps, no loops where a job jumps to the same machine
				x_new = list(x) # make a copy of x
				x_new[item] = jumps+1 # do the jump
				cost.append([getMakespan(x_new),x_new]) # append the new makespan and the new x to cost

	new_cost = min(i[0] for i in cost) # Select the best jump
	
	# print(cost) # print the list of lists to see how it works!

	gain = makespan - new_cost # if the jump results in a gain
	if gain > 0:
		x = [i[1] for i in cost if i[0] == new_cost][0] # set x to new_x

	return x


#----------------------------------------------------------------------------------------#
# MAYBE ATTRIBUTE PROCESSING TIMES TO JOB OBJECT???
#class Job(object):
#    def __init__(self, processing_time,jobIndex):
#    	self.index = jobIndex
#        self.proctime = processing_time

#jobs = {
    # Job with processing time 10
#    "p1": Job(1,10),
#    "p2": Job(2,7),
#    "p3": Job(3,11)
#    }


# input: a feasible solution x (which format?)
# output: the maximum total processing time over all machines
def getMakespan(x):

	makespan = 0
	x = convertSol_toSetsOfJobs(x)

	for sublist in x:
		spanMachine = 0

		for jobIndex in sublist:

			spanMachine += instance[jobIndex-1]

		if spanMachine > makespan:
			makespan = spanMachine

	return makespan






#----------------------------------------------------------------------------------------#
# CONVERTING BETWEEN DIFFERENT VIEWS OF A SOLUTION
# NB: need to be careful with indexing vs. job/machine names


# Eg. x = [[1, 3], [2, 4]]
# to  x_new = [1, 2, 1, 2]
def convertSol_toListOfMachines(x):

	if not all(isinstance(i, list) for i in x):
		return x

	# initialise machine number 0 for each job
	numJobs = max(max(x))
	x_new = []
	for job in range(numJobs):
		x_new.append(0)

	# get the machine of each job
	for machineNumber, machine in enumerate(x):  # machine is the list of jobs
		for job in machine:
			x_new[job-1] = machineNumber+1

	return x_new

# Eg. x = [1, 2, 1, 2]
# to  x_new = [[1, 3], [2, 4]]
def convertSol_toSetsOfJobs(x):

	if all(isinstance(i, list) for i in x):
		return x

	x_new = []

	# initialise empty list for each machine
	numMachines = max(x)
	for machine in range(numMachines):
		x_new.append([])

	# add each job to set of its corresponding machine
	for jobIndex in range(len(x)):
		x_new[x[jobIndex]-1].append(jobIndex+1)

	return x_new

#----------------------------------------------------------------------------------------#


# EXAMPLE OF SUCCESSFUL JUMP

instance = [7,8,4,2,2] # Instance: (p1,p2,p3,p4,m)
print(findBestNeighbour_jumpSwap([2,2,1,2],1))










