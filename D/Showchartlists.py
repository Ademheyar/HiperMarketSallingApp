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
        
        # Color scheme
        self.bg_dark = "#0d47a1"      # Deep blue
        self.bg_light = "#1565c0"     # Darker blue
        self.accent_blue = "#1976d2"  # Medium blue
        self.text_light = "#ffffff"   # White text
        self.bg_darker = "#0a3d91"    # Even darker blue
        self.button_style = {"font": ("Arial", 11, "bold"), "bg": self.accent_blue, "fg": self.text_light, "activebackground": self.bg_light, "activeforeground": self.text_light, "relief": tk.FLAT, "bd": 0}
        
        # create a Toplevel window for the chart list form
        self.chart_list_form = tk.Toplevel(self.master)
        self.chart_list_form.title("Chart List Form ~ " + str(self.master.chart_index))
        self.chart_list_form.configure(bg=self.bg_dark)

        # calculate the center coordinates of the screen
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        x = (screen_width / 2) - (600 / 2)
        y = (screen_height / 2) - (400 / 2)

        # set the position of the chart list form window to center
        self.chart_list_form.geometry(f"600x400+{int(x)}+{int(y)}")
        self.chart_list_form.grid_rowconfigure(0, weight=1)
        self.chart_list_form.grid_columnconfigure(0, weight=1)

        # Title label
        title_label = tk.Label(self.chart_list_form, text="Charts List", font=("Arial", 14, "bold"), 
                              bg=self.bg_dark, fg=self.text_light)
        title_label.grid(row=0, column=0, sticky="ew", padx=10, pady=10)

        # Listbox container frame
        list_frame = tk.Frame(self.chart_list_form, bg=self.bg_light)
        list_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=5)
        self.chart_list_form.grid_rowconfigure(1, weight=1)

        self.include_var = tk.StringVar()
        self.chart_list = tk.Listbox(list_frame, listvariable=self.include_var, width=70, font=("Arial", 10),
                                    bg=self.bg_darker, fg=self.text_light, selectmode=tk.SINGLE, 
                                    highlightthickness=0, bd=0)
        self.chart_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Scrollbar for listbox
        scrollbar = tk.Scrollbar(list_frame, bg=self.bg_light, activebackground=self.accent_blue)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.chart_list.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.chart_list.yview)

        # retrieve chart data from the database
        chart_data = fetch_as_dict_list("SELECT * FROM pre_doc_table", ())
        for chart in chart_data:
            print('chart: ', chart)
            chart_info = f"ID: {chart['id']} | Price: {chart['PRICE']} | Barcode: {chart['exitems_doc_barcode']} | Date: {chart['doc_created_date']}"
            self.chart_list.insert("end", chart_info)

        # Buttons frame
        buttons_frame = tk.Frame(self.chart_list_form, bg=self.bg_dark)
        buttons_frame.grid(row=2, column=0, sticky="ew", padx=10, pady=10)
        buttons_frame.columnconfigure((0, 1, 2, 3), weight=1)

        self.select_button = tk.Button(buttons_frame, text="Select", command=self.select_chart, **self.button_style)
        self.select_button.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        self.delete_selected_button = tk.Button(buttons_frame, text="Delete Selected", command=self.delete_selected, **self.button_style)
        self.delete_selected_button.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)

        self.delete_all_button = tk.Button(buttons_frame, text="Delete All", command=self.delete_all, **self.button_style)
        self.delete_all_button.grid(row=0, column=2, sticky="nsew", padx=5, pady=5)

        self.close_button = tk.Button(buttons_frame, text="Close", command=self.chart_list_form.destroy, **self.button_style)
        self.close_button.grid(row=0, column=3, sticky="nsew", padx=5, pady=5)

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
