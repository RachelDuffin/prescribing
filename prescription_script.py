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

print("If the API is down, a CSV is provided as a test.")

try:
    try:
        spendingAPI= 'https://openprescribing.net/api/1.0/spending_by_practice/?code=5.1&format=json&org=14L' #API for number of antibiotics prescribed by practice in Manchester CCG
        listsizeAPI= 'https://openprescribing.net/api/1.0/org_details/?format=json&org_type=practice&org=14L&keys=total_list_size' #API for number of patients by practice in Manchester CCG
        prescribing_df = pd.merge(download(API=spendingAPI), download(API= listsizeAPI), on=['row_id','date', 'row_name']) #downloads data in json format using APIs and loads into pandas dataframes, then merges dataframes on three columns
    except:
        print("Data could not be downloaded from APIs, trying csv files")
    else:
        print("Data successfully downloaded from API.")
except:
    try:
	    prescribe_data = pd.read_csv("spending-by-practice-0501.csv") #csv of number of antibiotics by practice in Manchester CCG, data same as spendingAPI
	    size_data = pd.read_csv("Total-list-size-14L.csv") #csv of number of patients by practive in Manchester CCG, data same as listsizeAPI
	    prescribing_df = pd.merge(prescribe_data, size_data, on=['row_id','date', 'row_name'])
    except:
        print("Data could not be loaded from csv files")
    else:
        print("Data successfully loaded from csv files:")

#Define functions-------------------------------------------------------------------------------------------------

#Calculation of outliers using interquartile range
def calculate_outliers_iqr_method(values):

    q1 = values.quantile(q=0.25)
    q3 = values.quantile(q=0.75)
    iqr = q3 - q1

    outliers = []
    for value in values:
        if value > q3 + 1.5*iqr or value < q1 - 1.5*iqr:
            outliers.append(value)
    return outliers		

#Line plots

def line_plot(x, y, title, xlabel, ylabel, filename, multi_line_graph, whole_ccg):
    plt.title(title, loc='center', pad=None) #specify graph title and positioning ylabel, filename, multi_line_graph, whole_ccg):
    fig, ax = plt.subplots(figsize=(30,10)) #Plots graph of size 30,10
    plt.title(title, loc='center', pad=None)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.xticks(rotation=90) #rotates the axis labels 90 degrees so that they are readable
    if multi_line_graph==True:
        for key, grp in prescribing_df.groupby(['row_name']): 
            ax = grp.plot(ax=ax, kind='line', x=x, y=y, label=key) #Specifies graph as line graph, and determines what is on each axis
    if whole_ccg ==True:
        ax.plot(x, y, label='Prescriptions') #plots the graph of the mean        
    ax.legend(bbox_to_anchor=(1.01, 1.05), ncol = 2) # moves the legend so that it sits outside the plot and has two columns
    plt.close(fig.savefig('{}.png'.format(filename), format='png', dpi=200)) #save figure as png with specified name

#Standard deviation plot

def std_ccg(x, y, title, xlabel, ylabel, filename, min, max, std):
    fig, ax = plt.subplots(figsize=(20,10)) #specifies size of plot
    plt.title(title, loc='center', pad=None) #specify graph title and positioning
    plt.xlabel(xlabel) #specify x-axis label
    plt.ylabel(ylabel) #specify y-axis label
    plt.xticks(rotation=90) #rotates the axis labels 90 degrees so that they are readable
    ax.plot(x, y, label='Mean') #plots the graph of the mean
    plt.fill_between(x, y - std, y + std,color='#888888', alpha=0.4, label = 'Standard deviation') #shades in grey one standard deviation above and below the mean, in brackets the x-axis values are specified, then the lower values on the y-axis followed by upper values
    ax.plot(x, min, label = 'Minimum')
    ax.plot(x, max, label = 'Maximum')
    ax.legend(bbox_to_anchor=(1.01, 1.05), ncol = 2) # moves the legend so that it sits outside the plot and has two columns
    plt.close(fig.savefig('{}.png'.format(filename), format='png', dpi=200)) #save figure as png	

#Scatter plot on mean line plot
def scatter(x, y, title, xlabel, ylabel, filename, scatter_x, scatter_y, hue, data):
    fig, ax = plt.subplots(figsize=(20,10)) #creates a space to plot the graph
    plt.title(title, loc='center', pad=None) #specify graph title and positioning
    plt.xlabel(xlabel) #specifies label of the x-axis
    plt.ylabel(ylabel) #specifies label for y-axis
    plt.xticks(rotation=90) #rotates the axis labels 90 degrees so that they are readable(self, parameter_list):
    ax.plot(x, y, label = 'Mean') #plots mean line
    ax = sns.scatterplot(x = scatter_x, y = scatter_y, hue = hue, data = data, legend = 'full') #uses the outlier data to plot a scatter graph with each practice a different colour
    plt.close(fig.savefig('{}.png'.format(filename), format='png', dpi=200)) #save figure as png	

#Calculations ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

#Calculate prescribed items per 1000 patients at each practice
prescribing_df['items_per_1000'] = prescribing_df['items']/prescribing_df['total_list_size']*1000 #Adds column to dataframe of prescribed items per 1,000 registered patients as some practices are smaller than others

#calculate mean and standard deviation across all practices per month
prescribe_desc = prescribing_df.groupby(by='date')['items_per_1000'].describe() #Calculates mean and standard deviation across all practices for each month per 1000 registered patients

#Caclulate outliers using outlier function

outlier_list = [] # creates an empty list for outliers to be appended to
 
for date in prescribing_df['date'].unique():
    outliers = calculate_outliers_iqr_method(prescribing_df[prescribing_df['date'] == date]['items_per_1000'])
    for outlier in outliers:
        outlier_list.append([date, outlier]) #determines outliers for each month and adds date and outlier value to a list as a tuple


outlier_df = pd.DataFrame(outlier_list, columns = ['date', 'items_per_1000']) # puts the list of outliers in a dataframe with 2 columns (date and outlier). Outlier column is named 'items per 1000' so that these values can be mapped back to the original dataframe to find the associated practice

outlier_practice = pd.merge(outlier_df, prescribing_df, on=['date', 'items_per_1000']) #merges outlier df with original df using date and items per 1000

outlier_practice = outlier_practice.drop(columns = ['setting', 'actual_cost', 'items', 'quantity', 'total_list_size']) # removes columns we don't need in this dataframe


#Add outliers to the original dataframe
#outlier_practice = pd.merge((pd.DataFrame(outlier_list, columns = ['date', 'items per 1000'])),  # creates dataframe of date and outliers (column named 'items per 1000' so values can be mapped back to the original dataframe to find the associated practice
 #                   pd.DataFrame(prescribing_df, columns = ['date', 'items per 1000', 'row_id', 'ccg', 'row_name']), #select the columns from the original dataframe that we need
  #                  on=['date', 'items per 1000']) #Merge created dataframe with original prescribing dataframe on 'date' and 'items per 1000'

#outlier_practice.index = outlier_practice['date'] #'date' column was the index, so this adds it as a column
#outlier_practice = outlier_practice.reset_index(drop=True)
#print(outlier_practice)

#Plot graphs of prescribed items over time for each practice in Manchester CCG (using defined functions)-------------------------------------------------------------------------------------------------

#Plot graph of antibiotics prescribed by GP practices in Manchester over time
practice_plot = line_plot(x='date', y='items', 
                title = "Antibiotics prescribed by GP practices in Manchester CCG over time", 
                filename="antibiotics_prescribed_in_Manchester_over_time", 
                xlabel = "Date", ylabel= "Number of antibiotics prescribed", 
                multi_line_graph=True, whole_ccg=False) #plot basic graph showing number of antibiotics prescribed by each practice each month over time

#Plot graph of normalised antibiotics prescribed by GP practices in Manchester over time
mean_practice_plot = line_plot(x='date', y='items_per_1000', 
                    title = "Graph of antibiotics prescribed per 1000 patients by GP practices in Manchester CCG over time", 
                    filename="normalised_antibiotics_prescribed_in_manchester_over_time", 
                    xlabel = "Date", ylabel = "Number of antibiotics prescribed", 
                    multi_line_graph=True, whole_ccg=False) #plots normalised graph accounting for patient population size (prescribed items per 1,000 registered patients)

#Plot graphs of mean for whole Manchester CCG------------------------------------------------------------------------------------------------------------------------------------------------------------

#Plot graph of normalised mean antibiotics for Manchester CCG
mean_ccg_plot = line_plot(x = prescribe_desc.index.values, y = prescribe_desc['mean'], 
                title = "Normalised mean antibiotics prescribed per 1000 patients in Manchester CCG", 
                xlabel = "Date", ylabel = "Antibiotics prescribed per 1000 patients", 
                filename = "Normalised_mean_antibiotics", 
                multi_line_graph=False, whole_ccg=True)

#Plot graph of mean +- 1 standard deviation for Manchester CCG-------------------------------------------------------------------------------------------------------------------------------------------
mean_std_ccg_plot = std_ccg(x = prescribe_desc.index.values, y =  prescribe_desc['mean'], 
                    title = 'Mean plus minus one standard deviation of antibiotics prescribed per 1000 patients in Manchester CCG', 
                    xlabel = "Date", 
                    ylabel = "Antibiotics prescribed per 1000 patients",
                    min = prescribe_desc['min'],
                    max = prescribe_desc['max'],
                    std = prescribe_desc['std'],
                    filename = "Mean_and_sd_antibiotics_per_1000_patients")

#Plot boxplot showing spread of data within each month-----------------------------------------------------------------------------------------------------------------------------

plt.figure(figsize=(20, 10)) #plot figure of size 20,10
fig = sns.boxplot(prescribing_df['date'], prescribing_df['items_per_1000']) #use seaborn to plot boxplot of month vs antibiotics prescribed per 1000 patients
plt.xticks(rotation=90) #plots the x labels at a 90 degree rotation
plt.title(label= 'Boxplot showing antibiotics prescribed per 1000 patients in Manchester CCG per month', loc='center', pad=None) #specifies title of plot
fig.figure.savefig("boxplot.png", format='png', dpi=200)			

#plotdata=pd.DataFrame(prescribing_df, columns = ['date', 'items per 1000'])

#pd.DataFrame.to_string(prescribing_df)

#Plot outliers on graph of the mean- IS SHOWING SOME ERRORS IN THIS SECTION!

outliers_line_graph = scatter(x = prescribe_desc.index.values, y =  prescribe_desc['mean'], 
                        title = 'Prescription outliers in Manchester CCG',
                        xlabel = 'Date',
                        ylabel = 'Antibiotics prescribed per 1000 patients',
                        filename = 'Prescription_outliers_in_Manchester_CCG',
                        scatter_x = outlier_practice.date, scatter_y = outlier_practice.items_per_1000,
                        hue = outlier_practice.row_name, data=outlier_practice
                        )

#Create a heatmap- WORKS FINE--------------------------------------------------------------------------------------------------------------------------------------------------------------
data_by_practice = prescribing_df.pivot(index='row_name', columns='date', values='items_per_1000') #pivots data frame so that it gives items per 1000 by practice over time

fig, ax = plt.subplots(figsize=(20,20))   #specify figure size
plt.title(label='Antibiotics prescribed per 1000 patients in Manchester CCG by practice', loc='center', pad=None) #specifies title of plot
plot = sns.heatmap(data_by_practice, cmap='coolwarm', robust=True) #plots a heatmap where low prescribing is blue and high prescribing is red, robust sets contrast levels based on quantiles
fig = plot.get_figure()
fig.savefig("Heatmap.png", format = 'png', dpi = 200)

#Notes - still to do-----------------------------------------------------------------------------------------------------------------------------------------------------------

#Add tests
#make an output saying graph plotted successfully after each graph 
#make output saying 'table is the expected size'

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------