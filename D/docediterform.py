import tkinter as tk
from tkinter import ttk

import sqlite3
import datetime
import os
import sys
import os
import sys
current_dir = os.path.abspath(os.path.dirname(__file__))
MAIN_dir = os.path.join(current_dir, '..')
sys.path.append(MAIN_dir)
#from M.Display import DisplayFrame

from D.searchbox import search_entry
from D.ChooseCustemr import UserManagementApp
from D.iteminfo import *


data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data'))
db_path = os.path.join(data_dir, 'my_database.db')
conn = sqlite3.connect(db_path)
cursor = conn.cursor()


class DocEditForm(tk.Frame):
    def __init__(self, master, items, id):
        tk.Frame.__init__(self, master)
        print("items:"+str(items))
        self.items = items
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
        self.search_entry = search_entry(items_tab, font=("Arial", 12))
        #tk.Entry
        self.search_entry.grid(row=0, column=0, columnspan=4, sticky="nsew")

        self.list_items = ttk.Treeview(items_tab, columns=("CODE", "BARCODE", "ITEM Name", "AT SHOP", "COLOR", "SIZE", "QTY", "PRICE", "DISCOUNT", "TAX", "TOTAL PRICE"))
        #self.list_items.grid_propagate(False)

        
        # Add vertical scrollbar
        tree_scrollbar_y = ttk.Scrollbar(self.list_items, orient='vertical', command=self.list_items.yview)
        self.list_items.configure(yscrollcommand=tree_scrollbar_y.set)
        tree_scrollbar_y.pack(side='right', fill='y')

        # Add horizontal scrollbar
        tree_scrollbar_x = ttk.Scrollbar(self.list_items, orient='horizontal', command=self.list_items.xview)
        self.list_items.configure(xscrollcommand=tree_scrollbar_x.set)
        tree_scrollbar_x.pack(side='bottom', fill='x')

        self.list_items.grid(row=1, column=0, columnspan=4, sticky="nsew")
        self.list_items.heading("#0", text="Id", anchor=tk.W)
        self.list_items.column("#0", stretch=tk.NO, minwidth=25, width=100)   
        self.list_items.heading("#1", text="CODE", anchor=tk.W)
        self.list_items.column("#1", stretch=tk.NO, minwidth=25, width=50)
        self.list_items.heading("#2", text="BARCODE", anchor=tk.W)
        self.list_items.column("#2", stretch=tk.NO, minwidth=25, width=100)
        self.list_items.heading("#3", text="ITEM Name", anchor=tk.W)
        self.list_items.column("#3", stretch=tk.NO, minwidth=25, width=125)
        self.list_items.heading("#4", text="AT SHOP", anchor=tk.W)
        self.list_items.column("#4", stretch=tk.NO, minwidth=25, width=100)
        self.list_items.heading("#5", text="COLOR", anchor=tk.W)
        self.list_items.column("#5", stretch=tk.NO, minwidth=25, width=100)
        self.list_items.heading("#6", text="SIZE", anchor=tk.W)
        self.list_items.column("#6", stretch=tk.NO, minwidth=25, width=50)
        self.list_items.heading("#7", text="QTY", anchor=tk.W)
        self.list_items.column("#7", stretch=tk.NO, minwidth=25, width=50)
        self.list_items.heading("#8", text="PRICE", anchor=tk.W)
        self.list_items.column("#8", stretch=tk.NO, minwidth=25, width=100)
        self.list_items.heading("#9", text="DISCOUNT", anchor=tk.W)
        self.list_items.column("#9", stretch=tk.NO, minwidth=25, width=100)
        self.list_items.heading("#10", text="TAX", anchor=tk.W)
        self.list_items.column("#10", stretch=tk.NO, minwidth=25, width=100)
        self.list_items.heading("#11", text="TOTAL PRICE", anchor=tk.W)
        self.list_items.column("#11", stretch=tk.NO, minwidth=25, width=100)

        
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

<<<<<<< HEAD
        self.list_payment = ttk.Treeview(payment_tab, columns=("Peyment Type", "Paid", "Paid Date", "Updated Date", "User"))
=======
        self.list_payment = ttk.Treeview(payment_tab, columns=("Peyment Type", "Paid", "Paid Date", "Updated Date", "User", "Paid", "Extantion Bracodes"))
>>>>>>> db9ae79 (adding seller)
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
<<<<<<< HEAD
=======
        self.list_payment.heading("#6", text="Paid", anchor=tk.W)
        self.list_payment.column("#6", stretch=tk.NO, width=250)
        self.list_payment.heading("#7", text="Extantion Bracodes", anchor=tk.W)
        self.list_payment.column("#7", stretch=tk.NO, width=250)
>>>>>>> db9ae79 (adding seller)
        
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

    def load_items(self):
        print("tiems : " + str(self.items[5]))
        items_lists = self.items[5].split("|),")
        if "|)," in self.items[5]:
            print("spliting by |")
            items_lists = self.items[5].split("|),")
            for values in items_lists:
                item = values.split("|,|")
                code, name, shop, color, size, qty, price, total_price, PRICE, \
                disc, Disc, tax, TAX, payments = ['', '', '', "","","","",0,0,"",0,"",0, ""]
                if len(item) == 10:
                    print("there is id :")
                    #for each items
                    id = item[0].replace("(|", "")
                    code = item[1]
                    name = item[2]
                    # if item shop and sold shop not same
                    shop = item[3]
                    color = item[4]
                    size = item[5]
                    qty = item[6]
                    price = item[7]
                    total_price = float(qty)*float(price)
                    PRICE += total_price
                    disc = item[8].replace("|)", "").replace("|", "")
                    Disc += float(disc)
                    tax = item[9].replace("|)", "")
                    TAX += float(tax)
                elif len(item) == 9:
                    print("no id :")
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
                    disc = item[7].replace("|)", "").replace("|", "")
                    Disc += float(disc)
                    tax = item[8].replace("|)", "")
                    TAX += float(tax)
                if len(item) >= 9:
                    print("list | " + str([code, "", name, shop, color, size, qty, price, total_price, PRICE, disc, Disc, tax, TAX]))
                    self.list_items.insert("", 'end', text=id, values=(code, "", name, shop, color, size, qty, price, total_price, PRICE, disc, Disc, tax, TAX))
                    self.olditems.append([id, code, name, shop, color, size, qty, price])
        else:
            print("spliting by :")
            items_lists = self.items[5].split(":),")
            for values in items_lists:
                id, code, barcode, name, shop, color, size, qty, price, total_price, PRICE, \
                disc, Disc, tax, TAX, payments = [0,'', '', '', '', "","","","",0,0,"",0,"",0, ""]
                item = values.split(":,:")
                if len(item) == 10:
                    print("no bar code :")
                    #for each items
                    id = item[0].replace("(:", "")
                    code = item[1]
                    name = item[2]
                    # if item shop and sold shop not same
                    shop = item[3]
                    color = item[4]
                    size = item[5]
                    qty = item[6]
                    price = item[7]
                    total_price = float(qty)*float(price)
                    PRICE += total_price
                    disc = item[8]
                    Disc += float(disc)
                    tax = item[9].replace(":)", "")
                    TAX += float(tax)
                elif len(item) == 11:
                    print("with barcode :")
                    #for each items
                    id = item[0].replace("(:", "")
                    code = item[1].replace("(:", "")
                    barcode = item[2]
                    name = item[3]
                    # if item shop and sold shop not same
                    shop = item[4]
                    color = item[5]
                    size = item[6]
                    qty = item[7]
                    price = item[8]
                    total_price = float(qty)*float(price)
                    PRICE += total_price
                    disc = item[9]
                    Disc += float(disc)
                    tax = item[10].replace(":)", "")
                    TAX += float(tax)
                if len(item) >= 9:
                    print("list : " + str([code, barcode, name, shop, color, size, qty, price, total_price, PRICE, disc, Disc, tax, TAX]))
                    self.list_items.insert("", 'end', text=id, values=(code, barcode, name, shop, color, size, qty, price, total_price, PRICE, disc, Disc, tax, TAX))
                    self.olditems.append([id, code, barcode, name, shop, color, size, qty, price])

    def add_item(self, item, barcode, shop_name, color, size, qty):
        self.list_items.insert("", "end", text=str(item[0]), values=(item[2], "", item[1], shop_name, color, size, float(qty), item[9], item[10],float(float(qty))*float(item[9]), 0, self.disc, 0, 0))
    
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
            price = item[1]
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
        item = ""
        price = 0
        disc = 0
        tax = 0
        items = 0
        for a in self.list_items.get_children():
            items += 1
            print(str(self.list_items.item(a)))
            i = self.list_items.item(a)
            iv = i['values']
            id = i['text']
            print(str(id))
            cursor.execute("SELECT * FROM product WHERE id=?", (id,))
            it = cursor.fetchone()
            if it:
                item += "(:"
                item += str(id) # ID
                item += ":,:"
                item += str(iv[0]) # code
                item += ":,:"
                item += str(iv[1]) # barcode
                item += ":,:"
                item += str(iv[2]) # name
                item += ":,:"
                item += str(iv[3]) # shop
                item += ":,:"
                item += str(iv[4]) # color
                item += ":,:"
                item += str(iv[5]) # size
                item += ":,:"
                item += str(iv[6]) # qty
                item += ":,:"
                item += str(iv[7])  # price
                price += float(iv[6])*float(iv[7])
                item += ":,:"
                item += str(iv[8])  # disc
                disc += float(iv[8])
                item += ":,:"
                item += str(iv[9])  # tax
                tax += float(iv[9])
                
                if items+1 <= len(self.list_items.get_children()):
                    item += ":),"
                else:
                    item += ":)"
                havetoaddqty = 0
                found = 0
                for olditem in self.olditems:
                    # [id, code, name, shop, color, size, qty, price]
                    if found == 0 and havetoaddqty == 0 and (olditem[1] == iv[0] and olditem[2] == iv[2] or olditem[0] == id) and \
                        olditem[4] == iv[3] and olditem[5] == iv[4] and olditem[6] == iv[5]:
                        print("olditem : " + str(olditem))
                        if float(olditem[7]) == float(iv[6]):
                            self.olditems.remove(olditem)
                            found = 1
                        elif float(olditem[7]) < float(iv[6]):
                            havetoaddqty = float(iv[6]) - float(olditem[7])
                            olditem[7] = str(havetoaddqty)
                        elif float(olditem[7]) > float(iv[6]):
                            olditem[7] = str(float(olditem[7]) - float(iv[6]))
                            found = 1
                        break
                
                if found == 0:
                    if havetoaddqty == 0:
                        havetoaddqty = float(iv[6])
                    print("iv : " + str(iv))
                    print("REDUSE item11 found : " + str([str(it[12]), 0, str(iv[3]), str(iv[4]),str(iv[5]), str(havetoaddqty)]))
                    it_info = reduc_qty(str(it[12]), 0, str(iv[3]), str(iv[4]),str(iv[5]), str(havetoaddqty))
                    print("REDUSE item12 found : " + str(it_info))
                
                    cursor.execute('UPDATE product SET more_info=? WHERE id=?', (it_info, id))
        for olditem in self.olditems:
            # [id, code, name, shop, color, size, qty, price]
            cursor.execute("SELECT * FROM product WHERE id=?", (olditem[0],))
            it = cursor.fetchone()
            if len(it) > 0:
                print("REDUSE item21: " + str([str(it[12]), 1, str(olditem[4]), str(olditem[5]),str(olditem[6]), str(olditem[7])]))
                it_info = reduc_qty(str(it[12]), 1, str(olditem[4]), str(olditem[5]),str(olditem[6]), str(olditem[7]))
                print("REDUSE item22 : " + str(it_info))
            
                cursor.execute('UPDATE product SET more_info=? WHERE id=?', (it_info, olditem[0]))
                
        print("updated item = " + str(item))
        payment_name = []
        payments_ = ""
        slip_payments = ""
        payment_enable = 0
        payment_quick_pay = 0
        payment_customer_required = 0
        payment_print_slip = 0
        payment_change_allowed = 0
        payment_mark_pad = 0
        payment_open_drower = 0 
        date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        if payment_customer_required:
            if self.selected_user.get() == "":
                app = UserManagementApp(self)
                if app.user_details:
                    self.selected_user.insert(0, app.user_details['id'])
                    print(self.selected_user)

        custmer = self.selected_user
        du_date = self.entry_due_date.get()
        external_doc = self.entry_external_doc.get()
        paid = 0
        pay_index = 0
        for a in self.list_payment.get_children():
            pay_index += 1
            print(str(self.list_payment.item(a)))
            p = self.list_payment.item(a)
            iv = p['values']
            id = p['text']
            cursor.execute("SELECT * FROM tools WHERE name=?", (iv[0],))
            rows = cursor.fetchall()
            print("rows:" + str(rows))
            if rows[0][6] == 1: # chack if enabled
                payment_enable += 1
            if rows[0][7] == 1 and payment_quick_pay == 0: # chack if enabled
                payment_quick_pay = 1
            if rows[0][8] == 1 and payment_customer_required == 0: # chack if enabled
                payment_customer_required = 1
            if rows[0][9] == 1 and payment_print_slip == 0: # chack if enabled
                payment_print_slip = 1
            if rows[0][10] == 1 and payment_change_allowed == 0: # chack if enabled
                payment_change_allowed = 1
            if rows[0][11] == 1 and payment_mark_pad == 0: # chack if enabled
                payment_mark_pad = 1
            if rows[0][12] == 1 and payment_open_drower == 0: # chack if enabled
                payment_open_drower = 1
            payments_ += "(" + str(pay_index) + "," + str(rows[0][1]) + "," +  str(iv[1]) + "," + str(iv[2]) + "," + str(iv[3]) + "," + str(iv[4]) + "),"
            slip_payments += str(pay_index) + ". " + str(rows[0][1]) + ", " +  str(iv[1]) + ", " +  str(iv[2]) + "\n"
            paid += float(iv[1])
            payment_name.append([str(rows[0][1]), str(iv[1])])
            break
        print("updated pyment "+str(payment_enable) + ":" + str(payments_))
    
        
        #TODO: CHACK IF IT IS PAID OR HAVE CRDITE
        #paid = self.checkbox_paid()
        
        cursor.execute('UPDATE doc_table SET extension_barcode=?, customer_id=?, item=?, qty=?, price=?, discount=?, tax=?, payments=?, doc_expire_date=?, doc_updated_date=? WHERE id=?', (external_doc, custmer, str(item), items, price, disc, tax, payments_, du_date, date, self.id))
        # Commit the changes to the database
        conn.commit()
        
        print(str(["23-200-" + str(), "extension_barcode", "customer_id", "type", item, disc, tax, payments_, "doc_created_date", "doc_expire_date", "doc_updated_date"]))
        
        print("pyment sitting equal :" + str([payment_name, payment_quick_pay, payment_customer_required, payment_print_slip, 
                                                payment_change_allowed, payment_mark_pad, payment_open_drower]))

    def done(self):
        self.save_change()
        self.master.destroy()

    def close_tab(self, test_tab):
        test_tab.destroy()
