'''
Created on Sep 3, 2013

@author: marcelo
'''
import unittest

import os
import sys
import etc.properties
import delegated.api
import commons.utils
import commons.getfile
import rpki.ripeval_stats

##################################################################
class Test(unittest.TestCase):
    
    def setUp(self):
        self.rvr = rpki.ripeval_stats.BatchValidationResults()
        fname = commons.utils.get_tmp_file_name("lacnic-roa-prefixes.csv")
        url_org = "file:///%s" % (commons.utils.get_tmp_file_name("lacnic-roa-prefixes.csv.org") )
        commons.getfile.getfile(url_org, fname)
        self.rvr.read_csv(fname)        

    def test_ripeval_init(self):
        self.assertTrue(self.rvr != None, "setUp failed")
    ##
    
    def test_ripeval_load_entries(self):
        rx = self.rvr.stats('prefixes')
        self.assertTrue(rx > 1, "at least one prefix should have been loaded")
    
    def test_resource_query(self):
        rx = self.rvr.query("origin_as=:origin_as", {'origin_as', '28000'})
        rows = rx.fetchall()
        self.assertTrue( len(rows) >= 1, "as 28000 has at least one prefix in roas")
        

##################################################################

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test_ripeval_base']
    unittest.main()