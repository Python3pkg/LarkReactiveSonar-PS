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
from PerfSonarAccessor import PerfSonarAccessor
from HTCondorAccessor import HTCondorAccessor

"""

To generate HTML documentation for this issue the following command:

    pydoc -w ReactiveSonarManager

"""

__author__ =  'Andrew B. Koerner'
__email__=  'AndrewKoerner.b@gmail.com'

PERFSONAR_PROJECTS_HTCONDOR_ATTRIBUTE_KEYWORD = "PERFSONAR_PROJECTS"

class ReactiveSonarManager(object):

    projects = []
    perfSonarAccessors = []
    preferredPerfSonarGLS = None



    def __init__(self):

        self.projects = HTCondorAccessor.getHTCondorConfigAttribute(PERFSONAR_PROJECTS_HTCONDOR_ATTRIBUTE_KEYWORD)

        for project in self.projects:
            self.perfSonarAccessors = PerfSonarAccessor(project, self.preferredPerfSonarGLS)