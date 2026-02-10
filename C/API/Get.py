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

from C.API import API

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

from D.Security import *
from C.API.API import *



# this will fetch data as dict list from data base
# query : str = the sql query
# values : tuple = the values to be used in the query
def fetch_as_dict_list(query, values):
    try:
        cur.execute(query, values)
        items = cur.fetchall()
         #print("items len", len(items))
        columns = [col[0] for col in cur.description]
        #print("columns")
        #print(str(columns))
        #print("items len", len(items))
        results = []
        for row in items:
            #print("row")
            #print(str(row))
            #print("items len", len(items))
            if len(columns) != len(row):
                raise ValueError("Mismatch between number of columns and rows "+ str(len(columns)) + ", "+ str(len(row)))
                
            results.append(dict(zip(columns, row)))
        return results
    except Exception as e:
        print("Error executing query:", e)
        return []


# USER

# THIS WILL GET User BY ITS GIVEN VALUES
# NAME AND PASSWORD IS RQUERDE FOR FACHING ALL INFO

def Get_WORKER(Link, ARG, VALUE):
    
    
    url = Link
    entry = {'Do': "GET USER", 'User_name': User_name, 'User_password' : User_password }
    while 1:
        response_data = Sand_API(url, entry)
        if not response_data == []:
            if response_data['status'] == 'success':
                if response_data['Value']:
                    print("USER FOUND")
                    return response_data['Value']
                else:
                    print("USER NOT FOUND")
                    return []
            else:
                print("There is Error FOUND")
                return False
        break

# FOR FACING ANY USER, COSTUMER EVEN WORKER BASIC INFO
# AT LIST NAME AND USER NAME IS RQUERDE
def Get_User(Link, ARG, VALUE):
    query = ""
    value = None
    for a, arg in  enumerate(ARG):
        if len(VALUE) > a:
            query += " " + arg + "=?"
            if value:
                value = value + (VALUE[a],)
            else:
                value = (VALUE[a], )
            if a+1 < len(ARG):
                query += " AND"

    if Link and islinked(Link):
        url = Link
        entry = {'Do': "GET USER", 'QUERYS': query, 'QUERYVALUES' : value }
        response_data = Sand_API(url, entry)
        if not response_data == [] and response_data:
            if response_data['status'] == 'success':
                if response_data['Value']:
                    print("USER FOUND")
                    return response_data['Value']
                else:
                    print("USER NOT FOUND")
                    return []
            else:
                print("There is Error FOUND")
    else:
        print("API Error")


    print("query ", query)
    print("value ", value)
    users = fetch_as_dict_list("SELECT * FROM USERS WHERE" + query, value)
    if users:
        return users
   

# Shop Get

# this will get user shop data with its name and brand name the user must be connected to that shop
# FOR FACING ANY Shop, COSTUMER EVEN WORKER BASIC INFO
# AT LIST NAME AND Shop NAME IS RQUERDE
def Get_Shop(Link, user, ARG, ShopsVALUE):
    query = ""
    value = None
    Shop = None
    for a, arg in  enumerate(ARG):
        if len(ShopsVALUE) > a:
            query += " " + arg + "=?"
            if value:
                value = value + (ShopsVALUE[a],)
            else:
                value = (ShopsVALUE[a], )
            if a+1 < len(ARG):
                query += " AND"

    if Link and islinked(Link):
        url = Link
        entry = {'Do': "GET SHOP", 'User': user, 'QUERYS': query, 'QUERYVALUES' : value }
        response_data = Sand_API(url, entry)
        if response_data and not response_data == []:
            if response_data['status'] == 'success':
                if response_data['Value']:
                    print("SHOP FOUND : ", response_data['Value'])
                    return response_data['Value']
                else:
                    print("SHOP NOT FOUND")
                    Shop = None
            else:
                print("There is Error FOUND")
                Shop = None
    else:
        print("API Error")

    print("shop query ", query)
    print("shop value ", value)
    if query == "":
        Shops = fetch_as_dict_list("SELECT * FROM Shops", ())
    else:
        Shops = fetch_as_dict_list("SELECT * FROM Shops WHERE" + query, value)
    if Shops:
        return Shops


# GET USER WORK SHOPS FROM LOCAL DATABASE Or Online
def Get_all_User_work_shops_info(Link, user, User_work_shops):
    print("Link : " + str(Link))
    Shops = []
    if User_work_shops and user:
        for Shop in User_work_shops:
            print("Shop : " + str(Shop))
            s = Get_Shop(Link, user, ["Shop_Id", "Shop_name", "Shop_brand_name"], [str(Shop[0]), str(Shop[1]), str(Shop[2])])
            print("s : " + str(s))
            if s:
                if isinstance(s, list) and len(s) > 0:
                    Shops.append(s[0])
                else:
                    Shops.append(s)
                print("Shops : ", Shops)
    return Shops


# setting up the database
def Get_Setting(user, ARG, VALUE):
    query = ""
    value = None

    for a, arg in  enumerate(ARG):
        if len(VALUE) > a:
            query += " " + arg + "=?"
            if value:
                value = value + (VALUE[a],)
            else:
                value = (VALUE[a], )
            if a+1 < len(ARG):
                query += " AND"
    cursor.execute("SELECT * FROM setting WHERE " + query, value)
    setting = cursor.fetchall()
    if setting:
        columns = [col[0] for col in cursor.description]
        return dict(zip(columns, setting[0]))
    else:
        return None
    
# END OF FILE