# AAH 2016 Group Assignment: Lotte, Ken, Ria

# This file contains:
# Method to run experiments on each heuristic
# Instance generator

# Packages
import random
from MS_heuristics import *

#----------------------------------------------------------------------------------------#
# EXPERIMENTS
# input: heuristic name (GLS, VDS or "???"); instanceList
# output: list of makespans for instance; list of runtimes for each instance
def runHeuristic(heuristic, instanceList):

	# methods to use:
	# GLS
	# VDS
	# ourHeuristic

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