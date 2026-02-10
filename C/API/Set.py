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
cur = conn.cursor()

import requests

current_dir = os.path.abspath(os.path.dirname(__file__))
MAIN_dir = os.path.join(current_dir, '..')
sys.path.append(MAIN_dir)

from C.API import *
from C.API.Get import *
from C.API.Set import *


# USER
# THIS WILL SET User BY ITS GIVEN VALUES
# this function will add new user to system data base all data must be given
def Set_User(Link, ARG, VALUE, parent=None):
    query = "("
    value = None
    user_name = ""
    for a, arg in enumerate(ARG):
        if len(VALUE) > a:
            query += "`" + arg + "`, "
            if value:
                value = value + (VALUE[a],)
            else:
                value = (VALUE[a], )
            if arg == 'user_name':
                user_name = VALUE[a]
    if query != "(":    
        if query.endswith(", "):
            query = query[:-2]
        query += ") "
        query += "VALUES (" + ("?, " * len(ARG)).rstrip(", ") + ")"
    print("Set_User query ", query)
    User_data = None
    if Link and islinked(Link):
        url = Link
        entry = {'Do': "SET USER", 'QUERYS': query, 'QUERYVALUES' : value , 'user_name': user_name}
        response_data = Sand_API(url, entry)
        if not response_data == [] and response_data:
            if response_data['status'] == 'success':
                if response_data['Value']:
                    print("USER DATA UPLODED Secessfully")
                    User_data = response_data['Value']
                else:
                    print("Faild To Upload USER Data")
                    return "Faild To Upload USER Data"
            else:
                print("There is Error FOUND")
                return "There is Error FOUND"
    else:
        print("API Error")

    if User_data:
        answer = tk.messagebox.askquestion("Question", "User Created Online Secccesfully. for fast performance better to download datas. Do you what to download user data?", parent=parent)
        if answer == 'yes':
            User_data = Set_User(None, ['User_id', 'User_fname', 'User_Lname', 'User_name', 'User_gender', 'User_country', 'User_phone_num', 'User_email', 'User_address', 'User_home_no', 'User_id_pp_num', 'User_password', 'User_type', 'User_about', 'User_shop', 'User_work_shop', 'User_likes', 'User_following_shop', 'User_favoraite_items', 'User_rate', 'User_access', 'User_pimg', 'User_following_shop'], [User_data['User_id'], User_data['User_fname'], User_data['User_Lname'], User_data['User_name'], User_data['User_gender'], User_data['User_country'], User_data['User_phone_num'], User_data['User_email'], User_data['User_address'], User_data['User_home_no'], User_data['User_id_pp_num'], User_data['User_password'], User_data['User_type'], User_data['User_about'], User_data['User_shop'], User_data['User_work_shop'], User_data['User_likes'], User_data['user_following_shop'], User_data['user_favoraite_items'], User_data['user_rate'], User_data['user_access'], User_data['user_pimg'], User_data['user_following_shop']], parent=parent)
    else:
        # Insert the new user into the database
        query = query.replace("`", "")
        cur.execute('INSERT INTO Users' + query, value)
        Id = cur.lastrowid
        # Commit the changes to the database
        conn.commit()
        cur.execute('SELECT * FROM Users WHERE Id=?', (Id,))
        row = cur.fetchone()
        if row:
            columns = [col[0] for col in cur.description]
            User_data = dict(zip(columns, row))
    return User_data

# this will add user data to system database user data mast be given dict list key : value
def Add_User_data_From_list(User_data):
    #print("Add_User_data_From_list User_data ", User_data)
    return Set_User(None, ['User_id', 'User_fname', 'User_Lname', 'User_name', 'User_gender', 'User_country', 'User_phone_num', 'User_email', 'User_address', 'User_home_no', 'User_id_pp_num', 'User_password', 'User_type', 'User_about', 'User_shop', 'User_work_shop', 'User_likes', 'User_following_shop', 'User_favoraite_items', 'User_rate', 'User_access', 'User_pimg', 'User_following_shop'], [User_data['User_id'], User_data['User_fname'], User_data['User_Lname'], User_data['User_name'], User_data['User_gender'], User_data['User_country'], User_data['User_phone_num'], User_data['User_email'], User_data['User_address'], User_data['User_home_no'], User_data['User_id_pp_num'], User_data['User_password'], User_data['User_type'], User_data['User_about'], User_data['User_shop'], User_data['User_work_shop'], User_data['User_likes'], User_data['User_following_shop'], User_data['User_favoraite_items'], User_data['User_rate'], User_data['User_access'], User_data['User_pimg'], User_data['User_following_shop']])


# this will get user shop data with its name and brand name the user must be connected to that shop
# FOR FACING ANY Shop, COSTUMER EVEN WORKER BASIC INFO
# AT LIST NAME AND Shop NAME IS RQUERDE
# shop_find_Arg = [ "Shop_id", "Shop_name", "Shop_brand_name" ]
def Update_User(Link, user, ARG, UserVALUE, find_Arg, find_Value):
    query = ""
    value = None
    fquery = ""
    fvalue = None
    
    User = None

    for a, arg in  enumerate(find_Arg):
        if len(find_Value) > a:
            fquery += " " + arg + "=?"
            if fvalue:
                fvalue = fvalue + (find_Value[a],)
            else:
                fvalue = (find_Value[a], )
            if a+1 < len(find_Arg):
                fquery += " AND"

    for a, arg in  enumerate(ARG):
        if len(UserVALUE) > a:
            query += " " + arg + "=?"
            if value:
                value = value + (UserVALUE[a],)
            else:
                value = (UserVALUE[a], )
            if a+1 < len(ARG):
                query += " AND"

    if Link and islinked(Link):
        url = Link
        entry = {'Do': "UPDATE USER", 'User': user, 'QUERYS': query, 'QUERYVALUES' : value,  'FIND_ARG': fquery, 'FIND_VALUE': fvalue}
        print("Update_User entry ", entry)
        response_data = Sand_API(url, entry)
        if response_data and not response_data == []:
            if response_data['status'] == 'success':
                if response_data['Value']:
                    print("User Updated Secessfuly", response_data['Value'])
                    return response_data['Value']
                else:
                    print("Faild To Update User Data")
                    User = None
            else:
                if response_data['Value']:
                    print("There is Error in Update User Data", response_data['Value'])
                    User = response_data['Value']
                else:
                    print("There is Error in Update User Data")
                    User = None
    else:
        print("API Error")

    print("user query ", query)
    print("user value ", value)
    if query != "" and User == None:
        # Update the user into the database                
        cur.execute('UPDATE Users SET ' + query + ' WHERE '+fquery, value + fvalue)
        # Commit the changes to the database
        conn.commit()
        cur.execute('SELECT * FROM Users WHERE '+fquery, fvalue)
        row = cur.fetchone()
        if row:
            columns = [col[0] for col in cur.description]
            User = dict(zip(columns, row))
    return User








# SHOP


# this function will add new Shop to system data base all data must be given
def Add_new_Shop(Shop_id, Shop_name, Shop_brand_name, Shop_oweners_id, Shop_type, Shop_location, Shop_email, Shop_contact, Shop_password, Shop_Page, Shop_rate, Shop_items, Shop_followers, Shop_workers, Shop_Payment_Tools, Shop_about, Shop_Security_Levels, Company_Started_Date, Shop_likes, Shop_rules, Shop_link, Shop_Settings, Shop_profile_img, Shop_banner_imgs, Shop_payment_info, Shop_isenabled, Shop_Slip_Settings, Shop_Expenses, Shop_Actions):
    Shop_id = "" # TODO MAKE SHOP ID SAME
    Shop_Security_Levels = "" # TODO USE THIS INFOS FOR ONLINE AND OFFLINE
    Shop_rules = ""
    Shop_Slip_Settings = ""
    Shop_Expenses = ""
    Shop_Actions = ""
    
    #make Shop id same
    if Shop_name == "" or Shop_brand_name == "":
       pass
    else:
        # Insert the new user into the database
        if Shop_id == "" or Shop_id == None:
            cur.execute('INSERT INTO Shops(Shop_name, Shop_brand_name, Shop_oweners_id, Shop_type, Shop_location, Shop_email, Shop_contact, Shop_password, Shop_Page, Shop_rate, Shop_items, Shop_followers, Shop_workers, Shop_Payment_Tools, Shop_about, Shop_Security_Levels, Company_Started_Date, Shop_likes, Shop_rules, Shop_link, Shop_Settings, Shop_profile_img, Shop_banner_imgs, Shop_payment_info, Shop_isenabled, Shop_Slip_Settings, Shop_Expenses, Shop_Actions) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (Shop_name, Shop_brand_name, Shop_oweners_id, Shop_type, Shop_location, Shop_email, Shop_contact, Shop_password, Shop_Page, Shop_rate, Shop_items, Shop_followers, Shop_workers, Shop_Payment_Tools, Shop_about, Shop_Security_Levels, Company_Started_Date, Shop_likes, Shop_rules, Shop_link, Shop_Settings, Shop_profile_img, Shop_banner_imgs, Shop_payment_info, Shop_isenabled, Shop_Slip_Settings, Shop_Expenses, Shop_Actions))
        else:
            cur.execute('INSERT INTO Shops(Shop_id, Shop_name, Shop_brand_name, Shop_oweners_id, Shop_type, Shop_location, Shop_email, Shop_contact, Shop_password, Shop_Page, Shop_rate, Shop_items, Shop_followers, Shop_workers, Shop_Payment_Tools, Shop_about, Shop_Security_Levels, Company_Started_Date, Shop_likes, Shop_rules, Shop_link, Shop_Settings, Shop_profile_img, Shop_banner_imgs, Shop_payment_info, Shop_isenabled, Shop_Slip_Settings, Shop_Expenses, Shop_Actions) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (Shop_id, Shop_name, Shop_brand_name, Shop_oweners_id, Shop_type, Shop_location, Shop_email, Shop_contact, Shop_password, Shop_Page, Shop_rate, Shop_items, Shop_followers, Shop_workers, Shop_Payment_Tools, Shop_about, Shop_Security_Levels, Company_Started_Date, Shop_likes, Shop_rules, Shop_link, Shop_Settings, Shop_profile_img, Shop_banner_imgs, Shop_payment_info, Shop_isenabled, Shop_Slip_Settings, Shop_Expenses, Shop_Actions))
        # Commit the changes to the database
        conn.commit()                 

'''item_id = int(self.Found_User_id_var)
print("item_id : " + str(item_id))
# UPDATE the new user into the database
#cur.execute('UPDATE Shops SET User_work_shop=?, User_Lname=?, User_name=?, User_gender=?, User_country=?, User_phone_num=?, User_email=?, User_address=?, User_home_no=?, User_id_pp_num=?, User_type=?, User_password=?, User_about=?, User_shop=?, User_work_shop=?, User_access=?, User_pimg=? WHERE Shop_id=?', (User_fname, User_Lname, User_name, User_gender, User_country, User_phone_num, User_email, User_address, User_home_no, User_id_pp_num, User_type, User_password0, User_about, User_shop, User_work_shop, User_access, User_pimg, item_id))
#self.Secc.config(text="UPDATE Secccesfully", fg="Green")
#self.clear_user_details_widget()

if self.User_data and new_id:
#json.loads(ITEM)
#ITEM = json.dumps(self.Selected_items)
uws = json.dumps([[new_id, str(User_fname), str(User_name), [10]]])
cur.execute('UPDATE USERS SET User_work_shop=? WHERE User_id=?', (uws, self.User_data[0]))
print("user work place and owner is added", uws)
# Commit the changes to the database
conn.commit()'''

# this will add Shop data to system database Shop data mast be given dict list key : value
def Add_Shop_data_From_list(Shop_data):    
    Add_new_Shop(Shop_data['Shop_Id'], Shop_data['Shop_name'], Shop_data['Shop_brand_name'], Shop_data['Shop_oweners_id'], Shop_data['shop_type'], Shop_data['Shop_location'], Shop_data['shop_email'], Shop_data['Shop_contact'], Shop_data['Shop_password'], Shop_data['Shop_Page'], Shop_data['Shop_rate'], Shop_data['Shop_items'], Shop_data['Shop_followers'], Shop_data['Shop_workers'], Shop_data['Shop_Payment_Tools'], Shop_data['Shop_about'], "Shop_data['Shop_Security_Levels']", Shop_data['Company_Started_Date'], Shop_data['Shop_likes'], "Shop_data['Shop_rules']", Shop_data['Shop_linke'], Shop_data['Shop_settings'], Shop_data['Shop_profile_img'], Shop_data['Shop_banner_imgs'], Shop_data['Shop_payment_info'], Shop_data['Shop_isenabled'], "Shop_data['Shop_Slip_Settings']", "Shop_data['Shop_Expenses']", "Shop_data['Shop_Actions']")
    
    
 











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

# Shop Get

# this will get user shop data with its name and brand name the user must be connected to that shop
# FOR FACING ANY Shop, COSTUMER EVEN WORKER BASIC INFO
# AT LIST NAME AND Shop NAME IS RQUERDE
# shop_find_Arg = [ "Shop_id", "Shop_name", "Shop_brand_name" ]
def Update_Shop(Link, user, ARG, ShopsVALUE, find_Arg, find_Value):
    query = ""
    value = None
    fquery = ""
    fvalue = None
    
    Shop = None

    for a, arg in  enumerate(find_Arg):
        if len(find_Value) > a:
            fquery += " " + arg + "=?"
            if fvalue:
                fvalue = fvalue + (find_Value[a],)
            else:
                fvalue = (find_Value[a], )
            if a+1 < len(find_Arg):
                fquery += " AND"

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
        entry = {'Do': "UPDATE SHOP", 'User': user, 'QUERYS': query, 'QUERYVALUES' : value,  'FIND_ARG': fquery, 'FIND_VALUE': fvalue}
        print("Update_Shop entry ", entry)
        response_data = Sand_API(url, entry)
        if response_data and not response_data == []:
            if response_data['status'] == 'success':
                if response_data['Value']:
                    print("SHop Updated Secessfuly", response_data['Value'])
                    return response_data['Value']
                else:
                    print("Faild To Update Shop Data")
                    Shop = None
            else:
                if response_data['Value']:
                    print("There is Error in Update Shop Data", response_data['Value'])
                    Shop = response_data['Value']
                else:
                    print("There is Error in Update Shop Data")
                    Shop = None
    else:
        print("API Error")

    print("shop query ", query)
    print("shop value ", value)
    if query != "" and Shop == None:
        # Update the shop into the database                
        cur.execute('UPDATE Shops SET ' + query + ' WHERE '+fquery, value + fvalue)
        # Commit the changes to the database
        conn.commit()
        cur.execute('SELECT * FROM Shops WHERE '+fquery, fvalue)
        row = cur.fetchone()
        if row:
            columns = [col[0] for col in cur.description]
            Shop = dict(zip(columns, row))
    return Shop


# GET USER WORK SHOPS FROM LOCAL DATABASE Or Online
def Get_all_User_work_shops_info(Link, user, User_work_shops):
    print("Link : " + str(Link))
    Shops = []
    if User_work_shops and user:
        for Shop in User_work_shops:
            print("Shop : " + str(Shop))
            s = Get_Shop(Link, user, ["Shop_id", "Shop_name", "Shop_brand_name"], [str(Shop[0]), str(Shop[1]), str(Shop[2])])

            if s:
                Shops.append(s[0])
                print("s : " + str(s))
                print("Shops : " + str(Shops))  
    return Shops



# setting up the database
def Set_Setting(user, ARG, VALUE):
    query = "("
    value = None
    setting_data = ""
    for a, arg in enumerate(ARG):
        if len(VALUE) > a:
            query += "`" + arg + "`, "
            if value:
                value = value + (VALUE[a],)
            else:
                value = (VALUE[a], )
            if arg == 'user_name':
                user_name = VALUE[a]
    if query != "(":    
        if query.endswith(", "):
            query = query[:-2]
        query += ") "
        query += "VALUES (" + ("?, " * len(ARG)).rstrip(", ") + ")"
    print("Set_Setting query ", query)
    

    if query != "":
        print("Set_Setting query ", query)
        print("Set_Setting value ", value)
        # Insert the new user into the database
        cur.execute('INSERT INTO setting ' + query, value)
        Id = cur.lastrowid
        # Commit the changes to the database
        conn.commit()
        cur.execute('SELECT * FROM setting WHERE Id=?', (Id,))
        row = cur.fetchone()
        if row:
            columns = [col[0] for col in cur.description]
            setting_data = dict(zip(columns, row))
            return setting_data
        
    return None