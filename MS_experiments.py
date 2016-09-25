# AAH 2016 Group Assignment: Lotte, Ken, Ria

# This file contains:
# Method to run experiments on each heuristic
# Instance generator

# Packages
from __future__ import division
import random, time, numpy, csv
from MS_heuristics import *

#----------------------------------------------------------------------------------------#
# EXPERIMENTS
# input: heuristic name (GLS, VDS or "???"); instanceList
# output: list of makespans for instance; list of runtimes for each instance
def runHeuristic(heuristic, instanceList, k, debugging):

	# methods to use:
	# GLS
	# VDS
	# ourHeuristic

	makespanList = []
	runtimeList = []

	neighbourhood = 'jump'
	initSolType = 'random'


	if heuristic == 1: # run the greedy local search
		for instance in instanceList:

			if debugging:
				print("GLS for instance {}:".format(instanceList.index(instance)+1)) # debugging
				print 'k = %s; Neighbourhood: %s; Initial solution type: %s' %(k, neighbourhood, initSolType)

			[x_star, makespan, runtime] = GLS(instance, k,neighbourhood,initSolType)

			if debugging:
				print '\nFinal:', x_star, 'with makespan', makespan

			makespanList.append(makespan)
			runtimeList.append(runtime)

	elif heuristic == 2: # run the variable depth search
		for instance in instanceList:
			[x_star, makespan, runtime] = VDS(instance, k,neighbourhood,initSolType)

			makespanList.append(makespan)
			runtimeList.append(runtime)

	elif heuristic == 3: # run our heuristic
		for instance in instanceList:
			[x_star, makespan, runtime] = ourHeuristic(instance, k)

			makespanList.append(makespan)
			runtimeList.append(runtime)

	return makespanList, runtimeList


#----------------------------------------------------------------------------------------#
# GENERATE INSTANCES

# input: n jobs
# output: 1xn array, dur, of n random durations
def generateRandomDurations(n,worstCase,seed):
	maxDur = 100 # what val to use here?

	if seed:
		# To be completed
		numpy.random.seed(0)

	if worstCase:
		# To be completed
		dur = [numpy.random.randint(1,maxDur) for i in range(n)]
	else:
		dur = [numpy.random.randint(1,maxDur) for i in range(n)]

	return dur

# input: number of jobs n; number of machines m; number of instances to generate
# output: list of lists (the instances)
def generateRandomInstances(n,m,numToGenerate,worstCase,seed):

	instances = [None for i in range(numToGenerate)]

	for i in range(numToGenerate):
		dur = generateRandomDurations(n,worstCase,seed)
		instances[i] = dur+[m]

	return instances


#----------------------------------------------------------------------------------------#
# EXPERIMENTS

def main():
	# sample input instances
	#instanceList = [[7,8,3,2,2],[9,7,4,3,2,2,2,1,3],[3,6,8,2,7,13,5,14,2,3,2,6,5]]

	# run the first heuristic (GLS) on the instance list with k=1
	#[makespanList, runtimeList] = runHeuristic(1,instanceList,k)
	#print("makespan values: {}\nrunning times: {}".format(makespanList, runtimeList))


	# Define constants for experiments
	k=1						# number of exchanges
	realizations=20			# number of empirical data points
	worstCase=False			# whether to test the worst case for processing times
	seed=False				# whether to seed the randomization
	debugging=False			# whether to print solutions


	# Define n and m values to run experiments for
	nList=[10,20,30,40,50]
	mList=[2,3,4,5]

	nList=[10,20,30,40,50,60,70,80,90,100]
	mList=[2,4,6,8,10]


	# Initialize output files
	makespanError = open('data/makespanError_k%s.csv' %(k), 'w')
	runtime = open('data/runtime_k%s.csv' %(k), 'w')
	

	print '\nEXPERIMENTS'
	print 'k=%s with %s empirical data points' %(k,realizations),

	if seed: print('(seeded) and')
	else: print('(unseeded) and')

	if worstCase: print 'fat-tailed distribution of processing times.'
	else: print 'uniformly distributed processing times.'

	for i in range(len(mList)):
		print '\nExperimentizing with %s machines and...' %(mList[i])

		for j in range(len(nList)):
			print '...%s jobs' %(nList[j])
			# Generate random instances for the given n and m
			instanceList = generateRandomInstances(nList[j],mList[i],realizations,worstCase,seed)

			# Run the GLS on the test instances
			makespanList, runtimeList = runHeuristic(1,instanceList,k,debugging)

			# Find a lower bound on each instance's makespan
			makespanLBList = findMakespanLowerBound(instanceList)

			# Calculate the percentage that each makespan is above its lower bound
			makespanErrorList = [(ms/lb-1)*100 for ms, lb in zip(makespanList,makespanLBList)]

			# Find the mean of the results
			avgMakespanError = sum(makespanErrorList)/realizations
			avgRuntime = sum(runtimeList)/realizations

			# Store the results
			if j+1 == len(nList):
				makespanError.write('%f' % avgMakespanError)
				runtime.write('%f' % avgRuntime)
			else:
				makespanError.write('%f,' % avgMakespanError)
				runtime.write('%f,' % avgRuntime)

		makespanError.write('\n')
		runtime.write('\n')


	makespanError.close()
	runtime.close()
	print "\nResults are stored in 'makespan_k%s.csv' and 'runtime_k%s.csv'\n" %(k,k)

if __name__ == "__main__":
	main()
