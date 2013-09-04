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
import etc.properties
import delegated.api
import rpki.ripeval_stats
import commons.getfile
import commons.dprint
import commons.utils

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

    try:
        # Setup argument parser
        parser = ArgumentParser(description=program_license, formatter_class=RawDescriptionHelpFormatter)
        # parser.add_argument("-r", "--recursive", dest="recurse", action="store_true", help="recurse into subfolders [default: %(default)s]")
        # parser.add_argument("-v", "--verbose", dest="verbose", action="count", help="set verbosity level [default: %(default)s]")
        parser.add_argument("-r", "--rir", dest="rir", help="RIR Name to process. [default: %(default)s]", metavar="RE" )
        parser.add_argument("-s", "--section", dest="section", help="stat section to generate. [default: %(default)s]", metavar="RE" )
        parser.add_argument('-V', '--version', action='version', version=program_version_message)
        # parser.add_argument(dest="paths", help="paths to folder(s) with source file(s) [default: %(default)s]", metavar="path", nargs='+')
        
        # Process arguments
        args = parser.parse_args()
        
        rir = args.rir
        section = args.section
                
        if not rir or not section:
            sys.stderr.write("Both rir and section MUST be defined.\n")
            raise CLIError("Both rir and section MUST be defined.")
        
        ## init logging
        dp = commons.dprint.dprint()
        
        ##
        # rpki per-country stats
        
        # get delegated
        dp.log("Downloading stat file for RIR %s..." % (rir))
        dlg_tmpfile = commons.utils.get_tmp_file_name("delegated-lacnic-latest")
        commons.getfile.getfile("ftp://ftp.lacnic.net/pub/stats/lacnic/delegated-lacnic-latest", dlg_tmpfile, 3600)
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
            drec = dlg_api.resource_find_inside(row['prefix'])
            if drec:
                if drec['cc'] == 'UY':
                    print row
            else:
                dp.log("\n ERROR: prefix :%s: should have been found in dlg file" % (row['prefix']))
        
        return 0
    
    except KeyboardInterrupt:
        ### handle keyboard interrupt ###
        return 0
    except Exception, e:
        if DEBUG or TESTRUN:
            raise(e)
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