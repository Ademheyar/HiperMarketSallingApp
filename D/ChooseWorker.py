import tkinter as tk
from tkinter import ttk
import sqlite3, os

data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data'))
db_path = os.path.join(data_dir, 'my_database.db')

import sqlite3
import shutil
import datetime
import os
import atexit
import sys
import random

current_dir = os.path.abspath(os.path.dirname(__file__))
MAIN_dir = os.path.join(current_dir, '..')
sys.path.append(MAIN_dir)

from D.GetVALUE import GetvalueForm

from C.API.Get import *
from C.API.API import *
from C.API.Set import *

class CreateWorkerDialog(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)

        self.parent = parent

        self.name_var = tk.StringVar()
        self.address_var = tk.StringVar()
        self.id_num_var = tk.StringVar()
        self.phone_num_var = tk.StringVar()
        self.email_var = tk.StringVar()
        self.type_var = tk.StringVar()
        self.password_var = tk.StringVar()
        self.access_var = tk.StringVar()

        self.type_var.set("WORKER")
        name_label = tk.Label(self, text="Name", font=("Arial", 14))
        name_label.grid(row=0, column=0, padx=10, pady=10)

        name_entry = tk.Entry(self, textvariable=self.name_var, font=("Arial", 14))
        name_entry.grid(row=0, column=1, padx=10, pady=10)

        address_label = tk.Label(self, text="Address", font=("Arial", 14))
        address_label.grid(row=1, column=0, padx=10, pady=10)

        address_entry = tk.Entry(self, textvariable=self.address_var, font=("Arial", 14))
        address_entry.grid(row=1, column=1, padx=10, pady=10)

        id_num_label = tk.Label(self, text="ID Number", font=("Arial", 14))
        id_num_label.grid(row=2, column=0, padx=10, pady=10)

        id_num_entry = tk.Entry(self, textvariable=self.id_num_var, font=("Arial", 14))
        id_num_entry.grid(row=2, column=1, padx=10, pady=10)

        phone_num_label = tk.Label(self, text="Phone Number", font=("Arial", 14))
        phone_num_label.grid(row=3, column=0, padx=10, pady=10)

        phone_num_entry = tk.Entry(self, textvariable=self.phone_num_var, font=("Arial", 14))
        phone_num_entry.grid(row=3, column=1, padx=10, pady=10)

        email_label = tk.Label(self, text="Email", font=("Arial", 14))
        email_label.grid(row=4, column=0, padx=10, pady=10)

        email_entry = tk.Entry(self, textvariable=self.email_var, font=("Arial", 14))
        email_entry.grid(row=4, column=1, padx=10, pady=10)

        type_label = tk.Label(self, text="Type", font=("Arial", 14))
        type_label.grid(row=5, column=0, padx=10, pady=10)

        type_entry = tk.Entry(self, textvariable=self.type_var, font=("Arial", 14))
        type_entry.grid(row=5, column=1, padx=10, pady=10)

        password_label = tk.Label(self, text="Password", font=("Arial", 14))
        password_label.grid(row=6, column=0, padx=10, pady=10)

        password_entry = tk.Entry(self, textvariable=self.password_var, font=("Arial", 14))
        password_entry.grid(row=6, column=1, padx=10, pady=10)

        access_label = tk.Label(self, text="Access", font=("Arial", 14))
        access_label.grid(row=7, column=0, padx=10, pady=10)

        access_entry = tk.Entry(self, textvariable=self.access_var, font=("Arial", 14))
        access_entry.grid(row=7, column=1, padx=10, pady=10)

        create_button = tk.Button(self, text="Create", command=self.create_user, font=("Arial", 14))
        create_button.grid(row=8, column=0, padx=10, pady=10)
        


        cancel_button = tk.Button(self, text="Cancel", command=self.destroy, font=("Arial", 14))
        cancel_button.grid(row=8, column=1, padx=10, pady=10)

        self.transient(self.master)
        self.grab_set()
        self.master.wait_window(self)

    def create_user(self):
        name = self.name_var.get()
        address = self.address_var.get()
        id_num = self.id_num_var.get()
        phone_num = self.phone_num_var.get()
        email = self.email_var.get()
        user_type = self.type_var.get()
        password = self.password_var.get()
        access = self.access_var.get()

        Update_table_database("INSERT INTO Users (User_name, User_address, User_id_pp_num, User_phone_num, User_email, User_type, User_password, User_access) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                       (name, address, id_num, phone_num, email, user_type, password, access))
        conn.commit()

        self.parent.fill_user_listbox()
        self.master.username_entry.insert(0, name)
        self.master.username_var.set(name)
        self.destroy()

class WorkerManagementApp(tk.Tk):
    def __init__(self, master, doc_bar, T_qty):
        #super().__init__(parent)
        
        self.getvalue_form = tk.Toplevel(master)
        self.getvalue_form.title("Choose Worker")

        self.master = master

        self.user_details = {}
        self.T_qty = T_qty
        self._qty = 0
        self.doc_bar = doc_bar
        self.username_var = tk.StringVar()

        username_label = tk.Label(self.getvalue_form, text="Worker name", font=("Arial", 14))
        username_label.grid(row=0, column=0, padx=10, pady=10)

        self.username_entry = tk.Entry(self.getvalue_form, textvariable=self.username_var, font=("Arial", 14))
        self.username_entry.grid(row=0, column=1, padx=10, pady=10)
        
        search_button = tk.Button(self.getvalue_form, text="Search", command=self.search, font=("Arial", 14))
        search_button.grid(row=0, column=2, sticky="w", padx=10, pady=10)
        
        self.user_listbox = tk.Listbox(self.getvalue_form, font=("Arial", 14), width=30)
        self.user_listbox.grid(row=1, column=0, columnspan=5, rowspan=5, padx=10, pady=10)
        self.user_listbox.bind("<<ListboxSelect>>", self.on_user_select)

        self.create_user_button = tk.Button(self.getvalue_form, text="Create User", command=self.create_user_dialog, font=("Arial", 14))
        self.create_user_button.grid(row=6, column=0, sticky="w", padx=10, pady=10)

        self.create_user_button = tk.Button(self.getvalue_form, text="Ok", command=self.done_selecting, font=("Arial", 14))
        self.create_user_button.grid(row=6, column=2, sticky="w", padx=10, pady=10)
        
        self.details_panel = tk.Frame(self.getvalue_form)
        self.details_panel.grid(row=7, column=0, columnspan=3, rowspan=3, padx=10, pady=10, sticky="n")

        self.fill_user_listbox()
        # TODO: show this user info
        # TODO: user can change name, or password in this form
        # TODO: user can add sub user depending on its usertype
        self.search()
        
        self.username_var.trace('w', self.entry_changed)
        
        # show the Payment Form window
        self.getvalue_form.transient(self.master)
        self.getvalue_form.grab_set()
        self.getvalue_form.focus_set()
        self.getvalue_form.transient(self.master)
        self.getvalue_form.bind("<Up>", self.select_button)
        self.getvalue_form.bind("<Down>", self.select_button)
        self.getvalue_form.bind("<Escape>", lambda _: self.getvalue_form.destroy())
        self.getvalue_form.bind("<Return>", lambda _: self.done_selecting())

        
        self.master.wait_window(self.getvalue_form)
        
    def select_button(self, event):
        current_selection = self.user_listbox.curselection()
        if event.keysym == "Up":
            if current_selection:
                next_index = (current_selection[0]-1)% self.user_listbox.size()
                self.user_listbox.selection_clear(0, tk.END)
                self.user_listbox.selection_set(next_index)
            else:
                self.user_listbox.selection_set(0)
        elif event.keysym == "Down":
            if current_selection:
                next_index = (current_selection[0]+1)% self.user_listbox.size()
                self.user_listbox.selection_clear(0, tk.END)
                self.user_listbox.selection_set(next_index)
            else:
                self.user_listbox.selection_set(0)
        selected_username = self.user_listbox.get(self.user_listbox.curselection())[0]
        self.show_user_details(selected_username)
        
    def show_user_details(self, id):
        row = fetch_as_dict_list("SELECT * FROM Users WHERE User_id = ?", (id,))
        

        self.clear_details_panel()

        if row:
            print("row : "+str(row))
            user_id = row[0]
            name  = row[3]
            addres  = row[4]
            id_num  = row[5]
            phone_num  = row[6]
            email  = row[7]
            utype  = row[11]
            password  = row[12]
            acsess= row[13]

            user_id_label = tk.Label(self.details_panel, text="User ID: " + str(user_id), font=("Arial", 14))
            user_id_label.grid(row=0, column=0, sticky="w")

            username_label = tk.Label(self.details_panel, text="Username: " + str(name), font=("Arial", 14))
            username_label.grid(row=1, column=0, sticky="w")

            first_name_label = tk.Label(self.details_panel, text="Name: " + str(row[1])+ " "+ str(row[2]), font=("Arial", 14))
            first_name_label.grid(row=2, column=0, sticky="w")

            last_name_label = tk.Label(self.details_panel, text="phone number: " + str(phone_num), font=("Arial", 14))
            last_name_label.grid(row=3, column=0, sticky="w")

            email_label = tk.Label(self.details_panel, text="Email: " + str(email), font=("Arial", 14))
            email_label.grid(row=4, column=0, sticky="w")

            type_label = tk.Label(self.details_panel, text="Type : " + str(utype), font=("Arial", 14))
            type_label.grid(row=5, column=0, sticky="w")

            self.user_details = {
                "User_id": user_id,
                "User_name": name,
                "User_address": addres,
                "User_id_pp_num": id_num,
                "User_phone_num": phone_num,
                "Email": email,
                "type": utype,
                "password": password,
                "acsess": acsess
            }

    def fill_user_listbox(self):
        self.user_listbox.delete(0, tk.END)
        rows = fetch_as_dict_list("SELECT User_name FROM Users")
        
        for row in rows:
            self.user_listbox.insert(tk.END, row[0])

    def clear_details_panel(self):
        for widget in self.details_panel.winfo_children():
            widget.destroy()

    def on_user_select(self, event):
        #print("self.user_listbox.curselection() " + str(self.user_listbox.curselection()))
        #print("self.user_listbox.get( " + str(self.user_listbox.get(self.user_listbox.curselection())))
        selected_username = self.user_listbox.get(self.user_listbox.curselection())[0]
        self.show_user_details(selected_username)

    def done_selecting(self):
        #print("aaaa")
        if self.user_details:
            selected_username = self.user_listbox.get(self.user_listbox.curselection())[0]
            #print("aaab")
            DATE = datetime.datetime.now().strftime('%Y-%m-%d')
            m = GetvalueForm(self, self.T_qty-self._qty, str(self.user_details["User_name"]) + "ITEM SELLED")
            i = float(m.value)
            if self._qty + i > self.T_qty:
                i = self.T_qty-self._qty
            self._qty += i
            Update_table_database("INSERT INTO COUNT_SELL (SELLER_ID, SELLER_NAME, DOC_BARCODE, ITEM_COUNTED, DATE) VALUES (?, ?, ?, ?, ?)",
                           (self.user_details["User_id"], self.user_details["User_name"], self.doc_bar, i, DATE))
            conn.commit()
            if self.T_qty != self._qty:
                return
            else:
                if selected_username == self.user_details["User_id"]:
                    self.getvalue_form.destroy()
        else:
            #print("aaac")
            self.user_details = {
                "User_id": None,
                "User_name": "It-Salf",
                "User_address": "",
                "User_id_pp_num": "",
                "User_phone_num": "",
                "Email": "",
                "type": "",
                "password": "",
                "acsess": ""
            }
            self.getvalue_form.destroy()
    def entry_changed(self, *args):
        self.search()
        
    def search(self):
        username = self.username_var.get()
        rows = fetch_as_dict_list("SELECT * FROM Users WHERE (User_name LIKE ? OR User_address LIKE ? OR User_id_pp_num LIKE ? OR User_phone_num LIKE ? OR User_email LIKE ? OR User_access LIKE ?) AND User_type=?", 
                    ('%' + username + '%','%' + username + '%','%' + username + '%','%' + username + '%','%' + username + '%','%' + username + '%',"WORKER"))
        
        self.user_listbox.delete(0, tk.END)
        for row in rows:
            self.user_listbox.insert(tk.END, [row[0], row[3]])

    def create_user_dialog(self):
        CreateWorkerDialog(self)

    def close_connection(self):
        cursor.close()
        conn.close()
        
'''if __name__ == "__main__":
    root = tk.Tk()
    app = UserManagementApp(root)

    if app.user_details:
        print(app.user_details)
    root.mainloop()
    app.close_connection()'''
