import tkinter as tk
from tkinter import ttk
import sqlite3
import shutil
import datetime
import os
import atexit
import sys
import random
import sqlite3, os
import base64
import json

current_dir = os.path.abspath(os.path.dirname(__file__))
MAIN_dir = os.path.join(os.path.join(current_dir, '..'), '..')
sys.path.append(MAIN_dir)

data_dir = os.path.join(MAIN_dir, 'data')
db_path = os.path.join(data_dir, 'my_database.db')
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

import requests

current_dir = os.path.abspath(os.path.dirname(__file__))
MAIN_dir = os.path.join(current_dir, '..')
sys.path.append(MAIN_dir)



# API Connection 
def Sand_API(url, entry):
    response_data = None
    try:
        # Send the data to the API
        print('Chacke_Connection Data  ', entry)
        print('Chacke_Connection Data send to ', url)
        
        response = requests.post(url, json=entry)

        if response.status_code == 200:
            print('Chacke_Connection Data sent successfully.')
            print('Chacke_Connection Data sent response.', response)
            try:
                response_data = response.json()
            except requests.exceptions.RequestException as e:
                print('Chacke_Connection Failed to read data:', e)
            return response_data
        else:
            print('Chacke_Connection Failed to retrieve data from the website.')
    except requests.exceptions.RequestException as e:
        print('Chacke_Connection Failed to send data:', e)
    return None
    
def Chacke_Connection(Link):
    url = Link
    entry = {'Do': "Testing Connection", 'shop': 0, 'user' : 0, 'ISNEW_USER' : 0 , 'ISNEW_SHOP' : 0 }
    while 1:
        response_data = Sand_API(url, entry)
        if response_data and not response_data == []:
            if response_data['status'] == 'success':
                print("Chacke_Connection there is connection")
                return True
            elif response_data['status'] == 'Erorr':
                if response_data['Erorr'] == 'NO USER FOUND':
                    print("Chacke_Connection there is Erorr")
                elif response_data['Erorr'] == 'NO SHOP FOUND':
                    print("Chacke_Connection there is Erorr")
                elif response_data['Erorr'] == 'Try Agane':
                    print("Chacke_Connection there is Erorr")    
                elif response_data['Erorr'] == 'FILED REGISTERING SHOP':
                    print("Chacke_Connection there is Erorr")
            else:
                print('Chacke_Connection Failed to save data:', response_data['message'])
                #self.found_linke_list_box.insert('', 'end', text="Failed Reading Data", values=(shop['Shop_name'], shop['Shop_link']))
                break
        break
