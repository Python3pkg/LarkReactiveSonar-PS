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
import sys
import urllib2
import BeautifulSoup
 
usage = "Run the script: ./ISO_3166-1-alpha-2_Geolocation.py IPAddress"

def normalizeWhitespace(str):
    import re
    str = str.strip()
    str = re.sub(r'\s+', ' ', str)
    return str

if len(sys.argv)!=2:
    print(usage)
    sys.exit(0)
 
if len(sys.argv) > 1:
    ipAddress = sys.argv[1]

geody = "http://www.geody.com/geoip.php?ip=" + ipAddress
html_page = urllib2.urlopen(geody).read()
soup = BeautifulSoup.BeautifulSoup(html_page)

paragraph = soup('p')[3]
 

geo_txt = re.sub(r'<.*?>', '', str(paragraph))

haystack = []

lines = open("ISO_3166-1-alpha-2.txt", 'r').readlines()
for line in lines:
    haystack.append(line.strip().split('\t',1))

needle = geo_txt[32:].upper().strip()

haystack = list(haystack)
for index, key in enumerate(haystack):
    if  normalizeWhitespace(haystack[index][1]) in normalizeWhitespace(needle):
        print "ISO_3166-1_alpha-2:" + haystack[index][0] + " " + haystack[index][1]
        return "ISO_3166-1_alpha-2:" + haystack[index][0] + " " + haystack[index][1]

#print haystack
