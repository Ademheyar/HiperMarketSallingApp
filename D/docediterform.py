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
#from M.Display import DisplayFrame

from D.searchbox import search_entry
from D.ChooseCustemr import UserManagementApp
from D.iteminfo import *
from D.Security import *
from D.printer import PrinterForm


from C.API.Get import *
data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data'))
db_path = os.path.join(data_dir, 'my_database.db')


class DocEditForm(tk.Frame):
    def __init__(self, master, Shops_info, user, Shops, items, docbarcode):
        tk.Frame.__init__(self, master)
        print("items:"+str(items))
        print("Shops:"+str(Shops))
        self.Selected_items = []
        self.Selected_Shop = Shops[0]['Shop_name']
        self.barcode = docbarcode
        
        self.items = items
        self.Shops_info = Shops_info
        self.user = user
        self.Shops = Shops
        self.id = id
        self.qty = 0
        self.disc = 0
        self.pid_peyment = []
        self.olditems = []
        
        # Child frame 1 - TOP_FORM
        top_form = tk.Frame(self)
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
        label_customer = tk.Label(top_form, text="Customer")
        label_customer.grid(row=0, column=0)
        self.selected_user = tk.StringVar()
        self.selected_user = items[3]
        cursor.execute("SELECT * FROM users")
        rows = cursor.fetchall()
        # create the combo box
        self.entry_customer = ttk.Combobox(top_form, width=20, font=("Arial", 12), textvariable=self.selected_user)
        self.entry_customer.grid(row=0, column=1)
        users_options = []
        for row in rows:
            users_options.append(row[1])
        # set the list of options
        self.entry_customer['values'] = users_options

        # Label "External Doc" and self.Entry
        label_external_doc = tk.Label(top_form, text="External Document")
        label_external_doc.grid(row=0, column=2)
        self.entry_external_doc = tk.Entry(top_form)
        self.entry_external_doc.insert(0, items[1])
        self.entry_external_doc.grid(row=0, column=3)


        # Label "Due Date" and self.Entry
        label_due_date = tk.Label(top_form, text="Due Date")
        label_due_date.grid(row=0, column=4)
        self.entry_due_date = tk.Entry(top_form)
        self.entry_due_date.insert(0, items[13])
        self.entry_due_date.grid(row=0, column=5)

        # Label "Data" and self.Entry
        label_data = tk.Label(top_form, text="Data")
        label_data.grid(row=1, column=0)
        self.entry_data = tk.Entry(top_form)
        self.entry_data.insert(0, items[2])
        self.entry_data.grid(row=1, column=1)

        # Checkbox "Paid"
        checkbox_paid = tk.Checkbutton(top_form, text="Paid")
        checkbox_paid.grid(row=1, column=2)
        
        
        # Label "Number" and self.Entry
        label_User = tk.Label(top_form, text="User : " + items[2])
        label_User.grid(row=1, column=3)
        self.created_user = items[2]

        label_type = tk.Label(top_form, text="Type : " + items[4])
        label_type.grid(row=1, column=4)

        label_User = tk.Label(top_form, text="User : " + items[2])
        label_User.grid(row=2, column=0)
        label_User = tk.Label(top_form, text="User : " + items[2])
        label_User.grid(row=2, column=1)
        label_User = tk.Label(top_form, text="User : " + items[2])
        label_User.grid(row=2, column=2)

        self.created_date = items[11]
        label_createdate = tk.Label(top_form, text="CREATED DATE : " + items[11])
        label_createdate.grid(row=2, column=3)
        label_updatedate = tk.Label(top_form, text="UPDATED DATE : " + items[13])
        label_updatedate.grid(row=2, column=4)

        
        # Child frame 2 - SEARCH_FORM
        search_form = tk.Frame(self)
        search_form.grid(row=1, column=0, rowspan=4, sticky="nsew")

        # Child frame 3 - CENTER_FORM
        center_form = tk.Frame(self)
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
        items_tab = tk.Frame(center_notebook)
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

        self.Frame_contaner_frame = tk.Frame(items_tab)
        self.Frame_contaner_frame.grid(row=1, column=0, columnspan=4, sticky="nsew")
        
        self.List_Frame_contaner_frame = tk.Frame(self.Frame_contaner_frame)
        self.List_Frame_contaner_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.List_Frame = tk.Frame(self.List_Frame_contaner_frame)
        self.List_Frame.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        
        self.item_List_canvas = tk.Canvas(self.List_Frame)
        self.item_List_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        
        self.item_List_yscrollbar = tk.Scrollbar(self.List_Frame, orient='vertical', command=self.item_List_canvas.yview)
        self.item_List_yscrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.item_List_xscrollbar = tk.Scrollbar(self.List_Frame_contaner_frame, orient='horizontal', command=self.item_List_canvas.xview)
        self.item_List_xscrollbar.pack(side=tk.TOP, fill=tk.X)
        
        self.item_List_canvas.configure(xscrollcommand=self.item_List_xscrollbar.set, yscrollcommand=self.item_List_yscrollbar.set)
        #self.New_item_contener_canvas.bind('<Configure>', lambda e: self.New_item_contener_canvas.configure(scrollregion=self.New_item_contener_canvas.bbox("all")))

        self.Selected_item_Display_frame = tk.Frame(self.item_List_canvas)
        self.item_List_canvas.create_window((0, 0), window=self.Selected_item_Display_frame, anchor=tk.NW)
        self.Selected_item_Display_frame.bind('<Configure>', lambda e: self.item_List_canvas.configure(scrollregion=self.item_List_canvas.bbox("all")))
        
        items_tools = tk.Frame(items_tab)
        items_tools.grid(row=2, column=4)
        self.item_remove_btn = tk.Button(items_tools, text="Remove", command=self.remove_item)
        self.item_remove_btn.grid(row=0, column=0)
        
        # Tab 2 - Payment
        payment_tab = tk.Frame(center_notebook)
        center_notebook.add(payment_tab, text="Payment")
        payment_tab.columnconfigure(0, weight=1)
        payment_tab.rowconfigure(0, weight=0)
        payment_tab.rowconfigure(1, weight=1)
        payment_tab.rowconfigure(2, weight=1)

        self.list_payment = ttk.Treeview(payment_tab, columns=("Peyment Type", "Paid", "Paid Date", "Updated Date", "User", "Paid", "Extantion Bracodes"))
        self.list_payment.grid(row=0, column=0, columnspan=4, sticky="nsew")
        self.list_payment.heading("#0", text="ID", anchor=tk.W)
        self.list_payment.column("#0", stretch=tk.NO, width=50)
        self.list_payment.heading("#1", text="Peyment Type", anchor=tk.W)
        self.list_payment.column("#1", stretch=tk.NO, width=250)
        self.list_payment.heading("#2", text="Paid", anchor=tk.W)
        self.list_payment.column("#2", stretch=tk.NO, width=50)
        self.list_payment.heading("#3", text="Paid Date", anchor=tk.W)
        self.list_payment.column("#3", stretch=tk.NO, width=50)
        self.list_payment.heading("#4", text="Updated Date", anchor=tk.W)
        self.list_payment.column("#4", stretch=tk.NO, width=250)
        self.list_payment.heading("#5", text="User", anchor=tk.W)
        self.list_payment.column("#5", stretch=tk.NO, width=250)
        self.list_payment.heading("#6", text="Paid", anchor=tk.W)
        self.list_payment.column("#6", stretch=tk.NO, width=250)
        self.list_payment.heading("#7", text="Extantion Bracodes", anchor=tk.W)
        self.list_payment.column("#7", stretch=tk.NO, width=250)
        
        payment_tools = tk.Frame(payment_tab)
        payment_tools.grid(row=1, column=0)
        
        payment_tools_label_type = tk.Label(payment_tools, text="Type")
        payment_tools_label_type.grid(row=0, column=0)
        self.selected_pay_type = tk.StringVar()
        cursor.execute("SELECT * FROM tools")
        rows = cursor.fetchall()
        # create the combo box
        self.payment_tools_entry_type = ttk.Combobox(payment_tools, width=20, font=("Arial", 12), textvariable=self.selected_pay_type)
        self.payment_tools_entry_type.grid(row=0, column=1)
        pay_type_options = []
        for row in rows:
            pay_type_options.append(row[1])
        # set the list of options
        self.payment_tools_entry_type['values'] = pay_type_options
        
        payment_tools_label_amount = tk.Label(payment_tools, text="Amount")
        payment_tools_label_amount.grid(row=0, column=2)
        self.payment_tools_entry_amount = tk.Entry(payment_tools)
        self.payment_tools_entry_amount.insert(0, "0")
        self.payment_tools_entry_amount.grid(row=0, column=3)
        
        payment_tools_label_date = tk.Label(payment_tools, text="Data")
        payment_tools_label_date.grid(row=0, column=4)
        self.payment_tools_entry_date = tk.Entry(payment_tools)
        self.payment_tools_entry_date.insert(0, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        self.payment_tools_entry_date.grid(row=0, column=5)
        
        self.pay_add_btn = tk.Button(payment_tools, text="Add", command=self.add_payment)
        self.pay_add_btn.grid(row=0, column=6)

        self.pay_change_btn = tk.Button(payment_tools, text="Change", command=self.change_payment)
        self.pay_change_btn.grid(row=0, column=7)

        self.pay_remove_btn = tk.Button(payment_tools, text="Remove", command=self.remove_payment)
        self.pay_remove_btn.grid(row=0, column=8)
        


        
        
        # Child frame 4 - INFO_FORM
        info_form = tk.Frame(self)
        info_form.grid(row=4, column=1, columnspan=3, sticky="nsew")

        button = tk.Button(info_form, text="Done", command=self.done)
        button.grid(row=2, column=4)

        self.load_items()
        self.load_payment()
        #self.done()

            

    def chack_list(self):
        total_discount = 0
        total_tax = 0
        total_qty = 0
        all_total_price = 0

        for a, selected_item in enumerate(self.Selected_items):
            print("in update item: " + str(selected_item[0]))
            print("in update item: " + str(selected_item[0]))
            print("in update item: " + str(selected_item[6]))
            print("in update item: " + str(selected_item[8]))
            
            qty = float(selected_item[7])
            price = float(selected_item[8])
            discount = float(selected_item[9])
            tax = float(selected_item[10])
            total_price = float(selected_item[11])
            
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
        # QTY
        self.Selected_items[index][7] = data[4].get()
        # price
        self.Selected_items[index][8] = new_item_Price_Spinbox.get()
        # shop
        self.Selected_items[index][12] = data[0].get()
        #code
        self.Selected_items[index][2] = data[1].get()
        # color
        self.Selected_items[index][5] = data[2].get()
        # size
        self.Selected_items[index][6] = data[3].get()
        new_item_TPrice_Spinbox.set(str(float(data[4].get())*float(new_item_Price_Spinbox.get())))
        self.update_info()

    def remove_ex_items(self, ex_bar_frame, search_label):
        for i, selected_item in enumerate(self.Selected_items):
            if selected_item[13] == search_label.cget("text"):
                self.Selected_items.remove(selected_item)
        self.Update_Selected_item()
        ex_bar_frame.grid_forget()
            
    def Update_Selected_item(self):
        for items in self.Selected_item_Display_frame.winfo_children():
            items.destroy()
        #self.midel_frame
        for i, selected_item in enumerate(self.Selected_items):
            print("selected_item ", selected_item)
            selected_item_info = selected_item[0]
            print("selected_item_info |", selected_item_info)
            print("selected_item ", selected_item)
            
            #if isinstance(selected_item_info, str):
            #    selected_item_info = ast.literal_eval(selected_item_info)
            item = [""]
            
            new_item_fram = tk.Frame(self.Selected_item_Display_frame, highlightthickness=2, highlightbackground="black")
            new_item_fram.grid(row=len(self.Selected_item_Display_frame.winfo_children()), column=0, pady=1, sticky=tk.EW)

            # TODO ADD IMAGE 

            new_item_name = tk.Label(new_item_fram, text=str(selected_item[4]), font=("Arial", 11))
            new_item_name.grid(row=0, column=1, columnspan=6, sticky="nsew")

            new_item_QTY_fram = tk.Frame(new_item_fram)
            new_item_QTY_fram.grid(row=2, column=1, rowspan=2, sticky="nsew")
            
            new_item_QTY_Label = tk.Label(new_item_QTY_fram, text="QTY Max is " + str(selected_item[7]), font=("Arial", 8))
            new_item_QTY_Label.grid(row=1, column=1, sticky="nsew")
            new_item_QTY_Spinbox = ttk.Spinbox(new_item_QTY_fram, from_=0, to=100, width=10)
            new_item_QTY_Spinbox.grid(row=2, column=1, sticky="nsew")
            new_item_QTY_Spinbox.set(str(selected_item[7]))
            price_ = ""
            price_ = str(selected_item_info['values']['price'])
            new_item_Price_Label = tk.Label(new_item_fram, text="Price " + price_, font=("Arial", 7))
            new_item_Price_Label.grid(row=2, column=2, sticky="nsew")
            new_item_Price_Spinbox = ttk.Spinbox(new_item_fram, from_=0, to=100, width=10)
            new_item_Price_Spinbox.grid(row=3, column=2, sticky="nsew")
            new_item_Price_Spinbox.set(str(selected_item[8]))

            new_item_Shop_Label = tk.Label(new_item_fram, text="Shop :" , font=("Arial", 7))
            new_item_Shop_Label.grid(row=2, column=3, sticky="nsew")
            new_item_Shop_Combobox = ttk.Combobox(new_item_fram, values=[], width=10)
            new_item_Shop_Combobox.grid(row=3, column=3, padx=5, pady=5, sticky=tk.W)
            new_item_Shop_Combobox.set(str(selected_item[12]))
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
            
            new_exbarcode_Label = tk.Label(new_item_fram, text=str(selected_item[13]), font=("Arial", 7))
            new_exbarcode_Label.grid(row=1, column=1, sticky="nsew")
            
            new_barcode_Label = tk.Label(new_item_fram, text=str(selected_item[3]), font=("Arial", 7))
            new_barcode_Label.grid(row=1, column=5, sticky="nsew")
            
            new_exbarcode_Label = tk.Label(new_item_fram, text=str(selected_item[3]), font=("Arial", 7))
            new_exbarcode_Label.grid(row=1, column=8, sticky="nsew")
            
            new_Extrmal = tk.Label(new_item_fram, text="", font=("Arial", 13))
            new_Extrmal.grid(row=0, column=8, sticky="nsew")
            
            del_button = tk.Button(new_item_fram, text="x", font=("Arial", 12), command= lambda index=i, frame=new_item_fram: self.remove_item(index, frame))
            del_button.grid(row=0, column=7, sticky="nsew")
            # self.master.bind("<Delete>", lambda _: self.remove_item())
            
            new_item_TPrice_Label = tk.Label(new_item_fram, text="Total Price is " , font=("Arial", 13))
            new_item_TPrice_Label.grid(row=1, column=7, sticky="nsew")
            new_item_TPrice_Spinbox = ttk.Spinbox(new_item_fram, from_=0, to=100, width=10)
            new_item_TPrice_Spinbox.grid(row=2, column=7, sticky="nsew")
            new_item_TPrice_Spinbox.set(str(float(selected_item[7])*float(selected_item[8])))
            
            data = [new_item_Shop_Combobox, new_item_Code_Combobox, new_item_Color_Combobox, new_item_Size_Combobox, new_item_QTY_Spinbox, new_barcode_Label]

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
                                                                                                                        
            
    def load_items(self):
        print("tiems : " + str(self.items[14]))
        items = json.loads(self.items[14])
        for item in items:
            it = fetch_as_dict_list("SELECT * FROM product WHERE id=?", 
                                    (str(item[0]),))[0]
            if it:
                    doc_item_info = {'values': it, 'type': 'DOCUMENT', 'item_list':[]}
                    self.Selected_items.append([doc_item_info, str(item[0]), item[1], item[2], item[3], item[5], item[6], item[7], item[8], item[9], item[10], 0, item[4], self.barcode])
                    self.Update_Selected_item()
        
    def add_item(self, item_info):
        print("item_info = " + str(item_info))
        if (item_info['type'] == "ITEM"):
            for data in item_info['extra_data']:
                #shop = self.Shops_Names
                #if self.Selected_Shop != "":
                #shop = [self.Selected_Shop]
                    
                items, doc, selected_type, barcode, shop_name, code, color, size, qty = \
                     item_info['values'], None, item_info['type'], data[5], data[0], data[1], data[2], data[3], data[4]
                value = [str(items['id']), code, barcode, items['name'], color, size, float(qty), items['price'], self.disc, items['include_tax'], float(qty)*float(items['price']), shop_name, ""]
                self.Selected_items.append([item_info, str(value[0]), value[1], value[2], value[3], value[4], value[5], value[6], value[7], value[8], value[9], value[10], value[11], value[12]])
                #self.list_items.insert("", "end", text=str(item_info[0]), values=(item_info[1], item_info[2], item_info[3], item_info[4], item_info[5], item_info[6], item_info[7], item_info[8], item_info[9], item_info[10], item_info[11], item_info[12]))
                self.disc = 0

        if (item_info['type'] == "DOCUMENT"):
            items = json.loads(item_info['values']['item'])
            for item in items:
                it = fetch_as_dict_list("SELECT * FROM product WHERE id=?", 
                                (item[0],))[0]
                if it:
                    doc_item_info = {'values': it, 'type': 'DOCUMENT', 'item_list':[]}
                    #print("items===========%%%%%%% = " + str(it))
                    #print("items===========%%%%%%% = " + str(item))
                    #print("items===========%%%%%%% = " + str(doc_item_info))
                    self.Selected_items.append([doc_item_info, str(item[0]), item[1], item[2], item[3], item[5], item[6], item[7], item[8], item[9], item[10], 0, item[4], item_info['values']['doc_barcode']])
                else:
                    pass
                
        self.Update_Selected_item()
        
        #self.list_items.insert("", "end", text=str(item[0]), values=(code, barcode, item[1], shop_name, color, size, float(qty), item[9], item[10],float(float(qty))*float(item[9]), 0, self.disc, 0, 0))
    
    def remove_item(self):
        # Function to remove selected items from the list
        for a in self.list_items.selection():
            self.list_items.delete(a)
    
    def load_payment(self):
        #print("tiems : " + str(self.items[10]))
        if ")" in self.items[10] or ")," in self.items[10]:
            items_lists = (self.items[10] + ",").split("),")
            index = 0
            for p in range(len(items_lists)-1):
                item = items_lists[p].split(",")
                print("item ;" + str(item))
                #for each items+
                pay_id = item[0].replace("(", "")
                pay_type = item[1]
                pay_pid = item[2]
                pay_pid_date = item[3].replace(",", "")
                pay_updated_date = item[4].replace(",", "")
                pay_user = item[5].replace(",", "")
                
                price = item[1]
                #print("list : " + str([name, price]))
                self.list_payment.insert("", 'end', text=pay_id, values=(pay_type, pay_pid, pay_pid_date, pay_updated_date, pay_user))
                index += 1
                
        elif "," in self.items[10]:
            items_lists = self.items[10].split(",")
            index = 0
            for p in range(len(items_lists)-1):
                item = items_lists[p].split(" = ")
                print("item :" + str(item))
                #for each items
                name = item[0].replace("(:", "")
                price = item[1]
                #print("list : " + str([name, price]))
                self.list_payment.insert("", 'end', text=index, values=(name, price, self.created_date, self.created_date, self.created_user))
                index += 1
        else:
            item = self.items[10].split(" = ")
            print("item :" + str(item))
            name = item[0].replace("(:", "")
            price = item[0]
            self.list_payment.insert("", 'end', text="0", values=(name, price, self.created_date, self.created_date, self.created_user))
        
            
    def add_payment(self):
        # Function to remove selected items from the list
        #TODO get the bigest id and set +1 for new pyment
        date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.list_payment.insert("", 'end', text="", values=(self.selected_pay_type.get(), self.payment_tools_entry_amount.get(), self.payment_tools_entry_date.get(),  date, self.master.master.master.master.master.master.master.user))

    def change_payment(self):
        # Function to remove selected items from the list
        self.list_payment.insert("", 'end', text=index, values=(name, price))
        
    def remove_payment(self):
        # Function to remove selected items from the list
        for a in self.list_payment.selection():
            self.list_payment.delete(a)

    
    def save_change(self):
        a = Chacke_Security(self, self.user, 0)
        if a:
            print("user "+str(self.user))
            answer = tk.messagebox.askquestion("Question", "do you whant to continue?")
            if answer != 'yes':
                return
            # GET COPY OF ALL GIVEN INFO
            list_items_copy = self.Selected_items

            date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

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
            doc_code = datetime.datetime.now().strftime('%y:%m') + "-11"
            b = 0
            while True:
                ex_doc = cursor.execute("SELECT * FROM doc_table WHERE doc_barcode=?", (doc_code+str(b),)).fetchone()
                if ex_doc:
                    b = random.randint(0, 10000)
                else:
                    brcod = doc_code+str(b)
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
            disc = 0  # for new items disc
            T_disc = 0  # for total new items dics
            tax = 0  # tax
            T_tax = 0  # tax 
            change = 0
            
            doc_found = []
            print("brcod :" + str(brcod))
            #print("count sold items :" + str(len(list_items_copy.get_children())))
            print("sold list_items_copy :" + str(list_items_copy))
            for iv in list_items_copy:
                print("iv :" + str(iv))
                print("len(iv) :" + str(len(iv)))
                if len(iv) >= 13:
                    found_index = next((i for i, d in enumerate(doc_found) if d["Barcode"] == iv[13]), -1)
                    if found_index:
                        selected_item_info = {
                            "Barcode" : iv[13],
                            'payments_' : [],
                            'pay_index' : 0,
                            'itemforslip' : "",
                            'item' : "",
                            'new_items' : [],
                            'count_new_items' : 0,
                            'price' : 0,
                            'pid' : 0,
                            'T_pid' : 0,
                            'def_pid' : 0,
                            'disc' : 0,
                            'T_disc' : 0,
                            'tax' : 0,
                            'T_tax' : 0,
                            'change' : ""
                        }
                        doc_found.append(selected_item_info)
                        found_index = len(doc_found) -1 

                    print("found_index :" + str(found_index))
                    doc_found[found_index]['count_new_items'] += 1
                    print(str(iv[1]))
                    print("item id " + str(iv[0]['values']['id']) + " to item")
                    it = fetch_as_dict_list("SELECT * FROM product WHERE id=?", (iv[0]['values']['id'],))
                    print("item it " + str(it) + " to item")
                    if it:
                        it = it[0]
                        itl = [iv[1], iv[2], iv[3], iv[4], iv[12], iv[5], iv[6], iv[7], iv[8], iv[9], iv[10]]
                
                        doc_found[found_index]['price'] += float(iv[7])*float(iv[8])
                        doc_found[found_index]['disc'] += float(iv[9])
                        doc_found[found_index]['tax'] += float(iv[10])
                        doc_found[found_index]['new_items'].append(itl)
                    
                        print("adding " + str(it) + " to item")
                        print("adding " + str(iv) + " to item")
                        print("adding " + str(iv[7]) + " to item_tobechanged")
                        item_tobechanged.append([iv[1], iv[0]['values']['more_info'], 0, str(iv[12]), str(iv[2]), str(iv[5]),str(iv[6]), str(iv[7])])            
                    else:
                        # message there is proplame on item change_item
                        erroritemsearchanswer = tk.messagebox.askquestion("Question", "There is proplame finding On one of Item Do you whant to continue?")
                        if erroritemsearchanswer != 'yes':
                                return
                                    
                    print("\n\n sold items collect :" + str(doc_found[found_index]['new_items'])+"\n\n")
                    print("\n\n items collect than doc_found :" + str(doc_found)+"\n\n")
            
            p = 0
            while p < len(self.pid_peyment):
                print("self.pid_peyment:" + str(self.pid_peyment))
                print("self.ex_pid_peyment:" + str(self.ex_pid_peyment))
                print("self.pid_peyment[p]:" + str(self.pid_peyment[p]))
                if len(self.pid_peyment[p]) > 7:  
                    print("\n\n items collect than self.pid_peyment[p][7] :" + str(self.pid_peyment[p][7])+"\n\n")
                    found_index = next((i for i, d in enumerate(doc_found) if d["Barcode"] == self.pid_peyment[p][7]), -1)
                    if found_index:
                        selected_item_info = {
                            "Barcode" : self.pid_peyment[p][7],
                            'payments_' : [],
                            'pay_index' : 0,
                            'itemforslip' : "",
                            'item' : "",
                            'new_items' : [],
                            'count_new_items' : 0,
                            'price' : 0,
                            'pid' : 0,
                            'T_pid' : 0,
                            'def_pid' : 0,
                            'disc' : 0,
                            'T_disc' : 0,
                            'tax' : 0,
                            'T_tax' : 0,
                            'change' : ""
                        }
                        doc_found.append(selected_item_info)
                        found_index = len(doc_found) -1 
                    doc_found[found_index]['pay_index'] += 1
                    print("self.pid_peyment[p]:" + str(self.pid_peyment[p]))
                    rows = 0
                    for r in self.Shop_Payment_Tools:
                        if r[0] == self.pid_peyment[p][1]:
                            rows = r
                            break
                    if rows:
                        print("rows:" + str(rows))
                        print("price-disc "+str(doc_found[found_index]['price']-doc_found[found_index]['disc']) + ":pid " + str(doc_found[found_index]['pid']) + ":def_pid " + str(def_pid))
                        c = float(self.pid_peyment[p][2])
                        print("c:" + str(c))
                        # "Tool Name", "Tool Method", "Tool ID", "Tool Short cut", "Tool Acsess key", "Tool enabel", "Tool Quick_pay","Tool Markpad", "Tool Customer_required", "Tool Open_drower", "Tool Printslip"
                        if rows[5] == '1': # chack if enabled
                            payment_enable += 1
                        if rows[7] == '1' and payment_mark_pad == 0: # chack if enabled
                            payment_mark_pad = 1
                        if rows[8] == '1' and payment_customer_required == 0: # chack if enabled
                            payment_customer_required = 1
                        if rows[9] == '1' and payment_open_drower == 0: # chack if enabled
                            payment_open_drower = 1
                        if rows[10] == '1' and payment_print_slip == 0: # chack if enabled
                            payment_print_slip = 1
                        '''if rows[11] == 1 and payment_change_allowed == 0: # chack if enabled
                            payment_change_allowed = 1
                        if rows[11] == 1 and payment_item_required == 0: # chack if enabled
                            payment_item_required = 1'''
                        if not rows[6]:
                            doc_found[found_index]['price'] += c
                            doc_found[found_index]['def_pid'] += c
                        
                        if doc_found[found_index]['price']-doc_found[found_index]['disc'] == doc_found[found_index]['pid']:
                            payments_extra.append([str(doc_found[found_index]['pay_index']), str(self.pid_peyment[p][1]), str(self.pid_peyment[p][2]), date, date, self.user['User_name'], str(rows[10]), str(self.pid_peyment[p][3])])
                        else:
                            if doc_found[found_index]['pid'] + c > doc_found[found_index]['price']-doc_found[found_index]['disc']:
                                pr = (doc_found[found_index]['price']-doc_found[found_index]['disc']) # item price
                                pl = pr-doc_found[found_index]['pid']     # price left to pay
                                if c > pl:
                                    e = c - pl
                                    payments_extra.append([str(doc_found[found_index]['pay_index']), str(self.pid_peyment[p][1]), str(e), date, date, self.user['User_name'], str(rows[10]), str(self.pid_peyment[p][3])])
                                    c = pl # taking only what pied
                                else:
                                    c = pl
                            if rows[6]:
                                print("pid+c ")
                                doc_found[found_index]['T_pid'] += float(self.pid_peyment[p][2])
                                doc_found[found_index]['pid'] += c
                            doc_found[found_index]['payments_'].append([str(doc_found[found_index]['pay_index']), str(self.pid_peyment[p][1]), str(c), date, date, self.user['User_name'], str(rows[11]), str(self.pid_peyment[p][3])])
                self.pid_peyment.remove(self.pid_peyment[p])
                print("\n\n payments_ pid collect :" + str(doc_found[found_index]['payments_'])+"\n\n")
                print("\n\n payments_extra pid collect :" + str(payments_extra)+"\n\n")
            
                
            f_user_s = cursor.execute("SELECT * FROM setting WHERE User_id=?", (int(self.user['User_id']),)).fetchall()
            print("f_user_s "+str(f_user_s))
            Seller_id = None

            for px, extra_payment in enumerate(payments_extra):
                print("--extra_payment = " + str(extra_payment))
                c = float(extra_payment[2])
                for i, d in enumerate(doc_found):
                    print("--item = " + str(d['item']))
                    print("--payments_ : " + str(d['payments_']))
                    if d['price']-d['disc'] != d['pid']:
                        if d['pid'] + c > d['price']-d['disc']:
                            pr = (d['price']-d['disc']) # item price
                            pl = pr-d['pid']     # price left to pay
                            if c > pl:
                                e = c - pl
                                # payments_extra.append([str(d['pay_index']), str(self.pid_peyment[p][1]), str(e), date, date, self.user['User_name'], str(rows[10]), str(self.pid_peyment[p][3])])
                                payments_extra[px][2] = str(e)
                                c = pl # taking only what pied
                            else:
                                c = pl
                        doc_found[i]['pay_index'] += 1
                        doc_found[i]['pid'] += c
                        doc_found[i]['payments_'].append([str(doc_found[i]['pay_index']), str(extra_payment[1]), str(c), extra_payment[3], date, extra_payment[5], extra_payment[6], extra_payment[7]])
                

            if f_user_s and f_user_s[0] and f_user_s[0][5]:
                print("opning worker dialog")
                app = WorkerManagementApp(self, str(brcod), float(count_new_items))
                if app.user_details:
                    print("app.user_details['User_id'] "+str(app.user_details['User_id']))
                    Seller_id = app.user_details['User_id']
                else:
                    return
                
            print("--item_tobechanged : " + str(item_tobechanged))
            
            name = ""
            phone_num = ""
            cm_id = None
            old_cm_id = None
                            
            slip_doc_code = []
            '''while True:
                continue'''
            print("item_tobechanged  : " + str(item_tobechanged))
            for change_item in item_tobechanged:
                print("item : " + str(change_item[1]), change_item[2], str(change_item[3]), str(change_item[4]),str(change_item[5]), str(change_item[6]))
                print("item info befor : " + str(change_item[1]))
                qty_info_list = []
                print("change_item[1]  : " + str(change_item[1]))
                if change_item[1]:
                    qty_info_list = json.loads(change_item[1])
                print("qty_info_list[1]  : " + str(qty_info_list))
                it_info = change_qty(qty_info_list, change_item[2], str(change_item[3]), str(change_item[4]), str(change_item[5]),str(change_item[6]), str(change_item[7]))

                if not it_info:
                        # message there is proplame on item change_item
                        erroriteminfoanswer = tk.messagebox.askquestion("Question", "There is Proplame On one Item Do you whant to continue?")
                        if erroriteminfoanswer != 'yes':
                                return
                                
                print("item info befor  : " + str(it_info))
                #while True:
                #    continue
                cursor.execute('UPDATE product SET more_info=? WHERE id=?', (json.dumps(it_info), change_item[0]))
                        
                cursor.execute("SELECT * FROM product WHERE id=?", (change_item[0],))
                it2 = cursor.fetchone()
                        
                print("item info updated : " + str(it2[12]))
                
                # Commit the changes to the database
                conn.commit()
                
            if payment_customer_required:
                if self.custemr == "" or not self.app:
                    self.Add_Custumer()
                cm_id = self.custemr
                name = self.app.user_details['User_name']
                phone_num = self.app.user_details['User_phone_num']
                print(self.app.user_details)

                
            for i, d in enumerate(doc_found):
                print("--d = " + str(d))
                print("--item = " + str(d['item']))
                print("--d['new_items'] = " + str(d['new_items']))
                print("--payments_ : " + str(d['payments_']))
                if d['payments_'] != [] or float(d['count_new_items']) != 0:
                        if d["Barcode"] != "":
                                rows = cursor.execute("SELECT * FROM doc_table WHERE doc_barcode=?", (d["Barcode"],)).fetchall()
                                if rows and rows[0][4]:
                                    old_cm_id = rows[0][4]
                                
                                print("cmd old id = " + str(rows[0]) + " new id " + str(cm_id))
                                if cm_id and old_cm_id != str(cm_id):
                                    #[each item [barcode, isitem, ispay, ex_item, ex_item_items, payments, ex_payment_count, ex_item_pric, ex_item_T_disc, ex_item_T_tax, ex_pid]
                                    cursor.execute('UPDATE doc_table SET customer_id=? WHERE doc_barcode=?', (cm_id, d["Barcode"]))
                                    # Commit the changes to the database
                                    conn.commit()
                                if Seller_id != None:
                                    #[each item [barcode, isitem, ispay, ex_item, ex_item_items, payments, ex_payment_count, ex_item_pric, ex_item_T_disc, ex_item_T_tax, ex_pid]
                                    cursor.execute('UPDATE doc_table SET Seller_id=? WHERE doc_barcode=?', (Seller_id, d["Barcode"]))
                                    # Commit the changes to the database
                                    conn.commit()
                                if float(d['count_new_items']):
                                    #[each item [barcode, isitem, ispay, ex_item, ex_item_items, payments, ex_payment_count, ex_item_pric, ex_item_T_disc, ex_item_T_tax, ex_pid]
                                    cursor.execute('UPDATE doc_table SET item=?, qty=?, price=?, discount=?, tax=?, doc_updated_date=? WHERE doc_barcode=?', (json.dumps(d['new_items']), float(d['count_new_items']), d['price'], d['disc'], d['tax'], date, d["Barcode"]))
                                    # Commit the changes to the database
                                    conn.commit()
                                if d['payments_']:
                                    #todo if needed add pid in doc e_doc_info[10]
                                    cursor.execute('UPDATE doc_table SET pid=?, payments=?, doc_updated_date=? WHERE doc_barcode=?', (str(d['pid']), json.dumps(d['payments_']), date, d["Barcode"]))
                                    # Commit the changes to the database
                                    conn.commit()
                                slip_doc_code.append(d["Barcode"])
                        elif d["Barcode"] == "":
                                print("custemer : " + str(self.custemr) + "isneded : " + str(payment_customer_required))
                                # TODO: chacke if self.At_Shop_Id is selected if not make user selecte one
                                        
                                cursor.execute('INSERT INTO upload_doc (doc_barcode, extension_barcode, At_Shop_Id, user_id, customer_id, Seller_id, type, item, qty, price, discount, tax, payments, pid, doc_created_date, doc_expire_date, doc_updated_date) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (str(brcod), "extension_barcode", self.At_Shop_id, self.user['User_id'], self.custemr, Seller_id, "Sale_item", json.dumps(d['new_items']), float(d['count_new_items']), d['price'], d['disc'], d['tax'], json.dumps(d['payments_']), d['T_pid'], date, date, date))
                                cursor.execute('INSERT INTO doc_table (doc_barcode, extension_barcode, At_Shop_Id, user_id, customer_id, Seller_id, type, item, qty, price, discount, tax, payments, pid, doc_created_date, doc_expire_date, doc_updated_date) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (str(brcod), "extension_barcode", self.At_Shop_id, self.user['User_id'], self.custemr, Seller_id, "Sale_item", json.dumps(d['new_items']), float(d['count_new_items']), d['price'], d['disc'], d['tax'], json.dumps(d['payments_']), d['T_pid'], date, date, date))
                                # Commit the changes to the database
                                conn.commit()
                                slip_doc_code.append(brcod)
                             
            if payment_open_drower == 1:
                PrinterForm.open_drower(self, self.user)
             


    def done(self):
        self.save_change()
        self.master.master.destroy()

    def close_tab(self, test_tab):
        test_tab.destroy()
