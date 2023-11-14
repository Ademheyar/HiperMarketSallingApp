import tkinter as tk
from tkinter import ttk
import sqlite3

<<<<<<< HEAD
=======
from M.Display import DisplayFrame
>>>>>>> db9ae79 (adding seller)

import os
data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'data'))
db_path = os.path.join(data_dir, 'my_database.db')
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

<<<<<<< HEAD
cursor.execute("SELECT * FROM USERS WHERE name=? AND password=?", ('adem', '123'))
=======
cursor.execute("SELECT * FROM USERS WHERE User_name=? AND User_password=?", ('adem', '123'))
>>>>>>> db9ae79 (adding seller)
us = cursor.fetchone()

if not us:
   cursor.execute("""
<<<<<<< HEAD
    INSERT INTO USERS (name, password)
    VALUES ('adem', '123');
=======
    INSERT INTO USERS (User_name, User_password, User_type)
    VALUES ('adem', '123', 'IT');
>>>>>>> db9ae79 (adding seller)
    """)

conn.commit()

class Loging_Frame(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        
        self.logging_frame = tk.Frame(self, bg="red", height=screen_height, width=screen_width)
        self.logging_frame.pack()

        self.logging_box = tk.Frame(self.logging_frame, bg="white", bd=5, relief="groove")
        self.logging_box.place(relx=0.5, rely=0.5, anchor="center", width=400, height=300)

        # Main frame that will hold the other frames
        # Main frame that will hold the other frames
<<<<<<< HEAD
        self.logo_label = tk.Label(self.logging_box, text="ADOTSHOPPING", font=("Helvetica", 36), bg="#2c3e50", fg="#ffffff")
        self.logo_label.pack(pady=20)


        self.username_label = tk.Label(self.logging_box, text="Username", bg="#2c3e50", fg="#ffffff")
        self.username_entry = tk.Entry(self.logging_box, bg="#ecf0f1", fg="#34495e")
=======
        self.logo_label = tk.Label(self.logging_box, text="Hiper Market", font=("Helvetica", 36), bg="#2c3e50", fg="#ffffff")
        self.logo_label.pack(pady=20)

        '''self.node_combobox = ttk.Combobox(self.root, state="readonly")
        self.node_combobox.pack(fill=tk.X, pady=10)
        self.node_combobox.bind("<<ComboboxSelected>>", self.update_combobox_values)
        '''
        
        self.username_label = tk.Label(self.logging_box, text="Username", bg="#2c3e50", fg="#ffffff")
        self.username_entry = tk.Entry(self.logging_box, bg="#ecf0f1", fg="#34495e")

        cursor.execute("SELECT * FROM setting")
        b = cursor.fetchall()
        
        # ToDO make it chacke setting saved user name every time new word pressed
>>>>>>> db9ae79 (adding seller)
        self.password_label = tk.Label(self.logging_box, text="Password", bg="#2c3e50", fg="#ffffff")
        self.password_entry = tk.Entry(self.logging_box, show="*", bg="#ecf0f1", fg="#34495e")

        self.username_label.pack(side="top", anchor="n")
        self.username_entry.pack(side="top", anchor="n")
        self.password_label.pack(side="top", anchor="n")
        self.password_entry.pack(side="top", anchor="n")
        self.log_in_button = tk.Button(self.logging_box, text="Log In", command=self.log_in, bg="#2ecc71", fg="#ffffff")
        self.log_in_button.pack(side="top", anchor="n")
<<<<<<< HEAD
        self.username_entry.insert(0,"adem")
        self.password_entry.insert(0,"123")
        
=======
        self.username_entry.insert(0,"")
        self.password_entry.insert(0,"")
                  
    def update_combobox_values(self):
        #print("ss "+ str([";"] + [name[0] for name in self.node_hierarchy]))
        pass #self.node_combobox["values"] = [";"] + [name[0] for name in self.node_hierarchy]

>>>>>>> db9ae79 (adding seller)

    def log_in(self):
        entered_username = self.username_entry.get()
        entered_password = self.password_entry.get()

<<<<<<< HEAD
        cursor.execute("SELECT * FROM USERS WHERE name=? AND password=?", (entered_username, entered_password))
        user = cursor.fetchone()

        if user:
            error_label = tk.Label(self.logging_box, text="Login Secsesfull", font=("Helvetica", 18), bg="#e74c3c", fg="green")
            error_label.pack(pady=20)
            self.master.frames["DisplayFrame"].user = entered_username
            self.master.frames["DisplayFrame"].load()
=======
        cursor.execute("SELECT * FROM USERS WHERE User_name=? AND User_password=?", (entered_username, entered_password))
        users = cursor.fetchall()
         
        if users:
           for user in users:
              if "IT" in user[11] or "Admin" in user[11] or "Worker" in user[11]:
                  #print("User : " + str(user))
                  #print("User11 : " + str(user[15]))
                  error_label = tk.Label(self.logging_box, text="Login Secsesfull", font=("Helvetica", 18), bg="#e74c3c", fg="green")
                  error_label.pack(pady=20)
                  self.master.display_frame = DisplayFrame(self.master, user)
                  self.master.display_frame.grid(row=0, column=0, sticky="nsew")
                  self.master.frames["DisplayFrame"] = self.master.display_frame
                  self.master.frames["DisplayFrame"].user = user
                  self.master.frames["DisplayFrame"].load()
>>>>>>> db9ae79 (adding seller)
        else:
            error_label = tk.Label(self.logging_box, text="Login failed", font=("Helvetica", 18), bg="#e74c3c", fg="#ffffff")
            error_label.pack(pady=20)
    
    def show_first_frame(self):
        # call the function in the main file to show the first frame
        self.master.show_frame("DisplayFrame")
