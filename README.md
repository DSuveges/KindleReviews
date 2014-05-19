KindleReviews
=============

## Motivation

I love to read and I love my Kindle e-book reader. I really think that electronic books have revolutionize reading. As over the years, I bought around ten devices for family and friends as gifts, and I saw how dramatic developments occured. It is almost quite impossible to find any space for further developments. I was courious how the opinion of customers have changed over time and over the these striking developments.

On the other hand answering this question provided me a great opportunity to get an exposure to python and its powerful libraries: pandas, numpy and matplotlib.


### Source data

I used the [wikipedia article](http://en.wikipedia.org/wiki/Amazon_Kindle) to get a complete list of Kindle e-book readers. Then all the models were identifed in the [Amazon](http://www.amazon.com/s/ref=nb_sb_ss_c_0_6?url=search-alias%3Ddigital-text&field-keywords=kindle&sprefix=kindle%2Caps%2C321) marketplace. Here is the list and the links to the products:

| Model         | Year          | Number <br /> of reviews |
| ------------- |:-------------:|-----:|
| [Kindle 1](http://www.amazon.com/Kindle-Amazons-Original-Wireless-generation/dp/B000FI73MA/ref=sr_1_1?s=digital-text&ie=UTF8&qid=1400461600&sr=1-1&keywords=kindle+1st+generation) | 2007 | 7971 |
| [Kindle 2](http://www.amazon.com/Kindle-Wireless-Reading-Device-Display/dp/B0015T963C/ref=sr_1_1?s=digital-text&ie=UTF8&qid=1400461636&sr=1-1&keywords=kindle+2nd+generation) | 2009 |  17991 |
| [Kindle DX Graphite](http://www.amazon.com/Kindle-DX-Wireless-Reader-3G-Global/dp/B002GYWHSQ/ref=sr_1_1?s=digital-text&ie=UTF8&qid=1400462391&sr=1-1&keywords=kindle+dx) | 2009 | 4920 |
| [Kindle keyboard](http://www.amazon.com/Kindle-Special-Offers-Wireless-Reader/dp/B004HFS6Z0/ref=sr_1_1?s=digital-text&ie=UTF8&qid=1400462356&sr=1-1&keywords=kindle+keyboard) | 2010| 41466 |
| [Kindle basic](http://www.amazon.com/Kindle-eReader-eBook-Reader-e-Reader/dp/B00492CIC8/ref=cm_cr_pr_product_top) | 2011 | 8547 |
| [Kindle touch](http://www.amazon.com/Kindle-Touch-e-Reader-Touch-Screen-Wi-Fi-Special-Offers/dp/B005890G8Y/ref=sr_1_12?s=digital-text&ie=UTF8&qid=1400469899&sr=1-12&keywords=kindle+reader) | 2011 | 8580 |
| [Kindle](http://www.amazon.com/Kindle-Ereader-ebook-reader/dp/B007HCCNJU/ref=sr_1_3?s=digital-text&ie=UTF8&qid=1400470162&sr=1-3&keywords=new+kindle) | 2012 | 10095|
| [Kindle Paperwhite](http://www.amazon.com/Kindle-Paperwhite-Touch-light/dp/B007OZNZG0/ref=sr_1_6?s=digital-text&ie=UTF8&qid=1400470162&sr=1-6&keywords=new+kindle) | 2012 | 19664 |
| [Kindle Paperwhite 2](http://www.amazon.com/Kindle-Paperwhite-Ereader/dp/B00AWH595M/ref=sr_1_1?s=digital-text&ie=UTF8&qid=1400470621&sr=1-1&keywords=kindle+paper) | 2013 | 11544 |

These were the models that my analysis based on.


### Data collection

Then I used the `ReviewDownloader.py` script to download all the reviews. The process involved the following steps:

1. The product names and links are stored in a dictionary.
2. The program leaps through the dictionary, and downloads review pages (via **request** package).
3. html files are processed as xml structures (via **lxlm** package)
4. Fields are extracted with a series of xpath expressions.
5. I was interested in the following fields of the reviews: date, rating, title, text.
6. These fields had to be cleaned to prepare to analysis: date -> ISO 8601 format (**datetime** package), special UTF8 characters were removed from the text of the review
7. cleaned values were saved in a .csv file
6. The downloading process itself was really long (over hundred thousand reviwes on ten thousand pages), I had to make sure, once the program stops because of whatever reason, it can continue data collection upon restart. When a program starts, checks the number of lines of the saved cvs (**commands** package), that can be translated to the progression.

### Analysis - getting started

The csv files are read by the `csv_process.py` script. Though the text of the reviews are also available to analyse, at this point I am focusing on the date of the reviews and the pure ratings. <br />

The script reads all the saved csv file then takes the date (as datetime object) and the rating value (as float) and builds a pandas dataframe object. Then the dataframes of each model is stored in a dictionary as a value. <br />

The workflow of the subsequent scripts are rely on the usage of a suitable IDE like [spyder](https://code.google.com/p/spyderlib/), as I the analyses are relying on the variables created by this script.

