# carlos@lacnic.net 20121128
#
# version 0.1 20121128
# version 0.2 20130102: addition of two sk's
# version 0.3 20131011: reset key value


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

import os
import sys
import gzip
import ipaddr
import time
import json

## counter class
class statkeeper():
    """
    This class implements a generic statistic counter. Statistics are stored as 'keys' and can 
    be incremented by 1 or by an arbitrary number and can be printed just with 'print'
    """
    def __init__(self):
        self.keys = {}
    #
    def incKey(self, w_key, w_increment = 1):
        """
        Increment key w_key by w_increment.
        
        :param w_key: (str) key name
        :param w_increment: (int) increment value, defaults to 1
        """
        self.keys[w_key] = self.keys.get(w_key, 0) + w_increment
    #
    def getKey(self, w_key):
        """
        Get a single key value by name or 0 if key not present.
        """
        return self.keys.get(w_key, 0)
    #
    def getAllKeys(self):
        '''
        Returns all available keys in a dictionary
        '''
        return self.keys
    #
    def getJSON(self):
        '''
        Returns all available keys in JSON format
        '''
        return json.dumps(self.keys)
    
    #
    def setKey(self, w_key, w_value=0):
        '''
        Set key value. Defaults to zero.
        '''
        self.keys['w_key'] = w_value
    
    #
    def __repr__(self):
        rs = ""
        for k in self.keys.keys():
            rs = rs + "%s: %s\n" % (k, self.keys[k]) 
        return rs
    #
    def add_merge(self, w_sk):
        """
        Additive merge of two sk's. The behaviour is as follows:
        - keys that do not exist in one of the sk's are copied into the recipient sk
        - keys that hold NUMERIC values and exist in both sk's are ADDED
        - keys that do not hold NUMERIC values and that exist on both are IGNORED 
            (meaning the value stored in the recipient is maintained)
        """
        for wk in self.keys.keys():
            try:
                self.keys[wk] =  self.keys[wk] + w_sk.keys[wk]
            except KeyError:
                # local key does not exist in foreign sk
                pass
            except:
                raise
        #
        # copy foreign keys
        # determine keys from foreign that are not in local
        local_keys = set(self.keys.keys())
        foreign_keys = set(w_sk.keys.keys())
        for wk2 in (foreign_keys-local_keys):
            self.keys[wk2] = w_sk.keys[wk2]
## end counter class

if __name__ == "__main__":
    print "Running test #1: sk additive merge"
    sk1 = statkeeper()
    sk2 = statkeeper()
    sk1.incKey('k1')
    sk1.incKey('k2')
    sk2.incKey('k1')
    sk2.incKey('k3')
    sk1.add_merge(sk2)
    sk1.add_merge(sk2)
    print sk1.getJSON()
    #

##