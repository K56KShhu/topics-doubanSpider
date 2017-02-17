from urllib.request import urlopen
from bs4 import BeautifulSoup
from operator import itemgetter
import re


bag = []
def getTopics(topics):
    global bag
    for topic in topics:
        times = topic.parent.next_sibling.next_sibling.next_sibling.next_sibling.get_text()
        if times == '':
            continue
        times = int(times) 
        if times > 100:
            L = []
            L.append(times)
            L.append(topic["title"])
            L.append(topic["href"])
            bag.append(L)

index = 0
def getNextPage(Url, pageNumber):
    global index
    index += 1
    print("[%d]waiting..." % index)
    newUrl = Url + str(pageNumber)
    html = urlopen(newUrl)
    bs0bj = BeautifulSoup(html, "lxml")
    try:
        topics =  bs0bj.find("table", {"class":"olt"}).findAll("a", href=re.compile("https://www.douban.com/group/topic/.*"))
        getTopics(topics)
        newPageNumber = pageNumber + 25
        getNextPage(Url, newPageNumber)
    except AttributeError:
        return 


number = "102062"
firstUrl = "https://www.douban.com/group/" + number + "/"
secondUrl = "https://www.douban.com/group/"+ number + "/discussion?start="

html = urlopen(firstUrl)
bs0bj = BeautifulSoup(html, "lxml")
topics =  bs0bj.find("table", {"class":"olt"}).findAll("a", href=re.compile("https://www.douban.com/group/topic/.*"))
getTopics(topics)

getNextPage(secondUrl, pageNumber=50)


for title in sorted(bag, key=itemgetter(0)):
    print(title)
