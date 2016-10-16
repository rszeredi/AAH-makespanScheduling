import os
from pprint import pprint


def getNumbers(filename):

	worse=0
	same=0
	better=0
	totalInstances=0

	worseGapSum =0

	print filename

	if os.path.isfile(filename):
		print filename
		for line in open(filename):
			line = line.strip()
			parts = line.split(", ")

			gap=parts[8]
			gap = gap.split(": ")
			if gap[1] == '0':
				gap=int(gap[1])
			else:
				gap=float(gap[1])

			# get status
			CP=parts[3]
			CP = CP.split(": ")
			status=CP[1]

			# get ratio
			ratioPart=parts[8]
			ratioPart = ratioPart.split(": ")
			ratio=float(ratioPart[1])

			if status == 'Suboptimal':
				totalInstances += 1
				if gap > 0:
					worse += 1
					worseGapSum += gap
				elif gap == 0:
					same += 1
				else:
					better += 1

	else:
		print "Cannot find instance_count file."

	if worse > 0:
		averageWorseGap = worseGapSum/float(worse)
	else:
		averageWorseGap = None

	return worse, same, better, averageWorseGap

def getMaxGap(filename):

	summ=0
	totalInstances=0
	maxGap=0

	print filename

	if os.path.isfile(filename):
		print filename
		for line in open(filename):
			line = line.strip()
			parts = line.split(", ")

			gap=parts[8]
			gap = gap.split(": ")
			if gap[1] == '0':
				gap=int(gap[1])
			else:
				gap=float(gap[1])

			# get status
			CP=parts[3]
			CP = CP.split(": ")
			status=CP[1]

			# get ratio
			ratioPart=parts[8]
			ratioPart = ratioPart.split(": ")
			ratio=float(ratioPart[1])

			if status == 'Suboptimal' and gap > 0:
				summ += gap
				totalInstances += 1
				if gap > maxGap:
					maxGap = gap

	else:
		print "Cannot find instance_count file."

	if totalInstances > 0:
		ratioAverage = summ/totalInstances
	else:
		ratioAverage = None
	return maxGap

def getOptimalNumber(filename):

	suboptimal = 0
	optimal =0

	if os.path.isfile(filename):
		# print filename
		for line in open(filename):
			line = line.strip()
			parts = line.split(", ")

			gap=parts[8]
			gap = gap.split(": ")
			if gap[1] == '0':
				gap=int(gap[1])
			else:
				gap=float(gap[1])

			# get status
			CP=parts[3]
			CP = CP.split(": ")
			status=CP[1]

			if status == 'Suboptimal' or not status:
				suboptimal += 1
			elif status == 'Optimal':
				optimal += 1

	return optimal, suboptimal



def getOptimalProportion(filename, measureBetterThanOptimal):

	totalInstances=0
	optimalInstances=0
	betterThanOptimalInstances=0
	summ=0

	print filename

	if os.path.isfile(filename):
		print filename
		for line in open(filename):
			line = line.strip()
			parts = line.split(", ")

			gap=parts[8]
			gap = gap.split(": ")
			if gap[1] == '0':
				gap=int(gap[1])
			else:
				gap=float(gap[1])

			# get status
			CP=parts[3]
			CP = CP.split(": ")
			status=CP[1]

			# get ratio
			ratioPart=parts[8]
			ratioPart = ratioPart.split(": ")
			ratio=float(ratioPart[1])

			if status == 'Optimal':
				totalInstances += 1
			else:
				continue

			if gap == 0 and not measureBetterThanOptimal:
				optimalInstances += 1
			elif gap <= 0 and measureBetterThanOptimal:
				betterThanOptimalInstances += 1
			elif status == 'Optimal':
				summ += ratio
		print 'Total:', totalInstances
		print "Summ:", summ

	else:
		print "Cannot find instance_count file."

	if totalInstances > 0 and not measureBetterThanOptimal:
		proportionOptimal = optimalInstances/float(totalInstances)
		proportionOptimal = round(proportionOptimal,2)*100
		ratioAverage = None
	elif totalInstances > 0 and measureBetterThanOptimal:
		proportionBetterThanOptimal = betterThanOptimalInstances/float(totalInstances)
		proportionBetterThanOptimal = round(proportionBetterThanOptimal,2)*100
		ratioAverage=round((summ/totalInstances)*100,2)
	elif not measureBetterThanOptimal:
		proportionOptimal = None
		ratioAverage = None
	else:
		proportionBetterThanOptimal = None
		ratioAverage = None

	print ratioAverage

	# if ratioAverage is not None:
	# 	ratioAverage=round(ratioAverage,3)

	if measureBetterThanOptimal:
		# return proportionBetterThanOptimal
		return ratioAverage
	else:
		# return proportionOptimal
		return ratioAverage

if __name__ == '__main__':
	SOURCE="/Users/riaszeredi/Documents/uni/MSc-coursework/2016-Sem2/approximation-algorithms/assessment/groupProject/AAH-makespanScheduling/data/optimal"

	nList=[10,20,30,40,50,60,70,80,90,100]
	mList=[2,4,6,8,10]

	proportionOptimal = {}

	measureBetterThanOptimal = True

	if measureBetterThanOptimal:
		# output="%s/SA_proportionBetterThanOptimal_table.txt" %(SOURCE)
		output="%s/SA_ratios_table.txt" %(SOURCE)
	else:
		output="%s/SA_proportionOptimal_table.txt" %(SOURCE)

	for m in mList:
		for n in nList:
			filename = "%s/optimal_m%s_n%s.txt" %(SOURCE,m,n)

			proportionOptimal[m,n] = getOptimalProportion(filename,measureBetterThanOptimal)

	pprint(proportionOptimal)

	# write to file
	f = open(output, 'w')

	for m in mList:
		for i, n in enumerate(nList):
			f.write(" %s\t" %(proportionOptimal[m,n]))
			if i != len(nList)-1:
				f.write('&')
		f.write('\\\\ \n')

	# f.close()

	# maxGap = {}
	# for m in mList:
	# 	for n in nList:
	# 		filename = "%s/optimal_m%s_n%s.txt" %(SOURCE,m,n)

	# 		maxGap[m,n] = getMaxGap(filename)

	# pprint(maxGap)
	# print max(maxGap.values())

	# worse = {}
	# same = {}
	# better = {}
	# full = {}
	# averageWorseGap = {}
	# for m in mList:
	# 	for n in nList:
	# 		filename = "%s/optimal_m%s_n%s.txt" %(SOURCE,m,n)
	# 		full[n,m] = []

	# 		worse[n,m], same[n,m], better[n,m], averageWorseGap[n,m] = getNumbers(filename)
	# 		full[n,m].append(worse[n,m])
	# 		full[n,m].append(same[n,m])
	# 		full[n,m].append(better[n,m])


	# print "WORSE"
	# pprint(worse)
	
	# # print "SAME"
	# # pprint(same)
	# # print "BETTER"
	# # pprint(better)
	# print 'worse gap'
	# pprint(averageWorseGap)

	# print sum(worse.values())
	# print sum(same.values())
	# print sum(better.values())

	# # print "FULL"
	# # pprint(full)
	# # print sum([full.values()[i] for i)

	# for key in averageWorseGap.keys():
	# 	if not averageWorseGap[key]:
	# 		averageWorseGap.pop(key, None)

	# pprint(averageWorseGap)
	# print sum(averageWorseGap.values())/len(averageWorseGap.keys())

	# get optimal 

	# optimal = {}
	# suboptimal = {}
	# full = {}


	# for m in mList:
	# 	for n in nList:
	# 		filename = "%s/optimal_m%s_n%s.txt" %(SOURCE,m,n)
	# 		full[n,m] = []

	# 		optimal[n,m], suboptimal[n,m] = getOptimalNumber(filename)
	# 		full[n,m].append(optimal[n,m])
	# 		full[n,m].append(suboptimal[n,m])

	# 		# print full[n,m],
	# 		if optimal[n,m] + suboptimal[n,m] >0:
	# 			proportionOptimal = optimal[n,m]/float(optimal[n,m] + suboptimal[n,m])
	# 		else:
	# 		 proportionOptimal = None
	# 		# print full[n,m],
	# 		print proportionOptimal,
	# 	print ''

	# pprint(full)
