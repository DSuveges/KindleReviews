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

version: 2.0 Last modified: 2017.01.14

Update:
    1) New Kindle version were added.
    2) xml parsing was adjusted to the new xml structure.
    3) Fake user agent is sent with the request to fool amazon.
    4) A more sophisticated error handling during page download.
    5) More efficient way to strucure and save data.

@author: Daniel Suveges
"""
#from lxml import xml    # xml parsing methods.
from lxml import html   # html files are processed as xml
import requests         # manages remote file access
import datetime         # to format data
import commands         # to keep track where the downlad stops last 
import sys
import time

def DownloadPage(link):
    '''
    This function download one page of reviews at a time. 
    It also emulates a regular user agent as amazon does not allows parsing
    '''
    headers = {'User-Agent': ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36')}
    proxies = {'http' : 'http://10.10.1.10:3128'}
    page = requests.get(link, 
        headers=headers, 
        proxies=proxies)
    brFreePage = page.text.replace("<br />", "") # all <br /> tags have to be removed!!     
    tree = html.fromstring(brFreePage)

    while "you're not a robot" in "".join(tree.xpath('//text()')):
        time.sleep(1)
        page = requests.get(link, headers=headers, proxies=proxies)
        brFreePage = page.text.replace("<br />", "") # all <br /> tags have to be removed!!     
        tree = html.fromstring(brFreePage)
        print "[Warning] Robot check has failed! Page reloaded."

    return tree

def LastPage(link):
    '''
    A function to get the last page of reviews. 
    '''
    tree = DownloadPage((link+str(1)))
    LastPage = tree.xpath('//li[@class="page-button"]//text()')
    
    # If there is no returned data, we wait and repeat:
    while len(LastPage) < 1:
        time.sleep(0.5)
        tree = DownloadPage((link+str(1)))
        LastPage = tree.xpath('//li[@class="page-button"]//text()')

    return LastPage[-1].replace(",", "")

def PageToDownLoad(product):
    '''
    Based on the progression of previous runs, this function
    can decide which page should we continue downloading the reviews.
    '''
    GetLengthCommand = "wc -l " + product + "_review.csv"
    wcAnswer = commands.getoutput(GetLengthCommand)
    wcAnswer = wcAnswer.lstrip()
    
    # Test if the file existed or not:
    firstWord = wcAnswer.split(" ")[0]
    try:
        return (int(float(firstWord)/10+0.5))

    except:
        return 1


'''
There are small functions to clear all returned fields.
'''
def clearRatings(ratingList):
    if len(ratingList) == 0:
        print "[Warning] Rating is missing!"
        return "NA"
    else:
        return ratingList[0][0:3]

def cleanAuthors(authors):
    if len(authors) == 0:
        return "NA"
    else:
        return removeNonAscii(authors[0])

def clearDate(revDate):
    '''
    The format of the date in the reviews is not nice. Format it!
    Expected format: 'on December 4, 2013'
    January 15, 2012 -> 2012-01-15
    '''
    if len(revDate) == 0:
        print "[Warning] Review date is missing!"
        return "NA"
    else:
        return datetime.datetime.strptime(revDate[0], "on %B %d, %Y").strftime("%Y-%m-%d")

def clearText(texts):
    if len(texts) == 0:
        print "[Warning] rating is missing!"
        return "NA"
    else:
        text = removeNonAscii(texts[0])
        return text.replace(",", "")

'''
Helpper functions for the above routines:
'''
def removeNonAscii(s): 
    '''
    Non-ASCII UTF-8 characters could easily cause problems, we have to remove them...
    (Although it should not be a problem...)
    '''
    return "".join(i for i in s if ord(i) < 128)

def formatRevText(revlists):
    if len(revlists) == 0:
        print "[Warning] Review text is missing!"
        return "NA"
    else:
        return removeNonAscii(revlists[0])


# Core process does most of the stuff
def Core(product, link):
    print "\n[Info] We are processing %s" % product

    lastpage = LastPage(link)          # The last page of reviews
    startpage = PageToDownLoad(product) # Where to start downloading.

    reviewfile = open(product + "_review.csv", "a+") # The output csv file for storing the data

    # main loop
    for pageNo in range(int(startpage), int(lastpage)+1):

        # Status update:    
        sys.stdout.write("\rWe are on page {0} (out of {2}) of the reviews of {1}\r".format(str(pageNo), product, lastpage))
        sys.stdout.flush()

        # Downloading review page:        
        tree = DownloadPage(link+str(pageNo))

        # Step 3 -> Extracting information from the html file:
        authors = tree.xpath('//a[@data-hook="review-author"]//text()')
        
        # If authors could not be extracted we can assume somethig has gone wrong. we wait and repeat 
        tryCnt = 0
        while len(authors) < 1:
            time.sleep(1)
            tree = DownloadPage(link+str(pageNo))
            authors = tree.xpath('//a[@data-hook="review-author"]//text()')
            tryCnt += 1 
            print "\n".join(tree.xpath('//text()')) # Downloads usually fail because robot check... I don't know how to overcome it.
 
            if tryCnt == 10:
                print "[Warning] 10 attempts to download reviews for %s has been failed for page %s." %(product, pageNo)
                print "[Warning] Adding blank lines then going to next page."
                continue
        
        # Parsing xml file:
        for node in tree.xpath('//div[@data-hook="review"]'):
            
            # Initializing variables:
            authors, ratings, dates, titles, revtexts = ([] for i in range(5))
            
            # Extracting data:
            authors = node.xpath('.//a[@data-hook="review-author"]//text()')
            ratings = node.xpath('.//i[@data-hook="review-star-rating"]//text()')
            dates = node.xpath('.//span[@data-hook="review-date"]//text()')
            titles = node.xpath('.//a[@data-hook="review-title"]//text()')
            revtexts = node.xpath('.//span[@class="a-size-base review-text"]//text()')
            
            # Step 4 -> Cleaning downloaded data
            cleanAuthor = cleanAuthors(authors)
            cleanRating = clearRatings(ratings)
            cleanDate = clearDate(dates)
            cleanTitle = clearText(titles)
            cleanText = clearText(revtexts)

            # Step 5. saving parsed data:
            try:
                reviewfile.writelines(",".join([cleanDate, cleanAuthor, cleanRating, cleanTitle, cleanText])+"\n")
                #print ",".join([cleanDate, cleanAuthor, cleanRating, cleanTitle, cleanText])
            except:
                print "[Warnings] There were problem with saving data."

    # Once all pages have downloaded the file handle is closed.
    reviewfile.close()

# Might not all the generations are listed here, but definately most of them.... 
kindles =   {
    # 1st generation Kindle: 2007
    "Kindle_1": "http://www.amazon.com/Kindle-Amazons-Original-Wireless-generation/product-reviews/B000FI73MA/ref=cm_cr_dp_see_all_summary?pageNumber=",

    # 2nd generation: 2009
    "Kindle_2": "http://www.amazon.com/Kindle-Wireless-Reading-Device-Display/product-reviews/B0015T963C/ref=sr_1_1_cm_cr_acr_txt?pageNumber=",

    # Kindle DX: 2009
    #"Kindle_DX": "http://www.amazon.com/Kindle-DX-Wireless-Reader-3G-Global/product-reviews/B002GYWHSQ/ref=dp_top_cm_cr_acr_txt?ie=UTF8&showViewpoints=1",

    # 3rd generation (Kindle keyboard): 2010
    #"Kindle_keyboard": "http://www.amazon.com/Kindle-Wireless-Reader-Wifi-Graphite/product-reviews/B002Y27P3M/ref=sr_1_2_cm_cr_acr_txt?pageNumber=",

    # 4th generation - Kindle 2011
    #"Kindle_basic": "http://www.amazon.com/Kindle-eReader-eBook-Reader-e-Reader/product-reviews/B00492CIC8/ref=cm_cr_pr_btm_link_2?pageNumber=",

    # 5th generation - Kindle 2012
    #"Kindle": "http://www.amazon.com/Kindle-Ereader-ebook-reader/product-reviews/B007HCCNJU/ref=cm_cr_dp_see_all_btm?pageNumber=",

    # Kindle touch 2011
    #"Kindle_touch" : "http://www.amazon.com/Kingle-Touch-e-Reader-Touchscreen-Touch-Screen-Wi-Fi/product-reviews/B005890FN0/ref=sr_1_1_cm_cr_acr_txt?",

    # Kindle Paperwhite, 6" High Resolution  45,694 reviews
    "Kindle_paperwhite_2": "http://www.amazon.com/Kindle-Paperwhite-Ereader/product-reviews/B00AWVXK5O/ref=sr_1_1_cm_cr_acr_txt?pageNumber=",

    # Kindle Paperwhite 3G, 6" 22,153 reviews
    #"Kindle_paperwhite": "http://www.amazon.com/Kindle-Paperwhite-3G/product-reviews/B007OZNUCE/ref=pr_all_summary_cm_cr_acr_txt?pageNumber=",

    # Kindle glare free 2016 3,604 reviews
    #"Kindle_noglare" : "https://www.amazon.com/All-New-Kindle-ereader-Glare-Free-Touchscreen/product-reviews/B00ZV9PXP2/ref=cm_cr_arp_d_paging_btm_2?ie=UTF8&reviewerType=all_reviews&showViewpoints=0&sortBy=recent&pageNumber=",

    # Kindle Paperwhite high-res 2015 35,264 reviews
    "Kindle_paperwhite_hires" : "https://www.amazon.com/All-New-Kindle-ereader-Glare-Free-Touchscreen/dp/B00ZV9PXP2/ref=sr_tr_sr_1?ie=UTF8&qid=1484086464&sr=8-1&keywords=kindle&th=1#customerReviews",

    # Kindle voyage 2014 : 11,467 reviews
    #"Kindle_voyage" : "https://www.amazon.com/Amazon-Kindle-Voyage-6-Inch-4GB-eReader/product-reviews/B00IOY8XWQ/ref=cm_cr_dp_qt_see_all_top?ie=UTF8&reviewerType=avp_only_reviews&showViewpoints=1&sortBy=helpful",

    # Kindle Oasis  2016 : 2,571 reviews
    #"Kindle_oasis" : "https://www.amazon.com/Amazon-Kindle-Oasis-eReader-with-Leather-Charging-Cover/dp/B00REQKWGA/ref=sr_tr_sr_4?ie=UTF8&qid=1484086464&sr=8-4&keywords=kindle#customerReviews"
}

# Looping through the dictionary and download the reviews of all Kindles
for kindle, URL in kindles.iteritems():
    Core(kindle, URL)    
