import tkinter as tk
from tkinter import ttk
import sqlite3, os, sys
import datetime

data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data'))
db_path = os.path.join(data_dir, 'my_database.db')
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

current_dir = os.path.abspath(os.path.dirname(__file__))
MAIN_dir = os.path.join(current_dir, '..')
sys.path.append(MAIN_dir)
from D.ItemSelector import ItemSelectorWidget
import os
from D.Calan import calander_entry

class GetDateForm(tk.Tk):
    def __init__(self, master, from_date, to_date):
        self.master = master
        self.start_value = []
        self.end_value = []
        self.date = datetime.datetime.now().strftime('%Y-%m-%d')
        # create a Toplevel window for the payment form
        self.getvalue_form = tk.Toplevel(self.master)

        # calculate the center coordinates of the screen
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        x = (screen_width / 2) - (300 / 2)  # 500 is the width of the Payment Form window
        y = (screen_height / 2) - (300 / 2)  # 500 is the height of the Payment Form window

        # set the position of the Payment Form window to center
        self.getvalue_form.geometry(f"600x400+{int(x)}+{int(y)}")
        self.getvalue_form.grid_rowconfigure(0, weight=1)
        self.getvalue_form.grid_rowconfigure(1, weight=1)
        self.getvalue_form.grid_rowconfigure(2, weight=1)
        self.getvalue_form.grid_rowconfigure(3, weight=1)
        self.getvalue_form.grid_rowconfigure(4, weight=1)
        self.getvalue_form.grid_rowconfigure(5, weight=1)
        self.getvalue_form.grid_rowconfigure(6, weight=1)
        self.getvalue_form.grid_rowconfigure(7, weight=1)
        self.getvalue_form.grid_columnconfigure(0, weight=1)
        self.getvalue_form.grid_columnconfigure(1, weight=1)
        
        self.getvalue_form.grid_columnconfigure(2, weight=1)
        
        self.getvalue_form.grid_columnconfigure(3, weight=1)
        self.getvalue_form.grid_columnconfigure(4, weight=1)
        
        self.getvalue_form.grid_columnconfigure(5, weight=1)
        self.getvalue_form.grid_columnconfigure(6, weight=1)


        self.strt_calander = calander_entry(self.getvalue_form, str(from_date))
        self.end_calander = calander_entry(self.getvalue_form, str(to_date))

        self.lable0 = tk.Label(self.getvalue_form, text="Period")
        self.lable0.grid(row=0, column=2, columnspan=3, sticky="nsew")#3
        self.got_date = tk.Label(self.getvalue_form, text=str(self.strt_calander.selected_dmd) + "-" + str(self.strt_calander.selected_dmd))
        self.got_date.grid(row=1, column=2, columnspan=3, sticky="nsew")#3

        self.lable1 = tk.Label(self.getvalue_form, text="Strat")
        self.lable1.grid(row=2, column=0, columnspan=2, sticky="nsew")#2
        self.lable2 = tk.Label(self.getvalue_form, text="End")
        self.lable2.grid(row=2, column=3, columnspan=2, sticky="nsew")#2

        self.lable3 = tk.Label(self.getvalue_form, text="Predefined Period")
        self.lable3.grid(row=2, column=5, columnspan=2, sticky="nsew") # 2
        
        # calanders
        
        self.end_calander.grid(row=3, column=3, columnspan=2, rowspan=5, sticky="nsew")
        self.strt_calander.grid(row=3, column=0, columnspan=2, rowspan=5, sticky="nsew")
        self.end_calander.var.trace('w', lambda *_:self.changed())
        self.strt_calander.var.trace('w', lambda *_: self.changed())
        #

        self.Today_button = tk.Button(self.getvalue_form, text="Today", font=("Arial", 12), command= lambda:self.saved_pariods("Today"))
        self.Today_button.grid(row=3, column=5, sticky="nsew")
        self.Yesterday_button = tk.Button(self.getvalue_form, text="Yesterday", font=("Arial", 12), command=lambda:self.saved_pariods("Yesterday"))
        self.Yesterday_button.grid(row=3, column=6, sticky="nsew")

        self.This_Week_button = tk.Button(self.getvalue_form, text="This Week", font=("Arial", 12), command=lambda:self.saved_pariods("This Week"))
        self.This_Week_button.grid(row=4, column=5, sticky="nsew")
        self.Last_Week_button = tk.Button(self.getvalue_form, text="Last Week", font=("Arial", 12), command=lambda:self.saved_pariods("Last Week"))
        self.Last_Week_button.grid(row=4, column=6, sticky="nsew")

        self.This_Month_button = tk.Button(self.getvalue_form, text="This Month", font=("Arial", 12), command=lambda:self.saved_pariods("This Month"))
        self.This_Month_button.grid(row=5, column=5, sticky="nsew")
        self.Last_Month_button = tk.Button(self.getvalue_form, text="Last Month", font=("Arial", 12), command=lambda:self.saved_pariods("Last Month"))
        self.Last_Month_button.grid(row=5, column=6, sticky="nsew")

        self.This_Year_button = tk.Button(self.getvalue_form, text="This Year", font=("Arial", 12), command=lambda:self.saved_pariods("This Year"))
        self.This_Year_button.grid(row=6, column=5, sticky="nsew")
        self.Last_Year_button = tk.Button(self.getvalue_form, text="Last Year", font=("Arial", 12), command=lambda:self.saved_pariods("Last Year"))
        self.Last_Year_button.grid(row=6, column=6, sticky="nsew")

        self.Ok_button = tk.Button(self.getvalue_form, text="Ok", font=("Arial", 12), command=self.run)
        self.Ok_button.grid(row=7, column=5, sticky="nsew")
        self.Cancel_button = tk.Button(self.getvalue_form, text="Cancel", font=("Arial", 12), command=lambda : self.getvalue_form.destroy())
        self.Cancel_button.grid(row=7, column=6, sticky="nsew")


        # show the Payment Form window
        self.getvalue_form.transient(self.master)
        self.getvalue_form.grab_set()
        self.getvalue_form.focus_set()
        #self.getvalue_form.bind("<KeyPress>", lambda event: self.add_num(event, ""))
        self.getvalue_form.transient(self.master)
        self.master.wait_window(self.getvalue_form)

    def changed(self):
        self.start_value = self.strt_calander.selected_dmd
        self.end_value = self.end_calander.selected_dmd
        self.got_date.config(text=str(self.strt_calander.selected_dmd) + "-" + str(self.end_calander.selected_dmd))
        
    def run(self):
        self.start_value = self.strt_calander.selected_dmd
        self.end_value = self.end_calander.selected_dmd
        self.getvalue_form.destroy()
        
    def saved_pariods(self, change):
        if change == "Today":
            self.strt_calander.go_to("Today")
            self.end_calander.go_to("Today")
        if change == "Yesterday":
            self.strt_calander.go_to("Yesterday")
            self.end_calander.go_to("Yesterday")
        if change == "This Week":
            self.strt_calander.go_to("Start This Week")
            self.end_calander.go_to("End This Week")
        if change == "Last Week":
            self.strt_calander.go_to("Start Last Week")
            self.end_calander.go_to("End Last Week")
        if change == "This Month":
            self.strt_calander.go_to("Start This Month")
            self.end_calander.go_to("End This Month")
        if change == "Last Month":
            self.strt_calander.go_to("Start Last Month")
            self.end_calander.go_to("End Last Month")
        if change == "This Year":
            self.strt_calander.go_to("Start This Year")
            self.end_calander.go_to("End This Year")
        if change == "Last Year":
            self.strt_calander.go_to("Start Last Year")
            self.end_calander.go_to("End Last Year")
            
    def add_num(self, event, text):
        # Get the current value of the Entry widget
        current_value = self.include_var.get()
        if event and text == "":
            text = event.keysym
        print("text : " + str(text))

        if text in ["clean", "Escape"]:
            # Clear the Entry widget
            if not self.include_var.get() == "":
                self.include_var.set("")
                self.get_amount_entry.delete(0, 'end')
            elif text == "Escape":
                self.getvalue_form.destroy()
        elif text == "BackSpace":
            self.get_amount_entry.delete(len(self.get_amount_entry.get())-1, 'end')
        elif text == "":
            # Do nothing if the button is "+", "-", "0", ".", or "enter"
            pass
        elif text in ["Return", "KP_Enter", "enter"]:
            try:
                # Attempt to convert the current value to a float
                self.value = float(current_value)
                # Call the give_value method to set self.vv and destroy the Toplevel window
                self.getvalue_form.destroy()
            except ValueError:
                # If the current value cannot be converted to a float, do nothing
                pass
        elif "." in current_value and text == ".":
            # Do nothing if the current value already contains a decimal point
            pass
        else:
            # Append the button text to the current value of the Entry widget
            self.include_var.set(current_value + text)
