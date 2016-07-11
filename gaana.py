#!/usr/bin/python
#dev Ashish_G
# Please make sure you have all used libraries installed
# python 2.x


import urllib2
import sys
import subprocess
import youtube_dl
from bs4 import BeautifulSoup

baseurl="http://gaana.com"
youtube_search="https://www.youtube.com/results?search_query="
youtube_base="https://www.youtube.com"
cache_flag=True    # By default a cache file will be created to store chart-link map

def downloadNow(youtube_link,dir):
	output_path=dir
	subprocess.call(['youtube-dl',"-x","-o", dir+"/%(title)s.%(ext)s'","--extract-audio","--audio-format","mp3",youtube_link])
    	
def grabYoutubeURL(query):
	url="https://www.youtube.com/results?search_query="+query
	cls="yt-uix-tile-link"
	o=urllib2.urlopen(url)
	resp=o.read()
	soup=BeautifulSoup(resp,'lxml')
	div = soup.find("a",{"class":cls})
	return str(youtube_base+div['href'])

def genCache(write):
	chart_links=[]
	chart_title=[]
	if write:
		b_file=open("cache.txt","w")
	tmp_=urllib2.urlopen(baseurl+"/topcharts")
	charts=tmp_.read()
	soup=BeautifulSoup(charts,'lxml')
	div="featured_playlist_data"
	for pun in soup.findAll("div",{"class":div}):
		l=pun.find("a",{"class":"pjax"})['href']
		chart_links.append(l)
		chart_title.append(pun.find("span",{"class":"pjax"})['title'])
		try:
			if write:
				b_file.write(chart_title[-1]+":"+chart_links[-1]+"\n")
		except:
			continue
	if write:
		b_file.close()
	return chart_title,chart_links

def fetchFromCache(file):
	chart_links=[]
	chart_title=[]
	c1=b_file.read().split("\n")
	for line in c1:
		chart_title.append(line.split(":")[0])
		chart_links.append(line.split(":")[-1])
	file.close()
	return chart_title,chart_links



chart_links=[]
chart_title=[]
if cache_flag:
	try:		
		b_file=open("cache.txt","r")	
		chart_title,chart_links=fetchFromCache(b_file)
	except IOError:
		print("Cache no found! Caching...")
		chart_title,chart_links=genCache(True)
else:
	chart_title,chart_links=genCache(True)

print("\n********************  Gaana Top Charts  **************************\n")

i=1
for name in chart_title:
	if name=="":
		continue
	print(str(i)+". "+name)
	i+=1
while True:
	c=int(input("Select list (1-"+str(i-1)+"): "))
	if c>=len(chart_links):
		print("Enter valid Input!")
		continue
	if c<0:
		print("Enter valid Input!")
		continue
	break

url=chart_links[c-1]
chart_name=chart_title[c-1]
print("\nFetching Songs List. Please wait...")




response = urllib2.urlopen(baseurl+url)
content = response.read()
print("\n*******************  Songs List  **************************\n")
soup=BeautifulSoup(content,'lxml')
container_class="inn-content content-container"
songList=soup.find('div',{"class":container_class})
y_qry=[]
songs=[]
count=1
for hgrp in songList.findAll("hgroup"):
	songCurr=hgrp.h2.a['title']
	i=0
	for artGrp in hgrp.findAll("a",{"class":"pjax a-d1 _artist"}):
		if i==0:
			artist=artGrp['title']
		else: 
			artist+=","+artGrp['title']
		i+=1
	songCurr=artist+"-"+songCurr
	songs.append(songCurr)
	print(str(count)+". "+songCurr)	
	count+=1		
	y_qry.append("+".join(songCurr.split(" "))+"+audio+only")
print("\nTotal: "+str(len(songs))+" songs will be downloaded\n ")
dirname=str(raw_input("Enter directory name:"))
if dirname=="":
	dirname="Downloads"
if " " in dirname:
	dirname=dirname.split(" ")[0]
print("\nStarting with download...")
ps=0

for sng in songs:
	try:
		print("\n**************************************************************")
		print("**************** Downloading "+str(ps+1)+" of "+str(len(songs))+" ******************")
		print("**************************************************************")
		print("\nScraping download url for "+sng)
		yurl=grabYoutubeURL(y_qry[ps])
		print("Subprocess call...")
		downloadNow(str(yurl),str(dirname))
	except Exception as e:
		print(e)
		print("Error while downloading: "+sng+"! Will resume for the next one though!")
		ps+=1
	ps+=1
print("\n\n************************** Success All! ******************************")

