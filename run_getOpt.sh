#!/bin/bash

mList="10"
nList="100"

for m in $mList
do
	for n in $nList
	do
		./getOptimalSolutions_CP.sh $m $n
	done
done