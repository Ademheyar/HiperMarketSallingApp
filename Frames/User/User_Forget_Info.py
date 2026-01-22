import tkinter as tk
from tkinter import ttk
import sqlite3

# Connect to the database or create it if it does not exist

import os
import os, sys
current_dir = os.path.abspath(os.path.dirname(__file__))
MAIN_dir = os.path.join(os.path.join(current_dir, '..'), '..')
sys.path.append(MAIN_dir)

#from D.docediterform import DocEditForm
from D.printer import PrinterForm
from C.slipe import load_slip

data_dir = os.path.join(MAIN_dir, 'data')
db_path = os.path.join(data_dir, 'my_database.db')
conn = sqlite3.connect(db_path)
cur = conn.cursor()

conn.commit()

class User_Forget_Info_Frame(tk.Frame):
    def __init__(self, parent, Canceal_callback, User_data):
        tk.Frame.__init__(self, parent)
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        self.Canceal_callback = Canceal_callback
        self.User_data = User_data

        # Android-style dark blue color scheme
        bg_dark = "#0d47a1"      # Deep blue
        bg_light = "#1565c0"     # Darker blue
        accent_blue = "#1976d2"  # Medium blue
        text_light = "#ffffff"

        self.User_Info_Frame = tk.Frame(self, bg=bg_dark, height=screen_height, width=screen_width)
        self.User_Info_Frame.pack()
        
        self.details_frame = tk.Frame(self.User_Info_Frame, bg=bg_dark, height=screen_height, width=screen_width)
        self.details_frame.place(relx=0.5, rely=0.5, anchor="center")

        # Create the widgets for the user details
        tk.Label(self.details_frame,
             text="Hello! Please Fill Your Profile To Find Your Account.",
             bg=bg_dark, fg=text_light, font=("Arial", 12, "bold")
             ).grid(row=0, column=0, columnspan=4, padx=5, pady=10, sticky=tk.W)
             
        tk.Label(self.details_frame,
             text="This First Form Must be Filled.",
             bg=bg_dark, fg=accent_blue, font=("Arial", 10)
             ).grid(row=1, column=0, columnspan=4, padx=5, pady=5, sticky=tk.W)
        
        self.f_and_lname_label = tk.Label(self.details_frame, text='First and Last Name :', bg=bg_dark, fg=text_light)
        self.fname_entry = tk.Entry(self.details_frame, bg=bg_light, fg=text_light, insertbackground=text_light)
        self.lname_entry = tk.Entry(self.details_frame, bg=bg_light, fg=text_light, insertbackground=text_light)
        self.gender_label = tk.Label(self.details_frame, text='Gender :', bg=bg_dark, fg=text_light)
        self.gender_entry = tk.Entry(self.details_frame, bg=bg_light, fg=text_light, insertbackground=text_light)
        self.id_num_label = tk.Label(self.details_frame, text='Id No :', bg=bg_dark, fg=text_light)
        self.id_num_entry = tk.Entry(self.details_frame, bg=bg_light, fg=text_light, insertbackground=text_light)
        self.home_no_label = tk.Label(self.details_frame, text='Home No :', bg=bg_dark, fg=text_light)
        self.home_no_entry = tk.Entry(self.details_frame, bg=bg_light, fg=text_light, insertbackground=text_light)
        self.cuntry_label = tk.Label(self.details_frame, text='Country :', bg=bg_dark, fg=text_light)
        self.cuntry_entry = tk.Entry(self.details_frame, bg=bg_light, fg=text_light, insertbackground=text_light)
        
        self.f_and_lname_label.grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        self.fname_entry.grid(row=2, column=1, padx=5, pady=5, sticky=tk.W)
        self.lname_entry.grid(row=3, column=1, padx=5, pady=5, sticky=tk.W)
        self.gender_label.grid(row=4, column=0, padx=5, pady=5, sticky=tk.W)
        self.gender_entry.grid(row=4, column=1, padx=5, pady=5, sticky=tk.W)
        self.id_num_label.grid(row=5, column=0, padx=5, pady=5, sticky=tk.W)
        self.id_num_entry.grid(row=5, column=1, padx=5, pady=5, sticky=tk.W) 
        self.home_no_label.grid(row=6, column=0, padx=5, pady=5, sticky=tk.W)
        self.home_no_entry.grid(row=6, column=1, padx=5, pady=5, sticky=tk.W)
        self.cuntry_label.grid(row=7, column=0, padx=5, pady=5, sticky=tk.W)
        self.cuntry_entry.grid(row=7, column=1, padx=5, pady=5, sticky=tk.W)
        
        tk.Label(self.details_frame,
             text="At Least Fill 3.",
             bg=bg_dark, fg=accent_blue, font=("Arial", 10)
             ).grid(row=1, column=2, columnspan=2, padx=5, pady=5, sticky=tk.W)
             
        self.name_label = tk.Label(self.details_frame, text='User Name :', bg=bg_dark, fg=text_light)
        self.name_entry = tk.Entry(self.details_frame, bg=bg_light, fg=text_light, insertbackground=text_light)
        self.password_num0_label = tk.Label(self.details_frame, text='Password :', bg=bg_dark, fg=text_light)
        self.password_num0_entry = tk.Entry(self.details_frame, show="*", bg=bg_light, fg=text_light, insertbackground=text_light)
        self.password_num1_entry = tk.Entry(self.details_frame, show="*", bg=bg_light, fg=text_light, insertbackground=text_light)
        self.show_password_var = tk.IntVar()
        self.show_password_checkbutton = tk.Checkbutton(self.details_frame, text='Show Passwords', variable=self.show_password_var, bg=bg_dark, fg=text_light, selectcolor=bg_light)
        self.show_password_checkbutton.bind("<Button-1>", self.show_password_fuc)
        self.phone_num_label = tk.Label(self.details_frame, text='Phone No :', bg=bg_dark, fg=text_light)
        self.phone_num_entry = tk.Entry(self.details_frame, bg=bg_light, fg=text_light, insertbackground=text_light)
        self.email_label = tk.Label(self.details_frame, text='Email :', bg=bg_dark, fg=text_light)
        self.email_entry = tk.Entry(self.details_frame, bg=bg_light, fg=text_light, insertbackground=text_light)
        self.addres_label = tk.Label(self.details_frame, text='Address :', bg=bg_dark, fg=text_light)
        self.addres_entry = tk.Entry(self.details_frame, bg=bg_light, fg=text_light, insertbackground=text_light)
        self.type_label = tk.Label(self.details_frame, text='Type :', bg=bg_dark, fg=text_light)
        self.type_entry = tk.Entry(self.details_frame, bg=bg_light, fg=text_light, insertbackground=text_light)
        self.about_label = tk.Label(self.details_frame, text='About :', bg=bg_dark, fg=text_light)
        self.about_entry = tk.Entry(self.details_frame, bg=bg_light, fg=text_light, insertbackground=text_light)
        self.shops_label = tk.Label(self.details_frame, text='Shop :', bg=bg_dark, fg=text_light)
        self.shops_entry = tk.Entry(self.details_frame, bg=bg_light, fg=text_light, insertbackground=text_light)
        self.work_shop_label = tk.Label(self.details_frame, text='Work Shop :', bg=bg_dark, fg=text_light)
        self.work_shop_entry = tk.Entry(self.details_frame, bg=bg_light, fg=text_light, insertbackground=text_light)
        self.acsess_entry = tk.Entry(self.details_frame, bg=bg_light, fg=text_light, insertbackground=text_light)
        self.pimg_entry = tk.Entry(self.details_frame, bg=bg_light, fg=text_light, insertbackground=text_light)
        
        self.name_label.grid(row=2, column=2, padx=5, pady=5, sticky=tk.W)
        self.name_entry.grid(row=2, column=3, padx=5, pady=5, sticky=tk.W)
        self.password_num0_label.grid(row=3, column=2, padx=5, pady=5, sticky=tk.W)
        self.password_num0_entry.grid(row=3, column=3, padx=5, pady=5, sticky=tk.W)
        self.show_password_checkbutton.grid(row=4, column=3, padx=5, pady=5, sticky=tk.W)
        self.phone_num_label.grid(row=5, column=2, padx=5, pady=5, sticky=tk.W)
        self.phone_num_entry.grid(row=5, column=3, padx=5, pady=5, sticky=tk.W)
        self.email_label.grid(row=6, column=2, padx=5, pady=5, sticky=tk.W)
        self.email_entry.grid(row=6, column=3, padx=5, pady=5, sticky=tk.W)
        self.addres_label.grid(row=7, column=2, padx=5, pady=5, sticky=tk.W)
        self.addres_entry.grid(row=7, column=3, padx=5, pady=5, sticky=tk.W)
        self.type_label.grid(row=8, column=2, padx=5, pady=5, sticky=tk.W)
        self.type_entry.grid(row=8, column=3, padx=5, pady=5, sticky=tk.W)
        self.about_label.grid(row=9, column=2, padx=5, pady=5, sticky=tk.W)
        self.about_entry.grid(row=9, column=3, padx=5, pady=5, sticky=tk.W)

        self.fname_entry.bind('<KeyRelease>', self.on_name_entry)
        self.lname_entry.bind('<KeyRelease>', self.on_name_entry)
        self.name_entry.bind('<KeyRelease>', self.on_name_entry)
        
        self.forget_password_label = tk.Label(self.details_frame, text="User Found! Did You Forget Password?", fg=accent_blue, bg=bg_dark, cursor="hand2", font=("Arial", 10, "underline"))
        self.forget_password_label.bind("<Button-1>", self.forget_password_fuc)
        self.Found_User_id_var = ""
        
        self.add_button = tk.Button(self.details_frame, text='Find', command=self.add_user, bg=accent_blue, fg=text_light, font=("Arial", 10, "bold"), padx=10, pady=5)
        self.cancle_button = tk.Button(self.details_frame, text='Cancel', command=self.canceal_callback, bg=bg_light, fg=text_light, font=("Arial", 10, "bold"), padx=10, pady=5)

        self.add_button.grid(row=17, column=0, padx=5, pady=10, sticky=tk.W)
        self.cancle_button.grid(row=17, column=1, padx=5, pady=10, sticky=tk.W)
        
    def set_back_function(self, back_function):
        self.Canceal_callback = back_function

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
               if user[1] == self.name_entry.get():
                  self.forget_password_label.grid(row=1, column=2, padx=5, pady=5, sticky=tk.W)
                  self.Found_User_id_var = user[0];
                  self.add_button.config(text="Find")
                  return
        else:
            self.forget_password_label.grid_remove()
            self.add_button.config(text="Find")


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
        self.password_num_entry.delete(0, "end")
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
              if self.add_button.cget("text") == "Find":        
                  # Insert the new user into the database
                  User_likes = ""
                  User_following_shop = ""
                  User_favoraite_items = ""
                  User_rate = ""
                  cur.execute('INSERT INTO Users(User_fname, User_Lname, User_name, User_gender, User_country, User_phone_num, User_email, User_address, User_home_no, User_type, User_password, User_about, User_shop, User_work_shop, User_likes, User_following_shop, User_favoraite_items, User_rate, User_access, User_pimg) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',(User_fname, User_Lname, User_name, User_gender, User_country, User_phone_num, User_email, User_address, User_home_no, User_type, User_password0, User_about, User_shop, User_work_shop, User_likes, User_following_shop, User_favoraite_items, User_rate, User_access, User_pimg))
                    
              else:
                  item_id = int(self.Found_User_id_var)
                  print("item_id : " + str(item_id))
                  # UPDATE the new user into the database
                  cur.execute('UPDATE Users SET User_fname=?, User_Lname=?, User_name=?, User_gender=?, User_country=?, User_phone_num=?, User_email=?, User_address=?, User_home_no=?, User_id_pp_num=?, User_type=?, User_password=?, User_about=?, User_shop=?, User_work_shop=?, User_access=?, User_pimg=? WHERE User_id=?', (User_fname, User_Lname, User_name, User_gender, User_country, User_phone_num, User_email, User_address, User_home_no, User_id_pp_num, User_type, User_password0, User_about, User_shop, User_work_shop, User_access, User_pimg, item_id))
              
              # Commit the changes to the database
              conn.commit()
