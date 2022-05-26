#!/bin/bash

# Usage: ./paste2file input1 input2 output

input1=$1
input2=$2


if   [ $4 == "energy" ] ; then  
	paste $input1 $input2  | awk '{if($1~"+1"){print}}' > $3
elif [ $4 == "stress" ] ; then
	paste $input1 $input2  | awk '{if($1~"s_"){print}}' > $3
else
	paste $input1 $input2  | awk '{if(($1!~"+1")&&($1!~"s_")){print}}' > $3 
fi
