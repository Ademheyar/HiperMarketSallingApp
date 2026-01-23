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
        if not response_data == []:
            if response_data['status'] == 'success':
                if response_data['Value']:
                    print("SHOP FOUND", response_data['Value'])
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
    Shops = fetch_as_dict_list("SELECT * FROM Shops WHERE" + query, value)
    if Shops:
        return Shops


# GET USER WORK SHOPS FROM LOCAL DATABASE Or Online
def Get_all_User_work_shops_info(Link, user, User_work_shops):
    Shops = []
    if User_work_shops and user:
        for Shop in User_work_shops:
            s = Get_Shop(Link, user, ["Shop_id", "Shop_name", "Shop_brand_name"]
            [str(Shop[0]), str(Shop[1]), str(Shop[2])])

            if s:
                Shops.append(s[0])
                #print("s : " + str(s))
                #print("Shops : " + str(Shops))  
    return Shops




class UploadingForm(tk.Toplevel):
    def __init__(self, master, user, Shops):
        super().__init__(master)
        self.Shops = Shops
        
        self.master = master
        self.user = user

        self.found_linkes = []
        
        self.title("Uploading Form")
        self.name_var = tk.StringVar()
        self.address_var = tk.StringVar()
        self.id_num_var = tk.StringVar()
        self.phone_num_var = tk.StringVar()
        self.email_var = tk.StringVar()
        self.type_var = tk.StringVar()
        self.password_var = tk.StringVar()
        self.access_var = tk.StringVar()

        self.type_var.set("Costumer")
        Date_and_time_label = tk.Label(self, text="Date : \n Time : \n", font=("Arial", 14))
        Date_and_time_label.grid(row=0, column=0, padx=10, pady=10)
        self.Top_info_label = tk.Label(self, text="No Connection Yat!", font=("Arial", 14))
        self.Top_info_label.grid(row=1, column=0, padx=10, pady=10)

        self.Shops_Names = [shop['Shop_name'] for shop in self.Shops]                            
        self.selected = tk.StringVar()
        self.User_Shopes_Combobox = ttk.Combobox(self, textvariable=self.selected, values=self.Shops_Names, width=10)
        self.User_Shopes_Combobox.grid(row=2, column=0, padx=10, pady=10)
        
        self.User_Shopes_Combobox.current(0)

        self.Refrash_button = tk.Button(self, text="Refrash", font=("Arial", 12), command=self.Refrash)
        self.Refrash_button.grid(row=3, column=0, sticky="nsew")

        self.RefrashUpload_button = tk.Button(self, text="Refrash/Upload", font=("Arial", 12), command=self.Do_All)
        self.RefrashUpload_button.grid(row=3, column=1, sticky="nsew")

        
        self.Notebook = ttk.Notebook(self)
        self.Notebook.grid(row=4, column=0, padx=10, pady=10)
        # Create the frame for the Shop Info
        self.Connections_frame = tk.Frame(self.Notebook)
        self.Connections_frame.pack()
        
        self.Notebook.add(self.Connections_frame, text="Connections")
        

        self.found_linke_list_box = ttk.Treeview(self.Connections_frame)
        self.found_linke_list_box.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
        #self.found_linke_list_box.bind('<<TreeviewSelect>>', self.USER_SECURITY_on_select)
        self.found_linke_list_box['columns'] = ("Connection", "Shop Name", "Links")
        self.found_linke_list_box.heading("#0", text="Connection")
        self.found_linke_list_box.heading("#1", text="Shop Name")
        self.found_linke_list_box.heading("#2", text="Links")

        # Create the frame for the Shop Info
        self.Shop_Upload_frame = tk.Frame(self.Notebook)
        self.Shop_Upload_frame.pack()
        self.Notebook.add(self.Shop_Upload_frame, text="Upload ")

        self.UploadAll_button = tk.Button(self.Shop_Upload_frame, text="Upload All", font=("Arial", 12), command=self.Upload)
        self.UploadAll_button.grid(row=0, column=0, sticky="nsew")
        
        self.Uploadproductes_button = tk.Button(self.Shop_Upload_frame, text="Upload productes", font=("Arial", 12), command=self.Upload_productes)
        self.Uploadproductes_button.grid(row=0, column=1, sticky="nsew")
        
        self.UploadActivetis_button = tk.Button(self.Shop_Upload_frame, text="Upload Activetis", font=("Arial", 12), command=self.Upload_Activetis)
        self.UploadActivetis_button.grid(row=0, column=2, sticky="nsew")
        
        self.Upload_productesinfo_label = tk.Label(self.Shop_Upload_frame, text="PRODUCTE UPLODED : 0\n PRODUCTE Filed TO UPLODE : 0\n", font=("Arial", 14))
        self.Upload_productesinfo_label.grid(row=1, column=0, padx=10, pady=10)
        
        self.Upload_Activetisinfo_label  = tk.Label(self.Shop_Upload_frame, text="ACTIVETIS UPLODED : 0\n ACTIVETIS Filed TO UPLODE : 0\n", font=("Arial", 14))
        self.Upload_Activetisinfo_label.grid(row=2, column=0, padx=10, pady=10)
        
        # Create the frame for the Shop Info
        self.Shop_Upgrade_frame = tk.Frame(self.Notebook)
        self.Shop_Upgrade_frame.pack()
        self.Notebook.add(self.Shop_Upgrade_frame, text="Upgrade ")

        self.UpgradeAll_button = tk.Button(self.Shop_Upgrade_frame, text="Upgrade All", font=("Arial", 12), command=self.Upload)
        self.UpgradeAll_button.grid(row=0, column=0, sticky="nsew")
        
        self.Upgradeproductes_button = tk.Button(self.Shop_Upgrade_frame, text="Upgrade productes", font=("Arial", 12), command=self.Upload)
        self.Upgradeproductes_button.grid(row=0, column=1, sticky="nsew")
        
        self.UpgradeActivetis_button = tk.Button(self.Shop_Upgrade_frame, text="Upgrade Activetis", font=("Arial", 12), command=self.Upload)
        self.UpgradeActivetis_button.grid(row=0, column=2, sticky="nsew")
        
        
        self.selected.trace('w', self.update_info)
        
        a = Chacke_Security(self, self.user, 7)
        #if a:
            #self.update()
        self.Refrash();
    
    def update_Upload_info(self):
        Total_upload_items = 0
        cursor.execute("SELECT * FROM upload_doc")
        b = cursor.fetchall()
        Total_upload_Activetis = len(b)
        Total_upload = Total_upload_Activetis
        for where_info in self.found_linkes:
            if self.User_Shopes_Combobox.get() == where_info['shop']['Shop_name'] or self.User_Shopes_Combobox.get() == "":
                # Fetch data from the database
                Total_upload_items += len(where_info['Product_to_upload'])
                Total_upload += Total_upload_items
        self.Notebook.tab(1, text="Upload "+str(Total_upload))
        self.UploadAll_button.config(text="Upload All "+str(Total_upload))
        self.Uploadproductes_button.config(text="Upload productes "+str(Total_upload_items))
        self.UploadActivetis_button.config(text="Upload Activetis "+str(Total_upload_Activetis))
    
    def update_Upgrade_info(self):
        Total_Upgrade = 0
        Total_Upgrade_Activetis = 0
        item_toupgraded = []
        for where_info in self.found_linkes:
            if self.User_Shopes_Combobox.get() == where_info['shop']['Shop_name'] or self.User_Shopes_Combobox.get() == "":
                shop = where_info['shop'];
                found_shop_items = json.loads(shop['Shop_items'])
                if found_shop_items:
                    for item in found_shop_items:
                        value = fetch_as_dict_list(cur, 'SELECT * FROM product WHERE id=?', (str(item[0]),))
                        if not value or len(value) == 0:
                            item_toupgraded.append(item)
                Total_Upgrade_Activetis += len(where_info['Product_to_upgrade'])
                Total_Upgrade += Total_Upgrade_Activetis
        Total_Upgrade += len(item_toupgraded)
        self.Notebook.tab(2, text="Upgrade "+str(Total_Upgrade))
        self.UpgradeAll_button.config(text="Upgrade All "+str(Total_Upgrade))
        self.Upgradeproductes_button.config(text="Upgrade productes "+str(len(item_toupgraded)))
        self.UpgradeActivetis_button.config(text="Upgrade Activetis "+str(Total_Upgrade_Activetis))
            
    def update_info(self, *args):
        if len(self.found_linkes) == 0:
            self.Top_info_label.config(text="There is No Connection Found.")
        else:
            total = 0
            for where_info in self.found_linkes:
                if self.User_Shopes_Combobox.get() == where_info['shop']['Shop_name'] or self.User_Shopes_Combobox.get() == "":
                    total+=1
            self.Top_info_label.config(text=str(total)+ " Connection Found.")
        self.update_Upload_info()
        self.update_Upgrade_info()


    def Upload_productes(self):
        found = 0
        filde = 0
        for where_info in self.found_linkes:
            if self.User_Shopes_Combobox.get() == where_info['shop']['Shop_name'] or self.User_Shopes_Combobox.get() == "":
                # Fetch data from the database
                url = where_info['shop']['Shop_link']
                isuploadproduct = 0
                if len(where_info['Product_to_upload']) > 0:
                    for Prod in where_info['Product_to_upload']:
                        value = fetch_as_dict_list(cursor, 'SELECT * FROM product WHERE id=?', (str(Prod[0]),))
                        if value and not len(value) == 0:
                            entry = {
                                'On': "Upload",
                                'shop': where_info['shop'],
                                'Product': value[0],
                                'isuploadproduct': 1
                            }
                            #print("\n\nentry : " + str(entry))
                            #print("\n\nentry : " + str(entry['item']))
                            response = 0
                            try:
                                print('senting entry.')
                                # Send the data to the API
                                response = requests.post(url, json=entry)
                            except requests.exceptions.RequestException as e:
                                print('Failed to send data:', e)                    
                                filde += 1
                                self.Upload_productesinfo_label.config(text="PRODUCTE UPLODED : "+str(found)+"\nPRODUCTE Filed TO UPLODE : "+str(filde)+"\n")
                    
                            if response and response.status_code == 200:
                                print('Data sent successfully.', response)
                                response_data = 0
                                try:
                                    response_data = response.json()
                                except requests.exceptions.RequestException as e:
                                    print('Failed to read data:', e)                    
                                    filde += 1
                                    self.Upload_productesinfo_label.config(text="PRODUCTE UPLODED : "+str(found)+"\nPRODUCTE Filed TO UPLODE : "+str(filde)+"\n")
                        
                                if response_data and response_data['status'] == 'success':
                                    print('Saved data:', response_data['message'])
                                    #new_row = response_data['row']
                                    found += 1
                                    self.Upload_productesinfo_label.config(text="PRODUCTE UPLODED : "+str(found)+"\nPRODUCTE Filed TO UPLODE : "+str(filde)+"\n")
                                    self.Refrash();
                                elif response_data:
                                    print('Failed to save data:', response_data['message'])
                                    filde += 1
                                    self.Upload_productesinfo_label.config(text="PRODUCTE UPLODED : "+str(found)+"\nPRODUCTE Filed TO UPLODE : "+str(filde)+"\n")
                                else:
                                    self.Upload_productesinfo_label.config(text="PRODUCTE UPLODED : "+str(found)+"\nPRODUCTE Filed TO UPLODE : "+str(filde)+"\n")
                            else:
                                print('Failed to retrieve data from the website.')
                                filde += 1
                                self.Upload_productesinfo_label.config(text="PRODUCTE UPLODED : "+str(found)+"\nPRODUCTE Filed TO UPLODE : "+str(filde)+"\n")
            
    def Upload_Activetis(self):
        found = 0
        filde = 0
        for where_info in self.found_linkes:
            if self.User_Shopes_Combobox.get() == where_info['shop']['Shop_name'] or self.User_Shopes_Combobox.get() == "":
                # Fetch data from the database
                url = where_info['shop']['Shop_link']
                b = fetch_as_dict_list(cursor, 'SELECT * FROM upload_doc', ())
                if len(b) > 0:
                    ind = -1
                    # Convert the fetched data to a list of dictionaries
                    for row in b:
                        ind += 1
                        entry = {
                            'On': "Upload",
                            'isuploadActivetis': 1,
                            'shop': where_info['shop'],
                            'doc': row
                        }
                        #print("row : " + str(row))
                        print("\n\nentry : " + str(entry))
                        #print("\n\nentry : " + str(entry['item']))
                        try:
                            # Send the data to the API
                            response = requests.post(url, json=entry)

                            if response.status_code == 200:
                                print('Data sent successfully.')
                                response_data = response.json()
                                if response_data['status'] == 'Get_Items_image':
                                    new_row = response_data['row']
                                    print('Get_Items_image:', str(new_row))
                                    new_row.replace(" ", "")
                                    items_path = new_row.split(",")
                                    for path in items_path:
                                        if path == "":
                                            break
                                        image_data = None
                                        with open(path, 'rb') as file:
                                            image_data = file.read()
                                        if not image_data == None:
                                            encoded_image_data = base64.b64encode(image_data).decode('utf-8')
                                            print('image_data:', str("encoded_image_data"))
                                            image_entry = {'type': 'Update_Image', 'image': encoded_image_data}
                                            image_response = requests.post(url, json=image_entry)
                                            try:
                                                image_response_data = image_response.json()
                                                if image_response.status_code == 200:
                                                    print('Saved data:', image_response_data['message'])
                                                    imahe_new_row = response_data['row']
                                                    print('Data sent successfully.')
                                                    print('Newly added row:', imahe_new_row)
                                                    found += 1
                                                    self.Upload_Activetisinfo_label.config(text="ACTIVETIS UPLODED : "+str(found)+"\n ACTIVETIS Filed TO UPLODE : "+str(filde)+"\n")
                                                else:
                                                    filde += 1
                                                    self.Upload_Activetisinfo_label.config(text="ACTIVETIS UPLODED : "+str(found)+"\n ACTIVETIS Filed TO UPLODE : "+str(filde)+"\n")
                                                    print('Failed to save image:', image_response_data['message'])
                                            except json.JSONDecodeError as e:
                                                filde += 1
                                                self.Upload_Activetisinfo_label.config(text="ACTIVETIS UPLODED : "+str(found)+"\n ACTIVETIS Filed TO UPLODE : "+str(filde)+"\n")
                                                print('Error: Response is not valid JSON.', str(e))
                                elif response_data['status'] == 'Error0':
                                    filde += 1
                                    print('Error0 data:', response_data['message'])
                                    self.Upload_Activetisinfo_label.config(text="ACTIVETIS UPLODED : "+str(found)+"\n ACTIVETIS Filed TO UPLODE : "+str(filde)+"\n")
                                elif response_data['status'] == 'success':
                                    print('Saved data:', response_data['message'])
                                    new_row = response_data['row']
                                    print('row:', new_row)
                                    try:
                                        cursor.execute("DELETE FROM `upload_doc` WHERE `id`=?", (row['id'],))                                        
                                        # Commit the changes to the database
                                        conn.commit()
                                    except conn.Error as err:
                                        print('erroror:', err)
                                    
                                    if cursor.rowcount < 0:
                                        filde += 1
                                        print('item not deleted :', conn)
                                    else:
                                        found += 1
                                        print('cursor.rowcount:', cursor.rowcount)
                                    self.Upload_Activetisinfo_label.config(text="ACTIVETIS UPLODED : "+str(found)+"\n ACTIVETIS Filed TO UPLODE : "+str(filde)+"\n")
                                    self.Refrash();
                                else:
                                    filde += 1
                                    self.Upload_Activetisinfo_label.config(text="ACTIVETIS UPLODED : "+str(found)+"\n ACTIVETIS Filed TO UPLODE : "+str(filde)+"\n")
                                    print('Failed to save data:', response_data['message'])
                                    break;
                            else:
                                filde += 1
                                self.Upload_Activetisinfo_label.config(text="ACTIVETIS UPLODED : "+str(found)+"\n ACTIVETIS Filed TO UPLODE : "+str(filde)+"\n")
                                print('Failed to retrieve data from the website.')
                        except requests.exceptions.RequestException as e:
                            filde += 1
                            self.Upload_Activetisinfo_label.config(text="ACTIVETIS UPLODED : "+str(found)+"\n ACTIVETIS Filed TO UPLODE : "+str(filde)+"\n")
                            print('Failed to send data:', e)
                        print('\n\n\n')

    def Upload(self):
        self.Upload_productes()
        self.Upload_Activetis()

    def Upgrade(self):
        pass

    
    def Refrash(self):
        self.found_linkes = []
        self.found_linke_list_box.delete(*self.found_linke_list_box.get_children())
        for shop in self.Shops:
            if self.User_Shopes_Combobox.get() == shop['Shop_name'] or self.User_Shopes_Combobox.get() == "":
                url = shop['Shop_link']
                entry = {'On': "Test", 'shop': shop, 'user' : self.user, 'ISNEW_USER' : 0 , 'ISNEW_SHOP' : 0 }
                while 1:
                    try:
                        # Send the data to the API
                        print('Data  ', entry)
                        print('Data send to ', url)
                        
                        response = requests.post(url, json=entry)

                        if response.status_code == 200:
                            print('Data sent successfully.')
                            print('Data sent response.', response)
                            response_data = []
                            try:
                                response_data = response.json()
                            except requests.exceptions.RequestException as e:
                                print('Failed to read data:', e)
                                self.found_linke_list_box.insert('', 'end', text="Failed Read Resived Data", values=(shop['Shop_name'], shop['Shop_link']))
                            print('Data sent response_data .', response_data)
                            if not response_data == []:
                                if response_data['status'] == 'success':
                                    self.found_linke_list_box.insert('', 'end', text="success", values=(shop['Shop_name'], shop['Shop_link']))
                                    self.found_linkes.append({'shop': shop, 'Product_to_upgrade': [], 'Product_to_upload': response_data['Product_to_upload']})
                                    self.update_info();
                                elif response_data['status'] == 'Erorr':
                                    if response_data['Erorr'] == 'NO USER FOUND':
                                        entry = {'On': "Test", 'shop': shop, 'user' : self.user, 'ISNEW_USER' : 1 , 'ISNEW_SHOP' : 1 }
                                        answer = tk.messagebox.askquestion("Question", "User Was Not Found Do you what to sand User Info For Register?")
                                        if answer == 'yes':
                                            continue
                                        else:
                                            self.found_linke_list_box.insert('', 'end', text="Erorr "+str(response_data['message']), values=(shop['Shop_name'], shop['Shop_link']))

                                            
                                    elif response_data['Erorr'] == 'NO SHOP FOUND':
                                        entry = {'On': "Test", 'shop': shop, 'user' : self.user, 'ISNEW_USER' : 0 , 'ISNEW_SHOP' : 1 }
                                        answer = tk.messagebox.askquestion("Question", "USERS SHOP WHERE NOT FOUND DO YOU WHANT TO SAND INFO FOR REGISTER?")
                                        if answer == 'yes':
                                            continue
                                        else:
                                            self.found_linke_list_box.insert('', 'end', text="Erorr "+str(response_data['message']), values=(shop['Shop_name'], shop['Shop_link']))
                                    
                                    elif response_data['Erorr'] == 'Try Agane':
                                        entry = {'On': "Test", 'shop': shop, 'user' : self.user, 'ISNEW_USER' : 0 , 'ISNEW_SHOP' : 0 }
                                        answer = tk.messagebox.askquestion("Question", str(response_data['message'])+ "?")
                                        if answer == 'yes':
                                            continue
                                        else:
                                            self.found_linke_list_box.insert('', 'end', text="Erorr "+str(response_data['message']), values=(shop['Shop_name'], shop['Shop_link']))
                                            
                                    elif response_data['Erorr'] == 'FILED REGISTERING SHOP':
                                        self.found_linke_list_box.insert('', 'end', text="FILED REGISTERING SHOP "+str(response_data['message']), values=(shop['Shop_name'], shop['Shop_link']))
                                else:
                                    print('Failed to save data:', response_data['message'])
                                    self.found_linke_list_box.insert('', 'end', text="Failed Reading Data", values=(shop['Shop_name'], shop['Shop_link']))
                                    break
                        else:
                            print('Failed to retrieve data from the website.')
                            self.found_linke_list_box.insert('', 'end', text="Failed To Fetch Data", values=(shop['Shop_name'], shop['Shop_link']))
                    except requests.exceptions.RequestException as e:
                        print('Failed to send data:', e)
                        self.found_linke_list_box.insert('', 'end', text="Failed Network Connection", values=(shop['Shop_name'], shop['Shop_link']))
                    break


    def Do_All(self):
        self.Refrash()
        self.Upload()
        self.Upgrade()
        
    def update(self):
        #'''
        # Fetch data from the database
        url = 'http://localhost/Adot/update-api-endpoint.php'
        cursor.execute("SELECT * FROM upload_doc")
        b = cursor.fetchall()
        if len(b) > 0:
            ind = -1
            # Convert the fetched data to a list of dictionaries
            for row in b:
                ind += 1
                entry = {
                    'id': row[0],
                    'doc_barcode': str(row[1]),
                    'extension_barcode': str(row[2]),
                    'user_id': str(row[3]),
                    'customer_id': str(row[4]),
                    'type': str(row[5]),
                    'item': str(row[6]),
                    'qty': str(row[7]),
                    'price': str(row[8]),
                    'discount': str(row[9]),
                    'tax': str(row[10]),
                    'payments': str(row[11]),
                    'doc_created_date': str(row[12]),
                    'doc_expire_date': str(row[13]),
                    'doc_updated_date': str(row[14])
                }
                #print("row : " + str(row))
                print("\n\nentry : " + str(entry))
                #print("\n\nentry : " + str(entry['item']))
                try:
                    # Send the data to the API
                    response = requests.post(url, json=entry)

                    if response.status_code == 200:
                        print('Data sent successfully.')
                        response_data = response.json()
                        if response_data['status'] == 'Get_Items_image':
                            new_row = response_data['row']
                            print('Get_Items_image:', str(new_row))
                            new_row.replace(" ", "")
                            items_path = new_row.split(",")
                            for path in items_path:
                                if path == "":
                                    break
                                image_data = None
                                with open(path, 'rb') as file:
                                    image_data = file.read()
                                if not image_data == None:
                                    encoded_image_data = base64.b64encode(image_data).decode('utf-8')
                                    print('image_data:', str("encoded_image_data"))
                                    image_entry = {'type': 'Update_Image', 'image': encoded_image_data}
                                    image_response = requests.post(url, json=image_entry)
                                    try:
                                        image_response_data = image_response.json()
                                        if image_response.status_code == 200:
                                            print('Saved data:', image_response_data['message'])
                                            imahe_new_row = response_data['row']
                                            print('Data sent successfully.')
                                            print('Newly added row:', imahe_new_row)
                                        else:
                                            print('Failed to save image:', image_response_data['message'])
                                    except json.JSONDecodeError as e:
                                        print('Error: Response is not valid JSON.', str(e))

                        elif response_data['status'] == 'success':
                            print('Saved data:', response_data['message'])
                            new_row = response_data['row']
                            print('row:', new_row)
                            if ind != len(b) -1:
                                cursor.execute("DELETE FROM upload_doc WHERE id=?", (row[0],))
                                
                                # Commit the changes to the database
                                conn.commit()
                                print('Newly added row:', new_row)
                            
                        else:
                            print('Failed to save data:', response_data['message'])
                            break;
                    else:
                        print('Failed to retrieve data from the website.')
                except requests.exceptions.RequestException as e:
                    print('Failed to send data:', e)
                print('\n\n\n')
            
        # set the position of the Payment Form window to center
        # TODO: list z report for current day and history z reports for pev days but in notbook 
        # TODO: TO Print dayly, weekly, monthly and yearly report as user whats
        # show the Payment Form window
        #'''
        pass

if __name__ == "__main__":
    root = tk.Tk()
    app = UploadingForm(root)
    root.mainloop()
