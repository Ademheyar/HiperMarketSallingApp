import tkinter as tk
from tkinter import ttk
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
conn = sqlite3.connect(db_path)
cur = conn.cursor()

conn.commit()

from D.Getdefsize import ButtonEntryApp
from C.List import *

from C.API.Get import *
from D.printer import *
from D.GetVALUE import GetvalueForm
# Connect to the database or create it if it does not exist

from C.List import *
from D.Getdate import GetDateForm
from D.Chart.Chart import *

from C.API.Get import *

from C.Product.selecttype import *

access_types=["Add Unknown Item", # 0                        1
              "Void Order", # 0                              2
              "Change Activets", # 0                         3
              "SALLING", # 0                                 4
              "DELETE ITEM", # 0                             5
              "VOIDE ORDER", # 0                             6
              "ADD NEW ORDER", # 0                           7
              "NEXT ORDER", # 0                              8
              "PREVEUSE ORDER", # 0                          9
              "SEARCH ITEM", # 0                             10
              "UPLOAD", # 0                                  11
              # TODO: add payment tools type access
              "Give Credit", # 0                             12

              
              "CASH IN", # 1                                 13
              "CREADIT", # 1                                 14
              "SEARCH USER", # 1                              15
              "CREATE COSTUMER INFO", # 1                     16
              "MANAGER", # 1                                  17
              "OPEN CHASH DROWER", # 1                        18
              "SEARCH PRODUCTES", # 1                          19
              "CREATE PRODUCT", # 1                            20
              "GIVE PRODUCT PRICE", # 1                         21
              "CHANGE PRODUCTE PRICE", # 1                      22
              "GIVE PRODUCT STOCK", # 1                         23
              "CREAT TOOLS", # 1                                24
              "EXCHANGE RECORDED DOCUMENT ITEMS TO SAME ITEM", # 1                                25
              "CHANGE PRODUCTS TYPE", # 1                                26

              "CHANGE PRODUCTE STOCK", # 2                                27
              "CREATE NEW WORKER INFO", # 2                                28
              "CHANGE COSTUMER INFO", # 2                                29
              "REMOVE COSTUMER INFO", # 2                                30
              "CHANGE TOOLES", # 2                                31
              "REMOVE TOOLES", # 2                                32
              "EXCHANGE RECORDED DOCUMENT PAYMENT TYPE", # 2                                33
              "EXCHANGE RECORDED DOCUMENT ITEM TO DEFFERNT", # 2                                34
              "CHANGE SLIP SETTING", # 2                                35
              "CHANGE TOOLS SETTING", # 2                                36
              "CHANGE STOCK SETTING", # 2                                37
              "CHANGE USER SETTING", # 2                                38

              "REMOVE PRODUCTES", # 3                                   39
              "SHOW PRODUCTES COST", # 3                                40
              "SEARCH DOCUMENTS", # 3                                41
              "SHOW DOCUMENTS", # 3                                42
              "CHANGE PRODUTS", # 3                                43
              "DELETE PRODUTS", # 3                                44
              "CHANGE STOCK SETTING", # 3                                45
              "CHANGE DOCUMENT SETTING", # 3                        46

              "REMOVE DOCUMENT", # 4                                47
              "SHOW REPORTS", # 4                                48
              "SHOW TOTAL SALE", # 4                                49
              "CHANGE USER TYPE", # 4                                50
              "CREATE ADMINS USERS", # 4                                51
              "REMOVE DOCUMENTS", # 4                                52
              "CHANGE DOCUMENTS", # 4                                53
              "CHANGE USER INFO", # 4                                54
              "CHANGE SHOP SETTING" # 4                                55
              ]
class WorkersForm(tk.Frame):
    def __init__(self, master, User, Shops):
        tk.Frame.__init__(self, master)
        self.Selected_Shop = ""
        self.User = User
        self.Shops = Shops
        self.Shop_workers = []
        
        # Create the search bar
        # Create the frame for the search bar and buttons
        self.search_frame = tk.Frame(self)
        self.search_frame.pack(side=tk.TOP, padx=5, pady=5)

        # create a StringVar to represent the search box
        self.search_var = tk.StringVar()
        self.search_entry = tk.Entry(self.search_frame, textvariable=self.search_var)
        self.search_entry.bind('<KeyRelease>', self.update_search_results)
        self.search_entry.pack(side=tk.LEFT, padx=5, pady=5)
            
        # bind the update_search_results function to the search box
        self.search_var.trace("w", self.update_search_results)

        # Create the list box
        self.l_frame = tk.Frame(self)
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
        self.details_frame = tk.Frame(self.worker_docinfo_listbox)
        self.details_frame.pack_forget()
        self.selected_shop_name = ""
        self.selected_id = ""
        self.main_name = ""
        
        self.selected_shop_id = ""
        
        # Create the widgets for the worker details
        
        self.name_label = tk.Label(self.details_frame, text='User Name:')
        self.f_and_lname_label = tk.Label(self.details_frame, text='First and Last Name :')
        self.gender_label = tk.Label(self.details_frame, text='Gender :')
        self.email_label = tk.Label(self.details_frame, text='EMAIL:')
        self.phone_num_label = tk.Label(self.details_frame, text='PHONE NUMBER:')
        self.id_num_label = tk.Label(self.details_frame, text='ID Number:')
        self.cuntry_label = tk.Label(self.details_frame, text='Cuntry :')
        self.addres_label = tk.Label(self.details_frame, text='Adress :')
        self.home_no_label = tk.Label(self.details_frame, text='Home No :')
        self.type_label = tk.Label(self.details_frame, text='Type :')
        self.acsess_label = tk.Label(self.details_frame, text='ACSSES :')
        # create a StringVar to represent the search box
        self.acsess_var = tk.StringVar()
        self.acsess_entry = tk.Entry(self.details_frame, textvariable=self.acsess_var)
        # bind the update_search_results function to the search box
        self.acsess_var.trace("w", lambda g1,g2,g3: self.load_worker_access())
        
        # Create the listbox to display search results
        self.worker_access_list_forme = tk.Frame(self.details_frame)
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
        
        self.add_button = tk.Button(self.details_frame, text='Add', command=self.make_change_for_worker)
        self.cancle_button = tk.Button(self.details_frame, text='Cancle', command=self.hide_add_forme)
        
        self.add_new_button = tk.Button(self.search_frame, text='New Worker', command=self.show_add_forme)
        self.add_new_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.change_button = tk.Button(self.search_frame, text='Change', command=self.show_change_forme)
        self.change_button.pack(side=tk.LEFT, padx=5, pady=5)
        self.change_button.config(state=tk.DISABLED)

        self.delete_button = tk.Button(self.search_frame, text='Delete', command=self.delete_tool)
        self.delete_button.pack(side=tk.LEFT, padx=5, pady=5)
        self.delete_button.config(state=tk.DISABLED)


        
        # Pack the widgets for the user details
        self.name_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.E)
        self.f_and_lname_label.grid(row=1, column=0, padx=5, pady=5, sticky=tk.E)
        self.gender_label.grid(row=2, column=0, padx=5, pady=5, sticky=tk.E)
        self.cuntry_label.grid(row=3, column=0, padx=5, pady=5, sticky=tk.E)
        self.phone_num_label.grid(row=4, column=0, padx=5, pady=5, sticky=tk.E)
        self.email_label.grid(row=5, column=0, padx=5, pady=5, sticky=tk.E)
        self.addres_label.grid(row=6, column=0, padx=5, pady=5, sticky=tk.E)
        self.id_num_label.grid(row=7, column=0, padx=5, pady=5, sticky=tk.E)
        self.home_no_label.grid(row=8, column=0, padx=5, pady=5, sticky=tk.E)
        self.type_label.grid(row=9, column=0, padx=5, pady=5, sticky=tk.E)
        self.acsess_label.grid(row=10, column=0, padx=5, pady=5, sticky=tk.E)
        self.acsess_entry.grid(row=10, column=1, padx=5, pady=5, sticky=tk.W)

        self.worker_access_list_forme.grid(row=11, column=0, padx=5, pady=5, sticky=tk.W)
        
        self.add_button.grid(row=11, column=1, padx=5, pady=5, sticky=tk.W)
        self.cancle_button.grid(row=11, column=2, padx=5, pady=5, sticky=tk.W)
        self.update_WORKERS_listbox()
        self.load_worker_access()
        
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
                        print("user work leve " + str(get_level) + " <= acces level" +str(self.Shop_Security_Levels[l]))
                        if str(self.Shop_Security_Levels[l]) <= str(self.acsess_entry.get()):
                            self.worker_access_listbox.insert('', 'end', text=Level)
                    
    def show_tools_form(self):
        # call the function in the main file to show the first frame
        self.master.master.show_frame("ToolForm")
    
    def clear_tool_details_widget(self):
        # Clear the user details widgets
        self.name_label.config(text='User Name:')
        self.f_and_lname_label.config(text='First and Last Name :')
        self.gender_label.config(text='Gender :')
        self.email_label.config(text='EMAIL:')
        self.phone_num_label.config(text='PHONE NUMBER:')
        self.id_num_label.config(text='ID Number:')
        self.cuntry_label.config(text='Cuntry :')
        self.addres_label.config(text='Adress :')
        self.home_no_label.config(text='Home No :')
        self.type_label.config(text='Type :')
        self.acsess_entry.delete(0, "end")
        
    # Create the "Add New" button
    def show_add_forme(self):
        self.clear_tool_details_widget()
        self.on_name_entry(None)
        self.details_frame.pack(side=tk.RIGHT, fill=tk.Y, expand=False)
        
    def hide_add_forme(self):
        self.clear_tool_details_widget()
        self.details_frame.forget()

    # Create the "Change" button
    def show_change_forme(self):
        selected_product = self.worker_docinfo_listbox.selection()
        if selected_product:
            # Get the ID of the selected product
            
            user_id = self.worker_docinfo_listbox.item(selected_product)['text']
            usid, User_Fullname, User_name, typ, shop_name, shop_brand_name, acsess_level = [a for a in self.Shop_workers if a[0] == user_id][0]
            users = fetch_as_dict_list( 'SELECT * FROM USERS WHERE User_id=?', (user_id,))
            if users:
                user = users[0]
                self.selected_shop_id = user['User_id']
                self.selected_shop_name = shop_name
                
                self.selected_id = selected_product
                
                # Clear the current text
                # than add new one
                
                self.name_label.config(text='User Name: '+str(user['User_name']))
                self.f_and_lname_label.config(text='First and Last Name : '+str(user['User_fname']) + " " +str(user['User_Lname']))
                self.gender_label.config(text='Gender : '+str(user['User_gender']))
                self.email_label.config(text='EMAIL: '+str(user['User_email']))
                self.phone_num_label.config(text='PHONE NUMBER: '+str(user['User_phone_num']))
                #self.id_num_label.config(text='ID Number: '+str(user['User_id_pp_num']))
                self.cuntry_label.config(text='Cuntry : '+str(user['User_country']))
                self.addres_label.config(text='Adress : '+str(user['User_address']))
                self.home_no_label.config(text='Home No : '+str(user['User_home_no']))
                self.type_label.config(text='Type : '+str(typ))
                self.acsess_entry.insert(0, acsess_level)
                self.add_button.config(text="Update")
                # Commit the changes to the database
                conn.commit()
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
        print("update_search :"+str(workers)) 
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
            self.worker_docinfo_listbox.insert('', 'end', text=worker[0], values=(worker[1], worker[2], worker[3], worker[4], worker[5], worker[6]))

        
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
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        # Clear the product listbox
        self.worker_docinfo_listbox.delete(*self.worker_docinfo_listbox.get_children())
        self.Shop_workers = []
        results = []
        for s, shop in enumerate(self.Shops):
            #if self.Selected_Shop != "" and shop['Shop_name'] != self.Selected_Shop:
            #    continue
            if shop['Shop_oweners_id'] and shop['Shop_oweners_id'] != "":
                print("shop['Shop_oweners_id'] ", shop['Shop_oweners_id'])
                # Fetch the user details for the shop owner
                cur.execute('SELECT * FROM USERS WHERE User_id=?', (shop['Shop_oweners_id'],))
                users = cur.fetchall()
                if users:
                    self.Shop_workers.append([users[0][0], users[0][1] +" "+users[0][2], users[0][3], "OWNER", shop['Shop_name'], shop['Shop_brand_name'], "10"])
                    results.append([users[0][0], users[0][1] +" "+users[0][2], users[0][3], "OWNER", shop['Shop_name'], shop['Shop_brand_name'], "10"])
            

            print("Shop[0]['Shop_workers'] ", shop['Shop_workers'])
            if shop['Shop_workers'] and shop['Shop_workers'] != "":
                Shop_workers = json.loads(shop['Shop_workers'])
                print("Shop_workers ", Shop_workers)
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
                    print("shop ", shop)
                    Shop_workers = []
                    Shop_workers_copy = []
                    if not shop['Shop_workers'] == None and not shop['Shop_workers'] == 'None':
                        Shop_workers =json.loads(shop['Shop_workers'])
                    print("Shop_workers ", Shop_workers)
                    # e.g [2, 'Worker Name', 'Worker User Name', 'OWNER', 'Company Name', 'Company Brand', '10']
                    shop_worker_id = ""
                    shop_worker_username = ""
                    for sw, Shop_worker in enumerate(Shop_workers):
                        if Shop_worker[4] == shop['Shop_name'] and Shop_worker[5] == shop['Shop_brand_name']:
                            print("Shop_worker ", Shop_workers_copy)
                            shop_worker_id = Shop_worker[0]
                            shop_worker_username = Shop_worker[2]
                            print("shop_worker_id ", shop_worker_id)
                            Shop_worker[6] = acsess
                        Shop_workers_copy.append(Shop_worker)
                    users = None
                    if not shop_worker_id == "":
                        users = fetch_as_dict_list( 'SELECT * FROM USERS WHERE User_id=?', (str(shop_worker_id)))
                    
                    if users:
                        user = users[0]
                        print("Shop_workers_copy ", Shop_workers_copy)
                        print("user ", user)
                        cur.execute('UPDATE Shops SET Shop_workers=? WHERE Shop_id=?', (json.dumps(Shop_workers_copy), shop['Shop_id']))
                        # Commit the changes to the database
                        conn.commit()
                        self.Shops[s]['Shop_workers'] = json.dumps(Shop_workers_copy)
                        
                        User_work_shops = []
                        if user and not user['User_work_shop'] == None and not user['User_work_shop'] == 'None':
                            User_work_shops = json.loads(user['User_work_shop'])
                        print("User_work_shops ", User_work_shops)
                        User_work_shops_copy = []
                        # [Shops['Shop_id'], Shops['Shop_name'], Shops['Shop_brand_name'], [-1]]
                        for uws, User_work_shop in enumerate(User_work_shops):
                            if User_work_shop[0] == shop['Shop_id'] and  User_work_shop[1] == shop['Shop_name'] and  User_work_shop[2] == shop['Shop_brand_name']:
                                if User_work_shop[3] and len(User_work_shop[3]):
                                    User_work_shop[3][0] = acsess
                                else:
                                    User_work_shop[3] = [acsess]
                            User_work_shops_copy.append(User_work_shop)
                        print("User_work_shops_copy ", User_work_shops_copy)

                        cur.execute('UPDATE Users SET User_work_shop=? WHERE User_id=?', (json.dumps(User_work_shops_copy), user['User_id']))
                        # Commit the changes to the database
                        conn.commit()
        # Update the product listbox
        self.update_WORKERS_listbox()
        
    # Define the function for deleting a product
    def delete_tool(self):
        # Get the selected product from the listbox
        selected_product = self.worker_docinfo_listbox.selection()
        
        if selected_product:
            # Get the ID of the selected product
            product_id = self.worker_docinfo_listbox.item(selected_product)['values'][0]

            # Delete the product from the database
            cur.execute('DELETE FROM tools WHERE name=?', (product_id,))

            # Commit the changes to the database
            conn.commit()

            # Clear the product details widgets
            self.clear_tool_details_widget()

            # Update the product listbox
            self.update_WORKERS_listbox()












    def on_name_entry(self, event):
        cur.execute('SELECT * FROM tools')
        products = cur.fetchall()
        for product in products:
            if product[1] == self.name_entry.get():
                self.add_button.config(text="Update")    
                return
        if self.main_name == self.name_entry.get() and not self.main_name == "":
            self.add_button.config(text="Update")
        else:
            self.add_button.config(text="New")

    def on_select(self, event):
        print("onselect")
        if len(event.widget.selection()) > 0:
            self.change_button.config(state=tk.NORMAL)
            self.delete_button.config(state=tk.NORMAL)
        else:
            self.change_button.config(state=tk.DISABLED)
            self.delete_button.config(state=tk.DISABLED)

