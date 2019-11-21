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

new_df = pd.merge(spendingdf, listsizedf, on=['row_id','date', 'row_name']) #merges the data frames on 'row_id' and 'date'

#Graphs---------------------------------------------------------------------------------------------------------------------------------

#plot graph of prescribed items over time for each practice in Manchester CCG
import matplotlib.pyplot as plt

fig, ax = plt.subplots()

for key, grp in new_df.groupby(['row_name']):
    ax = grp.plot(ax=ax, kind='line', x='date', y='items', label=key)

#create new column in dataframe of number of prescribed items per 1,000 registered patients
new_df['items per 1000'] = new_df['items']/new_df['total_list_size']*1000
#check column by printing dataframe
print(new_df)

#plot graph prescribed items per 1,000 patients over time for each practice in Manchester CCG
fig, ax = plt.subplots()

for key, grp in new_df.groupby(['row_name']):
    ax = grp.plot(ax=ax, kind='line', x='date', y='items per 1000', label=key)
