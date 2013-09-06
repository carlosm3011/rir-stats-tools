#!/usr/local/bin/python2.7
# encoding: utf-8
'''
RPKI-STATS.py: Calculate different RPKI Stats

It defines classes_and_methods

@author:     Carlos Martinez
        
@copyright:  2013 LACNIC. All rights reserved.
        
@license:    license

@contact:    carlos@lacnic.net
@deffield    updated: Updated
'''

import sys
import os
import ipaddr
import etc.properties
import delegated.api
import rpki.ripeval_stats
import commons.getfile
import commons.dprint
import commons.utils
import commons.statkeeper

from argparse import ArgumentParser
from argparse import RawDescriptionHelpFormatter

__all__ = []
__version__ = 0.1
__date__ = '2013-09-04'
__updated__ = '2013-09-04'

DEBUG = 1
TESTRUN = 0
PROFILE = 0

class CLIError(Exception):
    '''Generic exception to raise and log different fatal errors.'''
    def __init__(self, msg):
        super(CLIError).__init__(type(self))
        self.msg = "E: %s" % msg
    def __str__(self):
        return self.msg
    def __unicode__(self):
        return self.msg

def main(argv=None): # IGNORE:C0111
    '''Command line options.'''
    
    if argv is None:
        argv = sys.argv
    else:
        sys.argv.extend(argv)

    program_name = os.path.basename(sys.argv[0])
    program_version = "v%s" % __version__
    program_build_date = str(__updated__)
    program_version_message = '%%(prog)s %s (%s)' % (program_version, program_build_date)
    program_shortdesc = __import__('__main__').__doc__.split("\n")[1]
    program_license = '''%s

  Created by carlos@lacnic.net on %s.
  Copyright 2013 LACNIC. All rights reserved.
  
  Licensed under the Apache License 2.0
  http://www.apache.org/licenses/LICENSE-2.0
  
  Distributed on an "AS IS" basis without warranties
  or conditions of any kind, either express or implied.

USAGE
''' % (program_shortdesc, str(__date__))

    program_banner = '''
        (c) Carlos M. Martinez, carlos@lacnic.net, 2013-09-05
        version %s\n
    ''' % (program_version_message)

    try:
        print "*** RPKI Stats Tooling\n"
        print program_banner
        # Setup argument parser
        parser = ArgumentParser(description=program_license, formatter_class=RawDescriptionHelpFormatter)
        # parser.add_argument("-r", "--rir", dest="rir", help="RIR Name to process. [default: %(default)s]", metavar="RIR" )
        parser.add_argument("-q", "--file-query", dest="filequery", help="Python-like query to be read from file and run via eval(). [default: %(default)s]", metavar="QUERY" )
        parser.add_argument('-V', '--version', action='version', version=program_version_message)
        parser.add_argument(dest="query", help="paths to folder(s) with source file(s) [default: %(default)s]", metavar="query", nargs='?')
        
        # Process arguments
        args = parser.parse_args()
        
        # rir = args.rir
        rir = 'lacnic'
        if args.query:
            query = " ".join(args.query)
        else:
            query = None
            
        ## if queryfile specified, we run the file and check for the expected functions and values
        if args.filequery:
            filequery = args.filequery
            fq_locals = {}
            execfile(filequery, globals(), fq_locals )
            try:
                rq_class = fq_locals['RoaQuery']
                roa_query_in = rq_class()
            except:
                raise
            #===================================================================
            # if not type(myloc.get('roa_test', None)):
            #     print myloc, myloc.get('roa_test')
            #     raise CLIError("Function roa_test not found in file %s" % (queryfile))
            # if not myloc.get('roa_match', None):
            #     myloc['roa_match'] = lambda x,y:True
            # if type(myloc.get('roa_no_match') != type(lambda x:x)):
            #     myloc['roa_no_match'] = lambda x,y:True
            #===================================================================
                
        if not query and not filequery:
            sys.stderr.write("Either query or filequery MUST be defined.\n")
            raise CLIError("Either query or filequery MUST be defined.\n")
        
        ## init logging
        dp = commons.dprint.dprint()
        
        # init local stats
        sk = commons.statkeeper.statkeeper()
        
        # get delegated
        dp.log("Downloading stat file for RIR %s..." % (rir))
        dlg_tmpfile = commons.utils.get_tmp_file_name("delegated-lacnic-latest")
        commons.getfile.getfile("ftp://ftp.lacnic.net/pub/stats/lacnic/delegated-lacnic-latest", dlg_tmpfile, 43200)
        dp.log(" OK\n")
        
        dp.log("Importing delegated stats in memory... ")
        dlg_api = delegated.api.Delegated(dlg_tmpfile)
        dlg_api.read_delegated()
        dp.log(" OK\n")        
        
        dp.log("Dowloading validator output... ")
        dlg_tmpfile = commons.utils.get_tmp_file_name("lacnic-roa-prefixes.csv")
        commons.getfile.getfile("http://ripeval.labs.lacnic.net/rpki/batch-validation/latest/lacnic.tal-roa-prefixes.csv", dlg_tmpfile, 3600)        
        dp.log(" OK\n")
        
        dp.log("Importing RIPE validator output for RIR %s... " % (rir))
        ripeval_stats = rpki.ripeval_stats.BatchValidationResults()
        ripeval_stats.read_csv(dlg_tmpfile)
        dp.log(" OK\n")
        
        ## process ROAs
        rx = ripeval_stats.query("1=1", {})
        for row in rx:
            sk.incKey('ripeval-proc-rows')
            pfx1 = ipaddr.IPNetwork(row['prefix'])
            pfx2 = ipaddr.IPNetwork(pfx1.network)
            drec = dlg_api.resource_find_inside(str(pfx2))
            if drec:
                if roa_query_in:
                    if roa_query_in.roa_test(drec):
                        sk.incKey('matched-rows')
                        roa_query_in.roa_match(drec, row)
                    else:
                        sk.incKey('non-matched-rows')
                        roa_query_in.roa_no_match(drec, row)
                elif query:
                    if eval(query, None, drec):
                        print "prefix %s, alloc_pfx %s, origin_as %s, cc %s" % (row['prefix'], drec['prefix'], row['origin_as'], drec['cc'])
                        sk.incKey('matched-rows')
                else:
                    sk.incKey('non-matched-rows')
                    pass
            else:
                sk.incKey('rows-not-found-in-dlg')
                dp.log("\n ERROR: prefix :%s: should have been found in dlg file\n" % (row['prefix']))
        ## end for
        roa_query_in.finalize()
        
        print "\n\nRun Stats:\n"
        print sk
        
        print "*** END Run\n"
        return 0
    
    except KeyboardInterrupt:
        ### handle keyboard interrupt ###
        return 0
    except Exception as e:
        if DEBUG or TESTRUN:
            print e.message
            raise e
        indent = len(program_name) * " "
        sys.stderr.write(program_name + ": " + repr(e) + "\n")
        sys.stderr.write(indent + "  for help use --help\n")
        return 2

if __name__ == "__main__":
    if DEBUG:
        # sys.argv.append("-h")
        pass
    if TESTRUN:
        import doctest
        doctest.testmod()
    if PROFILE:
        import cProfile
        import pstats
        profile_filename = '_profile.txt'
        cProfile.run('main()', profile_filename)
        statsfile = open("profile_stats.txt", "wb")
        p = pstats.Stats(profile_filename, stream=statsfile)
        stats = p.strip_dirs().sort_stats('cumulative')
        stats.print_stats()
        statsfile.close()
        sys.exit(0)
    sys.exit(main())