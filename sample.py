from urllib.request import urlopen
from urllib.parse import quote
from operator import itemgetter
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import re
import csv



def getTopics(topics):
    for topic in topics:
        responses = topic.parent.next_sibling.next_sibling.next_sibling.next_sibling.get_text()
        if responses == '':
            continue
        responses = int(responses) 
        if responses > 10:
            L = []
            L.append(responses)
            L.append(topic["title"])
            L.append(topic["href"])
            topicBag.append(L)



topicBag = []
index = 1
def getFirstPage(Url):
    global index
    print("<------------group %d------------>]" % index)
    index += 1
    print("waiting -->"+Url)

    try:
        html = urlopen(Url)
        bs0bj = BeautifulSoup(html, "lxml")
        topics =  bs0bj.find("table", {"class":"olt"}).findAll("a", href=re.compile("https://www.douban.com/group/topic/.*"))
        getTopics(topics)
        
        secondUrl = bs0bj.find("a", href=re.compile(".*start=50"))
        if secondUrl != None:
            return secondUrl["href"]
        else:
            return None
    except AttributeError:
        return



def getNextPage(Url, page):
    global pageBag
    print("waiting -->"+Url)

    try:
        html = urlopen(Url)
        bs0bj = BeautifulSoup(html, "lxml")
        topics =  bs0bj.find("table", {"class":"olt"}).findAll("a", href=re.compile("https://www.douban.com/group/topic/.*"))
        getTopics(topics)

        L = Url.split("=")
        newPageNumber = page + 25
        newUrl = L[0] + "=" + str(newPageNumber)
        getNextPage(newUrl, newPageNumber)
    except AttributeError:
        return



groupBag = set()
def findGroup(bs0bj):
    global groupBag
    groupUrls = bs0bj.findAll("a", href=re.compile("https://www.douban.com/link2/.*"))
    for groupUrl in groupUrls:
        groupBag.add(groupUrl["href"])

def extendPage(homeUrl):
    driver = webdriver.PhantomJS(executable_path='                  /phantomjs')
    driver.get(homeUrl)

    bar = 1
    while True:
        print("[%d]waiting..." % bar)
        bar += 1

        time.sleep(2)
        try:
            moreButton = driver.find_element(By.LINK_TEXT, "显示更多")
            moreButton.click()
        except:
            break
    driver.close()
    pageSource = driver.page_source
    bs0bj = BeautifulSoup(pageSource, "lxml")
    return bs0bj


search = input("Search: ")
homeUrl = "https://www.douban.com/search?cat=1019&q=" + quote(search)
bs0bj = extendPage(homeUrl)
findGroup(bs0bj)

for groupUrl in groupBag:
    secondUrl = getFirstPage(groupUrl)
    if secondUrl == None:
        continue
    else:
        getNextPage(secondUrl, page=50)

# show the message
# for title in sorted(topicBag, key=itemgetter(0), reverse=True):
#    print(title)


csvFile = open("                 ","w")
try:
    writer = csv.writer(csvFile)
    for topic in sorted(topicBag, key=itemgetter(0), reverse=True):
        writer.writerow(topic)
finally:
    csvFile.close()
    print("Done")



















