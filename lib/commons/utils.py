'''
Created on Sep 3, 2013

@author: marcelo
'''

import etc.properties
import tempfile
import os
import json

### begin
def get_tmp_file_name(w_name = None):
    '''
    returns a full path to a temp file name, using the current system properties
    if filename is None then a random name is created
    '''
    if w_name:
        fname = w_name
    else:
        tmp_fname = tempfile.NamedTemporaryFile().name
        fname = os.path.basename(tmp_fname)
    
    tmp_file = "%s/%s" % (etc.properties.paths['tmp'], fname)
    return tmp_file

### end

### begin
def json_load(w_file_name):
    fn = "%s/%s" % (etc.properties.srchome, w_file_name )
    try:
        cc_file = open(fn)
        cc_json = json.load(cc_file)
        return cc_json
    except:
        raise
        return "{'error': 'could not load file %s}'" % (fn)
### end json_load

if __name__ == "__main__":
    #for x in range(1,10):
    #    print "%s\n" % (get_tmp_file_name())
    print "not to be run directly"