#!/bin/bash


# Notes: WHEN RUN WITH: srun -N 1 -n 1 ${TASK}, $EXEC should NOT be compiled with MPI support
#        i.e. use g++ instead of mpicxx

# Expects a xyzlist.dat file to be generated in the working directory

NPROC=$1 	# This job is always run serially for now
EXEC=$2	 	# EXEC=/p/lscratchrza/rlindsey/RC4B_RAG/11-12-18/SVN_SRC-11-12-18/chimes_md
BASE=$3  	# ../../../../DUMB_FF/run_md.base
SUBJOB=$4

# Read the list of configurations.. format is: <natoms> <n_c> <n_o> </path/to/xyz/file>

readarray -t REPO_FILES < xyzlist.dat

rm -f xyzlist.energies

echo "Subjob $SUBJOB is running, with ${#REPO_FILES[@]} loop tasks"

rm -f md_statistics.out

for (( i=0; i<${#REPO_FILES[@]}; i++))
do
	NO_A=`echo ${REPO_FILES[$i]} | awk '{print $1}'`
	XYZF=`echo ${REPO_FILES[$i]} | awk '{print $NF}'`
	
	awk -v infile="../${XYZF}" '/CRDFILE/{print;getline;$0=infile}{print}' $BASE > run_md.in
	
	echo "	...job $i, subjob $SUBJOB	(../${XYZF})"

	${EXEC} run_md.in | tail -n 20 # > /dev/null

	awk -v natoms="${NO_A}" '{if(NR==3){print ($5*natoms); exit}}' md_statistics.out >> xyzlist.energies
	rm -f md_statistics.out
	
	echo ""
	
done

paste xyzlist.dat xyzlist.energies | awk '{print $NF/$1}' > xyzlist.energies_normed

exit 0

