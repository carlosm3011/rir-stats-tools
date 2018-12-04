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
Created on Sep 16, 2013

@author: carlos
'''

from commons.utils import json_load

# rirs and their files
rir_config_data = { 'lacnic': 
                        {'dlg1': ["ftp://ftp.lacnic.net/pub/stats/lacnic/delegated-lacnic-%s", "data/delegated-lacnic-latest"],
                         'dlge': ["ftp://ftp.lacnic.net/pub/stats/lacnic/delegated-lacnic-extended-%s", "data/delegated-lacnic-extended-latest"],
                         'roaexport': ['http://mvuy10.labs.lacnic.net/rpki/batch-validation/%s/lacnic.tal-roa-prefixes.csv'],
                         'countrydata': json_load('etc/lacnic_region.json')
                        },
                    'afrinic':
                        {'dlg1': ["ftp://ftp.lacnic.net/pub/stats/afrinic/delegated-afrinic-%s", "data/delegated-afrinic-latest"],
                         'dlge': ["ftp://ftp.lacnic.net/pub/stats/afrinic/delegated-afrinic-extended-%s", "data/delegated-afrinic-extended-latest"],
                         'roaexport': ['http://mvuy10.labs.lacnic.net/rpki/batch-validation/%s/afrinic.tal-roa-prefixes.csv']
                         },
                    'apnic':
                        {'dlg1': ["ftp://ftp.lacnic.net/pub/stats/apnic/delegated-apnic-%s", "data/delegated-apnic-latest"],
                         'dlge': ["ftp://ftp.lacnic.net/pub/stats/apnic/delegated-apnic-extended-%s", "data/delegated-apnic-extended-latest"] ,
                         'roaexport': ['http://mvuy10.labs.lacnic.net/rpki/batch-validation/%s/apnic.tal-roa-prefixes.csv'],
                        },                    
                    'ripencc':
                        {'dlg1': ["ftp://ftp.lacnic.net/pub/stats/ripencc/delegated-ripencc-%s", "data/delegated-ripencc-latest"], 
                         'dlge': ["ftp://ftp.lacnic.net/pub/stats/ripencc/delegated-ripencc-extended-%s", "data/delegated-ripencc-extended-latest"],
                         'roaexport': ['http://mvuy10.labs.lacnic.net/rpki/batch-validation/%s/ripe-ncc.tal-roa-prefixes.csv'],
                         'countrydata': json_load('etc/ripencc_region.json')
                    },
                    'arin':
                        {'dlg1': ["ftp://ftp.arin.net/pub/stats/arin/delegated-arin-%s", "data/delegated-arin-latest"],
                         'dlge': ["ftp://ftp.arin.net/pub/stats/arin/delegated-arin-extended-%s", "data/delegated-arin-extended-latest"],
                         'roaexport': ['http://mvuy10.labs.lacnic.net/rpki/batch-validation/%s/arin.tal-roa-prefixes.csv'],
                         'countrydata': json_load('etc/arin_region.json')                         
                         },                    
                    'lacnic_br':
                        {'dlg1': ["ftp://ftp.registro.br/pub/stats/delegated-ipv6-nicbr-latest", "data/delegated-ipv6-nicbr-latest"],
                         },                                                                
                 }

enabled_rirs = ['lacnic', 'afrinic', 'arin', 'ripencc', 'apnic']
# enabled_rirs = ['apnic']



if __name__ == "__main__":
    print "Not to be run directly."

#
