import urllib2
from bs4 import BeautifulSoup
from gi.repository import Notify

#Notify.Notification.new("Hi").show()
def word_of_the_day():
	url="http://www.merriam-webster.com/word-of-the-day"
	content=urllib2.urlopen(url).read()
	soup=BeautifulSoup(content,'lxml')
	div1=soup.find(class_='word-and-pronunciation')
	meaning=soup.findAll(class_='wod-definition-container')
	word=div1.find('h1').text
	mean=[]
	#print("Today's word:  "+word)
	for tags in meaning[0].findAll():
		if str(tags.text)=='Examples':
			break
		
		if str(tags.name)=="p":
			mean.append(tags.text)
	return word,mean
	


w,m=word_of_the_day()
c=''
print(w)

for a in m:
	c+='\n'+str(a)
Notify.init("Today's Word")
notification=Notify.Notification.new(w,str(c))

notification.show()
