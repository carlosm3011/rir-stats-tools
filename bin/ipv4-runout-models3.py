####
# ipv4_runout_models3
#
# Prediccion de agotamiento de ipv4 en fase 2 -- LACNIC
# (c) Elisa

## END

from numpy import *
from datetime import date
from datetime import timedelta
from time import sleep
from commons import getfile
import sys
import json
import commons.dprint
commons.dprint.setAutoFlush()


hoy = date.today()
print hoy
fecha_fase2 = date(2014, 6, 9)
lastdays = (hoy - fecha_fase2).days
print lastdays 
dias_pred = 300
dash8 = pow(2,24)
pool_reservado = pow(2,32-11)
ipv4libres_tmp = "tmp/reports_freespace.txt"


#fetch data
print "Fetching IPv4 allocation data...",
sys.stdout.flush()
serie_temporal = array([])
serie_ipv4libres = array([])
serie_temporal_pred = []
serie_ipv4libres_pred = []

getfile.getfile("http://opendata.labs.lacnic.net/ipv4stats/ipv4avail/lacnic?lastdays=%s" % (lastdays), ipv4libres_tmp, 30)
print "done!"

print "Parsing JSON data...",
jsd_file = open(ipv4libres_tmp, "r")
datos = json.load(jsd_file)
jsd_file.close()
i = 0
for row in datos['rows']:
	serie_temporal = append(serie_temporal, float(lastdays-i))
	fip4 = float(row['c'][1]['v'])
	serie_ipv4libres = append(serie_ipv4libres, fip4)
	i = i + 1
print "done!"

print "%s entries loaded." % (i)
		
print "Corriendo modelos:"
print "-- "
runout_offsets = []
dash10_offsets = []

model_poly = polyfit(serie_temporal, serie_ipv4libres, 1)
print "Polynomial degree %s fitted successfully, result is: %s" % (1, model_poly)
	
base_t =int(amax(serie_temporal))
	
time_series_future = xrange(0, base_t + dias_pred)
	
serie_temporal_pred.append(array([]))
serie_ipv4libres_pred.append(array([]))
	
dash10_offset = -1
f = open("tmp/pred_ipv4libres_%s.txt" % (str(hoy)), "w")
for t in time_series_future:
	ipv4libres_estimado = polyval(model_poly, t)
	serie_ipv4libres_pred[-1] = append(serie_ipv4libres_pred[-1], ipv4libres_estimado)
	serie_temporal_pred[-1] = append(serie_temporal_pred[-1], t)
	f.write(str(fecha_fase2 + timedelta(t))+","+str(ipv4libres_estimado)+"\n")
	print "t: %s, free_ipv4: %s" % (t, ipv4libres_estimado),
	if ipv4libres_estimado < 0.25*float(dash8) and dash10_offset == -1:
		dash10_offset =t-base_t
	if ipv4libres_estimado < pool_reservado:
		break
	print '\r',
	sleep(0.005)
		
print " "
f.close()
	
if t < base_t + dias_pred - 1:
	#print "Delta T for dash10 global policy trigger was %s" % (dash10_offset)
	print "Delta T for dash11 runout is %s" % (t-base_t)
	runout_offsets.append(t)
	dash10_offsets.append(dash10_offset)
	p3_date = fecha_fase2 + timedelta(t)
	print "Expected phase 3 entry date %s" % (p3_date)
else:
	print "Delta T could not be identified, check for numerity instability"
	serie_temporal_pred.pop()
	serie_ipv4libres_pred.pop()
		
print "--"		
	
