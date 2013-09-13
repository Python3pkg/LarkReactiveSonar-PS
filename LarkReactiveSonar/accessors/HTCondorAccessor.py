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

import sys, os, time
import htcondor
import classad
from LarkReactiveSonar.common.StaticClass import StaticClass

"""
This python wrapper module contains a mechanisms for interacting with the
HTCondor system.
command:

    pydoc -w HTCondorAccessor

"""

__author__ =  'Andrew B. Koerner'
__email__=  'AndrewKoerner.b@gmail.com'

class HTCondorAccessor(StaticClass):
    
    @staticmethod
    def getHTCondorConfigAttribute(attributeName):
        result = htcondor.param[attributeName]
        attributes = result.split(",");
        attributes = [attribute.strip() for attribute in attributes]
        return attributes

    @staticmethod
    def newClassAd(classAdType, classAdName, data):

        ad = classad.ClassAd()
        ad['MyType'] = classAdType
        ad['Name'] = clasAdName

        for key in data:
            ad[key] = data[key]

       ad['Timestamp'] = time.time()
