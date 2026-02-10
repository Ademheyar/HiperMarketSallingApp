import tkinter as tk
from tkinter import ttk
import sqlite3

# Connect to the database or create it if it does not exist

import os
import os, sys
current_dir = os.path.abspath(os.path.dirname(__file__))
MAIN_dir = os.path.join(os.path.join(current_dir, '..'), '..')
sys.path.append(MAIN_dir)

data_dir = os.path.join(MAIN_dir, 'data')
db_path = os.path.join(data_dir, 'my_database.db')
conn = sqlite3.connect(db_path)
cur = conn.cursor()

conn.commit()

#from D.docediterform import DocEditForm
from D.printer import PrinterForm
from C.slipe import load_slip
from C.API.Set import *


class User_Info_Frame(tk.Frame):
    def __init__(self, parent, Canceal_callback, User_data, link):
        tk.Frame.__init__(self, parent, bg="#0d47a1")
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        self.Canceal_callback = Canceal_callback
        self.User_data = User_data
        self.Link = link
        self.User_Info_Frame = tk.Frame(self, bg="#0d47a1", height=screen_height, width=screen_width)
        self.User_Info_Frame.pack()
        
        self.details_frame = tk.Frame(self.User_Info_Frame, bg="#1565c0", height=screen_height, width=screen_width)
        self.details_frame.place(relx=0.5, rely=0.5, anchor="center")

        # Create the widgets for the user details
        self.f_and_lname_label = tk.Label(self.details_frame, text='First and Last Name :', bg="#1565c0", fg="#ffffff")
        self.fname_entry = tk.Entry(self.details_frame, bg="#1976d2", fg="#ffffff")
        self.lname_entry = tk.Entry(self.details_frame, bg="#1976d2", fg="#ffffff")
        self.name_label = tk.Label(self.details_frame, text='User Name :', bg="#1565c0", fg="#ffffff")
        self.name_entry = tk.Entry(self.details_frame, bg="#1976d2", fg="#ffffff")
        
        self.main_name = ""
        self.fname_entry.bind('<KeyRelease>', self.on_name_entry)
        self.lname_entry.bind('<KeyRelease>', self.on_name_entry)
        self.name_entry.bind('<KeyRelease>', self.on_name_entry)
        
        self.forget_password_label = tk.Label(self.details_frame, text="User Found Did You Forgot Password?", fg="red", cursor="hand2", bg="#1565c0")
        self.forget_password_label.bind("<Button-1>", self.forget_password_fuc)
        self.Found_User_id_var = tk.StringVar()
        
        self.password_num0_label = tk.Label(self.details_frame, text='Password :', bg="#1565c0", fg="#ffffff")
        self.password_num0_entry = tk.Entry(self.details_frame, show="*", bg="#1976d2", fg="#ffffff")
        
        self.password_num1_label = tk.Label(self.details_frame, text='Confirm Password :', bg="#1565c0", fg="#ffffff")
        self.password_num1_entry = tk.Entry(self.details_frame, show="*", bg="#1976d2", fg="#ffffff")
        
        self.show_password_var = tk.IntVar()
        self.show_password_checkbutton = tk.Checkbutton(self.details_frame, text='Show Passwords', variable=self.show_password_var, bg="#1565c0", fg="#ffffff")
        self.show_password_checkbutton.bind("<Button-1>", self.show_password_fuc)
        
        self.gender_label = tk.Label(self.details_frame, text='Gender :', bg="#1565c0", fg="#ffffff")
        self.gender_entry = tk.Entry(self.details_frame, bg="#1976d2", fg="#ffffff")
        self.cuntry_label = tk.Label(self.details_frame, text='Cuntry :', bg="#1565c0", fg="#ffffff")
        self.cuntry_entry = tk.Entry(self.details_frame, bg="#1976d2", fg="#ffffff")
        self.phone_num_label = tk.Label(self.details_frame, text='Phone No :', bg="#1565c0", fg="#ffffff")
        self.phone_num_entry = tk.Entry(self.details_frame, bg="#1976d2", fg="#ffffff")
        self.email_label = tk.Label(self.details_frame, text='Email :', bg="#1565c0", fg="#ffffff")
        self.email_entry = tk.Entry(self.details_frame, bg="#1976d2", fg="#ffffff")
        self.addres_label = tk.Label(self.details_frame, text='Adress :', bg="#1565c0", fg="#ffffff")
        self.addres_entry = tk.Entry(self.details_frame, bg="#1976d2", fg="#ffffff")
        self.id_num_label = tk.Label(self.details_frame, text='Id No :', bg="#1565c0", fg="#ffffff")
        self.id_num_entry = tk.Entry(self.details_frame, bg="#1976d2", fg="#ffffff")
        self.home_no_label = tk.Label(self.details_frame, text='Home No :', bg="#1565c0", fg="#ffffff")
        self.home_no_entry = tk.Entry(self.details_frame, bg="#1976d2", fg="#ffffff")
        self.type_label = tk.Label(self.details_frame, text='Type :', bg="#1565c0", fg="#ffffff")
        self.type_entry = tk.Entry(self.details_frame, bg="#1976d2", fg="#ffffff")
        self.about_label = tk.Label(self.details_frame, text='About :', bg="#1565c0", fg="#ffffff")
        self.about_entry = tk.Entry(self.details_frame, bg="#1976d2", fg="#ffffff")
        
        self.pimg_label = tk.Label(self.details_frame, text='Image :', bg="#1565c0", fg="#ffffff")
        self.pimg_entry = tk.Entry(self.details_frame, bg="#1976d2", fg="#ffffff")

        self.shops_label = tk.Label(self.details_frame, text='Shop :', bg="#1565c0", fg="#ffffff")
        self.shops_entry = tk.Entry(self.details_frame, bg="#1976d2", fg="#ffffff")
        self.work_shop_label = tk.Label(self.details_frame, text='Work Shop :', bg="#1565c0", fg="#ffffff")
        self.work_shop_entry = tk.Entry(self.details_frame, bg="#1976d2", fg="#ffffff")
        self.acsess_label = tk.Label(self.details_frame, text='ACSSES :', bg="#1565c0", fg="#ffffff")
        self.acsess_entry = tk.Entry(self.details_frame, bg="#1976d2", fg="#ffffff")

        self.Secc = tk.Label(self.details_frame, bg="#1565c0", fg="#ffffff")
        self.add_button = tk.Button(self.details_frame, text='Create', command=self.add_user, bg="#1976d2", fg="#ffffff")
        self.cancle_button = tk.Button(self.details_frame, text='Cancle', command=self.canceal_callback, bg="#1976d2", fg="#ffffff")

        self.f_and_lname_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.fname_entry.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)
        self.lname_entry.grid(row=0, column=2, padx=5, pady=5, sticky=tk.W)
        self.name_label.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.name_entry.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)
        
        self.password_num0_label.grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        self.password_num0_entry.grid(row=2, column=1, padx=5, pady=5, sticky=tk.W)
        self.password_num1_label.grid(row=2, column=2, padx=5, pady=5, sticky=tk.W)
        self.password_num1_entry.grid(row=2, column=3, padx=5, pady=5, sticky=tk.W)
        self.show_password_checkbutton.grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)
        
        self.gender_label.grid(row=4, column=0, padx=5, pady=5, sticky=tk.W)
        self.gender_entry.grid(row=4, column=1, padx=5, pady=5, sticky=tk.W)
        self.cuntry_label.grid(row=5, column=0, padx=5, pady=5, sticky=tk.W)
        self.cuntry_entry.grid(row=5, column=1, padx=5, pady=5, sticky=tk.W)
        self.phone_num_label.grid(row=6, column=0, padx=5, pady=5, sticky=tk.W)
        self.phone_num_entry.grid(row=6, column=1, padx=5, pady=5, sticky=tk.W)
        self.email_label.grid(row=7, column=0, padx=5, pady=5, sticky=tk.W)
        self.email_entry.grid(row=7, column=1, padx=5, pady=5, sticky=tk.W)
        self.addres_label.grid(row=8, column=0, padx=5, pady=5, sticky=tk.W)
        self.addres_entry.grid(row=8, column=1, padx=5, pady=5, sticky=tk.W)
        self.id_num_label.grid(row=9, column=0, padx=5, pady=5, sticky=tk.W)
        self.id_num_entry.grid(row=9, column=1, padx=5, pady=5, sticky=tk.W) 
        self.home_no_label.grid(row=10, column=0, padx=5, pady=5, sticky=tk.W)
        self.home_no_entry.grid(row=10, column=1, padx=5, pady=5, sticky=tk.W)
        
        self.type_label.grid(row=3, column=2, padx=5, pady=5, sticky=tk.W)
        self.type_entry.grid(row=3, column=3, padx=5, pady=5, sticky=tk.W)
        self.about_label.grid(row=4, column=2, padx=5, pady=5, sticky=tk.W)
        self.about_entry.grid(row=4, column=3, padx=5, pady=5, sticky=tk.W)
        self.pimg_label.grid(row=5, column=2, padx=5, pady=5, sticky=tk.W)
        self.pimg_entry.grid(row=5, column=3, padx=5, pady=5, sticky=tk.W)

        if self.User_data:
           self.shops_label.grid(row=6, column=2, padx=5, pady=5, sticky=tk.W)
           self.shops_entry.grid(row=6, column=3, padx=5, pady=5, sticky=tk.W)
           self.work_shop_label.grid(row=7, column=2, padx=5, pady=5, sticky=tk.W)
           self.work_shop_entry.grid(row=7, column=3, padx=5, pady=5, sticky=tk.W)
           self.acsess_label.grid(row=8, column=2, padx=5, pady=5, sticky=tk.W)
           self.acsess_entry.grid(row=8, column=3, padx=5, pady=5, sticky=tk.W)
           self.add_button.config(text="Update")
        else:
           self.add_button.config(text="Create")

        # Fill fake test data for each entry widget
        self.fname_entry.insert(0, "John")
        self.lname_entry.insert(0, "Doe")
        self.name_entry.insert(0, "JD John")
        self.password_num0_entry.insert(0, "password123")
        self.password_num1_entry.insert(0, "password123")
        self.gender_entry.insert(0, "Male")
        self.cuntry_entry.insert(0, "USA")
        self.phone_num_entry.insert(0, "+1-555-1234")
        self.email_entry.insert(0, "john.doe@example.com")
        self.addres_entry.insert(0, "123 Main St")
        self.id_num_entry.insert(0, "ID123456")
        self.home_no_entry.insert(0, "Apt 5B")
        self.type_entry.insert(0, "Customer")
        self.about_entry.insert(0, "Test user account")
        self.pimg_entry.insert(0, "/path/to/image.jpg")
        self.shops_entry.insert(0, "Shop A")
        self.work_shop_entry.insert(0, "Workshop B")
        self.acsess_entry.insert(0, "Admin")
        self.add_button.grid(row=17, column=0, padx=5, pady=5, sticky=tk.W)
        self.cancle_button.grid(row=17, column=1, padx=5, pady=5, sticky=tk.W)
    def canceal_callback(self):
        self.Canceal_callback()
        self.destroy()

    def forget_password_fuc(self, event):
        self.master.show_frame("User_Forget_Info_Frame")
        pass
      
    def show_password_fuc(self, event):
        if self.show_password_var:
           self.password_num0_entry.config(show="")
           self.password_num1_entry.config(show="")
        else:
           self.password_num0_entry.config(show="*")
           self.password_num1_entry.config(show="*")
    
    def on_name_entry(self, event):
        if self.fname_entry.get() != "" and self.lname_entry.get() != "":
            if event.widget != self.name_entry and self.name_entry.get() != str(self.fname_entry.get()[0]+self.lname_entry.get()[0] + " " + self.fname_entry.get()):
               self.name_entry.delete(0, tk.END)
               self.name_entry.insert(0, self.fname_entry.get()[0]+self.lname_entry.get()[0] + " " + self.fname_entry.get())
        else:
            self.name_entry.delete(0, tk.END)
            
        cur.execute('SELECT * FROM Users WHERE (User_fname=? AND User_Lname=? AND User_name=?) OR User_name=?',
                    (self.fname_entry.get(), self.lname_entry.get(), self.name_entry.get(), self.name_entry.get()))
        users = cur.fetchall()
        if users:
            for user in users:
               print("on_name_entry\n"+str(user[1]))
               if user[1] == self.name_entry.get():
                  self.forget_password_label.grid(row=1, column=2, padx=5, pady=5, sticky=tk.W)
                  self.Found_User_id_var = user[0];
                  self.add_button.config(text="Update")
                  return
        else:
            self.forget_password_label.grid_remove()
            self.add_button.config(text="Create")


    def clear_user_details_widget(self):
        self.fname_entry.delete(0, "end")
        self.lname_entry.delete(0, "end")
        self.name_entry.delete(0, "end")
        self.gender_entry.delete(0, "end")
        self.cuntry_entry.delete(0, "end")
        self.phone_num_entry.delete(0, "end")
        self.email_entry.delete(0, "end")
        self.addres_entry.delete(0, "end")
        self.home_no_entry.delete(0, "end")
        self.id_num_entry.delete(0, "end")
        self.type_entry.delete(0, "end")
        self.password_num0_entry.delete(0, "end")
        self.password_num1_entry.delete(0, "end")
        self.about_entry.delete(0, "end")
        self.shops_entry.delete(0, "end")
        self.work_shop_entry.delete(0, "end")
        self.acsess_entry.delete(0, "end")
        self.pimg_entry.delete(0, "end")

    # Define the function for adding a new user
    def add_user(self):
        # Get the values from the user details widgets
        User_fname = self.fname_entry.get()
        User_Lname = self.lname_entry.get()
        User_name = self.name_entry.get()
        User_gender = self.gender_entry.get()
        User_country = self.cuntry_entry.get()
        User_phone_num = self.phone_num_entry.get()
        User_email = self.email_entry.get()
        User_address = self.addres_entry.get()
        User_home_no = self.home_no_entry.get()
        User_id_pp_num = self.id_num_entry.get()
        User_type = self.type_entry.get()
        
        User_password0 = self.password_num0_entry.get()
        User_password1 = self.password_num1_entry.get()
        
        User_about = self.about_entry.get()
        User_shop = self.shops_entry.get()
        User_work_shop = self.work_shop_entry.get()
        User_access = self.acsess_entry.get()
        User_pimg =  self.pimg_entry.get()
        if User_fname == "" or User_Lname == "" or User_name == "" or User_password0 == "" or User_password1 == "":
           pass
        else:
           if User_password0 == User_password1:
              if self.add_button.cget("text") == "Create":        
                  # Insert the new user into the database
                  User_likes = ""
                  User_following_shop = ""
                  User_favoraite_items = ""
                  User_rate = ""
                  user = Set_User(self.Link, ['User_fname', 'User_Lname', 'User_name', 'User_gender', 'User_country', 'User_phone_num', 'User_email', 'User_address', 'User_home_no', 'User_type', 'User_password', 'User_about', 'User_shop', 'User_work_shop', 'User_likes', 'User_following_shop', 'User_favoraite_items', 'User_rate', 'User_access', 'User_pimg'], [User_fname, User_Lname, User_name, User_gender, User_country, User_phone_num, User_email, User_address, User_home_no, User_type, User_password0, User_about, User_shop, User_work_shop, User_likes, User_following_shop, User_favoraite_items, User_rate, User_access, User_pimg])
                  if user:
                    if not 'Id' in user or user['Id'] == 0 or user['Id'] == None:
                        tk.Label(self.master.master.Error_list_frame, text="Online User Created Secccesfully", bg="#1565c0", fg="Green").pack(side=tk.TOP, fill=tk.X, expand=True)
                    elif 'Id' in user and user['Id'] != 0 and not user['Id'] == None and (user['User_id'] == 0 or user['User_id'] == None):
                        tk.Label(self.master.master.Error_list_frame, text="Offline User Created Secccesfully", bg="#1565c0", fg="Green").pack(side=tk.TOP, fill=tk.X, expand=True)
                    else:
                        tk.Label(self.master.master.Error_list_frame, text="User Created Secccesfully", bg="#1565c0", fg="Green").pack(side=tk.TOP, fill=tk.X, expand=True)
                    self.Canceal_callback()
                    self.destroy()
                  else:
                    self.Secc.config(text="Failed to Create User", fg="red")
              else:
                  item_id = int(self.Found_User_id_var)
                  print("item_id : " + str(item_id))
                  # UPDATE the new user into the database
                  cur.execute('UPDATE Users SET User_fname=?, User_Lname=?, User_name=?, User_gender=?, User_country=?, User_phone_num=?, User_email=?, User_address=?, User_home_no=?, User_id_pp_num=?, User_type=?, User_password=?, User_about=?, User_shop=?, User_work_shop=?, User_access=?, User_pimg=? WHERE User_id=?', (User_fname, User_Lname, User_name, User_gender, User_country, User_phone_num, User_email, User_address, User_home_no, User_id_pp_num, User_type, User_password0, User_about, User_shop, User_work_shop, User_access, User_pimg, item_id))
              
                  self.Secc.config(text="Updated Secccesfully", fg="Green")
              # Commit the changes to the database
              conn.commit()
              self.clear_user_details_widget()
           else:
               self.Secc.config(text="Sorry the password you put dont mauch", fg="red")
               
           self.Secc.grid(row=18, column=0, padx=5, pady=5, sticky=tk.W)
        

