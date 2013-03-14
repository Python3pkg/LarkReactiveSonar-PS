#!/usr/bin/env python
import sys, os, subprocess
import csv


#var = os.system('perl perfSonar_test.pl');
#print var
from subprocess import Popen, PIPE
command = 'perl get_ls_sitelist.pl'
argument = 'Internet2'

process = subprocess.Popen([command, argument], shell=True, stdout=subprocess.PIPE)
stdout, stderr = process.communicate()

reader = csv.DictReader(stdout.decode('ascii').splitlines(), delimiter=' ', skipinitialspace=True, fieldnames=['perfSonar Resource URL'])

for row in reader:
    print(row)
