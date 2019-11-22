#!/usr/bin/python3

#pip3 install requests numpy pandas matplotlib

#Import required packages-------------------------------------------------------------------------------------------------------------------------------------------------------
import requests, csv, json, sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

#Define functions--------------------------------------------------------------------------------------------------------------------------------------------------------------

#Download data in json format and load into pandas dataframe
def download(API):
    df = pd.DataFrame.from_dict(requests.get(API).json()) #gets data from API in json format, and creates pandas dataframe from dictionary format of json file 
    return(df)

#MANCHESTER CCG-----------------------------------------------------------------------------------------------------------------------------------------------------------------

#Download the data using APIs and load into pandas dataframe--------------------------------------------------------------------------------------------------------------------

spending = download(API='https://openprescribing.net/api/1.0/spending_by_practice/?code=5.1&format=json&org=14L') #gets json file of antibiotics prescribed per practice in Manchester CCG in json format
print(spending) #prints output of function to test output is correct

listsize = download(API='https://openprescribing.net/api/1.0/org_details/?format=json&org_type=practice&org=14L&keys=total_list_size') #gets total list size per GP practice in Manchester CCG in json format
print(listsize) #prints the listsize dataframe

new_df = pd.merge(spendingdf, listsizedf, on=['row_id','date', 'row_name']) #merges the two pandas dataframes on 'row_id' and 'date'

#Plot graph of prescribed items over time for each practice in Manchester CCG---------------------------------------------------------------------------------------------------

#Basic graph 
fig, ax = plt.subplots(figsize=(30,10)) #Plots graph of size 30,10

for key, grp in new_df.groupby(['row_name']): 
    ax = grp.plot(ax=ax, kind='line', x='date', y='items', label=key) #Specifies graph as line graph, and determines what is on each axis

#Normalised graph (shows prescribed items per 1,000 patients over time for each practice in Manchester CCG)---------------------------------------------------------------------
new_df['items per 1000'] = new_df['items']/new_df['total_list_size']*1000 #Adds column to dataframe of prescribed items per 1,000 registered patients as some practices are smaller than others
print(new_df) #check column has appended correctly by printing dataframe

fig, ax = plt.subplots(figsize=(30,10)) #Plots graph of size 30,10

for key, grp in new_df.groupby(['row_name']):
    ax = grp.plot(ax=ax, kind='line', x='date', y='items per 1000', label=key) #Specifies graph as line graph, and determines what is on each axis


#Calculate the mean 
prescribe_mean = new_df.groupby(by='date')['items per 1000'].mean() #Calculates mean prescriptions for each month per 1000 registered patients 


#Graph of mean for whole Manchester CCG-----------------------------------------------------------------------------------------------------------------------------------------
prescribe_mean = new_df.groupby(by='date')['items per 1000'].mean() #Calculates mean prescriptions for each month per 1000 registered patients 

plt.subplots(figsize=(20,10)) #plot a graph of mean precribing over time for whole CCG

ave_plot = plt.plot(prescribe_mean)
plt.show()

#Graph of mean for whole Manchester CCG with standard deviation-----------------------------------------------------------------------------------------------------------------
prescribe_desc = new_df.groupby(by='date')['items per 1000'].describe() #get standard deviation
print(prescribe_desc)

mean_min_std = prescribe_desc['mean'] - prescribe_desc['std'] #take standard deviation away from mean and add to mean so that these can be plotted
mean_add_std = prescribe_desc['mean'] + prescribe_desc['std']

prescribe_desc['mean_min_std'] = mean_min_std
prescribe_desc['mean_add_std'] = mean_add_std

print(prescribe_desc) #check mean take away std and add std has been added to dataframe

plt.subplots(figsize=(20,10)) #plot all description data

ave_plot = plt.plot(prescribe_desc)
plt.show()

plt.subplots(figsize=(20,10)) #plot mean, plus and minus standard deviation, need to add key

ave_plot = plt.plot(prescribe_mean)
ave_plot2 = plt.plot(mean_min_std)
ave_plot3 = plt.plot(mean_add_std) 
plt.show()

#COMPARED TO ALL CCGs------------------------------------------------------------------------------------------------------------------------------------------------------------

#Download the data using APIs and load into pandas dataframe---------------------------------------------------------------------------------------------------------------------
spending = requests.get('https://openprescribing.net/api/1.0/spending_by_ccg/?code=5.1&format=json').json()#gets json file of antibiotics prescribed per CCG
#print(json.dumps(spending, indent=4, sort_keys=True)) #print data
spendingdf = pd.DataFrame.from_dict(spending) #Creates pandas dataframe from the dictionary format of a json file
#print(spendingdf) #prints the spending dataframe

list_size = requests.get('https://openprescribing.net/api/1.0/org_details/?format=json&keys=total_list_size&org_type=ccg').json() #gets total list size per CCG
print(json.dumps(list_size, indent=4, sort_keys=True)) #print data
listsizedf = pd.DataFrame.from_dict(list_size) #Creates pandas dataframe from the dictionary format of a json file
#print(listsizedf) #prints the listsize dataframe

#Merge the two pandas data frames------------------------------------------------------------------------------------------------------------------------------------------------
new_df = pd.merge(spendingdf, listsizedf, on=['row_id','date', 'row_name']) #merges the data frames on 'row_id' and 'date'

#Calculate the mean antibiotics prescribed per 1000 patients across all CCGs-----------------------------------------------------------------------------------------------------

new_df['items per 1000'] = new_df['items']/new_df['total_list_size']*1000 #Adds column to dataframe of prescribed items per 1,000 registered patients as some practices are smaller than others

#Calculate the antibiotics prescribed per 1000 patients across Manchester CCG----------------------------------------------------------------------------------------------------

prescribe_mean = new_df.groupby(by='date')['items per 1000'].mean() #Calculates mean prescriptions for each month per 1000 registered patients 

#Plot graph of Manchester CCG----------------------------------------------------------------------------------------------------------------------------------------------------

