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
	chooseBestNeighbour = 0 # choose the first of the best neighbours

	# generate initial feasible solution
	if initSolType == 'inputOrder':
		# start with a naive assignment of jobs to machines
		x = findInitialFeasibleSolution_inputOrder(instance)
	elif initSolType == 'random':
		# start with a random assignment of jobs to machines
		x = findInitialFeasibleSolution_rand(instance)

	print 'Initial solution:', x # debugging: print initial solution

	# perform the k-exchange until a local minimum is found
	while True:

		# find the best neighbour and store as x_new
		bestNeighbourList = findBestNeighbour(instance, x, k, neighbourhood, differentSolRequired, jobsToConsider)
		x_new = bestNeighbourList[chooseBestNeighbour]

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
	debugging = False 

	# start timer
	start = time.time()

	# fixed parameters for GLS
	differentSolRequired = True
	numJobs = len(instance)-1 # get the number of jobs from the instance
	chooseBestNeighbour = 0 # choose the first of the best neighbours

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
			bestNeighbourList = findBestNeighbour(instance, alpha[j-1], k, neighbourhood, differentSolRequired, exchange)
			alpha[j] = bestNeighbourList[chooseBestNeighbour]

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
				print 'Best neighbours:', bestNeighbourList
				print 'Best neighbour chosen:', alpha[j]
				print 'Jobs changed:', jobsChanged
				print 'New exchange set:', exchange, '\n'

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
			print 'No improvement.'
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

	random.seed(100)

	# randomly assigns jobs to machines

	numJobs = len(instance)-1
	numMachines = instance[-1]

	x = [random.randint(1,numMachines) for i in range(numJobs)]

	return x

# input: the input instance;
#		 a feasible solution x of the form [1,2,1,2];
#		 number of exchanges k;
#		 a list of jobs (NUMBERS, not indices) that are allowed to jump
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
			
# alternative method for jump neighbourhood
# method only stores the current best	
# input: the input instance;
#		 a feasible solution x of the form [1,2,1,2];
#		 number of exchanges k;
#		 Boolean variable specfiying whether a different solution is required;
#		 a list of jobs (NUMBERS, not indices) that are allowed to jump
# output: the list of best feasible solutions in the k-exchange neighbourhood; or a set of the best feasible solutions (**do we need this??)
# NB: could return the input instance if differentRequired is False
def findBestNeighbour_jump_alt(instance, x, k, differentSolRequired, jobsToConsider):
		
	# temp
	createSetOfBestNeighbours = True # keeps ALL best neighbours, not just the first one found - might be useful? dunnooo
	debugging = False

	# get the number of machines
	numMachines = instance[-1]

	# set the best so far to the worst possible (sum of all processing times)
	bestNeighbourSoFar_cost = sum(instance[:-1]) # set the best so far to the worst possible (sum of all processing times; note that the last entry of instance is the number of machines)
	bestNeighbourSoFar = []

	if debugging:
		print 'Initial best neighbour cost:', bestNeighbourSoFar_cost, '\n'

	# iterate through each possible (unordered) combination of k jobs (in the set jobsToConsider) with repetition allowed
	for setOfJobsToJump in itertools.combinations_with_replacement(jobsToConsider, k):
		if debugging:
			print 'original x:', x
			print 'jobs to jump:', setOfJobsToJump

		# iterate through each possible ordered combination of k machines (in the set of all machines)
		# this represents which machines the jobs in setOfJobsToJump are to jump to 
		for machinesToJumpTo in itertools.product(range(1,numMachines+1), repeat = k):

			# make a copy of the current neighbour
			x_new = x[:]

			# jump the jobs and store in x_new
			for i, job in enumerate(setOfJobsToJump):
				x_new[job-1] = machinesToJumpTo[i] # do the jump
			# compute the new makespan
			makespan_new = getMakespan(instance, x_new)

			if debugging:
				print 'machines to jump to:', machinesToJumpTo
				print 'x_new =', x_new, 'with makespan', makespan_new	

			# first check whether we require a different solution and if x_new is the same as the initial solution
			# if both are true then we do nothing

			if (differentSolRequired and x_new == x):
				if debugging:
					print 'x_new is the same as the initial solution and we require a different solution.'
					print 'Action: no update to best neighbour.'
			else:

				# if the new makespan is strictly better than the current, update the best neighbour
				if makespan_new	< bestNeighbourSoFar_cost:

					# empty the current bestNeighbourSet and add x_new
					bestNeighbourSoFar = []
					bestNeighbourSoFar.append(x_new)

					# update the best makespan found so far
					bestNeighbourSoFar_cost = makespan_new

					if debugging:
						print 'Cost improvement.'
						print 'Action: Best so far updated.'
					
				# if x_new has the same makespan, but we are collecting all best solutions
				elif createSetOfBestNeighbours and makespan_new == bestNeighbourSoFar_cost:

					# add this neighbour to the set of best found so far
					bestNeighbourSoFar.append(x_new)

					if debugging:
						print 'Same as current makespan.'
						print 'Action: add to the best neighbour set.'
				else:
					if debugging:
						print 'No cost improvement.'
						print 'Action: no update to best neighbour.'

		if debugging:
			print ''

	# remove duplicate neighbours, if any
	bestNeighbourSoFar.sort()
	bestNeighbourSoFar = list(bestNeighbourSoFar for bestNeighbourSoFar,_ in itertools.groupby(bestNeighbourSoFar))

	return bestNeighbourSoFar

# input: the input instance;
#		 a feasible solution x of the form [1,2,1,2];
#		 number of exchanges k;
#		 a string specifying the neighbourhood to use (eg. 'jump', 'jump_alt', 'swap');
#		 Boolean variable specfiying whether a different solution is required; a list of jobs that are allowed to jump
# output: the best feasible solution in the k-exchange neighbourhood
# NB: could return the input instance if differentRequired is False
def findBestNeighbour(instance, x, k, neighbourhood, differentSolRequired, jobsToConsider):
	
	# initialise the best neighbour list
	bestNeighbourList = []

	# debugging
	debugging = False
	if debugging:
		print 'Finding the best neighbours of', x, 'with makespan', getMakespan(instance, x)
	
	# get the neighbourhood dictionaries (compute best neighbour in the case of jump_alt neighbourhood)
	if neighbourhood == 'jump':
		kNeighbours, kNeighboursCosts = getKNeighbours_jump(instance,x,k, jobsToConsider)
	elif neighbourhood == 'swap':
		kNeighbours, kNeighboursCosts = getKNeighbours_swap(instance,x,k, jobsToConsider)
	elif neighbourhood == 'jump_alt':
		bestNeighbourList = findBestNeighbour_jump_alt(instance, x, k, differentSolRequired, jobsToConsider)
		# findBestNeighbour_jump_alt finds best neighbour straight away, so exit
		return bestNeighbourList

	# search for the lowest cost among all neighbours exactly k-exchanges away
	min_cost = min(i for i in kNeighboursCosts[k])
	# get the indices of all neighbours with this cost
	bestNeighbourIndices = [index for index, element in enumerate(kNeighboursCosts[k]) if min_cost == element]

	# append each solution with the minimum makespan to the best neighbour list
	for index in bestNeighbourIndices:
		bestNeighbourList.append(kNeighbours[k][index])

	# remove duplicates, if any
	bestNeighbourList.sort()
	bestNeighbourList = list(bestNeighbourList for bestNeighbourList,_ in itertools.groupby(bestNeighbourList))
	
	# check whether we require a different solution and if there is only one element in the best neighbour list and this element is the same as the initial solution
	if differentSolRequired and len(bestNeighbourList) == 1 and x == bestNeighbourList[0]:

		# empty the best neighbour list
		bestNeighbourList = []

		# get indices of the elements that were transformed to the original x
		nonIdentityIndices = [index for index, element in enumerate(kNeighbours[k]) if element != x]

		# get the neighbours that are not equal to the original solution
		neighbours_excl_identity = []
		for index in nonIdentityIndices:
			neighbours_excl_identity.append(kNeighbours[k][index])

		# get the costs of those neighbours
		neighbours_excl_identity_costs = []
		for index in nonIdentityIndices:
			neighbours_excl_identity_costs.append(kNeighboursCosts[k][index])

		# find the best makespan in resulting list
		min_cost = min(neighbours_excl_identity_costs)

		# get the indices of all neighbours with this new min cost
		bestNeighbourIndices = [index for index, element in enumerate(kNeighboursCosts[k]) if min_cost == element]

		# append each solution with the minimum makespan to the best neighbour list
		for index in bestNeighbourIndices:
			bestNeighbourList.append(kNeighbours[k][index])

		# remove duplicates, if any
		bestNeighbourList.sort()
		bestNeighbourList = list(bestNeighbourList for bestNeighbourList,_ in itertools.groupby(bestNeighbourList))

	elif differentSolRequired and len(bestNeighbourList) > 1 and x in bestNeighbourList:

		# remove the initial solution
		bestNeighbourList.remove(x)

	return bestNeighbourList


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

	test = {}
	test['jump'] = False
	test['jump_alt'] = False
	test['GLS'] = True
	test['VDS'] = True

	# test instance
	instance = [7,8,4,2,2] # Instance: (p1,p2,p3,p4,m)
	initSol  = [1,2,2,1]

	instance = [9,7,4,3,2,2,2,1,3]
	initSol  = [1,1,2,1,3,1,3,2]

	instance = [3,6,8,2,7,13,5,14,2,3,2,6,5]
	initSol  = [1,1,2,4,3,1,3,2,5,3,4,1,5]

	numJobs = len(instance)-1

	# PARAMS
	k = 3
	differentSolRequired = True
	jobsToConsider = range(1,numJobs+1) # job NUMBERS - NOT indices

	# NEIGHBOURHOOD TESTING
	print 'NEIGHBOURHOOD TESTING\n'

	# EXAMPLE OF SUCCESSFUL SWAP	
	# bestNeighbour = findBestNeighbour_swap(instance,initSol,2)
	# print bestNeighbour, getMakespan(instance,bestNeighbour)

	# EXAMPLE OF SUCCESSFUL JUMP
	if test['jump']:
		neighbourhood = 'jump'
		print 'Neighbourhood: %s' %(neighbourhood)
		print 'k = %s; instance: %s;' %(k, instance)

		bestNeighbourList = findBestNeighbour(instance, initSol, k, neighbourhood, differentSolRequired, jobsToConsider)
		print 'Best neighbour list:', bestNeighbourList
		print 'Makespan:', getMakespan(instance,bestNeighbourList[0])

		print '\n'

	# JUMP ALTERNATIVE
	if test['jump_alt']:
		neighbourhood = 'jump_alt'
		print 'Neighbourhood: %s' %(neighbourhood)
		print 'k = %s; instance: %s;' %(k, instance)

		bestNeighbourList = findBestNeighbour(instance, initSol, k, neighbourhood, differentSolRequired, jobsToConsider)
		print 'Best neighbour list:', bestNeighbourList
		print 'Makespan:', getMakespan(instance,bestNeighbourList[0])


	# HEURISTIC TESTING
	print 'HEURISTIC TESTING\n'
	k = 1
	neighbourhood = 'jump_alt'
	initSolType = 'random'

	# GLS TESTING
	if test['GLS']:
		print 'GLS Testing'
		print 'Instance:', instance
		print 'k = %s; Neighbourhood: %s; Initial solution type: %s' %(k, neighbourhood, initSolType)

		x_star, makespan, runtime = GLS(instance, k, neighbourhood, initSolType)

		print 'Final:', x_star, 'with makespan', makespan
		print 'Runtime:', runtime, '\n'

	# VDS TESTING
	if test['VDS']:
		print 'VDS Testing'
		print 'Instance:', instance
		print 'k = %s; Neighbourhood: %s; Initial solution type: %s' %(k, neighbourhood, initSolType)

		x_star, makespan, runtime = VDS(instance, k, neighbourhood, initSolType)

		print 'Final:', x_star, 'with makespan', makespan
		print 'Runtime:', runtime, '\n'

if __name__ == "__main__":
	main()
