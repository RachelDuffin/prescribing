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

spendingAPI= 'https://openprescribing.net/api/1.0/spending_by_practice/?code=5.1&format=json&org=14L' #API for number of antibiotics prescribed by practice in Manchester CCG
listsizeAPI= 'https://openprescribing.net/api/1.0/org_details/?format=json&org_type=practice&org=14L&keys=total_list_size' #API for number of patients by practice in Manchester CCG

new_df = pd.merge(download(API=spendingAPI), download(API= listsizeAPI), on=['row_id','date', 'row_name']) #downloads data in json format using APIs and loads into pandas dataframes, then merges dataframes on three columns
new_df['items per 1000'] = new_df['items']/new_df['total_list_size']*1000 #Adds column to dataframe of prescribed items per 1,000 registered patients as some practices are smaller than others
print(new_df) #prints to check df is correct and check normalised column has appended correctly

#Plot graphs of prescribed items over time for each practice in Manchester CCG---------------------------------------------------------------------------------------------------

#Define function for plotting graphs
def plot(x, y):
    fig, ax = plt.subplots(figsize=(30,10)) #Plots graph of size 30,10
    for key, grp in new_df.groupby(['row_name']): 
        ax = grp.plot(ax=ax, kind='line', x=x, y=y, label=key) #Specifies graph as line graph, and determines what is on each axis
    plt.show()

#Plot graphs
plot(x='date', y='items') #plot basic graph showing number of antibiotics prescribed by each practice each month over time
plot(x='date', y='items per 1000') #plots normalised graph accounting for patient population size (prescribed items per 1,000 registered patients)


#Graph of mean for whole Manchester CCG-----------------------------------------------------------------------------------------------------------------------------------------
prescribe_desc = new_df.groupby(by='date')['items per 1000'].describe() #Calculates mean and standard deviation across all practices for each month per 1000 registered patients
print(prescribe_desc)

plt.subplots(figsize=(20,10)) #specifies size of plot
plt.show(plt.plot(prescribe_desc['mean'])) #plots the graph of the mean

#Graph of mean for whole Manchester CCG with standard deviation-----------------------------------------------------------------------------------------------------------------
mean_min_std = prescribe_desc['mean'] - prescribe_desc['std'] #calculates mean - standard deviation for plotting
mean_add_std = prescribe_desc['mean'] + prescribe_desc['std'] #calculates mean + standard deviation for plotting

plt.subplots(figsize=(20,10)) #plot mean, plus and minus standard deviation, need to add key

ave_plot = plt.plot(prescribe_desc['mean'])
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

