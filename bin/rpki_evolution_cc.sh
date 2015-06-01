#!/bin/bash

CC=$1
YEAR="2014"
DAYS="0101 0201 0301 0401 0501 0601 0701 0801 0901 0910 0920 0922 0924 0925 0927 0928 0930 1001"
RFNAME="./tmp/rpki_evolution_$CC.txt"
#DAYS="0101 0201"

unlink $RFNAME

for d in $DAYS
do
	r=$(./bin/run.sh ./bin/rpki-stats.py -r lacnic -d $YEAR$d -q ./bin/rq_roas_per_cc.py --extra $CC|grep prefixes)
	echo "$YEAR$d|$r" >> $RFNAME
done
