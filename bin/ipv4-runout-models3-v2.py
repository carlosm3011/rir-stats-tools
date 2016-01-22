####
# ipv4_runout_models3
#
# Prediccion de agotamiento de ipv4 en fase 2 -- LACNIC
# (c) Elisa

## END

from numpy import *
from datetime import date
from datetime import timedelta
from datetime import datetime
from time import sleep
from time import mktime
from commons import getfile
import sys
import json
import commons.dprint
import getopt
commons.dprint.setAutoFlush()

def parseMongoDate(stringDate):
	b=stringDate[5:-1]
	c=[int(x) for x in b.split(",")]
	d=datetime(c[0],c[1]+1,c[2],c[3],c[4],c[5])
	timestamp=mktime(d.timetuple())
	return timestamp

hoy = date.today()
fecha_fase2 = date(2014, 6, 9)
poly_degree = xrange(1,4)
lastdays = (hoy - fecha_fase2).days
print lastdays 
dias_pred = 600
dash8 = pow(2,24)
pool_reservado = 0
ipv4libres_tmp = "tmp/reports_freespace.txt"

#fetch data
print "Fetching IPv4 allocation data...",
sys.stdout.flush()
serie_temporal = array([])
serie_temporal_corrida = array([])
serie_ipv4libres = array([])
serie_temporal_pred = []
serie_ipv4libres_pred = []

getfile.getfile("http://opendata.labs.lacnic.net/ipv4stats/ipv4avail/lacnic?lastdays=%s" % (lastdays-1), ipv4libres_tmp, 30)
print "done!"

print "Parsing JSON data...",
jsd_file = open(ipv4libres_tmp, "r")
datos = json.load(jsd_file)
jsd_file.close()
i = 0
for row in reversed(datos['rows']):
	ts=parseMongoDate(row['c'][0]['v'])
	serie_temporal = append(serie_temporal, ts)
	fip4 = row['c'][1]['v']
	serie_ipv4libres = append(serie_ipv4libres, fip4)
	i = i + 1
print "done!"

rango = xrange(1, lastdays+1)

for r in rango:
	fecha_ts2 = fecha_fase2 + timedelta(float(r))
	ts2 = mktime(fecha_ts2.timetuple())
	serie_temporal_corrida = append(serie_temporal_corrida, ts2)

print date.fromtimestamp(serie_temporal_corrida[0])
print date.fromtimestamp(serie_temporal_corrida[-1])

print "%s entries loaded." % (i)
		
print "Corriendo modelos:"
print "-- "
runout_offsets = []
dash10_offsets = []

#try:
#	opts, args = getopt.getopt(sys.argv[1:],"d:",["degree="])
#	for o,a in opts:
#		if o in ("-d", "--degree"):
#			poly_degree = int(a)
#except getopt.GetoptError:
#	print './bin/ipv4_runout_models3.py -d <model_degree>'
#	sys.exit(2)

rango_pred = array([])	
rango_pred = append(rango_pred, serie_temporal_corrida)
for j in xrange(0,dias_pred):
	d = hoy + timedelta(j)
	ts = mktime(d.timetuple())
	rango_pred = append(rango_pred, ts)
	
fechas = []
for f in xrange(0, len(serie_temporal)):
	fechas.append(date.fromtimestamp(serie_temporal[f]))

#Armado de los polinomios y prediccion
fines = array([])
for md in poly_degree:
	model_poly = polyfit(serie_temporal, serie_ipv4libres, md)
	print "Polynomial degree %s fitted successfully, result is: %s" % (md, model_poly)
	base_t =int(amax(serie_temporal))
	cero = int(amin(serie_temporal))
	time_series_future = xrange(0, len(rango_pred))
	serie_temporal_pred.append(array([]))
	serie_ipv4libres_pred.append(array([]))
	dash10_offset = -1
	for t in time_series_future:
		ipv4libres_estimado = polyval(model_poly, rango_pred[t])
		serie_ipv4libres_pred[-1] = append(serie_ipv4libres_pred[-1], ipv4libres_estimado)
		serie_temporal_pred[-1] = append(serie_temporal_pred[-1], rango_pred[t])
	
		print "t: %s, free_ipv4: %s" % (t, ipv4libres_estimado),
		if ipv4libres_estimado < 0.25*float(dash8) and dash10_offset == -1:
			dash10_offset =t-lastdays-1
		if ipv4libres_estimado < pool_reservado:
			break
		print '\r',
		sleep(0.005)		
	print " "
			
	if t < lastdays - 1 + dias_pred - 1:
		print "Delta T for dash11 runout is %s" % (t-lastdays-1)
		runout_offsets.append(t)
		dash10_offsets.append(dash10_offset)
		p3_date = date.fromtimestamp(rango_pred[t])
		fines = append(fines,rango_pred[t])
		print "Expected phase 3 entry date %s" % (p3_date)
		
	else:
		print "Delta T could not be identified, check for numerity instability"

rango=xrange(0, len(serie_ipv4libres_pred[0])-1)

#Guardando datos en archivos
f = open("html/pred_ipv4libres3_%s.txt" % (str(hoy)), "w")
#g = open("tmp/vacios.txt", "w")
f.write("Fecha,Modelo1,Modelo2,Modelo3,Conocido,Limite\n")
for t in rango:
	int_ipv4libres_estimado1=int(round(serie_ipv4libres_pred[0][t]))	
	if date.fromtimestamp(rango_pred[t]) in fechas and t < len(serie_ipv4libres_pred[1]) and t < len(serie_ipv4libres_pred[2]):
		int_ipv4libres_estimado3=int(round(serie_ipv4libres_pred[2][t]))
		int_ipv4libres_estimado2=int(round(serie_ipv4libres_pred[1][t]))
		int_serie_ipv4libres=int(serie_ipv4libres[fechas.index(date.fromtimestamp(rango_pred[t]))])
		f.write(str(date.fromtimestamp(rango_pred[t]))+","+str(int_ipv4libres_estimado1)+","+str(int_ipv4libres_estimado2)+","+str(int_ipv4libres_estimado3)+","+str(int_serie_ipv4libres)+","+str(pool_reservado)+"\n")
	elif t < len(serie_ipv4libres_pred[1]) and t < len(serie_ipv4libres_pred[2]):
		int_ipv4libres_estimado2=int(round(serie_ipv4libres_pred[1][t]))
		int_ipv4libres_estimado3=int(round(serie_ipv4libres_pred[2][t]))
		f.write(str(date.fromtimestamp(rango_pred[t]))+","+str(int_ipv4libres_estimado1)+","+str(int_ipv4libres_estimado2)+","+str(int_ipv4libres_estimado3)+","+","+str(pool_reservado)+"\n")
		#g.write(str(date.fromtimestamp(rango_pred[t]))+"\n")
	elif t < len(serie_ipv4libres_pred[1]):
		int_ipv4libres_estimado2=int(round(serie_ipv4libres_pred[1][t]))
		f.write(str(date.fromtimestamp(rango_pred[t]))+","+str(int_ipv4libres_estimado1)+","+str(int_ipv4libres_estimado2)+",,,%s\n"%(str(pool_reservado)))
	else:
		f.write(str(date.fromtimestamp(rango_pred[t]))+","+str(int_ipv4libres_estimado1)+",,,,%s\n" % (str(pool_reservado)))
f.close()
	
print "Calculating model error..."
#Calculando el error
largo = xrange(0, len(serie_temporal)-1)
media_ipv4libres = sum(serie_ipv4libres)/float(len(serie_temporal))

errores = array([])
for mdl in xrange(0,3):
	print mdl
	total = 0
	residuo = 0
	for i in largo:
		residuo = residuo + (serie_ipv4libres[i]-serie_ipv4libres_pred[mdl][i])**2
		total = total + (serie_ipv4libres[i]-media_ipv4libres)**2
	error2 = 1 - residuo/total
	errores = append(errores, error2)
	print "done!"
	print "Error2 para modelo de grado %s es %s" % (mdl+1, error2)

#Calculando la fecha promedio ponderada
suma = errores[0]+errores[1]+errores[2]
res = 0
for i in (0,1,2):
	wi = errores[i]/suma
	res = res+wi*fines[i]
	
print "%s" % (date.fromtimestamp(res))

#Generacion de json para fechas	y errores	
a = open("html/fechas3.json", "w")
p3_date_md1 = date.fromtimestamp(serie_temporal_pred[0][-1])
p3_date_md2 = date.fromtimestamp(serie_temporal_pred[1][-1])
p3_date_md3 = date.fromtimestamp(serie_temporal_pred[2][-1])
p3_pond = date.fromtimestamp(res)
st = {'model-run-date':str(hoy), 
      'phase2-runout-date-md1':str(p3_date_md1), 
      'phase2-runout-date-md2':str(p3_date_md2),
      'phase2-runout-date-md3':str(p3_date_md3),
      'Error mdl 1': errores[0], 
      'Error mdl 2': errores[1], 
      'Error mdl 3': errores[2],
      'Fecha ponderada': str(p3_pond)}
dump = json.dumps(st)
a.write(dump)
a.close()

e = open("html/errores.json", "w")
st = {'Error mdl 1': errores[0], 'Error mdl 2': errores[1], 'Error mdl 3': errores[2]}
dump = json.dumps(st)
e.write(dump)
e.close()
	

print "--"		
	
