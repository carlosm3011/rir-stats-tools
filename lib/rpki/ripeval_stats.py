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
'''
Created on Sep 3, 2013

@author: marcelo
'''

import sys
import csv
import sqlite3
import string
import ipaddr
import math

### BEGIN
class BatchValidationResults:
    """
    Imports a RIPE Validator dump into a sqlite memory database. Allows generic SQL-like querying.
    
    In-memory database columns are:
    
        * uri
        * origin_as
        * prefix
        * max_len
        * valid_from, valid_until
        * istart
        * iend
    
    :author: carlos@lacnic.net
    """
    
    ### begin
    def __init__(self):
        '''
        Default constructor
        '''
        #
        try:
            #self.conn = sqlite3.connect('/tmp/res.db')
            self.conn = sqlite3.connect(':memory:')
            self.conn.row_factory = sqlite3.Row
            self.cursor = self.conn.cursor()
            self.cursor.execute(''' CREATE TABLE roapfx (uri text, origin_as text, prefix text, max_len int,  ''' + 
                                ''' valid_from text, valid_until text, istart unsigned big int, iend unsigned big int) ''')
            self.conn.commit()
        except:
            raise
    ### end        
    
    def read_csv(self, w_fname):
        '''
        Load ROA data from RIPE batch validator CSV output. 
        
        :param w_fname: file name of the CSV file to import. 
        '''
        # init variables
        try:
            self.file = open(w_fname, 'rb')
            self._stats = {}        
            csv_r = csv.reader(self.file, delimiter=",")
            # row = True
            for row in csv_r:
                # row = csv_r.next()
                record = {}
                if string.find(str(row), "#") != -1:
                    continue
                elif string.find(str(row), "URI") != -1:
                    continue
                else:
                    #sys.stderr.write("row: %s -- len row: %s" % (row, len(row)))
                    record['uri'] = row[0].strip()
                    record['origin_as'] = row[1].strip()[2:]
                    record['prefix'] = row[2].strip()
                    if row[3] != '':
                        record['max_len'] = int(row[3].strip())
                    else:
                        try:
                            prefix_parts = record['prefix'].split("/")
                            record['max_len'] = prefix_parts[1]
                        except:
                            sys.stderr.write("\nrecord: %s \nprefix:%s \nprefix_parts: %s\n" % (str(row), record['prefix'], str(prefix_parts)) )
                            raise
                    record['valid_from'] = row[4].strip()
                    record['valid_until'] = row[5].strip()
                    
                    #record['istart'] = 0
                    #record['iend'] = 0
                    
                    pfx = ipaddr.IPNetwork(record['prefix'])                    
                    if pfx.version == 4:
                        record['istart'] = int(pfx.network)
                        record['iend'] = int(pfx.broadcast)
                    elif pfx.version == 6:
                        pfx_norm_base = pow(2,64)
                        record['istart'] = int(pfx.network) / pfx_norm_base
                        record['iend'] = int(pfx.broadcast) / pfx_norm_base                    
                    
                    
                    # insert into db
                    #print(record)
                    try:
                        self.cursor.execute("INSERT INTO roapfx VALUES (:uri, :origin_as, :prefix, :max_len, " + 
                                            " :valid_from, :valid_until, :istart, :iend)", record)
                        self._stats['prefixes'] = self._stats.get('prefixes',0) + 1
                    except sqlite3.Error:
                        self._stats['failed_inserts'] = self._stats.get('failed_inserts',0) + 1 
        #            
        except csv.Error as e:
            print e
            raise
        except:
            raise
    
    ## begin
    def query(self, w_query, w_parameters):
        """
        Runs an arbitrary SQL query against the in-memory database.
        
        :param w_query: the query itself (what comes after the WHERE SQL keyword) using named parameters for column values, as in:
                        'origin_as=:oas'
                        
        :param w_parameters: an associative array with parameter values. Must be consistent with the names used for wquery, as in:
                            {'oas': '28000'}
        """
        sql = "SELECT * FROM roapfx WHERE %s" % (w_query)
        try:
            return self.cursor.execute(sql, w_parameters)
        except sqlite3.Error as e:
            raise
            return None
        except:
            raise
    ## end
    
    ## begin
    def stats(self, w_stat_name):
        """
        Returns the value of one of several collected stats during CSV import. 
        Returns None if w_stat_name does not exist.
        
        Currently defined stat values are:
        
            * faled_inserts: how many INSERT statements failed during import
            * prefixes: how many prefixes were succesfully inserted into the in-memory database
        
        :param w_stat_name: named stat value.
        """
        return self._stats.get(w_stat_name)
    ## end
### END
    


if __name__ == "__main__":
    print "not to be run directly"