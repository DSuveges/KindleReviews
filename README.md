KindleReviews
=============

## Motivation

I love to read and I love my Kindle e-book reader. I really think that electronic books have revolutionized reading. Over the years I bought around ten devices for family and friends as gifts, and I saw how dramatic developments occured. I was courious how the opinion of customers have changed over time and over these major developments.

Furthermore, answering this question provided me a great opportunity to get an exposure to python and its powerful libraries: pandas, numpy and matplotlib.


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

These were the models that my analysis was based on.


### Data collection

Then I used the `ReviewDownloader.py` script to download all the reviews. The process involved the following steps:

1. The product names and links are stored in a dictionary.
2. The program leaps through the dictionary, and downloads review pages (via the **request** package).
3. html files are processed as xml structures (via the **lxlm** package)
4. Fields are extracted with a series of xpath expressions.
5. I was interested in the following fields of the reviews: date, rating, title, text.
6. These fields had to be cleaned to prepare for analysis: date -> ISO 8601 format (**datetime** package), special UTF8 characters were removed from the text of the review.
7. Cleaned values were saved in a .csv file.
6. The downloading process itself was really long (over hundred thousand reviwes on ten thousand pages), I had to make sure that if the program stops for whatever reason, it can continue data collection upon restart. When the program starts, it checks the number of lines of the saved cvs file (**commands** package), so it can calculate the last page it read and continue from there.

### Analysis - getting started

The csv files are read by the `csv_process.py` script. Though the text of the reviews are also available to analyse, at this point I am only focusing on the date of the reviews and the pure ratings. <br />

The script reads all saved csv files then takes the date (as datetime object) and the rating value (as float) and builds a pandas dataframe object. Then the dataframe of each model is stored in a dictionary as a value. <br />

The workflow of the subsequent scripts rely on the usage of a suitable IDE like [spyder](https://code.google.com/p/spyderlib/).

### Analysis - First steps

At first, I wanted to create a table to summarize the number of reviews and ratings of different e-book readers:
```Python
print "| Model  | Number of Ratings | Average ratings | First Rating |"
print "|-------:|:-----------------:|:---------------:|:-------------|"
for i in range(len(kindles)):
    product     = kindles[i]
    Rev_number  = Grouped_DF[product].count()[0]
    Average_rev = round(Grouped_DF[product].mean()[0],2)
    rate_dates  = Grouped_DF[product].index.tolist()
    first_rate  = datetime.strftime(min(rate_dates), "%B %d, %Y")

    print ("| {} | {} | {} | {} |".format(product, Rev_number, Average_rev, first_rate))
```
| Model  | Number of Ratings | Average ratings | First Rating |
|-------:|:----------------:|:---------------:|:-------------|
| Kindle_1 | 7980 | 4.22 | November 18, 2007 |
| Kindle_2 | 17998 | 4.31 | February 23, 2009 |
| Kindle_DX | 4930 | 3.99 | June 10, 2009 |
| Kindle_keyboard | 41479 | 4.44 | August 26, 2010 |
| Kindle_basic | 8550 | 4.28 | September 28, 2011 |
| Kindle_touch | 8569 | 4.16 | November 14, 2011 |
| Kindle | 10063 | 4.36 | September 06, 2012 |
| Kindle_paperwhite | 19658 | 4.33 | October 01, 2012 |
| Kindle_paperwhite_2 | 11470 | 4.48 | September 30, 2013 |



### Time dependent analysis of the reviews

In this chapter I was looking at how the ratings of different kindle models changed over time. I could look at the number of reviews and the average rating the reader got on a scale of 1 to 5. Initially, I was thinking there might be a decrease in the ratings over time, as the announcements of newer models with more features makes the old ones less satisfactory, but at the same time I was also expecting a large decrease in the number of reviews when a model becomes out of date.

Steps:

1. The output of the previously introduced `csv_process.py` script was used
2. The time series were resampled to combine ratings of each month
3. A stacked plot was generated, and the number of reviews were plotted as area map
4. Then the average ratings and the standad errors were plotted over the areas
5. The graph was saved

#### The resulting graph:

![Amazon reviews of kindle readers](http://kepfeltoltes.hu/140525/reviews_vs_time_www.kepfeltoltes.hu_.png)

#### Discussion:

There are several interesting features of the graph:
* In general, ratings just slightly decrease over time, except the Kindle Touch model, where since the announcement of the Paperwhite models, the average ratings have decreased dramotically. The buyers could have made the wrong choice and accidentally purchased the thouch instead of the paperwhite (there are not too many reviews, 4-20 a month).
* The lack of the general decrease can be explained by the fact that the user who bought an obsolote model, probably does not have access to newer ones to compare.
* Another interesting feature that can be seen with many models: after announcing a new product, during the first few months the ratings are slightly increasing. I think the reason of this behavior is the nature of the population who buys freshly announced products: they probaby are highly motivated by the novelty or by the massive advertisments. These people might have extraordinarily high expectations leading to the lower ratings. Later the reviews belong to customers who just want to buy an e-book reader, and they are just satisfied as it is.
* An interesting piece of the kindle family is the DX model. It has never been as popular as other members, but because of its unique large display, DX equally satisfies customers over the 4.5 years since its announcement.
* The most frequently rated e-reader is the third generation Kindle announced in 2010. Since then, despite the extra features built in the newer models, readers have got fewer reviews (although since 2011 multiple models have been competing with each other).
* Though the variability in the average ratings for the same device is small (except months when the number of reviews were really low, so the error is high) we can see a striking outlier on the second generation kindle, at the 5th month (denoted by a red circle).

```Python
resampled_df["Kindle_2"][3:7]
Out[396]:
````

|      Date  | mean     | count |   sdt    |   SEM    |
| ---------- |:--------:|:-----:|:--------:|:--------:|
| 2009-05-31 | 4.306351 | 803   | 1.176790 | 0.041528 |
| 2009-06-30 | 4.415094 | 689   | 1.081882 | 0.041216 |
| **2009-07-31** | **2.777500** | **800**   | **1.845196** | **0.065238** |
| 2009-08-31 | 3.991653 | 599   | 1.488506 | 0.060819 |
| 2009-09-30 | 4.479936 | 623   | 1.010793 | 0.040497 |

As the number of the reviews are really high, this deviation is quite surprising. We might think there was a bad batch of readers and all the buyers were immediately complaining. If we compare the histogram of this period with the histogram of the total rating of Kindle 2 we can see how the weakest rating is highly populated.
```Python
f.subplots_adjust(hspace=0)
setp([a.get_xticklabels() for a in f.axes[:-1]], visible=False)


K2_july09 = Grouped_DF["Kindle_2"]['20090701':'20090731']
K2_total  = Grouped_DF["Kindle_2"]
f, ax = subplots(2,sharex=True)

ax[0].hist(K2_total.values, label="All time")
ax[0].set_ylabel("#Rating")
ax[0].legend(loc='upper center')

ax[1].hist(K2_july09.values, label="July 2011")
ax[1].set_xlabel("Rating")
ax[1].set_ylabel("#Rating")
ax[1].legend(loc='upper center')
```
![Distribution of ratings of Kindle 2 at different times](http://kepfeltoltes.hu/140525/Kindle2_raings_www.kepfeltoltes.hu_.png)

To find out more about this outlier, I will later analyse the text of the reviews of this period, as I could not find any news in the archives of major newsportals.

#### Combining reviews over time

Based on the clearly identifiable peaks after Christmas we can assume that the number of reviews are proportional to the number of sold items. If this is the case, by combining the number of reviews from all models, we can get an overview of the dynamics of the e-book reader market.

![Cumulative reviews](http://kepfeltoltes.hu/140525/cumul_rev_www.kepfeltoltes.hu_.png)

According to the stacked plot, since the introduction of Kindle readers in 2008, there was a great increase in the demand peaking around 2011 and 2012, but to maintain the interest a constant development is required like touch screen and backlight.

# To be continued...
