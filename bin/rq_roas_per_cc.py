#-----------------------------------------------------------
# RoaQuery class
#
#
#-----------------------------------------------------------


class RoaQuery():

	def __init__(self):
		self.ccs = ['AR', 'UY', 'CL', 'EC', 'PE', 'CO', 'VE', 'BO', 'PY', 'PA', 'CR', 'HN', 'CU', 'DO', 
					'SV', 'CW', 'AN', 'TT', 'BZ', 'NI', 'GT']
		self.counts = {}
		self.counts4 = {}
		self.counts6 = {}
		self.totals4 = {}
		self.totals6 = {}

	def roa_test(self, drec, dlg_row):
		
		if dlg_row['type'] == 'ipv4':
				self.totals4 = self.totals4.get(drec['cc'], 0) + int ( dlg_row['value'] / 256 )
		elif dlg_row['type'] == 'ipv6':
				n48s = 0
				self.totals6 = self.totals6.get(drec['cc'], 0) + n48s
		
		if drec['cc'] in self.ccs:
			return True
		else:
			return False

	def roa_match(self, drec, dlg_row):
		self.counts[drec['cc']] = self.counts.get(drec['cc'], 0) + 1

	def roa_no_match(self, drec, dlg_row):
		print "non-matched row cc: %s, pfx %s" % (drec['cc'], drec['prefix'])

	def finalize(self, extra=None):
		print "\n"
		for x in self.ccs:
			print "prefixes included in roas for country code %s: %s" % (x, self.counts.get(x,0))
