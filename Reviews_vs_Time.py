# -*- coding: utf-8 -*-
"""
Created on Fri May 23 16:03:09 2014

The time resolved analysis of the reviews of different kindle models.

For this analysis, the output of previously used  ... script, Grouped_DF variable was used

Steps:
    1) Resampling the reviews for months, get the number of reviews, the 
        average rating, and the std of the rating
    2) Calculation of the standard error of the mean
    3) Plotting number of reviews as a function of time (scale comparable)
    4) Plotting the average rating as a function of time with error bars
    5) Saving plot.
    
"""

from datetime import datetime, timedelta
import numpy as np
import matplotlib as plt


# Kindle models in order of their announcement:
kindles =   [
    "Kindle_1",             # 2007
    "Kindle_2",             # 2009
    "Kindle_DX",            # 2009
    "Kindle_keyboard",      # 2010
    "Kindle_basic",         # 2011
    "Kindle_touch",         # 2011
    "Kindle",               # 2012
    "Kindle_paperwhite",    # 2012
    "Kindle_paperwhite_2"   # 2013
]

# Looping through the Grouped_DF variable storing the reviews:
resampled_df = {}
for i in range(len(kindles)):
    product = kindles[i]
    print (Grouped_DF[product])
    resampled_df[product] = Grouped_DF[product].resample("M", how=['mean', 'count', np.std])
    resampled_df[product]["SEM"] = (resampled_df[product]["Ratings"]["std"]/sqrt(resampled_df[product]["Ratings"]["count"]))

# Initialize potting parameters:
x_min_list = []
x_max_list = []

for kindle in resampled_df.keys():
    print kindle
    x_min_list.append(resampled_df[kindle].index.tolist()[0])
    x_max_list.append(resampled_df[kindle].index.tolist()[-1])

x_min = min(x_min_list) - timedelta(60)
x_max = max(x_max_list) + timedelta(60)


# Get the min and max values of the x and y axes:
x_min_list  = []
x_max_list  = []
y_max_list  = []
for kindle in resampled_df.keys():
    print kindle
    x_min_list.append(resampled_df[kindle].index.tolist()[0])
    x_max_list.append(resampled_df[kindle].index.tolist()[-1])
    y_max_list.append(max(resampled_df[kindle]["Ratings"]["count"]))
# 60 days before and after the first and last date
x_limes         = [ min(x_min_list) - timedelta(60), max(x_max_list) + timedelta(60)] 
y_limes_area    = [0, max(y_max_list) + 500]
y_limes_scatter = [0.5, 5.5]

# Plotting averaged ratings over time.
rows = len(resampled_df.keys())
f, ax_arr = plt.subplots(rows, sharex=True, sharey=True, figsize=(6, 12))

for i in range(len(kindles)):      
    
    # Twin the x-axis to make independent y-axes.
    ax_arr[i].set_xlim(x_limes)    
    ax = [ax_arr[i], ax_arr[i].twinx()]
    
    # Set product
    product = kindles[i]
    
    # Plot area at first:    
    ax[0].set_autoscaley_on(False)    
    ax[0].set_ylim(y_limes_area)
    ax[0].set_yticks(np.arange(0,y_limes_area[1], 2000))
    ax[0].plot(resampled_df[product].index.tolist(),
        resampled_df[product]["Ratings"]["count"], 
        color="blue")
    ax[0].fill_between(resampled_df[product].index.tolist(),
        resampled_df[product]["Ratings"]["count"],
        0, 
        color='red')
        
    # PLot ratings next:   
    ax[1].errorbar(resampled_df[product].index.tolist(), 
        resampled_df[product]["Ratings"]["mean"], 
        yerr=resampled_df[product]["SEM"], 
        ecolor='black',
        ls = '',        
        capsize=2,        
        fmt="o", 
        ms=2,
        mec  = "b",
        mfc = 'b',
        label=product) 
    ax[1].set_ylim(y_limes_scatter)
    ax[1].set_yticks(np.arange(1,5.5,1))
    
    # Formatting the legend
    handles, labels = ax[1].get_legend_handles_labels()
    handles = [h[0] for h in handles]
    leg = ax[1].legend(labels, loc='best', fancybox=True, numpoints=1, markerscale=3)
    leg.get_frame().set_alpha(0)
    leg.get_frame().set_edgecolor('white')
    
    # Adding y and x axis labels only once:
    if i == 4:
        ax[0].set_ylabel("Number of reviews")
        ax[1].set_ylabel("Average rating")

    if i == 8 :
        ax[0].set_xlabel("Date of review")
        
    # Highlite outlier:
    if i == 1:
        ax[1].scatter(datetime.strptime("2009-08-1", "%Y-%m-%d"), 2.777500, s=100, c='w', edgecolor='r',marker='o')


f.subplots_adjust(hspace=0)
f.savefig("reviews_vs_time.png")
plt.show()
