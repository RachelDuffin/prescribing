#!/usr/bin/python3

#pip3 install requests pandas matplotlib seaborn 

#Import required packages------------------------------------------------------------------------------------------------------------------------------------------------------
import requests, csv, json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

#Create empty log file---------------------------------------------------------------------------------------------------------------------------------------------------------

Path('log.txt').touch() #creates empty log file

#Download data in json format and load into pandas dataframe-------------------------------------------------------------------------------------------------------------------
def download(API):
    df = pd.DataFrame.from_dict(requests.get(API).json()) #gets data from API in json format, and creates pandas dataframe from dictionary format of json file 
    return(df)

print("If the API is down, a CSV is provided as a test")

try:
    try:
        spendingAPI= 'https://openprescribing.net/api/1.0/spending_by_practice/?code=5.1&format=json&org=14L' #API for number of antibiotics prescribed by practice in Manchester CCG
        listsizeAPI= 'https://openprescribing.net/api/1.0/org_details/?format=json&org_type=practice&org=14L&keys=total_list_size' #API for number of patients by practice in Manchester CCG
        prescribing_df = pd.merge(download(API=spendingAPI), download(API= listsizeAPI), on=['row_id','date', 'row_name']) #downloads data in json format using APIs and loads into pandas dataframes, then merges dataframes on three columns
    except:
            print("Data could not be downloaded from APIs, trying csv files")
    else:
        print("Data successfully downloaded from API:")
except:
    try:
	    prescribe_data = pd.read_csv("spending-by-practice-0501.csv") #csv of number of antibiotics by practice in Manchester CCG, data same as spendingAPI
	    size_data = pd.read_csv("Total-list-size-14L.csv") #csv of number of patients by practive in Manchester CCG, data same as listsizeAPI
	    prescribing_df = pd.merge(prescribe_data, size_data, on=['row_id','date', 'row_name'])
    except:
            print("Data could not be loaded from csv files")
    else:
            print("Data successfully loaded from csv files:")

prescribing_df['items per 1000'] = prescribing_df['items']/prescribing_df['total_list_size']*1000 #Adds column to dataframe of prescribed items per 1,000 registered patients as some practices are smaller than others
print(prescribing_df) #prints to check df is correct and check normalised column has appended correctly

#if prescribing_df.empty == True:
#       print('DataFrame is empty')
#else:
#        print('DataFrame is not empty')


#Define graph functions-------------------------------------------------------------------------------------------------

#Line graphs

def plot(x, y, label, xlabel, ylabel, filename, multi_line_graph):
    fig, ax = plt.subplots(figsize=(30,10)) #Plots graph of size 30,10
    plt.title(label, loc='center', pad=None)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.xticks(rotation=90) #rotates the axis labels 90 degrees so that they are readable
    if multi_line_graph==True:
        for key, grp in prescribing_df.groupby(['row_name']): 
            ax = grp.plot(ax=ax, kind='line', x=x, y=y, label=key) #Specifies graph as line graph, and determines what is on each axis
    ax.legend(bbox_to_anchor=(1.01, 1.05), ncol = 2) # moves the legend so that it sits outside the plot and has two columns
    fig.savefig('{}.png'.format(filename), format='png', dpi=200) #save figure as png with specified name
    plt.close(fig)

#Scatter graphs



#Plot graphs of prescribed items over time for each practice in Manchester CCG (using defined functions)-------------------------------------------------------------------------------------------------

#Plot graphs
ccgs_plot = plot(x='date', y='items', 
            label = "Antibiotics prescribed by GP practices in Manchester CCG over time", 
            filename="antibiotics_prescribed_in_Manchester_over_time", 
            xlabel = "Date", ylabel= "Number of antibiotics prescribed", 
            multi_line_graph=True) #plot basic graph showing number of antibiotics prescribed by each practice each month over time

mean_ccgs_plot = plot(x='date', y='items per 1000', 
            label = "Graph of antibiotics prescribed per 1000 patients by GP practices in Manchester CCG over time", 
            filename="normalised_antibiotics_prescribed_in_manchester_over_time", 
            xlabel = "Date", ylabel = "Number of antibiotics prescribed", 
            multi_line_graph=True) #plots normalised graph accounting for patient population size (prescribed items per 1,000 registered patients)

#Graph of mean for whole Manchester CCG- NOT WORKING!----------------------------------------------------------------------------------------------------------------------------------------
prescribe_desc = prescribing_df.groupby(by='date')['items per 1000'].describe() #Calculates mean and standard deviation across all practices for each month per 1000 registered patients
prescribe_desc = prescribe_desc.reset_index()
print(prescribe_desc) #print to check df is correct and mean/std have been calculated correctly

manchester_mean = plot(x = prescribe_desc['date'], y = prescribe_desc['mean'],          
                    xlabel= 'Date',
                    ylabel= 'Antibiotics prescribed per 1000 patients',
                    label = 'Graph of mean per 1000 patients for Manchester CCG',
                    filename='Normalised_mean_antibiotics',
                    multi_line_graph=False)

#Graph of mean +- 1 standard deviation for Manchester CCG----------------------------------------------------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(20,10)) #specify figure size
plt.title(label='Mean plus minus one standard deviation of antibiotics prescribed per 1000 patients in Manchester CCG', loc='center', pad=None)
plt.xlabel("Date")
plt.ylabel("Antibiotics prescribed per 1000 patients")
ave_plot = ax.plot(prescribe_desc.index.values, prescribe_desc['mean'], label = 'Mean') #plot mean line
plt.fill_between(prescribe_desc.index.values, prescribe_desc['mean'] - prescribe_desc['std'], prescribe_desc['mean'] + prescribe_desc['std'], color='#888888', alpha=0.4, label = 'Standard deviation') #shades in grey one standard deviation above and below the mean, in brackets the x-axis values are specified, then the lower values on the y-axis followed by upper values

ave_plot4 = ax.plot(prescribe_desc.index.values, prescribe_desc['min'], label = 'Minimum') #plots minimum values for each date
ave_plot4 = ax.plot(prescribe_desc.index.values, prescribe_desc['max'], label = 'Maximum') #plots maximum values for each date

ax.legend() #creates a key using the label values

plt.xticks(rotation=90) #rotates the axis labels 90 degrees so that they are readable
fig.savefig('Mean_and_sd_antibiotics_per_1000_patients.png', format='png', dpi=200) #save figure as png

#Boxplot showing spread of data within each month------------------------------------------------------------------------------------------------------------------------------
plt.figure(figsize=(20, 10)) #plot figure of size 20,10
fig = sns.boxplot(x=prescribing_df['date'], y=prescribing_df['items per 1000']) #use seaborn to plot boxplot of month vs antibiotics prescribed per 1000 patients
plt.xticks(rotation=90) #plots the x labels at a 90 degree rotation
fig.figure.savefig("boxplot.png",
                    format='png',
                    dpi=200)

#defines a function to calculate outliers using interquartile range
def calculate_outliers_iqr_method(values):

    q1 = values.quantile(q=0.25)
    q3 = values.quantile(q=0.75)
    iqr = q3 - q1

    outliers = []
    for value in values:
        if value > q3 + 1.5*iqr or value < q1 - 1.5*iqr:
            outliers.append(value)

    return outliers					
					
outlier_list = [] # creates an empty list for outliers to be appended to

# uses the outlier function to find the outliers for each month then adds the date and outlier value to a list as a tuple
for date in prescribing_df['date'].unique():
    outliers = calculate_outliers_iqr_method(prescribing_df[prescribing_df['date'] == date]['items per 1000'])
    for outlier in outliers:
        outlier_list.append([date, outlier])
		
outlier_df = pd.DataFrame(outlier_list, columns = ['date', 'items per 1000']) # puts the list of outliers in a dataframe with 2 columns (date and outlier). Outlier column is named 'items per 1000' so that these values can be mapped back to the original dataframe to find the associated practice
outlier_df.head() # checks dataframe has been created correctly by printing first 5 rows

outlier_practice = pd.merge(outlier_df, prescribing_df, on=['date', 'items per 1000']) #merges outlier df with original df using date and items per 1000

outlier_practice = outlier_practice.drop(columns = ['setting', 'actual_cost', 'items', 'quantity', 'total_list_size']) # removes columns we don't need in this dataframe
print(outlier_practice) # prints df to check it's correct
print(outlier_practice) # prints df to check it's correct

outlier_practice.to_csv('outlier.csv') # puts list of dates and outliers into a csv

# plot outliers on graph of the mean
fig, ax = plt.subplots(figsize=(20,10)) #creates a space to plot the graph
plt.title(label='Prescription outliers in Manchester CCG', loc='center', pad=None) #specifies title of plot
plt.xlabel("Date") #specifies label of the x-axis
plt.ylabel("Antibiotics prescribed per 1000 patients") #specifies label for y-axis
ave_plot = ax.plot(prescribe_desc.index.values, prescribe_desc['mean'], label = 'Mean') #plots mean line
ax = sns.scatterplot(x='date', y='items per 1000', data=outlier_practice, hue='row_name', marker = 'x') #uses the outlier data to plot a scatter graph with each practice a different colour
ax.legend() #creates a key using the label values
plt.xticks(rotation=90) #rotates the axis labels 90 degrees so that they are readable

#Create a heatmap--------------------------------------------------------------------------------------------------------------------------------------------------------------
data_by_practice = prescribing_df.pivot(index='row_name', columns='date', values='items per 1000') #pivots data frame so that it gives items per 1000 by practice over time

data_by_practice.head() #previews first 5 rows to check data frame has been pivotted correctly

plt.title(label='Antibiotics prescribed per 1000 patients in Manchester CCG by practice', loc='center', pad=None) #specifies title of plot

sns.heatmap(data_by_practice, cmap='coolwarm', robust=True) #plots a heatmap where low prescribing is blue and high prescribing is red, robust sets contrast levels based on quantiles

#Notes - still to do-----------------------------------------------------------------------------------------------------------------------------------------------------------

#Add a mean line for all CCGs to manchester mean graph
#Add tests
#Remove zeros/append to a file so we know which have been removed?
#Maybe define some more functions
#Add min and max practice to our mean line graph

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------