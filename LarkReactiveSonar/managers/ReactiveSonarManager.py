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

from LarkReactiveSonar.accessors.PerfSonarAccessor import PerfSonarAccessor
from LarkReactiveSonar.accessors.HTCondorAccessor import HTCondorAccessor
from LarkReactiveSonar.accessors.PersistenceAccessor import PersistenceAccessor
from LarkReactiveSonar.common.StaticClass import StaticClass
import itertools
"""

To generate HTML documentation for this issue the following command:

    pydoc -w ReactiveSonarManager

"""

__author__ =  'Andrew B. Koerner'
__email__=  'AndrewKoerner.b@gmail.com'

PERFSONAR_PROJECTS_HTCONDOR_ATTRIBUTE_KEYWORD = "PERFSONAR_PROJECTS"
PERFSONAR_PREFERRED_GLOBAL_LOOKUP_SERVICE_KEYWORD = "PERFSONAR_PREFERRED_GLOBAL_LOOKUP_SERVICE"
PROJECT_DISCOVERY_MODE = False
PREFERRED_PERF_SONAR_GLOBAL_LOOKUP_SERVICE = "http://ps4.es.net:9990/perfSONAR_PS/services/gLS"
ROOT_CACHE_DIRECTORY = "~/cache"
SECONDS_AGO_TO_CACHE = 28800# 8 hours


class ReactiveSonarManager(StaticClass):

    @staticmethod
    def cachePerfSonarData():

        perfSonarProjects = []
        perfSonarAccessors = []
        tempPerfSonarAccessor = None
        tempProjectSiteList = []
        tempSiteEndPointPairListWithThroughputData = []
        throughputData = []


        #get the project names of interest to condor
        perfSonarProjects = HTCondorAccessor.getHTCondorConfigAttribute(PERFSONAR_PROJECTS_HTCONDOR_ATTRIBUTE_KEYWORD)
        
        #initialize data storage file structure for the throughput data
        PersistenceAccessor.setupStorageTree(ROOT_CACHE_DIRECTORY)

        #iterate over all projects of intrest to condor
        for perfSonarProject in perfSonarProjects:

            #iinstantiate a perfSonarAccessor for the project
            tempPerfSonarAccessor = PerfSonarAccessor(perfSonarProject, PREFERRED_PERF_SONAR_GLOBAL_LOOKUP_SERVICE, PROJECT_DISCOVERY_MODE)
            
            #get the list of sites associated with the project
            tempProjectSiteList = tempPerfSonarAccessor.getProjectSiteList()

            #iterate over the sites associated with the project
            for site in tempProjectSiteList:

                #get endpoint pair list for the site that has associated throughput data available
                tempPerfSonarAccessor.setCurrentSite(site)
                tempPerfSonarAccessor.fetchSiteEndPointPairListWithThroughputData()
                tempSiteEndPointPairListWithThroughputData = tempPerfSonarAccessor.getSiteEndPointPairListWithThroughputData()

                #iterate over endpoint pair list
                for endpointPairWithThroughputData in tempSiteEndPointPairListWithThroughputData:
                    tempPerfSonarAccessor.fetchThroughputData(endpointPairWithThroughputData["source"], endpointPairWithThroughputData["destination"], SECONDS_AGO_TO_CACHE)
                    print tempPerfSonarAccessor.getCurrentThroughputData()
            perfSonarAccessors.append(tempPerfSonarAccessor)

         



        return perfSonarAccessors;