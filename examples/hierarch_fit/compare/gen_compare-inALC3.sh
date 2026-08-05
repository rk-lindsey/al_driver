#!/bin/bash

paste b-labeled_comb.txt force.txt | awk '{if(($1!~"+1")&&($1!~"s")){print($2,$3)}}' > compare_bF.txt
paste b-labeled_comb.txt force.txt | awk '{if(($1~"+1")){print($2,$3)}}' > compare_bE.txt
paste b-labeled_comb.txt force.txt | awk '{if(($1~"s")){print($2,$3)}}' > compare_bS.txt
