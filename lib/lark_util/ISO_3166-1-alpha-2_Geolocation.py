
import re
import sys
import urllib2
import BeautifulSoup
 
usage = "Run the script: ./ISO_3166-1-alpha-2_Geolocation.py IPAddress "

def normalize_whitespace(str):
    import re
    str = str.strip()
    str = re.sub(r'\s+', ' ', str)
    return str

if len(sys.argv)!=2:
    print(usage)
    sys.exit(0)
 
if len(sys.argv) > 1:
    ipaddr = sys.argv[1]

geody = "http://www.geody.com/geoip.php?ip=" + ipaddr
html_page = urllib2.urlopen(geody).read()
soup = BeautifulSoup.BeautifulSoup(html_page)

paragraph = soup('p')[3]
 

geo_txt = re.sub(r'<.*?>', '', str(paragraph))

haystack = []

#haystack = f.readlines()
lines = open("ISO_3166-1-alpha-2.txt", 'r').readlines()
for line in lines:
    haystack.append(line.strip().split('\t',1))



#haystack = list(haystack)
needle = geo_txt[32:].upper().strip()
#print needle
#print haystack
#print len(list(haystack))

haystack = list(haystack)
for index, key in enumerate(haystack):
    #print index
    #print haystack[key]
    #print needle + " "+ haystack[key]
    #print normalize_whitespace(haystack[index][0]) + ":" + normalize_whitespace(needle)
    if  normalize_whitespace(haystack[index][1]) in normalize_whitespace(needle):
        print "ISO_3166-1_alpha-2:" + haystack[index][0] + " " + haystack[index][1]
        break

#print haystack
