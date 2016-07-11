import urllib2
import sys
from bs4 import BeautifulSoup


url="https://www.rgpv.ac.in"
try:
	content=urllib2.urlopen(url).read()
except:
	print("OOps! Error. Make sure connection is working!")
	sys.exit(1)
soup=BeautifulSoup(content,'lxml')
dialog=soup.find("div",{"id":"dialog"})
i=0
print("Recent RGPV Feeds: \n\n")
for tr in dialog.findAll('tr'):
	i+=1
	print(str(i)+". "+tr.text+"\n")
	if(i==5):
		break
