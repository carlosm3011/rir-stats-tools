#!/usr/bin/env python
# carlos@lacnic.net 20111220
#===============================================================================
# Copyright (c) 2011 LACNIC - Latin American and Caribbean Internet 
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

import unittest
from delegated.api import Delegated
from commons.getfile import getfile
import etc.properties 
import os
import sys

#################################################################################
class TDD_Delegated(unittest.TestCase):
    
    def setUp(self):
        self.loc_file = "%s/delegated-lacnic-latest" % (etc.properties.paths['tmp'])
        try:
            # getfile("ftp://ftp.lacnic.net/pub/stats/lacnic/delegated-lacnic-latest", self.loc_file)
            getfile("file:///"+self.loc_file+".org", self.loc_file)
        except Exception as e:
            raise e
        #
        self.dlg = Delegated(self.loc_file)
        self.dlg.read_delegated()
    ###
    
    def tearDown(self):
        if os.path.exists(self.loc_file):
            pass
            os.remove(self.loc_file)
    ####
    
    ####
    def test_get_dlg_file_ftp(self):
        self.assertTrue(os.path.exists(self.loc_file), "getfile failed, loc_file %s" % (self.loc_file) )
    ####
    
    ###
    def test_load_dlg_file(self):
        self.assertTrue(self.dlg != None, 'api not instantiated')
    ###
    
    ###
    def test_find_resource_exact(self):
        rx = self.dlg.resource_find_exact("200.40.0.0")
        print rx
        self.assertTrue(rx != None, "rx should not be none")
        self.assertTrue(rx['cc'] == 'UY', 'rx cc should be UY')
        #
        rx = self.dlg.resource_find_exact("2804:a0c::")
        self.assertTrue(rx != None, "rx should not be none")
        self.assertTrue(rx['cc'] == 'BR', 'rx cc should be BR')
        #
        rx = self.dlg.resource_find_exact("2904:a0c::")
        self.assertTrue(rx == None, "rx should be none")
        #
        rx = self.dlg.resource_find_exact("6057")
        self.assertTrue(rx != None, "rx should not be none")
        self.assertTrue(rx['cc'] == 'UY', '6057 cc should be UY')        
    ###
    
    ###
    def test_resource_find_inside_ipv4(self):
        rx = self.dlg.resource_find_inside('200.40.20.1/32')
        self.assertTrue(rx['cc'] == 'UY', '200.40.20.1/32 should be in UY')
        #
        rx = self.dlg.resource_find_inside('200.40.35.1')
        self.assertTrue(rx['cc'] == 'UY', '200.40.35.1 should be in UY')        
        #
        rx = self.dlg.resource_find_inside('144.22.1.1/21')
        #print ( "\nrx: ")
        #print( rx )
        self.assertTrue(rx['cc'] == 'CR', '144.22.1.1/21 should be in CR')
    ###
    
    ###
    def test_resource_find_inside_ipv6(self):
        tst_res = ['2001:13c7:7001::/128', '2001:13c7:7001::/48', '2800:a0::/30', '2800:a0:dead:beef::1/64', '2803:4e00::/32']
        for x in tst_res:
            rx = self.dlg.resource_find_inside(x)
            #print(rx)
            self.assertTrue( rx != None, "Prefix %s should have been found in dlg" % (x) )
            self.assertTrue( rx['cc'] == 'UY', x + ' should be in UY' )
    ###
    
    ###
    def test_resource_find_inside_asn(self):
        tst_res = ['1797', '6057', '28001']
        for x in tst_res:
            rx = self.dlg.resource_find_inside(x)
            #sys.stderr.write(str(rx)+'\n')
            self.assertTrue( rx != None, "Prefix %s should have been found in dlg" % (x) )
            self.assertTrue(rx['cc'] == 'UY', x + ' should be in UY')
    ###
    
    ###
    def test_dlg_generic_query(self):
        ## count prefixes
        test_cases = { 'UY': 110, 'AR': 1396 }
        for (x,y) in test_cases.iteritems():
            rx =  self.dlg.resource_query("cc = :cc", {'cc': x} )
            rows = rx.fetchall()
            self.assertTrue( len(rows) >= y, "%s recourds should count %s but counts %s" % (x,y,len(rows)) )
    ###    
    
#################################################################################

if __name__ == '__main__':
    unittest.main()
