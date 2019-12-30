#!/usr/bin/python3

# pip3 install requests pandas matplotlib seaborn

# Import required packages---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
import requests
import csv
import json
import os
import shutil
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path


# DEFINE FUNCTIONS-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# create directory for graphical outputs
def create_directory(graphs):
    if os.path.exists(graphs):
        shutil.rmtree(graphs)  # removes directory if already exists
    os.makedirs(graphs)  # creates directory

# DATA CALCULATION FUNCTIONS

# Create dataframe from API data


def get_api_data(api):
    try:
        return pd.DataFrame.from_dict(requests.get(api).json())
    except:
        print("Could not download from API")


# Create dataframe from CSV data
def get_csv_data(csv):
    try:
        return pd.read_csv(csv)
    except:
        print("Data could not be loaded from csv files")


# Download and merge prescribing data
def download(spendingAPI, listsizeAPI, size_csv, prescribing_csv):  # specifies inputs for defined function
    prescribe_data = get_api_data(spendingAPI)
    size_data = get_api_data(listsizeAPI)

    if prescribe_data is None:
        print("Prescriptions data could not be downloaded from APIs, trying csv files")
        prescribe_data = get_csv_data(prescribing_csv)
        if prescribe_data is None:
            print("Prescriptions data could not be obtained from CSVs")
        if size_data is not None:
            print("Prescriptions data was obtained from CSV")
    else:
        print("Prescriptions data obtained from APIs")

    if size_data is None:
        print("Patient numbers data could not be downloaded from APIs, trying csv files")
        size_data = get_csv_data(size_csv)
        if size_data is None:
            print("Patient numbers data could not be obtained from CSV")
        if size_data is not None:
            print("Patient numbers data was obtained from CSV")
    else:
        print("Patient numbers data obtained from APIs")

    if size_data is not None and prescribe_data is not None:
        return pd.merge(prescribe_data, size_data, on=['row_id', 'date', 'row_name'])


# Calculate outliers using interquartile range
def calculate_outliers_iqr_method(values):
    q1 = values.quantile(q=0.25)  # calculates lower quartile
    q3 = values.quantile(q=0.75)  # calculates upper quartlie
    iqr = q3 - q1  # calculates interquartile range (iqr)

    outliers = []  # creates empty list for outliers
    for value in values:
        # if values are outside mean ± 1.5x iqr, append to outliers list
        if value > q3 + 1.5*iqr or value < q1 - 1.5*iqr:
            outliers.append(value)
    return outliers  # returns a list of outlier values


# create new dataframe with outliers and corresponding dates
def add_dates_to_outliers(unique_dates, column_names, prescribing_df):
    outlier_list = []  # creates an empty list for outliers to be appended to
    for date in unique_dates:  # from a list of unique date values in prescribig_df
        outliers = calculate_outliers_iqr_method(
            prescribing_df[prescribing_df['date'] == date]['items_per_1000'])  # calculate a list of outlier values from the 'items_per_1000' values within the grouped date values for each month
        for outlier in outliers:
            # appends outlier values from 'outliers' to a dataframe, along with corresponding date from the unique date values in prescribing_df
            outlier_list.append([date, outlier])
    # create a dataframe of outliers and dates from 'outlier_list'
    return pd.DataFrame(outlier_list, columns=column_names)


# Merge outliers with original dataframe
def outlier_merge(outlier_df, original_df, columns):
    subset = pd.DataFrame(original_df[['date', 'items_per_1000', 'row_name']])
    # puts outliers list into a dataframe with 2 columns, and merges on 'date' and 'items_per_1000' with a subset of prescribing_df
    return pd.merge(outlier_df, subset, on=columns)


# GRAPH PLOTTING FUNCTIONS

# Set text size for plots
def text_size(SMALL_SIZE, MEDIUM_SIZE, BIGGER_SIZE):
    # fontsize of the axes title, and x and y labels
    plt.rc('axes', titlesize=BIGGER_SIZE, labelsize=MEDIUM_SIZE)
    plt.rc('xtick', labelsize=SMALL_SIZE)  # fontsize of the tick labels
    plt.rc('ytick', labelsize=SMALL_SIZE)  # fontsize of the tick labels
    plt.rc('legend', fontsize=SMALL_SIZE)  # legend fontsize


# Set generic plot layout
def plot_layout(xlabel, ylabel, title):
    global fig, ax
    fig, ax = plt.subplots(figsize=(30, 10))  # Creates figure of specified
    fig.suptitle(title)  # specifies graph title
    plt.xlabel(xlabel)  # specifies x-axis label
    plt.ylabel(ylabel)  # specifies y-axis label
    # rotates axis labels 90 degrees (makes them readable)
    plt.xticks(rotation=90)


# Line plots
def line_plot(x, y, title, xlabel, ylabel, filename, prescribing_df):
    global ax
    plot_layout(xlabel, ylabel, title)
    for key, grp in prescribing_df.groupby(['row_name']):
        # plot a line for each set of grouped data
        ax = grp.plot(ax=ax, kind='line', x=x, y=y, label=key)
    # legend has two columns, and sits outside the plot
    ax.legend(bbox_to_anchor=(1.01, 1.05), ncol=2)
    # saves .png to graphs folder
    return plt.close(fig.savefig('graphs/{}.png'.format(filename), format='png', dpi=200))


# Standard deviation plot
def mean_stdev_plot(x, y, title, xlabel, ylabel, filename, min, max, std, legendtitle):
    plot_layout(xlabel, ylabel, title)
    ax.plot(x, y, label='Mean')  # plots mean line
    # shades ± one standard deviation of mean in grey
    plt.fill_between(x, y - std, y + std, color='#888888',
                     alpha=0.4, label='Standard deviation')
    ax.plot(x, min, label='Minimum')  # plots minimum value for each month
    ax.plot(x, max, label='Maximum')  # plots maximum value for each month
    ax.legend(title=legendtitle)  # creates legend with specified title
    # saves .png to graphs folder
    return plt.close(fig.savefig('graphs/{}.png'.format(filename), format='png', dpi=200))

# Scatter plot on mean line plot


def scatter_plot(x, y, title, xlabel, ylabel, filename, scatter_x, scatter_y, hue, data):
    global ax
    plot_layout(xlabel, ylabel, title)
    ax.plot(x, y, label='Mean')  # plots mean line
    # plots outlier data as scatter graph (each practice is a different colour)
    ax = sns.scatterplot(x=scatter_x, y=scatter_y,
                         hue=hue, data=data, legend='full')
    # saves .png to graphs folder
    return plt.close(fig.savefig('graphs/{}.png'.format(filename), format='png', dpi=200))


# Boxplot function using seaborn
def box_plot(x, y, xlabel, ylabel, title, filename):
    plot_layout(xlabel, ylabel, title)
    fig = sns.boxplot(x, y)  # plots boxplot from specified x and y values
    return fig.figure.savefig('graphs/{}.png'.format(filename), format='png',
                              dpi=200)  # saves .png to graphs folder


# plots a heatmap where low prescribing is blue and high prescribing is red, robust sets contrast levels based on quantiles
def heatmap(df, index, columns, values, xlabel, ylabel, title, filename):
    # pivots data frame so that it gives items per 1000 by practice over time
    data_by_practice = df.pivot(index, columns, values)
    plot_layout(xlabel, ylabel, title)
    plot = sns.heatmap(data_by_practice, cmap='coolwarm',
                       robust=True)  # plots the heatmap
    fig = plot.get_figure()
    return fig.savefig('graphs/{}.png'.format(filename), format='png',
                       dpi=200)  # saves .png to graphs folder


# Main method ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


def main():
    # create directory for graphical outputs
    create_directory('graphs')

    # Set graph text sizes
    text_size(SMALL_SIZE=10, MEDIUM_SIZE=14, BIGGER_SIZE=18)

    # Download data from APIs
    prescribing_df = download(spendingAPI='https://openprescribing.net/api/1.0/spending_by_practice/?code=5.1&format=json&org=14L',  # API for number of antibiotics prescribed by practice in Manchester CCG
                              # API for number of patients by practice in Manchester CCG
                                listsizeAPI='https://openprescribing.net/api/1.0/org_details/?format=json&org_type=practice&org=14L&keys=total_list_size',
                                prescribing_csv = "spending-by-practice-0501.csv",
                                size_csv = "Total-list-size-14L.csv"
                                )

    # Calculate prescribed items per 1000 patients at each practice
    # Adds column to dataframe of prescribed items per 1,000 registered patients as some practices are smaller than others
    prescribing_df['items_per_1000'] = prescribing_df['items'] / \
        prescribing_df['total_list_size']*1000

    # calculate mean and standard deviation across all practices per month
    # Calculates mean and standard deviation across all practices for each month per 1000 registered patients
    prescribe_desc = prescribing_df.groupby(
        'date')['items_per_1000'].describe().reset_index()

    # Caclulate outliers using outlier function
    outlier_df = add_dates_to_outliers(unique_dates=prescribing_df['date'].unique(),
                                       column_names=['date', 'items_per_1000'], prescribing_df=prescribing_df)

    # Merge outliers with the original dataframe
    outlier_practice = outlier_merge(
        outlier_df=outlier_df, original_df=prescribing_df, columns=['date', 'items_per_1000'])

    # Plot graphs of prescribed items over time for each practice in Manchester CCG (using defined functions)-------------------------------------------------------------------------------------------------

    # Plot graph of antibiotics prescribed by GP practices in Manchester over time
    line_plot(x='date', y='items', title="Antibiotics prescribed by GP practices in Manchester CCG over time", filename="antibiotics_prescribed_in_Manchester_over_time",
              xlabel="Date", ylabel="Number of antibiotics prescribed", prescribing_df=prescribing_df)  # plot basic graph showing number of antibiotics prescribed by each practice each month over time

    # Plot graph of normalised antibiotics prescribed by GP practices in Manchester over time
    line_plot(x='date', y='items_per_1000', title="Graph of antibiotics prescribed per 1000 patients by GP practices in Manchester CCG over time", filename="normalised_antibiotics_prescribed_in_manchester_over_time",
              xlabel="Date", ylabel="Number of antibiotics prescribed", prescribing_df=prescribing_df)  # plots normalised graph accounting for patient population size (prescribed items per 1,000 registered patients)

    # Plot graphs of mean for whole Manchester CCG------------------------------------------------------------------------------------------------------------------------------------------------------------

    # Plot graph of mean +- 1 standard deviation for Manchester CCG-------------------------------------------------------------------------------------------------------------------------------------------
    mean_stdev_plot(x=prescribe_desc['date'], y=prescribe_desc['mean'], title='Mean ± one standard deviation of antibiotics prescribed per 1000 patients for GP practices in Manchester CCG', xlabel="Date",
                    ylabel="Antibiotics prescribed per 1000 patients", min=prescribe_desc['min'], max=prescribe_desc['max'], std=prescribe_desc['std'], filename="Mean_and_sd_antibiotics_per_1000_patients", legendtitle="Antibiotics prescribed per 1000 people")

    # Plot graph of mean with outliers------------------------------------------------------------------------------------------------------------------------------------------------------------

    scatter_plot(x=prescribe_desc['date'], y=prescribe_desc['mean'], title='Prescription outliers in Manchester CCG', xlabel='Date', ylabel='Antibiotics prescribed per 1000 patients',
                 filename='Prescription_outliers_in_Manchester_CCG', scatter_x=outlier_practice['date'], scatter_y=outlier_practice['items_per_1000'], hue=outlier_practice.row_name, data=outlier_practice)

    # Plot boxplot showing spread of data within each month-----------------------------------------------------------------------------------------------------------------------------
    # use seaborn to plot boxplot of month vs antibiotics prescribed per 1000 patients
    box_plot(x=prescribing_df['date'], y=prescribing_df['items_per_1000'], xlabel='Date', ylabel='Antibiotics prescribed per 1000 patients',
             title='Boxplot showing antibiotics prescribed per 1000 patients in Manchester CCG per month', filename="Box_plot")

    # Create a heatmap---------------------------------------------------------------------------------------------------------------------------------------------------------------
    heatmap(df=prescribing_df, index='row_name', columns='date', values='items_per_1000', xlabel='Date', ylabel='GP Practice in Manchester',
            title='Antibiotics prescribed per 1000 patients in Manchester CCG by practice', filename='heatmap')

    # Notes - still to do-----------------------------------------------------------------------------------------------------------------------------------------------------------

    # Add tests
    # make an output saying graph plotted successfully after each graph
    # make output saying 'table is the expected size'

# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


if __name__ == "__main__":
    print("Starting analysis")
    main()
    print("Finishing analysis, graphs saved as png files")
