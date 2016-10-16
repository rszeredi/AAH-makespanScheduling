#!/bin/bash

SOURCE="/Users/riaszeredi/Documents/uni/MSc-coursework/2016-Sem2/approximation-algorithms/assessment/groupProject/AAH-makespanScheduling"

if [[ -z "$1" ]] || [[ -z "$2" ]]; then
    echo 'Usage: ./getOptimalSolutions_CP.sh <m> <n>'
    exit 1
else
	m="$1"
	n="$2"
fi
echo m: $m
echo n: $n
TIMELIMIT="300"

# Create output destination
# DEST="${SOURCE}/data/optimal/optimal_m${m}_n${n}.txt"
DEST="${SOURCE}/data/optimal/optimal_uniform_m${m}_n${n}.txt"
echo dest $DEST
echo -n '' > $DEST

# Get all instances
INSTANCES="$(find $SOURCE -name "instance_m${m}_n${n}_*dzn" | sort)"
# INSTANCES = 

for inst in $INSTANCES
do
	tmp="${inst%.dzn}"
	instName="${tmp#*/minizinc/}"
	echo "$instName"

	# CP
	ulimit -t $TIMELIMIT

	# first try CP with GMS UB
	echo "Solving CP 1..."
	mzn-chuffed MS_CP.mzn $inst -D "include_GMS_UB=1;" > sol.txt 2> stats.txt

	if grep -q "makespan" sol.txt; then
		makespan_CP_1=$(grep "makespan" sol.txt | awk '{a=$3;} END {print a;}')

		if grep -q "==========" sol.txt; then
	        status="Optimal"
	        runtime_CP_1=$(grep "search time" stats.txt | awk '{a=$1;} END {print a;}')
		else
			status="Suboptimal"
			runtime_CP_1="$TIMELIMIT"
		fi
	else
		makespan_CP_1="None"
		status="No_sol_found"
		runtime_CP_1="$TIMELIMIT"
	fi
	echo "CP Makespan 1: $makespan_CP_1"

	# if status is No_sol_found or Suboptimal, try CP model without GMS UB
	if [ $status != "Optimal" ]; then
		echo "Solving CP 0..."
		mzn-chuffed MS_CP.mzn $inst -D "include_GMS_UB=0;" > sol.txt 2> stats.txt

		if grep -q "makespan" sol.txt; then
			makespan_CP_0=$(grep "makespan" sol.txt | awk '{a=$3;} END {print a;}')

			if grep -q "==========" sol.txt; then
		        status="Optimal"
		        runtime_CP_0=$(grep "search time" stats.txt | awk '{a=$1;} END {print a;}')
			else
				status="Suboptimal"
				runtime_CP_0="$TIMELIMIT"
			fi
		else
			makespan_CP_0="None"
			status="No_sol_found"
			runtime_CP_0="$TIMELIMIT"
		fi
		echo "CP Makespan 0: $makespan_CP_0"

		# get the better makespan
		if [ "$makespan_CP_1" != "None" ] && [ "$makespan_CP_0" != "None" ]; then
			if [ "$makespan_CP_1" -lt "$makespan_CP_0" ]; then
				makespan_CP=$makespan_CP_1
				runtime_CP=$runtime_CP_1
			else
				makespan_CP=$makespan_CP_0
				runtime_CP=$runtime_CP_0
			fi
		elif [ "$makespan_CP_1" != "None" ]; then
			makespan_CP=$makespan_CP_1
			runtime_CP=$runtime_CP_1
		elif [ "$makespan_CP_0" != "None" ]; then
			makespan_CP=$makespan_CP_0
			runtime_CP=$runtime_CP_0
		else
			makespan_CP="None"
			runtime_CP=$TIMELIMIT
		fi

	else
		makespan_CP=$makespan_CP_1
		runtime_CP=$runtime_CP_1
	fi

	# retrieve GMS value
	GMS=$(grep "GMS" ${inst} | awk '{a=$3;} END {print a;}')
	GMS=${GMS%;} # get rid of ";"
	# retrieve LB value (from sol file)
	LB=$(grep "LB" sol.txt | awk '{a=$2;} END {print a;}')

	# SA
	echo "Running SA..."
	python MS_heuristics.py test-instances/$instName.csv > sol_SA.txt
	makespan_SA=$(grep "Makespan =" sol_SA.txt | awk '{a=$3;} END {print a;}')
	runtime_SA=$(grep "Runtime" sol_SA.txt | awk '{a=$3;} END {print a;}')
	runtime_SA=$(printf "%0.2f" $runtime_SA)
	echo "SA Makespan: $makespan_SA"

	# calculate ratio
	if [ "$makespan_CP" != "None" ]; then
		ratio="$(bc <<< "scale = 4; ${makespan_SA}/${makespan_CP}-1")"
	else
		ratio="None"
	fi

	# append to dest file
	echo "$instName, GMS: $GMS, LB: $LB, CP: ${status}, $makespan_CP, ${runtime_CP} seconds, SA: $makespan_SA, ${runtime_SA} seconds, CP_SA_gap: $ratio" >> $DEST

	echo ""
done
