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

### BEGIN
class BatchValidationResults:
    
    ### begin
    def __init__(self):
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
        # init variables
        try:
            self.file = open(w_fname, 'rb')
            self._stats = {}        
            csv_r = csv.reader(self.file, delimiter=",")
            # row = True
            for row in csv_r:
                row = csv_r.next()
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
                    record['max_len'] = int(row[3].strip())
                    record['valid_from'] = row[4].strip()
                    record['valid_until'] = row[5].strip()
                    record['istart'] = 0
                    record['iend'] = 0
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
        return self._stats.get(w_stat_name)
    ## end
### END
    


if __name__ == "__main__":
    print "not to be run directly"