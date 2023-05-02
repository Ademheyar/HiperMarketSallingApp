import tkinter as tk
from tkinter import ttk
import sqlite3

conn = sqlite3.connect("my_database.db")
cursor = conn.cursor()

class ShowchartForm(tk.Tk):
    def __init__(self, master):
        self.master = master
        
        
        # create a Toplevel window for the payment form
        self.Showchart_form = tk.Toplevel(self.master)
        self.Showchart_form.title("Chart List Form")

        # calculate the center coordinates of the screen
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        x = (screen_width / 2) - (300 / 2)  # 500 is the width of the Payment Form window
        y = (screen_height / 2) - (300 / 2)  # 500 is the height of the Payment Form window

        # set the position of the Payment Form window to center
        self.getvalue_form.geometry(f"300x400+{int(x)}+{int(y)}")
        self.getvalue_form.grid_rowconfigure(0, weight=1)
        self.getvalue_form.grid_rowconfigure(1, weight=1)
        self.getvalue_form.grid_rowconfigure(2, weight=1)
        self.getvalue_form.grid_rowconfigure(3, weight=1)
        self.getvalue_form.grid_rowconfigure(4, weight=1)
        self.getvalue_form.grid_columnconfigure(0, weight=1)
        self.getvalue_form.grid_columnconfigure(1, weight=1)
        self.getvalue_form.grid_columnconfigure(2, weight=1)
        self.getvalue_form.grid_columnconfigure(3, weight=1)

        self.include_var = tk.StringVar()
        self.get_amount_entry = tk.Listbox(self.getvalue_form, textvariable=self.include_var, width=15, font=("Arial", 12))
        self.get_amount_entry.grid(row=0, column=0, sticky="nsew", columnspan=4)

        self.button15 = tk.Button(self.getvalue_form, text="Select", fg="white", font=("Arial", 12), command= lambda: self.add_num("enter"))
        self.button15.grid(row=4, column=2, sticky="nsew")
        self.close_btn = tk.Button(self.getvalue_form, text="Close", command= lambda: self.getvalue_form.destroy())
        self.close_btn.grid(row=4, column=3, sticky="nsew")

        # show the Payment Form window
        self.getvalue_form.transient(self.master)
        self.getvalue_form.grab_set()
        self.master.wait_window(self.getvalue_form)

    def selecte_chart(self):
        pass