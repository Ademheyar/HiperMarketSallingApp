import tkinter as tk
from tkinter import ttk
import sqlite3, os

data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data'))
db_path = os.path.join(data_dir, 'my_database.db')


from D.Security import *

from C.API.Get import *
from C.API.API import *
from C.API.Set import *


class CreateUserDialog(tk.Toplevel):
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

        self.type_var.set("Costumer")
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
        fname = name.split(" ")[0] if len(name.split(" ")) > 0 else name
        lname = name.split(" ")[1] if len(name.split(" ")) > 0 else ""
        address = self.address_var.get()
        id_num = self.id_num_var.get()
        phone_num = self.phone_num_var.get()
        email = self.email_var.get()
        user_type = self.type_var.get()
        password = self.password_var.get()
        access = self.access_var.get()

        Update_table_database("INSERT INTO Users (User_name, User_fname, User_lname, User_address, User_id_pp_num, User_phone_num, User_email, User_type, User_password, User_access) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                       (name, fname, lname, address, id_num, phone_num, email, user_type, password, access))
        conn.commit()

        self.parent.fill_user_listbox()
        self.master.username_entry.insert(0, name)
        self.master.username_var.set(name)
        self.destroy()
        
class UserManagementApp(tk.Toplevel):
    def __init__(self, parent, def_cm_id, user, Shops, on_Shop):
        super().__init__(parent)

        self.parent = parent
        self.user = user
        self.Shops = Shops
        self.on_Shop = on_Shop

        self.user_details = {}
        it = fetch_as_dict_list("SELECT * FROM Users WHERE User_id=?", (def_cm_id,))

        self.username_var = tk.StringVar()

        username_label = tk.Label(self, text="User name", font=("Arial", 14))
        username_label.grid(row=0, column=0, padx=10, pady=10)

        self.username_entry = tk.Entry(self, textvariable=self.username_var, font=("Arial", 14))
        if it:
            self.username_entry.insert(0, it[1])
            self.username_var.set(it[1])
        self.username_entry.grid(row=0, column=1, padx=10, pady=10)
        
        search_button = tk.Button(self, text="Search", command=self.search, font=("Arial", 14))
        search_button.grid(row=0, column=2, sticky="w", padx=10, pady=10)
        
        self.user_listbox = tk.Listbox(self, font=("Arial", 14), width=30)
        self.user_listbox.grid(row=1, column=0, columnspan=5, rowspan=5, padx=10, pady=10)
        self.user_listbox.bind("<<ListboxSelect>>", self.on_user_select)

        self.create_user_button = tk.Button(self, text="Create User", command=self.create_user_dialog, font=("Arial", 14))
        self.create_user_button.grid(row=6, column=0, sticky="w", padx=10, pady=10)

        self.create_user_button = tk.Button(self, text="Ok", command=self.done_selecting, font=("Arial", 14))
        self.create_user_button.grid(row=6, column=2, sticky="w", padx=10, pady=10)
        
        self.details_panel = tk.Frame(self)
        self.details_panel.grid(row=7, column=0, columnspan=3, rowspan=3, padx=10, pady=10, sticky="n")

        self.fill_user_listbox()
        # TODO: show this user info
        # TODO: user can change name, or password in this form
        # TODO: user can add sub user depending on its usertype
        self.search()
        
        self.username_var.trace('w', self.entry_changed)
        self.bind("<Up>", self.select_button)
        self.bind("<Down>", self.select_button)
        self.bind("<Return>", lambda _:self.done_selecting())
        # show the Payment Form window
        self.transient(self.master)
        self.grab_set()
        self.master.wait_window(self)
        
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
        selected_userId = self.user_listbox.get(self.user_listbox.curselection())[0]
        selected_usernid = self.user_listbox.get(self.user_listbox.curselection())[1]
        selected_username = self.user_listbox.get(self.user_listbox.curselection())[2]

        self.show_user_details(selected_userId, selected_usernid, selected_username)

    def show_user_details(self, Id, userid, username):
        
        if userid == None or userid == "None" or userid == "":
            row = fetch_as_dict_list("SELECT * FROM Users WHERE Id = ?", (Id,))
        else:
            row = fetch_as_dict_list("SELECT * FROM Users WHERE User_id = ?", (userid,))

        self.clear_details_panel()
        if row:
            row = row[0]
            print("row : "+str(row))
            Id = row['Id']
            user_id = row['User_id']
            username = row['User_name']
            if row['User_fname'] == None:
                row['User_fname'] = ""
            if row['User_Lname'] == None:
                row['User_Lname'] = ""
            name  = row['User_fname'] + " " + row['User_Lname']
            addres  = row['User_address']
            id_num  = row['User_id_pp_num']
            phone_num  = row['User_phone_num']
            email  = row['User_email']
            utype  = row['User_type']
            password  = row['User_password']
            acsess= row['User_access']

            user_id_label = tk.Label(self.details_panel, text="User ID: " + str(user_id), font=("Arial", 14))
            user_id_label.grid(row=0, column=0, sticky="w")

            username_label = tk.Label(self.details_panel, text="Username: " + str(name), font=("Arial", 14))
            username_label.grid(row=1, column=0, sticky="w")

            first_name_label = tk.Label(self.details_panel, text="Name: " + str(row['User_fname'])+ " "+ str(row['User_Lname']), font=("Arial", 14))
            first_name_label.grid(row=2, column=0, sticky="w")

            last_name_label = tk.Label(self.details_panel, text="phone number: " + str(phone_num), font=("Arial", 14))
            last_name_label.grid(row=3, column=0, sticky="w")

            email_label = tk.Label(self.details_panel, text="Email: " + str(email), font=("Arial", 14))
            email_label.grid(row=4, column=0, sticky="w")

            type_label = tk.Label(self.details_panel, text="Type : " + str(utype), font=("Arial", 14))
            type_label.grid(row=5, column=0, sticky="w")

            self.user_details = {
                "Id": Id,
                "User_id": user_id,
                "User_name": username,
                "User_fname": row['User_fname'],
                "User_Lname": row['User_Lname'],
                "User_address": addres,
                "User_id_pp_num": id_num,
                "User_phone_num": phone_num,
                "Email": email,
                "type": utype,
                "password": password,
                "acsess": acsess
            }
        else:
            no_details_label = tk.Label(self.details_panel, text="No details available", font=("Arial", 14))
            no_details_label.grid(row=0, column=0, sticky="w")
            self.user_details = None

    def fill_user_listbox(self):
        self.user_listbox.delete(0, tk.END)
        rows = fetch_as_dict_list("SELECT Id, User_id, User_name FROM Users", ())
        for row in rows:
            self.user_listbox.insert(tk.END, [row["Id"], row["User_id"], row["User_name"]])

    def clear_details_panel(self):
        for widget in self.details_panel.winfo_children():
            widget.destroy()

    def on_user_select(self, event):
        # print("self.user_listbox.curselection() " + str(self.user_listbox.curselection()))
        # print("self.user_listbox.get( " + str(self.user_listbox.get(self.user_listbox.curselection())))
        selected_userId = self.user_listbox.get(self.user_listbox.curselection())[0]
        selected_usernid = self.user_listbox.get(self.user_listbox.curselection())[1]
        selected_username = self.user_listbox.get(self.user_listbox.curselection())[2]

        self.show_user_details(selected_userId, selected_usernid, selected_username)

    def done_selecting(self):
        selected_userId = self.user_listbox.get(self.user_listbox.curselection())[0]
        selected_usernid = self.user_listbox.get(self.user_listbox.curselection())[1]
        selected_username = self.user_listbox.get(self.user_listbox.curselection())[2]
        if self.user_details:
            if str(selected_userId) == str(self.user_details["Id"]) and str(selected_usernid) == str(self.user_details["User_id"]) and selected_username == self.user_details["User_name"]:
                self.destroy()
            
    def entry_changed(self, *args):
        self.search()
        
    def search(self):
        username = self.username_var.get()
        rows = fetch_as_dict_list("SELECT * FROM Users WHERE User_name LIKE ? OR User_address LIKE ? OR User_id_pp_num LIKE ? OR User_phone_num LIKE ? OR User_email LIKE ? OR User_type LIKE ? OR User_access LIKE ?", 
                    ('%' + username + '%','%' + username + '%','%' + username + '%','%' + username + '%','%' + username + '%','%' + username + '%','%' + username + '%'))
        
        self.user_listbox.delete(0, tk.END)  
        for row in rows:
            self.user_listbox.insert(tk.END, [row['Id'], row['User_id'], row['User_name']])

    def create_user_dialog(self):
        if Chacke_Security(self, self.user, self.Shops[self.on_Shop], 20, f'User Not allowed to Create New Costumer'):
            CreateUserDialog(self)

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
