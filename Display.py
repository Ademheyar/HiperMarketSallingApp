import tkinter as tk
from tkinter import ttk
import sqlite3
from searchbox import search_entry
from Peymentsplit import PaymentForm
from GetVALUE import GetvalueForm
from ApprovedDisplay import ApproveFrame
from Product import ProductForm
from iteminfo import *

conn = sqlite3.connect("my_database.db")
cursor = conn.cursor()

class DisplayFrame(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.user = ""
        self.custemr = ""
        self.onchart = 0
        self.price = 0
        self.pid = 0
        self.pid_peyment = []
        self.items = []
        self.tax = 0
        self.qty = 0
        self.disc = 0
        self.total = 0
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        self.main_frame = tk.Frame(self, bg="black")
        self.main_frame.pack(side="top", fill="both", expand=True)

        # New frame at the top of the main frame
        self.top_frame = tk.Frame(self.main_frame, bg="red", height=screen_height * 0.10, width=screen_width)
        self.top_frame.pack(side="top", fill="both")

        # Create 4 button widgets and pack them to the top_frame
        self.button1 = tk.Button(self.top_frame, text="Barcode", width=int(self.top_frame.winfo_width() * 0.10), bg="red", fg="white", font=("Arial", 12))
        self.button1.pack(side="left", fill="both")
        self.button2 = tk.Button(self.top_frame, text="tag", width=int(self.top_frame.winfo_width() * 0.10), bg="red", fg="white", font=("Arial", 12))
        self.button2.pack(side="left", fill="both")
        self.button3 = tk.Button(self.top_frame, text="123", width=int(self.top_frame.winfo_width() * 0.10), bg="red", fg="white", font=("Arial", 12))
        self.button3.pack(side="left", fill="both")
        self.button4 = tk.Button(self.top_frame, text="Abc", width=int(self.top_frame.winfo_width() * 0.10), bg="red", fg="white", font=("Arial", 12))
        self.button4.pack(side="left", fill="both")

        # Create a label and an entry widget for the search box
        self.search_label = tk.Label(self.top_frame, text="Search:", width=int(self.top_frame.winfo_width() * 0.10), bg="red", fg="white", font=("Arial", 12))
        self.search_label.pack(side="left", fill="both")
        self.search_entry = search_entry(self.top_frame, width=int(screen_width * 0.50), font=("Arial", 12))
        #tk.Entry
        self.search_entry.pack(side="left", fill="both")

        # New frame next to list_items in the main frame
        self.midel_frame = tk.Frame(self.main_frame, bg="blue", height=int(screen_height * 0.90))
        self.midel_frame.pack(side="left", fill="both", expand=True)

        # New listbox in the main frame
        self.list_items = ttk.Treeview(self.midel_frame, columns=("CODE", "BARCODE", "ITEM Name", "AT SHOP", "COLOR", "SIZE", "QTY", "PRICE", "DISCOUNT", "TAX", "TOTAL PRICE"))
        self.list_items.grid_propagate(False)

        # Set the size of the self.list_items widget
        self.list_items.config(height=int(self.midel_frame.winfo_height() * 0.70))

        self.list_items.pack(side="top", fill="both", expand=True)
        self.list_items.heading("#0", text="Item", anchor=tk.W)
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
        
        
        self.total_frame = tk.Frame(self.midel_frame, bg="green")
        self.total_frame.pack(side="top", fill="both")

        # Set the top and bottom frames to fill the available space horizontally
        self.total_frame.pack(side="top")
        self.list_items.pack(side="top")

        # Create labels on the right side of total_frame
        self.total_items_label = tk.Label(self.total_frame, text="Total Items : 0", bg="green", fg="white", font=("Arial", 15))
        self.total_items_label.pack(side="left", padx=10)
        self.total_tax_label = tk.Label(self.total_frame, text="Total Tax : 0", bg="green", fg="white", font=("Arial", 15))
        self.total_tax_label.pack(side="left", padx=10)
        self.total_discount_label = tk.Label(self.total_frame, text="Item Discount : 0", bg="green", fg="white", font=("Arial", 15))
        self.total_discount_label.pack(side="left", padx=10)
        self.total_tdiscount_label = tk.Label(self.total_frame, text="Total Discount : 0", bg="green", fg="white", font=("Arial", 15))
        self.total_tdiscount_label.pack(side="left", padx=10)
        self.total_price_label = tk.Label(self.total_frame, text="Price Befor: 0", bg="green", fg="white", font=("Arial", 15))
        self.total_price_label.pack(side="left", padx=10)
        self.total_label = tk.Label(self.total_frame, text="Total After: 0", bg="green", fg="white", font=("Arial", 15))
        self.total_label.pack(side="left", padx=10)

        # New frame next to list_items in the main frame
        self.buttons_frame = tk.Frame(self.main_frame, bg="brown", height=int(screen_height * 0.90))
        self.buttons_frame.pack(side="left", fill="both", expand=True)

        # Set the grid configuration for buttons_frame
        self.buttons_frame.columnconfigure((0, 1, 2, 3), weight=1, minsize=int(self.buttons_frame.winfo_height() *0.1))
        self.buttons_frame.rowconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8, 9), weight=1, minsize=int(self.buttons_frame.winfo_height() *0.1))

        # Create 6 button widgets and add them to buttons_frame
        self.del_button = tk.Button(self.buttons_frame, text="Delete X", bg="red", fg="white", font=("Arial", 12), command=self.remove_item)
        self.del_button.grid(row=0, column=0, sticky="nsew")
        self.voidlist_button = tk.Button(self.buttons_frame, text="Void", bg="red", fg="white", font=("Arial", 12), command=self.void_items)
        self.voidlist_button.grid(row=0, column=1, sticky="nsew")
        self.qty_button = tk.Button(self.buttons_frame, text="Qty", bg="red", fg="white", font=("Arial", 12), command=self.make_qty)
        self.qty_button.grid(row=0, column=2, sticky="nsew")
        self.mang_button = tk.Button(self.buttons_frame, text="Manger", bg="red", fg="white", font=("Arial", 12), command=self.call_manager)
        self.mang_button.grid(row=0, column=3, sticky="nsew")
        self.prevlist_button = tk.Button(self.buttons_frame, text="Prev", bg="red", fg="white", font=("Arial", 12))
        self.prevlist_button.grid(row=1, column=0, sticky="nsew")
        self.newlist_button = tk.Button(self.buttons_frame, text="New", bg="red", fg="white", font=("Arial", 12))
        self.newlist_button.grid(row=1, column=1, sticky="nsew")
        self.discount_button = tk.Button(self.buttons_frame, text="Discount", bg="red", fg="white", font=("Arial", 12), command=self.make_dicount)
        self.discount_button.grid(row=1, column=2, sticky="nsew")
        self.userinfo_button = tk.Button(self.buttons_frame, text="Userinfo", bg="red", fg="white", font=("Arial", 12))
        self.userinfo_button.grid(row=1, column=3, sticky="nsew")
        self.endday_button = tk.Button(self.buttons_frame, text="Endday", bg="red", fg="white", font=("Arial", 12))
        self.endday_button.grid(row=2, column=0, sticky="nsew")
        self.activets_button = tk.Button(self.buttons_frame, text="Activets", bg="red", fg="white", font=("Arial", 12))
        self.activets_button.grid(row=2, column=1, sticky="nsew")
        self.logout_button = tk.Button(self.buttons_frame, text="Logout", bg="red", fg="white", font=("Arial", 12), command=self.call_loging)
        self.logout_button.grid(row=2, column=2, sticky="nsew")
        self.payment_button = tk.Button(self.buttons_frame, text="Payment", bg="red", fg="white", font=("Arial", 12), command=self.call_splitpayment)
        self.payment_button.grid(row=2, column=3, sticky="nsew")
        self.creat_payment_buttons()
        self.update_info()

    def call_manager(self):
        self.master.show_frame("ManageFrame")
    def call_loging(self):
        self.master.show_frame("LogingFrame")
    
    def call_splitpayment(self):
        i = 0
        for a in self.list_items.get_children():
            i+=1
        if i  <= 0:
            print("no list")
        else:
            PaymentForm(self)
    def add_chart(self):
        
        
        self.pid = 0
        self.price = 0
        item_dic = 0
        item_count = 0
        for a in self.list_items.get_children():
            item = self.list_items.item(a)['values']
            print("in update item: " + str(item))
            item_count += float(item[6])
            item_dic += float(item[8]) 
            self.price += float(item[7])
        print("Amount Pide : " + str(self.price))
        self.total_items_label.config(text="Total Items : " + str(item_count))
        self.total_tax_label.config(text="Total Tax : " + str(self.tax))
        self.total_discount_label.config(text="Item Discount : " + str(item_dic))
        self.total_tdiscount_label.config(text="Total Discount : " + str(self.disc))
        self.total_price_label.config(text="Price Befor : " + str(self.price))
        self.total_label.config(text="Price After: " + str((self.price - item_dic) - self.disc))

        doc_created_date = "doc_created_date"
        doc_expire_date = "doc_expire_date"
        doc_updated_date = "doc_updated_date"
        user_id = "user_id"
        customer_id = "customer_id"
        type = "type"
        discount_REAL = "discount REAL"
        CODE = "CODE"
        BARCODE = "BARCODE"
        ITEM_Name = "ITEM"
        AT_SHOP = "AT_SHOP"
        COLOR = "COLOR"
        SIZE = "SIZE"
        QTY = "QTY"
        PRICE = "PRICE"
        Item_Disc = "Item_Disc"
        TAX = "TAX"
        States = "States"        
        
        print(str([doc_created_date, doc_expire_date, doc_updated_date, user_id, customer_id, type, discount_REAL, CODE, BARCODE, ITEM_Name, AT_SHOP, COLOR, SIZE, QTY, PRICE, Item_Disc, TAX, States]))
        # Insert the new product into the database
        cursor.execute('INSERT INTO pre_doc_table (doc_created_date, doc_expire_date, doc_updated_date, user_id, customer_id, type, discount_REAL, CODE, BARCODE, ITEM_Name, AT_SHOP, COLOR, SIZE, QTY, PRICE, Item_Disc, TAX, States) VALUES ((?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (doc_created_date, doc_expire_date, doc_updated_date, user_id, customer_id, type, discount_REAL, CODE, BARCODE, ITEM_Name, AT_SHOP, COLOR, SIZE, QTY, PRICE, Item_Disc, TAX, States))

        # Commit the changes to the database
        conn.commit()
        
    def get_chart(self):
        cursor.execute("SELECT * FROM pre_doc_table WHERE id=?", (self.onchart,))
        result = self.cursor.fetchone()

        self.pid = 0
        self.price = 0
        item_dic = 0
        item_count = 0
        for a in self.list_items.get_children():
            item = self.list_items.item(a)['values']
            print("in update item: " + str(item))
            item_count += float(item[6])
            item_dic += float(item[8]) 
            self.price += float(item[7])
        print("Amount Pide : " + str(self.price))
        self.total_items_label.config(text="Total Items : " + str(item_count))
        self.total_tax_label.config(text="Total Tax : " + str(self.tax))
        self.total_discount_label.config(text="Item Discount : " + str(item_dic))
        self.total_tdiscount_label.config(text="Total Discount : " + str(self.disc))
        self.total_price_label.config(text="Price Befor : " + str(self.price))
        self.total_label.config(text="Price After: " + str((self.price - item_dic) - self.disc))
        self.update_info()


    def update_info(self):
        self.pid = 0
        self.price = 0
        item_dic = 0
        item_count = 0
        for a in self.list_items.get_children():
            item = self.list_items.item(a)['values']
            print("in update item: " + str(item))
            item_count += float(item[6])
            item_dic += float(item[8]) 
            self.price += float(item[7])
        print("Amount Pide : " + str(self.price))
        self.total_items_label.config(text="Total Items : " + str(item_count))
        self.total_tax_label.config(text="Total Tax : " + str(self.tax))
        self.total_discount_label.config(text="Item Discount : " + str(item_dic))
        self.total_tdiscount_label.config(text="Total Discount : " + str(self.disc))
        self.total_price_label.config(text="Price Befor : " + str(self.price))
        self.total_label.config(text="Price After: " + str((self.price - item_dic) - self.disc))

    def void_items(self):
        for a in self.list_items.get_children():
            self.list_items.delete(a)
        self.update_info()

    def remove_item(self):
        for a in self.list_items.selection():
            self.list_items.delete(a)
        self.update_info()

    def make_qty(self):
        i = GetvalueForm(self)
        if len(self.list_items.selection()) > 0:
            for a in self.list_items.selection():
                values = self.list_items.item(a)['values']
    
                # Modify the values of the item as required
                values[6] = i.value
                
                # Use the item method to update the selected item
                self.list_items.item(a, values=values)
                #a.config
                print("update qty on item "+str(values))
        elif i:
            self.qty = i.value
            print("update qty "+str(self.qty))
        self.update_info()    

    def make_dicount(self):
        i = None
        if len(self.list_items.get_children()) <= 0:
            print("no list")
        else:
            i = GetvalueForm(self)
        if len(self.list_items.selection()) > 0:
            for a in self.list_items.selection():
                values = self.list_items.item(a)['values']
    
                # Modify the values of the item as required
                values[8] = i.value
                
                # Use the item method to update the selected item
                self.list_items.item(a, values=values)
                #a.config
                print("update dicount on item "+str(values))
        elif i:
            self.disc = i.value
            print("update dicount "+str(self.disc))
        self.update_info()    

    def creat_payment_buttons(self):
        cursor.execute("SELECT * FROM tools")
        rows = cursor.fetchall()
        for row in rows:
            tool_name = row[1]
            # Check if the button already exists in the frame
            button_exists = False
            a = 0
            b = 0
            for widget in self.buttons_frame.winfo_children():
                if b == 3: 
                    b = 0
                    a += 1
                    continue
                if widget.cget("text") == tool_name:
                    button_exists = True
                    break
                b+=1
            # Create a new button if it doesn't exist
            if not button_exists:
                if b == 3: 
                    b = 0 
                new_button = tk.Button(self.buttons_frame, text=tool_name, command=lambda : self.call_payment(row[1], self.price))
                new_button.grid(row=a, column=b, sticky="nsew")
    
    def call_payment(self, name, price):
        self.pid_peyment.append(str(name) + " = " + str(price))
        self.process_payment()

    def process_payment(self):
        print("self.pid_peyment = " + str(self.pid_peyment))
        if len(self.list_items.get_children()) <= 0:
            print("no list")
        else:
            payment_name = []
            payment_enable = 0
            payment_quick_pay = 0
            payment_customer_required = 0
            payment_print_slip = 0
            payment_change_allowed = 0
            payment_mark_pad = 0
            payment_open_drower = 0    
            for pyment in self.pid_peyment:
                p = pyment.split(" = ")
                if len(p) <= 0: 
                    break
                cursor.execute("SELECT * FROM tools WHERE name=?", (p[0],))
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
                payment_name.append([str(rows[0][1]), str(p[1])])
                break

            if payment_enable == 0:
                print("no pyment")
            else:
                print("pyment:"+str(payment_enable))
                #add to doc table
                #create doc_id
                # 
                # 
                # item [(|item_code|,|item_name|,|item_shop|,|item_color|,
                #        |item_size|,|item_qty|,|item_price|,|item_disc|,|item_tax|),]    
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
                    cursor.execute("SELECT * FROM product WHERE code=?", (iv[0],))
                    it = cursor.fetchone()
                    item += "(|"
                    item += str(iv[0]) # code
                    item += "|,|"
                    item += str(iv[2]) # name
                    item += "|,|"
                    item += str(iv[3]) # shop
                    item += "|,|"
                    item += str(iv[4]) # color
                    item += "|,|"
                    item += str(iv[5]) # size
                    item += "|,|"
                    item += str(iv[6]) # qty
                    item += "|,|"
                    item += str(iv[7])  # price
                    price += float(iv[6])*float(iv[7])
                    item += "|,|"
                    item += str(iv[8])  # disc
                    disc += float(iv[8])
                    item += "|,|"
                    item += str(iv[9])  # tax
                    tax += float(iv[9])
                    if items+1 <= len(self.list_items.get_children()):
                        item += "|),"
                    else:
                        item += "|)"
                    print("item1 found : " + str(it[12]))
                    it_info = reduc_qty(str(it[12]), str(iv[3]), str(iv[4]),str(iv[5]), str(iv[6]))
                    print("item2 found : " + str(it_info))
                    cursor.execute('UPDATE product SET more_info=? WHERE code=?', (it_info, iv[0]))
                    
                    cursor.execute("SELECT * FROM product WHERE code=?", (iv[0],))
                    it2 = cursor.fetchone()
                    
                    print("item2 found : " + str(it2[12]))
                    # Commit the changes to the database
                    conn.commit()


                cursor.execute('INSERT INTO doc_table (doc_barcode, extension_barcode, user_id, customer_id, type, item, qty, price, discount, tax, doc_created_date, doc_expire_date, doc_updated_date) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', ("doc_barcode", "extension_barcode", "user_id", "customer_id", "type", item, float(items), price, disc, tax, "doc_created_date", "doc_expire_date", "doc_updated_date"))
                
                # Commit the changes to the database
                conn.commit()
                
                print(str(["doc_barcode", "extension_barcode", "user_id", "customer_id", "type", item, disc, tax, "doc_created_date", "doc_expire_date", "doc_updated_date"]))
                
                print("pyment sitting equal :" + str([payment_name, payment_quick_pay, payment_customer_required, payment_print_slip, 
                                                      payment_change_allowed, payment_mark_pad, payment_open_drower]))
                for name in payment_name:
                    ApproveFrame(self, self.list_items)


                # payment_type :: (1id , 2name TEXT, 3code TEXT, 4type TEXT, 5short_key TEXT, 6acsess TEXT,
                # 7enabel INTEGER, 8quick_pay INTEGER, 9customer_required INTEGER, 10printslip REAL, 
                # 11change_allowed REAL, 12markpad REAL, 13open_drower REAL
                
                for child in self.list_items.get_children():
                    print("pymrnt!!!!!", str(child))
        