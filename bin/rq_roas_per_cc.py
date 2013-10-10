#-----------------------------------------------------------
# RoaQuery class
#
#
#-----------------------------------------------------------

import etc.rirconfig
import sys
import ipaddr
import math

class RoaQuery():

	def __init__(self, w_rir, w_extra):
		
		if not w_extra:
			# self.ccs = etc.rirconfig.rir_config_data[w_rir]['countrydata']['country-codes'].keys()
			self.ccs = []
			self.learn_ccs = True
		else:
			self.ccs = [w_extra]
			self.learn_ccs = False
		
		self.counts = {}
		self.totals4 = {}
		self.totals6 = {}
		self.prefixes4 = {}
		self.prefixes6 = {}
		#
		self.allccs4 = 0
		self.allccs6 = 0

	## begin
	def roa_test(self, dlg_row, drec):
		if not dlg_row['cc'] in self.prefixes4.keys():
			self.prefixes4[dlg_row['cc']] = []
			self.prefixes6[dlg_row['cc']] = []
		if dlg_row['cc'] in self.ccs:
			return True
		else:
			# si tengo que aprender country codes, entonces lo agrego
			if self.learn_ccs:
				self.ccs.append(dlg_row['cc'])
				return True
			else:
				return False
	## end
			
	## begin
	def roa_match(self, dlg_row, drec):
		#
		# self.prefixes.append(drec['prefix'])
		try:
			if dlg_row['type'] == 'ipv4':
					self.prefixes4[dlg_row['cc']].append(ipaddr.IPv4Network(drec['prefix']))
					# sys.stderr.write("%s\n" % ( dict(drec) ))
			elif dlg_row['type'] == 'ipv6':
					self.prefixes6[dlg_row['cc']].append(ipaddr.IPv6Network(drec['prefix']))
					#self.allccs6 = self.allccs6 + v6blocks
		except IndexError:
			print "Invalid lines:\n dlg: %s\n drec: %s\n" % (dict(dlg_row), dict(drec))
			raise

		self.counts[dlg_row['cc']] = self.counts.get(dlg_row['cc'], 0) + 1

	def roa_no_match(self, drec, dlg_row):
		pass
		#print "non-matched row cc: %s, pfx %s" % (drec['cc'], drec['prefix'])

	def finalize(self, extra=None):
		# count space
		for cc in self.prefixes4.keys():
			pfx4_summarized = ipaddr.collapse_address_list(self.prefixes4[cc])
			for p in pfx4_summarized:
				v4blocks = (int(p.broadcast+1) - int(p.network)) / 256
				self.totals4[cc] = self.totals4.get(cc, 0) + v4blocks
				self.allccs4 = self.allccs4 + v4blocks
				
		for cc in self.prefixes6.keys():
			pfx6_summarized = ipaddr.collapse_address_list(self.prefixes6[cc])
			for p in pfx6_summarized:
				v6blocks = pow(2,32) / pow(2, p.prefixlen)
				# v6blocks = 0
				self.totals6[cc] = self.totals6.get(cc, 0) + v6blocks
				self.allccs6 = self.allccs6 + v6blocks
		
		# summarize
		print "\n"
		for x in self.ccs:
			print "prefixes included in roas for country code %s: %s, equivalent to %s /24s and %s /32s" % (
				x, self.counts.get(x,0), self.totals4.get(x, 0), self.totals6.get(x,0) 
			)
		
		print "\n"
		print "Total IPv4 /24s for all CCs: %s" % self.allccs4
		print "Total IPv6 /32s for all CCs: %s" % self.allccs6
		#