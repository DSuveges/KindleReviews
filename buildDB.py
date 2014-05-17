# -*- coding: utf-8 -*-
"""
Process:
    1) This script reads a series of csv files, downloaded form amazon.com
    2) builds dataframe of the date and the rating values
    3)  and adds an extra column with the name of the product
    4) merges review date of different product into a large dataframe,

Created on Fri May 16 10:38:35 2014

@author: daniel
"""
from   datetime import datetime
import pandas   as pd
import csv


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
        "Product" : [filename[0:-11]]*len(dates),
        "Dates"   : dates, 
        "Ratings" : ratings
    }
    f.close()
    
    # Build dataframe from the dict.
    df = pd.DataFrame(data)
    return(df)
    


# defining a list with the files to open:
kindles =   [
    "First_generation",
    "Second_generation",
    "Third_generation",
    "Fourth_generation",
    "Fourth_generation_2",
    "Fifth_generation",
    "Fifth_generation_2"
]


DF = {
    "Product" : [],
    "Dates"   : [],
    "Ratings" : []
}
largeDF = pd.DataFrame(DF)

# Looping through the dictionary and download the reviews of all Kindles
for kindle in kindles:

    # Get dataframe of one product:
    Short = open_csv(kindle)

    # concatenating DF-s
    largeDF = largeDF.append(Short, ignore_index=True)
    
# The LargeDF is processed in the downstream scripts... To be continued.
