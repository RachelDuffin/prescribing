#pip3 install requests
#pip3 install numpy
#pip3 install pandas

#Import required packages----------------------------------------------------------------------------------------------------------------------------------------------------------------
import requests, csv, json, sys
import numpy as np
import pandas as pd

#Download the data using APIs and load into pandas dataframe------------------------------------------------------------------------------------------------------------------------------------------------------------

spending = requests.get('https://openprescribing.net/api/1.0/spending_by_practice/?code=5.1&format=json&org=14L').json()#gets json file of antibiotics prescribed per practice in Manchester CCG in json format

print(json.dumps(spendingdata, indent=4, sort_keys=True)) #print data

spendingpd = pd.DataFrame(spending) #json to pandas dataframe for antibiotic data

list_size = requests.get('https://openprescribing.net/api/1.0/org_details/?org_type=practice&org=14L&keys=total_list_size').json() #gets total list size per GP practice in Manchester CCG in json format

listsizepd = pd.DataFrame(list_size) #json to pandas dataframe for patient number data

print(json.dumps(listdata, indent=4, sort_keys=True)) #print data


#Merge the two pandas data frames--------------------------------------------------------------------------------------------------------------------------------------------------------


