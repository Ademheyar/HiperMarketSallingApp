import tkinter as tk
from tkinter import ttk
import sqlite3
import os
import sys
import threading
import time
import json
import ast
current_dir = os.path.abspath(os.path.dirname(__file__))
MAIN_dir = os.path.join(current_dir, '..')
sys.path.append(MAIN_dir)

from D.ItemSelector import ItemSelectorWidget
from D.Doc.Loaddoc import *
from C.List import *

from C.API.Get import *
from C.API.API import *
from C.API.Set import *
from D.Security import *

data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data'))
db_path = os.path.join(data_dir, 'my_database.db')

import tkinter as tk
from tkinter import ttk

class search_entry(ttk.Entry):
    def __init__(self, master, Shops_info, user, Shops, *args, **kwargs):
        self.master = master
        self.user = user
        self.Shops = Shops
        self.Shops_Names = [shop['Shop_name'] for shop in self.Shops]
        self.homemaster = self
        p = 0
        while(True):
            p += 1
            #print("chacking parent p = " + str(p))
            if hasattr(self.homemaster, 'Shops_info') and hasattr(self.homemaster, 'onDisplayFrame'):
                break
            else:
                self.homemaster = self.homemaster.master
                        
        ttk.Entry.__init__(self, master, *args, **kwargs)
        self.var = self["textvariable"]
        if self.var == '':
            self.var = self["textvariable"] = tk.StringVar()
        self.chacke_ifitisallowed()
        self.var.trace('w', self.changed)
        self.bind("<Up>", self.treeview_naigation)
        self.bind("<Down>", self.treeview_naigation)
        self.bind("<Return>", self.select)
        self.bind("<Insert>", lambda _:self.Done_search())
        self.bind("<Escape>", lambda _: self.var.set(''))

        
        # Connect to database
        self.cursor = conn.cursor()
        # Initialize search type
        self.selected_indexd = -1;
        self.search_type = ""
        self.lb_up = False
        self.items = []
        self.all_items = []
        self.selected_products = []
        self.debounce_id = None

    def chacke_ifitisallowed(self):
        shop_obj = self.homemaster.Shops[self.homemaster.on_Shop]
        self.perm_actions = Chacke_Security(self, self.homemaster.user, shop_obj, 24, 'User Need Permetion To Search For Products')
        self.perm_items = Chacke_Security(self, self.homemaster.user, shop_obj, 9, 'User Need Permetion To Search For Actions')
        self.perm_docs = Chacke_Security(self, self.homemaster.user, shop_obj, 23, 'User Need Permetion To Search For Documents')

    def Load_Shop_items(self):
        for s, shop in enumerate(self.Shops):

            #print("Loop Shop ", shop['Shop_name'])
            #print("Selected Shop ", self.homemaster.Selected_Shop)
            #print("Shop items = ", shop['Shop_items'])
            if shop['Shop_items'] and (self.homemaster.Selected_Shop == "" or s == self.homemaster.User_Shopes_Combobox.current()):
                found_shop_items = json.loads(shop['Shop_items'])
                self.homemaster.Shops_info['Shop_Actions'] = shop['Shop_Actions']
                #print("Shop items --> ", found_shop_items)
                if found_shop_items:
                    for item in found_shop_items:
                        value = fetch_as_dict_list( 'SELECT * FROM product WHERE id=?', (str(item[0]),))
                        if value and not len(value) == 0:
                            self.homemaster.Shops_info['Shop_items'].append([value[0], []])
        
    def Update_selected_Ifo(self):
        Total_price = 0
        Total_qty = 0
        Total_Document = 0
        Total_Actions = 0
        for item_info in self.selected_products:
            price = 0
            if(item_info['type'] == 'ITEM'):
                for data in item_info['extra_data']:
                    #print("selected_data = ", data)
                    if data[7] != []:
                        for t, typ in enumerate(data[7]):                            
                            Total_qty += float(typ[1])
                            Total_price += float(typ[2])*float(typ[1])
                    else:
                        if price == 0:
                            price = float(item_info['values']['price'])
                        Total_qty += float(data[4])
                        price = price*float(data[4])
            elif(item_info['type'] == 'DOCUMENT'):
                Total_Document += 1
            elif(item_info['type'] == 'ACTIONS'):
                Total_Actions += 1
            Total_price += price
        self.Done_btn.config(text="Done \n Total QTY " + str(Total_qty) + " Total Price "+ str(Total_price)+ " Total Documents "+ str(Total_Document)+ " Total Actions "+ str(Total_Actions))

    def Selectd_item_add(self, item_id, extra_data, selected_type):
        selected_item_info = None
        for item_info in self.selected_products:
            if item_info['values']['id'] == item_id:
                selected_item_info = item_info
                if(item_info['type'] == 'ITEM'):
                    shop = extra_data[0].get()
                    code = extra_data[1].get()
                    color = extra_data[2].get()
                    size = extra_data[3].get()
                    qty = extra_data[4].get()
                    qtyleft = extra_data[5].cget('text')
                    if qty == '':
                        qty = '0'
                    barcode = extra_data[6].cget('text')
                    index = 0
                    foundtyp = 0
                    for data in item_info['extra_data']:
                        if data[0] == shop and data[1] == code and data[2] == color and data[3] == size:
                            if(selected_type != []):
                                #print("item_info['extra_data'][index][7] : ", item_info['extra_data'][index][7])
                                #print("selected_type[0] : ", selected_type[0])
                                for t, typ in enumerate(item_info['extra_data'][index][7]):
                                    if(typ[0] == selected_type[0]):
                                        item_info['extra_data'][index][7][t][1] += int(selected_type[1])
                                        foundtyp = 1
                            elif qty != '' and item_info['extra_data'][index][4] != '':
                                qty = float(item_info['extra_data'][index][4]) + float(qty)
                            break
                        index += 1
                    if foundtyp == 0:
                        if str(qty) != extra_data[4].get():
                            if(selected_type != []):
                                item_info['extra_data'][index][6].append(selected_type)
                            else:
                                item_info['extra_data'][index][4] = qty
                        else:
                            typ = []
                            if(selected_type != []):
                                typ = [selected_type]
                            
                            data = [shop, code, color, size, qty, qtyleft, barcode, typ]                    
                            item_info['extra_data'].append(data)
                        
                break

        if selected_item_info is None:
            for info in self.all_items:
                item = info[2]
                if item[0] == item_id:
                    if(info[0] == 'ITEM'):
                        typ = []
                        if(selected_type != []):
                            typ = [selected_type]
                        data = [extra_data[0].get(), extra_data[1].get(), extra_data[2].get(), extra_data[3].get(), extra_data[4].get(), extra_data[5].cget('text'), extra_data[6].cget('text'), typ]
                        selected_item_info = {'values': item, 'type': 'ITEM', 'extra_data': [data]}
                        self.selected_products.append(selected_item_info)
                    elif(info['type'] == 'DOCUMENT'):
                        selected_item_info = {'values': item, 'type': 'DOCUMENT'}
                        self.selected_products.append(selected_item_info)
                    
                    elif(info['type'] == 'ACTIONS'):
                        selected_item_info = {'values': item, 'type': 'ACTIONS'}
                        self.selected_products.append(selected_item_info)
                    break
        #print(self.selected_products)
        self.Update_selected_Ifo()
        
    def Selectd_item_remove(self, item_id, extra_data, selected_type):
        selected_item_info = None
        for item_info in self.selected_products:
            if item_info['values']['id'] == item_id:
                selected_item_info = item_info
                if(item_info['type'] == 'ITEM'):
                    shop = extra_data[0].get()
                    code = extra_data[1].get()
                    color = extra_data[2].get()
                    size = extra_data[3].get()
                    qty = extra_data[4].get()
                    barcode = extra_data[6].cget('text')
                    index = 0
                    foundtyp = 0
                    for data in item_info['extra_data']:
                        if data[0] == shop and data[1] == code and data[2] == color and data[3] == size:
                            if(selected_type != []):
                                #print("item_info['extra_data'][index][6] : ", item_info['extra_data'][index][7])
                                #print("selected_type[0] : ", selected_type[0])
                                for t, typ in enumerate(item_info['extra_data'][index][7]):
                                    if(typ[0] == selected_type[0]):
                                        qty = float(item_info['extra_data'][index][4]) - float(qty)
                                        found = 1
                                        foundtyp = 1
                            else:
                                qty = float(item_info['extra_data'][index][4]) - float(qty)
                                found = 1
                            break
                        index += 1
                    if found == 1 and str(qty) != "0":
                        item_info['extra_data'][index][4] = qty
                    elif index != -1:
                        item_info['extra_data'].remove(item_info['extra_data'][index])
                break

        '''if selected_item_info is None:
            for info in self.all_items:
                item = info[2]
                if item[0] == item_id:
                    if(info[0] == 'ITEM'):
                        typ = []
                        if(selected_type != []):
                            typ = [selected_type]
                        data = [extra_data[0].get(), extra_data[1].get(), extra_data[2].get(), extra_data[3].get(), extra_data[4].get(), extra_data[5].cget('text'), typ]
                        selected_item_info = {'values': item, 'type': 'ITEM', 'extra_data': [data]}
                        self.selected_products.append(selected_item_info)
                    elif(info['type'] == 'DOCUMENT'):
                        selected_item_info = {'values': item, 'type': 'DOCUMENT'}
                        self.selected_products.append(selected_item_info)
                    break'''
        #print(self.selected_products)
        self.Update_selected_Ifo()
        
    def Get_next_seletion(self, item_id, inputs, item_list):
        shop = inputs[0].get()
        code = inputs[1].get()
        color = inputs[2].get()
        size = inputs[3].get()
        qty = inputs[4].get()
        barcode = inputs[6].cget('text')
        if item_list['item_list']:
            #print(str(item_list['item_list']))
            info_list = item_list['item_list']
            
            sv = [s[0] for s in info_list]
            inputs[0].config(values=sv)
            
            if shop == "":
                if self.homemaster.Selected_Shop != "" and self.homemaster.Selected_Shop in sv:
                   inputs[0].set(self.homemaster.Selected_Shop)
                elif self.Shops_Names[0] in sv:
                    inputs[0].set(self.Shops_Names[0])
                shop = inputs[0].get()
            
            for i0, sh in enumerate(info_list):
                if sh[0] == shop or i0 == 0:
                    shv = [shc[0] for shc in info_list]
                    inputs[0].config(values=shv)
                    if len(shv) > 1 and inputs[0].get() == "":
                        inputs[0].focus_set()
                        inputs[0].selection_range(0, tk.END)
                    for i1, codes in enumerate(sh[1]):
                        if codes[0] == code or i1 == 0:
                            cov = [cc[0] for cc in sh[1]]
                            inputs[1].config(values=cov)
                            if len(cov) > 1 and inputs[1].get() == "":
                                inputs[1].focus_set()
                                inputs[1].selection_range(0, tk.END)
                            if len(cov) == 1 or codes[0] == code:
                                inputs[1].set(codes[0])
                                code = inputs[1].get()
                                
                            for i2, c in enumerate(codes[1]):
                                if c[0] == color or i2 == 0:
                                    cv = [colorc[0] for colorc in codes[1]]
                                    inputs[2].config(values=cv)
                                    if len(cv) > 1 and sh[0] == shop and inputs[2].get() == "":
                                        inputs[2].focus_set()
                                        inputs[2].selection_range(0, tk.END)
                                    if len(cv) == 1 or c[0] == color:
                                        inputs[2].set(c[0])
                                        color = inputs[2].get()
                                    for i3, s in enumerate(c[1]):
                                        if s[0] == size or i3 == 0:
                                            siv = [si[0] for si in c[1]]
                                            inputs[3].config(values=siv)
                                            if len(siv) > 1 and sh[0] == shop and codes[0] == code and inputs[3].get() == "":
                                                inputs[3].focus_set()
                                                inputs[3].selection_range(0, tk.END)
                                            if len(siv) == 1 or s[0] == size:
                                                inputs[3].set(siv[0])
                                                size = inputs[3].get()
                                            # TODO: SICURTY IF NOT ALLWOD TO SHOW QTY Left
                                            #print(s[1])
                                            #print(s[1][0])
                                            #print(s[1][0][5])
                                            
                                            inputs[4].set(float(s[1][0][4]))
                                            inputs[5].config(text=s[1][0][4])
                                            if(len(s[1]) > 1):
                                                inputs[7].grid(row=0, column=5)
                                                for t in s[1]:
                                                    ttk.Button(inputs[8], command=lambda j=item_id, v=inputs, st=[t[1], 1, t[2]]: self.Selectd_item_add(j, v, st), text=t[1].replace("[", "").replace("]", "").replace("\"", "")+" With " + str(t[2])).pack()
                                            if sh[0] == shop and codes[0] == code and c[0] == color and s[0] == size:
                                                inputs[4].focus_set()
                                                inputs[4].selection_range(0, tk.END)
                                                return
                                            
    def create_info_getter(self, sid, index, parent):
        info = self.all_items[index]
        item = info[2]
        #selected_item_info = {'values': item, 'type': 'ITEM', 'extra_data': []}
        #if sid != -1:
        #    pass # TODO get old value using sid
            
        #print(str(item))
        item_list = []
        item_info = item['more_info']
        #print("user shop item_info ", item_info)
        if item_info == "":
            return
        else:
            item_list = json.loads(item_info)
        #print("More infos")
        #print(str(item_list))
        #print("user shop ")
        #print(str(self.user['User_work_shop']))
        selected_item_info = {'values': item, 'type': 'ITEM', 'extra_data': [], 'item_list': item_list}

        barcode = ttk.Label(parent, text="barcode")
        
        qtyleft = ttk.Label(parent, text="")
        barcode.grid(row=0, column=3, columnspan=3)
        
        moreinfo_frame = ttk.Frame(parent)
        moreinfo_frame.grid(row=1, column=2, columnspan=4, padx=5, pady=5, sticky=tk.W)
        
        shop = ttk.Combobox(moreinfo_frame, values=[], width=10)
        shop.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        code = ttk.Combobox(moreinfo_frame, values=[], width=10)
        code.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)
        color = ttk.Combobox(moreinfo_frame, values=[], width=10)
        color.grid(row=0, column=2, padx=5, pady=5, sticky=tk.W)
        size = ttk.Combobox(moreinfo_frame, values=[], width=10)
        size.grid(row=0, column=3, padx=5, pady=5, sticky=tk.W)
        
        qty = ttk.Spinbox(moreinfo_frame, from_=0, to=100, width=10)
        qty.grid(row=0, column=4, padx=5, pady=5, sticky=tk.W)
        
        def start_new():
            shop.focus_set()
            code.config(text="")
            color.config(text="")
            size.config(text="")
            qty.config(text="")
            barcode.config(text="")
            
        qty.bind("<Home>", lambda _: start_new())
        qty.bind("<Insert>", lambda _:self.Done_search())
        

        type_frame = ttk.Frame(parent)
        
        action_frame = ttk.Frame(parent)
        
        
        ttk.Button(action_frame, text='Action').pack()
        ttk.Button(action_frame, text='Action').pack()
        ttk.Button(action_frame, text='Action').pack()
        
        
        def show_type():
            type_frame.grid(row=2, column=2, padx=5, pady=5, sticky=tk.W) 
            action_frame.grid_forget()
            
        def show_action():
            action_frame.grid(row=2, column=2, padx=5, pady=5, sticky=tk.W)
            type_frame.grid_forget()
            
        typebtn = ttk.Button(parent, text='type', command= show_type)
        actionbtn = ttk.Button(parent, text='Action', command=show_action).grid(row=0, column=5, sticky=tk.E)
        
        data = [shop, code, color, size, qty, qtyleft, barcode, typebtn, type_frame, actionbtn, action_frame]
        
        if sid == -1:
            self.Get_next_seletion(item['id'], data, selected_item_info)
            
        self.selected_products.append(selected_item_info)
        shop.bind("<<ComboboxSelected>>", lambda  _, j=item['id'], i=data, v=selected_item_info: self.Get_next_seletion(j, i, v))
        code.bind("<<ComboboxSelected>>", lambda  _, j=item['id'], i=data, v=selected_item_info: self.Get_next_seletion(j, i, v))
        color.bind("<<ComboboxSelected>>", lambda  _, j=item['id'], i=data, v=selected_item_info: self.Get_next_seletion(j, i, v))
        size.bind("<<ComboboxSelected>>", lambda  _, j=item['id'], i=data, v=selected_item_info: self.Get_next_seletion(j, i, v))
        qty.bind("<Return>", lambda _, i=item['id'], v=data: self.Selectd_item_add(i, v, []))
        qty.bind("<Delete>", lambda _, i=item['id'], v=data: self.Selectd_item_remove(i, v, []))
        #qty.config(command=lambda  i=data, v=selected_item_info: self.Get_next_seletion(i, v))
        ttk.Button(moreinfo_frame, text='Add', command=lambda i=item['id'], v=data: self.Selectd_item_add(i, v, [])).grid(row=0, column=5, padx=5, pady=5, sticky=tk.W)
        ttk.Button(moreinfo_frame, text='Remove', command=lambda i=item['id'], v=data: self.Selectd_item_remove(i, v, [])).grid(row=0, column=6, padx=5, pady=5, sticky=tk.W)
        
                        
    def toggle_selected(self, item_id, var, parent):
        if var.get():
            i = 0
            for info in self.all_items:
                item = info[2]
                if(info[0] == 'ITEM'):
                    if item['id'] == item_id:
                        self.create_info_getter(-1, i, parent)
                        break
                elif(info[0] == 'DOCUMENT'):
                    if item['doc_barcode'] == item_id:
                        selected_item_info = {'values': item, 'type': 'DOCUMENT'}
                        self.selected_products.append(selected_item_info)
                        break
                elif(info[0] == 'ACTIONS'):
                    if item[1] == item_id:
                        selected_item_info = {'values': item, 'type': 'ACTIONS'}
                        self.selected_products.append(selected_item_info)
                        break
                i += 1
        else:
            i = 0
            for item_info in self.selected_products:
                if item_info['type'] == 'ITEM' and item_info['values'][0] == item_id or item_info['type'] == 'DOCUMENT' and item_info['values']['doc_barcode'] == item_id:
                    #print(parent.winfo_children())
                    self.selected_products.remove(self.selected_products[i])
                    break
                i+=1
        #print(self.selected_products)
        self.Update_selected_Ifo()
        
    def changed(self, name, index, mode):
        if self.homemaster.Shops_info['Shop_items'] == []:
            self.Load_Shop_items()
        if self.debounce_id is not None:
                self.after_cancel(self.debounce_id)
                
        if self.var.get() == '' and self.main_frame:
            self.main_frame.destroy()
            self.lb_up = False
        else:
            words = self.comparison()
            w = self.grid_size()[0]
            h = self.grid_size()[1]
            
            screen_width = self.winfo_screenwidth()
            screen_height = self.winfo_screenheight()
            if words:
                if not self.lb_up:
                    # Main Frame (initially hidden)
                    self.main_frame = ttk.Frame(self.master.master)
                    self.Contener_frame = ttk.Frame(self.main_frame)
                    self.Contener_frame.pack(side=tk.LEFT, fill=tk.X)
                    #self.main_frame.pack_forget()  # Hide the main frame initially
                    
                    self.canvas = tk.Canvas(self.Contener_frame, width=screen_width-(screen_width/3), height=screen_height-(screen_height/3))
                    self.canvas.pack(side=tk.TOP, fill=tk.BOTH)
                    self.scrollbar = ttk.Scrollbar(self.main_frame, command=self.canvas.yview)
                    self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y, expand=1)
                    self.canvas.configure(yscrollcommand=self.scrollbar.set)
                    
                    # Clear existing widgets
                    #self.lb.destroy()
                    # Frame inside Canvas
                    self.lb = ttk.Frame(self.canvas, width=self.canvas.cget('width'))
                    self.canvas.create_window((0, 0), window=self.lb, anchor=tk.NW)
                    self.lb.bind('<Configure>', lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))


                    # Bind the scrollbar to update the scrollregion
                    self.lb.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

                    self.Manue_fram = ttk.Frame(self.Contener_frame)
                    self.Manue_fram.pack(side=tk.TOP, fill=tk.BOTH)
                    self.Cancel_btn = ttk.Button(self.Manue_fram, text='Cancel', command=self.cancel_search)
                    self.Cancel_btn.pack(side=tk.LEFT, expand=1)
                    self.Done_btn = ttk.Button(self.Manue_fram, text='Done', command=self.Done_search)
                    self.Done_btn.pack(side=tk.RIGHT, expand=1)
                    self.Update_selected_Ifo()
                    
                for child in self.lb.winfo_children():
                    child.destroy()
                self.selected_indexd = -1;
                w = 0
                n_w = 0
                d_w = 0

                # check security permissions to show items
                if not self.perm_items:
                    words = [word for word in words if word[0] != 'ITEM']
                if not self.perm_docs:
                    words = [word for word in words if word[0] != 'DOCUMENT']
                if not self.perm_actions:
                    words = [word for word in words if word[0] != 'ACTIONS']
                
                self.load_more_items(words[:5])
                self.canvas.bind("<MouseWheel>", lambda e: self.load_more_items(words))
                    
                self.main_frame.place(x=self.winfo_x(), y=self.winfo_y()+self.winfo_height()+25)
                self.lb_up = True
            else:
                self.chacke_ifitisallowed()
                if self.lb_up:
                    self.main_frame.destroy()
                    self.lb_up = False
                        
    def load_more_items(self, words):
            w = self.grid_size()[0]
            h = self.grid_size()[1]
            
            screen_width = self.winfo_screenwidth()
            screen_height = self.winfo_screenheight()
            # load morre items on scroll 
            start_index = len(self.lb.winfo_children())
            # Create new list widgets based on search results
            for w, info in enumerate(words[start_index:start_index+5]):
                item = info[2]
                if(info[0] == 'ITEM'):
                    #print("word: " + str(len(item)))
                    #print("item: " + str(item))
                    f = tk.Frame(self.lb, width=screen_width-(screen_width/3), bg="#0d47a1", highlightthickness=2, highlightbackground="black")
                    #f.grid(row=len(self.lb.winfo_children()), column=0, pady=1, sticky=tk.EW)
                    f.pack(fill='x', expand=True, pady=10, padx=10)
                    s = len([item for selecteditem in self.selected_products if item['id'] == selecteditem['values']['id']]) > 0
                    if s:
                        self.create_info_getter(s, w, f)
                    var = tk.BooleanVar()
                    var.set(s)
                    checkbox = ttk.Checkbutton(f, variable=var, command=lambda i=item['id'], v=var, p=f: self.toggle_selected(i, v, p))
                    checkbox.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
                    ttk.Label(f, text=f"Name: {item['name']}", wraplength=150).grid(row=0, column=1, columnspan=2, sticky=tk.W)
                    ttk.Label(f, text=f"Price: {item['price']}", wraplength=70).grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
                    qty_info_list = json.loads(item['more_info'])
                    qty = 0
                    def sub_list(ls, qty):
                        comen_qty = 0
                        if(isinstance(ls, list)):
                            for l in ls:
                                if len(l) > 4 and l[4] != ""and l[4] != " ":
                                    try:
                                        if isinstance(float(l[4]), float) or isinstance(int(l[4]), int):
                                            if comen_qty == 0:
                                                comen_qty = float(l[4])
                                            # TODO: FOR 2ps and more than one ps what to do
                                            qty += float(l[4])  
                                        '''
                                        ischar = any(char.isalpha() for char in l[4])
                                        if not ischar and (isinstance(float(l[4]), float) or isinstance(int(l[4]), int)):
                                            if comen_qty == 0:
                                                comen_qty = float(l[4])
                                            # TODO: FOR 2ps and more than one ps what to do
                                            qty += float(l[4])
                                        '''
                                    except Exception:
                                        print(f"Error processing item {l}")
                                elif len(l) == 2:
                                    #main_name.append(l[0])
                                    qty = sub_list(l[1], qty)
                        return qty
                    qty = sub_list(qty_info_list, qty)
                    ttk.Label(f, text=f"Left: {str(qty)}", wraplength=70).grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
                                                
                elif(info[0] == 'DOCUMENT'):
                    #print("word: " + str(len(item)))
                    #print("Documents: " + str(item))
                    f = tk.Frame(self.lb, width=screen_width-(screen_width/3), bg="#0d47a1", highlightthickness=2, highlightbackground="black")
                    #f.grid(row=len(self.lb.winfo_children()), column=0, pady=1, sticky=tk.EW)
                    f.pack(fill='x', expand=True, pady=10, padx=10)
                    var = tk.BooleanVar()
                    var.set(len([item for selecteditem in self.selected_products if item['doc_barcode'] == selecteditem[0]]) > 0)
                    checkbox = ttk.Checkbutton(f, variable=var, command=lambda i=item['doc_barcode'], v=var, p=f: self.toggle_selected(i, v, p))
                    checkbox.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
                    ttk.Label(f, text=f"Document : " + item['doc_barcode'], wraplength=150).grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)
                    #tk.Button(f, text='Remove', command=lambda i=item['id'], v=None: self.Selectd_item_remove(i, v)).grid(row=1, column=4, padx=5, pady=5, sticky=tk.W)
                    
                elif(info[0] == 'ACTIONS'):
                    #print("word: " + str(len(item)))
                    #print("ACTIONS: " + str(item))
                    f = tk.Frame(self.lb, width=screen_width-(screen_width/3), bg="#0d47a1", highlightthickness=2, highlightbackground="black")
                    #f.grid(row=len(self.lb.winfo_children()), column=0, pady=1, sticky=tk.EW)
                    f.pack(fill='x', expand=True, pady=10, padx=10)
                    var = tk.BooleanVar()
                    var.set(len([item for selecteditem in self.selected_products if item[1] == selecteditem[0]]) > 0)
                    checkbox = ttk.Checkbutton(f, variable=var, command=lambda i=item[1], v=var, p=f: self.toggle_selected(i, v, p))
                    checkbox.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
                    ttk.Label(f, text=f"ACTIONS : " + item[1], wraplength=150).grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)
                    #tk.Button(f, text='Remove', command=lambda i=item['id'], v=None: self.Selectd_item_remove(i, v)).grid(row=1, column=4, padx=5, pady=5, sticky=tk.W)
                                
                        
    def comparison(self):
        query = self.var.get()
        if query:
            #print("word: " + str(query) + " search_type: " + str(self.search_type))
            self.all_items = []
            results = []
            items_results = []
            unique_item_results = []
            barcode_results = []
            unique_barcode_results = []
            
            Actions_results = []
            unique_Actions_results = []
            
            unique_results = set()  # To store unique results

            #self.midel_frame
            #print("self.homemaster.Shops_info['Shop_items'] > ", self.homemaster.Shops_info['Shop_items'])
            # cache lowercase query and expensive lookups/permissions so we don't call Chacke_Security/json.loads repeatedly
            q_lower = str(query).lower()

            if self.perm_actions:
                shop_actions_str = self.homemaster.Shops_info.get('Shop_Actions', '')
                if shop_actions_str:
                    try:
                        Shop_Actions = json.loads(shop_actions_str)
                    except Exception:
                        Shop_Actions = []
                    for Actions in Shop_Actions:
                        key = Actions[1]
                        if key not in unique_Actions_results:
                            Actions_results.append(["ACTIONS", key, Actions])
                            unique_Actions_results.append(key)

            if self.perm_items:
                # iterate shop items once, avoid repeated lower() and json loads
                for item_entry in self.homemaster.Shops_info.get('Shop_items', []):
                    selected_item = item_entry[0]
                    item_id = selected_item['id']
                    if item_id in unique_item_results:
                        continue

                    # prepare searchable strings once
                    more_info_str = str(selected_item.get('more_info', '')).lower()
                    name_str = str(selected_item.get('name', '')).lower()
                    code_str = str(selected_item.get('code', '')).lower()
                    type_str = str(selected_item.get('type', '')).lower()

                    if q_lower in more_info_str or q_lower in name_str or q_lower in code_str or q_lower in type_str:
                        items_results.append(["ITEM", item_id, selected_item])
                        unique_item_results.append(item_id)

            if self.perm_docs:
                # single DB query for documents
                rows = [] # fetch_as_dict_list("SELECT * FROM doc_table WHERE doc_barcode LIKE ?", (f"%{query}%",))
                for row in rows:
                    barcode = row['doc_barcode']
                    if barcode not in unique_barcode_results:
                        barcode_results.append(["DOCUMENT", barcode, row])
                        unique_barcode_results.append(barcode)

            results.extend(items_results)
            results.extend(Actions_results)
            results.extend(barcode_results)
            #print("items_results: " + str(len(items_results)) + " query: " + str(query))
            #print("barcode_results: " + str(len(barcode_results)) + " query: " + str(query))
            #print("results: " + str(len(results)) + " query: " + str(query))
            self.all_items = results
            return results
        else:
            return []
        
    def cancel_search(self):
        self.lb_up = False
        self.items = []
        self.all_items = []
        self.selected_products = []
        self.main_frame.destroy()
        
    def Done_search(self):
        if self.search_type == "":
            self.search_type = "id"
        p = self
        
        while(True):
            if hasattr(p, 'add_item'):
                break
            else:
                p = p.master
        
        for item_info in self.selected_products:
            if(item_info['type'] == 'ITEM'):
                qty = 0
                if hasattr(p, 'qty'):
                    qty = p.qty
                index = -1
                found = 0
                p.add_item(item_info)
                
                p.qty = 0
                p.update_info()
            elif(item_info['type'] == 'DOCUMENT'):
                p.get_ex_doc_items(item_info)
                p.get_ex_doc_payments(item_info)
                p.update_info()
                
            elif(item_info['type'] == 'ACTIONS'):
                p.add_item(item_info)
                p.update_info()
        self.var.set("")
        self.lb_up = False
        self.items = []
        self.all_items = []
        self.selected_products = []
        self.main_frame.destroy()
     
    def treeview_naigation(self, event):
        if not (event.keysym == "Up" or event.keysym == "Down"):
            self.focus_set()
            
        if len(self.lb.winfo_children()):
            if self.selected_indexd == -1:
                self.selected_indexd = 0;
            
            elif event.keysym == 'Up':
                self.lb.winfo_children()[self.selected_indexd].configure(bg="#0d47a1")
                self.selected_indexd -= 1;
            elif event.keysym == 'Down':
                self.lb.winfo_children()[self.selected_indexd].configure(bg="#0d47a1")
                self.selected_indexd += 1;
                
            if self.selected_indexd <= -1:
                self.selected_indexd = len(self.lb.winfo_children())-1;
            elif self.selected_indexd >= len(self.lb.winfo_children()):
                self.selected_indexd = 0;
            elif self.selected_indexd == len(self.lb.winfo_children())-1 and len(self.all_items) != len(self.lb.winfo_children()):
                self.load_more_items(self.all_items)
                
            self.lb.winfo_children()[self.selected_indexd].configure(bg="#1a1a2e")

        
                

    def select(self, _):
        if len(self.lb.winfo_children()):
            if self.selected_indexd == -1:
                self.selected_indexd = 0;
            index_id = 0
            while(index_id < len(self.lb.winfo_children()[self.selected_indexd].winfo_children())):
                chackbox = self.lb.winfo_children()[self.selected_indexd].winfo_children()[index_id]
                if isinstance(chackbox, ttk.Checkbutton): 
                    chackbox.invoke()
                    break
                index_id += 1
            






















    def update_search_results(self, selected_id, selected_item, selected_type):
        #self.list_items.delete(0, tk.END)
        result = None
        #print("selected_type : " + str(selected_type))
        if self.search_type == "":
            self.search_type = "id"
        if (selected_type == "ITEM"):
            result = fetch_as_dict_list("SELECT * FROM product WHERE "+ self.search_type+ "=?", (selected_id,))
            
            self.search_type = ""
            if result:
                self.var.set(str(result[0]) + "   " + str(result[2]) + "   " + str(result[1]))
                qty = 0
                if hasattr(self.homemaster, 'qty'):
                    qty = self.homemaster.qty
                #print("selected_type2 : " + str(selected_item))
                a = ItemSelectorWidget(self, result[2], result[12], result[16], qty)
                self.wait_window(a.getvalue_form)
                #print("ret : " + str(a.selected_items))
                #print("info : " + str(result))
                for t in a.selected_items:
                    p = self
                    while(True):
                        if hasattr(p, 'add_item'):
                            break
                        else:
                            p = p.master
                            
                    p.add_item(result, None, selected_type, t[4][0], t[0], t[1], t[2], t[3], t[5])
                #column_name = tree.column("#1", "heading")
                for a in self.homemaster.list_items.get_children():
                    self.homemaster.list_items.item(a)['values'][2] = "000"
                    #print("item : " + str(self.homemaster.list_items.item(a)))
                self.homemaster.qty = 0
                self.homemaster.update_info()
        if (selected_type == "DOCUMENT"):
            result = [] #self.fetch_as_dict_list("SELECT * FROM doc_table WHERE "+ self.search_type+ "=?", (selected_id,))
            
            self.search_type = ""
            if result:
                self.homemaster.get_ex_doc_items(result[1])
                self.homemaster.get_ex_doc_payments(result[1])
                self.homemaster.update_info()
        self.var.set("")
