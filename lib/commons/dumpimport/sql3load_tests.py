'''
Created on Sep 18, 2013

@author: marcelo
'''
import unittest
import sys

from commons.utils import tempfile 
from commons.dumpimport.sql3load import Sql3Load

class Test(unittest.TestCase):


    def setUp(self):
        sys.stderr.write("Creating Sql3Load class instance\n")
        self.s3_template = {'name': 'text', 'age': 'integer', 'weigth': 'real'}
        self.s3l = Sql3Load(self.s3_template)
    ## end

    def tearDown(self):
        pass
    ## end

    def testClassInstantiation(self):
        # test relies on logic put in the setUp method
        pass
    
    def testRowInsertion(self):
        r = self.s3l._insert_row({'name': 'marcelo', 'age': 41, 'weight': 125.0})
        self.assertTrue(r, "record not inserted succesfully")
        
    def testRowRetrieval(self):
        r = self.s3l.query("1=1")
        self.assertTrue(r, 'query did not return a valid value')
        dr = dict(r)
        sys.stderr.write("%s" % (dr))
        self.assertTrue( dr['age'] == 41, 'age should be 41' )
        pass
        
    def testRowCount1(self):
        r = self.s3l.get_rowcount()
        self.assertEqual(r, 1, "rows should be exactly one, but instead count %s" % (r))
        

## end class Test

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()