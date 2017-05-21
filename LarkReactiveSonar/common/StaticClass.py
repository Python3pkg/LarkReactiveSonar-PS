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

import abc

__author__ =  'Andrew B. Koerner'
__email__=  'AndrewKoerner.b@gmail.com'

class StaticClassError(Exception):
    pass


class StaticClass(metaclass=abc.ABCMeta):
    def __new__(cls, *args, **kw):
        raise StaticClassError("%s is a static class and cannot be initiated."
                                % cls)