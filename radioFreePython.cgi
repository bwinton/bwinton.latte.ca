#!/usr/bin/env python

from BeautifulSoup import BeautifulSoup
import urllib

url = "http://radiofreepython.com/medium_quality.rss"
data = urllib.urlopen("http://radiofreepython.com/medium_quality.rss").read()
xml = BeautifulSoup(data)
for i in xml.findAll("enclosure"):
   i['url'] = i['url'].replace(" ", "%20")

print "Content-Type: application/rss+xml\n"
print xml
