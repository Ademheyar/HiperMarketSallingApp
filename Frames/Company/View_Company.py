import tkinter as tk
from tkinter import ttk
import sqlite3

import json
# Connect to the database or create it if it does not exist

import os
import os, sys
current_dir = os.path.abspath(os.path.dirname(__file__))
MAIN_dir = os.path.join(os.path.join(current_dir, '..'), '..')
sys.path.append(MAIN_dir)

# from D.docediterform import DocEditForm
from D.printer import PrinterForm
from C.slipe import load_slip

data_dir = os.path.join(MAIN_dir, 'data')
db_path = os.path.join(data_dir, 'my_database.db')

from C.API.Set import *
from C.API.Get import *
from C.API.API import *

class Company_Info_Frame(tk.Frame):
    def __init__(self, parent, Canceal_callback, User_data, Shop_data):
        tk.Frame.__init__(self, parent)
        # 
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        self.Canceal_callback = Canceal_callback
        self.User_data = User_data
        self.Shop_data = Shop_data

        self.User_Info_Frame = tk.Frame(self, bg="gray", height=screen_height, width=screen_width)
        self.User_Info_Frame.pack()
        
        self.details_frame = tk.Frame(self.User_Info_Frame, height=screen_height, width=screen_width)
        self.details_frame.place(relx=0.5, rely=0.5, anchor="center")

         # Create the widgets for the user details
        self.f_and_lname_label = tk.Label(self.details_frame, text='Company Name :')
        self.fname_entry = tk.Entry(self.details_frame)
        self.name_label = tk.Label(self.details_frame, text='Company Brand Name :')
        self.name_entry = tk.Entry(self.details_frame)
        
        self.main_name = ""
        self.fname_entry.bind('<KeyRelease>', self.on_name_entry)
        self.name_entry.bind('<KeyRelease>', self.on_name_entry)

        
        self.password_num0_label = tk.Label(self.details_frame, text='Password :')
        self.password_num0_entry = tk.Entry(self.details_frame, show="*")
        
        self.password_num1_label = tk.Label(self.details_frame, text='Confirm Password :')
        self.password_num1_entry = tk.Entry(self.details_frame, show="*")
                
        self.forget_password_label = tk.Label(self.details_frame, text="Company Found Did You Forgot Password?", fg="red", cursor="hand2")
        self.forget_password_label.bind("<Button-1>", self.forget_password_fuc)
        self.Found_User_id_var = tk.StringVar()
        
        self.show_password_var = tk.IntVar()
        self.show_password_checkbutton = tk.Checkbutton(self.details_frame, text='Show Passwords', variable=self.show_password_var)
        self.show_password_checkbutton.bind("<Button-1>", self.show_password_fuc)
        
        self.type_label = tk.Label(self.details_frame, text='Type :')
        self.type_entry = tk.Entry(self.details_frame)
        
        self.cuntry_label = tk.Label(self.details_frame, text='Cuntry :')
        self.cuntry_entry = tk.Entry(self.details_frame)
        self.phone_num_label = tk.Label(self.details_frame, text='Phone No :')
        self.phone_num_entry = tk.Entry(self.details_frame)
        self.email_label = tk.Label(self.details_frame, text='Email :')
        self.email_entry = tk.Entry(self.details_frame)
        self.addres_label = tk.Label(self.details_frame, text='Adress :')
        self.addres_entry = tk.Entry(self.details_frame)
        self.about_label = tk.Label(self.details_frame, text='About :')
        self.about_entry = tk.Entry(self.details_frame)
        
        self.pimg_label = tk.Label(self.details_frame, text='Image :')
        self.pimg_entry = tk.Entry(self.details_frame)

        self.Secc = tk.Label(self.details_frame)
        self.add_button = tk.Button(self.details_frame, text='Create', command=self.add_user)
        self.cancle_button = tk.Button(self.details_frame, text='Cancle', command=self.Canceal_callback)


        self.f_and_lname_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.fname_entry.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)
        self.name_label.grid(row=0, column=2, padx=5, pady=5, sticky=tk.W)
        self.name_entry.grid(row=0, column=3, padx=5, pady=5, sticky=tk.W)
        
        self.password_num0_label.grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        self.password_num0_entry.grid(row=2, column=1, padx=5, pady=5, sticky=tk.W)
        self.password_num1_label.grid(row=2, column=2, padx=5, pady=5, sticky=tk.W)
        self.password_num1_entry.grid(row=2, column=3, padx=5, pady=5, sticky=tk.W)
        self.show_password_checkbutton.grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)
        
        self.type_label.grid(row=4, column=0, padx=5, pady=5, sticky=tk.W)
        self.type_entry.grid(row=4, column=1, padx=5, pady=5, sticky=tk.W)
        self.cuntry_label.grid(row=5, column=0, padx=5, pady=5, sticky=tk.W)
        self.cuntry_entry.grid(row=5, column=1, padx=5, pady=5, sticky=tk.W)
        self.phone_num_label.grid(row=6, column=0, padx=5, pady=5, sticky=tk.W)
        self.phone_num_entry.grid(row=6, column=1, padx=5, pady=5, sticky=tk.W)
        self.email_label.grid(row=7, column=0, padx=5, pady=5, sticky=tk.W)
        self.email_entry.grid(row=7, column=1, padx=5, pady=5, sticky=tk.W)
        self.addres_label.grid(row=4, column=2, padx=5, pady=5, sticky=tk.W)
        self.addres_entry.grid(row=4, column=3, padx=5, pady=5, sticky=tk.W)
        self.about_label.grid(row=5, column=2, padx=5, pady=5, sticky=tk.W)
        self.about_entry.grid(row=5, column=3, padx=5, pady=5, sticky=tk.W)
        self.pimg_label.grid(row=6, column=2, padx=5, pady=5, sticky=tk.W)
        self.pimg_entry.grid(row=6, column=3, padx=5, pady=5, sticky=tk.W)

        if self.Shop_data:
           self.add_button.config(text="Update")
        else:
           self.add_button.config(text="Create")
           
        self.add_button.grid(row=17, column=0, padx=5, pady=5, sticky=tk.W)
        self.cancle_button.grid(row=17, column=1, padx=5, pady=5, sticky=tk.W)
        
    def forget_password_fuc(self, event):
        self.master.show_frame("Company_Forget_Info_Frame")
        pass
      
    def show_password_fuc(self, event):
        if self.show_password_var:
           self.password_num0_entry.config(show="")
           self.password_num1_entry.config(show="")
        else:
           self.password_num0_entry.config(show="*")
           self.password_num1_entry.config(show="*")
    
    def on_name_entry(self, event):
        shops = fetch_as_dict_list('SELECT * FROM Shops WHERE Shop_name=? AND Shop_brand_name=?', (self.fname_entry.get(), self.name_entry.get()))
        if shops:
            for shop in shops:
               if shop['Shop_name'] == self.fname_entry.get() and shop['Shop_brand_name'] == self.name_entry.get():
                  self.forget_password_label.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
                  self.Found_User_id_var = shop['Shop_Id'];
                  self.add_button.config(text="Update")
                  return
        else:
            self.forget_password_label.grid_remove()
            self.add_button.config(text="Create")


    def clear_user_details_widget(self):
        
        self.fname_entry.delete(0, "end")
        self.name_entry.delete(0, "end")
        self.cuntry_entry.delete(0, "end")
        self.phone_num_entry.delete(0, "end")
        self.email_entry.delete(0, "end")
        self.addres_entry.delete(0, "end")
        self.type_entry.delete(0, "end")
        self.password_num0_entry.delete(0, "end")
        self.password_num1_entry.delete(0, "end")
        self.about_entry.delete(0, "end")
        self.pimg_entry.delete(0, "end")

    # Define the function for adding a new user
    def add_user(self):
        # Get the values from the user details widgets
        User_fname = self.fname_entry.get()
        User_name = self.name_entry.get()
        User_country = self.cuntry_entry.get()
        User_phone_num = self.phone_num_entry.get()
        User_email = self.email_entry.get()
        User_address = self.addres_entry.get()
        User_type = self.type_entry.get()
        
        User_password0 = self.password_num0_entry.get()
        User_password1 = self.password_num1_entry.get()
        
        User_about = self.about_entry.get()
        User_pimg =  self.pimg_entry.get()
        if User_fname == "" or User_name == "" or User_password0 == "" or User_password1 == "":
           pass
        else:
            if User_password0 == User_password1:
                new_id = None
                if self.add_button.cget("text") == "Create":
                    if self.User_data:
                        print("new shop owner_id self.User_data[0] =  ", self.User_data)
                        owner_id = 0
                        owner_Userid = 0
                        if 'User_id' in self.User_data and self.User_data['User_id']:
                            owner_Userid = int(self.User_data['User_id'])
                        else:
                            owner_id = int(self.User_data['Id'])   
                        # Insert the new user into the database
                        User_likes = ""
                        User_following_shop = ""
                        User_favoraite_items = ""
                        User_rate = ""

                        user_info = User_phone_num + User_country + User_address
                        newShops = Set_Shop(None, ['Shop_name', 'Shop_brand_name', 'Shop_type', 'Shop_email', 'Shop_location', 'Shop_password', 'Shop_about', 'Shop_profile_img', 'Shop_oweners_id'], [User_fname, User_name, User_type, User_email, user_info, User_password0, User_about, User_pimg, owner_id])
                        print("newshop : ", newShops)
                        new_id = newShops['Shop_Id'] if newShops else None
                        print("company_name : ", newShops['Shop_name'])
                        print("company_brandname : ", newShops['Shop_brand_name'])
                        print("Shop_workers : ", newShops['Shop_workers'])

                        Shop_workers = []
                        if newShops and 'Shop_workers' in newShops and newShops['Shop_workers'] and not newShops['Shop_workers'] == 'None':
                            Shop_workers = json.loads(newShops['Shop_workers'])
                        found_worker_inshop = 0
                        for sw, Shop_worker in enumerate(Shop_workers):
                            if Shop_worker[0] == self.User_data['User_id']:
                                found_worker_inshop = 1
                                Shop_workers[sw] = [self.User_data['User_id'], self.User_data['User_fname'] + " "+ self.User_data['User_Lname'], self.User_data['User_name'], "WORKER", newShops['Shop_name'], newShops['Shop_brand_name'], [10]]
                        # e.g [2, 'Abdul Kedir', 'AK Abdul', 'OWNER', 'BELLEMA FASHION', 'ADOT', '10']        
                        # e.g [User Id, 'User Full Name', 'User Name', 'OWNER', 'Shop Name', 'Shop Brand', User permission in shop As (SHOP ASKED -2, USER ASKED -1, DISABLED 0, CUSTUMER 1, WORKER > 1 < 10, OWNER 10)]
                        if found_worker_inshop == 0:
                            print("self.User_data : ", self.User_data)
                            Shop_workers.append([self.User_data['User_id'], self.User_data['User_fname'] + " "+ self.User_data['User_Lname'], self.User_data['User_name'], "WORKER", newShops['Shop_name'], newShops['Shop_brand_name'], [10]])
                            print("Adding worker to shop workers list ", Shop_workers)
                            # Update the shop workers in the database
                            jsonShop_workers = json.dumps(Shop_workers)
                            if newShops['Shop_Id']:
                                newShops = Update_Shop(None, self.User_data, ['Shop_workers'], [jsonShop_workers], ['Shop_Id'], [newShops['Shop_Id']])
                            else:
                                newShops = Update_Shop(None, self.User_data, ['Shop_workers'], [jsonShop_workers], ['Id'], [newShops['Id']])
                            
                            if newShops:
                                print("Shop workers Updated Secessfuly", newShops)
                                if isinstance(newShops, list):
                                    newShops = newShops[0]

                        # Now update the User_work_shop field in Users table
                        User_work_shops = []
                        if self.User_data and not self.User_data['User_work_shop'] == None and not self.User_data['User_work_shop'] == 'None':                            
                            print("self.User_data['User_work_shop'] ", self.User_data['User_work_shop'])
                            try:
                                User_work_shops = json.loads(self.User_data['User_work_shop'])
                            except:
                                try:
                                    User_work_shops = json.loads(self.User_data['User_work_shop'])
                                except:
                                    print("user_work_shop json, load_list can not read it")
                                    pass  

                        found_shop_inworkes = 0
                        for uws, User_work_shop in enumerate(User_work_shops):
                            if User_work_shop[0] == newShops['Shop_Id']:
                                found_shop_inworkes = 1
                                User_work_shops[uws] = [newShops['Shop_Id'], newShops['Shop_name'], newShops['Shop_brand_name'], [10]]
                        # e.g [id, 'Shop Name', 'Shop Brand', User permission in shop As (SHOP ASKED -2, USER ASKED -1, DISABLED 0, CUSTUMER 1, WORKER > 1 < 10, OWNER 10)]

                        if found_shop_inworkes == 0:
                            print("Adding shop to user work shops list ", User_work_shops)
                            User_work_shops.append([newShops['Shop_Id'], newShops['Shop_name'], newShops['Shop_brand_name'], [10]])
                            # Update the Users table in the database
                            print("Updating user work shops list ", User_work_shops)
                            if self.User_data['User_id']:
                                User = Update_User(None, self.User_data, ['User_work_shop'], [json.dumps(User_work_shops)], ['User_id'], [self.User_data['User_id']])
                            else:
                                User = Update_User(None, self.User_data, ['User_work_shop'], [json.dumps(User_work_shops)], ['Id'], [self.User_data['Id']])
                            print("User : ", User)
                            self.User_data['User_work_shop'] = json.dumps(User_work_shops)
                            
                        print("new shop created ", new_id)
                        self.Secc.config(text="Created Secccesfully", fg="Green")
                        self.clear_user_details_widget()
                        self.Canceal_callback()
                    else:
                        self.Secc.config(text="filde no owner", fg="red")
                else:
                    item_id = int(self.Found_User_id_var)
                    print("item_id : " + str(item_id))
                    # UPDATE the new user into the database
                    Update_table_database('UPDATE Shops SET User_work_shop=?, User_Lname=?, User_name=?, User_gender=?, User_country=?, User_phone_num=?, User_email=?, User_address=?, User_home_no=?, User_id_pp_num=?, User_type=?, User_password=?, User_about=?, User_shop=?, User_work_shop=?, User_access=?, User_pimg=? WHERE Shop_id=?', (User_fname, User_Lname, User_name, User_gender, User_country, User_phone_num, User_email, User_address, User_home_no, User_id_pp_num, User_type, User_password0, User_about, User_shop, User_work_shop, User_access, User_pimg, item_id))
                    self.Secc.config(text="UPDATE Secccesfully", fg="Green")
                    self.clear_user_details_widget()
                  
                if self.User_data and new_id:
                    #json.loads(ITEM)
                    #ITEM = json.dumps(self.Selected_items)
                    uws = json.dumps([[new_id, str(User_fname), str(User_name), [10]]])
                    Update_table_database('UPDATE USERS SET User_work_shop=? WHERE User_id=?', (uws, self.User_data['User_id']))
                    print("user work place and owner is added", uws)
                self.Secc.grid(row=18, column=0, padx=5, pady=5, sticky=tk.W)

