import os
from pprint import pprint

def getOptimalProportion(filename):

	totalInstances=0
	optimalInstances=0

	if os.path.isfile(filename):
		for line in open(filename):
			line = line.strip()
			parts = line.split(", ")

			gap=parts[8]
			gap = gap.split(": ")
			gap=float(gap[1])

			totalInstances += 1

			if gap == 0:
				optimalInstances += 1
	else:
		print "Cannot find instance_count file."

	if totalInstances > 0:
		proportionOptimal = optimalInstances/float(totalInstances)
		proportionOptimal = round(proportionOptimal,2)*100
	else:
		proportionOptimal = None
	return proportionOptimal

if __name__ == '__main__':
	SOURCE="/Users/riaszeredi/Documents/uni/MSc-coursework/2016-Sem2/approximation-algorithms/assessment/groupProject/AAH-makespanScheduling/data/optimal"

	nList=[10,20,30,40,50,60,70,80,90,100]
	mList=[2,4,6,8,10]

	proportionOptimal = {}

	output="%s/SA_proportionOptimal_table.txt" %(SOURCE)

	for m in mList:
		for n in nList:
			filename = "%s/optimal_m%s_n%s.txt" %(SOURCE,m,n)

			proportionOptimal[m,n] = getOptimalProportion(filename)

	pprint(proportionOptimal)

	# write to file
	f = open(output, 'w')

	for m in mList:
		for i, n in enumerate(nList):
			f.write(" %s\t" %(proportionOptimal[m,n]))
			if i != len(nList)-1:
				f.write('&')
		f.write('\\\\ \n')

	f.close()
