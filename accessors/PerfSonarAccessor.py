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


class PerfSonarAccessor(object):

    globalLookupService = "http://ps4.es.net:9990/perfSONAR_PS/services/gLS"
    projectName = "Internet2"
    currentSite = "larkps.chtc.wisc.edu"

    projectSiteList = None
    projectList = None
    siteEndPointPairList = None;
    
    def __init__(self, globalLookupService, projectName):
        if(globalLookupService != ""):
            self.globalLookupService = globalLookupService
        if(projectName != ""):
            self.projectName = projectName

    def getGlobalLookupService(self):
        return self.globalLookupService

    def setGlobalLookupService(self, globalLookupService):
        self.globalLookupService = globalLookupService

    def getProjectName(self):
        return self.projectName

    def setProjectName(self, projectName):
        self.projectName = projectName

    def setCurrentSite(self, site):
        self.currentSite = site

    def getProjectSiteList(self):
        if(self.projectSiteList == None):
            raise Exception("ERROR: projectSiteList not set do fetchProjectSiteList and try again") 
            return None
        return self.projectSiteList

    def getProjectList(self):
        if(self.projectList == None):
            raise Exception("ERROR: siteList not set try fetchingProjectList") 
            return None
        return set(self.projectList)

    def getSiteEndPointPairList(self):
        if(self.siteEndPointPairList == None):
            raise Exception("ERROR: siteEndPointPairList not set try fetchingSiteEndPointPairList") 
            return None
        return list(self.siteEndPointPairList)

    def fetchProjectSiteList(self):
        command = "perl get_ls_sitelist.pl"
        process = subprocess.Popen(command + " \"" + self.projectName + "\" " + self.globalLookupService, shell=True, stdout=subprocess.PIPE, cwd="perfSonar")
        stdout, stderr = process.communicate()
        self.projectSiteList = csv.DictReader(stdout.decode('ascii').splitlines(), delimiter='\n', skipinitialspace=True, fieldnames=['site'])
        self.projectSiteList = [r['site'] for r in self.projectSiteList]
    def printProjectSiteList(self):
        if(self.siteProjectList == None):
            raise Exception("ERROR: siteList not set try fetchingProjectSiteList")
        else:
            for site in self.siteProjectList:
               print(site)

    def fetchSiteEndPointPairList(self, startUnixTimestamp, endUnixTimestamp):
        command = "perl get_ls_endpoint_pair.pl"
        command = command + " " + self.currentSite + " " + startUnixTimestamp + " " + endUnixTimestamp
        print command
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, cwd="perfSonar")
        stdout, stderr = process.communicate()
        self.siteEndPointPairList = csv.DictReader(stdout.decode('ascii').splitlines(), delimiter=' ', skipinitialspace=True, fieldnames=['source', 'destination'])
        #self.projectSiteList = [r['site'] for r in self.projectSiteList]
    
    def printSiteEndPointPairList(self):
        if(self.siteEndPointPairList == None):
            raise Exception("ERROR: siteEndPointPairList not set try fetchingSiteListEndPointPairList")
        else:
            for endPointPair in self.siteEndPointPairList:
               print(endPointPair)

    def fetchProjectList(self):
        command = "perl get_gls_projects.pl"
        process = subprocess.Popen(command + " " + self.globalLookupService, shell=True, stdout=subprocess.PIPE, cwd="perfSonar")
        stdout, stderr = process.communicate()
        self.projectList = csv.DictReader(stdout.decode('ascii').splitlines(), delimiter=':', skipinitialspace=True, fieldnames=['type', 'project'])
        self.projectList = [r['project'] for r in self.projectList]

    def printProjectList(self):
        if(self.projectList == None):
            raise Exception("ERROR: projectList not set try fetchingProjectList")
        else:
            for project in self.projectList:
               print(project)

    def projectExists(self, projectName):
        if(self.projectList == None):
            raise Exception("ERROR: projectList not set try fetchingProjectList")
        else:
            try:
                self.projectList.index(projectName)
                return True
            except:
                return False

