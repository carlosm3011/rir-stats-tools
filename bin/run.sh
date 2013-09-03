#!/bin/bash

PYTHON="/opt/local/bin/python2.7"
export SRCHOME="/Users/marcelo/Development/checkouts/cm2c-rir-stats-tools/"

####
export PYTHONPATH="$SRCHOME/lib:$SRCHOME/lib:$PYTHONPATH"

$PYTHON $*
