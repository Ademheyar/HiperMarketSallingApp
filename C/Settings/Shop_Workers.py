import tkinter as tk
from tkinter import ttk, filedialog
from PIL import Image, ImageTk
import sqlite3
import shutil
import datetime
import os
import atexit
import sys
import json
import ast

current_dir = os.path.abspath(os.path.dirname(__file__))
MAIN_dir = os.path.join(os.path.join(current_dir, '..'), '..')
sys.path.append(MAIN_dir)

data_dir = os.path.abspath(os.path.join(MAIN_dir, 'data'))
db_path = os.path.join(data_dir, 'my_database.db')

from D.Getdefsize import ButtonEntryApp
from C.List import *

from C.API.Get import *
from C.API.API import *
from C.API.Set import *

from D.printer import *
from D.GetVALUE import GetvalueForm
# Connect to the database or create it if it does not exist

from C.List import *
from D.Getdate import GetDateForm
from D.Chart.Chart import *

from C.API.Get import *

from C.Product.selecttype import *
access_types=[  "USER CAN INITIALIZE SYSTEM", # 0 0
                "USER CAN SEE PAYMENT TOOL BUTTONS", # 1 0
                "USER CAN USE CASH PAYMENT TOOL", # 2 0
                "USER CAN USE CARD PAYMENT TOOL", # 3 0
                "USER CAN USE CREADIT PAYMENT TOOL", # 4 0
                "USER CAN USE CASHOUT PAYMENT TOOL", # 5 0
                "USER CAN USE CASHIN PAYMENT TOOL", # 6 0
                "USER CAN USE OTHER PAYMENT TOOL", # 7 0
                "USER CAN CREATE UKNOWN ITEMS", # 8 0
                "USER CAN SEARCH PRODUCTS", # 9 0
                "USER CAN CREATE NEW ORDER", # 10 0
                "USER CAN VOIDE ORDER", # 11 0
                "USER CAN CHANGE ORDER", # 12 0
                "USER CAN DELETE ITEM FROM ORDER", # 13 0
                "USER CAN CHANGE ITEM QTY", # 14 0
                "USER CAN CHANGE ITEM PRICE", # 15 0
                "USER CAN CHANGE ITEM DISCOUNT", # 16 0
                "USER CAN CHANGE ITEM Type", # 17 0
                "USER CAN APPLY TOTAL DISCOUNT", # 18 0
                "USER CAN FINALIZE ORDER", # 19 0
                "USER CAN CREATE USER/COSTUMER INFO", # 20 0
                "USER CAN SEARCH USER/COSTUMER INFO", # 21 0
                "USER CAN SALL ORDER", # 22 0
                "USER CAN SEARCH DOCUMENTS", # 23 0
                "USER CAN SEARCH ACTIONS", # 24 1
                "USER CAN UPLOAD", # 25 0


                "USER CAN SEE MANAGER", # 26 1      
                    "USER CAN SEE DOCUMENT MANAGER", # 27 1
                    "USER CAN SEE PRODUCTE MANAGER", # 28 1
                    "USER CAN SEE USER MANAGER", # 29 1
                    "USER CAN SEE TOOL MANAGER", # 30 1
                    "USER CAN SEE ACTIONS MANAGER", # 31 1
                "USER CAN SEARCH TOOLS", # 32 1

                    
                "USER CAN CREATE OR CHANGE PRODUCT", # 33 2
                "USER CAN CHANGE PRODUCTS NAME", # 34 2
                "USER CAN CHANGE PRODUCT PRICE", # 35 2
                "USER CAN CHANGE PRODUCTS TYPE", # 36 2 ??
                "USER CAN CHANGE PRODUCTS IMAGE", # 37 2 ??
                "USER CAN CREATE NEW TOOLS", # 38 2
                "USER CAN CHANGE TOOLS ACTIONS", # 39 2
                "USER CAN CHANGE USER/COSTUMER INFO", # 40 2
                "USER CAN CREATE NEW ACTIONS", # 41 2
                "USER CAN FILTER ACTIONS", # 42 2
                "USER CAN EXPORT ACTIONS", # 43 2
                "USER CAN CHANGE RECORDED DOCUMENTS", # 44 2
                "USER CAN SEE TOTAL SALE", # 45 2
                  

                "USER CAN CHANGE PRODUCT COST", # 46 3
                "USER CAN CHANGE PRODUCTS TAX", # 47 3
                "USER CAN CHANGE PRODUCTS PROFITE PERSENT", # 48 3
                "USER CAN CHANGE PRODUCTS STOCK QTY", # 49 3
                "USER CAN CHANGE TOOLS TYPE", # 50 3
                "USER CAN DELETE TOOLS", # 51 3
                "USER CAN SEE DOCUMENT MANAGER", # 52 3
                    "USER CAN CREATE NEW DOCUMENTS", # 53 3
                    "USER CAN CHANGE RECORDED DOCUMENTS", # 54 3
                "USER CAN SEE SETTINGS MANAGER", # 55 3
                    "USER CAN SEE EXPENSES MANAGER", # 56 3
                        "USER CAN SEARCH EXPENSES", # 57 3
                    "USER CAN SEE WORKERS MANAGER", # 58 3
                        "USER CAN SEARCH WORKERS", # 59 3


                "USER CAN CREATE NEW WORKERS", # 60 4
                "USER CAN CHANGE WORKERS INFO", # 61 4
                "USER CAN DELETE WORKERS", # 62 4
                "USER CAN CHANGE SLIP SETTING", # 63 4
                "USER CAN SHOW PRODUCTES COST", # 64 4
                "USER CAN CHANGE TOOLS SETTING", # 65 4
                "USER CAN CHANGE STOCK SETTING", # 66 4
                "USER CAN CHANGE USER SETTING", # 67 4
                "USER CAN CHANGE PRODUCTE STOCK", # 68 4
                "USER CAN CHANGE PRODUTS", # 69 4
                "USER CAN REMOVE PRODUCTES", # 70 4
                "USER CAN CREATE NEW WORKER INFO", # 71 4
                "USER CAN REMOVE COSTUMER INFO", # 72 4


                "USER CAN SEE PROFIT", # 73 5
                "USER CAN CHANGE EXPENSES", # 74 5
                "USER CAN CREATE NEW EXPENSES", # 75 5
                "USER CAN DELETE EXPENSES", # 76 5
                "USER CAN CHANGE STOCK SETTING", # 77 5
                "USER CAN CHANGE EXPENSES SETTING", # 78 5
                "USER CAN CHANGE DOCUMENT SETTING", # 79 5
                "USER CAN DELETE PRODUTS", # 80 5
                "USER CAN DELETE RECORDED DOCUMENTS", # 81 5
                "USER CAN CHANGE USER TYPE", # 82 5
                "USER CAN CREATE ADMINS USERS", # 83 5
                "USER CAN SEE REPORT MANAGER", # 84 5
                    "USER CAN SEE SALES REPORTS", # 85 5
                    "USER CAN SEE STOCK REPORTS", # 86 5
                    "USER CAN SEE USER REPORTS", # 87 5
                    "USER CAN SEE EXPENSES REPORTS", # 88 5
                "USER CAN SEE SHOP SETTING", # 89 5
                    "USER CAN CHANGE SHOP SETTING" # 90 5
              ]

# 0, 0, 0, 0, 0, 0 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,1 , 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5

class WorkersForm(tk.Frame):
    def __init__(self, master, User, Shops, Shop, **arg):
        tk.Frame.__init__(self, master, **arg)
        self.Selected_Shop = ""
        self.User = User
        self.user = User
        self.Shop = Shop
        self.Shops = Shops
        self.Shop_workers = []
        
        self.bg_dark = "#0d47a1"      # Deep blue
        self.bg_light = "#1565c0"     # Darker blue
        self.accent_blue = "#1976d2"  # Medium blue
        self.text_light = "#ffffff"   # White text
        self.bg_darker = "#0a3d91"    # Even darker blue
        self.button_style = {"font": ("Arial", 11, "bold"), "bg": self.accent_blue, "fg": self.text_light, "activebackground": self.bg_light, "activeforeground": self.text_light, "relief": tk.FLAT, "bd": 0}

        
        self.homemaster = self
        while(True):
            if hasattr(self.homemaster, 'onDisplayFrame'):
                break
            else:
                self.homemaster = self.homemaster.master
                
        # Create the frame for the Shop Info
        self.USER_SECURITY_listinfo_frame = tk.Frame(self, bg=self.bg_dark)
        self.USER_SECURITY_listinfo_frame.pack(side=tk.TOP, fill=tk.X, expand=False)
        #self.add(self.USER_SECURITY_listinfo_frame, text="USER & SECURITY")
        
        self.USER_SECURITY_list_box = ttk.Treeview(self.USER_SECURITY_listinfo_frame)
        self.USER_SECURITY_list_box.pack(side=tk.TOP, fill=tk.X, expand=True)
        self.USER_SECURITY_list_box.bind('<<TreeviewSelect>>', self.USER_SECURITY_on_select)

        self.USER_SECURITY_list_box['columns'] = ("Access", "Level")
        self.USER_SECURITY_list_box.heading("#0", text="Access")
        self.USER_SECURITY_list_box.heading("#1", text="Level")
        Shop_Security_Levels = [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4, 4, 4, 4, 4]
        if self.Shop and self.Shop['Shop_Security_Levels']:
            Shop_Security_Levels = json.loads(self.Shop['Shop_Security_Levels'])
        else:
            pass
            # TODO : SAVE DEFAULT SECURITY LEVELS TO SHOP OR ALL WEBSITES HAS TO GIVE DEFAULT SECURITY LEVELS
            '''s = Update_Shop(self.Shop['Shop_link'], self.user, ['Shop_Security_Levels'], [json.dumps(Shop_Security_Levels)], ['Shop_Id'], [self.Shop['Shop_Id']])
            if s:
                # TODO : CHANGE SHOP SELECTED ONLY
                if isinstance(s, list) and len(s) > 0:
                    self.Shops = s
                    self.Shop = s[0]
                else:
                    self.Shops = [s]
                    self.Shop = s
                self.master.master.master.master.master.Shops[0] = self.Shop
            ''' 
        for l, Level in enumerate(access_types):
            if len(Shop_Security_Levels) > l:
                self.USER_SECURITY_list_box.insert('', 'end', text=Level, values=(str(Shop_Security_Levels[l])))

        # Create the search bar
        # Create the frame for the search bar and buttons
        self.search_frame = tk.Frame(self, bg=self.bg_dark)
        self.search_frame.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)

        # create a StringVar to represent the search box
        self.search_var = tk.StringVar()
        tk.Label(self.search_frame, text="Search Worker : ", bg=self.bg_dark, fg=self.text_light).pack(side=tk.LEFT, padx=5, pady=5)
        
        self.search_entry = tk.Entry(self.search_frame, textvariable=self.search_var)
        self.search_entry.bind('<KeyRelease>', self.update_search_results)
        self.search_entry.pack(side=tk.LEFT, padx=5, pady=5)
            
        # bind the update_search_results function to the search box
        self.search_var.trace("w", self.update_search_results)

        # Create the label and entry for the user ID search
        user_info = fetch_as_dict_list(self.homemaster.Link, 'SELECT * FROM USERS', ())  
        # prepare names lists with a blank first entry for null selection
        self.user_names = [''] + [u['User_name'] for u in user_info] if user_info else ['']

        # maps including blank -> ''
        self.user_map = {'': ''}
        self.user_map_id = {'': ''}
        if user_info:
            for u in user_info:
                if u['User_id'] is None:
                    uid = u['Id']
                else:
                    uid = u['User_id']
                self.user_map[u['User_name']] = u
                self.user_map_id[str(uid)] = u['User_id']

        self.user_id_var = tk.StringVar()    # will store the actual user_id (used by perform_search via .get())
        self.user_name_var = tk.StringVar()  # displayed in the combobox

        # Combobox for User ID (shows user_name but stores user_id)
        self.user_id_label = tk.Label(self.search_frame, text="Selecte Worker To Add", bg=self.bg_dark, fg=self.text_light)
        self.user_id_label.pack(side=tk.LEFT, padx=5, pady=5)
        
        self.user_combobox = ttk.Combobox(self.search_frame, textvariable=self.user_name_var, values=self.user_names)
        self.user_combobox.pack(side=tk.LEFT, padx=5, pady=5)

        self.selected_user = []
        def _on_user_selected(event=None):
            name = self.user_name_var.get()
            self.selected_user = self.user_map.get(name, '')
            
        def on_keyrelease(event=None):
            #print("on_keyrelease ")
            typed = self.user_combobox.get().lower()
            if typed == '':
                self.user_combobox['values'] = self.user_names
            else:
                filtered = [item for item in self.user_names if typed in item.lower()]
                self.user_combobox['values'] = filtered
                if filtered:
                    self.user_combobox.event_generate('<Down>')
            self.user_combobox.focus()
            self.user_combobox.icursor(tk.END)
            
        self.user_name_var.trace('w', lambda name, index, mode: on_keyrelease())
        self.user_combobox.bind('<<ComboboxSelected>>', _on_user_selected)


        
        self.add_new_button = tk.Button(self.search_frame, text='Join', command=self.show_add_forme, **self.button_style)
        self.add_new_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.change_button = tk.Button(self.search_frame, text='Change Acesses Level', command=self.show_change_forme, **self.button_style)
        self.change_button.pack(side=tk.LEFT, padx=5, pady=5)
        self.change_button.config(state=tk.DISABLED)

        self.delete_button = tk.Button(self.search_frame, text='Worker has Left', command=self.Remove_worker, **self.button_style)
        self.delete_button.pack(side=tk.LEFT, padx=5, pady=5)
        self.delete_button.config(state=tk.DISABLED)
        
        # Create the list box
        self.l_frame = tk.Frame(self, bg=self.bg_dark)
        self.l_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Create the listbox to display search results
        self.worker_docinfo_listbox = ttk.Treeview(self.l_frame)        
        self.worker_docinfo_listbox.bind('<<TreeviewSelect>>', self.on_select)
        #self.worker_docinfo_listbox.bind("<Button-1>", self.on_treeview_double_click)
        #self.listbox.grid_propagate(False)


        # Add vertical scrollbar
        tree_scrollbar_y = ttk.Scrollbar(self.l_frame, orient='vertical', command=self.worker_docinfo_listbox.yview)
        self.worker_docinfo_listbox.configure(yscrollcommand=tree_scrollbar_y.set)
        tree_scrollbar_y.pack(side='right', fill='y')

        # Add horizontal scrollbar
        tree_scrollbar_x = ttk.Scrollbar(self.l_frame, orient='horizontal', command=self.worker_docinfo_listbox.xview)
        self.worker_docinfo_listbox.configure(xscrollcommand=tree_scrollbar_x.set)
        tree_scrollbar_x.pack(side='bottom', fill='x', )
        
        self.worker_docinfo_listbox.pack(side='top', fill='both', expand=True)
        
        # Create the frame for the product details
        self.details_frame = tk.Frame(self.worker_docinfo_listbox, bg=self.bg_dark)
        self.details_frame.pack_forget()
        self.selected_shop_name = ""
        self.selected_id = ""
        self.main_name = ""
        
        self.selected_shop_id = ""
        
        # Create the widgets for the worker details
        
         # Create the widgets for the user details
        self.User_image_frame = tk.Label(self.details_frame, bg=self.bg_dark)
        
        self.name_label = tk.Label(self.details_frame, text='User Name:', bg=self.bg_dark, fg=self.text_light)
        self.f_and_lname_label = tk.Label(self.details_frame, text='First and Last Name :', bg=self.bg_dark, fg=self.text_light)
        self.gender_label = tk.Label(self.details_frame, text='Gender :', bg=self.bg_dark, fg=self.text_light)
        self.email_label = tk.Label(self.details_frame, text='EMAIL:', bg=self.bg_dark, fg=self.text_light)
        self.phone_num_label = tk.Label(self.details_frame, text='PHONE NUMBER:', bg=self.bg_dark, fg=self.text_light)
        self.id_num_label = tk.Label(self.details_frame, text='ID Number:', bg=self.bg_dark, fg=self.text_light)
        self.addres_label = tk.Label(self.details_frame, text='Adress :', bg=self.bg_dark, fg=self.text_light)
        self.acsess_label = tk.Label(self.details_frame, text='ACSSES :', bg=self.bg_dark, fg=self.text_light)
        # create a StringVar to represent the search box
        self.acsess_var = tk.StringVar()
        self.acsess_entry = tk.Entry(self.details_frame, textvariable=self.acsess_var)
        # bind the update_search_results function to the search box
        self.acsess_var.trace("w", lambda g1,g2,g3: self.load_worker_access())
        
        # Create the listbox to display search results
        self.worker_access_list_forme = tk.Frame(self.details_frame, bg=self.bg_dark)
        self.worker_access_listbox = ttk.Treeview(self.worker_access_list_forme)        
        self.worker_access_listbox.bind('<<TreeviewSelect>>', self.on_select)
        #self.worker_access_listbox.bind("<Button-1>", self.on_treeview_double_click)
        #self.listbox.grid_propagate(False)
        self.Shop_Security_Levels = []
        

        # Add vertical scrollbar
        worker_access_listtree_scrollbar_y = ttk.Scrollbar(self.worker_access_list_forme, orient='vertical', command=self.worker_access_listbox.yview)
        self.worker_access_listbox.configure(yscrollcommand=worker_access_listtree_scrollbar_y.set)
        worker_access_listtree_scrollbar_y.pack(side='right', fill='y')

        # Add horizontal scrollbar
        worker_access_listtree_scrollbar_x = ttk.Scrollbar(self.worker_access_list_forme, orient='horizontal', command=self.worker_access_listbox.xview)
        self.worker_access_listbox.configure(xscrollcommand=worker_access_listtree_scrollbar_x.set)
        worker_access_listtree_scrollbar_x.pack(side='bottom', fill='x', )
        
        self.worker_access_listbox.pack(side='top', fill='both', expand=True)
        
        self.add_button = tk.Button(self.details_frame, text='Add', command=self.make_change_for_worker, **self.button_style)
        self.cancle_button = tk.Button(self.details_frame, text='Cancle', command=self.hide_add_forme, **self.button_style)

        self.User_image_frame.grid(row=0, column=0, rowspan=2, columnspan=2, padx=5, pady=5, sticky=tk.W)
        self.acsess_label.grid(row=2, column=0, padx=5, pady=5, sticky=tk.E)
        self.acsess_entry.grid(row=2, column=1, padx=5, pady=5, sticky=tk.W)
        self.worker_access_list_forme.grid(row=3, column=0, rowspan=7, columnspan=2, padx=5, pady=5, sticky=tk.W)
        
        
        # Pack the widgets for the user details
        self.f_and_lname_label.grid(row=0, column=2, padx=5, pady=5, sticky=tk.E)
        self.name_label.grid(row=1, column=2, padx=5, pady=5, sticky=tk.E)
        self.gender_label.grid(row=2, column=2, padx=5, pady=5, sticky=tk.E)
        self.phone_num_label.grid(row=3, column=2, padx=5, pady=5, sticky=tk.E)
        self.email_label.grid(row=4, column=2, padx=5, pady=5, sticky=tk.E)
        self.id_num_label.grid(row=5, column=2, padx=5, pady=5, sticky=tk.E)
        self.addres_label.grid(row=6, column=2, padx=5, pady=5, sticky=tk.E)
        self.add_button.grid(row=8, column=2, padx=5, pady=5, sticky=tk.W)
        self.cancle_button.grid(row=8, column=3, padx=5, pady=5, sticky=tk.W)

        self.update_WORKERS_listbox()
        self.load_worker_access()
        
    def USER_SECURITY_on_select(self, *arg):
        if self.Shop:
            # Modify the quantity of the item as required
            if len(self.USER_SECURITY_list_box.selection()) > 0:
                for a in self.USER_SECURITY_list_box.selection():
                    values = self.USER_SECURITY_list_box.item(a)['values']
                    text = self.USER_SECURITY_list_box.item(a)['text']
                    i = GetvalueForm(self, values[0], ["Change Access Level of " + text])
                    if not i.value[0] == None and not i.value[0] == "" and i.value[0] > -1:
                        values[0] = i.value[0]
                        self.USER_SECURITY_list_box.item(a, values=values)
                Shop_Security_Levels = []
                for q in self.USER_SECURITY_list_box.get_children():
                    values = self.USER_SECURITY_list_box.item(q)['values']
                    Shop_Security_Levels.append(values[0])
                
                
                Update_table_database('UPDATE Shops SET Shop_Security_Levels=? WHERE Shop_id=?',
                        (json.dumps(Shop_Security_Levels), self.Shop['Shop_Id']))
                
    def load_worker_access(self):
        get_level = self.acsess_entry.get()
        if get_level and not get_level == "":
            for s, shop in enumerate(self.Shops):
                Shop_workers = []
                if self.Selected_Shop != "" and shop['Shop_name'] != self.Selected_Shop:
                    continue
                if shop:
                    if shop['Shop_Security_Levels']:
                        self.Shop_Security_Levels = json.loads(shop['Shop_Security_Levels'])
                    
                    self.worker_access_listbox.delete(*self.worker_access_listbox.get_children())
                    for l, Level in enumerate(access_types):
                        if not l >= len(self.Shop_Security_Levels):
                            #print("user work leve " + str(get_level) + " <= acces level" +str(self.Shop_Security_Levels[l]))
                            if str(self.Shop_Security_Levels[l]) <= str(self.acsess_entry.get()):
                                self.worker_access_listbox.insert('', 'end', text=Level)
                    
    def show_tools_form(self):
        # call the function in the main file to show the first frame
        self.master.master.show_frame("ToolForm")
    
    def clear_tool_details_widget(self):
        # Clear the user details widgets
        self.name_label.config(text='User Name : ')
        self.f_and_lname_label.config(text='First and Last Name : ')
        self.gender_label.config(text='Gender : ')
        self.email_label.config(text='EMAIL : ')
        self.phone_num_label.config(text='PHONE NUMBER : ')
        self.id_num_label.config(text='ID Number : ')
        self.acsess_entry.delete(0, "end")
        
    # Create the "Add New" button
    def show_add_forme(self):
        #[a for a in self.Shop_workers if a[0] == user_id]:
        # chake if self.found_Shops_result is list or dict
        #print("company_name : ", self.Shop['Shop_name'])
        #print("company_brandname : ", self.Shop['Shop_brand_name'])
        #print("Shop_workers : ", self.Shop['Shop_workers'])
        Shop_workers =json.loads(self.Shop['Shop_workers'])
        if Shop_workers == None or Shop_workers == 'None':
            Shop_workers = []

        found_worker_inshop = 0
        for sw, Shop_worker in enumerate(Shop_workers):
            if Shop_worker[0] == self.selected_user['User_id']:
                found_worker_inshop = 1
                Shop_workers[sw] = [self.selected_user['User_id'], self.selected_user['User_fname'] + " "+ self.selected_user['User_Lname'], self.selected_user['User_name'], "WORKER", self.Shop['Shop_name'], self.Shop['Shop_brand_name'], [-2]]
        # e.g [2, 'Abdul Kedir', 'AK Abdul', 'OWNER', 'BELLEMA FASHION', 'ADOT', '10']        
        # e.g [User Id, 'User Full Name', 'User Name', 'OWNER', 'Shop Name', 'Shop Brand', User permission in shop As (WORKER -2, OWNER -1, CUSTOMER 0, NOT WORKING 1)]
        if found_worker_inshop == 0:
            #print("self.selected_user : ", self.selected_user)
            Shop_workers.append([self.selected_user['User_id'], self.selected_user['User_fname'] + " "+ self.selected_user['User_Lname'], self.selected_user['User_name'], "WORKER", self.Shop['Shop_name'], self.Shop['Shop_brand_name'], [-2]])
            #print("Adding worker to shop workers list ", Shop_workers)
            # Update the shop workers in the database
            jsonShop_workers = json.dumps(Shop_workers)
            Shops = Update_Shop(None, self.selected_user, ['Shop_workers'], [jsonShop_workers], ['Shop_Id'], [self.Shop['Shop_Id']])
            if Shops:
                #print("Shop workers Updated Secessfuly", Shops)
                if isinstance(Shops, list):
                    Shops = Shops[0]
                else:
                    Shops = Shops
                for s, shop in enumerate(self.Shops):
                    if shop['Shop_Id'] == self.Shop['Shop_Id']:
                        self.Shop = Shops
                        self.Shops[s] = Shops

        # Now update the User_work_shop field in Users table
        User_work_shops = []
        if self.selected_user and not self.selected_user['User_work_shop'] == None and not self.selected_user['User_work_shop'] == 'None':                            
            #print("self.selected_user['User_work_shop'] ", self.selected_user['User_work_shop'])
            try:
                User_work_shops = json.loads(self.selected_user['User_work_shop'])
            except:
                try:
                    User_work_shops = load_list(self.selected_user['User_work_shop'])
                except:
                    #print("user_work_shop json, load_list can not read it")
                    pass  

        found_shop_inworkes = 0
        for uws, User_work_shop in enumerate(User_work_shops):
            if User_work_shop[0] == self.Shop['Shop_Id']:
                found_shop_inworkes = 1
                User_work_shops[uws] = [self.Shop['Shop_Id'], self.Shop['Shop_name'], self.Shop['Shop_brand_name'], [-1]]
        # e.g [id, 'Shop Name', 'Shop Brand', User permission in shop As (WORKER -2, OWNER -1, CUSTOMER 0, NOT WORKING 1)]

        if found_shop_inworkes == 0:
            #print("Adding shop to user work shops list ", User_work_shops)
            User_work_shops.append([Shops['Shop_Id'], Shops['Shop_name'], Shops['Shop_brand_name'], [-1]])
            # Update the Users table in the database
            #print("Updating user work shops list ", User_work_shops)
            User = Update_User(None, self.selected_user, ['User_work_shop'], [json.dumps(User_work_shops)], ['User_id'], [self.selected_user['User_id']])
            #print("User : ", User)
            self.selected_user['User_work_shop'] = json.dumps(User_work_shops)
        
        self.update_WORKERS_listbox()
        self.show_User(self.selected_user)
                
            
    def hide_add_forme(self):
        self.clear_tool_details_widget()
        self.details_frame.forget()

    # Create the "Change" button
    def show_change_forme(self):
        selected_product = self.worker_docinfo_listbox.selection()
        if selected_product:
            # Get the ID of the selected product
            user_id = self.worker_docinfo_listbox.item(selected_product)['text']
            users = fetch_as_dict_list(self.homemaster.Link, 'SELECT * FROM USERS WHERE User_id=?', (user_id,))
            if users:
                user = users[0]
                self.show_User(user)
            
    def show_User(self, user):
        if user:
            self.selected_shop_id = user_id = user['User_id']
            for work in [a for a in self.Shop_workers if a[0] == user_id]:
                usid, User_Fullname, User_name, typ, shop_name, shop_brand_name, acsess_level = work
                
                #self.selected_id = selected_product
                
                # Clear the current text
                # than add new one
                
                self.name_label.config(text='User Name: '+str(user['User_name']))
                if os.path.exists(MAIN_dir+"\\data\\Users\\" + str(user['User_name']) + "\\ProfileImage.jpg"):
                    img = Image.open(MAIN_dir+"\\data\\Users\\" + str(user['User_name']) + "\\ProfileImage.jpg").resize((100, 100))
                    img = ImageTk.PhotoImage(img)
                    self.User_image_frame.config(image=img)
                    self.User_image_frame.image = img
                else:
                    new_img = Image.open(MAIN_dir+"\\data\\Icon\\no_Profile_image.jpg").resize((100, 100))
                    new_img = ImageTk.PhotoImage(new_img)
                    self.User_image_frame.config(image=new_img)
                    self.User_image_frame.image = new_img
                    
                self.f_and_lname_label.config(text='First and Last Name : '+str(user['User_fname']) + " " +str(user['User_Lname']))
                self.gender_label.config(text='Gender : '+str(user['User_gender']))
                self.email_label.config(text='EMAIL: '+str(user['User_email']))
                self.phone_num_label.config(text='PHONE NUMBER: '+str(user['User_phone_num']))
                #self.id_num_label.config(text='ID Number: '+str(user['User_id_pp_num']))
                self.acsess_entry.insert(0, acsess_level)
                self.add_button.config(text="Update")
                
                self.details_frame.pack(side=tk.RIGHT, fill=tk.Y, expand=False)
                self.load_worker_access()
    
    def search_tools(self, search_text):        
        # Search for the entered text in the code, name, short_key, and type fields of the product table
        results = []
        for Shop_worker in self.Shop_workers:
            if search_text in str(Shop_worker):
                results.append(Shop_worker)
        return results

    def Add_WORKER_listbox(self, workers):
        #print("update_search :"+str(workers)) 
        # Clear the workers listbox
        self.worker_docinfo_listbox.delete(*self.worker_docinfo_listbox.get_children())
        self.worker_docinfo_listbox['columns'] = ('ID', 'First Name', 'Shop Name', 'Type', 'Shop Brand Name', 'ACSSES Level')
        self.worker_docinfo_listbox.heading("#0", text="ID")
        self.worker_docinfo_listbox.heading("#1", text="User Full Name")
        self.worker_docinfo_listbox.heading("#1", text="User Name")
        self.worker_docinfo_listbox.heading("#2", text="Type")
        self.worker_docinfo_listbox.heading("#3", text="Shop Name")
        self.worker_docinfo_listbox.heading("#4", text="Shop Brand Name")
        self.worker_docinfo_listbox.heading("#5", text="ACSSES Level")

        
        # Add the worker to the worker listbox
        for worker in workers:
            if worker[0]:
                workerid = worker[0]
            else:
                workerid = ""
            self.worker_docinfo_listbox.insert('', 'end', text=workerid, values=(worker[1], worker[2], worker[3], worker[4], worker[5], worker[6]))

        
    # create a function to update the search results whenever the search box changes
    def update_search_results(self, *args):
        # get the search string from the search box
        search_str = self.search_var.get()
        
        # search for products based on the search string
        results = self.search_tools(search_str) 
        # clear the current items in the list box
        self.worker_docinfo_listbox.delete(*self.worker_docinfo_listbox.get_children())
        self.Add_WORKER_listbox(results)
        
    # Define the function for updating the product listbox
    def update_WORKERS_listbox(self):
        #print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        # Clear the product listbox
        self.worker_docinfo_listbox.delete(*self.worker_docinfo_listbox.get_children())
        self.Shop_workers = []
        results = []
        for s, shop in enumerate(self.Shops):
            #if self.Selected_Shop != "" and shop['Shop_name'] != self.Selected_Shop:
            #    continue
            if shop['Shop_oweners_id'] and shop['Shop_oweners_id'] != "":
                #print("shop['Shop_oweners_id'] ", shop['Shop_oweners_id'])
                # Fetch the user details for the shop owner
                users = fetch_as_dict_list(self.homemaster.Link, 'SELECT * FROM USERS WHERE User_id=?', (shop['Shop_oweners_id'],))
                if users:
                    users= users[0]
                    self.Shop_workers.append([users['User_id'], users['User_fname'] +" "+users['User_Lname'], users['User_name'], "OWNER", shop['Shop_name'], shop['Shop_brand_name'], "10"])
                    results.append([users['User_id'], users['User_fname'] +" "+users['User_Lname'], users['User_name'], "OWNER", shop['Shop_name'], shop['Shop_brand_name'], "10"])
            

            #print("Shop[0]['Shop_workers'] ", shop['Shop_workers'])
            if shop['Shop_workers'] and shop['Shop_workers'] != "":
                Shop_workers = json.loads(shop['Shop_workers'])
                #print("Shop_workers ", Shop_workers)
                for Shop_worker in Shop_workers: 
                    if Shop_worker[6] == "-2" or Shop_worker[6] == -2:
                        self.Shop_workers.append(Shop_worker)
                        results.append([Shop_worker[0], Shop_worker[1], "Has Sent A Request ", "To Worke ", "?", "", ""])
                    else:
                        self.Shop_workers.append(Shop_worker)
                        results.append(Shop_worker)
                
        self.Add_WORKER_listbox(results)
        # Hide the product details frame
        self.hide_add_forme()
        self.change_button.config(state=tk.DISABLED)

    # Define the function for adding a new product
    def make_change_for_worker(self):
        acsess = self.acsess_entry.get()
        if acsess and not acsess == "":
            for s, shop in enumerate(self.Shops):
                if self.Selected_Shop != "" and shop['Shop_name'] != self.Selected_Shop:
                    continue
                if shop:
                    #print("shop ", shop)
                    Shop_workers = []
                    Shop_workers_copy = []
                    if not shop['Shop_workers'] == None and not shop['Shop_workers'] == 'None':
                        Shop_workers =json.loads(shop['Shop_workers'])
                    #print("Shop_workers ", Shop_workers)
                    # e.g [2, 'Worker Name', 'Worker User Name', 'OWNER', 'Company Name', 'Company Brand', '10']
                    shop_worker_id = ""
                    shop_worker_username = ""
                    for sw, Shop_worker in enumerate(Shop_workers):
                        if Shop_worker[4] == shop['Shop_name'] and Shop_worker[5] == shop['Shop_brand_name']:
                            #print("Shop_worker ", Shop_workers_copy)
                            shop_worker_id = Shop_worker[0]
                            shop_worker_username = Shop_worker[2]
                            #print("shop_worker_id ", shop_worker_id)
                            Shop_worker[6] = acsess
                        Shop_workers_copy.append(Shop_worker)
                    users = None
                    #print("Shop_workers_copy ", Shop_workers_copy)
                    if not shop_worker_id == "":
                        users = fetch_as_dict_list(self.homemaster.Link, 'SELECT * FROM USERS WHERE User_id=?', (str(shop_worker_id),))
                    
                    if users:
                        user = users[0]
                        #print("Shop_workers_copy ", Shop_workers_copy)
                        #print("user ", user)
                        Update_Shop(None, users, ['Shop_workers'], [json.dumps(Shop_workers_copy)], ['Shop_id'], [shop['Shop_Id']])
                        self.Shops[s]['Shop_workers'] = json.dumps(Shop_workers_copy)
                        
                        User_work_shops = []
                        if user and not user['User_work_shop'] == None and not user['User_work_shop'] == 'None':
                            User_work_shops = json.loads(user['User_work_shop'])
                        #print("User_work_shops ", User_work_shops)
                        User_work_shops_copy = []
                        # [Shops['Shop_Id'], Shops['Shop_name'], Shops['Shop_brand_name'], [-1]]
                        for uws, User_work_shop in enumerate(User_work_shops):
                            if User_work_shop[0] == shop['Shop_Id'] and  User_work_shop[1] == shop['Shop_name'] and  User_work_shop[2] == shop['Shop_brand_name']:
                                if User_work_shop[3] and len(User_work_shop[3]):
                                    User_work_shop[3][0] = acsess
                                else:
                                    User_work_shop[3] = [acsess]
                            User_work_shops_copy.append(User_work_shop)
                        #print("User_work_shops_copy ", User_work_shops_copy)
                        Update_User(None, users, ['User_work_shop'], [json.dumps(User_work_shops_copy)], ['User_id'], [user['User_id']])

        # Update the product listbox
        self.update_WORKERS_listbox()
        
    # Define the function for deleting a product
    def Remove_worker(self):
        selected_product = self.worker_docinfo_listbox.selection()
        if selected_product:
            # Get the ID of the selected product
            user_id = self.worker_docinfo_listbox.item(selected_product)['text']
            users = fetch_as_dict_list(self.homemaster.Link, 'SELECT * FROM USERS WHERE User_id=?', (user_id,))
            if users:
                user = users[0]
                User_work_shops = [] # all working palce 
                if user and not user['User_work_shop'] == None and not user['User_work_shop'] == 'None':
                    User_work_shops = json.loads(user['User_work_shop'])
                #print("User_work_shops ", User_work_shops)
                User_work_shops_copy = [] # it will live spacific shop and holled all working pace
                # [Shops['Shop_Id'], Shops['Shop_name'], Shops['Shop_brand_name'], [-1]]
                for uws, User_work_shop in enumerate(User_work_shops):
                    if User_work_shop[0] == self.Shop['Shop_Id'] and  User_work_shop[1] == self.Shop['Shop_name'] and  User_work_shop[2] == self.Shop['Shop_brand_name']:
                        continue
                        User_work_shops_copy.append(User_work_shop)
                #print("User_work_shops_copy ", User_work_shops_copy)
                Update_User(None, users, ['User_work_shop'], [json.dumps(User_work_shops_copy)], ['User_id'], [user['User_id']])
                Shop_workers = [] # all workers info holder
                Shop_workers_copy = [] # it will live that user working shop and hold all workers info
                if not self.Shop['Shop_workers'] == None and not self.Shop['Shop_workers'] == 'None':
                    Shop_workers =json.loads(self.Shop['Shop_workers'])
                #print("Shop_workers ", Shop_workers)
                # e.g [2, 'Worker Name', 'Worker User Name', 'OWNER', 'Company Name', 'Company Brand', '10']
                shop_worker_id = ""
                shop_worker_username = ""
                for sw, Shop_worker in enumerate(Shop_workers):
                    if Shop_worker[0] == user['User_id'] and Shop_worker[2] == user['User_name']:
                        continue
                    Shop_workers_copy.append(Shop_worker)
                #print("Shop_workers_copy ", Shop_workers_copy)
                Update_Shop(None, users, ['Shop_workers'], [json.dumps(Shop_workers_copy)], ['Shop_id'], [self.Shop['Shop_Id']])
                #user['User_work_shop']
                self.Shop['Shop_workers'] = json.dumps(Shop_workers_copy)
                        
        # Update the product listbox
        self.update_WORKERS_listbox()


    def on_select(self, event):
        #print("onselect")
        if len(event.widget.selection()) > 0:
            self.change_button.config(state=tk.NORMAL)
            self.delete_button.config(state=tk.NORMAL)
        else:
            self.change_button.config(state=tk.DISABLED)
            self.delete_button.config(state=tk.DISABLED)

