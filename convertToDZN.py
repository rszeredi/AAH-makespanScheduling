import sys, csv, os, glob
from MS_heuristics import getMakespan, findInitialFeasibleSolution_GMS

def convertToDZN(filename):
	outputFile = "./test-instances/minizinc/%s.dzn" %(filename)

	# Read in the input from the csv instance file
	file = open('./test-instances/%s.csv' %filename, 'rb')
	inputInst = list(csv.reader(file))

	# Get the number of machines
	nMachines = int(inputInst[0][0])

	# Get the processing times
	pTime = [ int(inputInst[j+1][0]) for j in range(len(inputInst)-1) ]

	# Get the number of jobs
	nJobs = len(pTime)

	file.close()

	# get GMS makespan
	instanceList = pTime + [nMachines]
	GMS = getMakespan(instanceList,findInitialFeasibleSolution_GMS(instanceList))

	# write to output
	file = open(outputFile, 'wb+')
	file.write('nMachines = %g;\n' %(nMachines))
	file.write('nJobs = %g;\n' %(nJobs))
	file.write('pTime = %s;\n' %(pTime))
	file.write('GMS = %s;\n' %(GMS))

	file.close()

if __name__ == "__main__":
	instances = glob.glob('./test-instances/instance*.csv')
	for i in range(len(instances)):
		instances[i] = instances[i].replace('./test-instances/','')
		instances[i] = instances[i].strip('.csv')

	for filename in instances:
		print filename
		convertToDZN(filename)