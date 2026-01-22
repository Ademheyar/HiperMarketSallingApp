import tkinter as tk
from tkinter import ttk
import sqlite3
import os
import sys
current_dir = os.path.abspath(os.path.dirname(__file__))
MAIN_dir = os.path.join(current_dir, '..')
sys.path.append(MAIN_dir)
from D.ItemSelector import ItemSelectorWidget
import os



data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data'))
db_path = os.path.join(data_dir, 'my_database.db')
conn = sqlite3.connect(db_path)


import datetime

class calander_entry(tk.Frame):
    def __init__(self, master, date):
        tk.Frame.__init__(self, master)
        self.var = tk.StringVar()
        self.fdmd = date.split("-")
        self.dmd = date.split("-")
        self.selected_dmd = date.split("-")
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure(3, weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)

        self.next_button = tk.Button(self, text="<<", font=("Arial", 12), command=self.get_prev)
        self.next_button.grid(row=0, column=0, sticky="nsew")
        self.year_month_label = tk.Label(self, text=str(self.dmd[0] + "-"+self.dmd[1]))
        self.year_month_label.grid(row=0, column=1, columnspan=2, sticky="nsew")
        self.prev_button = tk.Button(self, text=">>", font=("Arial", 12), command=self.get_next)
        self.prev_button.grid(row=0, column=3, sticky="nsew")
        
        self.day_list_frame = tk.Frame(self)
        self.day_list_frame.grid(row=1, column=0, columnspan=4, sticky="nsew")

        self.list_days()   
        '''self.bind("<Up>", self.treeview_naigation)
        self.bind("<Down>", self.treeview_naigation)
        self.bind("<Return>", self.select)
        self.bind("<Escape>", lambda _: self.var.set(''))'''

    def get_days(self):
        year = int(self.dmd[0])
        days_in_month = {
            1: 31,
            2: 29 if year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)else 28,
            3: 31, 4: 30, 5: 31, 6: 30, 7: 31, 8: 31, 9: 30, 10: 31, 11: 30, 12: 31, 
            }
        return list(range(1, days_in_month[int(self.dmd[1])] +1))
    def list_days(self):
        days = self.get_days()
        #
        for chiled in self.day_list_frame.winfo_children():
            chiled.destroy()
        x, y = 0, 0
        
        self.day_list_frame.grid_columnconfigure(0, weight=0)
        self.day_list_frame.grid_rowconfigure(0, weight=0)
        for day in days:
            btn = tk.Button(self.day_list_frame, text=str(day), font=("Arial", 12), command= lambda a=day: self.select_day(a))
            btn.grid(column=x, row=y, sticky="nsew")
            if int(self.selected_dmd[0]) == int(self.dmd[0]) and int(self.selected_dmd[1]) == int(self.dmd[1]) and day == int(self.selected_dmd[2]):
                btn.config(bg="blue")
            if x + 1 > 5:
                x = 0
                y += 1
                self.day_list_frame.grid_columnconfigure(x, weight=0)
                self.day_list_frame.grid_rowconfigure(y, weight=0)
            else:
                x += 1
                self.day_list_frame.grid_columnconfigure(x, weight=0)
                
    def select_day(self, day):
        self.dmd[2]=day
        print("selected : "+str(self.var))
        self.selected_dmd[0] = self.dmd[0]
        self.selected_dmd[1] = self.dmd[1]
        self.selected_dmd[2] = self.dmd[2]
        self.var.set(str(day))
        self.list_days()
        
    def go_to(self, do_):
        if do_ == "Today":
            self.dmd[0]=str(self.fdmd[0])
            self.dmd[1]=str(self.fdmd[1])
            self.dmd[2]=str(self.fdmd[2])
        elif do_ == "Yesterday":
            self.dmd[0]=str(self.fdmd[0])
            if int(self.fdmd[2])-1 <= 0:
                self.dmd[1]=str(int(self.fdmd[1])-1)
                if int(self.fdmd[1])-1 <= 0:
                    self.dmd[1]="12"
                    self.dmd[0]=str(int(self.fdmd[0])-1)
                g=self.get_days()
                self.dmd[2]=str(g[len(g)-1])
            else:
                self.dmd[1]=str(self.fdmd[1])
                self.dmd[2]=str(int(self.fdmd[2])-1)
                
            self.dmd[0]=str(int(self.fdmd[0]))
            self.dmd[1]=str(int(self.fdmd[1]))
            self.dmd[2]=str(int(self.fdmd[2])-1)
        elif do_ == 'Start This Week':
            self.dmd[0]=str(self.fdmd[0])
            if int(self.fdmd[2])-7 <= 0:
                d = 7-int(self.fdmd[2])
                self.dmd[1]=str(int(self.fdmd[1])-1)
                if int(self.fdmd[1])-1 <= 0:
                    self.dmd[1]="12"
                    self.dmd[0]=str(int(self.fdmd[0])-1)
                g=self.get_days()
                self.dmd[2]=str(g[len(g)-1]-d)
            else:
                self.dmd[1]=str(self.fdmd[1])
                self.dmd[2]=str(int(self.fdmd[2])-7)
        elif do_ == 'End This Week':
            self.dmd[0]=str(self.fdmd[0])
            self.dmd[0]=str(self.fdmd[1])
            self.dmd[0]=str(self.fdmd[2])
        elif do_ == 'Start Last Week':
            self.dmd[0]=str(self.fdmd[0])
            if int(self.fdmd[2])-14 <= 0:
                d = 14-int(self.fdmd[2])
                self.dmd[1]=str(int(self.fdmd[1])-1)
                if int(self.fdmd[1])-1 <= 0:
                    self.dmd[1]="12"
                    self.dmd[0]=str(int(self.fdmd[0])-1)
                g=self.get_days()
                self.dmd[2]=str(g[len(g)-1]-d)
            else:
                self.dmd[1]=str(self.fdmd[1])
                self.dmd[2]=str(int(self.fdmd[2])-14)
        elif do_ == 'End Last Week':
            self.dmd[0]=str(self.fdmd[0])
            self.dmd[0]=str(self.fdmd[1])
            self.dmd[0]=str(self.fdmd[2])
            return
        elif do_ == 'Start This Month':
            self.dmd[0]=str(self.fdmd[0])
            self.dmd[1]=str(self.fdmd[1])
            self.dmd[2]="1"
        elif do_ == 'End This Month':
            self.dmd[0]=str(self.fdmd[0])
            self.dmd[1]=str(self.fdmd[1])
            g=self.get_days()
            self.dmd[2]=str(g[len(g)-1])
        elif do_ == 'Start Last Month':
            self.dmd[0]=str(self.fdmd[0])
            self.dmd[1]=str(int(self.fdmd[1])-1)
            g=self.get_days()
            self.dmd[2]="1"
        elif do_ == 'End Last Month':
            self.dmd[0]=str(self.fdmd[0])
            self.dmd[1]=str(int(self.fdmd[1])-1)
            g=self.get_days()
            self.dmd[2]=str(g[len(g)-1])
        elif do_ == 'Start This Year':
            self.dmd[0]=str(self.fdmd[0])
            self.dmd[1]="1"
            self.dmd[2]="1"
        elif do_ == 'End This Year':
            self.dmd[0]=str(self.fdmd[0])
            self.dmd[1]="12"
            g=self.get_days()
            self.dmd[2]=str(g[len(g)-1])
        elif do_ == 'Start Last Year':
            self.dmd[0]=str(int(self.fdmd[0])-1)
            self.dmd[1]="1"
            self.dmd[2]="1"
        elif do_ == 'End Last Year':
            self.dmd[0]=str(int(self.fdmd[0])-1)
            self.dmd[1]="12"
            g=self.get_days()
            self.dmd[2]=str(g[len(g)-1])
        self.selected_dmd[0] = self.dmd[0]
        self.selected_dmd[1] = self.dmd[1]
        self.selected_dmd[2] = self.dmd[2]
        self.var.set(str(self.dmd[2]))
        self.year_month_label.config(text=str(self.dmd[0] + "-"+self.dmd[1]))
        self.list_days()
        
    def get_next(self):
        if int(self.dmd[1]) + 1 > 12:
            self.dmd[0]=str(int(self.dmd[0]) + 1)
            self.dmd[1]=str("1")
        else:
            self.dmd[1]=str(int(self.dmd[1]) + 1)
        self.year_month_label.config(text=str(self.dmd[0] + "-"+self.dmd[1]))
        self.list_days()
        
    def get_prev(self):
        if int(self.dmd[1]) - 1 <= 0:
            self.dmd[0]=str(int(self.dmd[0]) -1)
            self.dmd[1]=str("12")
        else:
            self.dmd[1]=str(int(self.dmd[1]) -1)
        self.year_month_label.config(text=str(self.dmd[0] + "-"+self.dmd[1]))
        self.list_days()


