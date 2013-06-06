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

import re
import sys, os
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)
import socket

sys.path.append('../../accessors')
import urllib2
import BeautifulSoup
import PerfSonarAccessor

"""
This python module contains a mechanisms and assorted methods for lark tasks
To generate HTML documentation for this module issue the
command:

    pydoc -w LarkUtilities

"""

__author__ =  'Andrew B. Koerner'
__email__=  'AndrewKoerner.b@gmail.com'

class LarkUtilities(object):

    @staticmethod
    def normalizeWhitespace(str):
        import re
        str = str.strip()
        str = re.sub(r'\s+', ' ', str)
        return str
    
    @staticmethod
    def locatePerfSonarInstances(ISO_3166CountryCode, perfSonarProjectName):

        matchingCountryPerfSonarList = []
        perfSonarAccessor = PerfSonarAccessor.PerfSonarAccessor(perfSonarProjectName)
        perfSonarResources = perfSonarAccessor.getProjectSiteList()

        for perfSonarResource in perfSonarResources:
            isIp = re.match("^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$", perfSonarResource)
            #print perfSonarResource
            if isIp:
                currentIP = perfSonarResource
            else:
                try:
                    currentIP = socket.gethostbyname(perfSonarResource)
                except:
                    continue
                    #currentIP = socket.getaddrinfo(perfSonarResource, None, socket.AF_INET6)
                    #print socket.getfqdn(currentIP)


            currentISO_3166_1_ALPHA_2_CountryCode = LarkUtilities.ISO_3166_1_ALPHA_2_IpAddressGeoLocate(currentIP)
            tempTouple = (perfSonarResource, currentISO_3166_1_ALPHA_2_CountryCode)
            #print tempTouple
            if currentISO_3166_1_ALPHA_2_CountryCode == None:
                continue
            if currentISO_3166_1_ALPHA_2_CountryCode[0] == None:
                continue
            #print ISO_3166CountryCode.lower() + " = " + currentISO_3166_1_ALPHA_2_CountryCode[0].lower() + " : " + ISO_3166CountryCode.lower() == currentISO_3166_1_ALPHA_2_CountryCode[0].lower()
            if ISO_3166CountryCode.lower() == currentISO_3166_1_ALPHA_2_CountryCode[0].lower():
                matchingCountryPerfSonarList.append(tempTouple)
        
        print perfSonarResources
        #print matchingCountryPerfSonarList
        return matchingCountryPerfSonarList
    
    @staticmethod
    def ISO_3166_1_ALPHA_2_IpAddressGeoLocate(ipAddress):

        try:
            geody = "http://www.geody.com/geoip.php?ip=" + ipAddress
            htmlDocument = urllib2.urlopen(geody).read()
            soup = BeautifulSoup.BeautifulSoup(htmlDocument)
            paragraph = soup('p')[3]
            geo_txt = re.sub(r'<.*?>', '', str(paragraph))
        except:
            print htmlDocument
            return
        haystack = []
        dname = os.path.dirname(abspath)
        os.chdir(dname)
        
        lines = open("ISO_3166-1-alpha-2.txt", 'r').readlines()
        for line in lines:
            haystack.append(line.strip().split('\t',1))

        needle = geo_txt[32:].upper().strip()

        haystack = list(haystack)
        for index, key in enumerate(haystack):
            if  LarkUtilities.normalizeWhitespace(haystack[index][1]) in LarkUtilities.normalizeWhitespace(needle):
                tuple = (haystack[index][0], haystack[index][1], needle);
                return tuple

    #@staticmethod
    #def whois(ipAddressOrHostName, attributes):
        
         

