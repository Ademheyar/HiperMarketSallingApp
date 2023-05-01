import tkinter as tk
from tkinter import ttk
import sqlite3

class InfoForm(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)

        # Create the search bar
        # Create the frame for the search bar and buttons
        self.search_frame = tk.Frame(self)
        self.search_frame.pack(side=tk.TOP, padx=5, pady=5)

        # create a StringVar to represent the search box
        # Create the frame for the product details
        

    def show_info_form(self):
        # call the function in the main file to show the first frame
        self.master.master.show_frame("InfoForm")