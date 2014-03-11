##################################################################
# ipv4 runout models
# (c) carlos@lacnic.net 2014-03-05
##################################################################
from numpy import *
time_horizon = 200

# fetch data
print "Fetching IPv4 allocation data... ",
time_series = array([1,2,3,4,5,6,7,8,9,10])
freeipv4_series = array([1000,900,850,820,750,720,730,700,650,640])
print "done!"


# load into numpy arrays
# --<may not be neccesary-->

# run models

model_poly = polyfit(time_series, freeipv4_series, 3)
print "Polynomial fitted sucessfully, result is: %s" % (model_poly)

# print out expected runout dates
# find the next zero-crossing
time_series_future = xrange(11,time_horizon)
for t in time_series_future:
    freeipv4_estimated = polyval(model_poly, t)
    print "t: %s, free_ipv4: %s" % (t, freeipv4_estimated)
    if freeipv4_estimated < 0:
        break

if t < time_horizon:
    print "Delta T for IPv4 runout is %s" % (t)
else:
    print "Delta T could not be identified, check for numeric instability"

# end for


##################################################################
