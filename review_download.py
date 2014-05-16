# -*- coding: utf-8 -*-
"""
This script was written to download reviews of a set of items from Amazon.com

Flow: 
    1) The product names and links are stored in a dictionary
    2) The program keeps track where it was when downloading the reviews
        So after a restart, the program can continue the data collection 
        from where it stopped
    3) Review data stored in a csv file for each kindle 
    
version: 0.0.1 Last modified: 2014.05.12
    - defined dict and links
    - loops through the dict
    - Last page checker
    - indexfile write/read, update
    - removing non-ascii characters from review texts

@author: daniel
"""
from lxml import html
import requests
import datetime

# Format rating 
def clearRatings(ratingList):
    clearedrating = []
    
    for rating in ratingList:
        clearedrating.append(rating[0:3])

    return(clearedrating)
    
def formatRevText(revlists):
    formatedRevtext = []
    
    for revtext in revlists:
        revtext = removeNonAscii(revtext)
        formatedRevtext.append(revtext.text)

    return(formatedRevtext)    
    
# format date of review:
def clearDate(revDate):
    clearedDate = []
    
    for date in revDate:
        clearedDate.append(datetime.datetime.strptime(date, "%B %d, %Y").strftime("%Y-%m-%d"))
                
    return(clearedDate)
    
# Clearing textual values.
def clearText(texts):
    clearedText = []
    
    for text in texts:
        text = removeNonAscii(text)
        clearedText.append(text.replace(",","" ))
        
    return(clearedText)
    
def removeNonAscii(s): 
    return "".join(i for i in s if ord(i)<128)

# pringing out downloaded values
def writeTable(date, rating, title, text):
    tableRows = []
    
    # The length should be 10, bu tapparently some values sometimes are missing...
    # We need to check if all the values are there, and write only those, that are there...
    for i in range(10):
        try:
            date[i]
        except:
            date.append("NA")
            print("Date was missing!")
        try:
            rating[i]
        except:
            rating.append("NA")
            print("Date was missing!")
        try:
            title[i]
        except:
            title.append("NA")
            print("Date was missing!")
        try:
            text[i]
        except:
            text.append("NA")
            print("Date was missing!")
            
        tableRows.append(date[i]+","+rating[i]+","+title[i]+","+text[i]+"\n")
    
    return(tableRows)

# A function to get the number of reviewpages
def LastPage(link):

    tree    = DownloadPage((link+str(1)))
    rating  = tree.xpath('//div[@class="CMpaginate"]/span/a/text()')
    return (rating[1])

# Downloads webpage and generates a xml tree from it, and returns. 
def DownloadPage(link):

    page           = requests.get(link)
    brFreePage     = page.text.replace("<br />", "") # all <br /> tags have to be removed!!  
    brFreePageUnic = brFreePage.decode('unicode_escape').encode('ascii','ignore')
    brFreePageUnic = brFreePageUnic.replace("uff0c", "")   
    tree           = html.fromstring(brFreePageUnic)
    return(tree)

# Before we start downloading the data, we want to see which page we should start with:    
def PageToDownLoad(product):
    filename = product + "_index"
    print ("Opening " + filename)
    
    try:
        f = open(filename, 'r')
        page = str(f.readlines()[-1])
        return (int(page))
        f.close()
    
    except:
        return ("0")

def Core(product, link):
    lastpage   = LastPage(link)
    startpage  = PageToDownLoad(product)
    
    indexfile  = open(product + "_index", "a+")
    reviewfile = open(product + "_review.csv", "a+")

    # main loop
    for pageNo in range(int(startpage), int(lastpage)):
        print("We are on page {0} (out of {2}) of the reviews of {1}".format(str(pageNo), product, lastpage))        
        tree  = DownloadPage(link+str(pageNo))
        
        # Step 3 -> Extracting information from the html file:
        rating  = tree.xpath('//span[@style="margin-right:5px;"]/span/span/text()')
        date    = tree.xpath('//span[@style="vertical-align:middle;"]/nobr/text()')
        title   = tree.xpath('//span[@style="vertical-align:middle;"]/b/text()')
        revtext = tree.xpath('//div[@class="reviewText"]/text()')
        
        # Step 4 -> Cleaning downloaded data
        cleanRating = clearRatings(rating)
        cleanDate   = clearDate(date)
        cleanTitle  = clearText(title)
        cleanText   = clearText(revtext)
        
        # Step 5. Returning downloaded and parsed data:
        table       = writeTable(cleanDate, cleanRating, cleanTitle, cleanText)
        reviewfile.writelines(table)
                
        indexfile.writelines(str(pageNo))
        
        
    indexfile.close()
    reviewfile.close()

kindles =   {
    # 1st generation Kindle reviews:     
    "First_generation": "http://www.amazon.com/Kindle-Amazons-Original-Wireless-generation/product-reviews/B000FI73MA/ref=cm_cr_dp_see_all_summary?pageNumber=",

    # 2nd generation:
    "Second_generation": "http://www.amazon.com/Kindle-Wireless-Reading-Device-Display/product-reviews/B0015T963C/ref=sr_1_1_cm_cr_acr_txt?pageNumber=",

    # 3rd generation (Kindle keyboard):
    "Third_generation": "http://www.amazon.com/Kindle-Wireless-Reader-Wifi-Graphite/product-reviews/B002Y27P3M/ref=sr_1_2_cm_cr_acr_txt?pageNumber=",  

    # 4th generation - Kindle
    "Fourth_generation": "http://www.amazon.com/Kindle-eReader-eBook-Reader-e-Reader/product-reviews/B00492CIC8/ref=cm_cr_pr_btm_link_2?pageNumber=",
    "Fourth_generation_2": "http://www.amazon.com/Kindle-Ereader-ebook-reader/product-reviews/B007HCCNJU/ref=cm_cr_dp_see_all_btm?pageNumber=",

    # 5th generation (Kindle paperwhite):
    "Fifth_generation": "http://www.amazon.com/Kindle-Paperwhite-Ereader/product-reviews/B00AWVXK5O/ref=sr_1_1_cm_cr_acr_txt?pageNumber=",    
    "Fifth_generation_2": "http://www.amazon.com/Kindle-Paperwhite-3G/product-reviews/B007OZNUCE/ref=pr_all_summary_cm_cr_acr_txt?pageNumber="
}


for kindle in kindles.keys():
    #lastpage = LastPage(kindles[kindle])
    Core(kindle,kindles[kindle])    

