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
from LarkReactiveSonar.common.StaticClass import StaticClass

"""

To generate HTML documentation for this issue the following command:

    pydoc -w PersistenceAssessor

"""

__author__ =  'Andrew B. Koerner'
__email__=  'AndrewKoerner.b@gmail.com'

class PersistenceAccessor(StaticClass):
    @staticmethod
    def setupStorageTree(path):
        try:
           if(os.path.isdir(path)):
               shutil.rmtree(path)
           os.makedirs(path)
        except OSError as exc: # Python >2.5
            if exc.errno == errno.EEXIST and os.path.isdir(path):
                pass
            else: raise


    @staticmethod
    def saveData(location, data):
        with open(location, 'wb') as file:
            cPickle.dump(data, file)

    @staticmethod
    def loadData(location):
        with open(location, 'rb') as file:
            return cPickle.load(file)

    @staticmethod
    def getDirectoryInfos(currentDir):
        infos = []
        for root, dirs, files in os.walk(currentDir): # Walk directory tree
            for f in files:
                infos.append(FileInfo(f,root))
        return infos