#!/usr/bin/python3

#pip3 install requests pandas matplotlib

#Import required packages------------------------------------------------------------------------------------------------------------------------------------------------------
import requests, csv, json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

#Define functions--------------------------------------------------------------------------------------------------------------------------------------------------------------

#Download data in json format and load into pandas dataframe
def download(API):
    df = pd.DataFrame.from_dict(requests.get(API).json()) #gets data from API in json format, and creates pandas dataframe from dictionary format of json file 
    return(df)

"""
If the API is down, a CSV is provided as a test
"""
try:
	
	spendingAPI= 'https://openprescribing.net/api/1.0/spending_by_practice/?code=5.1&format=json&org=14L' #API for number of antibiotics prescribed by practice in Manchester CCG
	listsizeAPI= 'https://openprescribing.net/api/1.0/org_details/?format=json&org_type=practice&org=14L&keys=total_list_size' #API for number of patients by practice in Manchester CCG

	new_df = pd.merge(download(API=spendingAPI), download(API= listsizeAPI), on=['row_id','date', 'row_name']) #downloads data in json format using APIs and loads into pandas dataframes, then merges dataframes on three columns

except:
	prescribe_data = pd.read_csv("spending-by-practice-0501.csv") #csv of number of antibiotics by practice in Manchester CCG, data same as spendingAPI
	size_data = pd.read_csv("Total-list-size-14L.csv") #csv of number of patients by practive in Manchester CCG, data same as listsizeAPI

	new_df = pd.merge(prescribe_data, size_data, on=['row_id','date', 'row_name'])

new_df['items per 1000'] = new_df['items']/new_df['total_list_size']*1000 #Adds column to dataframe of prescribed items per 1,000 registered patients as some practices are smaller than others
print(new_df) #prints to check df is correct and check normalised column has appended correctly

#Plot graphs of prescribed items over time for each practice in Manchester CCG-------------------------------------------------------------------------------------------------

#Define function for plotting graphs

def plot(x, y, label, xlabel, ylabel, name):
    fig, ax = plt.subplots(figsize=(30,10)) #Plots graph of size 30,10
    plt.title(label, loc='center', pad=None)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    for key, grp in new_df.groupby(['row_name']): 
        ax = grp.plot(ax=ax, kind='line', x=x, y=y, label=key) #Specifies graph as line graph, and determines what is on each axis
    ax.legend(bbox_to_anchor=(1.01, 1.05), ncol = 2) # moves the legend so that it sits outside the plot and has two columns
    fig.savefig('{}.png'.format(name), format='png', dpi=200) #save figure as png with specified name
    plt.close(fig)

#Plot graphs
plot(x='date', y='items', label = "Antibiotics prescribed by GP practices in Manchester CCG over time", name="antibiotics_prescribed_in_Manchester_over_time", xlabel = "Date", ylabel= "Number of antibiotics prescribed") #plot basic graph showing number of antibiotics prescribed by each practice each month over time
plot(x='date', y='items per 1000', label = "Graph of antibiotics prescribed per 1000 patients by GP practices in Manchester CCG over time", name="normalised_antibiotics_prescribed_in_manchester_over_time", xlabel = "Date", ylabel = "Number of antibiotics prescribed") #plots normalised graph accounting for patient population size (prescribed items per 1,000 registered patients)

#Graph of mean for whole Manchester CCG----------------------------------------------------------------------------------------------------------------------------------------
prescribe_desc = new_df.groupby(by='date')['items per 1000'].describe() #Calculates mean and standard deviation across all practices for each month per 1000 registered patients
print(prescribe_desc) #print to check df is correct and mean/std have been calculated correctly

fig, ax = plt.subplots(figsize=(20,10)) #specifies size of plot
plt.title(label='Mean antibiotics prescribed per 1000 patients in Manchester CCG', loc='center', pad=None) #specify graph title and positioning
plt.xlabel("Date") #specify x-axis label
plt.ylabel("Antibiotics prescribed per 1000 patients") #specify y-axis label
plt.xticks(rotation=90) #rotates the axis labels 90 degrees so that they are readable
plt.show(plt.plot(prescribe_desc['mean'])) #plots the graph of the mean
fig.savefig('Normalised_mean_antibiotics.png', format='png', dpi=200) #save figure as png
plt.close(fig)

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
fig = sns.boxplot(x=new_df['date'], y=new_df['items per 1000']) #use seaborn to plot boxplot of month vs antibiotics prescribed per 1000 patients
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
for date in new_df['date'].unique():
    outliers = calculate_outliers_iqr_method(new_df[new_df['date'] == date]['items per 1000'])
    for outlier in outliers:
        outlier_list.append([date, outlier])
		
outlier_df = pd.DataFrame(outlier_list, columns = ['date', 'items per 1000']) # puts the list of outliers in a dataframe with 2 columns (date and outlier). Outlier column is named 'items per 1000' so that these values can be mapped back to the original dataframe to find the associated practice
outlier_df.head() # checks dataframe has been created correctly by printing first 5 rows

outlier_practice = pd.merge(outlier_df, new_df, on=['date', 'items per 1000']) #merges outlier df with original df using date and items per 1000

outlier_practice = outlier_practice.drop(columns = ['setting', 'actual_cost', 'items', 'quantity', 'total_list_size']) # removes columns we don't need in this dataframe
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
plt.show() #show plot


#pivot df to be by practice and create a heatmap
data_by_practice = new_df.pivot(index='row_name', columns='date', values='items per 1000') # pivots data frame so that it gives items per 1000 by practice over time

data_by_practice.head() # previews first 5 rows to check data frame has been pivotted correctly


plt.title(label='Antibiotics prescribed per 1000 patients in Manchester CCG by practice', loc='center', pad=None) #specifies title of plot

sns.heatmap(data_by_practice, cmap='coolwarm', robust=True) # plots a heatmap where low prescribing is blue and high prescribing is red, robust sets contrast levels based on quantiles

				
#Notes - still to do-----------------------------------------------------------------------------------------------------------------------------------------------------------

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