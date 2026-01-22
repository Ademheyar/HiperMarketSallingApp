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
conn = sqlite3.connect(db_path)
cur = conn.cursor()

conn.commit()

class Company_Info_Frame(tk.Frame):
    def __init__(self, parent, Canceal_callback, User_data, Shop_data):
        tk.Frame.__init__(self, parent)
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
        
        self.type_entry.grid(row=4, column=0, padx=5, pady=5, sticky=tk.W)
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
        cur.execute('SELECT * FROM Shops WHERE Shop_name=? AND Shop_brand_name=?',
                    (self.fname_entry.get(), self.name_entry.get()))
        Shops = cur.fetchall()
        if Shops:
            for shop in Shops:
               if shop[1] == self.fname_entry.get() and shop[2] == self.name_entry.get():
                  self.forget_password_label.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
                  self.Found_User_id_var = shop[0];
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
                      owner_id = int(self.User_data['User_id'])    
                      # Insert the new user into the database
                      User_likes = ""
                      User_following_shop = ""
                      User_favoraite_items = ""
                      User_rate = ""
                      '''
                      Shop_id INTEGER PRIMARY KEY AUTOINCREMENT,
                      Shop_online_id INTEGER,
                      Shop_name TEXT,
                      Shop_brand_name TEXT,
                      Shop_oweners_id TEXT,
                      Shop_type TEXT,
                      Shop_location TEXT,
                      Shop_email TEXT,
                      Shop_contact TEXT,
                      Shop_password TEXT,
                      Shop_Page TEXT,
                      Shop_rate TEXT,
                      Shop_items TEXT,
                      Shop_followers TEXT,
                      Shop_workers TEXT,
                      Shop_Payment_Tools TEXT,
                      Shop_about TEXT,
                      Shop_Security_Levels TEXT,
                      Company_Started_Date TEXT,
                      Shop_likes TEXT,
                      Shop_rules TEXT,
                      Shop_link TEXT,
                      Shop_Settings TEXT,
                      Shop_profile_img TEXT,
                      Shop_banner_imgs TEXT,
                      Shop_payment_info TEXT,
                      Shop_isenabled TEXT,
                      Shop_Slip_Settings TEXT,
                      Shop_Expenses TEXT,
                      Shop_Actions TEXT,

                      
                      Shop_Items_type TEXT,
                      Shop_country TEXT,
                      Shop_payment_r TEXT,
                      Shop_Access_levels TEXT'''
                      user_info = User_phone_num + User_country + User_address
                      cur.execute('INSERT INTO Shops(Shop_name, Shop_brand_name, Shop_type, Shop_email, Shop_location, Shop_password, Shop_about, Shop_profile_img, Shop_oweners_id) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)', (User_fname, User_name, User_type, User_email, user_info, User_password0, User_about, User_pimg, owner_id))
                      new_id = cur.lastrowid
                      print("new shop created ", new_id)
                      self.Secc.config(text="Created Secccesfully", fg="Green")
                      self.clear_user_details_widget()
                  else:
                      self.Secc.config(text="filde no owner", fg="red")
              else:
                  item_id = int(self.Found_User_id_var)
                  print("item_id : " + str(item_id))
                  # UPDATE the new user into the database
                  cur.execute('UPDATE Shops SET User_work_shop=?, User_Lname=?, User_name=?, User_gender=?, User_country=?, User_phone_num=?, User_email=?, User_address=?, User_home_no=?, User_id_pp_num=?, User_type=?, User_password=?, User_about=?, User_shop=?, User_work_shop=?, User_access=?, User_pimg=? WHERE Shop_id=?', (User_fname, User_Lname, User_name, User_gender, User_country, User_phone_num, User_email, User_address, User_home_no, User_id_pp_num, User_type, User_password0, User_about, User_shop, User_work_shop, User_access, User_pimg, item_id))
                  self.Secc.config(text="UPDATE Secccesfully", fg="Green")
                  self.clear_user_details_widget()
                  
              if self.User_data and new_id:
                  #json.loads(ITEM)
                  #ITEM = json.dumps(self.Selected_items)
                  uws = json.dumps([[new_id, str(User_fname), str(User_name), [10]]])
                  cur.execute('UPDATE USERS SET User_work_shop=? WHERE User_id=?', (uws, self.User_data['User_id']))
                  print("user work place and owner is added", uws)
              # Commit the changes to the database
              conn.commit()
              self.Secc.grid(row=18, column=0, padx=5, pady=5, sticky=tk.W)

