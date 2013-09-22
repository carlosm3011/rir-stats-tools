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

"""
Delegated API Class
(c) carlos@lacnic.net
"""

import csv
import os
import sys
import string
import sqlite3
import ipaddr
import math
#
from commons.dprint import dprint

# BEGIN class delegated
class Delegated:
    file = None
    filename = None
    version_line = {}
    summary_lines = []
    record_lines = []
    filters = []
    cnt = {}
    
    def __init__(self, w_file):
        # init csv
        try:
            self.file = open(w_file, 'rb')
            self.file.close()
            self.filename = w_file
        except:
            raise Exception( "Could not open file %s" % (w_file) )
        #
        try:
            #self.conn = sqlite3.connect('/tmp/res.db')
            self.conn = sqlite3.connect(':memory:')
            self.conn.row_factory = sqlite3.Row
            self.cursor = self.conn.cursor()
            self.cursor.execute(''' CREATE TABLE resources (registry text, cc text, type text, start text, value text, ''' + 
                                ''' date text, status text, prefix text, istart unsigned big int, iend unsigned big int) ''')
            self.conn.commit()
        except:
            raise
    ## end init
    
    def read_delegated(self):
        """
        Load the stats file specified in the constructor.
        """
        # init variables
        self.file = open(self.filename, 'rb')        
        self.version_line = {}
        self.summary_lines = []
        self.record_lines = []
        self.cnt = {}        
        csv_r = csv.reader(self.file, delimiter="|")
        
        # load version line
        while True:
            try:
                row = csv_r.next() 
                if string.find(str(row), "#") == -1:
                    self.version_line['version'] = row[0].strip()
                    self.version_line['registry'] = row[1].strip()
                    self.version_line['serial'] = row[2].strip()
                    self.version_line['records'] = row[3].strip()
                    self.version_line['startdate'] = row[4].strip()
                    self.version_line['enddate'] = row[4].strip()
                    self.version_line['UTCoffset'] = row[5].strip()
                    break
            except IndexError as e:
                dprint("Error importing line: [%s]\n" % (row))
                sys.exit(1)
        ##
        
        # load summary lines
        if string.find(str(row), "#") == -1:
            row = csv_r.next()
            while row[5].strip() == 'summary':
                    summary_entry = { 'registry': row[0].strip(),
                                      'type': row[2].strip(),
                                      'count': row[4].strip()
                                     }
                    self.summary_lines.append(summary_entry)
                    row = csv_r.next()
        # end loading summary lines
        
        # load records
        self.cnt['all'] = 0
        self.cnt['imported'] = 0
        self.cnt['filtered'] = 0
        while row:
            try:
                record = {  'registry': row[0].strip(),
                            'cc': row[1].strip(),
                            'type': row[2].strip(),
                            'start': row[3].strip(),
                            'value': row[4].strip(),
                            'date': row[5].strip(),
                            'status': row[6].strip()
                          }
                # insert into db
                if record['type'] == 'ipv4':
                    pfx_len = 32 - int( math.log( int(record['value']), 2) )
                    pfx = ipaddr.IPv4Network(record['start'] + "/" + str(pfx_len))
                    record['prefix'] = str(pfx)
                    record['istart'] = int(pfx.network)
                    record['iend'] = int(pfx.broadcast)
                elif record['type'] == 'ipv6':
                    pfx_norm_base = pow(2,64)
                    pfx = ipaddr.IPv6Network( record['start'] + "/" + record['value'] )
                    record['prefix'] = str(pfx)
                    record['istart'] = int(pfx.network) / pfx_norm_base
                    record['iend'] = int(pfx.broadcast) / pfx_norm_base                    
                else:
                    record['prefix'] = 'na/asn'
                    record['istart'] = int(record['start'])
                    record['iend'] = int(record['start']) + int(record['value'])
                #
                self.cursor.execute("INSERT INTO resources VALUES (:registry, :cc, :type, :start, :value, :date, :status, " + 
                                    " :prefix, :istart, :iend)", record)
                #
                row = csv_r.next()
            except ValueError:
                sys.stderr.write('ERROR parsing line from delegated file: %s\n' % (row))
                raise
            except IndexError:
                # print "*"
                row = csv_r.next()
                pass
            except StopIteration:
                break
            except Exception as e:
                dprint( "Could not read line %s: %s" % (self.cnt['all'], row) )
                dprint( "Exception message %s" % (e.message) )
                raise
                #
        self.conn.commit()
        self.file.close()
    ## end read_delegated
    
    ### BEGIN
    def resource_query(self, query, parameters):
        """
        runs a generic query returning a db cursor
        """
        try:            
            #
            sql1 = "SELECT * FROM resources WHERE %s" % (query) 
            res = self.cursor.execute(sql1, parameters)
            if res:
                return res
            else:
                return None
        except sqlite3.DatabaseError as e:
            dprint("SQL error: %s" % (sql1) )
            return None
        except:
            raise  
    ### END

    ### BEGIN
    def resource_find_inside(self, w_resource):
        """
        Looks for w_resource inside assignments
        """
        # classify resource, get ranges
        try:        
            pfx = ipaddr.IPNetwork(w_resource)
            if pfx.version == 4:
                pfx_range = (int(pfx.network), int(pfx.broadcast))
                sql1 = "SELECT * FROM resources WHERE type='ipv4' and istart <= ? and iend >= ? LIMIT 1" 
            else:
                pfx_norm_base = pow(2,64)
                pfx_range = (int(pfx.network) / pfx_norm_base, int(pfx.broadcast) / pfx_norm_base)
                sql1 = "SELECT * FROM resources WHERE type='ipv6' and istart <= ? and iend >= ? LIMIT 1" 
        except ValueError as e:
            # if not a v4 or v6 pfx, assume its an asn
            pfx_range = (int(w_resource), int(w_resource))
            sql1 = "SELECT * FROM resources WHERE type='asn' and istart <= ? and iend > ? LIMIT 1" 
        except:
            raise
                
        try:            
            #
            #sql1 = "SELECT * FROM resources WHERE istart <= ? and iend >= ? LIMIT 1" 
            res = self.cursor.execute(sql1, pfx_range )
            if res:
                row = res.fetchone()
                #print("res:" + w_resource)
                #print(row)
                return row
            else:
                sys.stderr.write("No match for: istart <= %s and iend >= %s" % pfx_range ) 
                return None
        except sqlite3.DatabaseError as e:
            dprint("SQL error: %s" % (sql1) )
            raise e
        except:
            raise
        #
    # END resource_find_inside
    
    ### BEGIN
    def resource_find_exact(self, w_query):
        """
        looks for exact matches inside the delegated records
        """
        try:
            sql1 = "SELECT * FROM resources WHERE start='%s' LIMIT 1" % (w_query)
            res = self.cursor.execute(sql1)
            return res.fetchone()
        except sqlite3.DatabaseError as e:
            dprint("SQL error: %s" % (sql1) )
            raise e
        except:
            raise
    #                    
# END class delegated

## test cases
if __name__ == "__main__":
    print "not to be run directly"