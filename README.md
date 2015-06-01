# RIR-STATS-TOOLS

**Creacion**: 2013-08-29 

**Autores**: 

- Elisa Peirano <elisa @ lacnic.net>
- Carlos Martinez <carlos @ lacnic.net>

## Introduccion 

Este proyecto brinda un conjunto de herramientas para procesar datos 
estadisticos producidos por los diferentes Registros Regionales de Internet, en 
particular LACNIC.

## Herramientas

### Commons

Libreria python de funciones de apoyo:

* getfile: bajar archivos por HTTP
* dpring: debugging print

### RPKI Stats

Estadisticas de despliegue de RPKI. Algunos ejemplos:

**RPKI por codigo de pais**
```
 ./bin/run.sh ./bin/rpki-stats.py -r lacnic -q ./bin/rq_roas_per_cc.py
```

### IPv4 Runout Models

Estimaciones de fechas de agotamiento de IPv4

### IPv6 Stats

TBD

