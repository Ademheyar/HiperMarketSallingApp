import tkinter as tk
from tkinter import ttk
import sqlite3

# Connect to the database or create it if it does not exist

import os
data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data'))
db_path = os.path.join(data_dir, 'my_database.db')
conn = sqlite3.connect(db_path)
cur = conn.cursor()

conn.commit()

class UserForm(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)

        # Create the search bar
        # Create the frame for the search bar and buttons
        self.search_frame = tk.Frame(self)
        self.search_frame.pack(side=tk.TOP, padx=5, pady=5)

        # create a StringVar to represent the search box
<<<<<<< HEAD
        search_var = tk.StringVar()
        self.search_entry = tk.Entry(self.search_frame, textvariable=search_var)
        self.search_entry.bind('<KeyRelease>', self.update_search_results)
        self.search_entry.pack(side=tk.LEFT, padx=5, pady=5)
            
        # bind the update_search_results function to the search box
        search_var.trace("w", self.update_search_results)
=======
        self.search_var = tk.StringVar()
        self.search_entry = tk.Entry(self.search_frame, textvariable=self.search_var)
        #self.search_entry.bind('<KeyRelease>', self.update_search_results)
        self.search_entry.pack(side=tk.LEFT, padx=5, pady=5)
            
        # bind the update_search_results function to the search box
        self.search_var.trace("w", self.update_search_results)
>>>>>>> db9ae79 (adding seller)


        # Create the list box
        self.list_box = ttk.Treeview(self)
        self.list_box.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.list_box.bind('<<TreeviewSelect>>', self.on_select)

        # Create the frame for the user details
        self.details_frame = tk.Frame(self.list_box)
        self.details_frame.pack_forget()

        # Create the widgets for the user details
        self.name_label = tk.Label(self.details_frame, text='Name:')
        self.name_entry = tk.Entry(self.details_frame)
        self.main_name = ""
        self.name_entry.bind('<KeyRelease>', lambda: self.on_name_entry)
        self.type_label = tk.Label(self.details_frame, text='TYPE:')
        self.type_entry = tk.Entry(self.details_frame)
        self.phone_num_label = tk.Label(self.details_frame, text='PHONE NUMBER:')
        self.phone_num_entry = tk.Entry(self.details_frame)
        self.email_label = tk.Label(self.details_frame, text='EMAIL:')
        self.email_entry = tk.Entry(self.details_frame)
        self.id_num_label = tk.Label(self.details_frame, text='ID Number:')
        self.id_num_entry = tk.Entry(self.details_frame)
        self.addres_label = tk.Label(self.details_frame, text='Addres:')
        self.addres_entry = tk.Entry(self.details_frame)
        self.acsess_label = tk.Label(self.details_frame, text='ACSSES:')
        self.acsess_entry = tk.Entry(self.details_frame)
<<<<<<< HEAD

=======
        
        self.f_and_lname_label = tk.Label(self.details_frame, text='First and Last Name :')
        self.fname_entry = tk.Entry(self.details_frame)
        self.lname_entry = tk.Entry(self.details_frame)
        self.name_label = tk.Label(self.details_frame, text='User Name :')
        self.name_entry = tk.Entry(self.details_frame)
        self.gender_label = tk.Label(self.details_frame, text='Gender :')
        self.gender_entry = tk.Entry(self.details_frame)
        self.cuntry_label = tk.Label(self.details_frame, text='Cuntry :')
        self.cuntry_entry = tk.Entry(self.details_frame)
        self.phone_num_label = tk.Label(self.details_frame, text='Phone No :')
        self.phone_num_entry = tk.Entry(self.details_frame)
        self.email_label = tk.Label(self.details_frame, text='Email :')
        self.email_entry = tk.Entry(self.details_frame)
        self.addres_label = tk.Label(self.details_frame, text='Adress :')
        self.addres_entry = tk.Entry(self.details_frame)
        self.id_num_label = tk.Label(self.details_frame, text='Id No :')
        self.id_num_entry = tk.Entry(self.details_frame)
        self.home_no_label = tk.Label(self.details_frame, text='Home No :')
        self.home_no_entry = tk.Entry(self.details_frame)
        self.type_label = tk.Label(self.details_frame, text='Type :')
        self.type_entry = tk.Entry(self.details_frame)
        self.password_num_label = tk.Label(self.details_frame, text='Password :')
        self.password_num_entry = tk.Entry(self.details_frame)
        self.about_label = tk.Label(self.details_frame, text='About :')
        self.about_entry = tk.Entry(self.details_frame)
        
        self.shops_label = tk.Label(self.details_frame, text='Shop :')
        self.shops_entry = tk.Entry(self.details_frame)
        self.work_shop_label = tk.Label(self.details_frame, text='Work Shop :')
        self.work_shop_entry = tk.Entry(self.details_frame)
        self.acsess_label = tk.Label(self.details_frame, text='ACSSES :')
        self.acsess_entry = tk.Entry(self.details_frame)
        self.pimg_label = tk.Label(self.details_frame, text='Image :')
        self.pimg_entry = tk.Entry(self.details_frame)
        
>>>>>>> db9ae79 (adding seller)

        self.add_button = tk.Button(self.details_frame, text='Add', command=self.add_user)
        self.cancle_button = tk.Button(self.details_frame, text='Cancle', command=self.hide_user_details_frame)


        self.add_searchbutton = tk.Button(self.search_frame, text='Add New user', command=self.show_user_details_frame)
        self.add_searchbutton.pack(side=tk.LEFT, padx=5, pady=5)

        self.change_button = tk.Button(self.search_frame, text='Change', command=self.show_change_forme)
        self.change_button.pack(side=tk.LEFT, padx=5, pady=5)
        self.change_button.config(state=tk.DISABLED)

        self.delete_button = tk.Button(self.search_frame, text='Delete', command=self.delete_user)
        self.delete_button.pack(side=tk.LEFT, padx=5, pady=5)
        self.delete_button.config(state=tk.DISABLED)


        # Pack the widgets for the user details
<<<<<<< HEAD
        self.name_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.E)
        self.name_entry.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)
        self.type_label.grid(row=5, column=0, padx=5, pady=5, sticky=tk.E)
        self.type_entry.grid(row=5, column=1, padx=5, pady=5, sticky=tk.W)
        self.phone_num_label.grid(row=3, column=0, padx=5, pady=5, sticky=tk.E)
        self.phone_num_entry.grid(row=3, column=1, padx=5, pady=5, sticky=tk.W)
        self.email_label.grid(row=4, column=0, padx=5, pady=5, sticky=tk.E)
        self.email_entry.grid(row=4, column=1, padx=5, pady=5, sticky=tk.W)
        self.id_num_label.grid(row=2, column=0, padx=5, pady=5, sticky=tk.E)
        self.id_num_entry.grid(row=2, column=1, padx=5, pady=5, sticky=tk.W)
        self.addres_label.grid(row=1, column=0, padx=5, pady=5, sticky=tk.E)
        self.addres_entry.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)
        self.acsess_label.grid(row=6, column=0, padx=5, pady=5, sticky=tk.E)
        self.acsess_entry.grid(row=6, column=1, padx=5, pady=5, sticky=tk.W)
=======
        self.f_and_lname_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.E)
        self.fname_entry.grid(row=0, column=1, padx=5, pady=5, sticky=tk.E)
        self.lname_entry.grid(row=0, column=2, padx=5, pady=5, sticky=tk.W)
        self.name_label.grid(row=1, column=0, padx=5, pady=5, sticky=tk.E)
        self.name_entry.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)
        self.gender_label.grid(row=2, column=0, padx=5, pady=5, sticky=tk.E)
        self.gender_entry.grid(row=2, column=1, padx=5, pady=5, sticky=tk.W)
        self.cuntry_label.grid(row=3, column=0, padx=5, pady=5, sticky=tk.E)
        self.cuntry_entry.grid(row=3, column=1, padx=5, pady=5, sticky=tk.W)
        self.phone_num_label.grid(row=4, column=0, padx=5, pady=5, sticky=tk.E)
        self.phone_num_entry.grid(row=4, column=1, padx=5, pady=5, sticky=tk.W)
        self.email_label.grid(row=5, column=0, padx=5, pady=5, sticky=tk.E)
        self.email_entry.grid(row=5, column=1, padx=5, pady=5, sticky=tk.W)
        self.addres_label.grid(row=6, column=0, padx=5, pady=5, sticky=tk.E)
        self.addres_entry.grid(row=6, column=1, padx=5, pady=5, sticky=tk.W)
        self.id_num_label.grid(row=7, column=0, padx=5, pady=5, sticky=tk.E)
        self.id_num_entry.grid(row=7, column=1, padx=5, pady=5, sticky=tk.W)
        self.home_no_label.grid(row=8, column=0, padx=5, pady=5, sticky=tk.E)
        self.home_no_entry.grid(row=8, column=1, padx=5, pady=5, sticky=tk.W)
        self.type_label.grid(row=9, column=0, padx=5, pady=5, sticky=tk.E)
        self.type_entry.grid(row=9, column=1, padx=5, pady=5, sticky=tk.W)
        self.password_num_label.grid(row=10, column=0, padx=5, pady=5, sticky=tk.E)
        self.password_num_entry.grid(row=10, column=1, padx=5, pady=5, sticky=tk.W)
        self.about_label.grid(row=11, column=0, padx=5, pady=5, sticky=tk.E)
        self.about_entry.grid(row=11, column=1, padx=5, pady=5, sticky=tk.W)
        self.shops_label.grid(row=12, column=0, padx=5, pady=5, sticky=tk.E)
        self.shops_entry.grid(row=12, column=1, padx=5, pady=5, sticky=tk.W)
        self.work_shop_label.grid(row=13, column=0, padx=5, pady=5, sticky=tk.E)
        self.work_shop_entry.grid(row=13, column=1, padx=5, pady=5, sticky=tk.W)
        self.acsess_label.grid(row=14, column=0, padx=5, pady=5, sticky=tk.E)
        self.acsess_entry.grid(row=14, column=1, padx=5, pady=5, sticky=tk.W)
        self.pimg_label.grid(row=15, column=0, padx=5, pady=5, sticky=tk.E)
        self.pimg_entry.grid(row=15, column=1, padx=5, pady=5, sticky=tk.W)
>>>>>>> db9ae79 (adding seller)

        self.add_button.grid(row=17, column=0, padx=5, pady=5, sticky=tk.W)
        self.cancle_button.grid(row=17, column=1, padx=5, pady=5, sticky=tk.W)
        self.update_user_listbox()

    def on_name_entry(self, event):
<<<<<<< HEAD
        cur.execute('SELECT * FROM USERS')
=======
        cur.execute('SELECT * FROM Users')
>>>>>>> db9ae79 (adding seller)
        users = cur.fetchall()
        for user in users:
            print("on_name_entry\n"+str(user[1]))
            if user[1] == self.name_entry.get():
                self.add_button.config(text="Update")    
                return
        if self.main_name == self.name_entry.get() and not self.main_name == "":
            self.add_button.config(text="Update")
        else:
            self.add_button.config(text="New")

    def show_user_form(self):
        # call the function in the main file to show the first frame
        self.master.master.show_frame("UserForm")
        
<<<<<<< HEAD
    def search_users(self, search_text):        
        # Search for the entered text in the code, name, short_key, and type fields of the user table
        cur.execute("SELECT * FROM USERS WHERE code LIKE ? OR name LIKE ? OR short_key LIKE ? OR type LIKE ?", 
                    ('%' + search_text + '%', '%' + search_text + '%', '%' + search_text + '%', '%' + search_text + '%'))
=======
    def search_users(self, search_text):
        
        # Search for the entered text in the code, name, short_key, and type fields of the user table
        cur.execute("SELECT * FROM Users WHERE User_name LIKE ? OR User_address LIKE ? OR User_id_pp_num LIKE ? OR User_phone_num LIKE ? OR User_email LIKE ? OR User_type LIKE ? OR User_access LIKE ?", 
                    ('%' + search_text + '%','%' + search_text + '%','%' + search_text + '%','%' + search_text + '%','%' + search_text + '%','%' + search_text + '%','%' + search_text + '%'))
>>>>>>> db9ae79 (adding seller)
        results = cur.fetchall()
        
        return results
    
    # create a function to update the search results whenever the search box changes
    def update_search_results(self, *args):
        # get the search string from the search box
        search_str = self.search_var.get()
        
        # search for users based on the search string
        users = self.search_users(search_str)
<<<<<<< HEAD
        
        # clear the current items in the list box
        self.list_box.delete(*self.list_box.get_children())
        self.list_box['columns'] = ('Name', 'Code', 'Type', 'Price')
        self.list_box.heading("#0", text="ID")
        self.list_box.heading("#1", text="Name")
        self.list_box.heading("#2", text="Code")
        self.list_box.heading("#3", text="Type")
        self.list_box.heading("#4", text="Price")

        # Add the users to the user listbox
        for user in users:
            self.list_box.insert('', 'end', text=user[0], values=(user[1], user[2], user[3], user[9]))

    def clear_user_details_widget(self):
        # Clear the user details widgets
        self.name_entry.delete(0, tk.END)
        self.type_entry.delete(0, tk.END)
        self.phone_num_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)
        self.id_num_entry.delete(0, tk.END)
        self.addres_entry.delete(0, tk.END)
        self.acsess_entry.delete(0, tk.END)
        #self.active_var.set(0)
=======
        self.update_results(users)
        
    def update_results(self, users):
        # Clear the user listbox
        self.list_box.delete(*self.list_box.get_children())
        self.list_box['columns'] = ('Name', 'Type', 'Phone_Number', 'Id_Number', 'Email', 'Adress')
        self.list_box.heading("#0", text="ID")
        self.list_box.heading("#1", text="Name")
        self.list_box.heading("#2", text="Type")
        self.list_box.heading("#3", text="Phone_Number")
        self.list_box.heading("#4", text="Id_Number")
        self.list_box.heading("#4", text="Email")
        self.list_box.heading("#4", text="Adress")

        
        # Add the users to the user listbox
        for user in users:
            self.list_box.insert('', 'end', text=user[0], values=(user[1], user[2], user[3], user[4], user[5], user[6]))

        # Hide the user details frame
        self.hide_user_details_frame()
        self.change_button.config(state=tk.DISABLED)
        
    def clear_user_details_widget(self):
        # Clear the user details widgets
        
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
>>>>>>> db9ae79 (adding seller)

    # Create the "Add New" button
    def show_user_details_frame(self):
        self.clear_user_details_widget()
        self.on_name_entry(None)
        self.details_frame.pack(side=tk.RIGHT, fill=tk.Y, expand=False)
        
    def hide_user_details_frame(self):
        self.clear_user_details_widget()
        self.details_frame.forget()

    # Create the "Change" button
    def show_change_forme(self):
        selected_user = self.list_box.selection()
        if selected_user:
            # Get the ID of the selected user
<<<<<<< HEAD
            user_id = self.list_box.item(selected_user)['values'][0]

            # Delete the user from the database
            cur.execute('SELECT * FROM USERS WHERE name=?', (user_id,))
            users = cur.fetchall()

            print("name : " + str(users))
            id, name, addres, id_num, phone_num, email, \
                type, password, acsess = users[0]
            # Clear the current text
            # than add new one
            self.name_entry.delete(0, "end")
            self.name_entry.insert(0, name)
            self.main_name = name
            self.addres_entry.delete(0, "end")
            self.addres_entry.insert(0, addres)
            self.id_num_entry.delete(0, "end")
            self.id_num_entry.insert(0, id_num)
            self.phone_num_entry.delete(0, "end")
            self.phone_num_entry.insert(0, phone_num)
            self.email_entry.delete(0, "end")
            self.email_entry.insert(0, email)
            self.type_entry.delete(0, "end")
            self.type_entry.insert(0, type)
            #password
            self.acsess_entry.delete(0, "end")
            self.acsess_entry.insert(0, acsess)

            self.add_button.config(text="Update")
            # Commit the changes to the database
            conn.commit()
            self.details_frame.pack(side=tk.RIGHT, fill=tk.Y, expand=False)
=======
            user_id = self.list_box.item(selected_user)['text']

            # Delete the user from the database
            cur.execute('SELECT * FROM Users WHERE User_id=?', (user_id,))
            users = cur.fetchall()

            print("name : " + str(users))
            if users:
                id, User_fname, User_Lname, User_name, User_gender, User_country, User_phone_num, User_email, User_address, \
                    User_home_no, User_id_pp_num, User_type, User_password, User_about, User_shop, User_work_shop, User_likes, User_following_shop, User_favoraite_items, User_rate, User_access, User_pimg = users[0]
                # Clear the current text
                # than add new one
                self.fname_entry.delete(0, "end")
                self.fname_entry.insert(0, str(User_fname))
                self.lname_entry.delete(0, "end")
                self.lname_entry.insert(0, str(User_Lname))
                self.name_entry.delete(0, "end")
                self.name_entry.insert(0, str(User_name))
                self.gender_entry.delete(0, "end")
                self.gender_entry.insert(0, str(User_gender))
                self.cuntry_entry.delete(0, "end")
                self.cuntry_entry.insert(0, str(User_country))
                self.phone_num_entry.delete(0, "end")
                self.phone_num_entry.insert(0, str(User_phone_num))
                self.email_entry.delete(0, "end")
                self.email_entry.insert(0, str(User_email))
                self.addres_entry.delete(0, "end")
                self.addres_entry.insert(0, str(User_address))
                self.home_no_entry.delete(0, "end")
                self.home_no_entry.insert(0, str(User_home_no))
                self.id_num_entry.delete(0, "end")
                self.id_num_entry.insert(0, str(User_id_pp_num))
                self.type_entry.delete(0, "end")
                self.type_entry.insert(0, str(User_type))
                self.password_num_entry.delete(0, "end")
                self.password_num_entry.insert(0, str(User_password))
                self.about_entry.delete(0, "end")
                self.about_entry.insert(0, str(User_about))
                self.shops_entry.delete(0, "end")
                self.shops_entry.insert(0, str(User_shop))
                self.work_shop_entry.delete(0, "end")
                self.work_shop_entry.insert(0, str(User_work_shop))
                self.acsess_entry.delete(0, "end")
                self.acsess_entry.insert(0, str(User_access))
                self.pimg_entry.delete(0, "end")
                self.pimg_entry.insert(0, str(User_pimg))
                

                self.add_button.config(text="Update")
                # Commit the changes to the database
                conn.commit()
                self.details_frame.pack(side=tk.RIGHT, fill=tk.Y, expand=False)
>>>>>>> db9ae79 (adding seller)

    def on_select(self, event):
        if len(event.widget.selection()) > 0:
            self.change_button.config(state=tk.NORMAL)
            self.delete_button.config(state=tk.NORMAL)
        else:
            self.change_button.config(state=tk.DISABLED)
            self.delete_button.config(state=tk.DISABLED)

    # Define the function for updating the user listbox
    def update_user_listbox(self):
<<<<<<< HEAD
        # Clear the user listbox
        self.list_box.delete(*self.list_box.get_children())

        # Get the users from the database
        cur.execute('SELECT * FROM USERS')
        users = cur.fetchall()
        self.list_box['columns'] = ('Name', 'Type', 'Phone_Number', 'Id_Number', 'Email', 'Adress')
        self.list_box.heading("#0", text="ID")
        self.list_box.heading("#1", text="Name")
        self.list_box.heading("#2", text="Type")
        self.list_box.heading("#3", text="Phone_Number")
        self.list_box.heading("#4", text="Id_Number")
        self.list_box.heading("#4", text="Email")
        self.list_box.heading("#4", text="Adress")

        # Add the users to the user listbox
        for user in users:
            self.list_box.insert('', 'end', text=user[0], values=(user[1], user[2], user[3], user[4], user[5], user[6]))

        # Hide the user details frame
        self.hide_user_details_frame()
        self.change_button.config(state=tk.DISABLED)

    # Define the function for adding a new user
    def add_user(self):
        # Get the values from the user details widgets
        name = self.name_entry.get()
        typ = self.type_entry.get()
        email = self.email_entry.get()
        phone_num = self.phone_num_entry.get()
        id_num = self.id_num_entry.get()
        addres = self.addres_entry.get()
        acsess = self.acsess_entry.get()
        password = ""

        if self.add_button.cget("text") == "New":        
            # Insert the new user into the database
            cur.execute('INSERT INTO USERS (name, addres, id_num, phone_num, email, type, password, acsess) VALUES (?, ?, ?, ?, ?, ?, ?, ?)', (name, addres, id_num, phone_num, email, typ, password, acsess))
=======
        # Get the users from the database
        cur.execute('SELECT * FROM USERS')
        users = cur.fetchall()
        self.update_results(users)
        
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
        User_password = self.password_num_entry.get()
        User_about = self.about_entry.get()
        User_shop = self.shops_entry.get()
        User_work_shop = self.work_shop_entry.get()
        User_access = self.acsess_entry.get()
        User_pimg =  self.pimg_entry.get()
        
        if self.add_button.cget("text") == "New":        
            # Insert the new user into the database
            User_likes = ""
            User_following_shop = ""
            User_favoraite_items = ""
            User_rate = ""
            cur.execute('INSERT INTO Users(User_fname, User_Lname, User_name, User_gender, User_country, User_phone_num, User_email, User_address, User_home_no, User_type, User_password, User_about, User_shop, User_work_shop, User_likes, User_following_shop, User_favoraite_items, User_rate, User_access, User_pimg) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',(User_fname, User_Lname, User_name, User_gender, User_country, User_phone_num, User_email, User_address, User_home_no, User_type, User_password, User_about, User_shop, User_work_shop, User_likes, User_following_shop, User_favoraite_items, User_rate, User_access, User_pimg))
              
>>>>>>> db9ae79 (adding seller)
        else:
            item_id = int(self.list_box.item(self.list_box.selection())['text'])
            print("item_id : " + str(item_id))
            # UPDATE the new user into the database
<<<<<<< HEAD
            cur.execute('UPDATE USERS SET name=?, addres=?, id_num=?, phone_num=?, email=?, type=?, password=?, acsess=? WHERE id=?', (name, addres, id_num, phone_num, email, typ, password, acsess, item_id))
=======
            cur.execute('UPDATE Users SET User_fname=?, User_Lname=?, User_name=?, User_gender=?, User_country=?, User_phone_num=?, User_email=?, User_address=?, User_home_no=?, User_id_pp_num=?, User_type=?, User_password=?, User_about=?, User_shop=?, User_work_shop=?, User_access=?, User_pimg=? WHERE User_id=?', (User_fname, User_Lname, User_name, User_gender, User_country, User_phone_num, User_email, User_address, User_home_no, User_id_pp_num, User_type, User_password, User_about, User_shop, User_work_shop, User_access, User_pimg, item_id))
        
>>>>>>> db9ae79 (adding seller)
        # Commit the changes to the database
        conn.commit()

        # Clear the user details widgets
        self.clear_user_details_widget()
        
        # Update the user listbox
        self.update_user_listbox()

    # Define the function for deleting a user
    def delete_user(self):
        # Get the selected user from the listbox
        selected_user = self.list_box.selection()

        if selected_user:
            # Get the ID of the selected user
            user_id = self.list_box.item(selected_user)['values'][0]
        
            # Delete the user from the database
<<<<<<< HEAD
            cur.execute('DELETE FROM USERS WHERE name=?', (user_id,))
=======
            cur.execute('DELETE FROM Users WHERE User_id=?', (user_id,))
>>>>>>> db9ae79 (adding seller)

            # Commit the changes to the database
            conn.commit()
            # Update the user listbox
<<<<<<< HEAD
            self.update_user_listbox()
=======
            self.update_user_listbox()
>>>>>>> db9ae79 (adding seller)
