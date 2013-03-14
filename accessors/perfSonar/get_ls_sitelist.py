#!/usr/bin/env python
import sys, os
import csv
import getopt
import subprocess
import time



def get_ls_sitelist(project_name, gLs):
    command = "perl get_ls_sitelist.pl"

    if(gLs == ""):
        process = subprocess.Popen(command + " " +project_name, shell=True, stdout=subprocess.PIPE)
    else:
        process = subprocess.Popen(command + " " + project_name + " " + gLs, shell=True, stdout=subprocess.PIPE)


    syms = ['\\', '|', '/', '-']
    bs = '\b'
    print "Working...\\",
    while process.poll() is None:
        for sym in syms:
            sys.stdout.write("\b%s" % sym)
            sys.stdout.flush()
            time.sleep(.1)
    stdout, stderr = process.communicate()
    reader = csv.DictReader(stdout.decode('ascii').splitlines(), delimiter=' ', skipinitialspace=True, fieldnames=['site'])

    for row in reader:
       print(row)
    return reader

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
                if(len(args)>1):
                    return get_ls_sitelist(args[0], args[1])
                else:
                    return get_ls_sitelist(args[0], "")
        except getopt.error, msg:
             raise Usage(msg)
    except Usage, err:
        print >>sys.stderr, err.msg
        print >>sys.stderr, "for help use --help"
        return 2

if __name__ == "__main__":
    sys.exit(main())





