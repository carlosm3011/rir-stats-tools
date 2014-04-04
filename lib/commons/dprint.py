# carlos@lacnic.net 20121128
# version 0.1
#===============================================================================
# Copyright (c) 2012 LACNIC - Latin American and Caribbean Internet 
# Address Registry
# 
# Permission is hereby granted, free of charge, to any person 
# obtaining a copy of this software and associated documentation 
# files (the "Software"), to deal in the Software without 
# restriction, including without limitation the rights to use, copy, 
# modify, merge, publish, distribute, sublicense, and/or sell copies 
# of the Software, and to permit persons to whom the Software is 
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be 
# included in all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, 
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF 
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND 
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS 
# BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN 
# ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN 
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE 
# SOFTWARE.
#===============================================================================
'''
lib.commons.dprint (c) Marcelo 2013
Generic logging and debug printing utilities.
'''

import os
import sys

##############################################################################
def setAutoFlush():
    # reopen stdout file descriptor with write mode
    # and 0 as the buffer size (unbuffered)
    sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)
##############################################################################

##############################################################################
class dprint:
    def __init__(self, w_sys_loglevel = 3):
        '''
        Default constructor. Parameters are:
            w_sys_loglevel: current log level in the system
        '''
        self.sys_loglevel = w_sys_loglevel
        pass
    #
    def log(self, w_msg, w_level = 3):
        """
        Log message to standard error stream.
        """
        if w_level >= self.sys_loglevel:
            sys.stderr.write(w_msg)
##############################################################################

if __name__ == "__main__":
    print "dprint should not be used directly"