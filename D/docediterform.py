import tkinter as tk
from tkinter import ttk

import os
import sys
current_dir = os.path.abspath(os.path.dirname(__file__))
MAIN_dir = os.path.join(current_dir, '..')
sys.path.append(MAIN_dir)
#from M.Display import DisplayFrame

class DocEditForm(tk.Frame):
    def __init__(self, master, items):
        tk.Frame.__init__(self, master)
        print("items:"+str(items))
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
        
        # Label "Number" and Entry
        label_number = tk.Label(top_form, text="Number")
        label_number.grid(row=0, column=0)
        entry_number = tk.Entry(top_form)
        entry_number.insert(0, items[0])
        entry_number.grid(row=0, column=1)

        # Label "Data" and Entry
        label_data = tk.Label(top_form, text="Data")
        label_data.grid(row=0, column=4)
        entry_data = tk.Entry(top_form)
        entry_data.insert(0, items[2])
        entry_data.grid(row=0, column=5)

        # Checkbox "Paid"
        checkbox_paid = tk.Checkbutton(top_form, text="Paid")
        checkbox_paid.grid(row=0, column=6)

        # Label "External Doc" and Entry
        label_external_doc = tk.Label(top_form, text="External Document")
        label_external_doc.grid(row=1, column=0)
        entry_external_doc = tk.Entry(top_form)
        entry_external_doc.insert(0, items[1])
        entry_external_doc.grid(row=1, column=1)

        # Label "Due Date" and Entry
        label_due_date = tk.Label(top_form, text="Due Date")
        label_due_date.grid(row=1, column=4)
        entry_due_date = tk.Entry(top_form)
        entry_due_date.insert(0, items[4])
        entry_due_date.grid(row=1, column=5)

        # Label "Customer" and Entry
        label_customer = tk.Label(top_form, text="Customer")
        label_customer.grid(row=2, column=0)
        entry_customer = tk.Entry(top_form)
        entry_customer.insert(0, items[3])
        entry_customer.grid(row=2, column=1)

        # Button
        button = tk.Button(top_form, text="Button")
        button.grid(row=2, column=4)

        # Label "Stock Date" and Entry
        label_stock_date = tk.Label(top_form, text="Stock Date")
        label_stock_date.grid(row=2, column=5)
        entry_stock_date = tk.Entry(top_form)
        entry_stock_date.insert(0, items[6])
        entry_stock_date.grid(row=2, column=6)



        
        # Child frame 2 - SEARCH_FORM
        search_form = tk.Frame(self)
        search_form.grid(row=1, column=0, rowspan=4, sticky="nsew")

        # Child frame 3 - CENTER_FORM
        center_form = tk.Frame(self)
        center_form.grid(row=1, column=1, rowspan=3, columnspan=2, sticky="nsew")

        # Child frame 4 - INFO_FORM
        info_form = tk.Frame(self)
        info_form.grid(row=4, column=1, columnspan=3, sticky="nsew")

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
        list_items = ttk.Treeview(items_tab, columns=("Shop Name", "Color", "Size", "Barcode", "Qtyfirst", "Qty", "cdate", "update"))
        list_items.pack(side='top', fill='both')
        list_items.heading("#0", text="Shop Name", anchor=tk.W)
        list_items.column("#0", stretch=tk.NO, minwidth=25, width=125)
        list_items.heading("#1", text="Color", anchor=tk.W)
        list_items.column("#1", stretch=tk.NO, minwidth=25, width=125)
        list_items.heading("#2", text="Size", anchor=tk.W)
        list_items.column("#2", stretch=tk.NO, minwidth=25, width=125)
        list_items.heading("#3", text="Barcode", anchor=tk.W)
        list_items.column("#3", stretch=tk.NO, minwidth=25, width=125)
        list_items.heading("#4", text="Qtyfirst", anchor=tk.W)
        list_items.column("#4", stretch=tk.NO, minwidth=25, width=125)
        list_items.heading("#5", text="Qty", anchor=tk.W)
        list_items.column("#5", stretch=tk.NO, minwidth=25, width=125)
        list_items.heading("#6", text="cdate", anchor=tk.W)
        list_items.column("#6", stretch=tk.NO, minwidth=25, width=125)
        list_items.heading("#7", text="update", anchor=tk.W)
        list_items.column("#7", stretch=tk.NO, minwidth=25, width=125)
        print("tiems : " + str(items[5]))
        items_lists = items[5].split("|),")
        code, name, shop, color, size, qty, price, total_price, PRICE, \
        disc, Disc, tax, TAX, payments = ['', '', '', "","","","",0,0,"",0,"",0, ""]
        for values in items_lists:
            item = values.split("|,|")
            #for each items
            code = item[0].replace("(|", "")
            name = item[1]
            # if item shop and sold shop not same
            shop = item[2]
            color = item[3]
            size = item[4]
            qty = item[5]
            price = item[6]
            total_price = float(qty)*float(price)
            PRICE += total_price
            disc = item[7]
            Disc += float(disc)
            tax = item[8].replace("|)", "")
            TAX += float(tax)
            print("list : " + str([code, name, shop, color, size, qty, price, total_price, PRICE, disc, Disc, tax, TAX]))
            list_items.insert("", 'end', text="", values=(code, name, shop, color, size, qty, price, total_price, PRICE, disc, Disc, tax, TAX))

        # Tab 2 - Payment
        payment_tab = tk.Frame(center_notebook)
        center_notebook.add(payment_tab, text="Payment")
        list_payment = ttk.Treeview(payment_tab, columns=("Peyment Type", "Price", "Paid", "Paid Date"))
        list_payment.pack(side='top', fill='both')
        list_payment.heading("#0", text="ID", anchor=tk.W)
        list_payment.column("#0", stretch=tk.NO, width=50)
        list_payment.heading("#1", text="Peyment Type", anchor=tk.W)
        list_payment.column("#1", stretch=tk.NO, width=250)
        list_payment.heading("#2", text="Price", anchor=tk.W)
        list_payment.column("#2", stretch=tk.NO, width=50)
        list_payment.heading("#3", text="Paid", anchor=tk.W)
        list_payment.column("#3", stretch=tk.NO, width=50)
        list_payment.heading("#4", text="Paid Date", anchor=tk.W)
        list_payment.column("#4", stretch=tk.NO, width=250)
        print("tiems : " + str(items[10]))
        items_lists = items[10].split(",")
        code, name, shop, color, size, qty, price, total_price, PRICE, \
        disc, Disc, tax, TAX = ['', '', '', "","","","",0,0,"",0,"",0]
        id = 0
        for payment in items_lists:
            item = payment.split(" = ")
            print("item :" + str(item))
            #for each items
            code = item[0].replace("(|", "")
            name = item[1]
            print("list : " + str([code, name]))
            list_payment.insert("", 'end', text=id, values=(code, name))
            id += 1
