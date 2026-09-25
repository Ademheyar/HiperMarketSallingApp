import tkinter as tk
from tkinter import ttk, filedialog
from PIL import Image, ImageTk
import os, shutil
import sqlite3
import shutil
import datetime
import atexit
import sys
import json

import datetime
import random

current_dir = os.path.abspath(os.path.dirname(__file__))
MAIN_dir = os.path.join(current_dir, '..')
sys.path.append(MAIN_dir)
from D.Getdefsize import ButtonEntryApp
from C.List import *

from C.API.Get import *
from D.searchbox import search_entry

# Connect to the database or create it if it does not exist

import os
data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data'))
db_path = os.path.join(data_dir, 'my_database.db')

import tkinter as tk
from D.Getdate import GetDateForm
from D.Chart.Chart import *

from C.Product.selecttype import *

from D.docediterform import DocEditForm

from C.API.Get import *
from C.API.API import *
from C.API.Set import *


def is_float(value):
    try:
        #print()
        float (value)
        return True
    except ValueError:
        return False

# Function to search for documents in the doc_table SQLite database table
def search_documents(doc_id=None, doc_type=None, doc_barcode=None, extension_barcode=None, 
                    item=None, user_id=None, customer_id=None, sold_item_info=None, discount=None, 
                    tax=None, doc_created_date=None, doc_expire_date=None, doc_updated_date=None):
    given = []
    # Build the SQL query based on the provided attributes
    query = 'SELECT * FROM doc_table WHERE 1=1'
    if doc_id is not None and doc_id is not '':
        query += f" AND id='{doc_id}'"
    if doc_type is not None and doc_type != '':
        query += f" AND type='{doc_type}'"
    if doc_barcode is not None and doc_barcode is not '':
        query += f" AND doc_barcode='{doc_barcode}'"
    if extension_barcode is not None and extension_barcode is not '':
        query += f" AND extension_barcode='{extension_barcode}'"
    if item is not None and item is not '':
        query += f" AND item LIKE ?"
        if given == None:
            given.append(f'%{item}%')
        else:
            given.append(f'%{item}%')
    if user_id is not None and user_id is not '':
        query += f" AND user_id='{user_id}'"
    if customer_id is not None and customer_id is not '':
        query += f" AND customer_id='{customer_id}'"
    if sold_item_info is not None and sold_item_info is not '':
        query += f" AND sold_item_info='{sold_item_info}'"
    if discount is not None and discount is not '':
        query += f" AND discount='{discount}'"
    if tax is not None and tax is not '':
        query += f" AND tax='{tax}'"
    if doc_created_date is not None and doc_created_date is not '':
        query += f" AND doc_created_date LIKE ?"
        if given == None:
            given.append(f'%{doc_created_date}%')
        else:
            given.append(f'%{doc_created_date}%')
    if doc_expire_date is not None and doc_expire_date is not '':
        query += f" AND doc_expire_date='{doc_expire_date}'"
    if doc_updated_date is not None and doc_updated_date is not '':
        query += f" AND doc_updated_date='{doc_updated_date}'"
    
    #print(query+"\n")
    # Execute the SQL query and return the results as a list of tuples
    Update_table_database(query, (*given,))
    results = cur.fetchall()
    return results
# Example node hierarchy

class ActionsForm(tk.Frame):
    def __init__(self, master, user, Shops, Shops_info):
        self.bg_dark = "#0d47a1"      # Deep blue
        self.bg_light = "#1565c0"     # Darker blue
        self.accent_blue = "#1976d2"  # Medium blue
        self.text_light = "#ffffff"   # White text
        self.bg_darker = "#0a3d91"    # Even darker blue
        self.button_style = {"font": ("Arial", 11, "bold"), "bg": self.accent_blue, "fg": self.text_light, "activebackground": self.bg_light, "activeforeground": self.text_light, "relief": tk.FLAT, "bd": 0}

        
        tk.Frame.__init__(self, master, bg=self.accent_blue)
        self.master = master
        
        self.user_info = user
        self.user = user
        self.Shops = Shops
        self.Shops_info = Shops_info
        self.Shop_Actions = []
        self.Action_code = "" # for comparing changing action if the code is changing
        self.Created_date = datetime.datetime.now().strftime('%Y-%m-%d')
        self.start_value = datetime.datetime.now().strftime('%Y-%m-%d')
        self.end_value = self.start_value
        
        self.Selected_Shop = ""
        
        self.homemaster = self
        p = 0
        while(True):
            p += 1
            #print("chacking parent p = " + str(p))
            if hasattr(self.homemaster, 'Shops_info') and hasattr(self.homemaster, 'onDisplayFrame'):
                break
            else:
                self.homemaster = self.homemaster.master
        #print("produ user : " + str(user))
        self.nested_list = []

        # Create the frame for the product details
        self.Actions_list_frame = tk.Frame(self, bg=self.accent_blue)
        self.Actions_list_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Create the search bar
        # Create the frame for the search bar and buttons
        self.search_frame = tk.Frame(self.Actions_list_frame, bg=self.accent_blue)
        self.search_frame.pack(side=tk.TOP, padx=5, pady=5)

        # create a StringVar to represent the search box
        self.search_var = tk.StringVar()
        self.search_entry = tk.Entry(self.search_frame, textvariable=self.search_var)
        self.search_entry.bind('<KeyRelease>', self.update_search_results)
        self.search_entry.pack(side=tk.LEFT, padx=5, pady=5)
            
        # bind the update_search_results function to the search box
        self.search_var.trace("w", self.update_search_results)
        
        self.add_new_button = tk.Button(self.search_frame, text='New Action', command=self.show_add_forme, **self.button_style)
        self.add_new_button.pack(side=tk.LEFT, padx=5, pady=5)
        self.change_button = tk.Button(self.search_frame, text='Change', command=self.show_change_forme, **self.button_style)
        self.change_button.pack(side=tk.LEFT, padx=5, pady=5)
        self.change_button.config(state=tk.DISABLED)
        self.delete_button = tk.Button(self.search_frame, text='Delete', command=self.delete_action, **self.button_style)
        self.delete_button.pack(side=tk.LEFT, padx=5, pady=5)
        self.refresh_button = tk.Button(self.search_frame, text='Refresh', command= lambda :self.update_search_results([None, None]), **self.button_style)
        self.refresh_button.pack(side=tk.LEFT, padx=5, pady=5)
        
        
        # Create the list box
        self.list_box = ttk.Treeview(self.Actions_list_frame)
        self.list_box.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.list_box.bind('<<TreeviewSelect>>', self.on_select)


        # Add vertical scrollbar
        tree_scrollbar_y = ttk.Scrollbar(self.list_box, orient='vertical', command=self.list_box.yview)
        self.list_box.configure(yscrollcommand=tree_scrollbar_y.set)
        tree_scrollbar_y.pack(side='right', fill='y')

        # Add horizontal scrollbar
        tree_scrollbar_x = ttk.Scrollbar(self.list_box, orient='horizontal', command=self.list_box.xview)
        self.list_box.configure(xscrollcommand=tree_scrollbar_x.set)
        tree_scrollbar_x.pack(side='bottom', fill='x')

        self.notebook_frame = ttk.Notebook(self.list_box)
        self.notebook_frame.pack_forget()
        
        # Create the frame for the product details
        self.details_frame = tk.Frame(self.notebook_frame, bg=self.accent_blue)
        self.details_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.notebook_frame.add(self.details_frame)

        self.Action_image = ""
        self.Action_image_frame = tk.Frame(self.details_frame, bg=self.accent_blue)
        self.Action_image_frame.grid(row=0, column=0, rowspan=3, sticky="nsew")

        self.Action_code_label = tk.Label(self.details_frame, text='Action Code : ', bg=self.accent_blue, fg=self.text_light)
        self.Action_code_label.grid(row=3, column=0, padx=5, pady=5, sticky=tk.E)
        
        self.Action_code_entry = tk.Entry(self.details_frame)
        self.Action_code_entry.grid(row=3, column=1, padx=5, pady=5, sticky=tk.W)
        
        self.Action_image_avatarlabel = tk.Label(self.Action_image_frame, bg=self.accent_blue, fg=self.text_light)
        self.Action_image_avatarlabel.pack(pady=10)
        self.Action_image_avatarlabel.bind("<Button-1>", lambda _: self.change_Action_image())
        
        # Create the widgets for the product details
        self.load_action_image()
            
        self.Action_label = tk.Label(self.details_frame, text='Action Label : ', bg=self.accent_blue, fg=self.text_light)
        self.Action_label.grid(row=4, column=0, padx=5, pady=5, sticky=tk.E)
        
        self.Action_label_entry = tk.Entry(self.details_frame)
        self.Action_label_entry.grid(row=4, column=1, padx=5, pady=5, sticky=tk.W)
        
        self.Action_created_date_label = tk.Label(self.details_frame, text='Action Created Date : '+self.start_value, bg=self.accent_blue, fg=self.text_light)
        self.Action_created_date_label.grid(row=5, column=0, columnspan=4, padx=5, pady=5, sticky=tk.W)
        
        self.From_Date_label = tk.Label(self.details_frame, text='From_Date:', bg=self.accent_blue, fg=self.text_light)
        self.From_Date_label.grid(row=6, column=0, padx=5, pady=5, sticky=tk.E)
        self.From_Date_entry = tk.Entry(self.details_frame)
        self.From_Date_entry.grid(row=6, column=1, padx=5, pady=5, sticky=tk.W)
        self.TO_Date_label = tk.Label(self.details_frame, text='TO_Date:', bg=self.accent_blue, fg=self.text_light)
        self.TO_Date_label.grid(row=6, column=2, padx=5, pady=5, sticky=tk.E)
        self.TO_Date_entry = tk.Entry(self.details_frame)
        self.TO_Date_entry.grid(row=6, column=3, padx=5, pady=5, sticky=tk.W)
        
        self.add_button = tk.Button(self.details_frame, text='Add', command=self.Save_Shop_Actions, **self.button_style)
        self.add_button.grid(row=26, column=0, padx=5, pady=5, sticky=tk.W)
        self.cancle_button = tk.Button(self.details_frame, text='Cancle', command=self.hide_add_forme, **self.button_style)
        self.cancle_button.grid(row=26, column=1, padx=5, pady=5, sticky=tk.W)
      
      
        
        # Create the frame for the product details
        self.ifdetails_frame = tk.Frame(self.notebook_frame, bg=self.accent_blue)
        self.ifdetails_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.ifdetails_frame.rowconfigure(0, weight=0)
        self.ifdetails_frame.rowconfigure(1, weight=1)
        self.ifdetails_frame.rowconfigure(2, weight=1)
        self.ifdetails_frame.rowconfigure(3, weight=1)
        self.ifdetails_frame.rowconfigure(4, weight=1)
        self.ifdetails_frame.rowconfigure(5, weight=1)
        self.ifdetails_frame.rowconfigure(6, weight=1)
        self.ifdetails_frame.rowconfigure(7, weight=1)
        self.ifdetails_frame.rowconfigure(8, weight=1)
        self.ifdetails_frame.rowconfigure(9, weight=1)
        
        self.ifdetails_frame.columnconfigure(0, weight=1)
        self.ifdetails_frame.columnconfigure(1, weight=1)
        self.ifdetails_frame.columnconfigure(2, weight=1)
        self.ifdetails_frame.columnconfigure(3, weight=1)
        self.ifdetails_frame.columnconfigure(4, weight=1)
        self.ifdetails_frame.columnconfigure(5, weight=1)
        self.notebook_frame.add(self.ifdetails_frame, text='If :')

        
        self.ifProduct_Make_price_label = tk.Label(self.ifdetails_frame, text='IF Total price : ', bg=self.accent_blue, fg=self.text_light)
        self.ifProduct_Make_price_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.E)
        self.ifProduct_Make_price_entry = tk.Entry(self.ifdetails_frame)
        self.ifProduct_Make_price_entry.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.ifProduct_Make_Total_price_label = tk.Label(self.ifdetails_frame, text='If Total Discount :', bg=self.accent_blue, fg=self.text_light)
        self.ifProduct_Make_Total_price_label.grid(row=0, column=1, padx=5, pady=5, sticky=tk.E)
        self.ifProduct_Make_Total_price_entry = tk.Entry(self.ifdetails_frame)
        self.ifProduct_Make_Total_price_entry.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)
        self.ifProduct_Make_Discount_label = tk.Label(self.ifdetails_frame, text='If Total Items QTY : ', bg=self.accent_blue, fg=self.text_light)
        self.ifProduct_Make_Discount_label.grid(row=0, column=2, padx=5, pady=5, sticky=tk.E)
        self.ifProduct_Make_Discount_entry = tk.Entry(self.ifdetails_frame)
        self.ifProduct_Make_Discount_entry.grid(row=1, column=2, padx=5, pady=5, sticky=tk.W)
        self.ifProduct_Make_Total_Disc_label = tk.Label(self.ifdetails_frame, text='If Total Profite : ', bg=self.accent_blue, fg=self.text_light)
        self.ifProduct_Make_Total_Disc_label.grid(row=0, column=3, padx=5, pady=5, sticky=tk.E)
        self.ifProduct_Make_Total_Disc_entry = tk.Entry(self.ifdetails_frame)
        self.ifProduct_Make_Total_Disc_entry.grid(row=1, column=3, padx=5, pady=5, sticky=tk.W)
        self.Add_None_ifitem_button = tk.Button(self.ifdetails_frame, text="None", command=lambda: DocEditForm.Create_Unowen_item(self), **self.button_style)
        self.Add_None_ifitem_button.grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)

        
        self.ifSelected_items = []
        # Create a label and an entry widget for the search box
        self.search_entry = search_entry(self.ifdetails_frame, self.Shops_info, self.user, self.Shops, font=("Arial", 12))
        #tk.Entry
        self.search_entry.grid(row=4, column=0, columnspan=6, sticky="nsew")
        
        # * New frame next to list_items in the main frame
        self.ifmidel_frame = tk.Frame(self.ifdetails_frame, bg=self.accent_blue)
        self.ifmidel_frame.grid(row=3, column=0, columnspan=10, rowspan=7, sticky="nsew")
        
        self.ifFrame_contaner_frame = tk.Frame(self.ifmidel_frame, bg=self.accent_blue)
        self.ifFrame_contaner_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.ifList_Frame_contaner_frame = tk.Frame(self.ifFrame_contaner_frame, bg=self.accent_blue)
        self.ifList_Frame_contaner_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.ifList_Frame = tk.Frame(self.ifList_Frame_contaner_frame, bg=self.accent_blue)
        self.ifList_Frame.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        
        self.ifitem_List_canvas = tk.Canvas(self.ifList_Frame, bg=self.accent_blue)
        self.ifitem_List_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        
        self.ifitem_List_yscrollbar = tk.Scrollbar(self.ifList_Frame, orient='vertical', command=self.ifitem_List_canvas.yview)
        self.ifitem_List_yscrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.ifitem_List_xscrollbar = tk.Scrollbar(self.ifList_Frame_contaner_frame, orient='horizontal', command=self.ifitem_List_canvas.xview)
        self.ifitem_List_xscrollbar.pack(side=tk.TOP, fill=tk.X)
        
        self.ifitem_List_canvas.configure(xscrollcommand=self.ifitem_List_xscrollbar.set, yscrollcommand=self.ifitem_List_yscrollbar.set)
        #self.New_item_contener_canvas.bind('<Configure>', lambda e: self.New_item_contener_canvas.configure(scrollregion=self.New_item_contener_canvas.bbox("all")))

        self.ifSelected_item_Display_frame = tk.Frame(self.ifitem_List_canvas, bg=self.accent_blue)
        self.ifitem_List_canvas.create_window((0, 0), window=self.ifSelected_item_Display_frame, anchor=tk.NW)
        self.ifSelected_item_Display_frame.bind('<Configure>', lambda e: self.ifitem_List_canvas.configure(scrollregion=self.ifitem_List_canvas.bbox("all")))
        

        # Create the frame for the product details
        self.Dodetails_frame = tk.Frame(self.notebook_frame, bg=self.accent_blue)
        self.Dodetails_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.Dodetails_frame.rowconfigure(0, weight=0)
        self.Dodetails_frame.rowconfigure(1, weight=1)
        self.Dodetails_frame.rowconfigure(2, weight=1)
        self.Dodetails_frame.rowconfigure(3, weight=1)
        self.Dodetails_frame.rowconfigure(4, weight=1)
        self.Dodetails_frame.rowconfigure(5, weight=1)
        self.Dodetails_frame.rowconfigure(6, weight=1)
        self.Dodetails_frame.rowconfigure(7, weight=1)
        self.Dodetails_frame.rowconfigure(8, weight=1)
        self.Dodetails_frame.rowconfigure(9, weight=1)
        
        self.Dodetails_frame.columnconfigure(0, weight=1)
        self.Dodetails_frame.columnconfigure(1, weight=1)
        self.Dodetails_frame.columnconfigure(2, weight=1)
        self.Dodetails_frame.columnconfigure(3, weight=1)
        self.Dodetails_frame.columnconfigure(4, weight=1)
        self.Dodetails_frame.columnconfigure(5, weight=1)
        self.notebook_frame.add(self.Dodetails_frame, text='Do :')        
        
        self.doProduct_Make_price_label = tk.Label(self.Dodetails_frame, text='Make Total price : ', bg=self.accent_blue, fg=self.text_light)
        self.doProduct_Make_price_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.E)
        self.doProduct_Make_price_entry = tk.Entry(self.Dodetails_frame)
        self.doProduct_Make_price_entry.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.doProduct_Make_Total_price_label = tk.Label(self.Dodetails_frame, text='Make Total Discount :', bg=self.accent_blue, fg=self.text_light)
        self.doProduct_Make_Total_price_label.grid(row=0, column=1, padx=5, pady=5, sticky=tk.E)
        self.doProduct_Make_Total_price_entry = tk.Entry(self.Dodetails_frame)
        self.doProduct_Make_Total_price_entry.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)
        self.Add_None_doitem_button = tk.Button(self.Dodetails_frame, text="None", command=lambda: DocEditForm.Create_Unowen_item(self), **self.button_style)
        self.Add_None_doitem_button.grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        
        # Create a label and an entry widget for the search box
        self.Dosearch_entry = search_entry(self.Dodetails_frame, self.Shops_info, self.user, self.Shops, font=("Arial", 12))
        #tk.Entry
        self.Dosearch_entry.grid(row=3, column=0, columnspan=6, sticky="nsew")


        self.doSelected_items = []
        # * New frame next to list_items in the main frame
        self.domidel_frame = tk.Frame(self.Dodetails_frame, bg=self.accent_blue)
        self.domidel_frame.grid(row=4, column=0, columnspan=10, rowspan=7, sticky="nsew")
        


        self.doFrame_contaner_frame = tk.Frame(self.domidel_frame, bg=self.accent_blue)
        self.doFrame_contaner_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.doList_Frame_contaner_frame = tk.Frame(self.doFrame_contaner_frame, bg=self.accent_blue)
        self.doList_Frame_contaner_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.doList_Frame = tk.Frame(self.doList_Frame_contaner_frame, bg=self.accent_blue)
        self.doList_Frame.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        
        self.doitem_List_canvas = tk.Canvas(self.doList_Frame, bg=self.accent_blue)
        self.doitem_List_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        
        self.doitem_List_yscrollbar = tk.Scrollbar(self.doList_Frame, orient='vertical', command=self.doitem_List_canvas.yview)
        self.doitem_List_yscrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.doitem_List_xscrollbar = tk.Scrollbar(self.doList_Frame_contaner_frame, orient='horizontal', command=self.doitem_List_canvas.xview)
        self.doitem_List_xscrollbar.pack(side=tk.TOP, fill=tk.X)
        
        self.doitem_List_canvas.configure(xscrollcommand=self.doitem_List_xscrollbar.set, yscrollcommand=self.doitem_List_yscrollbar.set)
        #self.New_item_contener_canvas.bind('<Configure>', lambda e: self.New_item_contener_canvas.configure(scrollregion=self.New_item_contener_canvas.bbox("all")))

        self.doSelected_item_Display_frame = tk.Frame(self.doitem_List_canvas, bg=self.accent_blue)
        self.doitem_List_canvas.create_window((0, 0), window=self.doSelected_item_Display_frame, anchor=tk.NW)
        self.doSelected_item_Display_frame.bind('<Configure>', lambda e: self.doitem_List_canvas.configure(scrollregion=self.doitem_List_canvas.bbox("all")))

        
        # Pack the widgets for the product tab2
        #self.update_product_listbox()
        #
        self.update_search_results([None, None])
        self.update_Shop_Actions_listbox()

    def load_action_image(self):
        color = "Def_Color"
        if os.path.exists(MAIN_dir+"\\data\\Products\\"+ str(self.Action_code_entry.get()) + "\\"+ str(color) + "\\ActionImage.jpg"):
            img = Image.open(MAIN_dir+"\\data\\Products\\"+ str(self.Action_code_entry.get()) + "\\"+ str(color) + "\\ActionImage.jpg").resize((100, 100))
            img = ImageTk.PhotoImage(img)
            self.Action_image_avatarlabel.config(image=img)
            self.Action_image_avatarlabel.image = img
        else:
            # place holder
            img = Image.open(MAIN_dir+"\\data\\Icon\\no_Action_Image.jpg").resize((100, 100))
            img = ImageTk.PhotoImage(img)
            self.Action_image_avatarlabel.config(image=img)
            self.Action_image_avatarlabel.image = img
            
    def change_Action_image(self):
        if self.Action_code_entry.get() != "":
            color = "Def_Color"
            file_source = filedialog.askopenfilename(filetypes=[("Image Files", "*.png *.jpg *.jpeg")])
            dest_folder = MAIN_dir+"\\data\\Products\\"+ str(self.Action_code_entry.get()) + "\\"+ str(color) + "\\"
            imag_file_name  = "ActionImage.jpg"
            # make sur folder is there
            os.makedirs(dest_folder, exist_ok=True)
            # join name and folder path
            dest_full_path = os.path.join(dest_folder, imag_file_name)
            # copy it to dest folder
            shutil.copy2(file_source, dest_full_path)
            self.load_action_image()
            # TODO : MAKE SUIRE IT IS UPLODED TO WEBSITE 
                    
    def show_product_form(self):
        # call the function in the main file to show the first frame
        self.master.master.show_frame("ActionsForm")
    
    def clear_Shop_Actions_widget(self):
        # Clear the product details widgets
        self.Action_code_entry.delete(0, tk.END)
        self.Action_label_entry.delete(0, tk.END)
        
        self.ifSelected_items = []
        self.doSelected_items = []
        
        
        self.From_Date_entry.delete(0, tk.END)
        self.TO_Date_entry.delete(0, tk.END)
        self.From_Date_entry.insert(0, self.start_value)
        self.TO_Date_entry.insert(0, self.end_value)
        
        self.ifProduct_Make_price_entry.delete(0, tk.END)
        self.ifProduct_Make_Total_price_entry.delete(0, tk.END)
        self.ifProduct_Make_Discount_entry.delete(0, tk.END)
        self.ifProduct_Make_Total_Disc_entry.delete(0, tk.END)
        
        self.doProduct_Make_price_entry.delete(0, tk.END)
        self.doProduct_Make_Total_price_entry.delete(0, tk.END)
    
    def search_products(self, search_text): 
        # Search for the entered text in the code, name, short_key, and type fields of the product table
        results = []
        for Action in self.Shop_Actions:
            if search_text in str(Action):
                results.append(Action)
        return results

    # create a function to update the search results whenever the search box changes
    def update_search_results(self, *args):
        # get the search string from the search box
        search_str = self.search_var.get()
        
        # search for products based on the search string
        results = self.search_products(search_str)
        
        # clear the current items in the list box
        self.list_box.delete(*self.list_box.get_children())

        self.Add_tool_listbox(results)

    def Add_tool_listbox(self, results):
        #print("update_search :"+str(results))
        self.list_box['columns'] = ("Shop_Actions Id", "Shop_Actions Titel", "Created Date", "From", "To")
        self.list_box.heading("#0", text="Shop_Actions Code")
        self.list_box.heading("#1", text="Shop_Actions Titel")
        self.list_box.heading("#2", text="Created Date")
        self.list_box.heading("#3", text="From")
        self.list_box.heading("#4", text="To")

        # Add the products to the product listbox
        for num, Action in enumerate(self.Shop_Actions):
            #print("product :"+str(product))
            self.list_box.insert('', 'end', text=Action[0], values=(Action[1], Action[2], Action[3], Action[4], num))
        
   
    # Define the function for updating the product listbox
    def update_Shop_Actions_listbox(self):
        # Clear the product listbox
        self.list_box.delete(*self.list_box.get_children())
        self.Shop_Actions = []
        results = []
        for s, shop in enumerate(self.Shops):
            if self.Selected_Shop != "" and shop['Shop_name'] != self.Selected_Shop:
                continue
            
            if shop['Shop_Actions'] and shop['Shop_Actions'] != "":
                try:
                    Shop_Actions = json.loads(shop['Shop_Actions'])
                except ValueError:
                    Shop_Actions = []
                # Add the products to the product listbox
                for Shop_Action in Shop_Actions:
                    self.Shop_Actions.append(Shop_Action)
                    results.append(Shop_Action)
        self.Add_tool_listbox(results)
        # Hide the product details frame
        self.hide_add_forme()
        self.change_button.config(state=tk.DISABLED)


    def Save_Shop_Actions(self):
        # self.Action_image
        # TODO : Check if it is not empty and it is uniqe
        Action_code = self.Action_code_entry.get()
        Action_titel = self.Action_label_entry.get()
        from_date = self.From_Date_entry.get()
        to_date = self.TO_Date_entry.get()
        
        if_conditions = ["If", self.ifSelected_items, self.ifProduct_Make_price_entry.get(), self.ifProduct_Make_Total_price_entry.get(), self.ifProduct_Make_Discount_entry.get(), self.ifProduct_Make_Total_Disc_entry.get()]
        Do_makes = ["Do", self.doSelected_items, self.doProduct_Make_price_entry.get(), self.doProduct_Make_Total_price_entry.get()]
        
        for s, shop in enumerate(self.Shops):
            Shop_Actions = []
            if self.Selected_Shop != "" and shop['Shop_name'] != self.Selected_Shop:
                continue
            if shop:
                if shop['Shop_Actions'] and shop['Shop_Actions'] != "":
                    try:
                        Shop_Actions = json.loads(shop['Shop_Actions'])
                    except ValueError:
                        Shop_Actions = []
                
                if self.add_button.cget("text") == "New":
                    Shop_Actions.append([Action_code, Action_titel, self.Created_date, from_date, to_date, if_conditions, Do_makes])
                    Update_table_database("UPDATE Shops SET Shop_Actions=? WHERE Shop_id=? AND Shop_name=? AND Shop_brand_name=?", 
                                    (json.dumps(Shop_Actions), str(shop['Shop_Id']), str(shop['Shop_name']), str(shop['Shop_brand_name'])))
                else:
                    for a, action in enumerate(Shop_Actions):
                        if action[0] == self.Action_code: # if we need to change code so we will compare it with the old code not with new one
                            Shop_Actions[a] = [Action_code, Action_titel, self.start_value, from_date, to_date, if_conditions, Do_makes]
                            break

                    #print("Shop_Actions ", Shop_Actions)
                    Update_table_database("UPDATE Shops SET Shop_Actions=? WHERE Shop_id=? AND Shop_name=? AND Shop_brand_name=?", 
                                    (json.dumps(Shop_Actions), str(shop['Shop_Id']), str(shop['Shop_name']), str(shop['Shop_brand_name'])))
                self.Shops[s]['Shop_Actions'] = json.dumps(Shop_Actions)
                                
        # Update the product listbox
        self.clear_Shop_Actions_widget()
        #
        self.update_Shop_Actions_listbox()
        # Clear the product details widgets
        self.hide_add_forme()
        # Update the product listbox if needed
        self.update_search_results([None, None])

    def on_select(self, event):
        if len(event.widget.selection()) > 0:
            self.change_button.config(state=tk.NORMAL)
            self.delete_button.config(state=tk.NORMAL)
        else:
            self.change_button.config(state=tk.DISABLED)
            self.delete_button.config(state=tk.DISABLED)

    # Create the "Add New" button
    # Define the function for showing the product details frame
    def show_add_forme(self):
        self.clear_Shop_Actions_widget()
        # Show the product details frame
        self.add_button.config(text="New")
        self.notebook_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    def hide_add_forme(self):
        self.clear_Shop_Actions_widget()
        # Hide the add product button
        self.notebook_frame.pack_forget()

    # Create the "Change" button
    def show_change_forme(self):
        self.clear_Shop_Actions_widget()
        # Show the product details frame
        selected_item = self.list_box.selection()
        if selected_item:
            self.Action_code_entry.delete(0, tk.END)
            self.Action_code_entry.insert(0, self.list_box.item(selected_item, "text"))
            self.Action_code = self.list_box.item(selected_item, "text")
            self.Action_label_entry.delete(0, tk.END)
            self.Action_label_entry.insert(0, self.list_box.item(selected_item, "values")[0])

            self.From_Date_entry.delete(0, tk.END)
            self.From_Date_entry.insert(0, self.list_box.item(selected_item, "values")[2])
            self.TO_Date_entry.delete(0, tk.END)
            self.TO_Date_entry.insert(0, self.list_box.item(selected_item, "values")[3])
            
            actions = self.Shop_Actions[int(self.list_box.item(selected_item, "values")[4])]
            self.ifSelected_items = actions[5][1]
            
            self.ifProduct_Make_price_entry.delete(0, tk.END)
            self.ifProduct_Make_price_entry.insert(0, actions[5][2])
            self.ifProduct_Make_Total_price_entry.delete(0, tk.END)
            self.ifProduct_Make_Total_price_entry.insert(0, actions[5][3])
            self.ifProduct_Make_Discount_entry.delete(0, tk.END)
            self.ifProduct_Make_Discount_entry.insert(0, actions[5][4])
            self.ifProduct_Make_Total_Disc_entry.delete(0, tk.END)
            self.ifProduct_Make_Total_Disc_entry.insert(0, actions[5][5])
            
            self.doSelected_items = actions[6][1]
            
            self.doProduct_Make_price_entry.delete(0, tk.END)
            self.doProduct_Make_price_entry.insert(0, actions[6][2])
            self.doProduct_Make_Total_price_entry.delete(0, tk.END)
            self.doProduct_Make_Total_price_entry.insert(0, actions[6][3])
            
            self.add_button.config(text="Save")
            self.notebook_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
            
            self.Update_Selected_item()

    # Define the function for deleting a product
    def delete_action(self):
        # Get the selected product from the listbox
        selected_action = self.list_box.selection()

        if selected_action:
            # Get the ID of the selected product
            action_code = self.list_box.item(selected_action)['text']
            action_title = self.list_box.item(selected_action)['values'][0]
            action_created_date = self.list_box.item(selected_action)['values'][1]
            answer = tk.messagebox.askquestion("Question", "Do you what to delete "+str(action_title)+" ?")
            if answer == 'yes':
                for s, shop in enumerate(self.Shops):
                    Shop_Actions = []
                    if self.Selected_Shop != "" and shop['Shop_name'] != self.Selected_Shop:
                        continue
                    #print("shop['Shop_name'] ", shop['Shop_name'])
                    if shop:
                        if shop['Shop_Actions'] and shop['Shop_Actions'] != "":
                            try:
                                Shop_Actions = json.loads(shop['Shop_Actions'])
                            except ValueError:
                                Shop_Actions = []
                            shop_actionscopy = []
                            #print("#print( ", #print()
                            for sa, Shop_Action in enumerate(Shop_Actions):
                                #print("Shop_Action ", str(Shop_Action))
                                if not Shop_Action[0] == action_code:
                                    shop_actionscopy.append(Shop_Action)
                            Shop_Actions = shop_actionscopy
                            Update_table_database("UPDATE Shops SET Shop_Actions=? WHERE Shop_id=? AND Shop_name=? AND Shop_brand_name=?", 
                                            (json.dumps(Shop_Actions), str(shop['Shop_Id']), str(shop['Shop_name']), str(shop['Shop_brand_name'])))
                # Update the product listbox
                self.update_search_results()  


























    
    def update_info(self):
        total_qty, total_discount, total_tax, all_total_price = self.chack_list()
        '''self.total = (all_total_price - self.homemaster.tax) - self.homemaster.disc
        self.total_items_label.config(text="Total Items : " + str(total_qty))
        self.total_tax_label.config(text="Total Tax : " + str(self.homemaster.tax))
        self.total_discount_label.config(text="Item Discount : " + str(total_discount))
        self.total_tdiscount_label.config(text="Total Discount : " + str(self.homemaster.disc))
        self.total_price_label.config(text="Price Befor : " + str(all_total_price))
        self.total_label.config(text="Price After: " + str((all_total_price - self.homemaster.tax) - self.homemaster.disc))
        '''
        
    
                
    def Get_next_seletion(self, inputs, item_list):
        shop = inputs[0].get()
        code = inputs[1].get()
        color = inputs[2].get()
        size = inputs[3].get()
        qty = inputs[4].get()
        barcode = inputs[5].cget('text')
        #print("item_list['item_list'] ", item_list)
        if item_list['item_list']:
            #print(str(item_list['item_list']))
            info_list = item_list['item_list']
            
            sv = [s[0] for s in info_list]
            inputs[0].config(values=sv)
                
            if shop == "":
                if self.Selected_Shop != "" and self.Selected_Shop in sv:
                   inputs[0].set(self.Selected_Shop)
                elif self.homemaster.Shops_Names[0] in sv:
                    inputs[0].set(self.homemaster.Shops_Names[0])
            else:
                for s in info_list:
                    #print("code s")
                    #print(str(s))
                    if s[0] in shop:
                        #print("code s0")
                        #print(str(s[0]))
                        v = [c[0] for c in s[1]]
                        inputs[1].config(values=v)
                        if len(v) == 1:
                            inputs[1].set(v[0])
                        break
            
            if code == "":
                for s in info_list:
                    #print("code s")
                    #print(str(s))
                    if s[0] in shop:
                        #print("code s0")
                        #print(str(s[0]))
                        v = [c[0] for c in s[1]]
                        inputs[1].config(values=v)
                        if len(v) == 1:
                            inputs[1].set(v[0])
                        inputs[1].event_generate("<<ComboboxSelected>>")
                        return
            else:
                found = 0
                for s in info_list:
                    if s[0] in shop:
                        for codes in s[1]:
                            if codes[0] == code:
                                v = [color[0] for color in codes[1]]
                                inputs[2].config(values=v)
                                if len(v) == 1:
                                    inputs[2].set(v[0])
                                found = 1
                                break
                        if found:
                            break
                    
            if color == "":
                for s in info_list:
                    if s[0] in shop:
                        for codes in s[1]:
                            if codes[0] == code:
                                v = [color[0] for color in codes[1]]
                                inputs[2].config(values=v)
                                if len(v) == 1:
                                    inputs[2].set(v[0])
                                inputs[2].event_generate("<<ComboboxSelected>>")
                                return
            else:
                found = 0
                for s in info_list:
                    if s[0] in shop:
                        for codes in s[1]:
                            if codes[0] == code:
                                for c in codes[1]:
                                    if c[0] == color:
                                        v = [s[0] for s in c[1]]
                                        inputs[3].config(values=v)
                                        if len(v) == 1:
                                            inputs[3].set(v[0])
                                        found = 1
                                        break
                            if found:
                                break
                    if found:
                        break
                    
            if size == "":
                for s in info_list:
                    if s[0] in shop:
                        for codes in s[1]:
                            if codes[0] == code:
                                for c in codes[1]:
                                    if c[0] == color:
                                        v = [s[0] for s in c[1]]
                                        inputs[3].config(values=v)
                                        if len(v) == 1:
                                            inputs[3].set(v[0])
                                        inputs[3].event_generate("<<ComboboxSelected>>")
                                        return
            else:
                found = 0
                for s in info_list:
                    if s[0] in shop:
                        for codes in s[1]:
                            if codes[0] == code:
                                for c in codes[1]:
                                    if c[0] == color:
                                        for s in c[1]:
                                            if s[0] == size:
                                                #inputs[4].set(1)
                                                inputs[4].master.winfo_children()[0].config(text="QTY Max is " + str(s[1][0][4]))
                                                inputs[5].config(text=s[1][0][5])
                                                found = 1
                                            break
                                    if found:
                                        break
                            if found:
                                break
                    if found:
                        break
                    
            if qty == "":
                for s in info_list:
                    if s[0] in shop:
                        for codes in s[1]:
                            if codes[0] == code:
                                for c in codes[1]:
                                    if c[0] == color:
                                        for s in c[1]:
                                            if s[0] == size:
                                                inputs[4].set(1)
                                                inputs[4].master.winfo_children()[0].config(text="QTY Max is " + str(s[1][0][4]))
                                                inputs[5].config(text=s[1][0][5])
                                                return
                                            
    def Update_selected_item_info(self, data, selected_item_info, new_item_Price_Spinbox, new_item_TPrice_Spinbox, index):
        self.Get_next_seletion(data, selected_item_info)
        
        Selected_item_Display_frames = []
        Selected_items = []
        if str(self.notebook_frame.tab(self.notebook_frame.index("current"), "text")) == "Do :":
            Selected_items = [self.doSelected_items]
            Selected_item_Display_frames = [self.doSelected_item_Display_frame]
        else:
            Selected_items = [self.ifSelected_items, self.doSelected_items]
            Selected_item_Display_frames = [self.ifSelected_item_Display_frame, self.doSelected_item_Display_frame]
            
        for y, select in enumerate(Selected_item_Display_frames):
            Selected_item_Display_frame = Selected_item_Display_frames[y]
            Selected_item = Selected_items[y]
            
            if Selected_item == 0:
                return
            # QTY
            Selected_item[index][7] = data[4].get()
            # price
            Selected_item[index][10] = new_item_Price_Spinbox.get()
            # shop
            Selected_item[index][12] = data[0].get()
            #code
            Selected_item[index][2] = data[1].get()
            # color
            Selected_item[index][5] = data[2].get()
            # size
            Selected_item[index][6] = data[3].get()
            new_item_TPrice_Spinbox.set(str(float(data[4].get())*float(new_item_Price_Spinbox.get())))
            disc = ""
            if float(selected_item_info['values']['price'])-float(new_item_Price_Spinbox.get()) > 0:
                disc = " DISCOUNT " + str(float(selected_item_info['values']['price'])-float(new_item_Price_Spinbox.get()))
            data[6].config(text="Price " + str(selected_item_info['values']['price']) + disc)
            self.update_info()
    
    def remove_item(self, index, selected_frame):
        if str(self.notebook_frame.tab(self.notebook_frame.index("current"), "text")) == "If :":
            self.Selected_items = self.ifSelected_items
        elif str(self.notebook_frame.tab(self.notebook_frame.index("current"), "text")) == "Do :":
            self.Selected_items = self.doSelected_items
            
        if not self.Selected_items:
            return
        answer = tk.messagebox.askquestion("Question", "Do you whant to Delete "+str(self.Selected_items[index])+" items?")
        if answer == 'yes':
            self.selected_indexd = -1
            self.Selected_items.remove(self.Selected_items[index])
            selected_frame.destroy()
        self.Update_Selected_item()    
                
    def Update_Selected_item(self):
        Selected_item_Display_frames = []
        Selected_items = []
        if str(self.notebook_frame.tab(self.notebook_frame.index("current"), "text")) == "Do :":
            Selected_items = [self.doSelected_items]
            Selected_item_Display_frames = [self.doSelected_item_Display_frame]
        else:
            Selected_items = [self.ifSelected_items, self.doSelected_items]
            Selected_item_Display_frames = [self.ifSelected_item_Display_frame, self.doSelected_item_Display_frame]
            
        for y, select in enumerate(Selected_item_Display_frames):
            Selected_item_Display_frame = Selected_item_Display_frames[y]
            Selected_item = Selected_items[y]
            #print("selected item "+str(y) + " : "+str(Selected_item))
            for items in Selected_item_Display_frame.winfo_children():
                items.destroy()
                
            #self.midel_frame
            for i, selected_item in enumerate(Selected_item):
                
                #print("selected_item ", selected_item)
                selected_item_info = selected_item[0]
                #print("selected_item_info |", selected_item_info)
                #print("selected_item ", selected_item)
                
                #if isinstance(selected_item_info, str):
                #    selected_item_info = ast.literal_eval(selected_item_info)
                item = [""]
                
                new_item_fram = tk.Frame(Selected_item_Display_frame, bg=self.accent_blue, highlightthickness=2, highlightbackground="black")
                new_item_fram.grid(row=len(Selected_item_Display_frame.winfo_children()), column=0, pady=1, sticky=tk.EW)

                # TODO ADD IMAGE 

                new_item_name = tk.Label(new_item_fram, text=str(selected_item[4]), font=("Arial", 11), bg=self.accent_blue, fg=self.text_light)
                new_item_name.grid(row=0, column=1, columnspan=6, sticky="nsew")

                new_barcode_Label = tk.Label(new_item_fram, text=str("barcode"), font=("Arial", 7), bg=self.accent_blue, fg=self.text_light)
                new_barcode_Label.grid(row=1, column=1, columnspan=3, sticky="nsew")
                
                new_type_Label = tk.Label(new_item_fram, text=str(selected_item[15]), font=("Arial", 7), bg=self.accent_blue, fg=self.text_light)
                new_type_Label.grid(row=1, column=3, columnspan=3, sticky="nsew")
                
                new_item_QTY_fram = tk.Frame(new_item_fram, bg=self.accent_blue)
                new_item_QTY_fram.grid(row=2, column=1, rowspan=2, sticky="nsew")
                
                new_item_QTY_Label = tk.Label(new_item_QTY_fram, text="QTY Max is " + str(selected_item[8]), font=("Arial", 8), bg=self.accent_blue, fg=self.text_light)
                new_item_QTY_Label.grid(row=1, column=1, sticky="nsew")
                new_item_QTY_Spinbox = ttk.Spinbox(new_item_QTY_fram, from_=0, to=100, width=10)
                new_item_QTY_Spinbox.grid(row=2, column=1, sticky="nsew")
                new_item_QTY_Spinbox.set(str(selected_item[7]))
                price_ = ""
                price_ = str(selected_item_info['values']['price'])
                disc = ""
                if float(selected_item_info['values']['price'])-float(selected_item[10]) > 0:
                    disc = " DISCOUNT " + str(float(selected_item_info['values']['price'])-float(selected_item[10]))
                new_item_Price_Label = tk.Label(new_item_fram, text="Price " + price_ + disc, font=("Arial", 7), bg=self.accent_blue, fg=self.text_light)
                new_item_Price_Label.grid(row=2, column=2, sticky="nsew")
                new_item_Price_Spinbox = ttk.Spinbox(new_item_fram, from_=0, to=100, width=10)
                new_item_Price_Spinbox.grid(row=3, column=2, sticky="nsew")
                new_item_Price_Spinbox.set(str(selected_item[10]))

                new_item_Shop_Label = tk.Label(new_item_fram, text="Shop :" , font=("Arial", 7), bg=self.accent_blue, fg=self.text_light)
                new_item_Shop_Label.grid(row=2, column=3, sticky="nsew")
                new_item_Shop_Combobox = ttk.Combobox(new_item_fram, values=[], width=10)
                new_item_Shop_Combobox.grid(row=3, column=3, padx=5, pady=5, sticky=tk.W)
                new_item_Shop_Combobox.set(str(selected_item[13]))
                new_item_Code_Label = tk.Label(new_item_fram, text="Code :" , font=("Arial", 7), bg=self.accent_blue, fg=self.text_light)
                new_item_Code_Label.grid(row=2, column=4, sticky="nsew")
                new_item_Code_Combobox = ttk.Combobox(new_item_fram, values=[], width=10)
                new_item_Code_Combobox.grid(row=3, column=4, padx=5, pady=5, sticky=tk.W)
                new_item_Code_Combobox.set(str(selected_item[2]))
                new_item_Color_Label = tk.Label(new_item_fram, text="Color " , font=("Arial", 7), bg=self.accent_blue, fg=self.text_light)
                new_item_Color_Label.grid(row=2, column=5, sticky="nsew")
                new_item_Color_Combobox = ttk.Combobox(new_item_fram, values=[], width=10)
                new_item_Color_Combobox.grid(row=3, column=5, padx=5, pady=5, sticky=tk.W)
                new_item_Color_Combobox.set(str(selected_item[5]))
                new_item_Size_Label = tk.Label(new_item_fram, text="Size " , font=("Arial", 7), bg=self.accent_blue, fg=self.text_light)
                new_item_Size_Label.grid(row=2, column=6, sticky="nsew")
                new_item_Size_Combobox = ttk.Combobox(new_item_fram, values=[], width=10)
                new_item_Size_Combobox.grid(row=3, column=6, padx=5, pady=5, sticky=tk.W)
                new_item_Size_Combobox.set(str(selected_item[6]))
                
                new_exbarcode_Label = tk.Label(new_item_fram, text=str(selected_item[14]), font=("Arial", 7), bg=self.accent_blue, fg=self.text_light)
                new_exbarcode_Label.grid(row=1, column=7, sticky="nsew")
                
                del_button = tk.Button(new_item_fram, text="x", command= lambda index=i, frame=new_item_fram: self.remove_item(index, frame), **self.button_style)
                del_button.grid(row=0, column=7, sticky="nsew")
                # self.master.bind("<Delete>", lambda _: self.remove_item())
                
                new_item_TPrice_Label = tk.Label(new_item_fram, text="Total Price is " , font=("Arial", 13), bg=self.accent_blue, fg=self.text_light)
                new_item_TPrice_Label.grid(row=2, column=7, sticky="nsew")
                new_item_TPrice_Spinbox = ttk.Spinbox(new_item_fram, from_=0, to=100, width=10)
                new_item_TPrice_Spinbox.grid(row=3, column=7, sticky="nsew")
                new_item_TPrice_Spinbox.set(str(float(selected_item[7])*float(selected_item[8])))
                
                data = [new_item_Shop_Combobox, new_item_Code_Combobox, new_item_Color_Combobox, new_item_Size_Combobox, new_item_QTY_Spinbox, new_barcode_Label, new_item_Price_Label]

                self.Get_next_seletion(data, selected_item_info)
                

                new_item_Shop_Combobox.bind("<<ComboboxSelected>>", lambda  _, d=data, v=selected_item_info, p=new_item_Price_Spinbox, tp=new_item_TPrice_Spinbox, j=i: self.Update_selected_item_info(d, v, p, tp, j))
                new_item_Code_Combobox.bind("<<ComboboxSelected>>", lambda  _, d=data, v=selected_item_info, p=new_item_Price_Spinbox, tp=new_item_TPrice_Spinbox, j=i: self.Update_selected_item_info(d, v, p, tp, j))
                new_item_Color_Combobox.bind("<<ComboboxSelected>>", lambda  _, d=data, v=selected_item_info, p=new_item_Price_Spinbox, tp=new_item_TPrice_Spinbox, j=i: self.Update_selected_item_info(d, v, p, tp, j))
                new_item_Size_Combobox.bind("<<ComboboxSelected>>", lambda  _, d=data, v=selected_item_info, p=new_item_Price_Spinbox, tp=new_item_TPrice_Spinbox, j=i: self.Update_selected_item_info(d, v, p, tp, j))

                new_item_Shop_Combobox.bind("<<ComboboxClicked>>", lambda  _, d=data, v=selected_item_info, p=new_item_Price_Spinbox, tp=new_item_TPrice_Spinbox, j=i: self.Update_selected_item_info(d, v, p, tp, j))
                new_item_Code_Combobox.bind("<<ComboboxClicked>>", lambda  _, d=data, v=selected_item_info, p=new_item_Price_Spinbox, tp=new_item_TPrice_Spinbox, j=i: self.Update_selected_item_info(d, v, p, tp, j))
                new_item_Color_Combobox.bind("<<ComboboxClicked>>", lambda  _, d=data, v=selected_item_info, p=new_item_Price_Spinbox, tp=new_item_TPrice_Spinbox, j=i: self.Update_selected_item_info(d, v, p, tp, j))
                new_item_Size_Combobox.bind("<<ComboboxClicked>>", lambda  _, d=data, v=selected_item_info, p=new_item_Price_Spinbox, tp=new_item_TPrice_Spinbox, j=i: self.Update_selected_item_info(d, v, p, tp, j))

                new_item_Price_Spinbox.bind("<KeyRelease>", lambda  _, d=data, v=selected_item_info, p=new_item_Price_Spinbox, tp=new_item_TPrice_Spinbox, j=i: self.Update_selected_item_info(d, v, p, tp, j))
                new_item_QTY_Spinbox.bind("<KeyRelease>", lambda  _, d=data, v=selected_item_info, p=new_item_Price_Spinbox, tp=new_item_TPrice_Spinbox, j=i: self.Update_selected_item_info(d, v, p, tp, j))
                #new_item_TPrice_Spinbox.bind("<<KeyRelease>>", lambda  _, d=data, v=selected_item_info, p=new_item_Price_Spinbox, tp=new_item_TPrice_Spinbox, j=i: self.Update_selected_item_info(d, v, p, tp, j))

                new_item_Price_Spinbox.config(command= lambda d=data, v=selected_item_info, p=new_item_Price_Spinbox, tp=new_item_TPrice_Spinbox, j=i: self.Update_selected_item_info(d, v, p, tp, j))
                new_item_QTY_Spinbox.config(command= lambda  d=data, v=selected_item_info, p=new_item_Price_Spinbox, tp=new_item_TPrice_Spinbox, j=i: self.Update_selected_item_info(d, v, p, tp, j))
                #new_item_TPrice_Spinbox.bind(command= lambda d=data, v=selected_item_info, p=new_item_Price_Spinbox, tp=new_item_TPrice_Spinbox, j=i: self.Update_selected_item_info(d, v, p, tp, j))
            self.update_info()
        
  # this will
    def chack_list(self):
        total_discount = 0
        total_tax = 0
        total_qty = 0
        all_total_price = 0
        self.Selected_items = []
        
        
        Selected_item_Display_frames = []
        Selected_items = []
        if str(self.notebook_frame.tab(self.notebook_frame.index("current"), "text")) == "Do :":
            Selected_items = [self.doSelected_items]
            Selected_item_Display_frames = [self.doSelected_item_Display_frame]
        else:
            Selected_items = [self.ifSelected_items, self.doSelected_items]
            Selected_item_Display_frames = [self.ifSelected_item_Display_frame, self.doSelected_item_Display_frame]
            
        for y, select in enumerate(Selected_item_Display_frames):
            Selected_item_Display_frame = Selected_item_Display_frames[y]
            Selected_itemss = Selected_items[y]
            for a, selected_item in enumerate(Selected_itemss):
                #print("in update item: " + str(selected_item[0]))
                qty = float(selected_item[7])
                price = float(selected_item[10])
                discount = float(selected_item[0]['values']['price']) - float(selected_item[10])
                tax = float(selected_item[10])
                total_price = float(selected_item[11])
                
                # Calculate the expected total price based on quantity, price, discount, and tax
                expected_total_price = qty * (price)  # - tax
                
                # Update the total price in the item if it doesn't match the expected value
                if total_price != expected_total_price:
                    Selected_items[y][a][11] = expected_total_price
                
                # Update the price variable
                total_qty += qty
                total_discount += discount
                total_tax += tax
                all_total_price += expected_total_price
            
        return total_qty, total_discount, total_tax, all_total_price

    # this will add item to the list
    def add_item(self, item_info):
        #print("item_info = " + str(item_info))
        if (item_info['type'] == "UnKNOWN"):
            items = item_info['values']
            # selected_data = Id, code, color, size, qty, left, barcode, extr
            
            # in chake_action we will chack if item is in the list or not
            # id, code, barcode, name, color, size, qty, price, disc, includetax, total_price, shop, extr

            shopname = "Unknown Shop"
            code = "Unknown Code"
            color = "Unknown Color"
            size = "Unknown Size"
            
            # finde similar item in the list that has same price and cost
            for item in self.Shops_info['Shop_items']:
                # if item price and cost are in range of the unknown item price and cost +- 50% we will consider it as similar item
                if isinstance(item, list):
                    item = item[0]
                #print('item ', item)
                #print("item price ", item['price'], "item cost ", item['cost'], "uitemprice ", uitemprice, "uitemcost ", uitemcost)
                #print("item price range ", float(uitemprice) - float(uitemprice)/2, " - ", float(uitemprice) + float(uitemprice)/2 )
                uitemprice = float(items['price'])
                uitemcost = float(items['cost'])
                if ((float(item['cost']) > uitemprice/3 and float(item['cost']) <= (float(uitemcost) + float(uitemcost)/2)) and float(item['cost']) < uitemprice or  float(item['cost']) >= uitemprice/3 and(float(item['cost']) <= float(uitemprice))  ) and ((float(item['price']) >= float(uitemprice)) and (float(item['price']) <= float(uitemprice)) ):
                    # change this item name to unknown item and add it to the list
                    item_type = json.loads(item['more_info']) if item['more_info'] else {}
                    if not item_type == {}:
                        # get types shop name, code, color, size, extra data if item_type has it like [shops [codes [[colors ...[[sizes[extra data[],...],...],...],...],...],...],...]
                        def get_type_info(item_type, path):
                            #print("item_type ", item_type)
                            if len(item_type) == 2 and isinstance(item_type[0], str) and isinstance(item_type[1], list):
                                new_path = get_type_info(item_type[1], path + [item_type[0]])
                                if new_path:
                                    return new_path
                            elif isinstance(item_type[0], list):
                                new_path = get_type_info(item_type[0], path)
                                if new_path:
                                    return new_path
                            elif len(item_type) > 4:
                                if float(item_type[4]) > 0:
                                    #print("path ", path)
                                    path = path + [float(item_type[4])]
                                    return path
                            return None
                        path = get_type_info(item_type, [])
                        if path:
                            #print("path2 ", path)
                            shopname = path[0]
                            code = path[1]
                            color = path[2]
                            size = path[3]
                            qtylaft = path[4] if len(path) > 4 else 1
                            item_info = {'type': "ITEM", 'values': item, 'extra_data': [], 'item_list': []}
                            value = [str(item['id']), item['code'], item['barcode'], 'Unknown Item', color, size, 1, qtylaft, items['price'], item['include_tax'], items['price'], shopname, ""]
                            #                 :
                            if str(self.notebook_frame.tab(self.notebook_frame.index("current"), "text")) == "If :":
                                self.ifSelected_items.append([item_info, str(value[0]), value[1], value[2], value[3], value[4], value[5], value[6], value[7], "", value[8], value[9], value[10], value[11], value[12], ""])
                                self.doSelected_items.append([item_info, str(value[0]), value[1], value[2], value[3], value[4], value[5], value[6], value[7], "", value[8], value[9], value[10], value[11], value[12], ""])
                            elif str(self.notebook_frame.tab(self.notebook_frame.index("current"), "text")) == "Do :":
                                self.doSelected_items.append([item_info, str(value[0]), value[1], value[2], value[3], value[4], value[5], value[6], value[7], "", value[8], value[9], value[10], value[11], value[12], ""])
                                
                            
                            self.Update_Selected_item()
                            return
        
            # if not similar item found we will add the unknown item to the list with unknown shop and code and color and size
            # msg box to ask if user want to add this item to the shop items list with this info
            tk.messagebox.askquestion("Warning", "This item is not in the shop items list, do you want to add it to the shop items list with this info? \n\n Shop Name: " + shopname + "\n Code: " + code + "\n Color: " + color + "\n Size: " + size)
            

        if (item_info['type'] == "ITEM"):
            for data in item_info['extra_data']:
                shop = self.homemaster.Shops_Names
                if self.Selected_Shop != "":
                    shop = [self.Selected_Shop]
                items, doc, selected_type, barcode, shop_name, code, color, size, qty = \
                     item_info['values'], None, item_info['type'], data[6], data[0], data[1], data[2], data[3], data[4]
                
                # chacke if qty lefte is less than 0 or not
                # change this item name to unknown item and add it to the list
                item_type = json.loads(items['more_info']) if items['more_info'] else {}
                if not item_type == {}:
                    # get types shop name, code, color, size, extra data if item_type has it like [shops [codes [[colors ...[[sizes[extra data[],...],...],...],...],...],...],...]
                    def get_type_info(item_type, path):
                        #print("item_type ", item_type)
                        if len(item_type) == 2 and isinstance(item_type[0], str) and isinstance(item_type[1], list):
                            new_path = get_type_info(item_type[1], path + [item_type[0]])
                            if new_path:
                                return new_path
                        elif isinstance(item_type[0], list):
                            new_path = get_type_info(item_type[0], path)
                            if new_path:
                                return new_path
                        elif len(item_type) > 4:
                            if float(item_type[4]) > 0:
                                if float(item_type[4])-float(qty) >= 0:
                                    path = path + [qty]
                                    #print("path ", path)
                                    return path
                                else:
                                    path = path + [float(item_type[4])]
                                    #print("path ", path)
                                    return path
                        return None
                    path = get_type_info(item_type, [])
                    if path:
                        #print("path2 ", path)
                        #print("shop_name ", shop_name, "code ", code, "color ", color, "size ", size)
                        if not (path[0] == shop_name and path[1] == code and path[2] == color and path[3] == size):
                            ask = tk.messagebox.askquestion("Warning", "Selected Items Size, Color or Code Out of Stockd or will be out of stock, do you want to add it to the shop items list with this info? \n\n Shop Name: " + path[0] + "\n Code: " + path[1] + "\n Color: " + path[2] + "\n Size: " + path[3])
                            if ask == 'yes':
                                shopname = path[0]
                                code = path[1]
                                color = path[2]
                                size = path[3]
                                nqty = float(qty)-path[4]
                                qty = path[4]
                                item_info = {'type': "ITEM", 'values': items, 'extra_data': [], 'item_list': []}
                                value = [str(items['id']), items['code'], items['barcode'], items['name'], color, size, qty, items['price'], items['price'], items['include_tax'], items['price'], shopname, ""]
                                if str(self.notebook_frame.tab(self.notebook_frame.index("current"), "text")) == "If :":
                                    self.ifSelected_items.append([item_info, str(value[0]), value[1], value[2], value[3], value[4], value[5], value[6], value[7], "", value[8], value[9], value[10], value[11], value[12], ""])
                                    self.doSelected_items.append([item_info, str(value[0]), value[1], value[2], value[3], value[4], value[5], value[6], value[7], "", value[8], value[9], value[10], value[11], value[12], ""])
                                elif str(self.notebook_frame.tab(self.notebook_frame.index("current"), "text")) == "Do :":
                                    self.doSelected_items.append([item_info, str(value[0]), value[1], value[2], value[3], value[4], value[5], value[6], value[7], "", value[8], value[9], value[10], value[11], value[12], ""])
                                
                        else:
                            qty = float(qty)-float(path[4])
                            if data[7] != []:
                                for t, typ in enumerate(data[7]):                            
                                    QTY = int(typ[1])
                                    PRICE = int(typ[2])
                                    value = [str(items['id']), code, barcode, items['name'], color, size, float(QTY), PRICE, 0, items['include_tax'], float(QTY)*float(PRICE), shop_name, ""]
                                    if str(self.notebook_frame.tab(self.notebook_frame.index("current"), "text")) == "If :":
                                        self.ifSelected_items.append([item_info, str(value[0]), value[1], value[2], value[3], value[4], value[5], value[6], value[7], data[5], PRICE, value[9], value[10], value[11], value[12], typ[0]])
                                        self.doSelected_items.append([item_info, str(value[0]), value[1], value[2], value[3], value[4], value[5], value[6], value[7], data[5], PRICE, value[9], value[10], value[11], value[12], typ[0]])
                                    elif str(self.notebook_frame.tab(self.notebook_frame.index("current"), "text")) == "Do :":
                                        self.doSelected_items.append([item_info, str(value[0]), value[1], value[2], value[3], value[4], value[5], value[6], value[7], data[5], PRICE, value[9], value[10], value[11], value[12], typ[0]])
                                
                                    
                            else:
                                value = [str(items['id']), code, barcode, items['name'], color, size, float(path[4]), items['price'], 0, items['include_tax'], float(qty)*float(items['price']), shop_name, '']
                                if str(self.notebook_frame.tab(self.notebook_frame.index("current"), "text")) == "If :":
                                    self.ifSelected_items.append([item_info, str(value[0]), value[1], value[2], value[3], value[4], value[5], value[6], value[7], data[5], item_info['values']['price'], value[9], value[10], value[11], value[12], ""])
                                    self.doSelected_items.append([item_info, str(value[0]), value[1], value[2], value[3], value[4], value[5], value[6], value[7], data[5], item_info['values']['price'], value[9], value[10], value[11], value[12], ""])
                                elif str(self.notebook_frame.tab(self.notebook_frame.index("current"), "text")) == "Do :":
                                    self.doSelected_items.append([item_info, str(value[0]), value[1], value[2], value[3], value[4], value[5], value[6], value[7], data[5], item_info['values']['price'], value[9], value[10], value[11], value[12], ""])
                                
                            
                            if qty <= 0:
                                continue

                # finde similar item in the list that has same price and cost
                for item in self.Shops_info['Shop_items']:
                    # if item price and cost are in range of the unknown item price and cost +- 50% we will consider it as similar item
                    if isinstance(item, list):
                        item = item[0]
                    #print('item ', item)
                    #print("item price ", item['price'], "item cost ", item['cost'], "uitemprice ", uitemprice, "uitemcost ", uitemcost)
                    #print("item price range ", float(uitemprice) - float(uitemprice)/2, " - ", float(uitemprice) + float(uitemprice)/2 )
                    uitemprice = float(items['price'])
                    uitemcost = float(items['cost'])
                    if (float(item['price']) == float(uitemprice) and float(item['cost']) >= float(uitemcost) - float(uitemcost)/2 and float(item['cost']) <= float(uitemcost) + float(uitemcost)/2):
                        # change this item name to unknown item and add it to the list
                        item_type = json.loads(item['more_info']) if item['more_info'] else {}
                        if not item_type == {}:
                            # get types shop name, code, color, size, extra data if item_type has it like [shops [codes [[colors ...[[sizes[extra data[],...],...],...],...],...],...],...]
                            def get_type_info(item_type, path):
                                #print("item_type ", item_type)
                                if len(item_type) == 2 and isinstance(item_type[0], str) and isinstance(item_type[1], list):
                                    new_path = get_type_info(item_type[1], path + [item_type[0]])
                                    if new_path:
                                        return new_path
                                elif isinstance(item_type[0], list):
                                    new_path = get_type_info(item_type[0], path)
                                    if new_path:
                                        return new_path
                                elif len(item_type) > 4:
                                    if float(item_type[4]) > 0 and float(item_type[4]) - float(qty) >= 0:
                                        path = path + [qty]
                                        #print("path ", path)
                                        return path
                                return None
                            path = get_type_info(item_type, [])
                            if path:
                                ask = tk.messagebox.askquestion("Warning", "This item is out of stock, but we found similar item in the shop items list with this info: \n\n Shop Name: " + path[0] + "\n Code: " + path[1] + "\n Color: " + path[2] + "\n Size: " + path[3] + "\n\n Do you want to add this similar item to the list instead?")
                                if ask == 'yes':
                                    shopname = path[0]
                                    code = path[1]
                                    color = path[2]
                                    size = path[3]
                                    item_info = {'type': "ITEM", 'values': item, 'extra_data': [], 'item_list': []}
                                    value = [str(item['id']), item['code'], item['barcode'], 'Unknown Item', color, size, path[4], items['price'], items['price'], item['include_tax'], items['price'], shopname, ""]
                                    if str(self.notebook_frame.tab(self.notebook_frame.index("current"), "text")) == "If :":
                                        self.ifSelected_items.append([item_info, str(value[0]), value[1], value[2], value[3], value[4], value[5], value[6], value[7], "", value[8], value[9], value[10], value[11], value[12], ""])
                                        self.doSelected_items.append([item_info, str(value[0]), value[1], value[2], value[3], value[4], value[5], value[6], value[7], "", value[8], value[9], value[10], value[11], value[12], ""])
                                    elif str(self.notebook_frame.tab(self.notebook_frame.index("current"), "text")) == "Do :":
                                        self.doSelected_items.append([item_info, str(value[0]), value[1], value[2], value[3], value[4], value[5], value[6], value[7], "", value[8], value[9], value[10], value[11], value[12], ""])
                                
                                    break
                                else:
                                    if data[7] != []:
                                        for t, typ in enumerate(data[7]):                            
                                            QTY = int(typ[1])
                                            PRICE = int(typ[2])
                                            value = [str(items['id']), code, barcode, items['name'], color, size, float(QTY), PRICE, 0, items['include_tax'], float(QTY)*float(PRICE), shop_name, ""]
                                            if str(self.notebook_frame.tab(self.notebook_frame.index("current"), "text")) == "If :":
                                                self.ifSelected_items.append([item_info, str(value[0]), value[1], value[2], value[3], value[4], value[5], value[6], value[7], data[5], PRICE, value[9], value[10], value[11], value[12], typ[0]])
                                                self.doSelected_items.append([item_info, str(value[0]), value[1], value[2], value[3], value[4], value[5], value[6], value[7], data[5], PRICE, value[9], value[10], value[11], value[12], typ[0]])
                                            elif str(self.notebook_frame.tab(self.notebook_frame.index("current"), "text")) == "Do :":
                                                self.doSelected_items.append([item_info, str(value[0]), value[1], value[2], value[3], value[4], value[5], value[6], value[7], data[5], PRICE, value[9], value[10], value[11], value[12], typ[0]])
                                
                                    else:
                                        value = [str(items['id']), code, barcode, items['name'], color, size, float(path[4]), items['price'], 0, items['include_tax'], float(qty)*float(items['price']), shop_name, '']
                                        if str(self.notebook_frame.tab(self.notebook_frame.index("current"), "text")) == "If :":
                                            self.ifSelected_items.append([item_info, str(value[0]), value[1], value[2], value[3], value[4], value[5], value[6], value[7], data[5], item_info['values']['price'], value[9], value[10], value[11], value[12], ""])
                                            self.doSelected_items.append([item_info, str(value[0]), value[1], value[2], value[3], value[4], value[5], value[6], value[7], data[5], item_info['values']['price'], value[9], value[10], value[11], value[12], ""])
                                        elif str(self.notebook_frame.tab(self.notebook_frame.index("current"), "text")) == "Do :":
                                            self.doSelected_items.append([item_info, str(value[0]), value[1], value[2], value[3], value[4], value[5], value[6], value[7], data[5], item_info['values']['price'], value[9], value[10], value[11], value[12], ""])
                                
                                    break


        if(item_info['type'] == 'ACTIONS'):
           #print("item_info['values'] " + str(item_info['values']))
           #print("item_info['values'][6] " + str(item_info['values'][6]))
           #print("item_info['values'][6][1] " + str(item_info['values'][6][1]))
            for action in item_info['values'][6][1]:
                if str(self.notebook_frame.tab(self.notebook_frame.index("current"), "text")) == "If :":
                    self.ifSelected_items.append(action)
                    self.doSelected_items.append(action)
                elif str(self.notebook_frame.tab(self.notebook_frame.index("current"), "text")) == "Do :":
                    self.doSelected_items.append(action)
                
                
        if (item_info['type'] == "DOCUMENT"):
            self.Selected_items = []
            items = json.loads(item_info['values']['item'])
            for item in items:
                it = fetch_as_dict_list(self.homemaster.Link, "SELECT * FROM product WHERE id=?", (item[0],))[0]
                if it:
                    doc_item_info = {'values': it, 'type': 'DOCUMENT', 'item_list':[]}
                    #print("items===========%%%%%%% = " + str(it))
                    #print("items===========%%%%%%% = " + str(item))
                    #print("doc_item_info ===========%%%%%%% = " + str(doc_item_info))
                    # TODO: last empty one is type find it
                    typ = ""
                    if len(item) > 11:
                        typ = item[11]
                    qtyleft = "??"
                    if str(self.notebook_frame.tab(self.notebook_frame.index("current"), "text")) == "If :":
                        self.ifSelected_items.append([doc_item_info, str(item[0]), item[1], item[2], item[3], item[5], item[6], item[7], item[8], qtyleft, item[8], item[10], 0, item[4], item_info['values']['doc_barcode'], typ])
                        self.doSelected_items.append([doc_item_info, str(item[0]), item[1], item[2], item[3], item[5], item[6], item[7], item[8], qtyleft, item[8], item[10], 0, item[4], item_info['values']['doc_barcode'], typ])
                    elif str(self.notebook_frame.tab(self.notebook_frame.index("current"), "text")) == "Do :":
                        self.doSelected_items.append([doc_item_info, str(item[0]), item[1], item[2], item[3], item[5], item[6], item[7], item[8], qtyleft, item[8], item[10], 0, item[4], item_info['values']['doc_barcode'], typ])                                
                else:
                    pass
        
        self.Update_Selected_item()
        
    




    
    def chack_for_Action(Main_product_holder, if_product_holder):
        print("Done chack_for_Action ")
        for mphs_i, mphs_selected_items in enumerate(Main_product_holder):
            mphs_product_group_type = mphs_selected_items[1]
            mphs_product_group_name = mphs_selected_items[2]
            print("group type ", mphs_product_group_type)
            if not mphs_product_group_type == "":
                for mph_i, mph_selected_item in enumerate(mphs_selected_items[0]):
                    mph_selected_item_info = mph_selected_item[0]
                    
                    if not mph_selected_item[14] == "":
                        continue
                    # get All products info for mains
                    print("comppering main to mph_selected_item ", mph_selected_item)
                    mph_name = mph_selected_item[4]
                    mph_qty = mph_selected_item[7]
                    mph_price = mph_selected_item[10] 
                    mph_at_shop = mph_selected_item[13]
                    mph_code = mph_selected_item[2]
                    mph_color = mph_selected_item[5]
                    mph_size = mph_selected_item[6]
                    mph_t_price = float(mph_selected_item[7])*float(mph_selected_item[10])
                    for ifph_i, ifph_selected_item in enumerate(if_product_holder):
                        ifph_selected_item_info = ifph_selected_item[0]
                        print("comppering main to ifph_selected_item ", ifph_selected_item)
                        # get All products info for if condition to chack it 
                        ifph_name = ifph_selected_item[4]
                        ifph_qty = ifph_selected_item[7]
                        ifph_price = ifph_selected_item[10]
                        ifph_at_shop = ifph_selected_item[13]
                        ifph_code = ifph_selected_item[2]
                        ifph_color = ifph_selected_item[5]
                        ifph_size = ifph_selected_item[6]
                        ifph_t_price = float(ifph_selected_item[7])*float(ifph_selected_item[10])
                        
                        print("comppering main to mph_price ", mph_price)
                        print("comppering main to ifph_price ", ifph_price)
                        # compare the main give product and if products of there is one remove each side untile if product finshed
                        # then retrun the main value that are removed and the action
                        if  float(mph_price) == float(ifph_price) and mph_at_shop == ifph_at_shop:
                            print("price and shop same")
                            if mphs_product_group_name == 'Unknown Item' or ifph_name == 'Unknown Item' or mph_name == ifph_name and \
                                   mph_code == ifph_code and mph_color == ifph_color and mph_size == ifph_size:
                                print("it smae everiting redusing qty needed ")
                                if int(mph_qty) > int(ifph_qty):
                                    Main_product_holder[mphs_i][0][mph_i][7] = int(mph_qty) - int(ifph_qty)
                                elif int(mph_qty) < int(ifph_qty):
                                    if_product_holder[ifph_i][7] = int(ifph_qty) - int(mph_qty)
                                else:
                                    Main_product_holder[mphs_i][0].remove(Main_product_holder[mphs_i][0][mph_i])
                                    if len(Main_product_holder[mphs_i][0]) == 0:
                                        Main_product_holder.remove(Main_product_holder[mphs_i])
                                    if_product_holder.remove(if_product_holder[ifph_i])
                            print("if Product Found \n\n\n\n\n\n\n")
        if not if_product_holder or len(if_product_holder) == 0:
            print("if suceass finshed \n\n\n\n\n\n\n")
            return Main_product_holder
        else:
            return None





                    
