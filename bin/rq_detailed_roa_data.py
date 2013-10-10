#-----------------------------------------------------------
# RoaQuery class: Detailed ROA Information
#
# (c) carlos@lacnic.net
#-----------------------------------------------------------

import etc.rirconfig
import commons.statkeeper
import sys
import ipaddr
import math

class RoaQuery():

	def __init__(self, w_rir, w_extra = None):
		self.parameters = w_extra
		self.sk = commons.statkeeper.statkeeper()
		if not self.parameters:
			sys.stderr.write("Use --extra to pass a country code. Try Again.\n\n")
			sys.exit(-1)
		

	## begin
	def roa_test(self, dlg_row, rpki_row):
		if dlg_row['cc'] == self.parameters:
			self.sk.incKey('roa-count')
			print "ROA pfx: %s, DLG info: %s" % (rpki_row['prefix'], dict(dlg_row))

	## end
			
	## begin
	def roa_match(self, dlg_row, drec):
		pass

	def roa_no_match(self, drec, dlg_row):
		pass

	def finalize(self, extra=None):
		print "\n"
		print "ROA count for CC %s: %s" % (self.parameters, self.sk.getKey('roa-count'))