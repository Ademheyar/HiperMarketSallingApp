import tkinter as tk
from tkinter import ttk
import sqlite3
import shutil
import datetime
import os
import atexit
import sys
current_dir = os.path.abspath(os.path.dirname(__file__))
MAIN_dir = os.path.join(current_dir, '..')
sys.path.append(MAIN_dir)
from D.searchbox import search_entry
from D.Peymentsplit import PaymentForm
from D.GetVALUE import GetvalueForm
from D.Showchartlists import ShowchartForm
from D.ApprovedDisplay import ApproveFrame
from M.Product import ProductForm
from D.iteminfo import *
from D.endday import EnddayForm
from D.Upload_ import UploadingForm
from D.user_info import UserInfoForm
from D.printer import PrinterForm

from Manager import ManageForm

data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data'))
db_path = os.path.join(data_dir, 'my_database.db')
conn = sqlite3.connect(db_path)
cursor = conn.cursor()


class DisplayFrame(tk.Frame):
    def __init__(self, master, user):
        tk.Frame.__init__(self, master)
        self.user = user
        self.custemr = ""
        self.chart_index = 0
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
        self.main_Notebook = ttk.Notebook(self)
        self.main_Notebook.pack(side="top", fill="both", expand=True)

        '''
        # Create tabs
        tab1 = ttk.Frame(self.main_Notebook)
        tab2 = ttk.Frame(self.main_Notebook)

        # Add tabs to the self.main_Notebook
        self.main_Notebook.add(tab1, text='Tab 1')
        self.main_Notebook.add(tab2, text='Tab 2')

        # Add widgets to the tabs
        ttk.Label(tab1, text='This is tab 1').pack()
        ttk.Label(tab2, text='This is tab 2').pack()
        '''

        self.main_frame = tk.Frame(self.main_Notebook, bg="black")
        self.main_frame.grid()
        self.main_Notebook.add(self.main_frame, text='HOME')
        
        # Set the grid configuration for buttons_frame
        self.main_frame.columnconfigure((0, 1), weight=1)
        self.main_frame.columnconfigure(1, weight=0)
        self.main_frame.rowconfigure(0, weight=0)
        self.main_frame.rowconfigure(1, weight=2)


        # create the second frame and add it to the container
        self.manage_form = ManageForm(self.main_Notebook)
        self.manage_form.pack(side="top", fill="both", expand=True)
        self.main_Notebook.add(self.manage_form, text='MANAGE')
        #self.manage_form.grid(row=0, column=0, sticky="nsew")

        #self.frames["ManageFrame"] = manage_form

        # * New frame at the top of the main frame
        self.top_frame = tk.Frame(self.main_frame, bg="red", height=int(screen_height * 0.70))
        self.top_frame.grid(row=0, column=0, columnspan=2, sticky="nsew")
        # Set the grid configuration for buttons_frame
        self.top_frame.columnconfigure((0, 1, 2, 4), weight=0)
        self.top_frame.columnconfigure((5), weight=1)
        self.top_frame.rowconfigure((0), weight=1)
        
        # Create 4 button widgets and pack them to the top_frame
        self.button1 = tk.Button(self.top_frame, text="Barcode", width=int(self.top_frame.winfo_width() * 0.10), bg="red", fg="white", font=("Arial", 12))
        self.button1.grid(row=0, column=0, sticky="nsew")
        self.button2 = tk.Button(self.top_frame, text="tag", width=int(self.top_frame.winfo_width() * 0.10), bg="red", fg="white", font=("Arial", 12))
        self.button2.grid(row=0, column=1, sticky="nsew")
        self.button3 = tk.Button(self.top_frame, text="123", width=int(self.top_frame.winfo_width() * 0.10), bg="red", fg="white", font=("Arial", 12))
        self.button3.grid(row=0, column=2, sticky="nsew")
        self.button4 = tk.Button(self.top_frame, text="Abc", width=int(self.top_frame.winfo_width() * 0.10), bg="red", fg="white", font=("Arial", 12))
        self.button4.grid(row=0, column=3, sticky="nsew")

        # Create a label and an entry widget for the search box
        self.search_label = tk.Label(self.top_frame, text="Search:", bg="red", fg="white", font=("Arial", 12))
        self.search_label.grid(row=0, column=4, sticky="nsew")
        print("screen_width :: " + str((self.top_frame.winfo_width())) + " = " + str((screen_width/3)))
        self.search_entry = search_entry(self.top_frame, font=("Arial", 12))
        #tk.Entry
        self.search_entry.grid(row=0, column=5, columnspan=4, sticky="nsew")

        # * New frame next to list_items in the main frame
        self.midel_frame = tk.Frame(self.main_frame, bg="blue")
        self.midel_frame.grid(row=1, column=0, sticky="nsew")

        # New listbox in the main frame
        self.list_items = ttk.Treeview(self.midel_frame, columns=("CODE", "BARCODE", "ITEM Name", "AT SHOP", "COLOR", "SIZE", "QTY", "PRICE", "DISCOUNT", "TAX", "TOTAL PRICE"))
        #self.list_items.grid_propagate(False)

        
        # Add vertical scrollbar
        tree_scrollbar_y = ttk.Scrollbar(self.list_items, orient='vertical', command=self.list_items.yview)
        self.list_items.configure(yscrollcommand=tree_scrollbar_y.set)
        tree_scrollbar_y.pack(side='right', fill='y')

        # Add horizontal scrollbar
        tree_scrollbar_x = ttk.Scrollbar(self.list_items, orient='horizontal', command=self.list_items.xview)
        self.list_items.configure(xscrollcommand=tree_scrollbar_x.set)
        tree_scrollbar_x.pack(side='bottom', fill='x')

        self.list_items.pack(side="top", fill="both", expand=True)
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
        
        
        self.total_frame = tk.Frame(self.midel_frame, height=100, bg="green")
        self.total_frame.pack(side="top", fill="both")

        # Set the top and bottom frames to fill the available space horizontally
        self.total_frame.pack(side="top")
        self.list_items.pack(side="top")

        # Create labels on the right side of total_frame
        self.total_items_label = tk.Label(self.total_frame, text="Total Items : 0", bg="green", fg="white", font=("Arial", 10))
        self.total_items_label.pack(side="left", padx=5)
        self.total_tax_label = tk.Label(self.total_frame, text="Total Tax : 0", bg="green", fg="white", font=("Arial", 10))
        self.total_tax_label.pack(side="left", padx=5)
        self.total_discount_label = tk.Label(self.total_frame, text="Item Discount : 0", bg="green", fg="white", font=("Arial", 10))
        self.total_discount_label.pack(side="left", padx=5)
        self.total_tdiscount_label = tk.Label(self.total_frame, text="Total Discount : 0", bg="green", fg="white", font=("Arial", 10))
        self.total_tdiscount_label.pack(side="left", padx=5)
        self.total_price_label = tk.Label(self.total_frame, text="Price Befor: 0", bg="green", fg="white", font=("Arial", 10))
        self.total_price_label.pack(side="left", padx=5)
        self.total_label = tk.Label(self.total_frame, text="Total After: 0", bg="green", fg="white", font=("Arial", 10))
        self.total_label.pack(side="left", padx=5)

        # * New frame next to list_items in the main frame
        self.buttons_frame = tk.Frame(self.main_frame, bg="brown")
        self.buttons_frame.grid(row=1, column=1, rowspan=2, sticky="nsew")

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
        self.discount_button = tk.Button(self.buttons_frame, text="Discount", bg="red", fg="white", font=("Arial", 12), command=self.make_dicount)
        self.discount_button.grid(row=0, column=3, sticky="nsew")
        self.prevlist_button = tk.Button(self.buttons_frame, text="Prev", bg="red", fg="white", font=("Arial", 12), command=lambda: self.next_prev_chart("prev"))
        self.prevlist_button.grid(row=1, column=0, sticky="nsew")
        self.prevlist_button.config(state=tk.DISABLED)
        self.activets_button = tk.Button(self.buttons_frame, text="Activets", bg="red", fg="white", font=("Arial", 12), command=self.call_chartForm)
        self.activets_button.grid(row=1, column=1, sticky="nsew")
        self.newlist_button = tk.Button(self.buttons_frame, text="New", bg="red", fg="white", font=("Arial", 12), command=self.new_chart)
        self.newlist_button.grid(row=1, column=2, sticky="nsew")
        self.endday_button = tk.Button(self.buttons_frame, text="Endday", bg="red", fg="white", font=("Arial", 12), command=lambda: EnddayForm(self))
        self.endday_button.grid(row=1, column=3, sticky="nsew")
        self.userinfo_button = tk.Button(self.buttons_frame, text="Userinfo", bg="red", fg="white", font=("Arial", 12), command=lambda: UserInfoForm(self))
        self.userinfo_button.grid(row=2, column=0, sticky="nsew")
        self.logout_button = tk.Button(self.buttons_frame, text="Logout", bg="red", fg="white", font=("Arial", 12), command=self.exit)
        self.logout_button.grid(row=2, column=1, sticky="nsew")
        self.payment_button = tk.Button(self.buttons_frame, text="Payment", bg="red", fg="white", font=("Arial", 12), command=self.call_splitpayment)
        self.payment_button.grid(row=2, column=2, sticky="nsew")
        self.update_button = tk.Button(self.buttons_frame, text="update", bg="red", fg="white", font=("Arial", 12), command=lambda: UploadingForm(self))
        self.update_button.grid(row=2, column=3, sticky="nsew")
        # Register the backup function to be called when the application exits
        self.max_backups = 4     
        #self.void_items()
        #ApproveFrame(self, "", "", "", self.user)
        atexit.register(self.backup_database)
        self.creat_payment_buttons()
        self.update_info()
        self.update_list_items()
        

    # Function to perform the backup
    def backup_database(self):
        # Database file paths
        database_file = 'data/my_database.db'
        backup_folder = 'backup/'
        max_backups = self.max_backups
        # Create the backup folder if it doesn't exist
        os.makedirs(backup_folder, exist_ok=True)
        
        # List existing backup files
        existing_backups = sorted(os.listdir(backup_folder))
        
        # Delete oldest backups if exceeding the maximum allowed
        if len(existing_backups) >= max_backups:
            num_backups_to_delete = len(existing_backups) - max_backups + 1
            for i in range(num_backups_to_delete):
                file_to_delete = os.path.join(backup_folder, existing_backups[i])
                os.remove(file_to_delete)
                print("Deleted old backup:", file_to_delete)
        
        # Create a backup file name
        backup_file = os.path.join(backup_folder, 'backup_' + datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S') + '.db')
        
        # Connect to the database
        conn = sqlite3.connect(database_file)
        
        try:
            # Create a backup by copying the database file
            shutil.copy2(database_file, backup_file)
            print("Backup created successfully:", backup_file)
        except IOError as e:
            print("Error creating backup:", str(e))
        finally:
            # Close the database connection
            conn.close()
            
    def load_setting(self):
        cursor.execute("SELECT * FROM setting")
        b = cursor.fetchall()
        if len(b) <= 0:
            print("sitting : " + self.user)
            cursor.execute('INSERT INTO setting (user_name, barcode_count, printer) VALUES (?, ?, ?)', (self.user, 0, ""))
            # Commit the changes to the database
            conn.commit()
        else:
            print("sitting : " + str(b))
        
    def call_manager(self):
        self.master.show_frame("ManageFrame")

    def exit(self):
        self.master.show_frame("LogingFrame")

    def load(self):
        self.master.show_frame("DisplayFrame")
        self.load_setting()
        #ApproveFrame(self, [])
    
    def call_splitpayment(self):
        i = 0
        for a in self.list_items.get_children():
            i+=1
        if i  <= 0:
            print("no list")
        else:
            PaymentForm(self)
    def new_chart(self):
        self.update_info()
        if len(self.list_items.get_children()) > 0:
            cursor.execute("SELECT * FROM pre_doc_table")
            res = cursor.fetchall()
            self.chart_index = len(res)
            self.void_items()

    def update_chart(self):
        doc_created_date = "doc_created_date"
        doc_expire_date = "doc_expire_date"
        doc_updated_date = "doc_updated_date"
        AT_SHOP = "AT_SHOP"
        user_id = "user_id"
        customer_id = "customer_id"
        type = "type"
        ITEM = ""
        PRICE = 0
        Disc = 0
        TAX = 0
        States = "States"
        
        items = 0
        for a in self.list_items.get_children():
            items += 1
            print(str(self.list_items.item(a)))
            i = self.list_items.item(a)
            iv = i['values']
            id = i['text']
            ITEM += "(|"
            ITEM += str(id) # id
            ITEM += "|,|"
            ITEM += str(iv[0]) # code
            ITEM += "|,|"
            ITEM += str(iv[2]) # name
            ITEM += "|,|"
            ITEM += str(iv[3]) # shop
            ITEM += "|,|"
            ITEM += str(iv[4]) # color
            ITEM += "|,|"
            ITEM += str(iv[5]) # size
            ITEM += "|,|"
            ITEM += str(iv[6]) # qty
            ITEM += "|,|"
            ITEM += str(iv[7])  # price
            PRICE += float(iv[6])*float(iv[7])
            ITEM += "|,|"
            ITEM += str(iv[8])  # disc
            Disc += float(iv[8])
            ITEM += "|,|"
            ITEM += str(iv[9])  # tax
            TAX += float(iv[9])
            if items+1 <= len(self.list_items.get_children()):
                ITEM += "|),"
            else:
                ITEM += "|)"

        if items > 0:
            # Define the query to check if the ID exists in the table
            query = f"SELECT id FROM pre_doc_table WHERE id = {self.chart_index}"

            # Execute the query and fetch the results
            cursor.execute(query)
            result = cursor.fetchone()
            # Check if the query returned a result
            if result is not None:
                print(str([doc_created_date, doc_expire_date, doc_updated_date, AT_SHOP, user_id, customer_id, type, ITEM, PRICE, Disc, TAX, States]))
                # Insert the new product into the database
                cursor.execute('UPDATE pre_doc_table SET doc_created_date=?, doc_expire_date=?, doc_updated_date=?, AT_SHOP=?, user_id=?, customer_id=?, type=?, ITEM=?, PRICE=?, Disc=?, TAX=?, States=? WHERE id=?', (doc_created_date, doc_expire_date, doc_updated_date, AT_SHOP, user_id, customer_id, type, ITEM, float(PRICE), float(Disc), float(TAX), States, self.chart_index))

                # Commit the changes to the database
                conn.commit()
                print(f"Record with ID {self.chart_index} has been inserted into the table")                
                print(str([doc_created_date, doc_expire_date, doc_updated_date, AT_SHOP, user_id, customer_id, type, ITEM, float(PRICE), float(Disc), float(TAX), States, self.chart_index]))
            else:
                print(f"Record with ID {self.chart_index} does not exist in the table")
                print(str([doc_created_date, doc_expire_date, doc_updated_date, AT_SHOP, user_id, customer_id, type, ITEM, PRICE, Disc, TAX, States]))
                # Insert the new product into the database
                cursor.execute('INSERT INTO pre_doc_table (id, doc_created_date, doc_expire_date, doc_updated_date, AT_SHOP, user_id, customer_id, type, ITEM, PRICE, Disc, TAX, States) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (self.chart_index, doc_created_date, doc_expire_date, doc_updated_date, AT_SHOP, user_id, customer_id, type, ITEM, float(PRICE), float(Disc), float(TAX), States))

                print(str(["doc_barcode", "extension_barcode", "user_id", "customer_id", "type", ITEM, Disc, TAX, "doc_created_date", "doc_expire_date", "doc_updated_date"]))
                # Commit the changes to the database
                conn.commit()
                
                
    def update_list_items(self):
        # Define the SQL query to fetch the product information based on doc_created_date
        # Execute the query and fetch the results
        cursor.execute("SELECT * FROM pre_doc_table")
        res = cursor.fetchall()
        if len(res) > 1 and hasattr(self, 'prevlist_button'):
            self.prevlist_button.config(state=tk.NORMAL)
            
        cursor.execute("SELECT * FROM pre_doc_table WHERE id=?", (self.chart_index,))
        results = cursor.fetchall()
        print("update_list_items" + str(results))
        
        # Clear the existing items in the list
        self.list_items.delete(*self.list_items.get_children())
        print("on update_list_items")
        # Loop through the results and add each product to the list
        for result in results:
            # Extract the item information from the database record
            self.chart_index = result[0]
            doc_created_date = result[1]
            doc_expire_date = result[2]
            doc_updated_date = result[3]
            AT_SHOP = result[4]
            user_id = result[5]
            customer_id = result[6]
            type = result[7]
            ITEM = result[8]
            PRICE = result[9]
            Disc = result[10]
            TAX = result[11]
            States = result[12]

            if States != "States":
                self.chart_index += 1
                if self.chart_index == len(results) or self.chart_index < 0:
                    return
                else:
                    self.update_list_items()
            
            # Create a new item using the product information
            # from founded ITEM value fill this info
            items_lists = ITEM.split("|),")
            for items in items_lists:
                item = items.split("|,|")
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
                disc = item[8]
                Disc += float(disc)
                tax = item[9].replace("|)", "")
                TAX += float(tax)
                # Add the item to the list
                print(str([id, code, "", name, shop, color, size, qty, price, disc, tax, total_price]))
                self.list_items.insert("", "end", text=str(id), values=(code, "", name, shop, color, size, qty, price, disc, tax, total_price))
        # Update the totals in the GUI
        #self.update_totals()
        self.update_info()
        
    def next_prev_chart(self, towhere):
        print("in prev func with" + towhere +"\n\n")
        cursor.execute("SELECT * FROM pre_doc_table")
        results = cursor.fetchall()
        if towhere == "next":
            self.chart_index += 1
            if self.chart_index == len(results):
                self.chart_index = 0
        else:
            self.chart_index -= 1
            if self.chart_index < 0:
                self.chart_index = len(results)-1
        print("index : \n" + str(self.chart_index))
        self.update_list_items()
            
    def call_chartForm(self):
        v = ShowchartForm(self)
        self.chart_index = v.value
        print("selected chart : "+ str(v.value))
        self.update_list_items()

    def get_chart(self):
        cursor.execute("SELECT * FROM pre_doc_table WHERE id=?", (self.chart_index,))
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
        self.update_chart()

    def void_items(self):
        for a in self.list_items.get_children():
            self.list_items.delete(a)
        # delete this list on db
        cursor.execute("DELETE FROM pre_doc_table WHERE id=?", (self.chart_index,))
        # Commit the changes to the database
        conn.commit()
        # self.update_info() will be called in next_prev_chart 
        self.next_prev_chart("prev")

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
        buttons = []
        i = -1
        j = -1
        a = 0
        b = 0
        for widget in range(len(self.buttons_frame.winfo_children())-1):
            #print(" button " + str(a) + " , " + str(b))
            j += 1
            if b == 3: 
                b = 0
                a += 1
                continue
            if len(self.buttons_frame.winfo_children())-1 == j+1:
                a += 1
                b = 0
                for row in rows:
                    i += 1
                    if b == 3: 
                        b = 0
                        a += 1
                    tool_name = row[1]
                    # Create a new button
                    new_button = tk.Button(self.buttons_frame, text=tool_name)
                    new_button.configure(command=lambda b=new_button.cget("text"): self.call_payment(b, self.price))
                    new_button.grid(row=a, column=b, sticky="nsew")
                    b += 1
                break
            else:
                b+=1
    
    def call_payment(self, name, price):
        self.pid_peyment.append(str(str(name) + " = " + str(price)))
        print("self.pid_peyment = " + str(self.pid_peyment))
        self.process_payment()

    def process_payment(self):
        print("self.pid_peyment = " + str(self.pid_peyment))
        if len(self.list_items.get_children()) <= 0:
            print("no list")
        else:
            payment_name = []
            payments_ = ""
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
                payments_ += str(rows[0][1]) + " = " + str(p[1])
                payment_name.append([str(rows[0][1]), str(p[1])])
                break

            if payment_enable == 0:
                print("no pyment")
            else:
                print("pyment "+str(payment_enable) + ":" + str(payments_))
                #add to doc table
                #create doc_id
                # 
                # 
                # item [(|item_code|,|item_name|,|item_shop|,|item_color|,
                #        |item_size|,|item_qty|,|item_price|,|item_disc|,|item_tax|),]    
                item = ""
                itemforslip = ""
                price = 0
                disc = 0
                tax = 0
                items = 0
                brcod = 0
                cursor.execute("SELECT * FROM setting WHERE user_name=?", (self.user,))
                b = cursor.fetchone()
                if not len(b)<= 0:
                    brcod = b[2] # getting barcode
                brcod += 1
                print("brcod :" + str(brcod))
                for a in self.list_items.get_children():
                    items += 1
                    print(str(self.list_items.item(a)))
                    i = self.list_items.item(a)
                    iv = i['values']
                    id = i['text']
                    print(str(id))
                    cursor.execute("SELECT * FROM product WHERE id=?", (id,))
                    it = cursor.fetchone()
                    item += "(|"
                    item += str(id) # ID
                    item += "|,|"
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
                    # Code   | Name      | qty | price  | totale |
                    # TODO make equal space
                    v = [7, 10, 3, 8, 8]
                    vv = [str(iv[0]), str(iv[2]), str(iv[6]), str(iv[7]), str(float(iv[6])*float(iv[7]))]
                    print("vv : " + str(vv))
                    vvi = 0
                    for vi in v:
                        for w in range(vi):
                            if w < len(vv[vvi]):
                                print("vv : " + str(vv[vvi])+ " vvi :" + str(vvi) + " w :" + str(w))
                                itemforslip += vv[vvi][w]
                            else:
                                itemforslip += ' '
                        vvi += 1
                        itemforslip += "|"
                    itemforslip += "\n"
                    
                    if items+1 <= len(self.list_items.get_children()):
                        item += "|),"
                    else:
                        item += "|)"
                    print("item1 found : " + str(it[12]))
                    it_info = reduc_qty(str(it[12]), str(iv[3]), str(iv[4]),str(iv[5]), str(iv[6]))
                    print("item2 found : " + str(it_info))
                    cursor.execute('UPDATE product SET more_info=? WHERE id=?', (it_info, id))
                    
                    cursor.execute("SELECT * FROM product WHERE id=?", (id,))
                    it2 = cursor.fetchone()
                    
                    print("item2 found : " + str(it2[12]))
                    # Commit the changes to the database
                    conn.commit()
                
                cursor.execute('UPDATE setting SET barcode_count=? WHERE user_name=?', (brcod, self.user))
                    
                # Commit the changes to the database
                conn.commit()

                cursor.execute('INSERT INTO upload_doc (doc_barcode, extension_barcode, user_id, customer_id, type, item, qty, price, discount, tax, payments, doc_created_date, doc_expire_date, doc_updated_date) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', ("23-200-" + str(brcod), "extension_barcode", self.user, self.custemr, "Sale_item", item, float(items), price, disc, tax, payments_, "doc_created_date", "doc_expire_date", "doc_updated_date"))
                cursor.execute('INSERT INTO doc_table (doc_barcode, extension_barcode, user_id, customer_id, type, item, qty, price, discount, tax, payments, doc_created_date, doc_expire_date, doc_updated_date) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', ("23-200-" + str(brcod), "extension_barcode", self.user, self.custemr, "Sale_item", item, float(items), price, disc, tax, payments_, "doc_created_date", "doc_expire_date", "doc_updated_date"))
                
                # Commit the changes to the database
                conn.commit()
                
                print(str(["23-200-" + str(brcod), "extension_barcode", self.user, "customer_id", "type", item, disc, tax, payments_, "doc_created_date", "doc_expire_date", "doc_updated_date"]))
                
                print("pyment sitting equal :" + str([payment_name, payment_quick_pay, payment_customer_required, payment_print_slip, 
                                                      payment_change_allowed, payment_mark_pad, payment_open_drower]))

                brd = "23-200-" + str(brcod)
                # TODO create function that generate slipe text logo image
                slip = "-----------------------------------------\n" \
                       "Receipt No : " + brd + "\n"\
                       "extnsion Receipt No : extension_barcode\n"\
                       "Date : doc_created_date\n"\
                       "updated Date : doc_updated_date\n"\
                       "Due Date : doc_expire_date\n"\
                       "-----------------------------------------\n" \
                       "User : " + str(self.user) + "\n"\
                       "Customer : Customer Name\n"\
                       "Phone No : Phone Number\n"\
                       "-----------------------------------------\n" \
                       "Code   |Name      |qty| price  |totale  |\n" \
                       + itemforslip + \
                       "-----------------------------------------\n" \
                       "Item Counted    : " + str(items) + "\n"\
                       "Total Discount  : " + str(disc) + "\n"\
                       "Total Tax       : " + str(tax) + "\n"\
                       + str(payments_) + "\n" \
                       "=========================================\n" \
                       "Total price     : " + str(price) + "\n"\
                       "Total Paid      : " + str(price) + "\n"\
                       "Total Laft      : " + str(0) + "\n"\
                       "=========================================\n" \
                       "          " + str(brd) + "       \n"
                
                
                # payment_type :: (1id , 2name TEXT, 3code TEXT, 4type TEXT, 5short_key TEXT, 6acsess TEXT,
                # 7enabel INTEGER, 8quick_pay INTEGER, 9customer_required INTEGER, 10printslip REAL, 
                # 11change_allowed REAL, 12markpad REAL, 13open_drower REAL
                if payment_open_drower == 1:
                    PrinterForm.open_drower(self)
                    
                for name in payment_name:
                    ApproveFrame(self, self.list_items, slip, payment_print_slip, self.user)
                    
                for child in self.list_items.get_children():
                    print("pymrnt!!!!!", str(child))
                # call void         
                self.void_items()
        
