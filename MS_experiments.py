# AAH 2016 Group Assignment: Lotte, Ken, Ria

# This file contains:
# Method to run experiments on each heuristic
# Instance generator

# Packages
import random, time
from MS_heuristics import *

#----------------------------------------------------------------------------------------#
# EXPERIMENTS
# input: heuristic name (GLS, VDS or "???"); instanceList
# output: list of makespans for instance; list of runtimes for each instance
def runHeuristic(heuristic, instanceList, k):

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

			print("GLS for instance {}:".format(instanceList.index(instance)+1)) # debugging
			print 'k = %s; Neighbourhood: %s; Initial solution type: %s' %(k, neighbourhood, initSolType)

			[x_star, makespan, runtime] = GLS(instance, k,neighbourhood,initSolType)

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
def generateRandomDurations(n):
	maxDur = 20 # what val to use here?

	return dur

# input: number of jobs n; number of machines m; number of instances to generate
# output: list of lists (the instances)
def generateRandomInstances(n,m,numToGenerate):

	# methods to use:
	# generateRandomDurations

	return instances


#----------------------------------------------------------------------------------------#
# TESTING

# sample input instances
instanceList = [[7,8,3,2,2],[9,7,4,3,2,2,2,1,3],[3,6,8,2,7,13,5,14,2,3,2,6,5]]

# run the first heuristic (GLS) on the instance list with k=1
[makespanList, runtimeList] = runHeuristic(1,instanceList,2)
print("makespan values: {}\nrunning times: {}".format(makespanList, runtimeList))
