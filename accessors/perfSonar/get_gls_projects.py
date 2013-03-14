#!/usr/bin/env python
import sys, os
import csv
import getopt
import subprocess
import time



def get_gls_projects(gLs):
    command = "perl get_gls_projects.pl"
    process = subprocess.Popen(command + " " +gLs, shell=True, stdout=subprocess.PIPE)
	
    syms = ['\\', '|', '/', '-']
    bs = '\b'
    print "Working...\\",
    while process.poll() is None:
        for sym in syms:
            sys.stdout.write("\b%s" % sym)
            sys.stdout.flush()
            time.sleep(.1)
    stdout, stderr = process.communicate()
    print stdout
    reader = csv.DictReader(stdout.decode('ascii').splitlines(), delimiter=' ', skipinitialspace=True, fieldnames=['project'])

    for row in reader:
       print(row)
    #return reader

class Usage(Exception):
    def __init__(self, msg):
        self.msg = msg

def main(argv=None):
    if argv is None:
        argv = sys.argv
    try:
        try:
            opts, args = getopt.getopt(argv[1:], "h", ["help"])
            if(len(args) > 0):
                return get_gls_projects(args[0])
            else:
                return get_gls_projects("")
        except getopt.error, msg:
             raise Usage(msg)
    except Usage, err:
        print >>sys.stderr, err.msg
        print >>sys.stderr, "for help use --help"
        return 2

if __name__ == "__main__":
    sys.exit(main())





