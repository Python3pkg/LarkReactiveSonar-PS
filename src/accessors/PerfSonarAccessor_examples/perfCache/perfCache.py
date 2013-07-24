#!/usr/bin/env python

# copyright 2013 UNL Holland Computing Center
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#     you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#  
#        http://www.apache.org/licenses/LICENSE-2.0
#  
#    Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

#This script takes the projects located in the "projects" file and pulls all of the sites for the projects.
#Each site is interrogated for test data.  For each end point pair a file is created in the cache directory.  
#Every time this is run the cache dir is cleared.  
#
#
import sys, os
import getopt
import PerfSonarAccessor

"""

To generate HTML documentation for this issue the following command:

    pydoc -w PerfSonarAccessor

"""

__author__ =  'Andrew B. Koerner'
__email__=  'AndrewKoerner.b@gmail.com'



def cache_perfsonar_data():
    if setup():
        projects = get_projects()
        print os.getcwd()
        for project in projects:
            perfSonarAccessor = PerfSonarAccessor.PerfSonarAccessor(project)
            print perfSonarAccessor.getProjectSiteList()

def setup():

    # returns true on successful setup false on a falure.  A falure could be caused by falure to make a 
    #cache directory or other io exception.
    
    cache_directory = "cache"

    try:
        #first check if the cache directory exists if so clear the cache directory of stale data
        #otherwise make a cache directory.
        if os.path.exists('cache'):
            #clear dir
            for the_file in os.listdir(cache_directory):
                file_path = os.path.join(cache_directory, the_file)
                if os.path.isfile(file_path):
                    os.unlink(file_path)
        else:
            #try to create dir
            os.makedirs(cache_directory)
        return True
    except Exception, exception:
        print exception
        return False

def get_projects():
    return filter(None, [line.strip() for line in open('projects')])

class Usage(Exception):
    def __init__(self, msg):
        self.msg = msg

def main(argv=None):
    if argv is None:
        argv = sys.argv
    try:
        try:
            opts, args = getopt.getopt(argv[1:], "h", ["help"])
            cache_perfsonar_data()
        except getopt.error, msg:
             raise Usage(msg)
    except Usage, err:
        print >>sys.stderr, err.msg
        print >>sys.stderr, "for help use --help"
        return 2

if __name__ == "__main__":
    sys.exit(main())
