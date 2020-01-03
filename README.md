# Analysis of antibiotic prescription data for Manchester CCG (Clinical Commissioning Group)


## Installation

### Basic package installation

For this project, you must have the following packages installed on your system:
```
    Python 3
    PIP 3
```
Check python3 is installed:
```
which python3
```
If not installed, install python3:
```
sudo apt-get install python3
```
Check pip3 is installed:
```
which pip3
```
If not installed, install pip3:
```
sudo apt-get install python3-pip
```

### Further package installation using virtualenv

It is recommended that you use virtualenv to create an isolated Python environment. This enables multiple side-by-side installations of Python, one for each project, allowing different project environments to remain isolated. This means you are able to run this script without its installations affecting other projects. 

Install virtualenv:
```
pip3 install virtualenv
```

The packages required to run the script are located in 'requirements.txt'. To install these packages, run:
```
pip3 install -r requirements.txt
```

## Graphical output

To run the python script, run:
```
python3 prescription_script.py
```
The script will attempt to acquire two sets of data for GP practices in Manchester Clinical Commissioning Group (CCG) using two API keys provided by openprescribing.net. These sets of data are: 
*The number of antibiotic prescription events per GP practice per month. 
*The number of patients registered at each GP practice per month.

Progress is indicated by messages in the terminal. A box will appear part way through the analysis asking for the user to specify a location for saving the output graph files. If the user does not specify a filesave location (i.e. clicks the cancel or close button), the default filesave location 'graphs' is used. 

After specifying a filesave location, a set of six graphical outputs will be produced, displaying the antibiotic prescription data for GP practices in Manchester CCG in a way that can be more easily interpreted by the user. 

### Antibiotics prescribed in Manchester CCG
![](https://github.com/RachelDuffin/prescribing/blob/master/graphs/antibiotics_prescribed_in_Manchester_over_time.png)
This graph visualises the number of prescription events by each GP practice in Manchester CCG for each month in each year currently available on openprescribing.net. Each GP practice is represented by a coloured line as described in the key, enabling a visualisation of the trends for each GP practice in prescribing over time. However, this graph has obvious drawbacks. It is not very clear due to the large number of GP practices present in Manchester CCG meaning many lines are present on the graph. Additionally, different GP practices have different numbers of patients registered so this graph does not allow comparison of prescribing between different GP practices. To solve this second problem, the graph below is generated:

### Normalised antibotics prescribed in Manchester CCG:
![](https://github.com/RachelDuffin/prescribing/blob/master/graphs/normalised_antibiotics_prescribed_in_manchester_over_time.png)
This graph is similar to the graph above, however the data displayed has been normalised. Each line represents that prescriptions per 1000 registered patients for that GP practice, allowing better comparison between GP practices within Manchester. However, this graph is still difficult to interpret due to the large number of GP practices that have been plotted. 

### Mean, max, min and standard deviation plot:
![](https://github.com/RachelDuffin/prescribing/blob/master/graphs/Mean_and_sd_antibiotics_per_1000_patients.png)
This graph gives a more general indication of the trends in prescribing in Manchester CCG as a whole. The mean prescriptions in Manchester CCG for each month per 1000 registered patients have been plotted, with one standard deviation either side of the mean highlighted in grey. The maximum and minimum number of antibiotics prescribed by individual GP practices each month are plotted. This gives an overall visualisation of the spread of the data. 

### Outliers for antibiotic prescriptions in Manchester CCG:
![](https://github.com/RachelDuffin/prescribing/blob/master/graphs/Prescription_outliers_in_Manchester_CCG.png)
To highlight the GP practices and months for which prescribing falls outside of the expected range of values, a graph plotting the outliers and mean line for antibitoics prescribed per 1000 registered patients was created. GP practice names corresponding to each outlier are indicated in the key. 

### Box plot of antibiotics prescribed in Manchester CCG:
![](https://github.com/RachelDuffin/prescribing/blob/master/graphs/Box_plot.png) 
The boxplot above was created from the antibiotics prescribed per 1000 registered patients each month in Manchester CCG. The box of each boxplot show the median and middle 50% of values, with the whiskers showing the highest and lowest values excluding any outliers. Outliers have been displayed as black diamonds. 

### Heatmap of antibotics prescribed in Manchester CCG:
![](https://github.com/RachelDuffin/prescribing/blob/master/graphs/Heatmap.png)
The key is indicated on the right, with number of prescriptions per 1000 registered patients for each month at each GP practice in Manchester indicated by the key on the right (high number of prescriptions are displayed in red, and low in blue). This provides an easy visual summary of which practices and which months contain the highest and lowest number of prescriptions. 
