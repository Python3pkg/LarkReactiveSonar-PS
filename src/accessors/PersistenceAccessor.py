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
import shutil
import PerfSonarAccessor
import cPickle

"""

To generate HTML documentation for this issue the following command:

    pydoc -w PersistenceAssessor

"""

__author__ =  'Andrew B. Koerner'
__email__=  'AndrewKoerner.b@gmail.com'

class PersistenceAccessor:
    @classmethod
    def setupStorageTree(self, treeRoot):
        try: 
           shutil.rmtree(treeRoot)
           os.makedirs(treeRoot)
        except Exception, exception:
            print exception

    @classmethod
    def isStorageTreeLocked(self, treeRoot):
        return os.path.isfile(treeRoot+"/lock")

    @classmethod
    def lockStorageTree(self, treeRoot, lock):
        if(lock):
            PersistenceAccessor.touch(treeRoot+"/lock")
        else:
            os.remove(treeRoot+"/lock")

    @classmethod
    def touch(self, path):
        with open(path, 'a'):
            os.utime(path, None)

    @classmethod
    def saveData(self, location, data):
        with open(location, 'wb') as file:
            cPickle.dump(data, file)

    @classmethod
    def loadData(self, location):
        with open(location, 'rb') as file:
            return cPickle.load(file)