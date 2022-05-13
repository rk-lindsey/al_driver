#!/bin/bash

# NOTE: If this command fails, edit utilities/local_pydoc.py to call the same
# python path as you use to execute this driver

# NOTE: local_pydoc.py is simply the code located at: 
# https://github.com/python/cpython/blob/2.7/Lib/pydoc.py


cd src

rm -rf pydoc

cp utilities/local_pydoc.py .


for i in `ls *py`; do python2.7 local_pydoc.py -w ${i%*.py}; done

mkdir ../pydoc
mv *html ../pydoc

rm -f local_pydoc.py

browser=`which firefox`
loc=`pwd`

echo "Attempting to open ${loc}/doc/main.html with firefox..."

if [[ $browser == *"no firefox in"* ]] ; then

	echo "Cannot find browser firefox. Exiting"
	exit 0
elif [ ! $browser ] ; then
	
	echo "Cannot find browser firefox. Exiting"
	exit 0	
	
else
	echo "Opening documentation"

	firefox doc/main.html &
fi


