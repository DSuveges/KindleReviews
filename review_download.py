# -*- coding: utf-8 -*-
"""
This script was written to download reviews of a set of items from Amazon.com

Process: 
    1) The product names and links are stored in a dictionary
    2) The program leaps through the dictionary, and downloads review pages
    3) html files are processed as xml structures
    4) Fields are extracted with xpath expression    
    5) Saved variables: date, rating, title, text in a csv file
    6) The program keeps track the downloading progression
        So after a restart, the program can continue the data collection 
        from where it stopped
    
version: 1.5 Last modified: 2014.05.12

@author: Daniel Suveges
"""
from lxml import html   # html files are processed as xml
import requests         # manages remote file access
import datetime         # to format data
import commands         # to keep track where the downlad stops last time

# This function extract the rating number from the given field
def clearRatings(ratingList):
    
    clearedrating = []    
    for rating in ratingList:
        clearedrating.append(rating[0:3])

    return(clearedrating)

# non-ASCII UTF-8 characters could easily cause problems, we have to remove them    
def formatRevText(revlists):
    formatedRevtext = []
    
    for revtext in revlists:
        revtext = removeNonAscii(revtext)
        formatedRevtext.append(revtext.text)

    return(formatedRevtext)    
    
# the format of the date in the reviews is not nice. Format it!
    # January 15, 2012 -> 2012-01-15
def clearDate(revDate):
    clearedDate = []
    
    for date in revDate:
        clearedDate.append(datetime.datetime.strptime(date, "%B %d, %Y").strftime("%Y-%m-%d"))
                
    return(clearedDate)
    
# non-ASCII UTF-8 characters could easily cause problems, we have to remove them
def clearText(texts):
    clearedText = []
    
    for text in texts:
        text = removeNonAscii(text)
        clearedText.append(text.replace(",","" ))
        
    return(clearedText)

# As each entry in the output file equals to one review,
# And there are 10 reviews on one page, based on the length of the 
# output file, we can get the page, where the data collection ended
def PageToDownLoad(product):
    GetLengthCommand = "wc -l " + product + "_review.csv"
    wcAnswer = commands.getoutput(GetLengthCommand)
    wcAnswer = wcAnswer.lstrip()
    
    # Test if the file existed or not:
    firstWord = wcAnswer.split(" ")[0]
    try:
        return (int(firstWord)/10)

    except:
        return 1

# non-ASCII UTF-8 characters could easily cause problems, we have to remove them
def removeNonAscii(s): 
    return "".join(i for i in s if ord(i)<128)

# organizing downloaded values into a printable lines of csv file.
def writeTable(date, rating, title, text):
    tableRows = []
    
    # The length should be 10, but somehow some values sometimes are missing...
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

    tree      = DownloadPage((link+str(1)))
    LastPage  = tree.xpath('//div[@class="CMpaginate"]/span/a/text()')
    return (LastPage[1])

# Downloads webpage and generates a xml tree from it 
def DownloadPage(link):
    
    page           = requests.get(link)
    brFreePage     = page.text.replace("<br />", "") # all <br /> tags have to be removed!!     
    tree           = html.fromstring(brFreePage)
    return(tree)

# Core process does most of the stuff
def Core(product, link):
    
    lastpage   = LastPage(link)          # The last page of reviews
    startpage  = PageToDownLoad(product) # Where to start downloading.

    reviewfile = open(product + "_review.csv", "a+") # The output csv file for storing the data

    # main loop
    for pageNo in range(int(startpage), int(lastpage)):
        
        # Status update:        
        print("We are on page {0} (out of {2}) of the reviews of {1}".format(str(pageNo), product, lastpage))        
        
        # Downloading review page:        
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
        
        # Step 5. saving parsed data:
        table       = writeTable(cleanDate, cleanRating, cleanTitle, cleanText)
        reviewfile.writelines(table)
                
    reviewfile.close()

# Might not all the generations are listed here, but definately most of them.... 
kindles =   {
    # 1st generation Kindle: 2007
    "Kindle_1": "http://www.amazon.com/Kindle-Amazons-Original-Wireless-generation/product-reviews/B000FI73MA/ref=cm_cr_dp_see_all_summary?pageNumber=",

    # 2nd generation: 2009
    "Kindle_2": "http://www.amazon.com/Kindle-Wireless-Reading-Device-Display/product-reviews/B0015T963C/ref=sr_1_1_cm_cr_acr_txt?pageNumber=",

    # Kindle DX: 2009
    "Kindle_DX": "http://www.amazon.com/Kindle-DX-Wireless-Reader-3G-Global/product-reviews/B002GYWHSQ/ref=dp_top_cm_cr_acr_txt?ie=UTF8&showViewpoints=1",

    # 3rd generation (Kindle keyboard): 2010
    "Kindle_keyboard": "http://www.amazon.com/Kindle-Wireless-Reader-Wifi-Graphite/product-reviews/B002Y27P3M/ref=sr_1_2_cm_cr_acr_txt?pageNumber=",

    # 4th generation - Kindle 2011
    "Kindle_basic": "http://www.amazon.com/Kindle-eReader-eBook-Reader-e-Reader/product-reviews/B00492CIC8/ref=cm_cr_pr_btm_link_2?pageNumber=",

    # 5th generation - Kindle 2012
    "Kindle": "http://www.amazon.com/Kindle-Ereader-ebook-reader/product-reviews/B007HCCNJU/ref=cm_cr_dp_see_all_btm?pageNumber=",

    # Kindle touch 2011
    "Kindle_touch" : "http://www.amazon.com/Kingle-Touch-e-Reader-Touchscreen-Touch-Screen-Wi-Fi/product-reviews/B005890FN0/ref=sr_1_1_cm_cr_acr_txt?",

    # Kindle paperwhite first genertation: 2012
    "Kindle_paperwhite_2": "http://www.amazon.com/Kindle-Paperwhite-Ereader/product-reviews/B00AWVXK5O/ref=sr_1_1_cm_cr_acr_txt?pageNumber=",

    # Kindle paperwhite second generation: 2013
    "Kindle_paperwhite": "http://www.amazon.com/Kindle-Paperwhite-3G/product-reviews/B007OZNUCE/ref=pr_all_summary_cm_cr_acr_txt?pageNumber="

}

# Looping through the dictionary and download the reviews of all Kindles
for kindle in kindles.keys():
    Core(kindle,kindles[kindle])    
