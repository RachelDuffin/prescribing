#pip3 install requests
#pip3 install numpy
#pip3 install pandas
#cd /home/rachel/Documents/prescription_project


#Import required packages----------------------------------------------------------------------------------------------------------------------------------------------------------------
import requests, csv, json, sys
import numpy as np
import pandas as pd

#Download the data using APIs------------------------------------------------------------------------------------------------------------------------------------------------------------
antibiotics = requests.get(“https://openprescribing.net/api/1.0/spending_by_practice/?code=5.1&org=14L“) #gets json file of antibiotics prescribed per practice in Manchester CCG
patients = requests.get(“https://openprescribing.net/api/1.0/org_details/?org_type=practice&org=14L&keys=total_list_size“) #gets total list size per GP practice in Manchester CCG

