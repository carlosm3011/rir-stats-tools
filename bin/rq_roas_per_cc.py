#-----------------------------------------------------------
# RoaQuery class
#
#
#-----------------------------------------------------------

import etc.rirconfig

class RoaQuery():

	def __init__(self, w_rir):
		#self.ccs = ['AR', 'UY', 'CL', 'EC', 'PE', 'CO', 'VE', 'BO', 'PY', 'PA', 'CR', 'HN', 'CU', 'DO', 
		#			'SV', 'CW', 'AN', 'TT', 'BZ', 'NI', 'GT']
		
		self.ccs = etc.rirconfig.rir_config_data[w_rir]['countrydata']['country-codes'].keys()
		
		self.counts = {}
		self.counts4 = {}
		self.counts6 = {}
		self.totals4 = {}
		self.totals6 = {}

	def roa_test(self, dlg_row, drec):
				
		if dlg_row['cc'] in self.ccs:
			return True
		else:
			return False

	def roa_match(self, dlg_row, drec):
		try:
			if dlg_row['type'] == 'ipv4':
					self.totals4[dlg_row['cc']] = self.totals4.get(dlg_row['cc'], 0) + int ( int(dlg_row['value']) / 256 )
			elif dlg_row['type'] == 'ipv6':
					n48s = pow(2, 32-int(dlg_row['value'])) 
					self.totals6[dlg_row['cc']] = self.totals6.get(dlg_row['cc'], 0) + n48s
		except IndexError:
			print "Invalid lines:\n dlg: %s\n drec: %s\n" % (dict(dlg_row), dict(drec))
			raise
		
		self.counts[dlg_row['cc']] = self.counts.get(dlg_row['cc'], 0) + 1

	def roa_no_match(self, drec, dlg_row):
		print "non-matched row cc: %s, pfx %s" % (drec['cc'], drec['prefix'])

	def finalize(self, extra=None):
		print "\n"
		for x in self.ccs:
			print "prefixes included in roas for country code %s: %s, equivalent to %s /24s and %s /32s" % (
				x, self.counts.get(x,0), self.totals4.get(x, 0), self.totals6.get(x,0) 
			)
