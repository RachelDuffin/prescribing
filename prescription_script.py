#!/usr/bin/python

#pip3 install requests
#pip3 install numpy
#pip3 install pandas

#Import required packages----------------------------------------------------------------------------------------------------------------------------------------------------------------
import requests, csv, json, sys
import numpy as np
import pandas as pd


#Part 1 - Comparing number of antibiotics prescribed per patient per GP practice on average in Manchester CCG---------------------------------------------------------------------------------------

#Download the data using APIs and load into pandas dataframe------------------------------------------------------------------------------------------------------------------------------------------------------------

spending = requests.get('https://openprescribing.net/api/1.0/spending_by_practice/?code=5.1&format=json&org=14L').json()#gets json file of antibiotics prescribed per practice in Manchester CCG in json format
print(json.dumps(spending, indent=4, sort_keys=True)) #print data
spendingdf = pd.DataFrame.from_dict(spending) #json to pandas dataframe for antibiotic data
print(spendingdf) #prints the spending dataframe

list_size = requests.get('https://openprescribing.net/api/1.0/org_details/?format=json&org_type=practice&org=14L&keys=total_list_size').json() #gets total list size per GP practice in Manchester CCG in json format
print(json.dumps(list_size, indent=4, sort_keys=True)) #print data
listsizedf = pd.DataFrame.from_dict(list_size) #json to pandas dataframe for patient number data
print(listsizedf) #prints the listsize dataframe

#Merge the two pandas data frames--------------------------------------------------------------------------------------------------------------------------------------------------------

new_df = pd.merge(spendingdf, listsizedf, on=['row_id','date']) #merges the data frames on 'row_id' and 'date'

#Graphs---------------------------------------------------------------------------------------------------------------------------------


