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

from D.Security import Chacke_Security

current_dir = os.path.abspath(os.path.dirname(__file__))
MAIN_dir = os.path.join(current_dir, '..')
sys.path.append(MAIN_dir)
from D.Getdefsize import ButtonEntryApp
from C.List import *
from C.Sql3 import *

# Connect to the database or create it if it does not exist

data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data'))
db_path = os.path.join(data_dir, 'my_database.db')
conn = sqlite3.connect(db_path)
cur = conn.cursor()

conn.commit()

from D.Getdate import GetDateForm
from D.Chart.Chart import *
#from D.Product.PrintPriceTag import PrintPriceTagFrame

from C.Product.selecttype import *
from C.Product.ProductEdtion import ProductFullEditionForm
from C.Product.ProductEdtion import ProductQueckEditionForm
from C.Product.DisplayProductInfo import ProductFullInfoForm

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
    
    # print(query+"\n")
    # Execute the SQL query and return the results as a list of tuples
    cur.execute(query, (*given,))
    results = cur.fetchall()
    return results
# Example node hierarchy




class ProductForm(ttk.Frame):
    def __init__(self, master, user, Shops, on_Shop):
        ttk.Frame.__init__(self, master)
        self.master = master
        self.user = self.user_info = user
        self.Shops = Shops
        self.on_Shop = on_Shop
        self.Product_info_frame = None
        self.vv = []
        
        # Android-style dark blue color scheme
        self.bg_dark = "#0d47a1"      # Deep blue
        self.bg_light = "#1565c0"     # Darker blue
        self.accent_blue = "#1976d2"  # Medium blue
        self.text_light = "#ffffff"   # White text
        self.bg_darker = "#0a3d91"    # Even darker blue
        # Create the search bar
        # Create the frame for the search bar and buttons
        self.search_frame = ttk.Frame(self)
        self.search_frame.pack(side=tk.TOP, padx=5, pady=5)
        
        self.shop_name_label = tk.Label(self.search_frame, text='At Shop :')
        self.shop_name_label.pack(side=tk.LEFT, padx=5, pady=5)

        self.Shops_Names = [shop['Shop_name'] for shop in self.Shops]      
        self.shop_name_Combobox = ttk.Combobox(self.search_frame, values=self.Shops_Names)
        self.shop_name_Combobox.pack(side=tk.LEFT, padx=5, pady=5)
        self.shop_name_Combobox.current(0)
        self.shop_name_Combobox.bind('<KeyRelease>', self.update_search_results)
        
        self.chackname = Chacke_Security(self, self.user, self.Shops[self.on_Shop], 34, f'User Has No Permission To Access Change PRODUCT Name OR LOGIN AS ADMIN')
        self.chackprice = Chacke_Security(self, self.user, self.Shops[self.on_Shop], 35, f'User Has No Permission To Access Change PRODUCT Price OR LOGIN AS ADMIN')
        
        # create a StringVar to represent the search box
        self.search_var = tk.StringVar()
        self.search_entry = tk.Entry(self.search_frame, textvariable=self.search_var)
        if Chacke_Security(self, self.user, self.Shops[self.on_Shop], 9, f'User Has No Permission To Access SEARCH PRODUCT OR LOGIN AS ADMIN'):                        
            self.search_entry.bind('<KeyRelease>', self.update_search_results)
            # bind the update_search_results function to the search box
            self.search_var.trace("w", self.update_search_results)
        self.search_entry.pack(side=tk.LEFT, padx=5, pady=5, expand=True)

        
        self.add_new_button = tk.Button(self.search_frame, text='Add New product', command=self.Full_Edition_form)
        self.add_newmultyproduct_button = tk.Button(self.search_frame, text='Maulty Add Products', command=self.Queck_Edition_form)
        
        self.add_new_button.pack(side=tk.LEFT, padx=5, pady=5)
        self.add_newmultyproduct_button.pack(side=tk.LEFT, padx=5, pady=5)
        
        if not Chacke_Security(self, self.user, self.Shops[self.on_Shop], 33, f'User Has No Permission To Access Add PRODUCT OR LOGIN AS ADMIN'):                        
            self.add_new_button.config(state=tk.DISABLED)
            self.add_newmultyproduct_button.config(state=tk.DISABLED)

        self.delete_button = ttk.Button(self.search_frame, text='Delete', command=self.delete_product)
        self.delete_button.pack(side=tk.LEFT, padx=5, pady=5)
        self.refresh_button = ttk.Button(self.search_frame, text='Refresh', command=self.Load_Shop_items)
        self.refresh_button.pack(side=tk.LEFT, padx=5, pady=5)
        self.show_info_button = ttk.Button(self.search_frame, text='Show Information', command=self.Show_product_Info)
        self.show_info_button.pack(side=tk.LEFT, padx=5, pady=5)
        self.price_tag_button = ttk.Button(self.search_frame, text='Price Tag', command= lambda :PrintPriceTagFrame(self))
        self.price_tag_button.pack(side=tk.LEFT, padx=5, pady=5)
        
        
        # Create the list box
        self.treeFrame_contaner_frame = ttk.Frame(self)
        self.treeFrame_contaner_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=False)
        
        self.treeList_Frame_contaner_frame = ttk.Frame(self.treeFrame_contaner_frame)
        self.treeList_Frame_contaner_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.treeList_Frame = ttk.Frame(self.treeList_Frame_contaner_frame)
        self.treeList_Frame.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        
        self.treeitem_List_canvas = tk.Canvas(self.treeList_Frame, bg=self.bg_dark, highlightthickness=0)
        self.treeitem_List_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        
        self.treeitem_List_yscrollbar = ttk.Scrollbar(self.treeList_Frame, orient='vertical', command=self.treeitem_List_canvas.yview)
        self.treeitem_List_yscrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.treeitem_List_xscrollbar = ttk.Scrollbar(self.treeList_Frame_contaner_frame, orient='horizontal', command=self.treeitem_List_canvas.xview)
        self.treeitem_List_xscrollbar.pack(side=tk.TOP, fill=tk.X)
        
        self.treeitem_List_canvas.configure(xscrollcommand=self.treeitem_List_xscrollbar.set, yscrollcommand=self.treeitem_List_yscrollbar.set)
        #self.New_item_contener_canvas.bind('<Configure>', lambda e: self.New_item_contener_canvas.configure(scrollregion=self.New_item_contener_canvas.bbox("all")))

        self.tree = ttk.Treeview(self.treeitem_List_canvas, columns=
                                 ("Shop Name"))
        self.treeitem_List_canvas.create_window((0, 0), window=self.tree, anchor=tk.NW)
        self.tree.bind('<Configure>', lambda e: self.treeitem_List_canvas.configure(scrollregion=self.treeitem_List_canvas.bbox("all")))

        
        
        self.tree.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.tree.heading("#0", text="Value", anchor=tk.W)
        self.tree.column("#0")
        '''
        self.tree.heading("#1", text="Code", anchor=tk.W)
        self.tree.column("#1", stretch=tk.NO, minwidth=25, width=125)
        self.tree.heading("#2", text="Color", anchor=tk.W)
        self.tree.column("#2", stretch=tk.NO, minwidth=25, width=125)
        self.tree.heading("#3", text="Size", anchor=tk.W)
        self.tree.column("#3", stretch=tk.NO, minwidth=25, width=125)
        self.tree.heading("#4", text="Barcode", anchor=tk.W)
        self.tree.column("#4", stretch=tk.NO, minwidth=25, width=125)
        self.tree.heading("#5", text="Qtyfirst", anchor=tk.W)
        self.tree.column("#5", stretch=tk.NO, minwidth=25, width=125)
        self.tree.heading("#6", text="Qty", anchor=tk.W)
        self.tree.column("#6", stretch=tk.NO, minwidth=25, width=125)
        self.tree.heading("#7", text="cdate", anchor=tk.W)
        self.tree.column("#7", stretch=tk.NO, minwidth=25, width=125)
        self.tree.heading("#8", text="update", anchor=tk.W)
        self.tree.column("#8", stretch=tk.NO, minwidth=25, width=125)'''

        self.tree.bind('<<TreeviewSelect>>', self.update_selected_type)
        
        
        # Create the frame for the product details
        self.Frame_contaner_frame = ttk.Frame(self)
        self.Frame_contaner_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        self.List_Frame_contaner_frame = ttk.Frame(self.Frame_contaner_frame)
        self.List_Frame_contaner_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.List_Frame = ttk.Frame(self.List_Frame_contaner_frame)
        self.List_Frame.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        
        self.item_List_canvas = tk.Canvas(self.List_Frame, bg=self.bg_dark, highlightthickness=0)
        self.item_List_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        
        self.item_List_yscrollbar = ttk.Scrollbar(self.List_Frame, orient='vertical', command=self.item_List_canvas.yview)
        self.item_List_yscrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.item_List_xscrollbar= ttk.Scrollbar(self.List_Frame_contaner_frame, orient='horizontal', command=self.item_List_canvas.xview)
        self.item_List_xscrollbar.pack(side=tk.TOP, fill=tk.X)
        
        self.item_List_canvas.configure(xscrollcommand=self.item_List_xscrollbar.set, yscrollcommand=self.item_List_yscrollbar.set)
        #self.New_item_contener_canvas.bind('<Configure>', lambda e: self.New_item_contener_canvas.configure(scrollregion=self.New_item_contener_canvas.bbox("all")))

        self.item_List_frame = ttk.Frame(self.item_List_canvas)
        self.item_List_canvas.create_window((0, 0), window=self.item_List_frame, anchor=tk.NW)
        self.item_List_frame.bind('<Configure>', lambda e: self.item_List_canvas.configure(scrollregion=self.item_List_canvas.bbox("all")))


        self.itemtypes = []
        self.selectedtype= []
        self.Load_Shop_items()

        
    #
    #
    #
    # List Prucducts
    #
    #
    #
    def update_selected_type(self, event):
        selected = self.tree.focus()
        if selected:
            self.selectedtype = []
            def collect_paths(item):
                path = []
                while item:
                    if self.tree.item(item, 'text') == "ALL PRODUCTS":
                        break
                    path.append(self.tree.item(item, 'text'))
                    item = self.tree.parent(item)
                path.reverse()
                self.selectedtype.append(path)
            collect_paths(selected)
        self.Update_shop_item_list("")
        
        
    def Load_Shop_items(self):
        self.master.master.master.master.Shops_info['Shop_items'] = []
        for s, shop in enumerate(self.Shops):
            #print("Loop Shop ", shop['Shop_name'])
            #print("Selected Shop ", self.shop_name_Combobox.get())
            #print("Shop items = ", shop['Shop_items'])
            if shop['Shop_items'] and (shop['Shop_name'] == "" or s == self.shop_name_Combobox.current()):
                found_shop_items = json.loads(shop['Shop_items'])
                #print("Shop items --> ", found_shop_items)
                if found_shop_items:
                    for item in found_shop_items:
                        value = fetch_as_dict_list(cur, 'SELECT * FROM product WHERE id=?', (str(item[0]),))
                        if value and not len(value) == 0:
                            self.master.master.master.master.Shops_info['Shop_items'].append([value[0], [], "", "", "", "", "", "", "", "", "", "", ""])
        
        for i, item in enumerate(self.master.master.master.master.Shops_info['Shop_items']):
            product = selected_item = item[0]
            self.master.master.master.master.Shops_info['Shop_items'][i][1] = json.loads(product['more_info'])
            itemstypes = []
            def sub_list(ls, itemtypes):
                if(isinstance(ls, list)):
                    for l in ls:
                        if len(l) > 4 and l[4] != ""and l[4] != " ":
                            if l[1] != '' or l[1] != "":
                                try:
                                    #print("add ing = ", l[1])
                                    itemtypes.append(json.loads(l[1]))
                                except:
                                    print("error while loading item type = ", l[1])
                        elif len(l) == 2:
                            #print("going deep = ", l[1])
                            sub_list(l[1], itemtypes)
            #print("sanding typrs = ", self.master.master.master.master.Shops_info['Shop_items'][i][1])
            sub_list(self.master.master.master.master.Shops_info['Shop_items'][i][1], self.itemtypes)
        self.update_typetree(self.itemtypes)
        self.Update_shop_item_list("")
        
    def update_typetree(self, itemtypes):
        self.tree.delete(*self.tree.get_children())
        parents = {}
        All_Products = self.tree.insert("", "end", text="ALL PRODUCTS")
        def add_items(parent_id, items):
            newpid = None
            if not len(items) >= 1:
                return
            else:
                # print("items ", list(items))    
                # check if parent alredy exist
                existing_items = self.tree.get_children(parent_id)
                # print("existing_items ", list(existing_items))
                if existing_items:
                    existing_item_texts = []
                    for iid in existing_items:
                        existing_item_texts.append(self.tree.item(iid)['text'])
                    
                    # print("existing_item_texts ", existing_item_texts)
                    if items[0] in existing_item_texts:
                        # print("existing_item_texts.index[items[0] ", existing_item_texts.index(items[0]))
                        newpid = list(existing_items)[existing_item_texts.index(items[0])]
                        #newpid = self.tree.insert(parent_id, "end", text=items[0])
                    else:
                        newpid = self.tree.insert(parent_id, "end", text=items[0])
                else:
                    newpid = self.tree.insert(parent_id, "end", text=items[0])
                add_items(newpid, items[1:])
            
        
        for sublist in itemtypes:
            add_items(All_Products, sublist)


    def update_info(self):
        pass
        '''
self.tree.delete(*self.tree.get_children())
        parents = {}
        All_Products = self.tree.insert("", "end", text="ALL PRODUCTS")
        def add_items(parent_id, items):
            if len(items) == 1:
                self.tree.insert(parent_id, "end", text=items[0])
            else:
                for i, item in enumerate(items):
                    if i == 0:
                        # check if parent alredy exist
                        existing_items = self.tree.get_children(parent_id)
                        existing_item_texts = []
                        for iid in existing_items:
                            existing_item_texts.append(self.tree.item(iid)['text'])
                            
                        if item in existing_item_texts:
                            parent_id = existing_items[existing_item_texts.index(item)]
                        else:
                            parent_id = self.tree.insert(parent_id, "end", text=item)
                    else:
                        add_items(parent_id, items[i:])
        for sublist in itemtypes:
            add_items(All_Products, sublist)

total_qty, total_discount, total_tax, all_total_price = self.chack_list()
        self.total = (all_total_price - self.tax) - self.disc
        self.total_items_label.config(text="Total Items : " + str(total_qty))
        self.total_tax_label.config(text="Total Tax : " + str(self.tax))
        self.total_discount_label.config(text="Item Discount : " + str(total_discount))
        self.total_tdiscount_label.config(text="Total Discount : " + str(self.disc))
        self.total_price_label.config(text="Price Befor : " + str(all_total_price))
        self.total_label.config(text="Price After: " + str((all_total_price - self.tax) - self.disc))
        self.update_chart()
        '''
    def get_total_qty(self, inputs, item_list):
         if item_list:
            #print(str(item_list['item_list']))
            info_list = item_list
            total = 0
            for i0, s in enumerate(info_list):
                for i1, codes in enumerate(s[1]):
                    for i2, c in enumerate(codes[1]):
                        for i3, s in enumerate(c[1]):
                            if s[1][0][4] and s[1][0][4] != "":
                                total += float(s[1][0][4])
                                inputs[6].config(text="QTY Max is "+str(total))
            if not total == 0:
                inputs[6].config(text="QTY Max is "+str(total))
                
    def Get_next_seletion(self, do_what, inputs, item_list):
        shop = inputs[0].get()
        code = inputs[1].get()
        color = inputs[2].get()
        size = inputs[3].get()
        qty = inputs[4].get()
        barcode = inputs[5].cget('text')
        #print("item_list['item_list'] ", item_list)
        if item_list:
            #print(str(item_list['item_list']))
            info_list = item_list
            
            sv = [s[0] for s in info_list]
            inputs[0].config(values=sv)
                
            if shop == "":
                if self.shop_name_Combobox.current() != "" and self.shop_name_Combobox.current() in sv:
                   inputs[0].set(self.shop_name_Combobox.current())
                elif self.Shops_Names[0] in sv:
                    inputs[0].set(self.Shops_Names[0])
            total = 0
            for i0, sh in enumerate(info_list):
                if sh[0] == shop or i0 == 0:
                    for i1, codes in enumerate(sh[1]):
                        if codes[0] == code or i1 == 0:
                            cov = [cc[0] for cc in sh[1]]
                            inputs[1].config(values=cov)
                            if len(cov) == 1 or codes[0] == code:
                                inputs[1].set(codes[0])
                            for i2, c in enumerate(codes[1]):
                                if c[0] == color or i2 == 0:
                                    cv = [colorc[0] for colorc in codes[1]]
                                    inputs[2].config(values=cv)
                                    if len(cv) == 1 or c[0] == color:
                                        inputs[2].set(c[0])
                                    for i3, s in enumerate(c[1]):
                                        if s[0] == size or i3 == 0:
                                            siv = [si[0] for si in c[1]]
                                            inputs[3].config(values=siv)
                                            if len(siv) == 1 or s[0] == size:
                                                inputs[3].set(siv[0])
                                            if do_what == "Save" and sh[0] == shop and codes[0] == code and c[0] == color and s[0] == size:
                                                info_list[i0][1][i1][1][i2][1][i3][1][0][4] = inputs[4].get()
                                                self.get_total_qty(inputs, info_list)
                                                return info_list
                                            elif not do_what == "Save":
                                                if s[1][0][4] and s[1][0][4] != "":
                                                    inputs[4].set(float(s[1][0][4]))
                                                inputs[5].config(text=s[1][0][0])
                                                if sh[0] == shop and codes[0] == code and c[0] == color and s[0] == size:
                                                    #slef.get_total_qty(inputs, info_list)
                                                    return info_list
        return item_list
                                            
    def Update_selected_item_info(self, data, selected_item_info, new_item_Price_Spinbox, new_item_TPrice_Spinbox, index):
        self.Get_next_seletion("", data, selected_item_info)
        # QTY
        self.master.master.master.master.Shops_info['Shop_items'][index][7] = data[4].get()
        # price
        self.master.master.master.master.Shops_info['Shop_items'][index][8] = new_item_Price_Spinbox.get()
        # shop
        self.master.master.master.master.Shops_info['Shop_items'][index][12] = data[0].get()
        #code
        self.master.master.master.master.Shops_info['Shop_items'][index][2] = data[1].get()
        # color
        self.master.master.master.master.Shops_info['Shop_items'][index][5] = data[2].get()
        # size
        self.master.master.master.master.Shops_info['Shop_items'][index][6] = data[3].get()
        self.update_info()
        
    
    def SAVE_CHANGE(self, index, data, selected_item_info):
        #print("going to make change to = ", self.master.master.master.master.Shops_info['Shop_items'][index])
        newinfo_list = self.Get_next_seletion("Save", data, selected_item_info)
        if newinfo_list and not newinfo_list == 0:            
            cur.execute('UPDATE product SET name=?, price=?, more_info=? WHERE id=?', (data[9].get(), data[7].get(), json.dumps(newinfo_list), self.master.master.master.master.Shops_info['Shop_items'][index][0]['id']))
            data[8].config(text="Price "+data[7].get())
            it2 = fetch_as_dict_list(cur, 'SELECT * FROM product WHERE id=?', (str(self.master.master.master.master.Shops_info['Shop_items'][index][0]['id']),))
            if it2 and not len(it2) == 0:
                self.master.master.master.master.Shops_info['Shop_items'][index][0] = it2[0]
                self.master.master.master.master.Shops_info['Shop_items'][index][1] = newinfo_list
                #print("changed to = ", self.master.master.master.master.Shops_info['Shop_items'][index])

            
            # Commit the changes to the database
            conn.commit()
    
    def searchbytype(self):
        pass
    
    def Update_shop_item_list(self, search_str):
        oldloaded = len(self.item_List_frame.winfo_children())
        for items in self.item_List_frame.winfo_children():
            items.destroy()
        #self.midel_frame
        items = 0
        TQTY = 0
        Tprice = 0
        Tcost = 0
        vv = []
        self.vv = []
        counted = 0
        chackname = self.chackname 
        chackprice = self.chackprice
        itemstypes = []
        
        for i, item in enumerate(self.master.master.master.master.Shops_info['Shop_items']):
            product = selected_item = item[0]
            if not search_str == "" and not (search_str.lower() in (selected_item['name']).lower()):
                continue
            
            chacksize = 0
            cost = float(product['cost'])
            price = float(product['price'])
            #print("selected_item ", selected_item)
            qty_info_list = selected_item_info = self.master.master.master.master.Shops_info['Shop_items'][i][1]
            items += 1
            qty = 0
            def sub_list(ls, qty):
                comen_qty = 0
                itemtypes = []
                if(isinstance(ls, list)):
                    for l in ls:
                        if len(l) > 4 and l[4] != ""and l[4] != " ":
                            try:
                                ischar = any(char.isalpha() for char in l[4])
                                if not ischar and (isinstance(float(l[4]), float) or isinstance(int(l[4]), int)):
                                    if comen_qty == 0:
                                        comen_qty = float(l[4])
                                    # TODO: FOR 2ps and more than one ps what to do
                                    qty += float(l[4])

                                # this will collect types
                                if l[1] != '' or l[1] != "":
                                    try:
                                        itemtypes.append(json.loads(l[1]))
                                    except:
                                        print("error while loading item type = ", l[1])
                            except:
                                pass
                        elif len(l) == 2:
                            #main_name.append(l[0])
                            qty, itemtypes = sub_list(l[1], qty)
                return qty, itemtypes
            qty, itemtypes = sub_list(qty_info_list, qty)
            issametype = 0
            # print("self.selectedtype ", self.selectedtype)
            # print("types = ", itemtypes)
            for types in self.selectedtype:
                if types == []:
                    issametype = 1
                else:
                    for t, typ in enumerate(types):
                        for itemtype in itemtypes:
                            if len(itemtype) >= len(types):
                                if itemtype[t] == typ:
                                    issametype = 1
                                else:
                                    issametype = 0
                                    break
            if not issametype and len(self.selectedtype) :
                continue
             
            vv.append([str(product['id']), float(price), str(product['name'])])
            # TODO make user choosh in which name, code, id
            if qty > 0:
                Tprice += qty*price
                Tcost += qty*cost
                TQTY += qty
            
            if counted >= 10:
                continue
            counted += 1
            #print("selected_item_info |", selected_item_info)
            #print("selected_item ", selected_item)
            
            #if isinstance(selected_item_info, str):
            #    selected_item_info = ast.literal_eval(selected_item_info)
            item = [""]
            
            new_item_fram = ttk.Frame(self.item_List_frame) #,  highlightthickness=2, highlightbackground="black")
            new_item_fram.pack(fill=tk.X, padx=10, pady=10)

            # TODO ADD IMAGE 
            
            #if not Chacke_Security(self, self.user, self.Shops[self.on_Shop], 31, f'User Has No Permission To Access Change PRODUCT Image OR LOGIN AS ADMIN'):                        
            #     new_item_Img.config(state=tk.DISABLED)
        

            new_item_name_input = ttk.Entry(new_item_fram) #, font=("Arial", 11))
            new_item_name_input.grid(row=0, column=1, columnspan=6, sticky="nsew")
            new_item_name_input.insert(0, str(selected_item['name']))
            if not chackname:                        
                new_item_name_input.config(state=tk.DISABLED)
        
            new_item_QTY_fram = ttk.Frame(new_item_fram)
            new_item_QTY_fram.grid(row=1, column=1, rowspan=2, sticky="nsew")
            
            new_item_Price_Label = ttk.Label(new_item_fram, text="Price " + str(selected_item['price']))
            new_item_Price_Label.grid(row=1, column=2, sticky="nsew")
            new_item_Price_Spinbox = ttk.Spinbox(new_item_fram, from_=0, to=100, width=10)
            new_item_Price_Spinbox.grid(row=2, column=2, sticky="nsew")
            new_item_Price_Spinbox.set(str(selected_item['price']))

            if not chackprice:                        
                new_item_Price_Spinbox.config(state=tk.DISABLED)
        


            new_item_Shop_Label = ttk.Label(new_item_fram, text="Shop :")
            new_item_Shop_Label.grid(row=1, column=3, sticky="nsew")
            new_item_Shop_Combobox = ttk.Combobox(new_item_fram, values=[], width=10)
            new_item_Shop_Combobox.grid(row=2, column=3, padx=5, pady=5, sticky=tk.W)
            itemshop = [shop['Shop_name'] for shop in self.Shops if str(shop['Shop_id']) == str(selected_item['at_shop'])]
            if len(itemshop) > 0:
                new_item_Shop_Combobox.set(itemshop[0])
            new_item_Code_Label = ttk.Label(new_item_fram, text="Code :" )
            new_item_Code_Label.grid(row=1, column=4, sticky="nsew")
            new_item_Code_Combobox = ttk.Combobox(new_item_fram, values=[], width=10)
            new_item_Code_Combobox.grid(row=2, column=4, padx=5, pady=5, sticky=tk.W)
            #new_item_Code_Combobox.set("")
            new_item_Color_Label = ttk.Label(new_item_fram, text="Color ")
            new_item_Color_Label.grid(row=1, column=5, sticky="nsew")
            new_item_Color_Combobox = ttk.Combobox(new_item_fram, values=[], width=10)
            new_item_Color_Combobox.grid(row=2, column=5, padx=5, pady=5, sticky=tk.W)
            #new_item_Color_Combobox.set("")
            new_item_Size_Label = ttk.Label(new_item_fram, text="Size ")
            new_item_Size_Label.grid(row=1, column=6, sticky="nsew")
            new_item_Size_Combobox = ttk.Combobox(new_item_fram, values=[], width=10)
            new_item_Size_Combobox.grid(row=2, column=6, padx=5, pady=5, sticky=tk.W)
            #new_item_Size_Combobox.set("")

            new_item_QTY_Label = ttk.Label(new_item_fram, text="QTY Max is "+str(qty))
            new_item_QTY_Label.grid(row=1, column=7, sticky="nsew")
            new_item_QTY_Spinbox = ttk.Spinbox(new_item_fram, from_=0, width=10)
            new_item_QTY_Spinbox.grid(row=2, column=7, sticky="nsew")
            new_item_QTY_Spinbox.set(0)
            
            new_barcode_Label = ttk.Label(new_item_fram, text=str(selected_item['barcode']))
            new_barcode_Label.grid(row=1, column=5, sticky="nsew")
            
            del_button = ttk.Button(new_item_fram, text="Delete", command= lambda index=i, frame=new_item_fram: self.delete_product(index, frame))
            del_button.grid(row=0, column=8, sticky="nsew")
            Edit_button = ttk.Button(new_item_fram, text="Full Edit", command= lambda index=i, v=selected_item: self.Product_Edition_form(index, v))
            Edit_button.grid(row=1, column=8, sticky="nsew")
            # self.master.bind("<Delete>", lambda _: self.remove_item())
            
            data = [new_item_Shop_Combobox, new_item_Code_Combobox, new_item_Color_Combobox, new_item_Size_Combobox, new_item_QTY_Spinbox, new_barcode_Label, new_item_QTY_Label, new_item_Price_Spinbox, new_item_Price_Label, new_item_name_input]

            self.Get_next_seletion("", data, selected_item_info)
            #slef.get_total_qty(data, selected_item_info)
            
            save_button = ttk.Button(new_item_fram, text="Save Change", command= lambda index=i, d=data, v=selected_item_info: self.SAVE_CHANGE(index, d, v))
            save_button.grid(row=2, column=8, sticky="nsew")

            new_item_Shop_Combobox.bind("<<ComboboxSelected>>", lambda  _, d=data, v=selected_item_info, p=new_item_Price_Spinbox, tp=[], j=i: self.Update_selected_item_info(d, v, p, tp, j))
            new_item_Code_Combobox.bind("<<ComboboxSelected>>", lambda  _, d=data, v=selected_item_info, p=new_item_Price_Spinbox, tp=[], j=i: self.Update_selected_item_info(d, v, p, tp, j))
            new_item_Color_Combobox.bind("<<ComboboxSelected>>", lambda  _, d=data, v=selected_item_info, p=new_item_Price_Spinbox, tp=[], j=i: self.Update_selected_item_info(d, v, p, tp, j))
            new_item_Size_Combobox.bind("<<ComboboxSelected>>", lambda  _, d=data, v=selected_item_info, p=new_item_Price_Spinbox, tp=[], j=i: self.Update_selected_item_info(d, v, p, tp, j))

            new_item_Shop_Combobox.bind("<<ComboboxClicked>>", lambda  _, d=data, v=selected_item_info, p=new_item_Price_Spinbox, tp=[], j=i: self.Update_selected_item_info(d, v, p, tp, j))
            new_item_Code_Combobox.bind("<<ComboboxClicked>>", lambda  _, d=data, v=selected_item_info, p=new_item_Price_Spinbox, tp=[], j=i: self.Update_selected_item_info(d, v, p, tp, j))
            new_item_Color_Combobox.bind("<<ComboboxClicked>>", lambda  _, d=data, v=selected_item_info, p=new_item_Price_Spinbox, tp=[], j=i: self.Update_selected_item_info(d, v, p, tp, j))
            new_item_Size_Combobox.bind("<<ComboboxClicked>>", lambda  _, d=data, v=selected_item_info, p=new_item_Price_Spinbox, tp=[], j=i: self.Update_selected_item_info(d, v, p, tp, j))

            new_item_Price_Spinbox.bind("<KeyRelease>", lambda  _, d=data, v=selected_item_info, p=new_item_Price_Spinbox, tp=[], j=i: self.Update_selected_item_info(d, v, p, tp, j))

            new_item_Price_Spinbox.config(command= lambda d=data, v=selected_item_info, p=new_item_Price_Spinbox, tp=[], j=i: self.Update_selected_item_info(d, v, p, tp, j))
            new_item_QTY_Spinbox.config(command= lambda  d=data, v=selected_item_info, p=new_item_Price_Spinbox, tp=[], j=i: self.Update_selected_item_info(d, v, p, tp, j))
            #new_item_TPrice_Spinbox.bind(command= lambda d=data, v=selected_item_info, p=new_item_Price_Spinbox, tp=new_item_TPrice_Spinbox, j=i: self.Update_selected_item_info(d, v, p, tp, j))
        
        self.vv = [items, TQTY, Tprice, Tcost, vv]
        self.update_info()
        self.List_Frame_contaner_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        # Define the function for deleting a product
        
    def delete_product(self, index, frame):
        # Get the ID of the selected product
        product_id = selected_item = self.master.master.master.master.Shops_info['Shop_items'][index][0]['id']
        answer = tk.messagebox.askquestion("Question", "Do you what to delete "+str(product_id)+" ?")
        if answer == 'yes':
            itemshop = [[shop, i] for i, shop in enumerate(self.Shops) if str(shop['Shop_id']) == str(self.master.master.master.master.Shops_info['Shop_items'][index][0]['at_shop'])]
            if itemshop:
                at_shop = itemshop[0][0]['Shop_id']
                found_shop_items = json.loads(itemshop[0][0]['Shop_items'])
                if found_shop_items:
                    for si, sitem in enumerate(found_shop_items):
                        if sitem[0] == product_id:
                            found_shop_items.remove(sitem)
                            ITEM = json.dumps(found_shop_items)
                            #print("ITEM : " + str(ITEM))
                            #print("at_shop : " + str(at_shop))
                            cur.execute('UPDATE Shops SET Shop_items=? WHERE Shop_id=?', (ITEM, at_shop))
                            # Commit the changes to the database
                            conn.commit()
                            self.Shops[itemshop[0][1]]['Shop_items'] = ITEM
                            # Delete the product from the database
                            cur.execute('DELETE FROM product WHERE id=?', (product_id,))
                            # Commit the changes to the database
                            conn.commit()
                            break
            self.Load_Shop_items()
    #
    #
    #
    # OTHER
    #
    #
    #
    # for Searching Products in database And Displaying tham
    def Show_product_Info(self):
        if self.Product_info_frame:
            self.show_info_button.config(text="Show Information")
            self.Product_info_frame.destroy()
            self.Product_info_frame = None
        else:
            self.show_info_button.config(text="Hide Information")
            shop_items = self.vv
            #[item[0] for item in self.master.master.master.master.Shops_info['Shop_items']]
            self.Product_info_frame = ProductFullInfoForm(self.Frame_contaner_frame, self.user_info, self.Shops, shop_items)
            self.Product_info_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
    # for Adding new Product
    # Create the "Add New" button  
    def Queck_Edition_form(self):
        self.List_Frame_contaner_frame.pack_forget()
        notebook_frame = ProductQueckEditionForm(self.Frame_contaner_frame, self.user_info, self.Shops)
        notebook_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
    
    def Full_Edition_form(self):
        self.List_Frame_contaner_frame.pack_forget()
        notebook_frame = ProductFullEditionForm(self.Frame_contaner_frame, self.user_info, self.Shops)
        notebook_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        notebook_frame.clear_product_details_widget()

    # Create the "Change" button
    def Product_Edition_form(self, index, selected_product):
        self.List_Frame_contaner_frame.pack_forget()
        notebook_frame = ProductFullEditionForm(self.Frame_contaner_frame, self.user_info, self.Shops)
        notebook_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        notebook_frame.clear_product_details_widget()
        if selected_product:
            # Get the ID of the selected product
            product_id = selected_product['id']

            # Delete the product from the database
            cur.execute('SELECT * FROM product WHERE id=?', (product_id,))
            products = cur.fetchall()

            #print("name : " + str(products))
            id, name, code, _type, barcode, at_shop, quantity, cost, \
              tax, price, include_tax, price_change, more_info , images, \
                description , service , default_quantity, active = products[0]
            #load doc files
            notebook_frame.product_id = selected_product['id']
            notebook_frame.perform_doc_search(code)
            # Clear the current text
            # than add new one
            notebook_frame.name_entry.delete(0, tk.END)
            notebook_frame.name_entry.insert(0, name)
            notebook_frame.on_name_entry(name)
            notebook_frame.code_entry.delete(0, tk.END)
            notebook_frame.code_entry.insert(0, code)
            # notebook_frame.type_entry.delete(0, tk.END) notebook_frame.type_entry
            # notebook_frame.type_entry.insert(0, )
            notebook_frame.type_entry.load(_type)
            #notebook_frame.barcode_entry.delete(0, tk.END)
            #notebook_frame.barcode_entry.insert(0, barcode)
            #notebook_frame.at_shop_entry.delete(0, tk.END)
            #notebook_frame.at_shop_entry.insert(0, at_shop)
            #notebook_frame.quantity_entry.delete(0, tk.END)
            #notebook_frame.quantity_entry.insert(0, quantity)
            notebook_frame.cost_entry.delete(0, tk.END)
            notebook_frame.cost_entry.insert(0, cost)
            notebook_frame.tax_entry.delete(0, tk.END)
            notebook_frame.tax_entry.insert(0, tax)
            notebook_frame.price_entry.delete(0, tk.END)
            notebook_frame.price_entry.insert(0, price)
            notebook_frame.include_tax_var.set(int(include_tax))
            notebook_frame.price_change_var.set(int(price_change))
            notebook_frame.more_info_label.delete(0, tk.END)
            notebook_frame.more_info_label.insert(0, more_info)
            notebook_frame.get_inventory_nested_list(more_info, code) # this will save more_info after reading it
            
            notebook_frame.images_entry.delete(0, tk.END)
            notebook_frame.images_entry.insert(0, images)
            notebook_frame.description_entry.delete(0, tk.END)
            notebook_frame.description_entry.insert(0, description)
            notebook_frame.service_change_var.set(int(service))
            notebook_frame.default_quantity_change_var.set(int(default_quantity))
            notebook_frame.active_var.set(int(active))
            
            notebook_frame.add_button.config(text="Update")
            # Commit the changes to the database
            conn.commit()
            #notebook_frame.details_frame.pack(side=tk.RIGHT, fill=tk.Y, expand=False)
            #notebook_frame.notebook_frame.pack(side=tk.RIGHT, fill=tk.Y, expand=False)
            #print("change notebook_frame.nested_list = "+str(notebook_frame.nested_list))

    # create a function to update the search results whenever the search box changes
    def update_search_results(self, *args):
        # get the search string from the search box
        search_str = self.search_var.get()
        self.Update_shop_item_list(search_str)












    
        
    def show_product_form(self):
        # call the function in the main file to show the first frame
        self.master.master.show_frame("ProductFrame")
        self.chackname = Chacke_Security(self, self.user, self.Shops[self.on_Shop], 34, f'User Has No Permission To Access Change PRODUCT Name OR LOGIN AS ADMIN')
        self.chackprice = Chacke_Security(self, self.user, self.Shops[self.on_Shop], 35, f'User Has No Permission To Access Change PRODUCT Price OR LOGIN AS ADMIN')
        
    





        
    
    # Create the "Delete" button
    


    def get_item_by_code(self, item_code):
        self.cursor.execute("SELECT * FROM product WHERE code=?", (item_code,))
        result = self.cursor.fetchone()
        
        return result
    
    def update_item_info(self, id, code, it_info):
        pass

    
    def fix_date(self):
        v = GetDateForm(self, self.date_from_Entry.get(), self.date_to_Entry.get())
        self.start_value = str(v.start_value[0])+"-"+str(v.start_value[1])+"-"+str(v.start_value[2])
        #datetime.strftime(v.start_value, '%Y-%m-%d %H:%M:%S')
        self.end_value = str(v.end_value[0])+"-"+str(v.end_value[1])+"-"+str(v.end_value[2])
        #datetime.strftime(v.end_value, '%Y-%m-%d %H:%M:%S')
        #print("v.start_value :" + str(self.start_value))
        #print("v.end_value :" + str(self.end_value))
        self.date_from_Entry.delete(0, tk.END)
        self.date_to_Entry.delete(0, tk.END)
        self.date_from_Entry.insert(0, self.start_value)
        self.date_to_Entry.insert(0, self.end_value)
        self.perform_search()
        
    def create_sizes_form(self):
        selected_type = self.sizing_var.get()
        if selected_type == "Select Sizing Type":
            return

        self.form_frame.destroy()  # Clear previous form entries

        self.form_frame = ttk.Frame(self.second_frame)
        self.form_frame.pack(pady=10)

        self.form_entries = []  # Reset the list of form entries

        sizes_label = tk.Label(self.form_frame, text="Enter Quantities for the Sizes:")
        sizes_label.pack()

        sizes_text = tk.Text(self.form_frame, height=5, width=40)
        sizes_text.pack()

        sizes = []
        if selected_type == "Trouser Sizes":
            sizes = [str(size) + ":0" for size in range(21, 46)]
        elif selected_type == "Clothing Sizes":
            sizes = ["XS:0", "S:0", "M:0", "L:0", "XL:0", "2XL:0", "3XL:0", "4XL:0", "5XL:0"]
        elif selected_type == "Shoe Sizes":
            sizes = [str(size) + ":0" for size in range(1, 13)] + [str(a) + ":0" for a in range(30, 45)]

        for size in sizes:
            sizes_text.insert(tk.END, size + ", ")

        done_button = tk.Button(self.form_frame, text="Done", command=lambda: self.generate_list(selected_type, sizes_text.get("1.0", tk.END)))
        done_button.pack()

    def generate_list(self, sizing_type, sizes):
        sizes_list = sizes.strip().split(",")  # Split the entered sizes by comma
        sizes_list = [size.strip() for size in sizes_list]  # Remove leading/trailing whitespaces

        self.result = []
        for size in sizes_list:
            size_parts = size.split(":")
            if len(size_parts) == 2:
                size_value = size_parts[0].strip()
                quantity = size_parts[1].strip()
                if quantity != "0":
                    self.result.append([size_value, quantity])
                    
        for v in self.result:
            found = 0 
            i = 0
            for p in self.inventory:
                if p["shop_name"] == self.shop_name_Combobox.get() and p["color"] == self.color_entry.get() and \
                p["size"] == v[0]:
                    if p["barcode"] == self.bracode_entry.get() and p["qtyfirst"] == v[1] and \
                        p["qty"] == v[1]:
                        print("issame!!!" + str(p)) # TODO: show same earror
                        #    cdate#    update
                    else:
                        self.inventory[i]["barcode"] = self.bracode_entry.get()
                        self.inventory[i]["qty"] = v[1]
                    found = 1
                else:
                    found = 0
                i += 1
            # TODO add stock pathern in this new list
            found, self.nested_list = add_new_list(self.nested_list, self.shop_name_Combobox.get() + "|" + self.code_entry.get() + "|" + self.color_entry.get() + "|" + v[0], [self.bracode_entry.get(), v[1], v[1], "", self.images_entry.get(), "", ""])
            if found:
                self.add_info_(self.shop_name_Combobox.get(), self.code_entry.get(), self.color_entry.get(), v[0], self.bracode_entry.get(), v[1], v[1], "", "")
        txt = self.get_inventory_nested_list_text()
        self.more_info_label.delete(0, tk.END)
        self.more_info_label.insert(0, txt)

        
        
    
        
        
    
    def get_unique_shop_names(self):
        return list(set([p["shop_name"] for p in self.inventory]))

    def get_unique_codes_for_shop_name(self, shop_name):
        return list(set([p["code"] for p in self.inventory if p["shop_name"] == shop_name]))

    def get_unique_colors_for_shop_name(self, shop_name, code):
        return list(set([p["color"] for p in self.inventory if p["shop_name"] == shop_name and p["code"] == code]))

    def get_sizes_for_shop_name_and_color(self, shop_name, code, color):
        return list(set([p["size"] for p in self.inventory if p["shop_name"] == shop_name and p["code"] == code and p["color"] == color]))

    def get_barcode_and_qty_for_shop_name_and_color_and_size(self, shop_name, code, color, size):
        for p in self.inventory:
            if p["shop_name"] == shop_name and p["code"] == code and p["color"] == color and p["size"] == size:
                return (p["barcode"], p["qtyfirst"], p["qty"], p["cdate"], p["update"])
        return (None, None)
    
    def add_product_from_nested_list(self, nested_list):
        for s in nested_list:
            if not s:
                break
            shop_name, nested_items = s
            color, nested_items2 = nested_items
            size, nested_items3 = nested_items2
            #print("shop name : " + shop_name)
            #print("shop nested_item : " + str(nested_items))
            barcode, qtyfirst, qty, cdate, update = nested_items3
            self.add_info_(shop_name, color, size, barcode, qtyfirst, qty, cdate, update)
    
    def get_inventory_nested_list(self, text, code):
        #print("get_inventory_nested_list text = "+str(text))
        if "\"{" in str(text):
            self.nested_list = read_code(text, "", str(code), "", "")[4]
        else:
            self.nested_list = load_list(text) 
        self.update_tree()

    def get_inventory_nested_list_text(self):
        return str(self.nested_list)
    
    '''def update_tree(self):
        self.tree.delete(*self.tree.get_children())
        print("gount tot add tree ")
        for shop in self.nested_list:
            print("shop")
            shop_name_node = self.tree.insert("", "end", text=shop[0])
            for code in shop[1]:
                print("code")
                code_node = self.tree.insert(shop_name_node, "end", text=code[0])
                for color in code[1]:
                    color_node = self.tree.insert(code_node, "end", text=color[0])
                    for size in color[1]:
                        size_node = self.tree.insert(color_node, "end", text=size[0])
                        for value in size[1]:
                            print("value : " + str(value))
                            barcode, qtyfirst, qty, patern, imgs, cdate, update = ["", "", "", "", "", "", ""]
                            cvalue = value
                            if len(cvalue) == 7:
                                barcode, qtyfirst, qty, patern, imgs, cdate, update = value
                            if len(cvalue) == 4:
                                barcode, qtyfirst, qty, update = value
                            if barcode and qtyfirst and qty and cdate and update:
                                self.tree.insert(size_node, "end", text=value[0], values=(barcode, qtyfirst, qty, patern, imgs, cdate, update))
                            else:
                                self.tree.insert(size_node, "end", text=value[0], values=(barcode, qtyfirst, qty, patern, imgs, cdate, update))
    '''
                            
    def remove_info(self):
        path = ""
        if self.shop_name_Combobox.get() != "":
            path += self.shop_name_Combobox.get()
        if self.code_entry.get() != "":
            path += "|" + self.code_entry.get()
        if self.color_entry.get() != "":
            path += "|" + self.color_entry.get()
        if self.size_entry.get() != "":
            path += "|" + self.size_entry.get()
        #print("removeing : "+str([path, [self.bracode_entry.get(), self.qty_entry.get(), self.qty_entry.get(), "", self.images_entry.get(), "", ""]]))
        #print("self.nested_list : "+str(self.nested_list))
        found, self.nested_list = dele_list(self.nested_list, self.shop_name_Combobox.get() + "|" + self.code_entry.get() + "|" + self.color_entry.get() + "|" + self.size_entry.get() , [self.bracode_entry.get(), self.qty_entry.get(), self.qty_entry.get(), "", self.images_entry.get(), "", ""])
        self.more_info_label.delete(0, tk.END)
        self.more_info_label.insert(0, str(self.nested_list))
        self.update_tree()
        
    def add_info(self):
        found = 0 
        i = 0
        for p in self.inventory:
            if p["shop_name"] == self.shop_name_Combobox.get() and p["color"] == self.color_entry.get() and \
               p["size"] == self.size_entry.get():
                if p["barcode"] == self.bracode_entry.get() and p["qtyfirst"] == self.qty_entry.get() and \
                    p["qty"] == self.qty_entry.get():
                    print("issame!!!" + str(p)) # TODO: show same earror
                    #    cdate#    update
                else:
                    self.inventory[i]["barcode"] = self.bracode_entry.get()
                    self.inventory[i]["qty"] = self.qty_entry.get()
                found = 1
            else:
                found = 0
            i += 1

        #{'shop_name': '1', 'color': '2', 'size': '3', 'barcode': '4', 'qtyfirst': '4', 'qty': '4', 'cdate': '', 'update': ''}
                #return (p["barcode"], p["qtyfirst"], p["qty"], p["cdate"], p["update"])
        found, self.nested_list = add_new_list(self.nested_list, self.shop_name_Combobox.get() + "|" + self.code_entry.get() + "|" + self.color_entry.get() + "|" + self.size_entry.get() , [self.bracode_entry.get(), self.qty_entry.get(), self.qty_entry.get(), "", self.images_entry.get(), "", ""])
        #print("self.nested_list : " + str(self.nested_list))
        if found:
            self.add_info_(self.shop_name_Combobox.get(), self.code_entry.get(), self.color_entry.get(), self.size_entry.get(), self.bracode_entry.get(), self.qty_entry.get(), self.qty_entry.get(), "", self.images_entry.get(), "", "")
            
            

        txt = self.get_inventory_nested_list_text()
        self.more_info_label.delete(0, tk.END)
        self.more_info_label.insert(0, txt)
        self.update_tree()
        
    def new_stock_on_path_select(self, event):
        item = self.tree.selection()[0]
        found_values = []
        found_vv = []
        parent_item = item
        while parent_item:
            txt = self.tree.item(parent_item, "text")
            value = self.tree.item(parent_item, "value")
            found_values.append(txt)
            if value and len(value) > 4:
                found_vv = value
            parent_item = self.tree.parent(parent_item)
            
        found_values.reverse()
        #print("found_vv value : " + str(found_vv))
        if found_vv:
            found_values = found_values+list(found_vv)
        #print("found value : " + str(found_values))
        if found_values:
            self.shop_name_Combobox.current(0)
            self.code_entry.delete(0, tk.END)
            self.color_entry.delete(0, tk.END)
            self.size_entry.delete(0, tk.END)
            self.bracode_entry.delete(0, tk.END)
            self.qty_entry.delete(0, tk.END)
            self.images_entry.delete(0, tk.END)
            for i, value in enumerate(found_values):
                if i == 0:
                    self.shop_name_Combobox.current(self.Shops_Names.index(value))
                if i == 1:
                    self.code_entry.insert(0, value)
                if i == 2:
                    self.color_entry.insert(0, value)
                if i == 3:
                    self.size_entry.insert(0, value)
                if i == 7:
                    self.qty_entry.insert(0, value)
                if i == 9:
                    self.bracode_entry.insert(0, value)
                if i == 10:
                    self.images_entry.insert(0, value)
        #print("selected self.nested_list = "+str(self.nested_list))
    
