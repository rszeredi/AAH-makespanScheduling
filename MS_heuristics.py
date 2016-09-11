# AAH 2016 Group Assignment: Lotte, Ken, Ria

# This file contains:
# Heuristics (GLS, VDS, *our heuristic*)
# All auxiliary functions for heuristics

# FORMATTING:
# instance: 1 array (p1,p2,...,p_n,m)
# solution (x): 1xm list of sets (each entry i is a set of activities to be run on machine i)
# OR might it be easier if x is a 1xn array specifying the machine each job is assigned to?
# -> See below for methods for converting between the two

import random, time
import itertools

#----------------------------------------------------------------------------------------#
# HEURISTICS

# input: instance (see above); initial solution (list of sets); k-exchange value
# output: local optimum found from greedy local search; makespan of local optimum;
# runtime (not including calculation of makespan)
def GLS(instance, k):
	start = time.time()

	# methods to use:
	# findInitialFeasibleSolution
	# findBestNeighbour_jump
	# OR findBestNeighbour_jumpSwap
	# getMakespan

	# start with a naive assignment of jobs to machines
	#x = findInitialFeasibleSolution_inputOrder(instance)

	# start with a random assignment of jobs to machines
	x = findInitialFeasibleSolution_rand(instance)
	#x = [1,1,1,1] # debugging: worst case assignment for simplest instance

	print(x) # debubbing: print initial solution

	# perform the k-exchange until a local minimum is found
	while True:
		x_new = findBestNeighbour_jump(instance, x, k)

		if x_new == x:
			break # no exchange occured therefore we have reached a local minimum
		else:
			print(x_new) # debugging: print best neighbouring solution
			x = x_new # move to neighbouring feasible solution

	x_star = x

	end = time.time()
	runtime = end - start

	makespan = getMakespan(instance, x_star)

	return x_star, makespan, runtime

# input: instance (see above); initial solution (list of sets); k-exchange value
# output: local optimum found using variable depth search; makespan of local optimum;
# runtime (not including calculation of makespan)
def VDS(instance, k):
	start = time.time()

	# methods to use:
	# findInitialFeasibleSolution
	# findBestNeighbour_jump
	# OR findBestNeighbour_jumpSwap
	# getMakespan


	end = time.time()
	runtime = end - start

	makespan = getMakespan(instance, x_star)

	return x_star, makespan, runtime

# todo!
# input:
# output: 
def ourHeuristic(instance, k):
	start = time.time()


	end = time.time()
	runtime = end - start

	makespan = getMakespan(instance, x_star)

	return x_star, makespan, runtime

#----------------------------------------------------------------------------------------#
# AUXILIARY FUNCTIONS FOR HEURISTICS

# input: instance (defined by array of durations and number of machines as last entry)
# output: a feasible solution
def findInitialFeasibleSolution_inputOrder(instance):

	# assigns jobs to machines in the order of the input given
	# eg. instance = (p1, p2, p3, p4, p5, p6, p7, 3) will return x=[1,2,3,1,2,3,1]

	numJobs = len(instance)-1
	numMachines = instance[-1]

	x = [ i%numMachines + 1 for i in range(numJobs)]

	return x

# input: instance (defined by array of durations and number of machines as last entry)
# output: a feasible solution
def findInitialFeasibleSolution_rand(instance):

	# randomly assigns jobs to machines

	numJobs = len(instance)-1
	numMachines = instance[-1]

	x = [random.randint(1,numMachines) for i in range(numJobs)]

	return x

# input: the input instance; a feasible solution x (which format?); number of exchanges k
# output: the best feasible solution after performing a k-jump on x
def findBestNeighbour_jump(instance, x, k):
	
	# x of the form [1,2,1,2] and perform a k-jump.
	
	numMachines = instance[-1]
	makespan = getMakespan(instance,x)

	kNeighbours = [[x]]+[[] for i in range(k)] # list of lists storing the neighbours i-exchanges away, for i in 0,..,k
	kNeighboursCosts = [[makespan]]+[[] for i in range(k)] # list of lists storing the cost of each neighbour i-exchanges away, for i in 0,..,k
	
	# An example of kNeighboursCosts might be:
	#	[ [20] , 					# k=0 neighbours: cost of each neighbour after zero exchanges, ie cost of starting x
	#	  [13,12,17,18] , 			# k=1 neighbours: cost "			   " 1-exchange away from x 
	#	  [15,10,11,11,10,15]  ]	# k=2 neighbours: cost "			   " 2-exchanges away from x
	# kNeighbours has a similar structure but stores the job assignment instead of costs.

	for kDepth in range(k): # repeat exchange k times
		for neighbour in kNeighbours[kDepth]: # for each neighbour kDepth exchanges away from x
			for job in range(len(x)): # for all jobs
				for jump in range(numMachines): # for all machines 
					if jump+1 != neighbour[job]: # only consider jumps, no loops where a job jumps to the same machine
						x_new = list(neighbour) # make a copy of the current neighbour
						x_new[job] = jump+1 # do the jump
						if x_new not in kNeighbours[kDepth+1]: # only add the new neighbour if it isn't already in k-neighbourhood
							kNeighbours[kDepth+1].append(x_new) # append the neighbour to the set of neighbours k-exchanges away
							kNeighboursCosts[kDepth+1].append(getMakespan(instance,x_new)) # store the neighbour's cost

	
	# Debugging:
	print(kNeighbours)
	print(kNeighboursCosts)

	# search for the lowest cost among all neighbours exactly k-exchanges away
	new_cost = min(i for i in kNeighboursCosts[k])
	bestNeighbourIndex = kNeighboursCosts[k].index(new_cost) # store the best neighbour's index

	gain = makespan - new_cost # if the k-exchange results in a gain
	if gain > 0:
		x = kNeighbours[k][bestNeighbourIndex] # set x to the best neighbour

	return x


# input: the input instance; a feasible solution x (which format?); number of exchanges k
# output: the best feasible solution after performing a k-swap on x
def findBestNeighbour_swap(instance, x, k):
	
	# x of the form [1,2,1,2] and perform a k-swap.

	# performs k swap, and only stores neighbours of k swap, not 1,2,...,k swap.
	
	numMachines = instance[-1]
	makespan = getMakespan(instance,x)

	kNeighbours = [[x]]+[[]] # list of lists storing x and the neighbours exactly k-exchanges away]
	kNeighboursCosts = [[makespan]]+[[]] # list of lists storing the cost of x and of each neighbour exactly k-exchanges away
	
	# An example of kNeighboursCosts might be:
	#	[ [20] , 					# k=0 neighbours: cost of each neighbour after zero exchanges, ie cost of starting x
	#	  [13,12,17,18] , 			# k=1 neighbours: cost "			   " 1-exchange away from x 
	#	  [15,10,11,11,10,15]  ]	# k=2 neighbours: cost "			   " 2-exchanges away from x
	# kNeighbours has a similar structure but stores the job assignment instead of costs.

	for jobs in list(itertools.combinations(range(len(x)),k+1)): # for all combinations of k jobs to swap
		x_new = list(x) # make a copy of x
		for swaps in list(itertools.permutations(jobs,k+1)): # for all permutations of these k jobs, don't need to check whether you consider same job again? I think this does not matter.
			for i in range(len(swaps)):
				x_new[i] = x[swaps[i]] # perform the swap

			if x_new not in kNeighbours[1]: # only add the new neighbour if it isn't already in k-neighbourhood
				kNeighbours[1].append(x_new) # append the neighbour to the set of neighbours k-exchanges away
 				kNeighboursCosts[1].append(getMakespan(instance,x_new)) # store the neighbour's cost

	
	# Debugging:
	#print(kNeighbours)
	#print(kNeighboursCosts)

	# search for the lowest cost among all neighbours exactly k-exchanges away
	new_cost = min(i for i in kNeighboursCosts[1])
	bestNeighbourIndex = kNeighboursCosts[1].index(new_cost) # store the best neighbour's index

	gain = makespan - new_cost # if the k-exchange results in a gain
	if gain > 0:
		x = kNeighbours[1][bestNeighbourIndex] # set x to the best neighbour

	return x


# input: the input instance; a feasible solution x (which format?); number of exchanges k
# output: the best feasible solution after performing a k-jump-swap on x
def findBestNeighbour_jumpSwap(instance, x, k):

	# methods to use:
	# getMakespan
	

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


# input: the input instance; a feasible solution x (which format?)
# output: the maximum total processing time over all machines
def getMakespan(instance, x):

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


# EXAMPLE OF SUCCESSFUL SWAP

instance = [7,8,4,2,2] # Instance: (p1,p2,p3,p4,m)
print(findBestNeighbour_swap(instance,[2,2,1,2],2))

#GLS(instance,1)










