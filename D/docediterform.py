import tkinter as tk
from tkinter import ttk
import sqlite3
import shutil
import datetime
import os
import atexit
import sys
import random
import json
import ast


current_dir = os.path.abspath(os.path.dirname(__file__))
MAIN_dir = os.path.join(current_dir, '..')
sys.path.append(MAIN_dir)

from D.searchbox import search_entry
from C.API.Get import *
from C.API.API import *
from C.API.Set import *

from D.ChooseCustemr import UserManagementApp
from D.iteminfo import *
from D.Security import *
from D.printer import PrinterForm
from ApprovedDisplay import ApproveFrame
from D.GetVALUE import GetvalueForm



data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data'))
db_path = os.path.join(data_dir, 'my_database.db')


class DocEditForm(tk.Frame):
    def __init__(self, master, Shops_info, user, Shops, Selected_doc):
        tk.Frame.__init__(self, master)
        
        self.bg_dark = "#0d47a1"      # Deep blue
        self.bg_light = "#1565c0"     # Darker blue
        self.accent_blue = "#1976d2"  # Medium blue
        self.text_light = "#ffffff"   # White text
        self.bg_darker = "#0a3d91"    # Even darker blue
        self.button_style = {"font": ("Arial", 11, "bold"), "bg": self.accent_blue, "fg": self.text_light, "activebackground": self.bg_light, "activeforeground": self.text_light, "relief": tk.FLAT, "bd": 0}
        
        
        #print("items:"+str(Selected_doc))
        #print("Shops:"+str(Shops))
        self.Selected_Shop = Shops[0]['Shop_name']
        
        self.Shops_info = Shops_info
        self.user = user
        self.Shops = Shops
        self.Selected_doc = Selected_doc
        self.id = id
        self.qty = 0
        self.disc = 0
        self.pid_peyment = []
        self.olditems = []
        self.barcode = self.Selected_doc['doc_barcode']
        self.user = user
        self.Shops_info = Shops_info
        self.Shops = Shops
        #self.User_Shops_List = User_Shops_List
        self.Selected_Shop = ""
        self.Selected_items = []
        self.items = []
        
       #print("Disktop user : " + str(self.user))
        self.custemr = "" # for holding user or costumer name
        self.app = None # for holding user or costumer name
        self.chart_index = 0
        self.price = 0
        self.pid = 0
        self.creadit = 0
        self.pid_peyment = []
        self.ex_pid_peyment = []
        self.Loded_payment_buttons = []
        self.ex_items = []
        self.ex_doc = []
        self.tax = 0
        self.qty = 0
        self.disc = 0
        self.total = 0

        self.At_Shop_id = -1
        self.on_Shop = -1  
        self.main_frame = None
        p = 0
        self.homemaster = self
        while(True):
            p += 1
            #print("chacking parent p = " + str(p))
            if hasattr(self.homemaster, 'onDisplayFrame'):
                break
            else:
                self.homemaster = self.homemaster.master
                
        # Child frame 1 - TOP_FORM
        top_form = tk.Frame(self, bg=self.bg_light)
        top_form.grid(row=0, column=0, columnspan=3, sticky="nsew")

        top_form.grid_columnconfigure(0, weight=5)
        top_form.grid_columnconfigure(1, weight=5)
        top_form.grid_columnconfigure(2, weight=5)
        top_form.grid_columnconfigure(3, weight=5)
        top_form.grid_columnconfigure(4, weight=5)
        top_form.grid_columnconfigure(5, weight=5)
        top_form.grid_columnconfigure(6, weight=5)
        top_form.grid_rowconfigure(0, weight=5)
        top_form.grid_rowconfigure(1, weight=5)
        top_form.grid_rowconfigure(2, weight=5)
        
        
        # Label "Customer" and Entry
        self.custemr = []
        self.Add_custemur_label = tk.Label(top_form, text=self.Selected_doc['customer_id'] if not self.Selected_doc['customer_id'] == '' and not self.Selected_doc['customer_id'] == None else "+ Custumer", font=("Arial", 10, "bold"),
                                           fg="#4dd0e1", bg=self.bg_light, cursor="hand2")
        self.Add_custemur_label.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        self.Add_custemur_label.bind("<Button-1>", lambda _: self.Add_Custumer())
        
        # Label "Customer" and Entry
        #Todo: set user imadeiat ly
        self.User = []
        self.Add_User_label = tk.Label(top_form, text=self.Selected_doc['user_id'] if not self.Selected_doc['user_id'] == '' and not self.Selected_doc['user_id'] == None else "+ User", font=("Arial", 10, "bold"),
                                           fg="#4dd0e1", bg=self.bg_light, cursor="hand2")
        self.Add_User_label.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
        self.Add_User_label.bind("<Button-1>", lambda _: self.Add_Custumer())
        
        self.Seller = []
        self.Add_Seller_label = tk.Label(top_form, text=self.Selected_doc['Seller_id'] if not self.Selected_doc['Seller_id'] == '' and not self.Selected_doc['Seller_id'] == None else "+ Seller", font=("Arial", 10, "bold"),
                                           fg="#4dd0e1", bg=self.bg_light, cursor="hand2")
        self.Add_Seller_label.grid(row=0, column=2, sticky="nsew", padx=5, pady=5)
        self.Add_Seller_label.bind("<Button-1>", lambda _: self.Add_Custumer())

        
        # Label "Number" and self.Entry
        label_User = tk.Label(top_form, text="AT Shop : " + self.Selected_doc['At_Shop_Id'], bg=self.bg_light, fg=self.text_light)
        label_User.grid(row=0, column=3)
        self.created_user = self.Selected_doc['At_Shop_Id']
        
        # Checkbox "Paid" type 'Sale_item'
        checkbox_paid = tk.Checkbutton(top_form, text="Paid", bg=self.bg_light, fg=self.text_light)
        checkbox_paid.grid(row=0, column=4)


        # Label "External Doc" and self.Entry
        label_external_doc = tk.Label(top_form, text="External Document", bg=self.bg_light, fg=self.text_light)
        label_external_doc.grid(row=1, column=0)
        self.entry_external_doc = tk.Entry(top_form)
        self.entry_external_doc.insert(0, self.Selected_doc['extension_barcode'])
        self.entry_external_doc.grid(row=1, column=1)
        
        # Label "Data" and self.Entry
        label_Pide = tk.Label(top_form, text="Risived :", bg=self.bg_light, fg=self.text_light)
        label_Pide.grid(row=1, column=2)
        self.entry_Pide = tk.Entry(top_form)
        self.entry_Pide.insert(0, self.Selected_doc['price'])
        self.entry_Pide.grid(row=1, column=3)



        label_due_date = tk.Label(top_form, text="Due Date", bg=self.bg_light, fg=self.text_light)
        label_due_date.grid(row=1, column=4)
        self.entry_due_date = tk.Entry(top_form)
        self.entry_due_date.insert(0, self.Selected_doc['doc_expire_date'])
        self.entry_due_date.grid(row=1, column=5)


        
        label_qty = tk.Label(top_form, text="Total QTY : " + str(self.Selected_doc['qty']), bg=self.bg_light, fg=self.text_light)
        label_qty.grid(row=2, column=0)

        label_User = tk.Label(top_form, text="Total Profit : " + str(self.Selected_doc['Profite']), bg=self.bg_light, fg=self.text_light)
        label_User.grid(row=2, column=1)
        label_User = tk.Label(top_form, text="Total Discount : " + str(self.Selected_doc['discount']), bg=self.bg_light, fg=self.text_light)
        label_User.grid(row=2, column=2)
        label_User = tk.Label(top_form, text="Total tax : " + str(self.Selected_doc['tax']), bg=self.bg_light, fg=self.text_light)
        label_User.grid(row=2, column=3)

        self.created_date = self.Selected_doc['doc_created_date']
        label_createdate = tk.Label(top_form, text="CREATED DATE : " + self.Selected_doc['doc_created_date'], bg=self.bg_light, fg=self.text_light)
        label_createdate.grid(row=2, column=4)
        label_updatedate = tk.Label(top_form, text="UPDATED DATE : " + self.Selected_doc['doc_updated_date'], bg=self.bg_light, fg=self.text_light)
        label_updatedate.grid(row=2, column=5)

        
        # Child frame 2 - SEARCH_FORM
        search_form = tk.Frame(self, bg=self.bg_light)
        search_form.grid(row=1, column=0, rowspan=4, sticky="nsew")

        # Child frame 3 - CENTER_FORM
        center_form = tk.Frame(self, bg=self.bg_light)
        center_form.grid(row=1, column=1, rowspan=3, columnspan=2, sticky="nsew")

        # Configure column and row weights
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=1)
        self.grid_rowconfigure(4, weight=1)

        # Notebook widget - CENTER_NOTEBOK
        center_notebook = ttk.Notebook(center_form)
        center_notebook.pack(fill="both", expand=True)

        # Tab 1 - Items
        items_tab = tk.Frame(center_notebook, bg=self.bg_light)
        center_notebook.add(items_tab, text="Items")
        items_tab.columnconfigure(0, weight=1)
        items_tab.columnconfigure(1, weight=0)
        items_tab.columnconfigure(2, weight=0)
        items_tab.columnconfigure(3, weight=0)
        items_tab.rowconfigure(0, weight=0)
        items_tab.rowconfigure(1, weight=1)
        items_tab.rowconfigure(2, weight=0)

        # Create a label and an self.entry widget for the search box
        self.search_entry = search_entry(items_tab, self.Shops_info, self.user, self.Shops, font=("Arial", 12))
        #tk.Entry
        self.search_entry.grid(row=0, column=0, columnspan=4, sticky="nsew")

        self.Frame_contaner_frame = tk.Frame(items_tab, bg=self.bg_dark)
        self.Frame_contaner_frame.grid(row=1, column=0, columnspan=4, sticky="nsew")
        
        self.List_Frame_contaner_frame = tk.Frame(self.Frame_contaner_frame, bg=self.bg_dark)
        self.List_Frame_contaner_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        #self.List_Frame = tk.Frame(self.List_Frame_contaner_frame, bg=self.bg_dark)
        #self.List_Frame.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        
        self.item_List_canvas = tk.Canvas(self.List_Frame_contaner_frame, bg=self.bg_dark, highlightthickness=0)
        self.item_List_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        
        self.item_List_yscrollbar = tk.Scrollbar(self.List_Frame_contaner_frame, orient='vertical', 
                                                 command=self.item_List_canvas.yview, bg=self.bg_light, activebackground=self.accent_blue)
        self.item_List_yscrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.item_List_xscrollbar = tk.Scrollbar(self.List_Frame_contaner_frame, orient='horizontal', 
                                                 command=self.item_List_canvas.xview, bg=self.bg_light, activebackground=self.accent_blue)
        self.item_List_xscrollbar.pack(side=tk.TOP, fill=tk.X)
        
        self.item_List_canvas.configure(xscrollcommand=self.item_List_xscrollbar.set, 
                                       yscrollcommand=self.item_List_yscrollbar.set)

        self.Selected_item_Display_frame = tk.Frame(self.item_List_canvas, bg=self.bg_dark)
        self.item_List_canvas.create_window((0, 0), window=self.Selected_item_Display_frame, anchor=tk.NW)
        self.Selected_item_Display_frame.bind('<Configure>', lambda e: self.item_List_canvas.configure(scrollregion=self.item_List_canvas.bbox("all")))
        
        items_tools = tk.Frame(items_tab, bg=self.bg_light)
        items_tools.grid(row=2, column=4)
        self.item_remove_btn = tk.Button(items_tools, text="Remove", command=self.remove_item, **self.button_style)
        self.item_remove_btn.grid(row=0, column=0)
        
        # Tab 2 - Payment
        payment_tab = tk.Frame(center_notebook, bg=self.bg_light)
        center_notebook.add(payment_tab, text="Payment")
        payment_tab.columnconfigure(0, weight=1)
        payment_tab.rowconfigure(0, weight=0)
        payment_tab.rowconfigure(1, weight=1)
        payment_tab.rowconfigure(2, weight=1)

        self.list_payment = ttk.Treeview(payment_tab, columns=("Peyment Type", "Paid", "Paid Date", "Updated Date", "User", "Paid", "Extantion Bracodes"))
        self.list_payment.grid(row=0, column=0, columnspan=4, sticky="nsew")       
        self.list_payment.bind('<<TreeviewSelect>>', self.on_pyement_select)
        self.list_payment.heading("#0", text="Peyment Type", anchor=tk.W)
        self.list_payment.column("#0", stretch=tk.NO, width=100)
        self.list_payment.heading("#1", text="Peyment Name", anchor=tk.W)
        self.list_payment.column("#1", stretch=tk.NO, width=100)
        self.list_payment.heading("#2", text="Paid", anchor=tk.W)
        self.list_payment.column("#2", stretch=tk.NO, width=100)
        self.list_payment.heading("#3", text="Paid Date", anchor=tk.W)
        self.list_payment.column("#3", stretch=tk.NO, width=100)
        self.list_payment.heading("#4", text="Updated Date", anchor=tk.W)
        self.list_payment.column("#4", stretch=tk.NO, width=100)
        self.list_payment.heading("#5", text="User", anchor=tk.W)
        self.list_payment.column("#5", stretch=tk.NO, width=100)
        self.list_payment.heading("#6", text="Paid", anchor=tk.W)
        self.list_payment.column("#6", stretch=tk.NO, width=100)
        self.list_payment.heading("#7", text="Extantion Bracodes", anchor=tk.W)
        self.list_payment.column("#7", stretch=tk.NO, width=100)
        
        payment_tools = tk.Frame(payment_tab, bg=self.bg_light)
        payment_tools.grid(row=1, column=0)
        
        payment_tools_label_type = tk.Label(payment_tools, text="Type", bg=self.bg_light)
        payment_tools_label_type.grid(row=0, column=0)

        # create the combo box
        self.pay_type_options = [Shop_Payment_Tool[0] for Shop_Payment_Tool in self.homemaster.Shop_Payment_Tools]
        #print("self.homemaster.Shop_Payment_Tools in doc edit ", self.homemaster.Shop_Payment_Tools)
        self.selected_pay_type = tk.StringVar()
        # set the list of options
        self.payment_tools_entry_type = ttk.Combobox(payment_tools, width=20, font=("Arial", 12), textvariable=self.selected_pay_type)
        self.payment_tools_entry_type.grid(row=0, column=1)
        
        self.payment_tools_entry_type['values'] = self.pay_type_options
        
        payment_tools_label_amount = tk.Label(payment_tools, text="Amount")
        payment_tools_label_amount.grid(row=0, column=2)
        self.payment_tools_entry_amount = tk.Entry(payment_tools)
        self.payment_tools_entry_amount.insert(0, "0")
        self.payment_tools_entry_amount.grid(row=0, column=3)
        
        payment_tools_label_date = tk.Label(payment_tools, text="Data", bg=self.bg_light)
        payment_tools_label_date.grid(row=0, column=4)
        self.payment_tools_entry_date = tk.Entry(payment_tools)
        self.payment_tools_entry_date.insert(0, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        self.payment_tools_entry_date.grid(row=0, column=5)
        
        self.pay_add_btn = tk.Button(payment_tools, text="Add", command=self.add_payment, **self.button_style)
        self.pay_add_btn.grid(row=0, column=6)

        self.pay_change_btn = tk.Button(payment_tools, text="Change", command=self.change_payment, **self.button_style)
        self.pay_change_btn.grid(row=0, column=7)

        self.pay_remove_btn = tk.Button(payment_tools, text="Remove", command=self.remove_payment, **self.button_style)
        self.pay_remove_btn.grid(row=0, column=8)
        


        
        
        # Child frame 4 - INFO_FORM
        info_form = tk.Frame(self, bg=self.bg_light)
        info_form.grid(row=4, column=1, columnspan=3, sticky="nsew")

        button = tk.Button(info_form, text="Done", command=self.done, **self.button_style)
        button.grid(row=2, column=4)

        self.chackeqyu = Chacke_Security(self, self.user, self.Shops[self.on_Shop], 14, f'User Not allowed to Change QTY')
        self.chackeprice = Chacke_Security(self, self.user, self.Shops[self.on_Shop], 15, f'User Not allowed to Change Price')
        self.chakedisc = Chacke_Security(self, self.user, self.Shops[self.on_Shop], 16, f'User Not allowed to Give Discount')
        self.chacketype = Chacke_Security(self, self.user, self.Shops[self.on_Shop], 17, f'User Not allowed to Change ITEM TYPE')
        self.chaketotaldic = Chacke_Security(self, self.user, self.Shops[self.on_Shop], 18, f'User Not allowed to Change TOTALE Price OR Give TOTAL DISCOUNT')
        
        self.load_items()
        self.load_payment()
        #self.done()

    def on_pyement_select(self, *arg):
        # double-click
        selected_payment_list = self.list_payment.focus()  # Get the payment that was clicked
        if selected_payment_list:
            #self.payment_tools_entry_date.insert(0, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            #self.payment_tools_entry_amount.insert(0, str(self.total-self.pid))
            self.payment_tools_entry_date.delete(0, 'end')
            self.payment_tools_entry_amount.delete(0, 'end')
            self.selected_pay_type.set("")
            selected_payment_list_text = self.list_payment.item(selected_payment_list, "text")
            selected_payment_list_value = self.list_payment.item(selected_payment_list, "value")
            #print("Double-clicked selected_payment_list_value:", selected_payment_list_value)
            for payment_index, payment_tools in enumerate(self.homemaster.Shop_Payment_Tools):
                if payment_tools[1] == selected_payment_list_value[0]:
                    self.selected_pay_type.set(selected_payment_list_value[0])

            if selected_payment_list_value[3] == "":
                self.payment_tools_entry_date.insert(0, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            else:
                self.payment_tools_entry_date.insert(0, selected_payment_list_value[3])
            self.payment_tools_entry_amount.insert(0, selected_payment_list_value[1])

    def Add_Custumer(self):
        shop_obj = self.homemaster.Shops[self.homemaster.on_Shop] 
        if Chacke_Security(self, self.user, shop_obj, 21, f'User Not allowed to Search for Custumers'):
            self.app = UserManagementApp(self, "", self.user, self.Shops, self.homemaster.on_Shop)
            if self.app.user_details:
                #print("selected user == ", self.app.user_details)
                self.custemr = self.app.user_details['User_id']
                self.Add_custemur_label.config(text=self.app.user_details['User_name'])
            else:
                #print("user not selected")
                self.Add_custemur_label.config(text="+ Custumer")
                
    def chack_list(self):
        total_discount = 0
        total_tax = 0
        total_qty = 0
        all_total_price = 0

        for a, selected_item in enumerate(self.Selected_items):
            #print("in update item: " + str(selected_item[0]))
            #print("in update item: " + str(selected_item[0]))
            #print("in update item: " + str(selected_item[6]))
            #print("in update item:" + str(selected_item))
            
            qty = float(selected_item[7])
            price = float(selected_item[8])
            discount = float(selected_item[10])
            tax = float(selected_item[11])
            total_price = float(selected_item[12])
            
            # Calculate the expected total price based on quantity, price, discount, and tax
            expected_total_price = qty * price - discount # - tax
            
            # Update the total price in the item if it doesn't match the expected value
            if total_price != expected_total_price:
                    self.Selected_items[a][11] = expected_total_price
            
            # Update the price variable
            total_qty += qty
            total_discount += discount
            total_tax += tax
            all_total_price += expected_total_price
        
        return total_qty, total_discount, total_tax, all_total_price
            
    def update_info(self):
        self.tax = 0
        self.disc = 0
        total_qty, total_discount, total_tax, all_total_price = self.chack_list()
        '''self.total = (all_total_price - self.tax) - self.disc
        self.total_items_label.config(text="Total Items : " + str(total_qty))
        self.total_tax_label.config(text="Total Tax : " + str(self.tax))
        self.total_discount_label.config(text="Item Discount : " + str(total_discount))
        self.total_tdiscount_label.config(text="Total Discount : " + str(self.disc))
        self.total_price_label.config(text="Price Befor : " + str(all_total_price))
        self.total_label.config(text="Price After: " + str((all_total_price - self.tax) - self.disc))'''
        
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
                elif self.Shops_Names[0] in sv:
                    inputs[0].set(self.Shops_Names[0])
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
        # QTY
        if self.chackeqyu:
            self.Selected_items[index][7] = data[4].get()
        
        # price
        if self.chackeprice and self.chakedisc:
           self.Selected_items[index][10] = new_item_Price_Spinbox.get()
        else:
            new_item_Price_Spinbox.set(self.Selected_items[index][10])
        
        if self.chacketype:
            # shop
            self.Selected_items[index][12] = data[0].get()
            #code
            self.Selected_items[index][2] = data[1].get()
            # color
            self.Selected_items[index][5] = data[2].get()
            # size
            self.Selected_items[index][6] = data[3].get()
        
        if self.chaketotaldic:
            new_item_TPrice_Spinbox.set(str(float(data[4].get())*float(new_item_Price_Spinbox.get())))

        disc = ""
        if float(selected_item_info['values']['price'])-float(new_item_Price_Spinbox.get()) > 0:
            disc = " DISCOUNT " + str(float(selected_item_info['values']['price'])-float(new_item_Price_Spinbox.get()))
        data[6].config(text="Price " + str(selected_item_info['values']['price']) + disc)

        self.update_info()
    
    def remove_ex_items(self, ex_bar_frame, search_label):
        for i, selected_item in enumerate(self.Selected_items):
            #print("selected_item[14] ", selected_item[14])
            #print("search_label.cget(text) ", search_label.cget("text"))
            if selected_item[14] == search_label.cget("text"):
                #print("removed ")
                
                self.Selected_items.remove(selected_item)
        
        ex_bar_frame.grid_forget()
        self.Update_Selected_item() # it keep loading old
                
    def Update_Selected_item(self):
        for items in self.Selected_item_Display_frame.winfo_children():
            items.destroy()
        '''ex_doc_ = []
        for it in self.extrnal_frame.winfo_children():
            it.grid_forget()
        '''
        #self.midel_frame
        for i, selected_item in enumerate(self.Selected_items):
            #print("selected_item ", selected_item)
            ''' if not selected_item[14] in ex_doc_:
                ex_doc_.append(selected_item[14])
                ch = len(self.extrnal_frame.winfo_children())

                ex_bar_frame = tk.Frame(self.extrnal_frame, bg=self.accent_blue)
                ex_bar_frame.grid(row=0, column=ch, sticky="nsew", padx=2, pady=2)
                search_label = tk.Label(ex_bar_frame, text=selected_item[14], bg=self.accent_blue, fg=self.text_light, font=("Arial", 10, "bold"))
                search_label.grid(row=0, column=0, sticky="nsew", padx=5, pady=3)
                    
                update_button = tk.Button(ex_bar_frame, text="✕", command=lambda: self.remove_ex_items(ex_bar_frame, search_label), **self.button_style)
                update_button.grid(row=0, column=1, sticky="nsew", padx=2, pady=3)
            '''   
            selected_item_info = selected_item[0]
            #print("selected_item_info |", selected_item_info)
            #print("selected_item ", selected_item)
            
            #if isinstance(selected_item_info, str):
            #    selected_item_info = ast.literal_eval(selected_item_info)
            item = [""]

            #print("droing item list\n")
            new_item_fram = tk.Frame(self.Selected_item_Display_frame, highlightthickness=2, highlightbackground=self.accent_blue, bg=self.bg_darker)
            new_item_fram.pack(side="top", fill="x", expand=True)
            #new_item_fram.grid(row=len(self.Selected_item_Display_frame.winfo_children()), column=3, columnspan=5, pady=1)
            #


            # TODO ADD IMAGE 

            new_item_name = tk.Label(new_item_fram, text=str(selected_item[4]), font=("Arial", 12, "bold"), bg=self.bg_darker, fg=self.text_light)
            new_item_name.grid(row=0, column=1, columnspan=6, sticky="nsew")

            new_barcode_Label = tk.Label(new_item_fram, text=str("barcode"), font=("Arial", 8), bg=self.bg_darker, fg=self.text_light)
            new_barcode_Label.grid(row=1, column=1, columnspan=3, sticky="nsew")
            
            #new_type_Label = tk.Label(new_item_fram, text=str(selected_item[15]), font=("Arial", 8), bg=self.bg_darker, fg=self.text_light)
            #new_type_Label.grid(row=1, column=3, columnspan=3, sticky="nsew")
            
            new_item_QTY_fram = tk.Frame(new_item_fram, bg=self.bg_darker)
            new_item_QTY_fram.grid(row=2, column=1, rowspan=2, sticky="nsew")
            
            new_item_QTY_Label = tk.Label(new_item_QTY_fram, text="QTY Max is " + str(selected_item[8]), font=("Arial", 8), bg=self.bg_darker, fg=self.text_light)
            new_item_QTY_Label.grid(row=1, column=1, sticky="nsew")
            new_item_QTY_Spinbox = ttk.Spinbox(new_item_QTY_fram, from_=0, to=100, width=10)
            new_item_QTY_Spinbox.grid(row=2, column=1, sticky="nsew")
            new_item_QTY_Spinbox.set(str(selected_item[7]))
            price_ = ""
            price_ = str(selected_item_info['values']['price'])
            disc = ""
            if float(selected_item_info['values']['price'])-float(selected_item[10]) > 0:
                disc = " DISCOUNT " + str(float(selected_item_info['values']['price'])-float(selected_item[10]))
            new_item_Price_Label = tk.Label(new_item_fram, text="Price " + price_ + disc, font=("Arial", 8), bg=self.bg_darker, fg=self.text_light)
            new_item_Price_Label.grid(row=2, column=2, sticky="nsew")
            new_item_Price_Spinbox = ttk.Spinbox(new_item_fram, from_=0, to=100, width=10)
            new_item_Price_Spinbox.grid(row=3, column=2, sticky="nsew")
            new_item_Price_Spinbox.set(str(selected_item[10]))

            new_item_Shop_Label = tk.Label(new_item_fram, text="Shop :" , font=("Arial", 8), bg=self.bg_darker, fg=self.text_light)
            new_item_Shop_Label.grid(row=2, column=3, sticky="nsew")
            new_item_Shop_Combobox = ttk.Combobox(new_item_fram, values=[], width=10)
            new_item_Shop_Combobox.grid(row=3, column=3, padx=5, pady=5, sticky=tk.W)
            new_item_Shop_Combobox.set(str(selected_item[13]))
            new_item_Code_Label = tk.Label(new_item_fram, text="Code :" , font=("Arial", 8), bg=self.bg_darker, fg=self.text_light)
            new_item_Code_Label.grid(row=2, column=4, sticky="nsew")
            new_item_Code_Combobox = ttk.Combobox(new_item_fram, values=[], width=10)
            new_item_Code_Combobox.grid(row=3, column=4, padx=5, pady=5, sticky=tk.W)
            new_item_Code_Combobox.set(str(selected_item[2]))
            new_item_Color_Label = tk.Label(new_item_fram, text="Color " , font=("Arial", 8), bg=self.bg_darker, fg=self.text_light)
            new_item_Color_Label.grid(row=2, column=5, sticky="nsew")
            new_item_Color_Combobox = ttk.Combobox(new_item_fram, values=[], width=10)
            new_item_Color_Combobox.grid(row=3, column=5, padx=5, pady=5, sticky=tk.W)
            new_item_Color_Combobox.set(str(selected_item[5]))
            new_item_Size_Label = tk.Label(new_item_fram, text="Size " , font=("Arial", 8), bg=self.bg_darker, fg=self.text_light)
            new_item_Size_Label.grid(row=2, column=6, sticky="nsew")
            new_item_Size_Combobox = ttk.Combobox(new_item_fram, values=[], width=10)
            new_item_Size_Combobox.grid(row=3, column=6, padx=5, pady=5, sticky=tk.W)
            new_item_Size_Combobox.set(str(selected_item[6]))
            
            #new_exbarcode_Label = tk.Label(new_item_fram, text=str(selected_item[14]), font=("Arial", 8), bg=self.bg_darker, fg=self.text_light)
            #new_exbarcode_Label.grid(row=1, column=7, sticky="nsew")
            
            del_button = tk.Button(new_item_fram, text="✕", command= lambda index=i, frame=new_item_fram: self.remove_item(index, frame), **self.button_style)
            del_button.grid(row=0, column=7, sticky="nsew", padx=2, pady=2)
            # self.master.bind("<Delete>", lambda _: self.remove_item())
            
            new_item_TPrice_Label = tk.Label(new_item_fram, text="Total Price" , font=("Arial", 10, "bold"), bg=self.bg_darker, fg=self.accent_blue)
            new_item_TPrice_Label.grid(row=2, column=7, sticky="nsew")
            new_item_TPrice_Spinbox = ttk.Spinbox(new_item_fram, from_=0, to=100, width=10)
            new_item_TPrice_Spinbox.grid(row=3, column=7, sticky="nsew")
            new_item_TPrice_Spinbox.set(str(float(selected_item[7])*float(selected_item[10])))
            
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
                            value = [str(item['id']), item['code'], item['barcode'], 'Unknown Item', color, size, 1, qtylaft, items['price']-self.disc, item['include_tax'], items['price'], shopname, ""]
                            #                                                                                                            value[7] Qty left
                            self.Selected_items.append([item_info, str(value[0]), value[1], value[2], value[3], value[4], value[5], value[6], value[7], "", value[8], value[9], value[10], value[11], value[12], ""])        
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
                                value = [str(items['id']), items['code'], items['barcode'], items['name'], color, size, qty, items['price'], items['price']-self.disc, items['include_tax'], items['price'], shopname, ""]
                                self.Selected_items.append([item_info, str(value[0]), value[1], value[2], value[3], value[4], value[5], value[6], value[7], "", value[8], value[9], value[10], value[11], value[12], ""])           
                        else:
                            qty = float(qty)-float(path[4])
                            if data[7] != []:
                                for t, typ in enumerate(data[7]):                            
                                    QTY = int(typ[1])
                                    PRICE = int(typ[2])
                                    value = [str(items['id']), code, barcode, items['name'], color, size, float(QTY), PRICE, self.disc, items['include_tax'], float(QTY)*float(PRICE), shop_name, ""]
                                    self.Selected_items.append([item_info, str(value[0]), value[1], value[2], value[3], value[4], value[5], value[6], value[7], data[5], PRICE, value[9], value[10], value[11], value[12], typ[0]])
                            else:
                                value = [str(items['id']), code, barcode, items['name'], color, size, float(path[4]), items['price'], self.disc, items['include_tax'], float(qty)*float(items['price']), shop_name, '']
                                self.Selected_items.append([item_info, str(value[0]), value[1], value[2], value[3], value[4], value[5], value[6], value[7], data[5], item_info['values']['price'], value[9], value[10], value[11], value[12], ""])                        
                            
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
                                    value = [str(item['id']), item['code'], item['barcode'], 'Unknown Item', color, size, path[4], items['price'], items['price']-self.disc, item['include_tax'], items['price'], shopname, ""]
                                    self.Selected_items.append([item_info, str(value[0]), value[1], value[2], value[3], value[4], value[5], value[6], value[7], "", value[8], value[9], value[10], value[11], value[12], ""])        
                                    break
                                else:
                                    if data[7] != []:
                                        for t, typ in enumerate(data[7]):                            
                                            QTY = int(typ[1])
                                            PRICE = int(typ[2])
                                            value = [str(items['id']), code, barcode, items['name'], color, size, float(QTY), PRICE, self.disc, items['include_tax'], float(QTY)*float(PRICE), shop_name, ""]
                                            self.Selected_items.append([item_info, str(value[0]), value[1], value[2], value[3], value[4], value[5], value[6], value[7], data[5], PRICE, value[9], value[10], value[11], value[12], typ[0]])
                                    else:
                                        value = [str(items['id']), code, barcode, items['name'], color, size, float(path[4]), items['price'], self.disc, items['include_tax'], float(qty)*float(items['price']), shop_name, '']
                                        self.Selected_items.append([item_info, str(value[0]), value[1], value[2], value[3], value[4], value[5], value[6], value[7], data[5], item_info['values']['price'], value[9], value[10], value[11], value[12], ""])                        
                                    break

                self.disc = 0
        if(item_info['type'] == 'ACTIONS'):
           #print("item_info['values'] " + str(item_info['values']))
           #print("item_info['values'][6] " + str(item_info['values'][6]))
           #print("item_info['values'][6][1] " + str(item_info['values'][6][1]))
            for action in item_info['values'][6][1]:
                self.Selected_items.append(action)
                
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
                    self.Selected_items.append([doc_item_info, str(item[0]), item[1], item[2], item[3], item[5], item[6], item[7], item[8], qtyleft, item[8], item[10], 0, item[4], item_info['values']['doc_barcode'], typ]) 
                else:
                    pass
        
        self.Update_Selected_item()
        
    def add_payment(self, items, doc, selected_type, barcode):
        if not barcode in self.ex_pid_peyment:
            self.ex_pid_peyment.append(barcode)
        if (selected_type == "DOCUMENT"):
            #print("add_payment self.pid_peyment = " + str(self.pid_peyment))
            for item in items:
                if len(item) == 6:   
                    item.append(1)
                if len(item) == 7:
                    item.append(barcode)
                if len(item) >= 7:
                    item[7] = barcode
                #print("doc barcode = "+ str(barcode))
                #print("doc payment = "+ str(item))
                #print("doc payment[0] = "+ str(item[0]))
                # this is for old vistion that use the first index ad number not for type
                # in new version we need the payment type so we useing index 0
                payment_tool_type = item[0]
                if item[0].isdigit():
                    # if it is old v we will get it by searching
                    for spt, row in enumerate(self.homemaster.Shop_Payment_Tools):
                        if row[0] == item[1]:
                            payment_tool_type = row[1]
                item[0] = payment_tool_type
                if payment_tool_type == "CREADIT":
                    self.creadit += float(item[2])
                self.pid_peyment.append(item)
           

    def get_ex_doc_items(self, item_info):
        self.add_item(item_info)
        self.qty = 0

    def get_ex_doc_payments(self, item_info):
        #print("items===========%%%%%%% = " + str(item_info))
        b = json.loads(item_info['values']['payments'])
        #print("items===========%%%%%%% = " + str(b))
        self.add_payment(b, item_info['values'], "DOCUMENT", item_info['values']['doc_barcode'])
        self.qty = 0
        
    def remove_item(self):
        # Function to remove selected items from the list
        for a in self.list_items.selection():
            self.list_items.delete(a)
    
    def load_items(self):
        #print("tiems : " + str(self.Selected_doc['item']))
        items = json.loads(self.Selected_doc['item'])
        for item in items:
            it = fetch_as_dict_list(self.homemaster.Link, "SELECT * FROM product WHERE id=?", (str(item[0]),))
            if it:
                it = it[0]
                doc_item_info = {'values': it, 'type': 'DOCUMENT', 'item_list':[]}
                value = [str(it['id']), it['code'], it['barcode'], it['name'], item[5], item[6], item[7], it['price'], float( it['price'])-float(item[9]), it['include_tax'], it['price'], item[4], ""]
                self.Selected_items.append([doc_item_info, str(value[0]), value[1], value[2], value[3], value[4], value[5], value[6], value[7], "", value[8], value[9], value[10], value[11], value[12], self.Selected_doc['doc_barcode']])           
                self.Update_Selected_item()

    def Clear_payment(self):
        # Function to remove selected items from the list
        for d in self.list_payment.selection():
            self.list_payment.delete(d)
            
    def update_payment(self):
        self.Clear_payment()
        for p, item in enumerate(self.pid_peyment):
            pay_id = item[0]
            pay_type = item[1]
            pay_pid = item[2]
            pay_pid_date = item[3]
            pay_updated_date = item[4]
            pay_user = item[5]
            ispay_user = item[6]
            pay_barcode = item[7]
            self.list_payment.insert("", 'end', text=pay_id, values=(pay_type, pay_pid, pay_pid_date, pay_updated_date, pay_user, ispay_user, pay_barcode))

    def load_payment(self):
        payments = json.loads(self.Selected_doc['payments'])
        self.pid_peyment = []
        for p, item in enumerate(payments):
            pay_id = item[0]
            pay_type = item[1]
            pay_pid = item[2]
            pay_pid_date = item[3]
            pay_updated_date = item[4]
            pay_user = item[5]
                
            price = item[1]
            #print("list : " + str([name, price]))
                
            if len(item) == 7:
                item.append(self.Selected_doc['doc_barcode'])
            if len(item) >= 7 and (item[7] == None or item[7] == ''):
                item[7] = self.Selected_doc['doc_barcode']
            #print("doc barcode = "+ str(item[7]))
            #print("doc payment = "+ str(item))
            #print("doc payment[0] = "+ str(item[0]))
            # this is for old vistion that use the first index ad number not for type
            # in new version we need the payment type so we useing index 0
            payment_tool_type = item[0]
            if item[0].isdigit():
                # if it is old v we will get it by searching
                for spt, row in enumerate(self.homemaster.Shop_Payment_Tools):
                    if row[0] == item[1]:
                        payment_tool_type = row[1]
            item[0] = payment_tool_type
            if payment_tool_type == "CREADIT":
                self.creadit += float(item[2])
            self.pid_peyment.append(item)
        self.update_payment()
        
    def get_selected_payment(self):
        if len(self.list_payment.selection()):
            selected = self.list_payment.selection()[0]
            selected_payment_list_text = self.list_payment.item(selected, "text")
            selected_payment_list_value = self.list_payment.item(selected, "value")
        
            for index, item in enumerate(self.pid_peyment):
                pay_type = item[0]
                pay_name = item[1]
                pay_pid = item[2]
                pay_pid_date = item[3]
                pay_updated_date = item[4]
                pay_user = item[5]
                #print("selected_payment_index Found ", item)
                #print("selected_payment_list_text Found ", selected_payment_list_text)
                #print("selected_payment_list_value Found ", selected_payment_list_value)
                if pay_type == selected_payment_list_text and pay_name == selected_payment_list_value[0]\
                   and pay_pid == selected_payment_list_value[1]and pay_pid_date == selected_payment_list_value[2]:
                    return index
        return -1
            
    def add_payment(self):
        # Function to remove selected items from the list
        #TODO get the bigest id and set +1 for new pyment
        date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.pid_peyment.append(self.selected_pay_type.get(), self.selected_pay_type.get(), self.payment_tools_entry_amount.get(), self.payment_tools_entry_date.get(),  date, self.homemaster.user['User_name'])
        self.update_payment()
        

    def change_payment(self):
        date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        selected_payment_index = self.get_selected_payment()
        if selected_payment_index > -1 and selected_payment_index < len(self.pid_peyment) and self.pid_peyment[selected_payment_index]:
            #print("self.pid_peyment[selected_payment_index] change_payment ", self.pid_peyment[selected_payment_index])
            self.pid_peyment[selected_payment_index][0] = self.selected_pay_type.get()
            self.pid_peyment[selected_payment_index][1] = self.selected_pay_type.get()
            self.pid_peyment[selected_payment_index][2] = self.payment_tools_entry_amount.get()
            self.pid_peyment[selected_payment_index][4] = self.payment_tools_entry_date.get()
            self.pid_peyment[selected_payment_index][5] = self.homemaster.user['User_name']
            #print("self.pid_peyment[selected_payment_index] change_payment Done ", self.pid_peyment[selected_payment_index])
            self.update_payment()
        
    def remove_payment(self):
        selected_payment_index = self.get_selected_payment()
        if selected_payment_index > -1 and selected_payment_index < len(self.pid_peyment) and self.pid_peyment[selected_payment_index]:
            #print("self.pid_peyment[selected_payment_index] remove_payment ", self.pid_peyment[selected_payment_index])
            self.pid_peyment.remove(selected_payment_index)
            self.update_payment()
            
    
    def done(self):
        todaydate = str(datetime.datetime.now().strftime('%Y')) + "-"+str(datetime.datetime.now().strftime('%m')) + "-"+str(datetime.datetime.now().strftime('%d'))
        #givendate = self.date_year_Spinbox.get() + "-"+self.date_month_Spinbox.get() + "-"+self.date_day_Spinbox.get()

        self.process_payment(todaydate, self.user, self.custemr, self.Shops, self.on_Shop, self.Shops_info, self.Selected_items, self.pid_peyment)
        
        tabmaster = self
        while(True):
            if hasattr(tabmaster, 'perform_search'):
                break
            else:
                tabmaster = tabmaster.master
        tabmaster.perform_search()
        self.master.master.destroy()

    # about payment
    def process_payment(self, givendate, user, custemr, shop, shop_on, Shops_info, Selected_items, pid_peyment):
        if Chacke_Security(self, user, shop[shop_on], 22, f'User Not allowed to Sell'):
           #print("user "+str(user))
            answer = tk.messagebox.askquestion("Question", "do you whant to continue?")
            if answer != 'yes':
                return
            # GET COPY OF ALL GIVEN INFO
            list_items_copy = []
            if Selected_items and len(Selected_items) > 0 and isinstance(Selected_items[0][0], list):
                for Selected_item in Selected_items:
                    list_items_copy.extend(Selected_item[0])
            else:
                list_items_copy = Selected_items
                
            
            pid_peyment_copy = pid_peyment
            #print("Shops_info = ", shop[shop_on])
            Shop_brand_name = shop[shop_on]['Shop_brand_name']
            today_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
            date = givendate + " " + datetime.datetime.now().strftime('%H:%M')

            payments_extra = []
            extra_payment_needs = []
            
            Seller_id = None
            payment_item_required = 0
            payment_open_drower = 0
            payment_print_slip = 1
            payment_customer_required = 0
            payment_enable = 0
            payment_change_allowed = 0
            payment_mark_pad = 0
            
            item_tobechanged = []
            
            
            brcod = ""

            # doc_code = "1"
            # Year:Month-docType 1 doccreateplatform 1 doc_numb
            #TODO make it create randim number so that ont to count
            # create a mostly-unique doc barcode using timestamp (avoids needing extra imports)
            doc_code = datetime.datetime.now().strftime('%y:%m') + "-11"
            # use current microseconds as suffix to reduce collisions
            suffix = datetime.datetime.now().strftime('%f')
            while True:
                candidate = doc_code + suffix
                # use existing cursor 'cur'
                ex_doc = fetch_as_dict_list(self.homemaster.Link, "SELECT * FROM doc_table WHERE doc_barcode=?", (candidate,))
                if ex_doc:
                    ex_doc = ex_doc[0]
                    # fallback: increment numeric suffix until unique
                    try:
                        suffix = str(int(suffix) + 1)
                    except Exception:
                        suffix = '1'
                else:
                    brcod = candidate
                    break
            # ex_item = [each item [barcode, isitem, ispay, ex_item, ex_item_items, payments, ex_payment_count, ex_item_pric, ex_item_T_disc, ex_item_T_tax, ex_pid]
            ex_docs_info = []

            
            payments_ = []
            pay_index = 0
            itemforslip = ""
            item = "" # item found
            new_items = [] # item found
            count_new_items = 0 # itme counted
            price = 0 # new items price
            pid = 0   # for new items pid
            T_pid = 0 # for all pid 
            def_pid = 0# for cash with no item pid or credit
            T_disc = 0  # for total new items dics
            tax = 0  # tax
            T_tax = 0  # tax 
            change = 0
            
            doc_found = []
            #print("brcod :" + str(brcod))
            #print("count sold items :" + str(len(list_items_copy.get_children())))
            #print("sold list_items_copy :" + str(list_items_copy))

            # here we will collect all the item that are given new or prevuse added by document
            # then wil will set item to be changed in leter
            for iv in list_items_copy:
                #print("iv :" + str(iv))
                #print("self.ex_items :" + str(self.ex_items))
                #print("iv[11] :" + str(iv[11]))
                #print("len(iv) :" + str(len(iv)))
                # search for document that is created by or if it is new doc empty holder if it is created befor
                # if not created before create one
                found_index = next((i for i, d in enumerate(doc_found) if d["Barcode"] == iv[14]), -1)
                
                if found_index: # if found index is 0 it is the first time so we will create selected item info
                    selected_item_info = {
                            "Barcode" : iv[14],
                            'payments_' : [],
                            'pay_index' : 0,
                            'itemforslip' : "",
                            'item' : "",
                            'new_items' : [],
                            'count_new_items' : 0,
                            'price' : 0,
                            'Cost' : 0,
                            'Profite' : 0,
                            'pid' : 0,
                            'T_pid' : 0,
                            'def_pid' : 0,
                            'Creadit' : 0,
                            'disc' : 0,
                            'Tdisc' : 0,
                            'T_disc' : 0,
                            'tax' : 0,
                            'T_tax' : 0,
                            'change' : ""
                    }
                    doc_found.append(selected_item_info)
                    found_index = len(doc_found) -1 

                #print("found_index :" + str(found_index))
                #print(str(iv[1]))
                #print("item id " + str(iv[0]['values']['id']) + " to item")
                if iv[0]['values']['id'] == -1: # may be it means this is existing documnet item we are not sure if the item exist at this time
                    # TODO : add type here
                    disc = float(iv[0]['values']['price'])-float(iv[10])
                    itl = [iv[1], iv[2], iv[3], iv[4], iv[13], iv[5], iv[6], iv[7], iv[10], disc, iv[11], (iv[0]['values']['cost'])]
                        
                    doc_found[found_index]['count_new_items'] += float(iv[7])
                    doc_found[found_index]['price'] += float(iv[7])*float(iv[10])
                    doc_found[found_index]['Cost'] = (iv[0]['values']['cost'])
                    doc_found[found_index]['Profite'] += (float(iv[10]) - (iv[0]['values']['cost']))*float(iv[7])
                    doc_found[found_index]['Tdisc'] += disc
                    doc_found[found_index]['tax'] += float(iv[10])
                    doc_found[found_index]['new_items'].append(itl)
                    
                    #print("adding " + str(iv) + " to item")
                    #print("adding " + str(iv) + " to item")
                else:
                    it = fetch_as_dict_list(self.homemaster.Link, "SELECT * FROM product WHERE id=?", (iv[0]['values']['id'],))
                    #print("item it " + str(it) + " to item")
                    if it:
                        it = it[0]
                        # TODO : add type here
                        disc = float(iv[0]['values']['price'])-float(iv[10])
                        itl = [iv[1], iv[2], iv[3], iv[4], iv[13], iv[5], iv[6], iv[7], iv[10], disc, iv[11], (iv[0]['values']['cost'])]
                            
                        doc_found[found_index]['count_new_items'] += float(iv[7])
                        doc_found[found_index]['price'] += float(iv[7])*float(iv[10])
                        doc_found[found_index]['Cost'] = (iv[0]['values']['cost'])
                        doc_found[found_index]['Profite'] += (float(iv[10]) - (iv[0]['values']['cost']))*float(iv[7])
                        doc_found[found_index]['Tdisc'] += disc
                        doc_found[found_index]['tax'] += float(iv[10])
                        doc_found[found_index]['new_items'].append(itl)
                        
                        #print("adding " + str(it) + " to item")
                        #print("adding " + str(iv) + " to item")

                        # here we will collect items to be reduses
                        # we cant reduse here b/c if we incounter error we will make mistake on stocks
                        setted = 0
                        for i, itbc in enumerate(item_tobechanged):
                            if itbc[0] == iv[1]:
                                item_tobechanged[i][7] = str(float(item_tobechanged[i][7])+float(iv[7]))
                                setted = 1
                        if setted == 0:
                            item_tobechanged.append([iv[1], it['more_info'], 0, str(iv[13]), str(iv[2]), str(iv[5]),str(iv[6]), str(iv[7])])            
                    else:
                        # message there is proplame on item change_item
                        erroritemsearchanswer = tk.messagebox.askquestion("Question", "There is proplame finding On one of Item Do you whant to continue?")
                        if erroritemsearchanswer != 'yes':
                            return

            # here we will get document item to be added agene to make it balanced
            #
            for i, d in enumerate(doc_found):
                #print("--Barcode = " + str(d['Barcode']))
                if d['Barcode'] != '':
                    fdoc = fetch_as_dict_list(self.homemaster.Link, "SELECT * FROM doc_table WHERE doc_barcode=?", (d['Barcode'],))
                    #print("fdoc " + str(fdoc) + " to item")
                    if fdoc:
                        fdoc = fdoc[0]
                        items = json.loads(fdoc['item'])
                        for item in items:
                            #print('item ', item)
                            it = fetch_as_dict_list(self.homemaster.Link, "SELECT * FROM product WHERE id=?", (item[0],))
                            itemqty = item[7]
                            if it:
                                it = it[0]
                                for olditem in d['new_items']:
                                    if olditem[0] == item[0]:
                                        if olditem[7] < item[7]:
                                            itemqty -= olditem[7]
                                            if itemqty <= 0:
                                                break;
                                                
                                #print('itemqty ', itemqty)
                                if float(itemqty) > 0:
                                    #same here we will not add it here we have to hold to the end to avoide error
                                    item_tobechanged.append([item[0], it['more_info'], 1, str(item[4]), str(item[1]), str(item[5]),str(item[6]), str(itemqty)])
                                    #print("--removeing all old qty = " + str([item[1], it['more_info'], 0, str(item[4]), str(item[1]), str(item[5]),str(item[6]), str(item[7])]))

            '''
            # for developer and tester
            for di, doc_f in enumerate(doc_found):
                #print("chacking doc_f di = " + str(di) + " barcode= "+str(doc_f['Barcode']))
                for new_items_indoc in doc_f['new_items']:
                    #print("\t item collect :" + str(new_items_indoc))
                #print("\n\n")


            for item_toch in item_tobechanged:
                #print("checed item_tobechanged :" + str(item_toch))
                
            #print("\n\n done chaking document found\n\n")
            while True:
                continue
            #'''



            # here we will set its paymant for its owne document and get extra payments
            while len(pid_peyment_copy) > 0: #as Long As The payemn stell existes
                #print("pid_peyment_copy:" + str(pid_peyment_copy))
                found_index = next((i for i, d in enumerate(doc_found) if d["Barcode"] == pid_peyment_copy[0][7]), -1)
                if found_index:
                    selected_item_info = {
                            "Barcode" : pid_peyment_copy[0][7],
                            'payments_' : [],
                            'itemforslip' : "",
                            'item' : "",
                            'new_items' : [],
                            'count_new_items' : 0,
                            'price' : 0,
                            'pid' : 0,
                            'T_pid' : 0,
                            'def_pid' : 0,
                            'Creadit' : 0,
                            'disc' : 0,
                            'Tdisc' : 0,
                            'T_disc' : 0,
                            'tax' : 0,
                            'T_tax' : 0,
                            'Profite' : 0,
                            'change' : ""
                    }
                    
                    doc_found.append(selected_item_info)
                    found_index = len(doc_found) -1 
                #print("pid_peyment_copy[0]:" + str(pid_peyment_copy[0]))

                
                berd = brcod if pid_peyment_copy[0][7] == '' else pid_peyment_copy[0][7]

                HOME = self
                if hasattr(HOME, 'homemaster'):
                    HOME = self.homemaster
                for rows in HOME.Shop_Payment_Tools:
                    if rows[0] == pid_peyment_copy[0][1]: # get the right payment type to get its ruls
                        #print("rows:" + str(rows))
                        #print("price-disc "+str(doc_found[found_index]['price']-doc_found[found_index]['Tdisc']) + ": pid " + str(doc_found[found_index]['pid']) + ":def_pid " + str(def_pid))
                        # "Tool Name", "Tool Method", "Tool ID", "Tool Short cut", "Tool Acsess key", "Tool enabel", "Tool Quick_pay","Tool Markpad", "Tool Customer_required", "Tool Open_drower", "Tool#printslip"
                        # setting rules for payment 
                        if int(rows[5]) == 1: # chack if enabled
                            payment_enable += 1
                        if int(rows[7]) == 1 and payment_mark_pad == 0: # chack if enabled
                            payment_mark_pad = 1
                        if int(rows[8]) == 1 and payment_customer_required == 0: # chack if enabled
                            payment_customer_required = 1
                        if int(rows[9]) == 1 and payment_open_drower == 0: # chack if enabled
                            payment_open_drower = 1
                        if int(rows[10]) == 1 and payment_print_slip == 0: # chack if enabled
                            payment_print_slip = 1
                        '''if rows[11] == 1 and payment_change_allowed == 0: # chack if enabled
                            payment_change_allowed = 1
                        if rows[11] == 1 and payment_item_required == 0: # chack if enabled
                            payment_item_required = 1'''



                        c = float(pid_peyment_copy[0][2]) # holde the payment of that document
                        #print("c:" + str(c))
                            
                        if not rows[6]:
                            doc_found[found_index]['price'] += c
                            doc_found[found_index]['def_pid'] += c

                        # if the payment type is Creadit the we will ballance it later if needed
                        if rows[1] == 'CREADIT':
                            payments_extra.append([str(rows[1]), str(pid_peyment_copy[0][1]), str(pid_peyment_copy[0][2]), str(pid_peyment_copy[0][3] if pid_peyment_copy[0][3] != "" else date), str(pid_peyment_copy[0][4]), user['User_name'], str(rows[4]), berd])
                        # if needed price is got or equal to paid resived amount we will hold extar payment for balancing 
                        elif doc_found[found_index]['price']-doc_found[found_index]['Tdisc'] <= 0 or doc_found[found_index]['price']-doc_found[found_index]['Tdisc'] == doc_found[found_index]['pid']:
                            creadit_barcode = berd
                            if len(doc_found) > 1:
                                for i, crd in enumerate(doc_found):
                                    if not crd["Barcode"] == '':
                                        creadit_barcode = crd["Barcode"]
                                        break
                                    
                            # if there is no price needed or on item is give it is cash in or diposite 
                            if doc_found[found_index]['price']-doc_found[found_index]['Tdisc'] == 0:
                                doc_found[found_index]['payments_'].append([str(rows[1]), str(pid_peyment_copy[0][1]), str(pid_peyment_copy[0][2]), str(pid_peyment_copy[0][3] if pid_peyment_copy[0][3] != "" else date), str(pid_peyment_copy[0][4]), user['User_name'], str(rows[4]), creadit_barcode])
                                doc_found[found_index]['T_pid'] += float(pid_peyment_copy[0][2])  # add the pid to total total pid for recived even ifthere is change
                                doc_found[found_index]['pid'] += c  # add the pid to total pid
                                
                            if len(doc_found) > 1:
                                balanced = 0
                                for j, doc_f0 in enumerate(doc_found):
                                    if doc_f0['price']-doc_f0['Tdisc'] > 0 or doc_f0['price']-doc_f0['Tdisc'] < doc_f0['pid']:
                                        doc_found[j]['payments_'].append([str(rows[1]), str(pid_peyment_copy[0][1]), str(pid_peyment_copy[0][2]), str(pid_peyment_copy[0][3] if pid_peyment_copy[0][3] != "" else date), str(pid_peyment_copy[0][4]), user['User_name'], str(rows[4]), creadit_barcode])
                                        doc_found[j]['T_pid'] += float(pid_peyment_copy[0][2])  # add the pid to total total pid for recived even ifthere is change
                                        doc_found[j]['pid'] += c  # add the pid to total pid
                                        balanced = 1
                                        break
                                if not balanced:
                                    # this is for extar collecting to be balanced
                                    payments_extra.append([str(rows[1]), str(pid_peyment_copy[0][1]), str(pid_peyment_copy[0][2]), str(pid_peyment_copy[0][3] if pid_peyment_copy[0][3] != "" else date), str(pid_peyment_copy[0][4]), user['User_name'], str(rows[4]), berd])
                        else:
                            # if payemnt is not finded we will calculate give and sette it
                            pr = (doc_found[found_index]['price']-doc_found[found_index]['disc']) # item price

                            pl = pr-doc_found[found_index]['pid']     # price left to pay
                            if c > pl:
                                e = c - pl # we will get the remaing amount from extar pide side
                                # we will set the remaning extra to balance it later
                                payments_extra.append([str(rows[1]), str(pid_peyment_copy[0][1]), str(e), str(pid_peyment_copy[0][3] if pid_peyment_copy[0][3] != "" else date), str(pid_peyment_copy[0][4]), user['User_name'], str(rows[4]), berd])
                                # pid_peyment_copy[0][1]
                                #doc_found[found_index]['payments_'].append([str(rows[1]), str("test 1"), str(c), date, date, user['User_name'], str(rows[4]), str(pid_peyment_copy[0][3]), rows[1]])
                                c = pl # taking only what pied

                            # the price needed will be setted here
                            if rows[6]:
                                #print("pid+c ")
                                doc_found[found_index]['T_pid'] += float(pid_peyment_copy[0][2])  # add the pid to total total pid for recived even ifthere is change
                                doc_found[found_index]['pid'] += c  # add the pid to total pid

                            doc_found[found_index]['payments_'].append([str(rows[1]), str(pid_peyment_copy[0][1]), str(c), str(pid_peyment_copy[0][3] if pid_peyment_copy[0][3] != "" else date), str(pid_peyment_copy[0][4]), user['User_name'], str(rows[4]), berd])
                        break # after we find the right peyment we will live
                pid_peyment_copy.remove(pid_peyment_copy[0]) # lets remove opayment so that we dont read it agane
                
                #print("\n\n payments_ pid collect :" + str(doc_found[found_index]['payments_'])+"\n\n")
                #print("\n\n payments_extra pid collect :" + str(payments_extra)+"\n\n")
                
            #print("\n\n payments collect than doc_found :" + str(doc_found)+"\n\n")
            '''
            # for developer and tester
            for di, doc_f in enumerate(doc_found):
                #print("chacking payment di = " + str(di) + " barcode= "+str(doc_f['Barcode']))
                for new_items_indoc in doc_f['new_items']:
                    #print("\t item collect :" + str(new_items_indoc))
                #print("\n\n")
                
                for new_items_indoc in doc_f['payments_']:
                    #print("\t payments_ collect :" + str(new_items_indoc))
                #print("\n\n")

            for item_toch in item_tobechanged:
                #print("checed item_tobechanged :" + str(item_toch))

            #
            #print("\n\n done chaking document found\n\n")
            while True:
                continue
            #'''
            
            # balancing the payment collected
            for px, extra_payment in enumerate(payments_extra):
                #print("--extra_payment = " + str(extra_payment))
                c = float(extra_payment[2]) # holde one payment to distrbuc it to documnets
                while c > 0: # as long as we have payment that we hold on we will loopin

                    # we are going to distarbc holded payment to all document
                    for i, d in enumerate(doc_found):
                        if c == 0:
                            break
                        #print("--Barcode = " + str(d['Barcode']))
                        #print("--payments_ : " + str(d['payments_']))

                        if d['price']-d['Tdisc'] != d['pid']:
                            #print("--item = " + str(d['new_items']))
                            pr = (d['price']-d['disc']) # item price

                            # this will chacke if the payment is greter than needed price
                            # if so it will get only needed price and the remanin will live it to be balanced later
                            
                            pl = pr-d['pid']     # price left to pay
                            if c > pl:
                                e = c - pl # we will get the remaing amount from extar pide side
                                payments_extra[px][2] = str(e) # we will update the remaning extra to balance it later
                                c = pl # taking only what pied
                                    
                            # the price needed will be setted here
                            doc_found[i]['pid'] += c # add the pid to total pid
                            doc_found[i]['payments_'].append([str(extra_payment[0]), str(extra_payment[1]), str(c), extra_payment[3], date, extra_payment[5], extra_payment[6], extra_payment[7]])
                            for si, sd in enumerate(doc_found):
                                if sd == extra_payment[7]:
                                    doc_found[si]['payments_'].append([str(''), str('Balanced'), str(c), extra_payment[3], date, extra_payment[5], extra_payment[6], d['Barcode']])
                                    break
                            c = 0
                        #print("--c : " + str(c))
                    if c > 0:
                        #print("--payments_ : " + str(d['payments_']))
                        if extra_payment[7] == "":
                            doc_found[0]['payments_'].append([str(extra_payment[0]), "Change", str(-c), extra_payment[3], date, extra_payment[5], extra_payment[6], extra_payment[7]])
                        else:
                            doc_found[0]['payments_'].append([str(extra_payment[0]), "", str(-c), extra_payment[3], date, extra_payment[5], extra_payment[6], extra_payment[7]])
                        c = 0

            
            '''
            # for developer and tester
            for di, doc_f in enumerate(doc_found):
                #print("chacking doc_f di = " + str(di) + " barcode= "+str(doc_f['Barcode']))
                for new_items_indoc in doc_f['new_items']:
                    #print("\t item collect :" + str(new_items_indoc))
                #print("\n\n")
                
                for new_items_indoc in doc_f['payments_']:
                    #print("\t payments_ collect :" + str(new_items_indoc))
                #print("\n\n")

            for item_toch in item_tobechanged:
                #print("checed item_tobechanged :" + str(item_toch))
                
            #print("\n\n done chaking document found\n\n")
            while True:
                continue
            #'''
            
            #print("user :" + str(user))
            if user['User_id']:
                user_id = 'User_id'
                user_idv = user['User_id']
            else:
                user_id = 'Id'
                user_idv = user['Id']
            f_user_s = fetch_as_dict_list(self.homemaster.Link, "SELECT * FROM setting WHERE "+user_id+"=?", (int(user_idv),))
            #print("f_user_s "+str(f_user_s))
            Seller_id = None
            
            if f_user_s and f_user_s[0] and f_user_s[0]['Get_seller']:
                    #print("opning worker dialog")
                    app = WorkerManagementApp(self, str(brcod), float(count_new_items))
                    if app.user_details:
                        #print("app.user_details['User_id'] "+str(app.user_details['User_id']))
                        Seller_id = app.user_details['User_id']
                    else:
                        return
            #print("--item_tobechanged : " + str(item_tobechanged))
            
            costumer_name = ""
            phone_num = ""
            cm_id = None
            old_cm_id = None
            slip_doc_code = []
            
            #print("--payment_customer_required : " + str(payment_customer_required))
            if payment_customer_required:
                #print("--custemr : " + str(custemr))
                #print("--self.app : " + str(self.app))
                if custemr == "" or not self.app:
                    self.Add_Custumer()
                cm_id = custemr
                costumer_name = self.app.user_details['User_name']
                phone_num = self.app.user_details['User_phone_num']
                #print(self.app.user_details)
                
                
            for i, d in enumerate(doc_found):
                #print("--item = " + str(d['item']))
                #print("--payments_ : " + str(d['payments_']))
                if d['payments_'] == [] and payments_extra != []:
                    d['payments_'] = payments_extra
                    payments_extra = []
                    
                if d['payments_'] != [] or float(d['count_new_items']) != 0:
                        if d["Barcode"] != "":
                                #print("d[Barcode] = " + str(d["Barcode"]))
                                # Get_Document(None, user, ['doc_barcode'], [d["Barcode"]])
                                rows = fetch_as_dict_list(self.homemaster.Link, "SELECT * FROM doc_table WHERE doc_barcode=?", (d["Barcode"],))
                                # fetch_as_dict_list(self.homemaster.Link, "SELECT * FROM doc_table WHERE doc_barcode=?", (d["Barcode"],)).fetchall()
                                if rows and rows[0]['customer_id']: # if doc found
                                    old_cm_id = rows[0]['customer_id']
                                    #print("cmd old id = " + str(rows[0]) + " new id " + str(cm_id))
                                if cm_id and old_cm_id != str(cm_id):
                                    #[each item [barcode, isitem, ispay, ex_item, ex_item_items, payments, ex_payment_count, ex_item_pric, ex_item_T_disc, ex_item_T_tax, ex_pid]
                                    Update_Documente(None, user, ['customer_id'], [costumer_name], ['doc_barcode'], [d["Barcode"]])

                                    # Update_table_database('UPDATE doc_table SET customer_id=? WHERE doc_barcode=?', (cm_id, d["Barcode"]))
                                    # Commit the changes to the database
                                    # conn.commit()
                                if Seller_id != None:
                                    #[each item [barcode, isitem, ispay, ex_item, ex_item_items, payments, ex_payment_count, ex_item_pric, ex_item_T_disc, ex_item_T_tax, ex_pid]
                                    Update_Documente(None, user, ['Seller_id'], [Seller_id], ['doc_barcode'], [d["Barcode"]])
                                    # Update_table_database('UPDATE doc_table SET Seller_id=? WHERE doc_barcode=?', (Seller_id, d["Barcode"]))
                                    # Commit the changes to the database
                                    # conn.commit()
                                    
                                if d['payments_']:
                                    #todo if needed add pid in doc e_doc_info[10]
                                    Update_Documente(None, user, ['pid', 'payments', 'doc_updated_date'], [str(d['pid']), json.dumps(d['payments_']), today_date], ['doc_barcode'], [d["Barcode"]])
                                    # Update_table_database('UPDATE doc_table SET pid=?, payments=?, doc_updated_date=? WHERE doc_barcode=?', (str(d['pid']), json.dumps(d['payments_']), today_date, d["Barcode"]))
                                    # Commit the changes to the database
                                    #conn.commit()

                                #[each item [barcode, isitem, ispay, ex_item, ex_item_items, payments, ex_payment_count, ex_item_pric, ex_item_T_disc, ex_item_T_tax, ex_pid]
                                Update_Documente(None, user, ['item', 'qty', 'price', 'Profite', 'discount', 'tax', 'doc_updated_date'], [json.dumps(d['new_items']), float(d['count_new_items']), d['price'], d['Profite'], d['Tdisc'], d['tax'], today_date], ['doc_barcode'], [d["Barcode"]])
                                # Update_table_database('UPDATE doc_table SET item=?, qty=?, price=?, Profite=?, discount=?, tax=?, doc_updated_date=? WHERE doc_barcode=?', (json.dumps(d['new_items']), float(d['count_new_items']), d['price'], d['Profite'], d['Tdisc'], d['tax'], today_date, d["Barcode"]))
                                # Commit the changes to the database
                                # conn.commit()
                                
                                slip_doc_code.append(d["Barcode"])
                        elif d["Barcode"] == "":
                                #print("custemer : " + str(costumer_name) + "isneded : " + str(payment_customer_required))
                                # TODO: chacke if At_Shop_Id is selected if not make user selecte one
                                Set_Document(None, ["doc_barcode", "extension_barcode", "At_Shop_Id", "user_id", "customer_id", "Seller_id", "type", "item", "qty", "price", "discount", "tax", "payments", "pid", "doc_created_date", "doc_expire_date", "doc_updated_date"], [str(brcod), "extension_barcode", Shop_brand_name, self.user['User_name'], costumer_name, Seller_id, "Sale_item", json.dumps(d['new_items']), float(d['count_new_items']), d['price'], d['Tdisc'], d['tax'], json.dumps(d['payments_']), d['T_pid'], date, date, today_date])
                                #Update_table_database('INSERT INTO upload_doc (doc_barcode, extension_barcode, At_Shop_Id, user_id, customer_id, Seller_id, type, item, qty, price, discount, tax, payments, pid, doc_created_date, doc_expire_date, doc_updated_date) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (str(brcod), "extension_barcode", Shop_brand_name, self.user['User_name'], costumer_name, Seller_id, "Sale_item", json.dumps(d['new_items']), float(d['count_new_items']), d['price'], d['Tdisc'], d['tax'], json.dumps(d['payments_']), d['T_pid'], date, date, today_date))
                                #Update_table_database('INSERT INTO doc_table (doc_barcode, extension_barcode, At_Shop_Id, user_id, customer_id, Seller_id, type, item, qty, price, Profite, discount, tax, payments, pid, doc_created_date, doc_expire_date, doc_updated_date) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (str(brcod), "extension_barcode", Shop_brand_name, self.user['User_name'], costumer_name, Seller_id, "Sale_item", json.dumps(d['new_items']), float(d['count_new_items']), d['price'], d['Profite'], d['Tdisc'], d['tax'], json.dumps(d['payments_']), d['T_pid'], date, date, today_date))
                                # Commit the changes to the database
                                slip_doc_code.append(brcod)
                                
            # Now it is Safe to make change Stock
            #print("item_tobechanged  : " + str(item_tobechanged))
            for change_item in item_tobechanged:
                #print("item : " + str(change_item[1]), change_item[2], str(change_item[3]), str(change_item[4]),str(change_item[5]), str(change_item[6]))
                
                # we will get the letest stock information to change it
                it2 = fetch_as_dict_list(self.homemaster.Link, 'SELECT * FROM product WHERE id=?', (str(change_item[0]),))
                qty_info_list = []
                # load information 
                if it2:
                    it2=it2[0]
                    qty_info_list = json.loads(it2['more_info'])
                    if qty_info_list:
                        # make the change 
                        #print("item info befor  : " + str(qty_info_list))
                        it_info = change_qty(qty_info_list, change_item[2], str(change_item[3]), str(change_item[4]), str(change_item[5]),str(change_item[6]), str(change_item[7]))

                        if not it_info:
                                # message there is proplame on item change_item
                                erroriteminfoanswer = tk.messagebox.askquestion("Question", "There is Proplame On one Item Do you whant to continue?")
                                if erroriteminfoanswer != 'yes':
                                        pass #return 
                        else:               
                            #print("item info befor  : " + str(it_info))
                            # update the change 
                            Update_Producte(None, user, ['more_info'], [json.dumps(it_info)], ['id'], [change_item[0]])

                            # update shop_items that are orady loaded 
                            it2 = fetch_as_dict_list(self.homemaster.Link, 'SELECT * FROM product WHERE id=?', (str(change_item[0]),))
                            if it2 and not len(it2) == 0:
                                for i3, it3 in enumerate(Shops_info['Shop_items']):
                                    if it3[0]['id'] == it2[0]['id']:
                                        Shops_info['Shop_items'][i3][0] = it2[0] # we are updateing all information of the procuct
                                        break
                        continue
                
                # message there is proplame on item change_item
                erroriteminfoanswer = tk.messagebox.askquestion("Question", "There is Proplame on Finding oneitem Item Do you whant to continue?")
                if erroriteminfoanswer != 'yes':
                    pass #return
                
            if payment_open_drower == 1:
               PrinterForm.open_drower(self, self.user)
            
             #TODO: MAKE IT SEND SELECTEd SHOP
            ApproveFrame(HOME, user, shop[0], slip_doc_code, payments_extra, payment_print_slip)
            return slip_doc_code
   
    def close_tab(self, test_tab):
        self.master.perform_search()
        test_tab.destroy()


    # about add item btn
    def Create_Unowen_item(self):
        if not Chacke_Security(self.homemaster, self.homemaster.user, self.homemaster.Shops[self.homemaster.on_Shop], 8, f'User Not allowed to Create Uknown Item'):
            return
        # get item info
        #id = GetvalueForm(self, '1', "Enter Item ID")
        #name = GetvalueForm(self, 'Item Name', "Enter Item Name")
        itempriceandcost = GetvalueForm(self, '0', ["Enter Item Price", "How much cost?"])
        
        if itempriceandcost == None or itempriceandcost.value == [] or len(itempriceandcost.value) <= 0:
            return
        
        uitemprice = itempriceandcost.value[0]
        if len(itempriceandcost.value) == 2:
            uitemcost = itempriceandcost.value[1]
        
        self.add_item({'type': "UnKNOWN", 'values': {'id': 0, 'name': "Unkown Item", 'price': uitemprice, 'cost': uitemcost}, 'extra_data': [], 'item_list': []})
        
