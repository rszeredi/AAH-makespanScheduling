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
from pprint import pprint

#----------------------------------------------------------------------------------------#
# HEURISTICS

# input: instance (see above); initial solution (list of sets); k-exchange value
# output: local optimum found from greedy local search; makespan of local optimum;
# runtime (not including calculation of makespan)
def GLS(instance, k, neighbourhood, initSolType):
	start = time.time()

	# fixed parameters for GLS
	differentSolRequired = False
	numJobs = len(instance)-1 # get the number of jobs from the instance
	jobsToConsider = range(1,numJobs+1) # all jobs (job numbers not indices)

	# generate initial feasible solution
	if initSolType == 'inputOrder':
		# start with a naive assignment of jobs to machines
		x = findInitialFeasibleSolution_inputOrder(instance)
	elif initSolType == 'random':
		# start with a random assignment of jobs to machines
		x = findInitialFeasibleSolution_rand(instance)

	# start with a random assignment of jobs to machines
	# x = findInitialFeasibleSolution_rand(instance)

	print 'Initial solution:', x # debubbing: print initial solution

	# perform the k-exchange until a local minimum is found
	while True:

		# find the best neighbour and store as x_new
		x_new = findBestNeighbour(instance, x, k, neighbourhood, differentSolRequired, jobsToConsider)

		if x_new == x:
			break # no exchange occured therefore we have reached a local minimum
		else:
			# print 'x_new', x_new, getMakespan(instance, x_new) # debugging: print best neighbouring solution
			x = x_new # move to neighbouring feasible solution

	# store best solution found
	x_star = x

	end = time.time()
	runtime = end - start

	makespan = getMakespan(instance, x_star)

	return x_star, makespan, runtime

# input: instance (see above); initial solution (list of sets); k-exchange value
# output: local optimum found using variable depth search; makespan of local optimum;
# runtime (not including calculation of makespan)
def VDS(instance, k, neighbourhood, initSolType):

	# temp:
	debugging = True 

	# start timer
	start = time.time()

	# fixed parameters for GLS
	differentSolRequired = True
	numJobs = len(instance)-1 # get the number of jobs from the instance

	# generate initial feasible solution
	if initSolType == 'inputOrder':
		# start with a naive assignment of jobs to machines
		x = findInitialFeasibleSolution_inputOrder(instance)
	elif initSolType == 'random':
		# start with a random assignment of jobs to machines
		x = findInitialFeasibleSolution_rand(instance)

	print 'Initial solution:', x, 'with makespan', getMakespan(instance, x) # debugging: print initial solution

	# initialise
	improvement = True
	exchange = range(1,numJobs+1) # start with all jobs (job numbers not indices)
	j = 0
	alpha = {}
	alpha[j] = x

	# debugging
	iterNumber=0

	# while the solutions found are still improving
	while improvement:
		iterNumber+=1
		if debugging:
			print '\nITERATION', iterNumber

		# find alpha sequence - find best neighbours while there still remain jobs that haven't been changed
		while exchange:
			j += 1

			# find the best neighbour of alpha[j-1] that differs from alpha[j-1] by at least one 1 from the set 'exchange'
			# ** this is the same as the neighbour with the max gain right?
			alpha[j] = findBestNeighbour(instance, alpha[j-1], k, neighbourhood, differentSolRequired, exchange)

			# find the jobs that were changed
			jobsChanged = []
			for jobIndex in range(numJobs):
				if alpha[j][jobIndex] != alpha[j-1][jobIndex]:
					jobsChanged.append(jobIndex+1)				

			# update the exchange list
			for job in jobsChanged:
				exchange.remove(job)

			# print for debugging
			if debugging:
				print 'j:', j
				print 'Jobs changed:', jobsChanged
				print 'New exchange set:', exchange

		# compute all makespans of final alpha sequence
		makespan = {}
		for i in range(j+1):
			makespan[i] = getMakespan(instance, alpha[i])

		# compute gains between each consecutive alpha pairs
		gain = []
		for i in range(1,j+1):
			gain.append(makespan[0] - makespan[i])

		# find max gain index
		l = gain.index(max(gain))+1

		# print for debugging
		if debugging:
			print 'Final alpha:'
			pprint(alpha, width=100)
			print 'Makespans:', makespan
			print 'Gains:', gain
			print 'Best gain index (of alpha):', l
			print 'Gain value:', gain[l-1]


		# check if gain is positive
		if gain[l-1] > 0:

			# store current best solution
			best = alpha[l]

			# reset alpha dictionary
			alpha = {}

			# update current best solution
			alpha[0] = best

			# reset exchange set to be all jobs
			exchange = range(1,numJobs+1)

			# reset j
			j=0

			if debugging:
				print 'New alpha:', alpha, 'with makespan', getMakespan(instance, alpha[0])

		else:
			# terminate
			print 'No improvement'
			improvement = False

	# get the final best solution
	x_star = alpha[0]

	# stop timer
	end = time.time()
	runtime = end - start

	# calculate makespan of final best solution
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

# input: the input instance; a feasible solution x of the form [1,2,1,2]; number of exchanges k
# output: kNeighbours: dictionary of lists storing the neighbours i-exchanges away, for i in 0,..,k;
#		  kNeighboursCosts: dictionary of lists storing the cost of each neighbour i-exchanges away, for i in 0,..,k
# neighbourhood allows for loops
def getKNeighbours_jump(instance, x, k, jobsToConsider):
	
	numMachines = instance[-1]
	makespan = getMakespan(instance,x)

	# kNeighbours = [[x]]+[[] for i in range(k)] # list of lists storing the neighbours i-exchanges away, for i in 0,..,k
	# kNeighboursCosts = [[makespan]]+[[] for i in range(k)] # list of lists storing the cost of each neighbour i-exchanges away, for i in 0,..,k

	# An example of kNeighboursCosts might be:
	#	[ [20] , 					# k=0 neighbours: cost of each neighbour after zero exchanges, ie cost of starting x
	#	  [13,12,17,18] , 			# k=1 neighbours: cost "			   " 1-exchange away from x 
	#	  [15,10,11,11,10,15]  ]	# k=2 neighbours: cost "			   " 2-exchanges away from x
	# kNeighbours has a similar structure but stores the job assignment instead of costs.	

	# try dictionary for readability:
	kNeighbours = {} # dictionary of lists storing the neighbours i-exchanges away, for i in 0,..,k
	kNeighbours[0] = []
	kNeighbours[0].append(x)

	kNeighboursCosts = {} # dictionary of lists storing the cost of each neighbour i-exchanges away, for i in 0,..,k
	kNeighboursCosts[0] = []
	kNeighboursCosts[0].append(makespan)

	# An example of kNeighboursCosts might be:
	#	{0: [20] , 				# k=0 neighbours: cost of each neighbour after zero exchanges, ie cost of starting x
	#	 1: [13,12,17,18] , 		# k=1 neighbours: cost "			   " 1-exchange away from x 
	#	 2: [15,10,11,11,10,15]  }	# k=2 neighbours: cost "			   " 2-exchanges away from x
	# kNeighbours has a similar structure but stores the job assignment instead of costs.	
	
	for kDepth in range(k): # repeat exchange k times

		# initialise list in dictionaries
		kNeighbours[kDepth+1] = []
		kNeighboursCosts[kDepth+1] = []

		for neighbour in kNeighbours[kDepth]: # for each neighbour kDepth exchanges away from x
			# for job in range(len(x)): # for all jobs
			for job in jobsToConsider: # eg. in VDS, the jobs that have not yet been changed)
				for jump in range(numMachines): # for all machines 
					x_new = list(neighbour) # make a copy of the current neighbour
					x_new[job-1] = jump+1 # do the jump
					
					kNeighbours[kDepth+1].append(x_new) # append the neighbour to the set of neighbours k-exchanges away
					kNeighboursCosts[kDepth+1].append(getMakespan(instance,x_new)) # store the neighbour's cost
	
	# Debugging:
	# pprint(kNeighbours)
	# pprint(kNeighboursCosts)

	return kNeighbours, kNeighboursCosts

# input: the input instance; a feasible solution x of the form [1,2,1,2]; number of exchanges k; Boolean variable specfiying whether a different solution is required
# output: the best feasible solution in the k-exchange neighbourhood
# NB: could return the input instance if differentRequired is False
def findBestNeighbour(instance, x, k, neighbourhood, differentSolRequired, jobsToConsider):
	
	# debugging
	print 'Finding best neighbour of', x
	
	# get the neighbourhood dictionaries
	if neighbourhood == 'jump':
		kNeighbours, kNeighboursCosts = getKNeighbours_jump(instance,x,k, jobsToConsider)
	elif neighbourhood == 'swap':
		kNeighbours, kNeighboursCosts = getKNeighbours_swap(instance,x,k, jobsToConsider)

	# search for the lowest cost among all neighbours exactly k-exchanges away
	new_cost = min(i for i in kNeighboursCosts[k])
	bestNeighbourIndex = kNeighboursCosts[k].index(new_cost) # store the best neighbour's index

	x_new = kNeighbours[k][bestNeighbourIndex] # set x to the best neighbour
	
	if differentSolRequired and x == x_new:

		# get the neighbours that are not equal to the original solution
		neighbours_excl_identity = [x for x in kNeighbours[k] if kNeighbours[k][kNeighbours[k].index(x)] != x_new]
		# get the costs of those neighbours
		neighbours_excl_identity_costs = [cost for cost in kNeighboursCosts[k] if kNeighbours[k][kNeighboursCosts[k].index(cost)] != x_new]

		# re-calculate best neighbour from resulting list
		# NB: may be a different soltion with the same makespan
		new_cost = min(i for i in neighbours_excl_identity_costs)
		# store the best neighbour's index
		bestNeighbourIndex = neighbours_excl_identity_costs.index(new_cost)
		# update the best neighbour
		x_new = neighbours_excl_identity[bestNeighbourIndex]

	return x_new

# input: the input instance; a feasible solution x (which format?); number of exchanges k
# output: the best feasible solution after performing a k-cycle on x
def findBestNeighbour_cycle(instance, x, k):
	
	# x of the form [1,2,1,2] and perform a k-cycle.

	# performs k cycle, and only stores neighbours of k cycle, not 1,2,...,k swap.
	# The cycle exchange is only well defined for k>=2. 
	# For k=2 the cycle exchange is simply a 1-swap.

	numMachines = instance[-1]
	makespan = getMakespan(instance,x)

	kNeighbours = [[x]]+[[]] # list of lists storing x and the neighbours exactly k-exchanges away]
	kNeighboursCosts = [[makespan]]+[[]] # list of lists storing the cost of x and of each neighbour exactly k-exchanges away

	for jobs in list(itertools.combinations(range(len(x)),k)): # for all combinations of k jobs to exchange
		x_new = list(x) # make a copy of x
		for cycle in list(itertools.permutations(jobs,k)): # for all permutations of these k jobs, don't need to check whether you consider same job again? I think this does not matter.
			
			# Test if cycle is in fact a k-cycle. 
			isCycle = True
			for i in range(len(cycle)):
				if jobs[i] == cycle[i]: # cycle is not a k-cycle if job i is looped with itself
					isCycle = False
					break
				if x[jobs[i]] == x[cycle[i]]: # cycle is not a k-cycle if swapping jobs on the same machine
					isCycle = False
					break
			if isCycle == False:
				continue # if cycle is not a k-cycle, then consider next permutation

			for i in range(len(cycle)):
				x_new[jobs[i]] = x[cycle[i]] # perform the k-cycle
				
			if x_new not in kNeighbours[1]: # only add the new neighbour if it isn't already in k-neighbourhood
				kNeighbours[1].append(list(x_new)) # append the neighbour to the set of neighbours k-exchanges away
 				kNeighboursCosts[1].append(getMakespan(instance,x_new)) # store the neighbour's cost

	# Debugging:
	#print(kNeighbours)
	#print(kNeighboursCosts)

	# search for the lowest cost among all neighbours exactly k-exchanges away
	try: # Test if there are any k-cycle neighbours of x
		new_cost = min(i for i in kNeighboursCosts[1])
	except ValueError:
		return x

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

def main():
	# test instance
	instance = [7,8,4,2,2] # Instance: (p1,p2,p3,p4,m)
	# initSol = [1,2,1,2]

	# NEIGHBOURHOOD TESTING
	# print '\nNeighbourhood Testing'

	# EXAMPLE OF SUCCESSFUL SWAP	
	# bestNeighbour = findBestNeighbour_swap(instance,initSol,2)
	# print bestNeighbour, getMakespan(instance,bestNeighbour)

	# # EXAMPLE OF SUCCESSFUL JUMP	
	# jobsToConsider = [1,2,3,4] # job NUMBERS - NOT indices
	# initSol = [1,1,2,1]
	# k = 3
	# neighbourhood = 'jump'
	# differentSolRequired = True

	# bestNeighbour = findBestNeighbour(instance, initSol, k, neighbourhood, differentSolRequired, jobsToConsider)
	
	# print 'Best neighbour:', bestNeighbour
	# print 'Makespan:', getMakespan(instance,bestNeighbour)


	# GLS TESTING
	# k = 1
	# neighbourhood = 'jump'
	# print '\nGLS Testing'
	# print 'k =', k, '; instance:', instance, '; neighbourhood:', neighbourhood

	# x_star, makespan, runtime = GLS(instance, k, neighbourhood)

	# print 'Final:', x_star, 'with makespan', makespan

	# VDS TESTING
	instance = [9,7,4,3,2,2,2,1,3]
	k = 2
	neighbourhood = 'jump'
	initSolType = 'random'

	print '\nVDS Testing'
	print 'Instance:', instance
	print 'k = %s; Neighbourhood: %s; Initial solution type: %s' %(k, neighbourhood, initSolType)

	x_star, makespan, runtime = VDS(instance, k, neighbourhood, initSolType)

	print '\nFinal:', x_star, 'with makespan', makespan


if __name__ == "__main__":
	main()
