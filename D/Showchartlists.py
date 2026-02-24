import tkinter as tk
from tkinter import ttk
import sqlite3, os

from C.API.Get import *
from C.API.API import *
from C.API.Set import *

data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data'))
db_path = os.path.join(data_dir, 'my_database.db')
class ShowchartForm(tk.Tk):
    def __init__(self, master):
        self.master = master
        self.value = self.master.chart_index
        
        # create a Toplevel window for the chart list form
        self.chart_list_form = tk.Toplevel(self.master)
        self.chart_list_form.title("Chart List Form ~ " + str(self.master.chart_index))

        # calculate the center coordinates of the screen
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        x = (screen_width / 2) - (300 / 2)  # 300 is the width of the chart list form window
        y = (screen_height / 2) - (400 / 2)  # 400 is the height of the chart list form window

        # set the position of the chart list form window to center
        self.chart_list_form.geometry(f"600x400+{int(x)}+{int(y)}")
        self.chart_list_form.grid_rowconfigure(0, weight=1)
        self.chart_list_form.grid_columnconfigure(0, weight=1)

        self.include_var = tk.StringVar()
        self.chart_list = tk.Listbox(self.chart_list_form, listvariable=self.include_var, width=25, font=("Arial", 12))
        self.chart_list.grid(row=0, column=0, sticky="nsew")

        # retrieve chart data from the database
        chart_data = fetch_as_dict_list("SELECT * FROM pre_doc_table", ())
        for chart in chart_data:
            print('chart: ', chart)
            self.chart_list.insert("end", [chart['id'], chart['PRICE'], chart['exitems_doc_barcode'], chart['doc_created_date']])  # assuming chart name is stored in second column

        self.select_button = tk.Button(self.chart_list_form, text="Select", font=("Arial", 12), command=self.select_chart)
        self.select_button.grid(row=1, column=0, sticky="nsew")

        self.delete_selected_button = tk.Button(self.chart_list_form, text="Delete Selected", font=("Arial", 12), command=self.delete_selected)
        self.delete_selected_button.grid(row=2, column=0, sticky="nsew")

        self.delete_all_button = tk.Button(self.chart_list_form, text="Delete All", font=("Arial", 12), command=self.delete_all)
        self.delete_all_button.grid(row=3, column=0, sticky="nsew")

        self.close_button = tk.Button(self.chart_list_form, text="Close", font=("Arial", 12), command=self.chart_list_form.destroy)
        self.close_button.grid(row=4, column=0, sticky="nsew")

        # show the chart list form window
        self.chart_list_form.transient(self.master)
        self.chart_list_form.grab_set()
        self.master.wait_window(self.chart_list_form)

    def select_chart(self):
        # retrieve the selected chart name from the Listbox
        selection = self.chart_list.curselection()
        if selection:
            self.value = selection[0]
            # do something with the selected chart name, e.g. pass it to another function or update a variable
            
            print("Selected chart:", str(self.value))
            self.chart_list_form.destroy()
        else:
            print("No chart selected.")

    def delete_selected(self):
        # retrieve the selected chart name from the Listbox
        selection = self.chart_list.curselection()
        if selection:
            chart_name = self.chart_list.get(selection[0])[0]
            # delete the selected chart from the Listbox
            self.chart_list.delete(selection[0])
            # delete the selected chart from the database
            Update_table_database("DELETE FROM pre_doc_table WHERE id = ?", (chart_name,))
        else:
            print("No chart selected.")

    def delete_all(self):
        # delete all charts from the Listbox
        self.chart_list.delete(0, "end")
        # delete all charts from the database
        Update_table_database("DELETE FROM pre_doc_table")
