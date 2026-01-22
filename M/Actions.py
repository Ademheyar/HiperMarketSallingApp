import tkinter as tk
from tkinter import ttk
import sqlite3
import shutil
import datetime
import os
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
from C.Sql3 import *
from D.searchbox import search_entry

# Connect to the database or create it if it does not exist

import os
data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data'))
db_path = os.path.join(data_dir, 'my_database.db')
conn = sqlite3.connect(db_path)
cur = conn.cursor()

conn.commit()

import tkinter as tk
from D.Getdate import GetDateForm
from D.Chart.Chart import *

from C.Product.selecttype import *

def is_float(value):
    try:
        print()
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
    
    print(query+"\n")
    # Execute the SQL query and return the results as a list of tuples
    cur.execute(query, (*given,))
    results = cur.fetchall()
    return results
# Example node hierarchy

class ActionsForm(tk.Frame):
    def __init__(self, master, user, Shops, Shops_info):
        tk.Frame.__init__(self, master)
        self.master = master
        self.user_info = user
        self.user = user
        self.Shops = Shops
        self.Shops_info = Shops_info
        self.Shop_Actions = []
        
        self.start_value = datetime.datetime.now().strftime('%Y-%m-%d')
        self.end_value = self.start_value
        
        self.Selected_Shop = ""
        
        self.homemaster = self
        p = 0
        while(True):
            p += 1
            print("chacking parent p = " + str(p))
            if hasattr(self.homemaster, 'Shops_info') and hasattr(self.homemaster, 'onDisplayFrame'):
                break
            else:
                self.homemaster = self.homemaster.master
        #print("produ user : " + str(user))
        
        self.Actions_notebook = ttk.Notebook(self)
        self.Actions_notebook.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.nested_list = []

        # Create the frame for the product details
        self.Actions_list_frame = tk.Frame(self.Actions_notebook)
        self.Actions_list_frame.pack()
        self.Actions_notebook.add(self.Actions_list_frame, text="Actions")

        # Create the search bar
        # Create the frame for the search bar and buttons
        self.search_frame = tk.Frame(self.Actions_list_frame)
        self.search_frame.pack(side=tk.TOP, padx=5, pady=5)

        # create a StringVar to represent the search box
        self.search_var = tk.StringVar()
        self.search_entry = tk.Entry(self.search_frame, textvariable=self.search_var)
        self.search_entry.bind('<KeyRelease>', self.update_search_results)
        self.search_entry.pack(side=tk.LEFT, padx=5, pady=5)
            
        # bind the update_search_results function to the search box
        self.search_var.trace("w", self.update_search_results)
        
        self.add_new_button = tk.Button(self.search_frame, text='New Action', command=self.show_add_forme)
        self.add_new_button.pack(side=tk.LEFT, padx=5, pady=5)
        self.change_button = tk.Button(self.search_frame, text='Change', command=self.show_change_forme)
        self.change_button.pack(side=tk.LEFT, padx=5, pady=5)
        self.change_button.config(state=tk.DISABLED)
        self.delete_button = tk.Button(self.search_frame, text='Delete', command=self.delete_action)
        self.delete_button.pack(side=tk.LEFT, padx=5, pady=5)
        self.refresh_button = tk.Button(self.search_frame, text='Refresh', command= lambda :self.update_search_results([None, None]))
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
        self.details_frame = tk.Frame(self.notebook_frame)
        self.details_frame.pack()
        self.notebook_frame.add(self.details_frame)


        # Create the widgets for the product details
        
        self.Action_label = tk.Label(self.details_frame, text='Action Label : ')
        self.Action_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.E)
        
        self.Action_label_entry = tk.Entry(self.details_frame)
        self.Action_label_entry.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)
        
        self.Action_created_date_label = tk.Label(self.details_frame, text='Action Created Date : '+self.start_value)
        self.Action_created_date_label.grid(row=1, column=0, columnspan=4, padx=5, pady=5, sticky=tk.W)
        
        self.From_Date_label = tk.Label(self.details_frame, text='From_Date:')
        self.From_Date_label.grid(row=2, column=0, padx=5, pady=5, sticky=tk.E)
        self.From_Date_entry = tk.Entry(self.details_frame)
        self.From_Date_entry.grid(row=2, column=1, padx=5, pady=5, sticky=tk.W)
        self.TO_Date_label = tk.Label(self.details_frame, text='TO_Date:')
        self.TO_Date_label.grid(row=2, column=2, padx=5, pady=5, sticky=tk.E)
        self.TO_Date_entry = tk.Entry(self.details_frame)
        self.TO_Date_entry.grid(row=2, column=3, padx=5, pady=5, sticky=tk.W)
        
        self.add_button = tk.Button(self.details_frame, text='Add', command=self.Save_Shop_Actions)
        self.add_button.grid(row=26, column=0, padx=5, pady=5, sticky=tk.W)
        self.cancle_button = tk.Button(self.details_frame, text='Cancle', command=self.hide_add_forme)
        self.cancle_button.grid(row=26, column=1, padx=5, pady=5, sticky=tk.W)
      
      
        
        # Create the frame for the product details
        self.ifdetails_frame = tk.Frame(self.notebook_frame)
        self.ifdetails_frame.pack()
        self.notebook_frame.add(self.ifdetails_frame, text='If :')
        
        self.ifSelected_items = []
        # Create a label and an entry widget for the search box
        self.search_label = tk.Label(self.ifdetails_frame, text="Search:", font=("Arial", 12))
        self.search_label.grid(row=0, column=0, sticky="w")
        self.search_entry = search_entry(self.ifdetails_frame, self.Shops_info, self.user, self.Shops, font=("Arial", 12))
        #tk.Entry
        self.search_entry.grid(row=1, column=0, columnspan=4)
        
        # * New frame next to list_items in the main frame
        self.ifmidel_frame = tk.Frame(self.ifdetails_frame)
        self.ifmidel_frame.grid(row=2, column=0, columnspan=10, sticky="nsew")
        
        self.ifextrnal_frame = tk.Frame(self.ifmidel_frame)
        self.ifextrnal_frame.pack(side="top", fill="x")




        self.ifFrame_contaner_frame = tk.Frame(self.ifmidel_frame)
        self.ifFrame_contaner_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.ifList_Frame_contaner_frame = tk.Frame(self.ifFrame_contaner_frame)
        self.ifList_Frame_contaner_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.ifList_Frame = tk.Frame(self.ifList_Frame_contaner_frame)
        self.ifList_Frame.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        
        self.ifitem_List_canvas = tk.Canvas(self.ifList_Frame)
        self.ifitem_List_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        
        self.ifitem_List_yscrollbar = tk.Scrollbar(self.ifList_Frame, orient='vertical', command=self.ifitem_List_canvas.yview)
        self.ifitem_List_yscrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.ifitem_List_xscrollbar = tk.Scrollbar(self.ifList_Frame_contaner_frame, orient='horizontal', command=self.ifitem_List_canvas.xview)
        self.ifitem_List_xscrollbar.pack(side=tk.TOP, fill=tk.X)
        
        self.ifitem_List_canvas.configure(xscrollcommand=self.ifitem_List_xscrollbar.set, yscrollcommand=self.ifitem_List_yscrollbar.set)
        #self.New_item_contener_canvas.bind('<Configure>', lambda e: self.New_item_contener_canvas.configure(scrollregion=self.New_item_contener_canvas.bbox("all")))

        self.ifSelected_item_Display_frame = tk.Frame(self.ifitem_List_canvas)
        self.ifitem_List_canvas.create_window((0, 0), window=self.ifSelected_item_Display_frame, anchor=tk.NW)
        self.ifSelected_item_Display_frame.bind('<Configure>', lambda e: self.ifitem_List_canvas.configure(scrollregion=self.ifitem_List_canvas.bbox("all")))
        
        self.ifProduct_Make_price_label = tk.Label(self.ifdetails_frame, text='IF Total price : ')
        self.ifProduct_Make_price_label.grid(row=12, column=0, padx=5, pady=5, sticky=tk.E)
        self.ifProduct_Make_price_entry = tk.Entry(self.ifdetails_frame)
        self.ifProduct_Make_price_entry.grid(row=12, column=1, padx=5, pady=5, sticky=tk.W)
        self.ifProduct_Make_Total_price_label = tk.Label(self.ifdetails_frame, text='If Total Discount :')
        self.ifProduct_Make_Total_price_label.grid(row=13, column=0, padx=5, pady=5, sticky=tk.E)
        self.ifProduct_Make_Total_price_entry = tk.Entry(self.ifdetails_frame)
        self.ifProduct_Make_Total_price_entry.grid(row=13, column=1, padx=5, pady=5, sticky=tk.W)
        self.ifProduct_Make_Discount_label = tk.Label(self.ifdetails_frame, text='If Total Items QTY : ')
        self.ifProduct_Make_Discount_label.grid(row=14, column=0, padx=5, pady=5, sticky=tk.E)
        self.ifProduct_Make_Discount_entry = tk.Entry(self.ifdetails_frame)
        self.ifProduct_Make_Discount_entry.grid(row=14, column=1, padx=5, pady=5, sticky=tk.W)
        self.ifProduct_Make_Total_Disc_label = tk.Label(self.ifdetails_frame, text='If Total Profite : ')
        self.ifProduct_Make_Total_Disc_label.grid(row=15, column=0, padx=5, pady=5, sticky=tk.E)
        self.ifProduct_Make_Total_Disc_entry = tk.Entry(self.ifdetails_frame)
        self.ifProduct_Make_Total_Disc_entry.grid(row=15, column=1, padx=5, pady=5, sticky=tk.W)
        

        # Create the frame for the product details
        self.Dodetails_frame = tk.Frame(self.notebook_frame)
        self.Dodetails_frame.pack()
        self.notebook_frame.add(self.Dodetails_frame, text='Do :')        
        
        # Create a label and an entry widget for the search box
        self.Dosearch_label = tk.Label(self.Dodetails_frame, text="Search:", font=("Arial", 12))
        self.Dosearch_label.grid(row=0, column=0, sticky="w")
        self.Dosearch_entry = search_entry(self.Dodetails_frame, self.Shops_info, self.user, self.Shops, font=("Arial", 12))
        #tk.Entry
        self.Dosearch_entry.grid(row=1, column=0, columnspan=4, sticky="nsew")


        self.doSelected_items = []
        # * New frame next to list_items in the main frame
        self.domidel_frame = tk.Frame(self.Dodetails_frame)
        self.domidel_frame.grid(row=2, column=0, columnspan=10, sticky="nsew")
        
        self.doextrnal_frame = tk.Frame(self.domidel_frame)
        self.doextrnal_frame.pack(side="top", fill="x")




        self.doFrame_contaner_frame = tk.Frame(self.domidel_frame)
        self.doFrame_contaner_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.doList_Frame_contaner_frame = tk.Frame(self.doFrame_contaner_frame)
        self.doList_Frame_contaner_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.doList_Frame = tk.Frame(self.doList_Frame_contaner_frame)
        self.doList_Frame.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        
        self.doitem_List_canvas = tk.Canvas(self.doList_Frame)
        self.doitem_List_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        
        self.doitem_List_yscrollbar = tk.Scrollbar(self.doList_Frame, orient='vertical', command=self.doitem_List_canvas.yview)
        self.doitem_List_yscrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.doitem_List_xscrollbar = tk.Scrollbar(self.doList_Frame_contaner_frame, orient='horizontal', command=self.doitem_List_canvas.xview)
        self.doitem_List_xscrollbar.pack(side=tk.TOP, fill=tk.X)
        
        self.doitem_List_canvas.configure(xscrollcommand=self.doitem_List_xscrollbar.set, yscrollcommand=self.doitem_List_yscrollbar.set)
        #self.New_item_contener_canvas.bind('<Configure>', lambda e: self.New_item_contener_canvas.configure(scrollregion=self.New_item_contener_canvas.bbox("all")))

        self.doSelected_item_Display_frame = tk.Frame(self.doitem_List_canvas)
        self.doitem_List_canvas.create_window((0, 0), window=self.doSelected_item_Display_frame, anchor=tk.NW)
        self.doSelected_item_Display_frame.bind('<Configure>', lambda e: self.doitem_List_canvas.configure(scrollregion=self.doitem_List_canvas.bbox("all")))

        self.doProduct_Make_price_label = tk.Label(self.Dodetails_frame, text='Make Total price : ')
        self.doProduct_Make_price_label.grid(row=12, column=0, padx=5, pady=5, sticky=tk.E)
        self.doProduct_Make_price_entry = tk.Entry(self.Dodetails_frame)
        self.doProduct_Make_price_entry.grid(row=12, column=1, padx=5, pady=5, sticky=tk.W)
        self.doProduct_Make_Total_price_label = tk.Label(self.Dodetails_frame, text='Make Total Discount :')
        self.doProduct_Make_Total_price_label.grid(row=13, column=0, padx=5, pady=5, sticky=tk.E)
        self.doProduct_Make_Total_price_entry = tk.Entry(self.Dodetails_frame)
        self.doProduct_Make_Total_price_entry.grid(row=13, column=1, padx=5, pady=5, sticky=tk.W)
        
        # Pack the widgets for the product tab2
        #self.update_product_listbox()
        #
        self.update_search_results([None, None])
        self.update_Shop_Actions_listbox()

        
    def show_product_form(self):
        # call the function in the main file to show the first frame
        self.master.master.show_frame("ActionsForm")
    
    def clear_Shop_Actions_widget(self):
        # Clear the product details widgets
        
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
        for Shop_Payment_Tool in self.Shop_Actions:
            if search_text in str(Shop_Payment_Tool):
                results.append(Shop_Payment_Tool)
        return results

    def Add_tool_listbox(self, results):
        print("update_search :"+str(results))
        self.list_box['columns'] = ("Shop_Actions Id", "Shop_Actions Titel", "Created Date", "From", "To")
        self.list_box.heading("#0", text="Shop_Actions Id")
        self.list_box.heading("#1", text="Shop_Actions Titel")
        self.list_box.heading("#2", text="Created Date")
        self.list_box.heading("#3", text="From")
        self.list_box.heading("#4", text="To")

        # Add the products to the product listbox
        for num, product in enumerate(self.Shop_Actions):
            #print("product :"+str(product))
            print("product 4 :"+str(product[4]))
            print("product 5 :"+str(product[5]))
            print("product 5 :"+str(product[5][1]))
            print("product :"+str(len(product)))
            self.list_box.insert('', 'end', text=product[0], values=(product[1], product[2], product[3], product[4], num))
        
    # create a function to update the search results whenever the search box changes
    def update_search_results(self, *args):
        # get the search string from the search box
        search_str = self.search_var.get()
        
        # search for products based on the search string
        results = self.search_products(search_str)
        
        # clear the current items in the list box
        self.list_box.delete(*self.list_box.get_children())

        self.Add_tool_listbox(results)

    # Define the function for updating the product listbox
    def update_Shop_Actions_listbox(self):
        # Clear the product listbox
        self.list_box.delete(*self.list_box.get_children())
        self.Shop_Actions = []
        results = []
        for s, shop in enumerate(self.Shops):
            if self.Selected_Shop != "" and shop['Shop_name'] != self.Selected_Shop:
                continue

            Shop = fetch_as_dict_list(cur, "SELECT * FROM Shops WHERE Shop_id=? AND Shop_name=? AND Shop_brand_name=?", 
                                (str(shop['Shop_id']), str(shop['Shop_name']), str(shop['Shop_brand_name'])))
            if Shop and Shop[0] and Shop[0]['Shop_Actions'] and Shop[0]['Shop_Actions'] != "":
                print("Shop[0]['Shop_Actions'] ", Shop[0]['Shop_Actions'])
                '''cur.execute("UPDATE Shops SET Shop_Actions=? WHERE Shop_id=? AND Shop_name=? AND Shop_brand_name=?", 
                                (str(json.dumps([])), str(shop['Shop_id']), str(shop['Shop_name']), str(shop['Shop_brand_name'])))
                # Commit the changes to the database
                conn.commit()'''
                Shop_Actions = json.loads(Shop[0]['Shop_Actions'])
                # Add the products to the product listbox
                for Shop_Payment_Tool in Shop_Actions:
                    self.Shop_Actions.append(Shop_Payment_Tool)
                    results.append(Shop_Payment_Tool)
        self.Add_tool_listbox(results)
        # Hide the product details frame
        self.hide_add_forme()
        self.change_button.config(state=tk.DISABLED)
    
    

    def on_select(self, event):
        if len(event.widget.selection()) > 0:
            self.change_button.config(state=tk.NORMAL)
            self.delete_button.config(state=tk.NORMAL)
        else:
            self.change_button.config(state=tk.DISABLED)
            self.delete_button.config(state=tk.DISABLED)

    # Define the function for deleting a product
    def delete_action(self):
        # Get the selected product from the listbox
        selected_action = self.list_box.selection()

        if selected_action:
            # Get the ID of the selected product
            action_id = self.list_box.item(selected_action)['values'][0]
            print("Shop[0]['action_id'] ", action_id)
            action_title = self.list_box.item(selected_action)['values'][1]
            print("Shop[1]['action_title'] ", action_title)
            action_created_date = self.list_box.item(selected_action)['values'][2]
            print("Shop[2]['action_created_date'] ", action_created_date)
            answer = tk.messagebox.askquestion("Question", "Do you what to delete "+str(action_title)+" ?")
            if answer == 'yes':
                for s, shop in enumerate(self.Shops):
                    Shop_Actions = []
                    if self.Selected_Shop != "" and shop['Shop_name'] != self.Selected_Shop:
                        continue
                    print("shop['Shop_name'] ", shop['Shop_name'])
                    if shop:
                        print("shop['Shop_Actions'] ", shop['Shop_Actions'])
                        if shop['Shop_Actions'] and shop['Shop_Actions'] != "":
                            Shop_Actions = json.loads(shop['Shop_Actions'])  
                            shop_actionscopy = []
                            for sa, Shop_Action in enumerate(Shop_Actions):
                                print("Shop_Action ", str(Shop_Action))
                                if Shop_Action[0] == action_id and Shop_Action[1] == action_title and Shop_Action[2] == action_created_date:
                                    continue
                                else:
                                    shop_actionscopy.append(Shop_Action)
                            Shop_Actions = shop_actionscopy
                            cur.execute("UPDATE Shops SET Shop_Actions=? WHERE Shop_id=? AND Shop_name=? AND Shop_brand_name=?", 
                                            (str(Shop_Actions), str(shop['Shop_id']), str(shop['Shop_name']), str(shop['Shop_brand_name'])))
                            # Commit the changes to the database
                            conn.commit()
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
        print("item_list['item_list'] ", item_list)
        if item_list['item_list']:
            print(str(item_list['item_list']))
            info_list = item_list['item_list']
            
            sv = [s[0] for s in info_list]
            inputs[0].config(values=sv)
                
            if shop == "":
                if self.Selected_Shop != "" and self.Selected_Shop in sv:
                   inputs[0].set(self.Selected_Shop)
                elif self.Shops_Names[0] in sv:
                    inputs[0].set(self.Shops_Names[0])
            else:
                for s in info_list:
                    print("code s")
                    print(str(s))
                    if s[0] in shop:
                        print("code s0")
                        print(str(s[0]))
                        v = [c[0] for c in s[1]]
                        inputs[1].config(values=v)
                        if len(v) == 1:
                            inputs[1].set(v[0])
                        break
            
            if code == "":
                for s in info_list:
                    print("code s")
                    print(str(s))
                    if s[0] in shop:
                        print("code s0")
                        print(str(s[0]))
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
            self.Selected_items = 0
            
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
        self.Selected_items = 0
        if str(self.notebook_frame.tab(self.notebook_frame.index("current"), "text")) == "If :":
            self.Selected_items = self.ifSelected_items
        elif str(self.notebook_frame.tab(self.notebook_frame.index("current"), "text")) == "Do :":
            self.Selected_items = self.doSelected_items
            
        if self.Selected_items == 0:
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
            print("selected item "+str(y) + " : "+str(Selected_item))
            for items in Selected_item_Display_frame.winfo_children():
                items.destroy()
                
            #self.midel_frame
            for i, selected_item in enumerate(Selected_item):
                
                print("selected_item ", selected_item)
                selected_item_info = selected_item[0]
                print("selected_item_info |", selected_item_info)
                print("selected_item ", selected_item)
                
                #if isinstance(selected_item_info, str):
                #    selected_item_info = ast.literal_eval(selected_item_info)
                item = [""]
                
                new_item_fram = tk.Frame(Selected_item_Display_frame, highlightthickness=2, highlightbackground="black")
                new_item_fram.grid(row=len(Selected_item_Display_frame.winfo_children()), column=0, pady=1, sticky=tk.EW)

                # TODO ADD IMAGE 

                new_item_name = tk.Label(new_item_fram, text=str(selected_item[4]), font=("Arial", 11))
                new_item_name.grid(row=0, column=1, columnspan=6, sticky="nsew")

                new_barcode_Label = tk.Label(new_item_fram, text=str("barcode"), font=("Arial", 7))
                new_barcode_Label.grid(row=1, column=1, columnspan=3, sticky="nsew")
                
                new_type_Label = tk.Label(new_item_fram, text=str(selected_item[15]), font=("Arial", 7))
                new_type_Label.grid(row=1, column=3, columnspan=3, sticky="nsew")
                
                new_item_QTY_fram = tk.Frame(new_item_fram)
                new_item_QTY_fram.grid(row=2, column=1, rowspan=2, sticky="nsew")
                
                new_item_QTY_Label = tk.Label(new_item_QTY_fram, text="QTY Max is " + str(selected_item[8]), font=("Arial", 8))
                new_item_QTY_Label.grid(row=1, column=1, sticky="nsew")
                new_item_QTY_Spinbox = ttk.Spinbox(new_item_QTY_fram, from_=0, to=100, width=10)
                new_item_QTY_Spinbox.grid(row=2, column=1, sticky="nsew")
                new_item_QTY_Spinbox.set(str(selected_item[7]))
                price_ = ""
                price_ = str(selected_item_info['values']['price'])
                disc = ""
                if float(selected_item_info['values']['price'])-float(selected_item[10]) > 0:
                    disc = " DISCOUNT " + str(float(selected_item_info['values']['price'])-float(selected_item[10]))
                new_item_Price_Label = tk.Label(new_item_fram, text="Price " + price_ + disc, font=("Arial", 7))
                new_item_Price_Label.grid(row=2, column=2, sticky="nsew")
                new_item_Price_Spinbox = ttk.Spinbox(new_item_fram, from_=0, to=100, width=10)
                new_item_Price_Spinbox.grid(row=3, column=2, sticky="nsew")
                new_item_Price_Spinbox.set(str(selected_item[10]))

                new_item_Shop_Label = tk.Label(new_item_fram, text="Shop :" , font=("Arial", 7))
                new_item_Shop_Label.grid(row=2, column=3, sticky="nsew")
                new_item_Shop_Combobox = ttk.Combobox(new_item_fram, values=[], width=10)
                new_item_Shop_Combobox.grid(row=3, column=3, padx=5, pady=5, sticky=tk.W)
                new_item_Shop_Combobox.set(str(selected_item[13]))
                new_item_Code_Label = tk.Label(new_item_fram, text="Code :" , font=("Arial", 7))
                new_item_Code_Label.grid(row=2, column=4, sticky="nsew")
                new_item_Code_Combobox = ttk.Combobox(new_item_fram, values=[], width=10)
                new_item_Code_Combobox.grid(row=3, column=4, padx=5, pady=5, sticky=tk.W)
                new_item_Code_Combobox.set(str(selected_item[2]))
                new_item_Color_Label = tk.Label(new_item_fram, text="Color " , font=("Arial", 7))
                new_item_Color_Label.grid(row=2, column=5, sticky="nsew")
                new_item_Color_Combobox = ttk.Combobox(new_item_fram, values=[], width=10)
                new_item_Color_Combobox.grid(row=3, column=5, padx=5, pady=5, sticky=tk.W)
                new_item_Color_Combobox.set(str(selected_item[5]))
                new_item_Size_Label = tk.Label(new_item_fram, text="Size " , font=("Arial", 7))
                new_item_Size_Label.grid(row=2, column=6, sticky="nsew")
                new_item_Size_Combobox = ttk.Combobox(new_item_fram, values=[], width=10)
                new_item_Size_Combobox.grid(row=3, column=6, padx=5, pady=5, sticky=tk.W)
                new_item_Size_Combobox.set(str(selected_item[6]))
                
                new_exbarcode_Label = tk.Label(new_item_fram, text=str(selected_item[14]), font=("Arial", 7))
                new_exbarcode_Label.grid(row=1, column=7, sticky="nsew")
                
                del_button = tk.Button(new_item_fram, text="x", font=("Arial", 12), command= lambda index=i, frame=new_item_fram: self.remove_item(index, frame))
                del_button.grid(row=0, column=7, sticky="nsew")
                # self.master.bind("<Delete>", lambda _: self.remove_item())
                
                new_item_TPrice_Label = tk.Label(new_item_fram, text="Total Price is " , font=("Arial", 13))
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
        
        
    def void_(self):
        a = Chacke_Security(self, self.user, self.Shops[self.on_Shop], 2)
        if a:
            answer = tk.messagebox.askquestion("Question", "Do you whant to void order?")
            if answer == 'yes':
                 # call void         
                self.void_items()
            
    def void_items(self):
        self.clear_items()
        # delete this list on db
        cursor.execute("DELETE FROM pre_doc_table WHERE id=?", (self.chart_index,))
        # Commit the changes to the database
        conn.commit()
        # self.update_info() will be called in next_prev_chart 
        self.next_prev_chart("prev")
        
  # this will
    def chack_list(self):
        total_discount = 0
        total_tax = 0
        total_qty = 0
        all_total_price = 0
        self.Selected_items = 0
        
        
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
                print("in update item: " + str(selected_item[0]))
                print("in update item: " + str(selected_item[0]))
                print("in update item: " + str(selected_item[6]))
                print("in update item: " + str(selected_item[8]))

                qty = float(selected_item[7])
                price = float(selected_item[10])
                discount = float(selected_item[0]['values']['price']) - float(selected_item[10])
                tax = float(selected_item[10])
                total_price = float(selected_item[11])
                
                # Calculate the expected total price based on quantity, price, discount, and tax
                expected_total_price = qty * (price)  # - tax
                
                # Update the total price in the item if it doesn't match the expected value
                if total_price != expected_total_price:
                    self.Selected_items[a][11] = expected_total_price
                
                # Update the price variable
                total_qty += qty
                total_discount += discount
                total_tax += tax
                all_total_price += expected_total_price
            
        return total_qty, total_discount, total_tax, all_total_price
        
    def add_item(self, item_info):
        print("item_info = " + str(item_info))
        if (item_info['type'] == "ITEM"):
            for data in item_info['extra_data']:
                shop = self.homemaster.Shops_Names
                if self.Selected_Shop != "":
                    shop = [self.Selected_Shop]
                items, doc, selected_type, barcode, shop_name, code, color, size, qty = \
                     item_info['values'], None, item_info['type'], data[6], data[0], data[1], data[2], data[3], data[4]
                if data[7] != []:
                    for t, typ in enumerate(data[7]):                            
                        QTY = int(typ[1])
                        PRICE = int(typ[2])
                        items = chacke_action([str(items['id']), code, barcode, items['name'], color, size, float(QTY), PRICE, self.homemaster.disc, items['include_tax'], float(QTY)*float(PRICE), shop_name, ""])
                        if items:
                            for value in items:
                                if str(self.notebook_frame.tab(self.notebook_frame.index("current"), "text")) == "If :":
                                    self.ifSelected_items.append([item_info, str(value[0]), value[1], value[2], value[3], value[4], value[5], value[6], value[7], data[5], PRICE, value[9], value[10], value[11], value[12], typ[0]])
                                    self.doSelected_items.append([item_info, str(value[0]), value[1], value[2], value[3], value[4], value[5], value[6], value[7], data[5], PRICE, value[9], value[10], value[11], value[12], typ[0]])
                                elif str(self.notebook_frame.tab(self.notebook_frame.index("current"), "text")) == "Do :":
                                    self.doSelected_items.append([item_info, str(value[0]), value[1], value[2], value[3], value[4], value[5], value[6], value[7], data[5], PRICE, value[9], value[10], value[11], value[12], typ[0]])
                                
                else:
                    items = chacke_action([str(items['id']), code, barcode, items['name'], color, size, float(qty), items['price'], self.homemaster.disc, items['include_tax'], float(qty)*float(items['price']), shop_name, ''])
                    if items:
                        for value in items:
                            if str(self.notebook_frame.tab(self.notebook_frame.index("current"), "text")) == "If :":
                                self.ifSelected_items.append([item_info, str(value[0]), value[1], value[2], value[3], value[4], value[5], value[6], value[7], data[5], item_info['values']['price'], value[9], value[10], value[11], value[12], ""])
                                self.doSelected_items.append([item_info, str(value[0]), value[1], value[2], value[3], value[4], value[5], value[6], value[7], data[5], item_info['values']['price'], value[9], value[10], value[11], value[12], ""])
                            elif str(self.notebook_frame.tab(self.notebook_frame.index("current"), "text")) == "Do :":
                                self.doSelected_items.append([item_info, str(value[0]), value[1], value[2], value[3], value[4], value[5], value[6], value[7], data[5], item_info['values']['price'], value[9], value[10], value[11], value[12], ""])
                

        if (item_info['type'] == "DOCUMENT"):
            items = json.loads(item_info['values']['item'])
            for item in items:
                it = fetch_as_dict_list(cursor, "SELECT * FROM product WHERE id=?", 
                                (item[0],))[0]
                if it:
                    doc_item_info = {'values': it, 'type': 'DOCUMENT', 'item_list':[]}
                    #print("items===========%%%%%%% = " + str(it))
                    print("items===========%%%%%%% = " + str(item))
                    print("doc_item_info ===========%%%%%%% = " + str(doc_item_info))
                    # TODO: last empty one is type find it
                    typ = ""
                    if len(item) > 11:
                        typ = item[11]
                    qtyleft = "??"
                    self.Selected_items.append([doc_item_info, str(item[0]), item[1], item[2], item[3], item[5], item[6], item[7], item[8], qtyleft, item[8], item[10], 0, item[4], item_info['values']['doc_barcode'], typ]) 
                else:
                    pass
                
        self.Update_Selected_item()
        
    def Save_Shop_Actions(self):
        Action_titel = self.Action_label_entry.get()
        created_date = self.add_button.cget("text")
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
                    Shop_Actions = json.loads(shop['Shop_Actions']) 
                
                if self.add_button.cget("text") == "New":
                    Shop_Actions.append([len(Shop_Actions), Action_titel, created_date, from_date, to_date, if_conditions, Do_makes])
                    cur.execute("UPDATE Shops SET Shop_Actions=? WHERE Shop_id=? AND Shop_name=? AND Shop_brand_name=?", 
                                    (json.dumps(Shop_Actions), str(shop['Shop_id']), str(shop['Shop_name']), str(shop['Shop_brand_name'])))
                    # Commit the changes to the database
                    conn.commit()
                else:
                    Shop0 = fetch_as_dict_list(cur, "SELECT * FROM Shops WHERE Shop_id=? AND Shop_name=?", 
                                        (str(self.selected_shop_id), str(self.selected_shop_name)))
                    if Shop0 and Shop0[0] and Shop0[0]['Shop_Actions'] and Shop0[0]['Shop_Actions'] != "":
                        
                        Shop_Actions = json.loads(Shop0[0]['Shop_Actions'])

                        if int(self.selected_id) <= len(Shop_Actions):
                            Shop_Actions[int(self.selected_id)] = [product_id, name, code, shop, color, size, qty, price, total_price, add_new,
                                          make_price, make_total_price, make_discount, make_total_disc, enable, remove_when_expires, from_date, to_date]

                        print("Shop_Actions ", Shop_Actions)
                        cur.execute("UPDATE Shops SET Shop_Actions=? WHERE Shop_id=? AND Shop_name=? AND Shop_brand_name=?", 
                                    (str(json.dumps(Shop_Actions)), str(shop['Shop_id']), str(shop['Shop_name']), str(shop['Shop_brand_name'])))
                        # Commit the changes to the database
                        conn.commit()
                                
        # Update the product listbox
        self.update_Shop_Actions_listbox()
        # Clear the product details widgets
        self.clear_Shop_Actions_widget()
        self.hide_add_forme()
        # Update the product listbox if needed
        self.update_search_results([None, None])








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
            self.Action_label_entry.insert(0, self.list_box.item(selected_item, "values")[0])
            
            self.From_Date_entry.insert(0, self.list_box.item(selected_item, "values")[2])
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
            self.notebook_frame.pack(side=tk.RIGHT, fill=tk.Y, expand=False)
            
            self.Update_Selected_item()