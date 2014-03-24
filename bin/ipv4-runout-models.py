##################################################################
# ipv4 runout models
# (c) carlos@lacnic.net 2014-03-05
##################################################################
from numpy import *
from datetime import date 
from datetime import timedelta
from time import sleep
import sys
import csv
time_horizon = 250
model_degrees = [2,3,4,5]
reserve_pool_size = pow(2,32-10)
base_date = date(2011,7,22)

# fetch data
print "Fetching IPv4 allocation data... ",
#time_series = array([1,2,3,4,5,6,7,8,9,10])
time_series = array([])
#freeipv4_series = array([1000,900,850,820,750,720,730,700,650,640])
freeipv4_series = array([])
print "done!"


# load into numpy arrays
# --<may not be neccesary-->
with open('tmp/reports_freespace.txt') as csvfile:
	r = csv.reader(csvfile, delimiter='|')
	c = 0
	for row in r:
		#p_time_series = row[3]
		time_series = append(time_series, float(row[0]))
		freeipv4_series = append(freeipv4_series,float(row[1]))
		c = c + 1

print "%s entries loaded." % (c)
# print time_series.shape
# print freeipv4_series.shape


# run models
print "Now running different models:"
print "-- "

for md in model_degrees:
	model_poly = polyfit(time_series, freeipv4_series, md)
	print "Polynomial degree %s fitted sucessfully, result is: %s" % (md, model_poly)

	# print out expected runout dates
	# find the next zero-crossing
	base_t = int(amax(time_series))
	time_series_future = xrange(base_t, base_t + time_horizon)
	for t in time_series_future:
	    freeipv4_estimated = polyval(model_poly, t)
	    print "t: %s, free_ipv4: %s" % (t, freeipv4_estimated),
	    if freeipv4_estimated < reserve_pool_size:
	        break
	    print '\r',
	    sleep(0.01)
	    sys.stdout.flush()

	print " "
	# print "Polynomial degree is %s" % (md)
	if t < base_t + time_horizon - 1:
	    print "Delta T for IPv4 runout is %s" % (t-base_t)
	    p1_date = base_date + timedelta(t)
	    print "Expected phase 1 entry date %s" % (p1_date)
	else:
	    print "Delta T could not be identified, check for numeric instability"

# end for


##################################################################
