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
import os
from datetime import datetime
from dateutil import tz
import decimal
"""

To generate HTML documentation for this issue the following command:

    pydoc -w ReactiveSonarManager

"""

__author__ =  'Andrew B. Koerner'
__email__=  'AndrewKoerner.b@gmail.com'

PERFSONAR_PROJECTS_HTCONDOR_ATTRIBUTE_KEYWORD = "PERFSONAR_PROJECTS"
PERFSONAR_PREFERRED_GLOBAL_LOOKUP_SERVICE_KEYWORD = "PERFSONAR_PREFERRED_GLOBAL_LOOKUP_SERVICE"

PROJECT_DISCOVERY_MODE = False
PREFERRED_PERFSONAR_GLOBAL_LOOKUP_SERVICE = "http://ps4.es.net:9990/perfSONAR_PS/services/gLS"
ROOT_CACHE_DIRECTORY = "perfSonarCache"
SECONDS_AGO_TO_CACHE = 7200
PERFSONAR_CLASSAD_NAME = ""
PERFSONAR_CLASSAD_TYPE = "PerfSonar"

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
            
            #print perfSonarProject
            try:
                #iinstantiate a perfSonarAccessor for the project
                tempPerfSonarAccessor = PerfSonarAccessor(perfSonarProject, PREFERRED_PERFSONAR_GLOBAL_LOOKUP_SERVICE, PROJECT_DISCOVERY_MODE)
            except:
                 #no project results
                 print("Empty perfSonar Project: "+perfSonarProject)
                 continue

            #make dir for project
            PersistenceAccessor.setupStorageTree(ROOT_CACHE_DIRECTORY+"/"+tempPerfSonarAccessor.getProjectName())
            
            #get the list of sites associated with the project
            tempProjectSiteList = tempPerfSonarAccessor.getProjectSiteList()

            #iterate over the sites associated with the project
            for site in tempProjectSiteList:

                #get endpoint pair list for the site that has associated throughput data available
                tempPerfSonarAccessor.setCurrentSite(site)
                tempPerfSonarAccessor.fetchSiteEndPointPairListWithThroughputData()
                tempSiteEndPointPairListWithThroughputData = tempPerfSonarAccessor.getSiteEndPointPairListWithThroughputData()

                #make dir for site
                tempSitePath = ROOT_CACHE_DIRECTORY+"/"+tempPerfSonarAccessor.getProjectName()+"/"+tempPerfSonarAccessor.getCurrentSite()
                PersistenceAccessor.setupStorageTree(tempSitePath)

                #make dir for throughput data
                PersistenceAccessor.setupStorageTree(tempSitePath+"/throughput")
                #make dir for owamp data
                PersistenceAccessor.setupStorageTree(tempSitePath+"/owamp")

                #iterate over endpoint pair list
                for endpointPairWithThroughputData in tempSiteEndPointPairListWithThroughputData:
                    if(endpointPairWithThroughputData["source"] != None and endpointPairWithThroughputData["destination"] != None):
                        tempPerfSonarAccessor.fetchThroughputData(endpointPairWithThroughputData["source"], endpointPairWithThroughputData["destination"], SECONDS_AGO_TO_CACHE)
                        tempEndpointPairFileName = "source_"+endpointPairWithThroughputData["source"]+"_destination_"+endpointPairWithThroughputData["destination"]
                        PersistenceAccessor.saveData(tempSitePath+"/throughput/"+tempEndpointPairFileName, tempPerfSonarAccessor.getCurrentThroughputData())
            perfSonarAccessors.append(tempPerfSonarAccessor)

    @staticmethod
    def pushCachedPerfSonarDataToHTCondor():

        timezone = tz.tzutc()
        lastThroughputResult = {'throughput':0, 'timestamp':''}
        infos = PersistenceAccessor.getDirectoryInfos("perfSonarCache")
        datum = []
        for info in infos:
            path = info[0]
            file = info[1]
            absoluteFilePath = path+"/"+file
            pathSplit = path.split("/")
            fileSplit = file.split("_")

            project = pathSplit[1]
            site = pathSplit[2]
            source = fileSplit[1]
            destination = fileSplit[3]

            throughputResults = PersistenceAccessor.loadData(absoluteFilePath)
            decimal.getcontext().prec=4

            sum = decimal.Decimal(0)
            average = decimal.Decimal(0)
            

            for throughputResult in throughputResults:

                sum += decimal.Decimal(str(throughputResult["throughput"]))
                lastThroughputResult = throughputResult

            if(len(throughputResults)>0):
              average = sum/decimal.Decimal(len(throughputResults))

            data = {}
            
            
            data["PerfSonarProject"] = project
            data["PerfSonarSite"] = site
            data["Source"] = source
            data["Destination"] = destination

            data["AverageThroughput"] = str(average.normalize())
            data["MostRecentThroughput"] = str(lastThroughputResult["throughput"])
            data["MostRecentThroughputTimestamp"] = str(lastThroughputResult["timestamp"])

            data["AverageLatency"] = "0"
            data["MostRecentLatency"] = "0"
            data["TimePeriodForAverages"] = str(SECONDS_AGO_TO_CACHE)
            if average != 0:
                datum.append(data)
                print(average)

        HTCondorAccessor.newClassAds(datum, PERFSONAR_CLASSAD_TYPE)