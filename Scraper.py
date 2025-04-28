import csv
import requests
from bs4 import BeautifulSoup
import Ralis_Sniffer_v1
import AI_Tools

def csv_to_array(file_path):
    Data_array=[]
    with open(file_path,'r') as file:
        csv_reader=csv.reader(file)
        for row in csv_reader:
            
            #some sort of filter to only keep in the URLs
            
            Data_array.append(row)
            
    return Data_array

def GetPageMetaData(URL):
    response = requests.get(URL)
    soup = BeautifulSoup(response.text)
    metas = soup.find_all('meta')
    metas=str(metas)
    AI_Tools.DecodeAIRetur(AI_Tools.GetResponse(f"based on the following meta data, {metas} what are the interest of this accounts, give a list of 5 answers with no comentary"))
    return

def GenInterest(candidateFile):
    
    #candidate will be a user name that will then be given some atrabute interests that will be returned to be sent to the AI tool
    interest =[]
    Accounts=csv_to_array(candidateFile)
    
    for i in Accounts:
        GetPageMetaData(i)
    return interest

