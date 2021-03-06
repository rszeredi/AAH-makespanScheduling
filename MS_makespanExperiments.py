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
def runHeuristic(heuristic, instanceList, k, initSolType, debugging):

	# methods to use:
	# GLS
	# VDS
	# ourHeuristic

	makespanList = []
	runtimeList = []

	neighbourhood = 'jump_alt'
	#initSolType = 'random'


	if heuristic == 'GLS': # run the greedy local search
		for instance in instanceList:

			if debugging:
				print("GLS for instance {}:".format(instanceList.index(instance)+1)) # debugging
				print 'k = %s; Neighbourhood: %s; Initial solution type: %s' %(k, neighbourhood, initSolType)

			[x_star, makespan, runtime] = GLS(instance, k,neighbourhood,initSolType)

			if debugging:
				print '\nFinal:', x_star, 'with makespan', makespan

			makespanList.append(makespan)
			runtimeList.append(runtime)

	elif heuristic == 'VDS': # run the variable depth search
		for instance in instanceList:
			[x_star, makespan, runtime] = VDS(instance, k, neighbourhood, initSolType)

			makespanList.append(makespan)
			runtimeList.append(runtime)

	elif heuristic == 'Ours': # run our heuristic
		for instance in instanceList:

			[x_star, makespan, runtime] = ourHeuristic(instance, k, neighbourhood, initSolType)

			makespanList.append(makespan)
			runtimeList.append(runtime)

	return makespanList, runtimeList


#----------------------------------------------------------------------------------------#
# GENERATE INSTANCES

# input: n jobs
# output: 1xn array, dur, of n random durations
def generateRandomDurations(n,dist,seed):
	maxDur = n

	if dist == 'fatTailed':
		# Focus the processing times on very high and very low values
		# Note: max duration must be a 'nice' number (ie divisible by 5 or 10) for fatTailed to work

		# Define the distribution parameters
		kurtosis = 0.01		# sharpness of the peaks (lower means sharper)

		numHighProb = kurtosis*maxDur
		highProb = 0.45/numHighProb
		numLowProb = (1 - 2*kurtosis)*maxDur
		lowProb = 0.1/numLowProb

		# Initialize probability distribution function
		PDF = [lowProb for i in range(maxDur)]

		for i in range(maxDur):
			# Only processing times in the lowest 5% and highest 5% get high probabilities
			if (i < kurtosis*maxDur) or (i >= (1-kurtosis)*maxDur):
				PDF[i]=highProb

		# print sum(PDF)
		dur = [numpy.random.choice(numpy.arange(1,maxDur+1), replace=True, p=PDF) for i in range(n)]

	elif dist == 'uniform':
		# Uniformly distribute the processing times between 1 and the maximum
		dur = [numpy.random.randint(1,maxDur) for i in range(n)]

	return dur

# input: number of jobs n; number of machines m; number of instances to generate
# output: list of lists (the instances)
def generateRandomInstances(n,m,numToGenerate,dist,seed):

	instances = [None for i in range(numToGenerate)]

	if seed:
		numpy.random.seed(0)

	for i in range(numToGenerate):
		dur = generateRandomDurations(n,dist,seed)
		instances[i] = dur+[m]

	return instances

# input: number of jobs n; number of machines m; number of realizations of the instance to read in
# output: list of lists (the instances)
def readStoredInstances(n,m,numToRead,dist,inputDir='test-instances/',filename=False):

	instances = [None for i in range(numToRead)]

	for i in range(numToRead):
		filename = '{}instance_{}_m{}_n{}_{:03}.csv'.format(inputDir,dist,m,n,i+1)

		instances[i] = readInstance(filename)

	return instances


def saveInstances():

	nList=[10,20,30,40,50,60,70,80,90,100]
	mList=[2,4,6,8,10]

	nList = [50,100,500,1000,3000,5000,10000]
	mList = [45,90,450,900,2700,4500,9000]

	nList = [100,200,300,400,500,600,700,800,900,1000]
	mList = [20,40,60,80,100]

	realizations = 20
	dist = 'fatTailed'
	seed = True

	# for (m,n) in zip(mList,nList):
	for m in mList:
		
		for n in nList:
			# Generate instances for each n and m combination
			instanceList = generateRandomInstances(n,m,realizations,dist,seed)

			# Create output files for each realization
			for r in range(realizations):
				instanceOutput = open('test-instances/instance_{}_m{}_n{}_{:03}.csv'.format(dist,m,n,r+1), 'w')

				instanceOutput.write('%s\n' %(instanceList[r][-1])) # store the number of machines

				for i in range(n):
					instanceOutput.write('%s\n' %(instanceList[r][i]))

				instanceOutput.close()

def getvalueforinitialTemperature():

	numpy.random.seed(0)

	nList=[10,20,30,40,50,60,70,80,90,100]
	mList=[2,4,6,8,10]
	realizations = 100
	dist = 'uniform'
	seed = False
	k = 2

	# parameters to play with for initial temperature generation algorithm
	chi0 = 0.8			# desired acceptance probability
	S = 1000			# number of random transitions to generate
	p = 1 				# value in equation (6) in paper
	epsilon = 10**(-3)	# convergence criterion



	initialTempFile = open('data/initialTemp_k=%s_%s_S=1000_chi0=0.8.csv' %(k,realizations), 'w')

	for i in range(len(mList)):
		print '\nExperimentizing with %s machines and...' %(mList[i])

		for j in range(len(nList)):
			print '...%s jobs:'%(nList[j])

			temperaturelist = []

			instanceList = generateRandomInstances(nList[j],mList[i],realizations,dist,seed)
			for l in range(len(instanceList)):
				temp = getInitialTemp(instanceList[l], k, chi0, S, p, epsilon)
				temperaturelist.append(temp)

			avgTemperature = sum(temperaturelist)/realizations
			print '%.4f' %(avgTemperature)

# 			# Store the results
			if j+1 == len(nList):
				initialTempFile.write('%f' % avgTemperature)
			else:
				initialTempFile.write('%f,' % avgTemperature)
		
		initialTempFile.write('\n')


#----------------------------------------------------------------------------------------#
# EXPERIMENTS

def main():

	# Define constants for experiments
	k=2						# number of exchanges
	realizations=5			# number of empirical data points
	dist='fatTailed'			# distribution of processing times
	seed=True				# whether to seed the randomization
	debugging=False			# whether to print solutions
	alg='Ours'				# algorithm to use: 'GLS', 'VDS', or 'Ours'
	initSolType='GMS'		# initial solution to use: 'inputOrder', 'random', or 'GMS'
	inputDir = 'test-instances/'	# define the location of stored test data


	# Define n and m values to run experiments for
	nList=[10,20,30,40,50]
	mList=[2,3,4,5]

	nList=[10,20,30,40,50,60,70,80,90,100]
	mList=[2,4,6,8,10]

	# nList=[15,20,25,30,35,40,45,50]
	# mList=[2,4,6,8,10]

	# nList=[20,25,30,35,40,45]
	# mList=[2]

	# nList = [10,50,100,500,1000,3000,5000]
	# mList = [9,45,90,450,900,2700,4500]

	# nList = [100,200,300,400,500,600,700,800,900,1000]
	# mList = [20,40,60,80,100]
	

	print '\nEXPERIMENTS: %s\n' %(alg)

	print 'k-value:\t\t\t %s' %(k)
	print 'Empirical data points:\t\t %s' %(realizations)
	print 'Seeded randomization:\t\t %s' %(seed)
	print 'Initial solution type:\t\t %s'%(initSolType)
	print 'Processing times distribution:\t %s\n' %(dist)

	print('Number of Machines: {}'.format(mList))
	print('Number of Jobs: {}'.format(nList))

	for m in mList:

		print '\nExperimentizing with %s machines and...' %(m)

		for n in nList:
			print '...%s jobs' %(n)

			# Initialize output files
			if seed:
				makespan = open('data/makespan_%s_%s_seeded_%s_m%s_n%s.csv' %(alg,initSolType,dist,m,n), 'w')
			else:
				makespan = open('data/runtime_%s_%s_noSeed_%s_m%s_n%s.csv' %(alg,initSolType,dist,m,n), 'w')

			if seed:
				# Read in the previously stored data
				instanceList = readStoredInstances(n,m,realizations,dist,inputDir)
			else:
				# Generate random instances for the given n and m
				instanceList = generateRandomInstances(n,m,realizations,dist,False)

			# Run the algorithm on the test instances
			makespanList, runtimeList = runHeuristic(alg,instanceList,k,initSolType,debugging)

			
			GMSmakespanList = [getMakespan(instanceList[r],findInitialFeasibleSolution_GMS(instanceList[r])) for r in range(realizations)]
			# print makespanList
			# print GMSmakespanList

			for r in range(realizations):
				makespan.write('%d,' % makespanList[r])
				makespan.write('%d\n' % GMSmakespanList[r])

			makespan.close()


	print "\nFull results are stored in:"
	print "	data/makespan_%s_%s_seeded_%s_mX_nX.csv" %(alg,initSolType,dist)


if __name__ == "__main__":
	main()
	# getvalueforinitialTemperature()
	# saveInstances()
