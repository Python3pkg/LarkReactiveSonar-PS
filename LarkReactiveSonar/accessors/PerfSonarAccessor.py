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

#This is a simple python wrapper/bindings to a perl perfSonar abstraction layer.  This module enables easy interaction with perfSonar data including OWAMP, Throughtput, Project and site querying.  Read more about
#perfSonar at http://www.perfsonar.net/ and the Holland Computing Center at http://hcc.unl.edu/

import sys, os

#abspath = os.path.abspath(__file__)
#dname = os.path.dirname(abspath)
#os.chdir(dname)

import csv
import subprocess
import time
import decimal
import simplejson

"""
This python wrapper module contains a mechanisms for interacting with the
perfSonar client libraries in perl.  To generate HTML documentation for this module issue the
command:

    pydoc -w PerfSonarAccessor

"""

__author__ =  'Andrew B. Koerner'
__email__=  'AndrewKoerner.b@gmail.com'

class PerfSonarAccessor(object):

    globalLookupService = None
    projectName = None
    currentSite = None

    projectSiteList = None
    projectList = None

    siteEndPointPairListWithThroughputData = None;
    siteEndPointPairListWithOWAMPData = None;

    currentThroughputData = None;
    currentOWAMPData = None;

    def __init__(self, projectName = "Wisconsin", globalLookupService = "http://ps4.es.net:9990/perfSONAR_PS/services/gLS", autoProjectDiscoveryMode = False):
        
        """Set default attribute values only

        Keyword arguments:
        projectName -- The project name to initalize the PerfSonarAccessor with.  The default project name
        will be 'IWisconsin' if none is provided.
        globalLookupService -- The address of the perfSonar Global Lookup Service to use.  In no address
        is specified then 'http://ps4.es.net:9990/perfSONAR_PS/services/gLS' will be set as the gLs.

        Once initialized with a global lookup service and project the PerfSonarAccessor will externally 
        fetched from the global lookup service a list of available projects and all sites associated with
        the specified project.  To verify the project name the method  getProjectName with no arguments 
        can be called on any instance of a PerfSonarAccessor.  In the same manner that getProjectName can 
        be called the method getGlobalLookupService will return the current Global Lookup Service.  After 
        the constructor is invoked the methods getProjectList snd getProjectSiteList can be called to retrieve
        the populated lists mentioned above.

        Do not directly access class datamembers use the provided get/set methods.

        """

        if(globalLookupService != ""):
            self.globalLookupService = globalLookupService
        if(projectName != ""):
            self.projectName = projectName
 
        if(self.globalLookupService == None):
            self.globalLookupService = "http://ps4.es.net:9990/perfSONAR_PS/services/gLS"
        if(self.projectName == None):
            self.projectName = "Wisconsin"

        if(autoProjectDiscoveryMode):
            self.fetchProjectList()
        self.fetchProjectSiteList()

    def getGlobalLookupService(self):
        """Returns the Global Lookup Service

        Keyword arguments:
        NONE
        
        Preconditions:
        NONE
        
        Postconditions:
        NONE

        Throws:
        NONE
        """
        return self.globalLookupService

    def setGlobalLookupService(self, globalLookupService = "http://ps4.es.net:9990/perfSONAR_PS/services/gLS"):

        """Mutator/setter for the Global Lookup Service 

        Keyword arguments:
        globalLookupService -- The address of the perfSonar Global Lookup Service to use.  If no address
        is specified then 'http://ps4.es.net:9990/perfSONAR_PS/services/gLS' will be set as the gLs.
        
        Preconditions:
        NONE
        
        Postconditions:
        The projectList, projectSiteList and projectName will be reset to None.  After the global lookup service
        is mutated the project must be set.  This can be done by invoking setProjectName on any instance of the 
        PerfSonarAccessor with the desired project name as an argument.  A list of available projects maintained 
        by the global lookup service can be obtained by calling fetchProjectSiteList with no arguments on any 
        instance of a PerfSonarAccessor.  Before any throughput data can be obtained sites associated with a project
        must be known.  Available sites maintained by the specified Global Lookup Service can be externally fetched 
        by invoking fetchProjectSiteList on any instance of the PerfSonarAccessor.

        Throws:
        NONE
        """

        self.projectList = None
        self.projectSiteList = None
        self.projectName = None
        self.globalLookupService = globalLookupService

    def getProjectName(self):
        """Returns the Project Name

        Keyword arguments:
        NONE
        
        Preconditions:
        Project Name must be set
        
        Postconditions:
        NONE

        Throws:
        Excepiton if project == None
        """
        if(self.projectName == None):
            raise Exception("ERROR: Project not set the project and try again")
        return self.projectName

    def setProjectName(self, projectName):
        """Mutator/setter for the Project Name

        Keyword arguments:
        projectName -- name of the project e.g., 'Internet 2' or 'Wisconsin'.  This value is case sensitive
        and must be identical to the project as maintained by the provided global lookup service.  Spaces and 
        special charaters are significant e.g., 'Internet2' != 'Internet 2'. 
        
        Preconditions:
        NONE
        
        Postconditions:
        The PerfSonarAccessor project will be set to the project name provided and the projectSiteList will be 
        reset to none.  fetchProjectSiteList must be invoked after the project is changed see documentation for
        fetchProjectSiteList for more information.

        Throws:
        NONE
        """
        self.projectSiteList = None
        self.projectName = projectName

    def setCurrentSite(self, site):

        """Mutator/setter for the current site

        Keyword arguments:
        site -- address of the site to set the PerfSonarAccessor to e.g., 'larkps.chtc.wisc.edu', 'hcc-ps02.unl.edu' 
        for project 'Wisconsin'. A list of Global Lookup Services is maintained at http://www.perfsonar.net/gls.root.hints.
        
        Preconditions:
        NONE
        
        Postconditions:
        currentSite will be set.  the throughput and OWAMP end point pair list must be fetched once the currentSite is changed.

        Throws:
        NONE
        """

        self.currentSite = site

    def getProjectSiteList(self):

        """Returns a list of the project sites maintained by the global lookup service for the specified 
        project

        Keyword arguments:
        NONE
        
        Preconditions:
        The projectSiteList must be externally fetched at the global lookup service.  This is done
        when the PerfSonarAccessor is instantiated.  It must be manually done if the project name
        is altered by invoking fetchProjectSiteList on an instance of PerfSonarAccessor.
   
        Postconditions:
        NONE

        Throws:
        Excepiton if projectSiteList == None call fetchProjectSiteList to prevent this
        """

        if(self.projectSiteList == None):
            raise Exception("ERROR: projectSiteList not set do fetchProjectSiteList and try again") 
            return None
        return self.projectSiteList

    def getProjectList(self):

        """Returns a list of the projects maintained by the global lookup service

        Keyword arguments:
        NONE
        
        Preconditions:
        The projectList must be externally fetched at the global lookup service.  This is done
        when the PerfSonarAccessor is instantiated.  It must be manually done if the global lookup service
        is altered by invoking fetchProjectList on an instance of PerfSonarAccessor.
   
        Postconditions:
        NONE

        Throws:
        Excepiton if projectList == None call fetchProjectList to prevent this
        """

        if(self.projectList == None):
            raise Exception("ERROR: projectList not set try fetchingProjectList") 
            return None
        return self.projectList

    def getCurrentSite(self):

        """Returns the current site

        Keyword arguments:
        NONE
        
        Preconditions:
        The site must first be set by calling setCurrentSite with a site address.
   
        Postconditions:
        NONE

        Throws:
        Excepiton if currentSite == None call setCurrentSite with a site address to prevent this
        """

        if(self.currentSite == None):
            raise Exception("ERROR: currentSite not set try calling setCurrentSite") 
            return None
        return self.currentSite

    def fetchProjectList(self):

        """Fetches externally at the global lookup service the project list.

        Keyword arguments:
        NONE
        
        Preconditions:
        globalLookupService must be set, this is done at instantiation or can be done by callig setGlobalLookupService
        with a vaild global lookup service address
        
        Postconditions:
        projectList will be populated with projects maintained by the global lookup service.  This data is provided via
        the global lookup service.

        Throws:
        NONE
        """
        #EXAMPLE CALL:  perl -e 'require LarkSonar::Common; print LarkSonar::Common::get_gls_projects("http://ps4.es.net:9990/perfSONAR_PS/services/gLS");'

        command = "perl -e \'require LarkSonar::Common; print LarkSonar::Common::get_gls_projects(\""
        command += self.globalLookupService
        command += "\");\'"

        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
        stdout, stderr = process.communicate()
        self.projectList = simplejson.loads(stdout.decode('utf-8'))["project"]
        self.projectList = [str(element) for element in self.projectList]
        #self.projectList = csv.DictReader(stdout.decode('ascii').splitlines(), delimiter='\n', skipinitialspace=True, fieldnames=['project'])
        #self.projectList = list(self.projectList)

    def fetchProjectSiteList(self):

        """Fetches externally at the global lookup service the site list associated with the current set project

        Keyword arguments:
        NONE
        
        Preconditions:
        projectName must be set, this is done at instantiation or can be done by callig setProjectName
        with a vaild project name as indexed by the provided global lookup service
        
        globalLookupService must be set, this is done at instantiation or can be done by callig setGlobalLookupService
        with a vaild global lookup service address
        
        Postconditions:
        projectSiteList will be populated with sites associated with the current project.  This data is provided via
        the global lookup service

        Throws:
        NONE
        """

        #EXAMPLE CALL:  perl -e 'require LarkSonar::Common; print LarkSonar::Common::get_ls_sitelist("Wisconsin","http://ps4.es.net:9990/perfSONAR_PS/services/gLS");'

        command = "perl -e \'require LarkSonar::Common; print LarkSonar::Common::get_ls_sitelist(\""
        command += self.projectName
        command += "\",\""
        command += self.globalLookupService
        command += "\");\'"


        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
        stdout, stderr = process.communicate()
        self.projectSiteList = simplejson.loads(stdout.decode('utf-8'))["site"]
        self.projectSiteList = [str(element) for element in self.projectSiteList]
        #self.projectSiteList = csv.DictReader(stdout.decode('ascii').splitlines(), delimiter='\n', skipinitialspace=True, fieldnames=['site'])
        #self.projectSiteList = [r['site'] for r in self.projectSiteList]

    def getCurrentThroughputData(self):

        """Returns a list that is the current throughput data obtained by fetchThroughputData at the currently set site.  see fetchThroughputData
        documentation for more information.

        Keyword arguments:
        NONE
        
        Preconditions:
        Current throughput data must first be obtained by calling fetchThroughputData
   
        Postconditions:
        NONE

        Throws:
        Excepiton if currentThroughputData == None call fetchThroughputData
        """

        if(self.currentThroughputData == None):
            raise Exception("ERROR: currentThroughputData not set try calling fetchThroughputData") 
            return None
        return list(self.currentThroughputData)

    def getCurrentOWAMPData(self):

        """Returns a list that is the current OWAMP results obtained by fetchOWAMPData see fetchOWAMPData
        documentation for more information.

        Keyword arguments:
        NONE
        
        Preconditions:
        Current OWAMP results must first be obtained by calling fetchOWAMPData
   
        Postconditions:
        NONE

        Throws:
        Excepiton if currentOWAMPData == None call fetchOWAMPData
        """

        if(self.currentOWAMPData == None):
            raise Exception("ERROR: currentOWAMPData not set try calling fetchOWAMPData") 
            return None
        return list(self.currentOWAMPData)

    def getSiteEndPointPairListWithThroughputData(self):

        """Returns a list of endpoint pairs [source,destination] associated with the current site that has throughput data available.  The 
        endpoint pair list must first be externally fetched.

        Keyword arguments:
        NONE
        
        Preconditions:
        The endpoint pair list must first be externally fetched by calling fetchSiteEndPointPairListWithThroughputData.  See
        the documentation for fetchSiteEndPointPairListWithThroughputData. 
   
        Postconditions:
        NONE

        Throws:
        Excepiton if fetchSiteEndPointPairListWithThroughputData == None call fetchSiteEndPointPairListWithThroughputData to prevent this
        """

        if(self.siteEndPointPairListWithThroughputData == None):
            raise Exception("ERROR: siteEndPointPairListWithThroughputData not set") 
            return None
        return list(self.siteEndPointPairListWithThroughputData)

    def getSiteEndPointPairListWithOWAMPData(self):

        """Returns a list of endpoint pairs [source,destination] associated with the current site that has OWAMP data.  The 
        endpoint pair list must first be externally fetched by calling fetchSiteEndPointPairListWithOWAMPData.

        Keyword arguments:
        NONE
        
        Preconditions:
        The endpoint pair list must first be externally fetched by calling fetchSiteEndPointPairListWithOWAMPData.  See
        the documentation for fetchSiteEndPointPairListWithOWAMPData. 
   
        Postconditions:
        NONE

        Throws:
        Excepiton if siteEndPointPairListWithOWAMPData == None call fetchSiteEndPointPairListWithOWAMPData to prevent this
        """

        if(self.siteEndPointPairListWithOWAMPData == None):
            raise Exception("ERROR: currentOWAMPData not set") 
            return None
        return list(self.siteEndPointPairListWithOWAMPData)

    def fetchSiteEndPointPairListWithThroughputData(self):

        """Fetches externally at the current site endpoint pair list with throughtput data.

        Keyword arguments:
        NONE
        
        Preconditions:
        currentSite must be set, this  can be done by callig setCurrentSite
        with a vaild site address.  If no site is set then 'perfSonar.unl.edu' will be used.
        
        Postconditions:
        siteEndPointPairListWithThroughputData will be populated with endpoint pair list with throughtput data.  This data is provided via
        the current site.

        Throws:
        NONE
        """

        #EXAMPLE CALL: perl -e 'require LarkSonar::Common; print LarkSonar::Common::list_all_endpoints_with_throughput_data_available("hcc-ps02.unl.edu");'

        command = "perl -e \'require LarkSonar::Common; print LarkSonar::Common::list_all_endpoints_with_throughput_data_available(\""
        command += self.currentSite
        command += "\");\'"
 
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
        stdout, stderr = process.communicate()
        self.siteEndPointPairListWithThroughputData = simplejson.loads(stdout.decode('utf-8'))["endpoint_pair"]
        #self.siteEndPointPairListWithThroughputData = [str(element) for element in self.siteEndPointPairListWithThroughputData]
        #self.siteEndPointPairListWithThroughputData = csv.DictReader(stdout.decode('ascii').splitlines(), delimiter=' ', skipinitialspace=True, fieldnames=['source', 'destination'])

    def fetchSiteEndPointPairListWithOWAMPData(self):

        """Fetches externally at the current site end point pair list with OWAMP data available.

        Keyword arguments:
        NONE
        
        Preconditions:
        currentSite must be set, this  can be done by calling setCurrentSite
        with a vaild site address.
        
        Postconditions:
         siteEndPointPairListWithOWAMPData will be populated with throughput data specified in the source,
        destination and secondsAgo query.  This can be accessed by calling getCurrentThroughputResults. 

        Throws:
        If currentSite is None or empty then an exception is thrown.  This can be avoided by setting the current
        site call setCurrentSite with a vaild site address.
        """

        command = "perl list_all_endpoints_with_one_way_latency_data_available.pl"
        command = command + " " + self.currentSite

        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, cwd="perfSonar")
        stdout, stderr = process.communicate()

        self.siteEndPointPairListWithOWAMPData = csv.DictReader(stdout.decode('ascii').splitlines(), delimiter=' ', skipinitialspace=True, fieldnames=['source', 'destination'])

    def fetchThroughputData(self, source, destination, secondsAgo):


        """Fetches externally at the current site throughput data as specified by the query.

        Keyword arguments:
        source -- perfSonar resource hostname or address for the source
        destination -- perfSonar resource hostname or address for the destination
        secondsAgo -- How many seconds in the past to fetch data for.
        
        Preconditions:
        currentSite must be set, this  can be done by callig setCurrentSite
        with a vaild site address.
        
        Postconditions:
        currentThroughputData will be populated with throughput data specified in the source,
        destination and secondsAgo query.  This can be accessed by calling getCurrentThroughputData. 

        Throws:
        If currentSite is None or empty then an exception is thrown.  This can be avoided by setting the current
        site call setCurrentSite with a vaild site address.
        """

        if(self.currentSite == "" or self.currentSite == None):
           raise Exception("ERROR: no site set try setCurrentSite(site)")
           return None
        if(secondsAgo == "" or secondsAgo == None):
           secondsAgo = 3600

        now = int(time.time())

        #EXAMPLE CALL: perl -e 'require LarkSonar::Common; print LarkSonar::Common::get_throughput_between_two_endpoints("perfsonar02.hep.wisc.edu" ,"perfsonar02.hep.wisc.edu" , "perfsonar02.cmsaf.mit.edu", "1378000000", "1378410734");'

        command = "perl -e \'require LarkSonar::Common; print LarkSonar::Common::list_all_endpoints_with_throughput_data_available(\""
        command += self.currentSite
        command += "\",\""
        command += source
        command += "\",\""
        command += destination
        command += "\",\""
        command += secondsAgo
        command += "\",\""
        command += now
        command += "\");\'"

        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
        stdout, stderr = process.communicate()
        self.currentThroughputData = simplejson.loads(stdout.decode('utf-8'))["throughput_result"]
        #self.siteEndPointPairListWithThroughputData = [str(element) for element in self.siteEndPointPairListWithThroughputData]
        #self.currentThroughputData = csv.DictReader(stdout.decode('ascii').splitlines(), delimiter=',', skipinitialspace=True, fieldnames=['throughput', 'timestamp'])

    def fetchOWAMPData(self, source, destination, secondsAgo):


        """Fetches externally at the current site OWAMP data as specified by the query.

        Keyword arguments:
        source -- perfSonar resource hostname or address for the source
        destination -- perfSonar resource hostname or address for the destination
        secondsAgo -- How many seconds in the past to fetch data for.
        
        Preconditions:
        currentSite must be set, this  can be done by callig setCurrentSite
        with a vaild site address.
        
        Postconditions:
        currentOWAMPData will be populated with OWAMP data specified in the source,
        destination and secondsAgo query.  This can be accessed by calling getCurrentOWAMPData. 

        Throws:
        If currentSite is None or empty then an exception is thrown.  This can be avoided by setting the current
        site call setCurrentSite with a vaild site address.
        """

        if(self.currentSite == "" or self.currentSite == None):
           raise Exception("ERROR: no site set try setCurrentSite(site)")
           return None
        if(secondsAgo == "" or secondsAgo == None):
           secondsAgo = 3600

        command = "perl get_one_way_latency_between_two_endpoints.pl"
        command = command + " " + self.currentSite + " " + source + " " + destination + " " + str(secondsAgo)
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, cwd="perfSonar")
        stdout, stderr = process.communicate()
        self.currentOWAMPData = csv.DictReader(stdout.decode('ascii').splitlines(), delimiter=',', skipinitialspace=True, fieldnames=['duplicates', 'endTime', 'loss', 'maxError', 'maxTTL', 'max_delay', 'minTTL', 'min_delay', 'sent', 'startTime', 'timeType', 'value_buckets'])
        self.currentOWAMPData =  list(self.currentOWAMPData)
        for row in self.currentOWAMPData:
            value_buckets = row['value_buckets'].split(";")
            value_buckets_parsed = []
            try:
                for value_bucket in value_buckets:
                    print value_bucket
                    value_bucket = value_bucket.split(' ')
                    if len(value_bucket) > 0:
                        temp_val_bucket = {'count': value_bucket[0], 'value': value_bucket[1]}
                        value_buckets_parsed.append(temp_val_bucket)
                        print 'count:' + value_bucket[0] + 'value:' + value_bucket[1] + '\n'

                row['value_buckets'] = value_buckets_parsed
            except Exception: 
                pass

    def projectExists(self, projectName):

        """Returns true if the provided projectName as an argument exists in the global lookup service.

        Keyword arguments:
        projectName -- Name of project to verify with the global lookup service
        
        Preconditions:
        NONE
   
        Postconditions:
        NONE

        Throws:
        NONE
        """

        try:
            self.projectList.index(projectName)
            return True
        except:
            return False

