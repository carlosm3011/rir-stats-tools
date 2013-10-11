import commons.dumpimport.sql3load as sq3l
import commons.getfile as gf

print "Fetching riswhois dump for ipv4"
gf.getfile("http://www.ris.ripe.net/dumps/riswhoisdump.IPv4.gz", "tmp/riswhoisdump.IPv4.gz")

print "Importing dump into memory"

memdb = sq3l.sql3load([('originas','text'),('prefix','text'),('seenby','integer')])
memdb.importFile("tmp/riswhoisdump.IPv4.gz", "\t")

print "Getting import stats"
print memdb.getStats()

print "Get first 10 rows"
q = memdb.query("1=1 ORDER BY id DESC LIMIT 25")
for r in q:
	print dict(r)