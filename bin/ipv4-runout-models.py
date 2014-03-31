##################################################################
# ipv4 runout models
# (c) carlos@lacnic.net 2014-03-05
##################################################################
from numpy import *
from datetime import date 
from datetime import timedelta
from time import sleep
from commons import getfile
import sys
import csv
time_horizon = 500
model_degrees = [2,3,4]
reserve_pool_size = pow(2,32-10)
base_date = date(2011,7,22)

# fetch data
print "Fetching IPv4 allocation data... ",
time_series = array([])
freeipv4_series = array([])
getfile.getfile("http://www.labs.lacnic.net/reports_freespace.txt", "tmp/reports_freespace.txt")
print "done!"


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
runout_offsets = []

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
	    sleep(0.005)
	    sys.stdout.flush()

	print " "
	# print "Polynomial degree is %s" % (md)
	if t < base_t + time_horizon - 1:
	    print "Delta T for IPv4 runout is %s" % (t-base_t)
	    runout_offsets.append(t)
	    p1_date = base_date + timedelta(t)
	    print "Expected phase 1 entry date %s" % (p1_date)
	else:
	    print "Delta T could not be identified, check for numeric instability"

# compute a collated date, averaging previous models
avg_offset = mean(runout_offsets)
stddev_offset = std(runout_offsets)
p1_date_avg = base_date + timedelta(avg_offset)

print " "
print " -- "
print "Averaged date offset: %s" % (avg_offset)
print "StdDev   date offset: %s" % (stddev_offset)
print "Averaged runout date: %s" % (p1_date_avg)

#
print " "
print "Writing HTML widget...",
fo = open ("tmp/lacnic-ipv4runout-widget.html", "w")
fo.write("<html>\n")
fo.write("<head>\n")
fo.write('<link href="http://www2.lacnic.net/lacnic/depletion.css" rel="stylesheet" type="text/css">')
fo.write("</head>\n")
fo.write("<body>\n")
fo.write("<div class='l4runout'>\n")
fo.write("<div id='l4hdr'>LACNIC IPv4 Exhaustion Model</div>\n")
fo.write("<div id='l4addr'>%s</div>\n" % (freeipv4_series[-1])) 
fo.write("<div id='l4dash8'>%.2f</div>\n" % ( float(freeipv4_series[-1]) / pow(2,24) ) ) 
fo.write("<div id='l4date'>%s</div>\n" % ( p1_date_avg ) )
fo.write("</div>\n")
fo.write("</body>\n")
fo.write("</html>\n")
fo.close()
print "done!"

print "Writing log information....",
fo = open ("tmp/lacnic-ipv4runout-log.txt", "w+")
#log_line = "%s|%s|%s|%s" % ("date", "free_ips", "runout_date", "std_dev")
today = date.today()
today_fmt = today.strftime("%Y%m%d")
log_line = "%s|%s|%s|%s" % (today_fmt, freeipv4_series[-1], p1_date_avg, stddev_offset)
fo.write("%s\n" % (log_line))
fo.close()
print "done!"

##################################################################
