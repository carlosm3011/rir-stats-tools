##################################################################
# ipv4 runout models
# (c) carlos@lacnic.net 2014-03-05
#
# this version uses different exhaustion data
##################################################################
from matplotlib import use
use('Agg')
from matplotlib import pyplot
#
from numpy import *
from datetime import date 
from datetime import timedelta
from time import sleep
from commons import getfile
import sys
#import csv
import json
import commons.dprint
commons.dprint.setAutoFlush()


# avoid tkinter, allow headless plots

dash8 = pow(2,24)
time_horizon = 180
lastdays = 120
date_dash9_reached = date(2014,5,20)
date_debogon_start = date(2014,5,23)
model_degrees = [1,3]
reserve_pool_size = pow(2,32-10) 
base_date = date.today() - timedelta(lastdays)
freeipv4_tmpfile = "tmp/reports_freespace_fromextended.txt"

#
print "IPv4 RUNDOWN MODELS (c) Carlos M. Martinez, carlos@lacnic.net"
print "--"
print " "

# fetch data
print "Fetching IPv4 allocation data... ",
sys.stdout.flush()
time_series = array([])
freeipv4_series = array([])
time_series_pred = []
freeipv4_series_pred = []

getfile.getfile("http://opendata.labs.lacnic.net/ipv4stats/ipv4avail/lacnic?lastdays=%s" % (lastdays), freeipv4_tmpfile, 30)
print "done!"

print "Parsing JSON data...",
jsd_file = open(freeipv4_tmpfile, "r")
jsd_data = json.load(jsd_file)
jsd_file.close()
cnt = 0
for row in jsd_data['rows']:
    time_series     = append(time_series, float(lastdays-cnt))
    ref_date = base_date+timedelta(lastdays-cnt)
    fip4 = float(row['c'][1]['v']) 
    if  ref_date <= date_dash9_reached :
        print "0: %s, %s" % (lastdays-cnt, fip4  )
        freeipv4_series = append(freeipv4_series, fip4 )
    elif ref_date < date_debogon_start:
        print "1: %s, %s" % (lastdays-cnt, fip4 - dash8/8 )
        freeipv4_series = append(freeipv4_series, fip4 - dash8/8)        
    elif ref_date >= date_debogon_start: 
        print "2: %s, %s" % (lastdays-cnt, fip4  )
        freeipv4_series = append(freeipv4_series, fip4 )
    cnt = cnt + 1
print "done!"

print "%s entries loaded." % (cnt)

# sys.exit(0)

# run models
print "Now running different models:"
print "-- "
runout_offsets = []
dash9_offsets = []

for md in model_degrees:
    model_poly = polyfit(time_series, freeipv4_series, md)
    print "Polynomial degree %s fitted sucessfully, result is: %s" % (md, model_poly)

    # print out expected runout dates
    # find the next zero-crossing
    base_t = int(amax(time_series))
    # time_series_future = xrange(base_t, base_t + time_horizon)
    time_series_future = xrange(0, base_t + time_horizon)
    #
    time_series_pred.append(array([]))
    freeipv4_series_pred.append(array([]))
    #
    dash9_offset = -1
    for t in time_series_future:
        freeipv4_estimated = polyval(model_poly, t)
        freeipv4_series_pred[-1] = append(freeipv4_series_pred[-1], freeipv4_estimated)
        time_series_pred[-1] = append(time_series_pred[-1], t)
        print "t: %s, free_ipv4: %s" % (t, freeipv4_estimated),
        if freeipv4_estimated < 0.5*float(dash8) and dash9_offset == -1:
            dash9_offset = t-base_t
        if freeipv4_estimated < reserve_pool_size:
            break
        print '\r',
        sleep(0.005)

    print " "
    # print "Polynomial degree is %s" % (md)
    if t < base_t + time_horizon - 1:
        print "Delta T for dash9 global policy trigger is %s" % (dash9_offset)
        print "Delta T for IPv4 runout is %s" % (t-base_t)
        runout_offsets.append(t)
        dash9_offsets.append(dash9_offset)
        p1_date = base_date + timedelta(t)
        print "Expected phase 1 entry date %s" % (p1_date)
    else:
        print "Delta T could not be identified, check for numeric instability"
	time_series_pred.pop()
	freeipv4_series_pred.pop()

    print "--"

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
last_freeipv4 = freeipv4_series[0]
#

print " "
print "Writing HTML widget...",
#
fo = open ("tmp/lacnic-ipv4runout-widget.html", "w")
fo.write("<html>\n")
fo.write("<head>\n")
fo.write('<link href="http://www2.lacnic.net/lacnic/depletion.css" rel="stylesheet" type="text/css">')
fo.write("</head>\n")
fo.write("<body>\n")
fo.write("<div class='l4runout'>\n")
fo.write("<div id='l4hdr'>LACNIC IPv4 Exhaustion Model</div>\n")
fo.write("<div id='l4addr'>%s</div>\n" % ( int(last_freeipv4) ) )
fo.write("<div id='l4dash8'>%.3f</div>\n" % ( float(last_freeipv4) / dash8 )  )
fo.write("<div id='l4date'>%s</div>\n" % ( p1_date_avg ) )
fo.write("<div id='l4avalloc'>%.2f</div>\n" % ( last_freeipv4 - reserve_pool_size ) )
fo.write("</div>\n")
fo.write("</body>\n")
fo.write("</html>\n")
fo.close()
print "done!"


### PLOT #########################################################################
print "Writing plot...",
po = pyplot.plot(time_series, freeipv4_series, linewidth=2)
for x in xrange(0, len(time_series_pred)):
    po = pyplot.plot(time_series_pred[x], freeipv4_series_pred[x], 'r-')
#
locx = range(15, max(runout_offsets)+15, 30)
pyplot.xticks(locx, [base_date + timedelta(x) for x in locx])
#
locy, yl = pyplot.yticks()
pyplot.yticks(locy, [ "%.2f" % (float(y)/pow(2,32-8)) for y in locy])
pyplot.axhline(y=reserve_pool_size, linewidth=2, color='g')
pyplot.axhline(y=reserve_pool_size*2, linewidth=1, color='y')
pyplot.annotate("/9 Trigger", (50,reserve_pool_size*2+100000))
pyplot.annotate("/10 Reserve", (60,reserve_pool_size+100000))
pyplot.annotate("Generated on: %s" % (date.today()), (70,1.2*dash8))
pyplot.vlines(locx,0,1.49*dash8,linestyles='dotted')
#pyplot.vlines(avg_offset, 0, 0.75*dash8, linestyles='dotted', color='blue')
#pyplot.annotate("Approx. Runout Date: %s" % (p1_date_avg), (avg_offset-10, 0.78*dash8) )
pyplot.annotate("LACNIC reached its last /10 on 2014-06-10", (avg_offset-40, 0.78*dash8), color='red' )
pyplot.hlines(locy, 0, 135, linestyles='dotted')
pyplot.ylabel("Available IPv4 Space (in /8s)")
pyplot.xlabel("Time")
pyplot.savefig("tmp/lacnic-ipv4runout-plot.png", dpi=120)
print "done!"
##################################################################################

### LOG ##########################################################################
print "Writing log information....",
sys.stdout.flush()
fo = open ("tmp/lacnic-ipv4runout-log.txt", "a+")
#log_line = "%s|%s|%s|%s" % ("date", "free_ips", "runout_date", "std_dev")
today = date.today()
today_fmt = today.strftime("%Y%m%d")
log_line = "%s|%s|%s|%s" % (today_fmt, last_freeipv4, p1_date_avg, stddev_offset)
fo.write("%s\n" % (log_line))
fo.close()
print "done!"
##################################################################################

##################################################################
