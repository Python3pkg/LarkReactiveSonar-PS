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

import sys, os
import csv
import subprocess
import time
import decimal

"""
This python wrapper module contains a mechanisms for interacting with the
perfSonar client libraries.  To generate HTML documentation for this module issue the
command:

    pydoc -w PerfSonarAccessor

"""

__author__ =  'Andrew B. Koerner'
__email__=  'AndrewKoerner.b@gmail.com'

class PerfSonarAccessor(object):

    globalLookupService = None
    projectName = None#"Internet2"
    currentSite = None#"larkps.chtc.wisc.edu"

    projectSiteList = None
    projectList = None
    siteEndPointPairList = None;
    currentThroughputResults = None;
    
    def __init__(self, projectName = "Internet2", globalLookupService = "http://ps4.es.net:9990/perfSONAR_PS/services/gLS"):
        
        """Set default attribute values only

        Keyword arguments:
        projectName -- The project name to initalize the PerfSonarAccessor with.  The default project name
        will be 'Internet 2' if none is provided.
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
            self.projectName = "Internet2"

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
        globalLookupService -- The address of the perfSonar Global Lookup Service to use.  In no address
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
        for project 'Wisconsin'
        
        Preconditions:
        NONE
        
        Postconditions:
        currentSite will be set

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
        return self.projectList

    def getCurrentThroughputResults(self):

        """Returns a list that is the current throughput results obtained by fetchThroughputResults see fetchThroughputResults
        documentation for more information.

        Keyword arguments:
        NONE
        
        Preconditions:
        Current throughput results must first be obtained by calling fetchThroughputResults
   
        Postconditions:
        NONE

        Throws:
        Excepiton if currentThroughputResults == None call fetchThroughputResults
        """

        if(self.currentThroughputResults == None):
            raise Exception("ERROR: currentThroughputResults not set try calling fetchThroughputResults") 
            return None
        return list(self.currentThroughputResults)

    def getSiteEndPointPairList(self):

        """Returns a list of endpoint pairs [source,destination] associated with the current site.  The 
        endpoint pair list must first be externally fetched.

        Keyword arguments:
        NONE
        
        Preconditions:
        The endpoint pair list must first be externally fetched by calling fetchSiteEndPointPairList.  See
        the documentation for fetchSiteEndPointPairList. 
   
        Postconditions:
        NONE

        Throws:
        Excepiton if siteEndPointPairList == None call fetchSiteEndPointPairList to prevent this
        """

        if(self.siteEndPointPairList == None):
            raise Exception("ERROR: siteEndPointPairList not set try fetchingSiteEndPointPairList") 
            return None
        return list(self.siteEndPointPairList)

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

        command = "perl get_ls_sitelist.pl"
        process = subprocess.Popen(command + " \"" + self.projectName + "\" " + self.globalLookupService, shell=True, stdout=subprocess.PIPE, cwd="perfSonar")
        stdout, stderr = process.communicate()
        self.projectSiteList = csv.DictReader(stdout.decode('ascii').splitlines(), delimiter='\n', skipinitialspace=True, fieldnames=['site'])
        self.projectSiteList = [r['site'] for r in self.projectSiteList]

    def fetchSiteEndPointPairList(self, startUnixTimestamp = 0, endUnixTimestamp = 0):

        """Fetches externally at the current site endpoint pair list.

        Keyword arguments:
        startUnixTimestamp -- beginning time range to fetch endpoint pair list for
        endUnixTimestamp -- ending time range to fetch endpoint pair list for
        
        Preconditions:
        currentSite must be set, this  can be done by callig setCurrentSite
        with a vaild site address.  If no site is set then 'perfSonar.unl.edu' will be used.
        
        Postconditions:
        siteEndPointPairList will be populated with endpoint pair data available by the current site.  This data is provided via
        the current site.

        Throws:
        NONE
        """

        if(startUnixTimestamp == 0 or endUnixTimestamp == 0):
            startUnixTimestamp = 0
            endUnixTimestamp = int(time.time())
        if(self.currentSite != ""):
            currentSite = "perfSonar.unl.edu"
        command = "perl get_ls_endpoint_pair.pl"
        command = command + " " + self.currentSite + " " + str(startUnixTimestamp) + " " + str(endUnixTimestamp)
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, cwd="perfSonar")
        stdout, stderr = process.communicate()
        self.siteEndPointPairList = csv.DictReader(stdout.decode('ascii').splitlines(), delimiter=' ', skipinitialspace=True, fieldnames=['source', 'destination'])
        #self.projectSiteList = [r['site'] for r in self.projectSiteList]

    def fetchThroughputResults(self, source, destination, secondsAgo):


        """Fetches externally at the current site throughput data as specified by the query.

        Keyword arguments:
        source -- perfSonar resource address for the source
        destination -- perfSonar resource address for the destination
        secondsAgo -- How many seconds in the past to fetch data for.
        
        Preconditions:
        currentSite must be set, this  can be done by callig setCurrentSite
        with a vaild site address.
        
        Postconditions:
        currentThroughputResults will be populated with throughput data specified in the source,
        destination and secondsAgo query.  This can be accessed by calling getCurrentThroughputResults. 

        Throws:
        If currentSite is None or empty then an exception is thrown.  This can be avoided by setting the current
        site call setCurrentSite with a vaild site address.
        """

        if(self.currentSite == "" or self.currentSite == None):
           raise Exception("ERROR: no site set try setCurrentSite(site)")
           return None
        if(secondsAgo == "" or secondsAgo == None):
           secondsAgo = 3600

        command = "perl get_throughput_results.pl"
        command = command + " " + self.currentSite + " " + source + " " + destination + " " + str(secondsAgo)
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, cwd="perfSonar")
        stdout, stderr = process.communicate()
        self.currentThroughputResults = csv.DictReader(stdout.decode('ascii').splitlines(), delimiter=',', skipinitialspace=True, fieldnames=['throughput', 'timeValue'])
        #self.projectSiteList = [r['site'] for r in self.projectSiteList]

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

        command = "perl get_gls_projects.pl"
        process = subprocess.Popen(command + " " + self.globalLookupService, shell=True, stdout=subprocess.PIPE, cwd="perfSonar")
        stdout, stderr = process.communicate()
        self.projectList = csv.DictReader(stdout.decode('ascii').splitlines(), delimiter=':', skipinitialspace=True, fieldnames=['type', 'project'])
        self.projectList = [r['project'] for r in self.projectList]

    def projectExists(self, projectName):

        """Returns true if the provided projectName as an argument exists in the global lookup service

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

