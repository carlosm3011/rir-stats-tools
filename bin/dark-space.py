#!/usr/bin/env python2.7
# Copyright (c) 2015, LACNIC All rights reserved.

# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:

# 1. Redistributions of source code must retain the above copyright notice, this
# list of conditions and the following disclaimer.

# 2. Redistributions in binary form must reproduce the above copyright notice,
# this list of conditions and the following disclaimer in the documentation
# and/or other materials provided with the distribution.

# 3. Neither the name of the copyright holder nor the names of its contributors
# may be used to endorse or promote products derived from this software without
# specific prior written permission.

# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

# imports
import cmd
import readline
import sys
import os
import ipaddr
import json

from argparse import ArgumentParser
from argparse import RawDescriptionHelpFormatter

import etc.properties
import etc.rirconfig
import delegated.api
import commons.getfile
import commons.dprint
import commons.utils
import commons.statkeeper

# class def ######
class DarkSpaceId:
	#
	def __init__(self, w_rir='lacnic'):
		self.version = "0.1"
		self.rir = w_rir
		self.ddate = "latest"
		print "Dark Space Identification, version %s" % (self.version)
		print " -- "
		print " "
		print "getting delegated-extended for rir %s" % (self.rir),
		dlg_tmpfile = commons.utils.get_tmp_file_name("delegated-extended-%s-%s" % (self.rir, self.ddate))
		dlg_tmpfile = commons.getfile.getfile(etc.rirconfig.rir_config_data[self.rir]['dlge'][0] % (self.ddate), dlg_tmpfile, 43200)
		print " done!"
		print "importing delegated-extended into memory ",
		dlg = delegated.api.Delegated(dlg_tmpfile)
		print "done!"
	#
## end class ######

if __name__ == "__main__":
	did = DarkSpaceId()
	#

## END ############################################################################