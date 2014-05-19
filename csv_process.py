# -*- coding: utf-8 -*-
"""
Process:
    1) This script reads a series of csv files, downloaded form amazon.com
    2) builds dataframe of the date and the rating values
    3) creates a dictionary, where this dataframes are values and the keys are the names of the devices

Created on Fri May 16 10:38:35 2014

@author: daniel
"""
from   datetime import datetime
import pandas   as pd
import csv
import numpy    as np


# open and process cvs files:
def open_csv(filename):

    # generate filename, and open:
    filename += "_review.csv"
    f = open(filename, "rb")
    reader   = csv.reader(f)

    dates   = [] # Store data of the review
    ratings = [] # Store rating
    line    = 1  # Count lines

    # Selecting only the date and rating fields. If they are in the proper format
    for row in reader:
        print line

        try :
            dates.append(datetime.strptime(row[0],"%Y-%m-%d")) # Format date as date
            ratings.append(float(row[1])) # Format rating as float

        except:
            next

        line += 1

    # Combining data into a dictionary
    data = {
        "Ratings" : ratings
    }
    f.close()

    # Build dataframe from the dict.
    df = pd.DataFrame(data, index=dates)
    return(df)



# defining a list with the files to open:
kindles =   [
    "Kindle_1",
    "Kindle_2",
    "Kindle_keyboard",
    "Kindle_DX",
    "Kindle_basic",
    "Kindle",
    "Kindle_paperwhite",
    "Kindle_paperwhite_2",
    "Kindle_touch"
]

# Looping through the dictionary and download the reviews of all Kindles
Grouped_DF = dict()
for kindle in kindles:
    Grouped_DF[kindle] = open_csv(kindle)

# Resampling dataframes
resampled_df = dict()
for kindle in Grouped_DF.keys():

    # Apply resampling function:
    resampled_df[kindle] = Grouped_DF[kindle].resample("M", how=['mean', 'count', np.std])

# resampled_df will be used to plot different plots. ... at different script.
