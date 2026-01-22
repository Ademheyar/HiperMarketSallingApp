import tkinter as tk
from tkinter import ttk
import sqlite3

import json

from C.Sql3 import *

import os
data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'data'))
db_path = os.path.join(data_dir, 'my_database.db')
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

cursor.execute("SELECT * FROM USERS WHERE User_name=? AND User_password=?", ('adem', '123'))
us = cursor.fetchone()
if not us:
   cursor.execute("""
    INSERT INTO USERS (User_name, User_password, User_type)
    VALUES ('adem', '123', 'IT');
    """)

conn.commit()


class Loging_Frame(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        
        self.logging_frame = tk.Frame(self, bg="gray", height=screen_height, width=screen_width)
        self.logging_frame.pack()

        self.logging_box = tk.Frame(self.logging_frame, bg="white", bd=5, relief="groove")
        self.logging_box.place(relx=0.5, rely=0.5, anchor="center", width=500, height=400)

        # Main frame that will hold the other frames
        # Main frame that will hold the other frames
        self.logo_label = tk.Label(self.logging_box, text="Hiper Market", font=("Helvetica", 36))#, bg="#2c3e50", fg="#ffffff")
        self.logo_label.grid(row=0, column=0, columnspan=4, sticky="e")

        '''self.node_combobox = ttk.Combobox(self.root, state="readonly")
        self.node_combobox.pack(fill=tk.X, pady=10)
        self.node_combobox.bind("<<ComboboxSelected>>", self.update_combobox_values)
        '''
        
    
      
    def update_combobox_values(self):
        #print("ss "+ str([";"] + [name[0] for name in self.node_hierarchy]))
        pass #self.node_combobox["values"] = [";"] + [name[0] for name in self.node_hierarchy]


    
    def show_first_frame(self):
        # call the function in the main file to show the first frame
        self.master.show_frame("DisplayFrame")
