#!/bin/bash

#PYTHON="/opt/local/bin/python2.7"
PYTHON="/usr/bin/python"
#export SRCHOME="/Users/marcelo/Development/checkouts/cm2c-rir-stats-tools/"
export SRCHOME=$(pwd)

####
export PYTHONPATH="$SRCHOME/lib:$SRCHOME/lib:$PYTHONPATH"

$PYTHON $*
