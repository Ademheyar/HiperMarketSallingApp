import tkinter as tk
from tkinter import ttk
import sqlite3, os, sys
import datetime

data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data'))
db_path = os.path.join(data_dir, 'my_database.db')

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
        
        # Android-style dark blue color scheme
        self.bg_dark = "#0d47a1"      # Deep blue
        self.bg_light = "#1565c0"     # Darker blue
        self.accent_blue = "#1976d2"  # Medium blue
        self.text_light = "#ffffff"   # White text
        self.bg_darker = "#0a3d91"    # Even darker blue
        
        # create a Toplevel window for the payment form
        self.getvalue_form = tk.Toplevel(self.master)
        self.getvalue_form.configure(bg=self.bg_dark)

        # calculate the center coordinates of the screen
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        x = (screen_width / 2) - (300 / 2)
        y = (screen_height / 2) - (300 / 2)

        # set the position of the Payment Form window to center
        self.getvalue_form.geometry(f"600x400+{int(x)}+{int(y)}")
        for i in range(8):
            self.getvalue_form.grid_rowconfigure(i, weight=1)
        for i in range(7):
            self.getvalue_form.grid_columnconfigure(i, weight=1)

        self.strt_calander = calander_entry(self.getvalue_form, str(from_date))
        self.end_calander = calander_entry(self.getvalue_form, str(to_date))

        self.lable0 = tk.Label(self.getvalue_form, text="Period", bg=self.bg_dark, fg=self.text_light, font=("Arial", 14, "bold"))
        self.lable0.grid(row=0, column=2, columnspan=3, sticky="nsew", padx=5, pady=5)
        
        self.got_date = tk.Label(self.getvalue_form, text=f"{self.strt_calander.selected_dmd[0] + '-'+self.strt_calander.selected_dmd[1]+'-'+self.strt_calander.selected_dmd[2]} → {self.end_calander.selected_dmd[0] + '-'+self.end_calander.selected_dmd[1]+'-'+self.end_calander.selected_dmd[2]}", bg=self.bg_light, fg=self.text_light, font=("Arial", 12, "bold"))
        self.got_date.grid(row=1, column=2, columnspan=3, sticky="nsew", padx=5, pady=5)

        self.lable1 = tk.Label(self.getvalue_form, text="Start", bg=self.bg_dark, fg=self.text_light, font=("Arial", 12, "bold"))
        self.lable1.grid(row=2, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)
        
        self.lable2 = tk.Label(self.getvalue_form, text="End", bg=self.bg_dark, fg=self.text_light, font=("Arial", 12, "bold"))
        self.lable2.grid(row=2, column=3, columnspan=2, sticky="nsew", padx=5, pady=5)

        self.lable3 = tk.Label(self.getvalue_form, text="Predefined Period", bg=self.bg_dark, fg=self.text_light, font=("Arial", 12, "bold"))
        self.lable3.grid(row=2, column=5, columnspan=2, sticky="nsew", padx=5, pady=5)
        
        self.end_calander.grid(row=3, column=3, columnspan=2, rowspan=5, sticky="nsew", padx=5, pady=5)
        self.strt_calander.grid(row=3, column=0, columnspan=2, rowspan=5, sticky="nsew", padx=5, pady=5)
        self.end_calander.var.trace('w', lambda *_:self.changed())
        self.strt_calander.var.trace('w', lambda *_: self.changed())

        button_style = {"font": ("Arial", 11, "bold"), "bg": self.accent_blue, "fg": self.text_light, "activebackground": self.bg_light, "activeforeground": self.text_light, "relief": tk.FLAT, "bd": 0}
        
        self.Today_button = tk.Button(self.getvalue_form, text="Today", command=lambda:self.saved_pariods("Today"), **button_style)
        self.Today_button.grid(row=3, column=5, sticky="nsew", padx=3, pady=3)
        
        self.Yesterday_button = tk.Button(self.getvalue_form, text="Yesterday", command=lambda:self.saved_pariods("Yesterday"), **button_style)
        self.Yesterday_button.grid(row=3, column=6, sticky="nsew", padx=3, pady=3)

        self.This_Week_button = tk.Button(self.getvalue_form, text="This Week", command=lambda:self.saved_pariods("This Week"), **button_style)
        self.This_Week_button.grid(row=4, column=5, sticky="nsew", padx=3, pady=3)
        
        self.Last_Week_button = tk.Button(self.getvalue_form, text="Last Week", command=lambda:self.saved_pariods("Last Week"), **button_style)
        self.Last_Week_button.grid(row=4, column=6, sticky="nsew", padx=3, pady=3)

        self.This_Month_button = tk.Button(self.getvalue_form, text="This Month", command=lambda:self.saved_pariods("This Month"), **button_style)
        self.This_Month_button.grid(row=5, column=5, sticky="nsew", padx=3, pady=3)
        
        self.Last_Month_button = tk.Button(self.getvalue_form, text="Last Month", command=lambda:self.saved_pariods("Last Month"), **button_style)
        self.Last_Month_button.grid(row=5, column=6, sticky="nsew", padx=3, pady=3)

        self.This_Year_button = tk.Button(self.getvalue_form, text="This Year", command=lambda:self.saved_pariods("This Year"), **button_style)
        self.This_Year_button.grid(row=6, column=5, sticky="nsew", padx=3, pady=3)
        
        self.Last_Year_button = tk.Button(self.getvalue_form, text="Last Year", command=lambda:self.saved_pariods("Last Year"), **button_style)
        self.Last_Year_button.grid(row=6, column=6, sticky="nsew", padx=3, pady=3)

        action_button_style = {"font": ("Arial", 12, "bold"), "fg": self.text_light, "activeforeground": self.text_light, "relief": tk.FLAT, "bd": 0}
        
        self.Ok_button = tk.Button(self.getvalue_form, text="Ok", command=self.run, bg=self.bg_light, **action_button_style)
        self.Ok_button.grid(row=7, column=5, sticky="nsew", padx=3, pady=3)
        
        self.Cancel_button = tk.Button(self.getvalue_form, text="Cancel", command=lambda : self.getvalue_form.destroy(), bg=self.bg_darker, **action_button_style)
        self.Cancel_button.grid(row=7, column=6, sticky="nsew", padx=3, pady=3)

        self.getvalue_form.transient(self.master)
        self.getvalue_form.grab_set()
        self.getvalue_form.focus_set()
        self.master.wait_window(self.getvalue_form)

    def changed(self):
        self.start_value = self.strt_calander.selected_dmd
        
        if int(self.strt_calander.selected_dmd[0]) > int(self.end_calander.selected_dmd[0]):
            self.end_calander.selected_dmd[0] == int(self.strt_calander.selected_dmd[0])
        if int(self.strt_calander.selected_dmd[1]) > int(self.end_calander.selected_dmd[1]):
            self.end_calander.selected_dmd[1] == int(self.strt_calander.selected_dmd[1])
        if int(self.strt_calander.selected_dmd[2]) > int(self.end_calander.selected_dmd[2]):
            self.end_calander.selected_dmd[2] == int(self.strt_calander.selected_dmd[2])
            
        self.end_value = self.end_calander.selected_dmd 

        if int(self.end_calander.selected_dmd[0]) < int(self.strt_calander.selected_dmd[0]):
            self.strt_calander.selected_dmd[0] == self.end_calander.selected_dmd[0]
        if int(self.end_calander.selected_dmd[1]) < int(self.strt_calander.selected_dmd[1]):
            self.strt_calander.selected_dmd[1] == self.end_calander.selected_dmd[1]
        if int(self.end_calander.selected_dmd[2]) < int(self.strt_calander.selected_dmd[2]):
            self.strt_calander.selected_dmd[2] == self.end_calander.selected_dmd[2]

        self.got_date.config(text=f"{str(self.strt_calander.selected_dmd[0]) + '-'+str(self.strt_calander.selected_dmd[1])+'-'+str(self.strt_calander.selected_dmd[2])} → {str(self.end_calander.selected_dmd[0]) + '-'+str(self.end_calander.selected_dmd[1])+'-'+str(self.end_calander.selected_dmd[2])}")
        
    def run(self):
        self.start_value = self.strt_calander.selected_dmd
        self.end_value = self.end_calander.selected_dmd
        self.getvalue_form.destroy()
        
    def saved_pariods(self, change):
        periods = {
            "Today": ("Today", "Today"),
            "Yesterday": ("Yesterday", "Yesterday"),
            "This Week": ("Start This Week", "End This Week"),
            "Last Week": ("Start Last Week", "End Last Week"),
            "This Month": ("Start This Month", "End This Month"),
            "Last Month": ("Start Last Month", "End Last Month"),
            "This Year": ("Start This Year", "End This Year"),
            "Last Year": ("Start Last Year", "End Last Year"),
        }
        if change in periods:
            self.strt_calander.go_to(periods[change][0])
            self.end_calander.go_to(periods[change][1])
            
    def add_num(self, event, text):
        current_value = self.include_var.get()
        if event and text == "":
            text = event.keysym
        print("text : " + str(text))

        if text in ["clean", "Escape"]:
            if not self.include_var.get() == "":
                self.include_var.set("")
                self.get_amount_entry.delete(0, 'end')
            elif text == "Escape":
                self.getvalue_form.destroy()
        elif text == "BackSpace":
            self.get_amount_entry.delete(len(self.get_amount_entry.get())-1, 'end')
        elif text == "":
            pass
        elif text in ["Return", "KP_Enter", "enter"]:
            try:
                self.value = float(current_value)
                self.getvalue_form.destroy()
            except ValueError:
                pass
        elif "." in current_value and text == ".":
            pass
        else:
            self.include_var.set(current_value + text)
