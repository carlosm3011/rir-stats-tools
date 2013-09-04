'''
Created on Sep 3, 2013

@author: marcelo
'''

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
            self.stats = {}        
            csv_r = csv.reader(self.file, delimiter=",")
            row = True
            while row:
                row = csv_r.next()
                record = {}
                print(row)
                if string.find(str(row), "#") != -1:
                    continue
                elif string.find(str(row), "URI") != -1:
                    continue
                else:
                    sys.stderr.write("row: %s -- len row: %s" % (row, len(row)))
                    record['uri'] = row[0].strip()
                    record['origin_as'] = row[1].strip()                
        #            
        except StopIteration:
            pass
        except:
            raise
    
    def query(self, w_query, w_parameters):
        pass
### END
    


if __name__ == "__main__":
    print "not to be run directly"