#!/usr/bin/python3

#pip3 install requests pandas matplotlib

#Import required packages------------------------------------------------------------------------------------------------------------------------------------------------------
import requests, csv, json
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

#Plot graphs of prescribed items over time for each practice in Manchester CCG-------------------------------------------------------------------------------------------------

#Define function for plotting graphs
def plot(x, y, label, xlabel, ylabel):
    fig, ax = plt.subplots(figsize=(30,10)) #Plots graph of size 30,10
    plt.title(label, loc='center', pad=None)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    for key, grp in new_df.groupby(['row_name']): 
        ax = grp.plot(ax=ax, kind='line', x=x, y=y, label=key) #Specifies graph as line graph, and determines what is on each axis
    plt.show()

#Plot graphs
plot(x='date', y='items', label = "Antibiotics prescribed by GP practices in Manchester CCG over time", xlabel = "Date", ylabel= "Number of antibiotics prescribed") #plot basic graph showing number of antibiotics prescribed by each practice each month over time
plot(x='date', y='items per 1000', label = "Graph of antibiotics prescribed per 1000 patients by GP practices in Manchester CCG over time", xlabel = "Date", ylabel = "Number of antibiotics prescribed") #plots normalised graph accounting for patient population size (prescribed items per 1,000 registered patients)

#Graph of mean for whole Manchester CCG----------------------------------------------------------------------------------------------------------------------------------------
prescribe_desc = new_df.groupby(by='date')['items per 1000'].describe() #Calculates mean and standard deviation across all practices for each month per 1000 registered patients
print(prescribe_desc) #print to check df is correct and mean/std have been calculated correctly

plt.subplots(figsize=(20,10)) #specifies size of plot
plt.title(label='Mean antibiotics prescribed per 1000 patients in Manchester CCG', loc='center', pad=None)
plt.xlabel("Date")
plt.ylabel("Antibiotics prescribed per 1000 patients")
plt.xticks(rotation=90) #rotates the axis labels 90 degrees so that they are readable
plt.show(plt.plot(prescribe_desc['mean'])) #plots the graph of the mean

#Graph of mean +- 1 standard deviation for Manchester CCG----------------------------------------------------------------------------------------------------------------------
mean_min_std = prescribe_desc['mean'] - prescribe_desc['std'] #calculates mean - standard deviation for plotting
mean_add_std = prescribe_desc['mean'] + prescribe_desc['std'] #calculates mean + standard deviation for plotting

plt.subplots(figsize=(20,10)) #plot mean, plus and minus standard deviation, need to add key
plt.title(label='Mean plus minus one standard deviation of antibiotics prescribed per 1000 patients in Manchester CCG', loc='center', pad=None)
plt.xlabel("Date")
plt.ylabel("Antibiotics prescribed per 1000 patients")
ave_plot = plt.plot(prescribe_desc['mean']) #plot mean line
ave_plot2 = plt.plot(mean_min_std) #plot mean - standard deviation line
ave_plot3 = plt.plot(mean_add_std) #plot mean + standard deviation line
plt.xticks(rotation=90) #rotates the axis labels 90 degrees so that they are readable
plt.show() #show plot


#create boxplot to see spread of data for each month
import seaborn as sns
plt.figure(figsize=(20, 10))
bplot = sns.boxplot(x=new_df['date'], y=new_df['items per 1000'])
plt.xticks(rotation=90)

# output file name
plot_file_name="boxplot.jpg"
 
# save boxplot as jpeg
bplot.figure.savefig(plot_file_name,
                    format='jpeg',
                    dpi=100)

#Notes - still to do-----------------------------------------------------------------------------------------------------------------------------------------------------------
#Sort out the graph axis labels
#Add a mean line for all CCGs to manchester mean graph
#Add grey band for standard deviation either side of mean
#Find outliers for mean graph
#Add tests
#Download a dataset to test it with - save a csv file and upload to github
#Possibly create boxplot using .boxplot
#Remove zeros/append to a file so we know which have been removed?
#Maybe define some more functions
#Maybe make a heat map
#Add min and max practice to our mean line graph

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------