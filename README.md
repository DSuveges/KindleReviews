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

The csv files are read by the `csv_process.py` script. Though the text of the reviews are also available to analyse, at this point I am only focusing on the date of the reviews and the pure ratings. <br />

The script reads all the saved csv file then takes the date (as datetime object) and the rating value (as float) and builds a pandas dataframe object. Then the dataframes of each model is stored in a dictionary as a value. <br />

The workflow of the subsequent scripts rely on the usage of a suitable IDE like [spyder](https://code.google.com/p/spyderlib/), as I the analyses are using the variables created by this script.

### Analysis - First steps

At first I wanted to create a table to summarize the number of reviews and ratings of different e-book reader:

### Time dependent analysis of the reviews

In this chapter I was looking at how the ratings of different kindle models changed over time. I could look at the number of reviews and the average rating the reader got on a scale of 1 to 5. Initially I was thinking there might be a decrease in the ratings over time, as the announcements of newer models, with more features makes the old ones less satisfactory, but at the same time I was also expecting a large decrease of the number of reviews when a model becomes out of date.

Steps:

1. The output of the previously introduced `csv_process.py` script was used
2. The time series were resampled to combine ratings of each month
3. A stacked plot was generated, and the number of reviews were plotted as area map
4. Then the average ratings and the standad errors were plotted over the areas
5. The graph was saved

#### The resulting graph:

![Amazon reviews of kindle readers](http://kepfeltoltes.hu/140525/reviews_vs_time_www.kepfeltoltes.hu_.png)

#### Discussion:

There are many interesting features on the graph:
* In general, ratings just slightly decrease over time, except the Kindle Touch model, where since the announce of the Paperwhite models, the average ratings have decreased dramotically. I think the buyers could possibly made a wrong choice and accidentally purchased the thouch instead of the paperwhite. (there are not too many reviews, 4-20 a month)
* The lack of the general decrease can be explained by the fact that one user, who bought an obsolote model, probably do not have access to newer ones to compare.
* An other interesting feature we can be seen in many models: after announcing a new product, during the first few months the ratings are slightly increasing. I think the reason of this behavior is the nature of the population who buys freshly announced products: they probaby are highly motivated by the novelty or by the massive advertisments. These people might have extraordinarily high expectations leading to the lower ratings. Latter the reviews belong to customers who just want to buy an e-book reader, and they just satisfied as it is.
* An interesting piece of the kindle family is the DX model. It has never been as popular as other members, but because of its unique large display, DX equally satisfies customers over the 4 and a half years since its announcement.
* Interestingly the most frequently rated e-reader is the third generation Kindle announced in 2010. Since then, however the extra features built in the newer models, readers have got less reviews. (Though, since 2011 multiple models have been competing with each other) This trend might indicates the peak of the e-book reader market if we assume that the number of reviews are proportional to the number of sold items.
* Though the distribution of the ratings are quite even (except months when the number of reviews were really low, so the error is high) we can see a really striking outlier on the second generation kindle:

```Python
resampled_df["Kindle_2"][:5]
Out[396]:
````

|            | Ratings                     |  SEM     |
| ---------- |:---------------------------:|---------:|
|            | mean     | count |   sdt    |          |
| ---------- |:------:|:-------:|:--------:|:--------:|
| 2009-05-31 | 4.306351 | 803   | 1.176790 | 0.041528 |
| 2009-06-30 | 4.415094 | 689   | 1.081882 | 0.041216 |
| 2009-07-31 | 2.777500 | 800   | 1.845196 | 0.065238 |
| 2009-08-31 | 3.991653 | 599   | 1.488506 | 0.060819 |
| 2009-09-30 | 4.479936 | 623   | 1.010793 | 0.040497 |






