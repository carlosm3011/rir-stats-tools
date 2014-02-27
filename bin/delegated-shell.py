#!/usr/bin/env python2.7
'''
Created on Sep 25, 2013

@author: carlos
'''
import cmd
import readline
import sys
import os
import ipaddr

from argparse import ArgumentParser
from argparse import RawDescriptionHelpFormatter

import etc.properties
import etc.rirconfig
import delegated.api
import commons.getfile
import commons.dprint
import commons.utils
import commons.statkeeper

## definitions
program_license = "This program is provided AS IS. (c) Carlos Martinez, carlos@lacnic.net"
program_version = "0.1.1"
release_date = "2013-09-25"
changed_date = "2013-09-25"
program_version_message = "Version %s, released %s, changed %s" % (program_version, release_date, changed_date)

## delegated shell ##################################
class DelegatedShell(cmd.Cmd):
    
    intro = "Welcome to the Delegated-Stats shell. Type ? for help."
    # rir = 'lacnic'
    # prompt = "(dlg-%s: latest)" % (rir)
    env = dict()
    
    def __init__(self, w_rir='lacnic'):
        #self.dlgapi = w_dlg_api
        #super(DelegatedShell, self).__init__()
	self.rir = w_rir
    	self.prompt = "(dlg-%s: latest)" % (self.rir)
        self.do_load('latest')
        cmd.Cmd.__init__(self)
    
    def do_info(self, line):
        print "Hello! This is the delegated-shell version %s" % (program_version)
        print ""
        print "Table name is 'resources'"
        print "Column names are: %s" % ('TBC')
        print "(c) carlos@lacnic.net, released %s" % (release_date)
    #
    def do_EOF(self, line):
        return True
    #
    def do_echo(self, line):
        """
        Echo command, useful for inserting comments into output
        """
        print "%s" % (line)
        
    #
    def emptyline(self):
        pass
    
    #
    def do_select(self, line):
        """
        Perform a query against the in-memory sqlite3 database. The table name to be used is 'resources'.
        The syntax is as follows:
             select * from resources where <where clause>
        """
        sql = "select %s" % (line)
        rx = self.dlgapi.raw_query(sql, {'tblname': 'resources'})
        c = 0
        try:            
            for row in rx:
                if self.env.get('output','') == 'csv':
                    if c==0:
                        # print header
                        keys = dict(row).keys()
                        keys = [str(x) for x in keys]
                        print "|".join(keys)
                        
                    values = dict(row).values()
                    values = [str(x) for x in values]
                    print "|".join(values)
                else:
                    print "R%s: %s" % (c, dict(row) )
                c = c + 1
        except:
            # raise
            # print 
            print "Error - cmd was: %s " % (sql)
            
    # 
    def do_set(self, line):
        """
        Set operational parameters. Syntax is set var=value.
        Currently defined variables:
        - output = csv -- produces CSV output suitable for spreadsheets 
        """
        try:
            (var, value) = line.split("=")
            self.env[var] = value
            print "%s = %s" % (var, value)
        except:
            raise
            print "Error - cmd was set %s" % (line)
        
    # end
            
    #
    def do_load(self, line):
        """
        Load delegated-stats file and current RIR for given date (YYYYMMDD|latest)
        """
        # get delegated
        ddate = line
        dp.log("Downloading stat file for RIR %s, date %s..." % (self.rir, ddate))
        dlg_tmpfile = commons.utils.get_tmp_file_name("delegated-extended-%s-%s" % (self.rir, ddate))
        dlg_tmpfile = commons.getfile.getfile( etc.rirconfig.rir_config_data[rir]['dlge'][0] % (ddate), dlg_tmpfile, 43200)
        dp.log(" OK\n")
        
        dp.log("Importing delegated stats in memory... ")
        self.dlgapi = None
        self.dlgapi = delegated.api.Delegated(dlg_tmpfile)
        self.dlgapi.read_delegated()
        dp.log(" OK\n")
        
        self.prompt = "(dlg-%s: %s)" % (self.rir, ddate)
    # end          
        
#####################################################

## main
if __name__ == "__main__":
    # init environment
    
    ## init logging
    dp = commons.dprint.dprint()    
    
    # parse arguments
    # Setup argument parser
    parser = ArgumentParser(description=program_license, formatter_class=RawDescriptionHelpFormatter)
    parser.add_argument("-d", "--date", dest="date", help="Date or latest. [default: %(default)s]", metavar="DATE", default='latest' )
    parser.add_argument("-e", "--extra", dest="extra", help="Extra arguments to be passed to the DlgQuery instance. [default: %(default)s]", metavar="DATE", default=None )
    parser.add_argument("-r", "--rir", dest="rir", help="RIR Name to process. [default: %(default)s]", metavar="RIR", default='lacnic' )
    # parser.add_argument("-q", "--file-query", dest="filequery", help="Python-like query to be read from file and run via eval(). [default: %(default)s]", metavar="QUERY" )
    parser.add_argument('-V', '--version', action='version', version=program_version_message)
    parser.add_argument(dest="query", help="paths to folder(s) with source file(s) [default: %(default)s]", metavar="query", nargs='?')  
    
    args = parser.parse_args()  
    rir = args.rir      
    
    # start shell
    cli = DelegatedShell(rir)
    cli.cmdloop()
