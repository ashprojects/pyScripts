#!/usr/bin/python
# dev Ashish_G

import urllib2
import sys
from bs4 import BeautifulSoup
from gi.repository import Notify
import os
if not 'DISPLAY' in os.environ:
    os.environ['DISPLAY'] = ':0'


url="http://timesofindia.indiatimes.com/rssfeedstopstories.cms"
try:
	content=urllib2.urlopen(url).read()
except:
	print("OOps! Error. Make sure connection is working!")
	sys.exit(1)
print("Data Fetched!")
soup=BeautifulSoup(content,'lxml')
entries=soup.findAll("item")
i=0
Notify.init("Today's Word")
for entry in entries:
	i+=1
	w=entry.title.text
	c=entry.description.text
	
	Notify.Notification.new(w,str(c)).show()

	
	if(i>1):   #only two notifications selected! change it if you want more!
		break
