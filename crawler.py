
import requests
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import xlsxwriter


def websiteCrawler(startingpage, repitionsBeforeQuit, internalLinkType, maxURL, *linkNotToCrawl):
    manualurls = []
    
    url = [startingpage]
    newList = []
    safetyStop = [0]

    # Function 1: The goal is for the user to add manual URLs to the list
    def addingManualURLs():
        for x in manualurls:
            url.append(x)

    # Function 2: The goal is to set up an API connection to pull data out of a page
    def urlScraper(URL):
        r = requests.get(URL)
        html_doc = r.text
        soup = BeautifulSoup(html_doc, "html.parser")
        a_tags = soup.find_all("a")
        return a_tags

    # Function 3: The goal is to check if the link is an internal link
    def internalLinkChecker(internalLinkType, hreflink):
        #this line produces error. the "/" should not be standalone
        if internalLinkType == 1 and hreflink[0] == "/" and len(hreflink) > 1:
            return True
        elif internalLinkType == 0 and hreflink[0] == "h" and startingpage in hreflink:
            return True
        else:
            return False
    
    # Function 4: The goal is to check if certain internal links should not be crawled
    def doNotCrawl(link, *linkNotToCrawl):
        noCrawl = []
        for x in linkNotToCrawl:
            if x in link:
                noCrawl.append(x)
        if len(noCrawl) > 0:
            return False
        else:
            return True
        
    # Function 5: The goal is to organize the data to put it into an organized filtered list
    def listOrganizer(scraperData):
        for link in scraperData:
            x = link.get("href")
            if type(x) == str:
                if internalLinkChecker(internalLinkType, x) == True:
                    if doNotCrawl(x, *linkNotToCrawl) == True:
                        #this is for type 1 internal link
                        if startingpage[:-1] + x not in newList and internalLinkType == 1:
                            newList.append(startingpage[:-1] + link.get("href"))
                        #this is for type 0 internal link
                        #bug we can only add if part of domain
                        elif x not in newList and internalLinkType == 0:
                            newList.append(link.get("href"))

    # Function 6: The goal is to add any pages to the URL object that we have not crawled yet 
    def urlAdding():
        for x in newList:
            if x not in url:
                url.append(x)

    # Function 7: A safety for the loop to stop
    def crawlSafety(lengthData):
        if len(safetyStop) > repitionsBeforeQuit:
            if safetyStop[-1] == safetyStop[-repitionsBeforeQuit]:
                safetyStop.append(-1)
                print(safetyStop)
            else:
                safetyStop.append(len(lengthData))
                print(safetyStop)
                return safetyStop
        else:
            safetyStop.append(len(lengthData))
            print(safetyStop)
            return safetyStop

    # Function 8: The goal is to have a final list of URLs in a list. 
    def totalCrawl():
        caller = 0
        addingManualURLs()
        while caller < len(url):
            try:
                currentPageScraped = urlScraper(url[caller])
                listOrganizer(currentPageScraped)
                urlAdding()
                print(url[caller])
                caller = caller + 1
                if safetyStop[-1] == -1:
                    print("STOP")
                    return newList
                    #break
                else:
                    crawlSafety(newList)
                if len(url) > maxURL:
                    print("STOP")
                    return newList
                    #break
                print("newlist: "+str(len(newList)))
                print("Url: " + str(len(url)))
                print("caller: " + str(caller))
                
            except IndexError:
                print("INDEXERROR")
                print(newList)
                caller = caller + 1
                crawlSafety(newList)
                #break
        return newList

    totalCrawl()

    #Function 9 : The goal is to push new list into a pandas dataframe and then transfer it to excel
    def listToXls(listData):
        df = pd.DataFrame(listData, columns = ["URLs"])
        dataToExcel = pd.ExcelWriter("new_file.xlsx", engine = "xlsxwriter")
        df.to_excel(dataToExcel, sheet_name = "URLs")
        dataToExcel.save()
        return df
    
    listToXls(totalCrawl())
    print(listToXls(totalCrawl()))


websiteCrawler("https://example.com", 100, 1, 1000, "cdn-cgi", "paragraph-", "/node", ".pdf", ".jpg" , "?")
#Arg 1: String - The URL to be crawled
#Arg 2: Int - The repitions new URLs should be crawled without finding new hrefs not already in list
#Arg 3: Int - 0 or 1. if 0 then the internal link is http(s) if 1 then it is /
#Arg 4: Int - The maximum URLs to be crawl before script should stop
#Arg 4: String - As many arguments as needed. Any parts of the site which should be not crawled. 

#TODOS
#only look at links from domain
#further update - if error use try and except to still push update live
#make *listnottocrawl an array for further input
#FrontEnd for others to use
