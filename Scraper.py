import csv
import requests
from bs4 import BeautifulSoup
import AI_Tools

def csv_to_array(file_path):
    Data_array=[]
    with open(file_path,'r') as file:
        csv_reader=csv.reader(file)
        for row in csv_reader:           
            Data_array.append(row)
            
    return Data_array

def GetPageMetaData(URL,otherData):
    response = requests.get(URL)
    soup = BeautifulSoup(response.text, features="lxml")
    metas = soup.find_all('meta')
    metas=str(metas)
    interests = AI_Tools.DecodeAIRetur(AI_Tools.GetResponse(f"based on the following data, {metas} and {otherData} what are the interest of this accounts, give a list of 5 answers with no comentary"))
    return interests

def GenInterest(candidateFile, otherData):
    
    #candidate will be a user name that will then be given some atrabute interests that will be returned to be sent to the AI tool
    interest =""
    
    for i in candidateFile:
        interest=interest+GetPageMetaData(i,otherData)
    return interest

