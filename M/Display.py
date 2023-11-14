import tkinter as tk
from tkinter import ttk
import sqlite3
import shutil
import datetime
import os
import atexit
import sys
<<<<<<< HEAD
=======
import random

>>>>>>> db9ae79 (adding seller)
current_dir = os.path.abspath(os.path.dirname(__file__))
MAIN_dir = os.path.join(current_dir, '..')
sys.path.append(MAIN_dir)
from D.ChooseCustemr import UserManagementApp
<<<<<<< HEAD
=======
from D.ChooseWorker import WorkerManagementApp
>>>>>>> db9ae79 (adding seller)
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
from C.slipe import load_slip
<<<<<<< HEAD
=======
from D.Doc.Loaddoc import *
from C.List import *
>>>>>>> db9ae79 (adding seller)

from Manager import ManageForm

data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data'))
db_path = os.path.join(data_dir, 'my_database.db')
conn = sqlite3.connect(db_path)
cursor = conn.cursor()


class DisplayFrame(tk.Frame):
    def __init__(self, master, user):
        tk.Frame.__init__(self, master)
        self.user = user
<<<<<<< HEAD
=======
        print("Disktop user : " + str(self.user))
>>>>>>> db9ae79 (adding seller)
        self.custemr = ""
        self.chart_index = 0
        self.price = 0
        self.pid = 0
        self.pid_peyment = []
<<<<<<< HEAD
        self.items = []
=======
        self.ex_pid_peyment = []
        self.items = []
        self.ex_items = []
>>>>>>> db9ae79 (adding seller)
        self.tax = 0
        self.qty = 0
        self.disc = 0
        self.total = 0
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        self.main_Notebook = ttk.Notebook(self)
        self.main_Notebook.pack(side="top", fill="both", expand=True)

<<<<<<< HEAD
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

=======
>>>>>>> db9ae79 (adding seller)
        self.main_frame = tk.Frame(self.main_Notebook, bg="black")
        self.main_frame.grid()
        self.main_Notebook.add(self.main_frame, text='HOME')
        
        # Set the grid configuration for buttons_frame
        self.main_frame.columnconfigure((0, 1), weight=1)
        self.main_frame.columnconfigure(1, weight=0)
        self.main_frame.rowconfigure(0, weight=0)
        self.main_frame.rowconfigure(1, weight=2)
<<<<<<< HEAD


        # create the second frame and add it to the container
        self.manage_form = ManageForm(self.main_Notebook)
=======
        self.main_frame.rowconfigure(2, weight=0)


        # create the second frame and add it to the container
        self.manage_form = ManageForm(self.main_Notebook, self.user)
>>>>>>> db9ae79 (adding seller)
        self.manage_form.pack(side="top", fill="both", expand=True)
        self.main_Notebook.add(self.manage_form, text='MANAGE')
        #self.manage_form.grid(row=0, column=0, sticky="nsew")

        #self.frames["ManageFrame"] = manage_form

        # * New frame at the top of the main frame
<<<<<<< HEAD
        self.top_frame = tk.Frame(self.main_frame, bg="red", height=int(screen_height * 0.70))
=======
        self.top_frame = tk.Frame(self.main_frame, height=int(screen_height * 0.70))
>>>>>>> db9ae79 (adding seller)
        self.top_frame.grid(row=0, column=0, columnspan=2, sticky="nsew")
        # Set the grid configuration for buttons_frame
        self.top_frame.columnconfigure((0), weight=0)
        self.top_frame.columnconfigure((5), weight=1)
        self.top_frame.rowconfigure((0), weight=1)

        # Create a label and an entry widget for the search box
<<<<<<< HEAD
        self.search_label = tk.Label(self.top_frame, text="Search:", bg="red", fg="white", font=("Arial", 12))
=======
        self.search_label = tk.Label(self.top_frame, text="Search:", font=("Arial", 12))
>>>>>>> db9ae79 (adding seller)
        self.search_label.grid(row=0, column=0, sticky="nsew")
        print("screen_width :: " + str((self.top_frame.winfo_width())) + " = " + str((screen_width/3)))
        self.search_entry = search_entry(self.top_frame, font=("Arial", 12))
        #tk.Entry
        self.search_entry.grid(row=0, column=5, columnspan=4, sticky="nsew")

        # * New frame next to list_items in the main frame
<<<<<<< HEAD
        self.midel_frame = tk.Frame(self.main_frame, bg="blue")
        self.midel_frame.grid(row=1, column=0, sticky="nsew")

        # New listbox in the main frame
        self.list_items = ttk.Treeview(self.midel_frame, columns=("CODE", "BARCODE", "ITEM Name", "AT SHOP", "COLOR", "SIZE", "QTY", "PRICE", "DISCOUNT", "TAX", "TOTAL PRICE"))
=======
        self.midel_frame = tk.Frame(self.main_frame)
        self.midel_frame.grid(row=1, column=0, sticky="nsew")
        
        self.extrnal_frame = tk.Frame(self.midel_frame, height=int(screen_height * 0.050))
        self.extrnal_frame.pack(side="top", fill="x")
        
        # New listbox in the main frame
        self.list_items = ttk.Treeview(self.midel_frame, columns=("CODE", "BARCODE", "ITEM Name", "QTY", "PRICE", "DISCOUNT", "TAX", "TOTAL PRICE", "COLOR", "SIZE", "AT SHOP", "Extantion Barcode"))
>>>>>>> db9ae79 (adding seller)
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
<<<<<<< HEAD
        self.list_items.column("#0", stretch=tk.NO, minwidth=25, width=100)   
=======
        self.list_items.column("#0", stretch=tk.NO, minwidth=0, width=0)   
>>>>>>> db9ae79 (adding seller)
        self.list_items.heading("#1", text="CODE", anchor=tk.W)
        self.list_items.column("#1", stretch=tk.NO, minwidth=25, width=50)
        self.list_items.heading("#2", text="BARCODE", anchor=tk.W)
        self.list_items.column("#2", stretch=tk.NO, minwidth=25, width=100)
        self.list_items.heading("#3", text="ITEM Name", anchor=tk.W)
        self.list_items.column("#3", stretch=tk.NO, minwidth=25, width=125)
<<<<<<< HEAD
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
=======
        self.list_items.heading("#4", text="COLOR", anchor=tk.W)
        self.list_items.column("#4", stretch=tk.NO, minwidth=25, width=100)
        self.list_items.heading("#5", text="SIZE", anchor=tk.W)
        self.list_items.column("#5", stretch=tk.NO, minwidth=25, width=50)
        self.list_items.heading("#6", text="QTY", anchor=tk.W)
        self.list_items.column("#6", stretch=tk.NO, minwidth=25, width=50)
        self.list_items.heading("#7", text="PRICE", anchor=tk.W)
        self.list_items.column("#7", stretch=tk.NO, minwidth=25, width=50)
        self.list_items.heading("#8", text="DISCOUNT", anchor=tk.W)
        self.list_items.column("#8", stretch=tk.NO, minwidth=25, width=50)
        self.list_items.heading("#9", text="TAX", anchor=tk.W)
        self.list_items.column("#9", stretch=tk.NO, minwidth=25, width=50)
        self.list_items.heading("#10", text="TOTAL PRICE", anchor=tk.W)
        self.list_items.column("#10", stretch=tk.NO, minwidth=25, width=100)
        self.list_items.heading("#11", text="AT SHOP", anchor=tk.W)
        self.list_items.column("#11", stretch=tk.NO, minwidth=25, width=50)
        self.list_items.heading("#12", text="Extantion Barcode", anchor=tk.W)
        self.list_items.column("#12", stretch=tk.NO, minwidth=25, width=100)     
        
        
        self.total_frame = tk.Frame(self.main_frame, height=150)
        self.total_frame.grid(row=2, column=0, columnspan=4, sticky="nsew")
        #self.total_frame.pack(side="top", fill="both")

        # Set the top and bottom frames to fill the available space horizontally
        #self.total_frame.pack(side="top")
        #self.list_items.pack(side="top", fill="both")

        # Create labels on the right side of total_frame
        self.total_items_label = tk.Label(self.total_frame, text="Total Items : 0", font=("Arial", 13))
        self.total_items_label.pack(side="left", padx=5)
        self.total_tax_label = tk.Label(self.total_frame, text="Total Tax : 0", font=("Arial", 13))
        self.total_tax_label.pack(side="left", padx=5)
        self.total_discount_label = tk.Label(self.total_frame, text="Item Discount : 0", font=("Arial", 13))
        self.total_discount_label.pack(side="left", padx=5)
        self.total_tdiscount_label = tk.Label(self.total_frame, text="Total Discount : 0", font=("Arial", 13))
        self.total_tdiscount_label.pack(side="left", padx=5)
        self.total_price_label = tk.Label(self.total_frame, text="Price Befor: 0", font=("Arial", 13))
        self.total_price_label.pack(side="left", padx=5)
        self.total_label = tk.Label(self.total_frame, text="Total After: 0", font=("Arial", 18))
        self.total_label.pack(side="left", padx=5)

        # * New frame next to list_items in the main frame
        self.buttons_frame = tk.Frame(self.main_frame)
        self.buttons_frame.grid(row=1, column=1, rowspan=1, sticky="nsew")
>>>>>>> db9ae79 (adding seller)

        # Set the grid configuration for buttons_frame
        self.buttons_frame.columnconfigure((0, 1, 2, 3), weight=1, minsize=int(self.buttons_frame.winfo_height() *0.1))
        self.buttons_frame.rowconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8, 9), weight=1, minsize=int(self.buttons_frame.winfo_height() *0.1))

        # Create 6 button widgets and add them to buttons_frame
<<<<<<< HEAD
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
=======
        self.del_button = tk.Button(self.buttons_frame, text="Delete X\nDelete", font=("Arial", 12), command=self.remove_item)
        self.del_button.grid(row=0, column=0, sticky="nsew")
        self.master.bind("<Delete>", lambda _: self.remove_item())
        
        self.voidlist_button = tk.Button(self.buttons_frame, text="Void\nF2", font=("Arial", 12), command=self.void_items)
        self.voidlist_button.grid(row=0, column=1, sticky="nsew")
        self.master.bind("<F2>", lambda _: self.void_items())
        self.qty_button = tk.Button(self.buttons_frame, text="Qty\nF3", font=("Arial", 12), command=self.make_qty)
        self.qty_button.grid(row=0, column=2, sticky="nsew")
        self.master.bind("<F3>", lambda _: self.make_qty())
        self.discount_button = tk.Button(self.buttons_frame, text="Discount\nF4", font=("Arial", 12), command=self.make_dicount)
        self.discount_button.grid(row=0, column=3, sticky="nsew")
        self.master.bind("<F4>", lambda _: self.make_dicount())
        self.prevlist_button = tk.Button(self.buttons_frame, text="Prev\nF5", font=("Arial", 12), command=lambda: self.next_prev_chart("prev"))
        self.prevlist_button.grid(row=1, column=0, sticky="nsew")
        self.prevlist_button.config(state=tk.DISABLED)
        self.master.bind("<F5>", lambda _: self.next_prev_chart("prev"))
        self.activets_button = tk.Button(self.buttons_frame, text="Activets\nF6", font=("Arial", 12), command=self.call_chartForm)
        self.activets_button.grid(row=1, column=1, sticky="nsew")
        self.master.bind("<F6>", lambda _: self.call_chartForm())
        self.newlist_button = tk.Button(self.buttons_frame, text="New\nF7", font=("Arial", 12), command=self.new_chart)
        self.newlist_button.grid(row=1, column=2, sticky="nsew")
        self.master.bind("<F7>", lambda _: self.new_chart())
        self.update_button = tk.Button(self.buttons_frame, text="update\nCtrl+U", font=("Arial", 12), command=lambda: UploadingForm(self))
        self.update_button.grid(row=1, column=3, sticky="nsew")
        #self.master.bind("<F8>", lambda _: UploadingForm(self))
        self.endday_button = tk.Button(self.buttons_frame, text="Cash Drawer\nCtrl+D", font=("Arial", 12), command=lambda: self.open_drower())
        self.endday_button.grid(row=2, column=0, sticky="nsew")
        self.userinfo_button = tk.Button(self.buttons_frame, text="Userinfo\nCtrl+I", font=("Arial", 12), command=lambda: UserInfoForm(self))
        self.userinfo_button.grid(row=2, column=1, sticky="nsew")
        #self.master.bind("<CtrlI>", lambda _: UserInfoForm(self))
        self.logout_button = tk.Button(self.buttons_frame, text="Logout\nCtrl+L", font=("Arial", 12), command=self.exit)
        self.logout_button.grid(row=2, column=2, sticky="nsew")
        #self.master.bind("<CtrlL>", lambda _: self.exit())
        self.payment_button = tk.Button(self.buttons_frame, text="Payment\nF12", font=("Arial", 12), command=self.call_splitpayment)
        self.payment_button.grid(row=2, column=3, sticky="nsew")
        self.master.bind("<F12>", lambda _: self.call_splitpayment())
>>>>>>> db9ae79 (adding seller)
        # Register the backup function to be called when the application exits
        self.max_backups = 4     
        #self.void_items()
        #ApproveFrame(self, "", "", "", self.user)
        atexit.register(self.backup_database)
        self.create_payment_buttons()
<<<<<<< HEAD
        self.update_info()
        self.update_list_items()
        
=======
        self.update_list_items()
        self.update_info()
        #self.list_items.bind("<KeyPress>", self.change_focus)
        #self.bind("<KeyPress>", self.change_focus)
        #self.bind("<KeyPress>", self.change_focus)
        #self.bind("<KeyPress>", self.change_focus)
        
    def change_focus(self, event):
        self.search_entry.focus_set()
    # about Display control
    def call_manager(self):
        self.master.show_frame("ManageFrame")

    def exit(self):
        self.master.show_frame("LogingFrame")

    def load(self):
        self.master.show_frame("DisplayFrame")
        self.load_setting()
        #ApproveFrame(self, [])
    
>>>>>>> db9ae79 (adding seller)

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
<<<<<<< HEAD
            
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
            ITEM += "(:"
            ITEM += str(id) # id
            ITEM += ":,:"
            ITEM += str(iv[0]) # code
            ITEM += ":,:"
            ITEM += str(iv[2]) # name
            ITEM += ":,:"
            ITEM += str(iv[3]) # shop
            ITEM += ":,:"
            ITEM += str(iv[4]) # color
            ITEM += ":,:"
            ITEM += str(iv[5]) # size
            ITEM += ":,:"
            ITEM += str(iv[6]) # qty
            ITEM += ":,:"
            ITEM += str(iv[7])  # price
            PRICE += float(iv[6])*float(iv[7])
            ITEM += ":,:"
            ITEM += str(iv[8])  # disc
            Disc += float(iv[8])
            ITEM += ":,:"
            ITEM += str(iv[9])  # tax
            TAX += float(iv[9])
            if items+1 <= len(self.list_items.get_children()):
                ITEM += ":),"
            else:
                ITEM += ":)"

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
            items_lists = ITEM.split(":),")
            for items in items_lists:
                item = items.split(":,:")
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

    def chack_list(self):
        total_discount = 0
        total_tax = 0
        total_qty = 0
        all_total_price = 0

        for a in self.list_items.get_children():
            item = self.list_items.item(a)['values']
            print("in update item: " + str(item))

            qty = float(item[6])
            price = float(item[7])
            discount = float(item[8])
            tax = float(item[9])
            total_price = float(item[10])
            
            # Calculate the expected total price based on quantity, price, discount, and tax
            expected_total_price = qty * price - discount + tax
            
            # Update the total price in the item if it doesn't match the expected value
            if total_price != expected_total_price:
                item[10] = expected_total_price
                self.list_items.item(a, values=item)
            
            # Update the price variable
            total_qty += qty
            total_discount += discount
            total_tax += tax
            all_total_price += expected_total_price
        
        return total_qty, total_discount, total_tax, all_total_price

    # this will 
    def update_info(self):
        cursor.execute("SELECT * FROM pre_doc_table WHERE id=?", (self.chart_index,))
        result = cursor.fetchone()

        total_qty, total_discount, total_tax, all_total_price = self.chack_list()
        self.total = (all_total_price - self.tax) - self.disc
        self.total_items_label.config(text="Total Items : " + str(total_qty))
        self.total_tax_label.config(text="Total Tax : " + str(self.tax))
        self.total_discount_label.config(text="Item Discount : " + str(total_discount))
        self.total_tdiscount_label.config(text="Total Discount : " + str(self.disc))
        self.total_price_label.config(text="Price Befor : " + str(all_total_price))
        self.total_label.config(text="Price After: " + str((all_total_price - self.tax) - self.disc))
        self.update_chart()

    def void_items(self):
=======

    # about settings
    def open_drower(self):
        # TODO CHACK IF IT IS LOGED IN AND LOGED IN HAS AUTORITI
        PrinterForm.open_drower(self, self.user)
        
    # loading all setting 
    def load_setting(self):
        cursor.execute("SELECT * FROM setting WHERE User_id=?", (int(self.user[0]),))
        b = cursor.fetchall()
        if len(b) <= 0:
            #print("sitting : " + self.user)
            cursor.execute('INSERT INTO setting (User_id, barcode_count, printer) VALUES (?, ?, ?)', (int(self.user[0]), 0, ""))
            # Commit the changes to the database
            conn.commit()
        else:
            #print("sitting : " + str(b))
            pass
        

    # display buttons profermans
    
                                  
    # void btn
    def clear_items(self):
>>>>>>> db9ae79 (adding seller)
        for a in self.list_items.get_children():
            self.list_items.delete(a)
        # delete all items
        self.pid_peyment = []
<<<<<<< HEAD
        self.custemr = ""
=======
        self.ex_pid_peyment = []
        self.items = []
        self.ex_items = []
        self.custemr = ""
        self.disc = 0
        for it in self.extrnal_frame.winfo_children():
            it.grid_forget()
        
    def void_items(self):
        self.clear_items()
>>>>>>> db9ae79 (adding seller)
        # delete this list on db
        cursor.execute("DELETE FROM pre_doc_table WHERE id=?", (self.chart_index,))
        # Commit the changes to the database
        conn.commit()
        # self.update_info() will be called in next_prev_chart 
        self.next_prev_chart("prev")
<<<<<<< HEAD
        
    def add_item(self, item, barcode, shop_name, color, size, qty):
        self.list_items.insert("", "end", text=str(item[0]), values=(item[2], barcode, item[1], shop_name, color, size, float(qty), item[9], self.disc, item[10],float(qty)*float(item[9])))
    
    def remove_item(self):
        # Function to remove selected items from the list
        for a in self.list_items.selection():
            self.list_items.delete(a)
        self.update_info()

    def make_qty(self):
        # Function to update the quantity of selected items or set the default quantity
        i = GetvalueForm(self)
=======

    # about chart
    def make_qty(self):
        # Function to update the quantity of selected items or set the default quantity
>>>>>>> db9ae79 (adding seller)
        if len(self.list_items.selection()) > 0:
            for a in self.list_items.selection():
                values = self.list_items.item(a)['values']
                
                # Modify the quantity of the item as required
<<<<<<< HEAD
                values[6] = i.value
=======
                i = GetvalueForm(self, values[5], "Change Quantity of " + values[2])
                if not i.value == None and not i.value == "" and i.value > -1:
                    values[5] = i.value
>>>>>>> db9ae79 (adding seller)
                
                # Update the selected item with the modified values
                self.list_items.item(a, values=values)
                print("update qty on item " + str(values))
<<<<<<< HEAD
        elif i:
            self.qty = i.value
            print("update qty " + str(self.qty))
        self.update_info()

    def make_discount(self):
        # Function to update the discount of selected items or set the default discount
        i = None
        if len(self.list_items.get_children()) <= 0:
            print("no list")
        else:
            i = GetvalueForm(self)
        if len(self.list_items.selection()) > 0:
=======
        else:
            i = GetvalueForm(self, self.qty, "Give Quantity")
            if not i.value == None and not i.value == "" and i.value > -1:
                self.qty = i.value
                print("update qty " + str(self.qty))
        self.update_info()

    def make_dicount(self):
        # Function to update the discount of selected items or set the default discount

        if len(self.list_items.get_children()) > 0 and len(self.list_items.selection()) > 0:
>>>>>>> db9ae79 (adding seller)
            for a in self.list_items.selection():
                values = self.list_items.item(a)['values']
                
                # Modify the discount of the item as required
<<<<<<< HEAD
                values[8] = i.value
=======
                i = GetvalueForm(self, values[7], "Give Discount For " + values[2])
                if not i.value == None and not i.value == "" and i.value > -1:
                    values[7] = i.value
>>>>>>> db9ae79 (adding seller)
                
                # Update the selected item with the modified values
                self.list_items.item(a, values=values)
                print("update discount on item " + str(values))
<<<<<<< HEAD
        elif i:
            self.disc = i.value
            print("update discount " + str(self.disc))
=======
        else:
            i = GetvalueForm(self, self.disc, "Give TOTAL Discount")
            if not i.value == None and not i.value == "" and i.value > -1:
                self.disc = i.value
                print("update disc " + str(self.disc))
>>>>>>> db9ae79 (adding seller)
        self.update_info()

    def create_payment_buttons(self):
        # Function to create payment buttons based on tools in the database
        cursor.execute("SELECT * FROM tools")
        rows = cursor.fetchall()
        buttons = []
        i = -1
        j = -1
        a = 0
        b = 0
        for widget in range(len(self.buttons_frame.winfo_children()) - 1):
            j += 1
            if b == 3:
                b = 0
                a += 1
                continue
            if len(self.buttons_frame.winfo_children()) - 1 == j + 1:
                a += 1
                b = 0
                for row in rows:
<<<<<<< HEAD
                    i += 1
                    if b == 3:
=======
                    print("creating row btn = " + str(row[4]))
                    i += 1
                    if b > 3:
>>>>>>> db9ae79 (adding seller)
                        b = 0
                        a += 1
                    tool_name = row[1]
                    # Create a new button
<<<<<<< HEAD
                    new_button = tk.Button(self.buttons_frame, text=tool_name, command=lambda d=tool_name: self.call_payment(d))
=======
                    
                    new_button = tk.Button(self.buttons_frame, text=tool_name+"\nCtrl + "+str(row[4]), command=lambda r=str(row[4]), d=tool_name: self.Q_Payment(r, d))
                    new_button.bind("<Button-3>", lambda d=str(row[4]): self.Q_Payment(d, d.widget["text"].split("\n")[0]))
                    self.master.bind("<KeyPress-" + str(row[4]) + ">", lambda r=str(row[4]), d=tool_name, k=new_button: self.Q_Payment(r, d) if "Control" in str(r)else print(""))
>>>>>>> db9ae79 (adding seller)
                    new_button.grid(row=a, column=b, sticky="nsew")
                    b += 1
                break
            else:
                b += 1
<<<<<<< HEAD

    def call_payment(self, name):
        # Function called when a payment button is clicked
        self.pid_peyment.append([str(name), str(self.total)])
        print("call_payment self.pid_peyment = " + str(self.pid_peyment))
        self.process_payment()
=======
                
    # Function called when a payment button is clicked to make quike payment
    # it will get value from user if price is same to pid or give it will prosess payment
    def Q_Payment(self, event, text):
        print("alt + " + str(text))
        p = 0
        for pid in self.pid_peyment:
            p += float(pid[2])
        i = GetvalueForm(self, str(self.total-p), "Make " + str(text) + " Peyment")
        if i.value > 0:
            self.pid_peyment.append(["1", str(text), str(i.value), ""])
            p += float(i.value)
        if p > 0 and p >= self.total:
            print("call_payment self.pid_peyment = " + str(self.pid_peyment))
            self.process_payment()
>>>>>>> db9ae79 (adding seller)
        
    def remove_item(self):
        for a in self.list_items.selection():
            self.list_items.delete(a)
        self.update_info()

<<<<<<< HEAD
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

    def process_payment(self):
        print("self.pid_peyment = " + str(self.pid_peyment))
        if len(self.list_items.get_children()) <= 0:
            print("no list")
        else:
            date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            payments_ = ""
            payment_enable = 0
            payment_quick_pay = 0
            payment_customer_required = 0
            payment_print_slip = 0
            payment_change_allowed = 0
            payment_mark_pad = 0
            payment_open_drower = 0
            pay_index = 0
            for p in range(len(self.pid_peyment)):
                pay_index += 1
                print("self.pid_peyment[p]:" + str(self.pid_peyment[p]))
                if self.pid_peyment[p][1] == "":
                    break
                cursor.execute("SELECT * FROM tools WHERE name=?", (self.pid_peyment[p][0],))
                rows = cursor.fetchall()
                print("rows:" + str(rows))
                if rows[0][6] == 1: # chack if enabled
                    payment_enable += 1
                if rows[0][7] == 1 and payment_quick_pay == 0: # chack if enabled
                    payment_quick_pay = 1
=======
    # splitpayment btn
    def call_splitpayment(self):
        if len(self.list_items.get_children())  > 0 or len(self.pid_peyment)> 0:
            PaymentForm(self)
        else:
            print("no list")
    
    # about chart btn
    def new_chart(self):
        if len(self.list_items.get_children()) > 0:
            index = 0
            while(True):
                res = cursor.execute(f"SELECT id FROM pre_doc_table WHERE id = {index}").fetchall()
                if not res:
                    break
                else:
                    index += 1
            self.chart_index = index
            self.clear_items()
            self.update_info()
            
    def next_prev_chart(self, towhere):
        print("in prev func with" + towhere +"\n\n")
        cursor.execute("SELECT id FROM pre_doc_table")
        results = cursor.fetchall()
        p = self.chart_index
        l = -1
        n = 0
        i = 0
        print("self.chart_index == : " + str(self.chart_index))
        for r in results:
            if r[0] == self.chart_index:
                if towhere == "next":
                    if not i+1 >= len(results):
                        l = results[i+1][0]
                    else:
                        l = results[0][0]
                    break
                else:
                    if not i-1 < 0:
                        l = results[i-1][0]
                    elif len(results)-1 < 0:
                        l = 0
                    else:
                        l = results[len(results)-1][0]
                    break
            i += 1
        if l == -1:
            if len(results) > 0:
                l = results[0][0]
            else:
                l = self.chart_index
        self.chart_index = l
                    
        self.clear_items()
        print("index : \n" + str(self.chart_index))
        self.update_list_items()
            
    def call_chartForm(self):
        v = ShowchartForm(self)
        if v.value != self.chart_index:
            self.chart_index = v.value
            self.clear_items()
            print("selected chart : "+ str(v.value))
            self.update_list_items()


    # chart
    # this will
    def chack_list(self):
        total_discount = 0
        total_tax = 0
        total_qty = 0
        all_total_price = 0

        for a in self.list_items.get_children():
            item = self.list_items.item(a)['values']
            print("in update item: " + str(item))

            qty = float(item[5])
            price = float(item[6])
            discount = float(item[7])
            tax = float(item[8])
            total_price = float(item[9])
            
            # Calculate the expected total price based on quantity, price, discount, and tax
            expected_total_price = qty * price - discount + tax
            
            # Update the total price in the item if it doesn't match the expected value
            if total_price != expected_total_price:
                item[9] = expected_total_price
                self.list_items.item(a, values=item)
            
            # Update the price variable
            total_qty += qty
            total_discount += discount
            total_tax += tax
            all_total_price += expected_total_price
        
        return total_qty, total_discount, total_tax, all_total_price
    
    def update_info(self):
        total_qty, total_discount, total_tax, all_total_price = self.chack_list()
        self.total = (all_total_price - self.tax) - self.disc
        self.total_items_label.config(text="Total Items : " + str(total_qty))
        self.total_tax_label.config(text="Total Tax : " + str(self.tax))
        self.total_discount_label.config(text="Item Discount : " + str(total_discount))
        self.total_tdiscount_label.config(text="Total Discount : " + str(self.disc))
        self.total_price_label.config(text="Price Befor : " + str(all_total_price))
        self.total_label.config(text="Price After: " + str((all_total_price - self.tax) - self.disc))
        self.update_chart()

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
        ex_item = ""
        ex_pay = ""
        
        for ex in self.ex_items:
            ex_item += str(ex) + ","
        for ex in self.ex_pid_peyment:
            ex_pay += str(ex) + ","
        
        items = 0
        for a in self.list_items.get_children():
            items += 1
            print("CHART ITEM FOUND : " + str(self.list_items.item(a)))
            i = self.list_items.item(a)
            iv = i['values']
            id = i['text']
            if len(iv) == 12 and  iv[11] != "":
                continue
            if ITEM != "":
                ITEM += ","
            ITEM += "(:"
            ITEM += str(id) # id
            ITEM += ":,:"
            ITEM += str(iv[0]) # code
            ITEM += ":,:"
            ITEM += str(iv[2]) # name
            ITEM += ":,:"
            ITEM += str(iv[10]) # shop
            ITEM += ":,:"
            ITEM += str(iv[3]) # color
            ITEM += ":,:"
            ITEM += str(iv[4]) # size
            ITEM += ":,:"
            ITEM += str(iv[5]) # qty
            ITEM += ":,:"
            ITEM += str(iv[6])  # price
            PRICE += float(iv[5])*float(iv[6])
            ITEM += ":,:"
            ITEM += str(iv[7])  # disc
            Disc += float(iv[7])
            ITEM += ":,:"
            ITEM += str(iv[8])  # tax
            TAX += float(iv[8])
            ITEM += ":)"

        if items > 0 or ex_item != "" or ex_pay != "":
            # Define the query to check if the ID exists in the table
            query = f"SELECT id FROM pre_doc_table WHERE id = {self.chart_index}"

            # Execute the query and fetch the results
            cursor.execute(query)
            result = cursor.fetchone()
            # Check if the query returned a result
            if result is not None:
                print(str([doc_created_date, doc_expire_date, doc_updated_date, AT_SHOP, user_id, customer_id, type, ITEM, PRICE, Disc, TAX, States, ex_item, ex_pay]))
                # Insert the new product into the database
                cursor.execute('UPDATE pre_doc_table SET doc_created_date=?, doc_expire_date=?, doc_updated_date=?, AT_SHOP=?, user_id=?, customer_id=?, type=?, ITEM=?, PRICE=?, Disc=?, TAX=?, States=?, exitems_doc_barcode=?, expayment_doc_barcode=? WHERE id=?', (doc_created_date, doc_expire_date, doc_updated_date, AT_SHOP, user_id, customer_id, type, ITEM, float(PRICE), float(Disc), float(TAX), States, ex_item, ex_pay, self.chart_index))

                print(f"Record with ID {self.chart_index} has been UPDATE into the table\n\n1\n\n")                
                print(str([doc_created_date, doc_expire_date, doc_updated_date, AT_SHOP, user_id, customer_id, type, ITEM, float(PRICE), float(Disc), float(TAX), States, self.chart_index, ex_item, ex_pay]))
            else:
                print(f"Record with ID {self.chart_index} does not exist in the table\n\n2\n\n")
                print(str([doc_created_date, doc_expire_date, doc_updated_date, AT_SHOP, user_id, customer_id, type, ITEM, PRICE, Disc, TAX, States, ex_item, ex_pay]))
                # Insert the new product into the database
                cursor.execute('INSERT INTO pre_doc_table (id, doc_created_date, doc_expire_date, doc_updated_date, AT_SHOP, user_id, customer_id, type, ITEM, PRICE, Disc, TAX, States, exitems_doc_barcode, expayment_doc_barcode) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (self.chart_index, doc_created_date, doc_expire_date, doc_updated_date, AT_SHOP, user_id, customer_id, type, ITEM, float(PRICE), float(Disc), float(TAX), States, ex_item, ex_pay))

                print(str(["doc_barcode", "extension_barcode", "user_id", "customer_id", "type", ITEM, Disc, TAX, "doc_created_date", "doc_expire_date", "doc_updated_date", ex_item, ex_pay]))
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
        # Loop through the results and add each product to the list
        self.list_items.delete(*self.list_items.get_children())
        for result in results:
            self.pid_peyment = []
            self.ex_pid_peyment = []
            self.items = []
            self.ex_items = []
            
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
            ex_item = result[13]
            ex_pay = result[14]
            
            if States != "States":
                self.chart_index += 1
                if self.chart_index == len(results) or self.chart_index < 0:
                    return
                else:
                    self.update_list_items()
            
            # Create a new item using the product information
            # from founded ITEM value fill this info
            items_lists = ITEM.split(":),")
            print("on update_list_items"+str(items_lists))
            for items in items_lists:
                item = items.split(":,:")
                if len(item) > 3:
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
                    ex_bar = ""
                    if len(item) > 10:
                        ex_bar = item[10].replace(":)", "")
                    # Add the item to the list
                    print(str([id, code, "", name, shop, color, size, qty, price, disc, tax, total_price]))
                    self.list_items.insert("", "end", text=str(id), values=(code, "", name, color, size, qty, price, disc, tax, total_price, shop, ex_bar))
            
        
            exs = ex_item.split(",")
            if exs != ex_item:
                for ex in exs:
                    self.get_ex_doc_items(ex)

            exs = ex_pay.split(",")
            if exs != ex_pay:
                for ex in exs:
                    self.get_ex_doc_payments(ex)
 
        # Update the totals in the GUI
        #self.update_totals()
        self.update_info()
        
    def get_ex_doc_items(self, doc_barcode):
        cursor.execute("SELECT * FROM doc_table WHERE doc_barcode=?", (doc_barcode,))
        result = cursor.fetchone()
        search_type = "DOCUMENT"
        if result:
            a = load_items(result[6])
            #print("info : " + str(result))
            #print("ret : " + str(result[11]))
            self.add_item(a, result, "DOCUMENT", result[1], "", "", "","", "")
            self.qty = 0
            
    def get_ex_doc_payments(self, doc_barcode):
        cursor.execute("SELECT * FROM doc_table WHERE doc_barcode=?", (doc_barcode,))
        result = cursor.fetchone()
        search_type = "DOCUMENT"
        if result:
            b = load_payment(result[11])
            #print("info : " + str(result[11]))
            #print("ret : " + str(b))
            self.add_payment(b, result, "DOCUMENT", result[1])
            self.qty = 0

    def add_item(self, items, doc, selected_type, barcode, shop_name, code, color, size, qty):
        if (selected_type == "ITEM"):
            self.list_items.insert("", "end", text=str(items[0]), values=(code, barcode, items[1], color, size, float(qty), items[9], self.disc, items[10], float(qty)*float(items[9]), shop_name, ""))
            self.disc = 0
        if (selected_type == "DOCUMENT"):
            if not barcode in self.ex_items:
                self.ex_items.append(barcode)
                ch = len(self.extrnal_frame.winfo_children())

                ex_bar_frame = tk.Frame(self.extrnal_frame, bg="green")
                ex_bar_frame.grid(row=0, column=ch, sticky="nsew")
                search_label = tk.Label(ex_bar_frame, text=barcode, bg="green", fg="white", font=("Arial", 12))
                search_label.grid(row=0, column=0, sticky="nsew")
                    
                update_button = tk.Button(ex_bar_frame, text="X", bg="red", fg="white", font=("Arial", 12), command=lambda: self.remove_ex_items(ex_bar_frame, search_label))
                update_button.grid(row=0, column=1, sticky="nsew")
                
            for item in items:                
                #list_itemss.append([ code, "", name, color, size, qty7, price, total_price, PRICE, disc, Disc, tax, TAX, shop]
                self.list_items.insert("", "end", text=str(item[0]), values=(item[1], item[2], item[3], item[5], item[6], item[7], item[8], item[11], item[12],item[9], item[4], barcode))
                
    def remove_ex_items(self, ex_bar_frame, search_label):
        for items in self.list_items.get_children():
            values = self.list_items.item(items)['values']
            if len(values) != 12:
                continue
            if str(values[11]) == search_label.cget("text"):
                self.list_items.delete(items)
        for ex in self.ex_items:
            if str(ex) == search_label.cget("text"):
                self.ex_items.remove(ex)
                ex_bar_frame.grid_forget()
                self.update_info()
                break
        
    def add_payment(self, items, doc, selected_type, barcode):
        if not barcode in self.ex_pid_peyment:
            self.ex_pid_peyment.append(barcode)
        if (selected_type == "DOCUMENT"):
            for item in items:
                if len(item) == 6:   
                    item.append(1)
                if len(item) == 7:
                    item.append(barcode)
                self.pid_peyment.append(item)
        print("add_payment self.pid_peyment = " + str(self.pid_peyment))
    
    def remove_item(self):
        # Function to remove selected items from the list
        for a in self.list_items.selection():
            self.list_items.delete(a)
        self.update_info()

    # about payment
    def process_payment(self):
        print("user "+str(self.user))
        f_user_s = cursor.execute("SELECT * FROM setting WHERE User_id=?", (int(self.user[0]),)).fetchall()
        print("f_user_s "+str(f_user_s))
        Seller_id = None
        if f_user_s and f_user_s[0] and f_user_s[0][5]:
            print("opning worker dialog")
            app = WorkerManagementApp(self)
            '''if app.user_details:
                self.custemr = app.user_details['User_id']
                cm_id = self.custemr'''
        '''if sittings:
            #print("sitting2 : " + str(sittings))
            for sitting in sittings:
                if sitting[1] == self.user[3]:
                    self.load_type_info(sitting[4])'''
        
        
        # GET COPY OF ALL GIVEN INFO
        list_items_copy = ttk.Treeview(self.midel_frame, columns=("CODE", "BARCODE", "ITEM Name", "QTY", "PRICE", "DISCOUNT", "TAX", "TOTAL PRICE", "COLOR", "SIZE", "AT SHOP", "Extantion Barcode"))
        for a in self.list_items.get_children():
            items = self.list_items.item(a)
            list_items_copy.insert("", "end", text=items['text'], values= items['values'])

        
        date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        payments_ = ""
        
        payments_extra = []
        extra_payment_needs = []
        
        payment_item_required = 0
        payment_open_drower = 0
        payment_print_slip = 1
        payment_customer_required = 0
        
        payment_enable = 0
        
        payment_change_allowed = 0
        payment_mark_pad = 0
        pay_index = 0
        #self.get_ex_doc_items(ex)
        #self.get_ex_doc_payments(ex)
        itemforslip = ""
        item_tobechanged = []
        item = "" # item found
        items = 0 # itme counted
        price = 0 # new items price
        pid = 0   # for new items pid
        T_pid = 0 # for all pid 
        def_pid = 0# for cash with no item pid or credit
        disc = 0  # for new items disc
        T_disc = 0  # for total new items dics
        tax = 0  # tax
        T_tax = 0  # tax 
        change = 0
        
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
        
        print("brcod :" + str(brcod))
        print("count sold items :" + str(len(list_items_copy.get_children())))
        print("sold items :" + str(list_items_copy.get_children()))
        for a in list_items_copy.get_children():
            i = list_items_copy.item(a)
            print(str(list_items_copy.item(a)))
            iv = i['values']
            id = i['text']
            print("self.ex_items :" + str(self.ex_items))
            print("iv[11] :" + str(iv[11]))
            print("len(iv) :" + str(len(iv)))
            if len(iv) >= 12 and str(iv[11]) != "" and str(iv[11]) in self.ex_items:
                continue
            if item != "":
                item += ":),"
            items += 1
            print(str(id))
            cursor.execute("SELECT * FROM product WHERE id=?", (id,))
            it = cursor.fetchone()
            item += "(:"
            item += str(id) # ID
            item += ":,:"
            item += str(iv[0]) # code
            item += ":,:"
            item += str(iv[1]) # barcode
            item += ":,:"
            item += str(iv[2]) # name
            item += ":,:"
            item += str(iv[10]) # shop
            item += ":,:"
            item += str(iv[3]) # color
            item += ":,:"
            item += str(iv[4]) # size
            item += ":,:"
            item += str(iv[5]) # qty
            item += ":,:"
            item += str(iv[6])  # price
            price += float(iv[5])*float(iv[6])
            item += ":,:"
            item += str(iv[7])  # disc
            disc += float(iv[7])
            item += ":,:"
            item += str(iv[8])  # tax
            tax += float(iv[8])
            item += ":)"
            print("adding " + str(iv[5]) + " to item_tobechanged")
            item_tobechanged.append([id, str(it[12]), 0, str(iv[10]), str(iv[0]), str(iv[3]),str(iv[4]), str(iv[5])])            
            list_items_copy.delete(a)
        p = 0

        print("\n\n sold items collect :" + str(item)+"\n\n")
        
        while p < len(self.pid_peyment):
            print("self.pid_peyment:" + str(self.pid_peyment))
            print("self.ex_pid_peyment:" + str(self.ex_pid_peyment))
            print("self.pid_peyment[p]:" + str(self.pid_peyment[p]))
            if self.pid_peyment[p][1] == "" or len(self.pid_peyment[p]) >= 8 and self.pid_peyment[p][7] in self.ex_pid_peyment:
                p += 1
                continue
            pay_index += 1
            print("self.pid_peyment[p]:" + str(self.pid_peyment[p]))
            rows = cursor.execute("SELECT * FROM tools WHERE name=?", (self.pid_peyment[p][1],)).fetchall()
            if rows:
                print("rows:" + str(rows))
                print("price-disc "+str(price-disc) + ":pid " + str(pid) + ":def_pid " + str(def_pid))
                c = float(self.pid_peyment[p][2])
                print("c:" + str(c))
                if rows[0][6] == 1: # chack if enabled
                    payment_enable += 1
                if rows[0][7] == 1 and payment_item_required == 0: # chack if enabled
                    payment_item_required = 1
>>>>>>> db9ae79 (adding seller)
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
<<<<<<< HEAD
                payments_ += "(" + str(pay_index) + "," + str(self.pid_peyment[p][0]) + "," +  str(self.pid_peyment[p][1]) + "," + date + "," + date + "," + self.user + "),"
                
            if payment_enable == 0:
                print("no pyment")
            else:
                print("pyment "+str(payment_enable) + ":" + str(payments_))
                #add to doc table
                #create doc_id
                # 
                # 
                # item [(:item_code:,:item_name:,:item_shop:,:item_color:,
                #        :item_size:,:item_qty:,:item_price:,:item_disc:,:item_tax:),]    
                
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
                    print("item1 found : " + str(it[12]))
                    it_info = reduc_qty(str(it[12]), 0, str(iv[3]), str(iv[4]),str(iv[5]), str(iv[6]))
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
                
                
                print("custemer : " + str(self.custemr) + "isneded : " + str(payment_customer_required))
                name = ""
                phone_num = ""
                if payment_customer_required:
                    app = UserManagementApp(self)

                    if app.user_details:
                        self.custemr = app.user_details['id']
                        name = app.user_details['name']
                        phone_num = app.user_details['phone_num']
                        print(app.user_details)

                
                cursor.execute('INSERT INTO upload_doc (doc_barcode, extension_barcode, user_id, customer_id, type, item, qty, price, discount, tax, payments, doc_created_date, doc_expire_date, doc_updated_date) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', ("23-200-" + str(brcod), "extension_barcode", self.user, self.custemr, "Sale_item", item, float(items), price, disc, tax, payments_, date, "doc_expire_date", date))
                cursor.execute('INSERT INTO doc_table (doc_barcode, extension_barcode, user_id, customer_id, type, item, qty, price, discount, tax, payments, doc_created_date, doc_expire_date, doc_updated_date) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', ("23-200-" + str(brcod), "extension_barcode", self.user, self.custemr, "Sale_item", item, float(items), price, disc, tax, payments_, date, "doc_expire_date", date))
                
                # Commit the changes to the database
                conn.commit()
                slip0 = ["23-200-" + str(brcod), "extension_barcode", self.user, self.custemr, "Sale_item", item, float(items), price, disc, tax, payments_, date, "doc_expire_date", date]
                print(str(slip0))
                slip1 = load_slip(slip0, 0) #TODO GET ID
                print(str(slip1))
                print("pyment sitting equal :" + str([payments_, payment_quick_pay, payment_customer_required, payment_print_slip, 
                                                      payment_change_allowed, payment_mark_pad, payment_open_drower]))
                
                if payment_open_drower == 1:
                    PrinterForm.open_drower(self)
                
                ApproveFrame(self, self.list_items, slip1, payment_print_slip, self.user)
                    
                # call void         
                self.void_items()
        
=======
                if not rows[0][7]:
                    price += c
                    def_pid += c
                    
                if price-disc == pid:
                    payments_extra.append([str(pay_index), str(self.pid_peyment[p][1]), str(self.pid_peyment[p][2]), date, date, self.user[3], str(rows[0][11]), str(self.pid_peyment[p][3])])
                else:
                    if pid + c > price-disc:
                        pr = (price-disc) # item price
                        pl = pr-pid     # price left to pay
                        if c > pl:
                            e = c - pl
                            payments_extra.append([str(pay_index), str(self.pid_peyment[p][1]), str(e), date, date, self.user[3], str(rows[0][11]), str(self.pid_peyment[p][3])])
                            c = pl # taking only what pied
                        else:
                            c = pl
                    if rows[0][7]:
                        print("pid+c ")
                        T_pid += float(self.pid_peyment[p][2])
                        pid += c
                    payments_ += "(" + str(pay_index) + "," + str(self.pid_peyment[p][1]) + "," +  str(c) + "," + date + "," + date + "," + self.user[3] + "," + str(rows[0][11]) + "," + str(self.pid_peyment[p][3]) + "),"
                self.pid_peyment.remove(self.pid_peyment[p])
            elif p+1 < len(self.pid_peyment):
                p += 1

        print("\n\n payments_ pid collect :" + str(payments_)+"\n\n")
        
        print("--payments_extra : " + str(payments_extra))
        print("count ex_items items :" + str(len(list_items_copy.get_children())))
        for ex_i in self.ex_items:
            ex_doc = cursor.execute("SELECT * FROM doc_table WHERE doc_barcode=?", (ex_i,)).fetchone()
            if ex_doc:
                ex_item_list = load_items(ex_doc[6])
                ite = "" # item found
                ex_item_count = 0 # itme counted
                ex_T_price = 0 # new items price
                ex_T_pid = 0   # for new items pid
                ex_T_disc = 0  # for total new items dics
                ex_T_tax = 0  # tax 
                print("ex_item_list : " + str(ex_item_list))
                iti = 0
                while(iti < len(ex_item_list)):
                    itf = 0 # IF IT VALUE TO DELET OR NOT
                    it = ex_item_list[iti]
                    print("ex_it : " + str(it))
                    ex_tax = 0  # tax
                    ex_disc = 0  # for new items disc
                    for a in list_items_copy.get_children():
                        print(str(id))
                        i = list_items_copy.item(a)
                        iv = i['values']
                        id = i['text']
                        print("comparring id "+str(id)+" and it[0] " + str(it[0]))
                        if iv[11] == ex_i and id == it[0]:
                            print("item is same " + str(list_items_copy.item(a)))
                            ex_item_count += 1
                           
                            p_it = cursor.execute("SELECT * FROM product WHERE id=?", (id,)).fetchone()
                            q = None
                            print("searching item in product "+str(id))
                            if p_it:
                                if ite != "":
                                    ite += ","
                                ite += "(:"
                                ite += str(id) # ID
                                ite += ":,:"
                                ite += str(iv[0]) # code
                                ite += ":,:"
                                ite += str(iv[1]) # barcode
                                ite += ":,:"
                                ite += str(iv[2]) # name
                                ite += ":,:"
                                ite += str(iv[10]) # shop
                                ite += ":,:"
                                ite += str(iv[3]) # color
                                ite += ":,:"
                                ite += str(iv[4]) # size
                                ite += ":,:"
                                ite += str(iv[5]) # qty
                                ite += ":,:"
                                ite += str(iv[6])  # price
                                ex_T_price += float(iv[5])*float(iv[6])
                                ite += ":,:"
                                ite += str(iv[7])  # disc
                                ex_T_disc += float(iv[7])
                                ite += ":,:"
                                ite += str(iv[8])  # tax
                                ex_T_tax += float(iv[8])
                                ite += ":)"
                                
                                print("item info :" + str(iv))
                                q = float(it[7]) - float(iv[5]) if float(it[7]) < float(iv[5]) else float(iv[5]) - float(it[7])
                                
                            if q != 0 and q != None:
                                print("2adding " + str(iv[5]) + " to item_tobechanged")
                                print("len :" + str(q))
                                item_tobechanged.append([id, str(p_it[12]), 1, str(iv[10]), str(iv[0]), str(iv[3]),str(iv[4]), str(q)]) 
                            list_items_copy.delete(a)
                            itf = 1 # remove founded item
                    if(itf == 1):
                        ex_item_list.remove(it)
                    else:
                        iti += 1
                ex_docs_info.append([ex_i, 1, 0, ite, ex_item_count, "", 0, ex_T_price, ex_T_disc, ex_T_tax, 0])
                # THIS WILL TALL TO REMOVE REDUSDE ITEMS FROM DOC IF NOT MANTIOND IN THE NEW ONE
                if len(ex_item_list) > 0:
                    for it in ex_item_list:
                        print("left ex_it : " + str([it[1], it[3]]))
                        p_it = cursor.execute("SELECT * FROM product WHERE id=?", (it[0],)).fetchone()
                        if not p_it:
                            p_it = cursor.execute("SELECT * FROM product WHERE code LIKE ? AND name LIKE ?", ('%' + it[1] + '%', '%' + it[3] + '%')).fetchone()   
                            
                        print("p_it : " + str(p_it))
                        
                        print("3adding " + str(it[5]) + " to item_tobechanged")
                        item_tobechanged.append([p_it[0], str(p_it[12]), 1, str(it[4]), str(it[1]), str(it[5]),str(it[6]), str(it[7])])
                        ex_item_list.remove(it)
            print("--ex_item_list : " + str(ex_item_list))

        print("\n\n ex_docs_info item collect :" + str(ex_docs_info)+"\n\n")
        
        # todo what if the ex doc is orady payed in ex doc work on chane ex doc
        for ex_p in self.ex_pid_peyment:
            ex_doc = cursor.execute("SELECT * FROM doc_table WHERE doc_barcode=?", (ex_p,)).fetchone()
            if ex_doc:
                ex_item_list = load_payment(ex_doc[11])
                ex_pay_t = ""
                ex_pay_count = 0
                ex_pid = 0
                fou = -1
                e = 0
                for ex_d_info in ex_docs_info:
                    if ex_d_info[0] == ex_p:
                        fou = e
                        break
                    e += 1
                if fou == -1:
                    #todo get in doc value its price, disc, tax to append in next list
                    ex_docs_info.append([ex_p, 0, 0, "", 0, "", "", 0, 0, 0, 0])
                    fou = len(ex_docs_info)-1
                    
                for it in ex_item_list:
                    for p in self.pid_peyment:
                        print("p[] "+str(p) + ":" + str(ex_p))
                        if p[7] == ex_p:
                            print("self.extra_pid_peyment[p]:" + str(it))
                            if p[1] == "":
                                self.pid_peyment.remove(p)
                                continue
                            pay_index += 1
                            if ex_pay_t != "":
                                ex_pay_t += ","
                            rows = cursor.execute("SELECT * FROM tools WHERE name=?", (p[0],)).fetchall()
                            ispid = 1
                            if rows:
                                ispid = rows[0][11]
                            c = float(p[2])
                            print("\n\nc "+str(c))
                            print("ex_pid "+str(ex_pid))
                            print("ex_docs_info[fou][7] "+str(ex_docs_info[fou][7]))
                            print("ex_docs_info[fou][8] "+str(ex_docs_info[fou][8]))
                            print("\n\n")
                            ex_pay_count += 1
                            # todo chacke if updated date is deffernt
                            ex_pay_t += "(" + str(it[0]) + "," + str(p[1]) + "," +  str(p[2]) + "," + it[3] + "," + date + "," + it[5] + "," + str(ispid) + "," + p[7] + ")"
                            if ex_pid + c <= float(ex_docs_info[fou][7])-float(ex_docs_info[fou][8]):
                                ex_pid += c
                            else:
                                colect = 0
                                if ex_pid + c > float(ex_docs_info[fou][7])-float(ex_docs_info[fou][8]):
                                    ex_pay_count += 1
                                    pr = (float(ex_docs_info[fou][7])-float(ex_docs_info[fou][8]))-ex_pid # get remaning price unpid one
                                    c = c-pr # didact extra pid amount the remaing aount
                                    ex_pid += pr # update pid with filling remaing amount
                                    # save it
                                    #ex_pay_t += "(" + str(it[0]) + "," + str(p[1]) + "," +  str(c) + "," + it[3] + "," + date + "," + it[5] + "," + str(ispid) + "," + p[7] + ")"                                    
                                    if pid != 0 and price-disc != pid: # cacke if new item have remaning unpid amunt
                                        if price-disc-pid >= c:
                                            c=c
                                        if price-disc-pid < c:
                                            colect = c-price-disc
                                            c = price-disc-colect
                                        pid += c
                                        payments_ += "(" + str(it[0]) + "," + str(p[1]) + "," + str(c) + "," + it[3] + "," + date + "," + it[5] + "," + str(ispid) + "," + p[7] + ")"
                                        ex_pay_t += ",("+ str(it[0]) + ","+str(brcod)+",-" +  str(c) + "," + it[3] + "," + date + "," + it[5] + "," + str(ispid) + "," + p[7] + ")"
                                      
                                if price-disc == pid or colect > 0:
                                    for e_p_n in extra_payment_needs:
                                        for ex_d_info in ex_docs_info:
                                            if ex_d_info[0] == e_p_n:
                                                if float(ex_d_info[7])-float(ex_d_info[8])-float(ex_d_info[10]) >= c:
                                                    c=c
                                                if float(ex_d_info[7])-float(ex_d_info[8])-float(ex_d_info[10]) < c:
                                                    colect = c-float(ex_d_info[7])-float(ex_d_info[8])
                                                    c = float(ex_d_info[7])-float(ex_d_info[8])-colect
                                                
                                                ept = "(" + str(it[0]) + "," + str(p[1]) + "," + str(c) + "," + it[3] + "," + date + "," + it[5] + "," + str(ispid) + "," + p[7] + ")"
                                                print("ept "+str(ept))
                                                ex_d_info[2] = 1
                                                co = ""
                                                if ex_d_info[5] != "":
                                                    co = ","
                                                ex_d_info[5] = str(ex_d_info[5]) + co + ept
                                                ex_d_info[6] = float(ex_d_info[6]) + 1
                                                ex_d_info[10] = str(float(ex_d_info[10]) + float(c))
                                                break
                                if colect > 0: # else put extra payment for othere use
                                    payments_extra.append([str(it[0]), str(p[1]), str(exp), it[3], date, it[5], str(ispid), p[7]])
                                    
                        self.pid_peyment.remove(p)
                left = (float(ex_docs_info[fou][7])-float(ex_docs_info[fou][8])) - ex_pid
                print("[[fou][7], [fou][8], ex_pid " + str([float(ex_docs_info[fou][7]), float(ex_docs_info[fou][8]), ex_pid]) + " left "+str(left))
                print("payments_extra :: " + str(payments_extra))
                if left != 0:
                    # TODO IF PAID IS LESS AND THERE IS NO EXTRA PAIMENT RETURN ERROR SHORT PAYMENT
                    L = []
                    colect = 0
                    for ex_pa in payments_extra:
                        p = float(ex_pa[2])
                        colect += p
                        ex_bc = ex_pa[7]
                        if ex_bc == '':
                            ex_bc = ex_p
                        if colect > left:
                            q = colect-left
                            ex_pa[2] = q
                            p = colect - q
                        elif colect < left:
                            L.append("(" + str(ex_pa[0]) + "," + str(ex_pa[1]) + "," +  str(p) + "," + ex_pa[3] + "," + ex_pa[4] + "," + ex_pa[5] + "," + str(ex_pa[6]) + "," + ex_bc + ")")
                            ex_pa = []
                            continue
                        if colect == left:
                            L.append("(" + str(ex_pa[0]) + "," + str(ex_pa[1]) + "," +  str(p) + "," + ex_pa[3] + "," + ex_pa[4] + "," + ex_pa[5] + "," + str(ex_pa[6]) + "," + ex_bc + ")")
                            for inl in L:
                                if ex_pay_t != "":
                                    ex_pay_t += ","
                                ex_pay_t += inl
                        if ex_pa[7] == "":
                            T_pid -= float(ex_pa[2])
                        payments_extra.remove(ex_pa)
                        
                if ex_pay_t != "":
                    if fou != -1:
                        print("ex_pay_t "+str(ex_pay_t))
                        ex_docs_info[fou][2] = 1
                        co = ""
                        if ex_docs_info[fou][5] != "":
                            co = ","
                        ex_docs_info[fou][5] = str(ex_docs_info[fou][5]) + co + ex_pay_t
                        ex_docs_info[fou][6] = float(ex_docs_info[fou][6]) + ex_pay_count
                        ex_docs_info[fou][10] = str(float(ex_docs_info[fou][10]) + ex_pid)



        print("\n\n sold items collect :" + str(item)+"\n\n")
        print("\n\n payments_ pid collect :" + str(payments_)+"\n\n")
        print("\n\n ex_docs_info item collect :" + str(ex_docs_info)+"\n\n")
        print("\n\n ex_docs_info payment collect :" + str(ex_docs_info)+"\n\n")
        
        print("--payments_extra : " + str(payments_extra))


        print("price-disc "+str(price-disc) + ":pid " + str(pid) + ":def_pid " + str(def_pid))

        if not def_pid == 0 and price-disc != pid and price-disc == pid + def_pid:
            pid += def_pid
        if pid == 0 and item != "":
            for e_doc_info in ex_docs_info:
                if float(ex_d_info[7])-float(ex_d_info[8]) < float(ex_d_info[10]) and float(ex_d_info[10])-float(ex_d_info[7])-float(ex_d_info[8]) == price-disc:
                    if not e_doc_info[1]:
                        e_doc_info[1] = 1
                        e_doc_info[3] = ""
                    elif e_doc_info[3] != "":
                        e_doc_info[3] += ","
                    e_doc_info[3] += item
                    item = ""
                elif e_doc_info[1] and e_doc_info[3] == "":
                    e_doc_info[3] = item
                    item = ""
        print("--item = " + str(item))
        print("--payments_ : " + str(payments_))
        print("pyment "+str(price) + ":" + str(pid))
        print("--item_tobechanged : " + str(item_tobechanged))
        
        print("--ex_docs_info : " + str(ex_docs_info))
        name = ""
        phone_num = ""
        cm_id = None
        old_cm_id = None
                        
        slip_doc_code = []
        '''while True:
            continue'''
        for change_item in item_tobechanged:
            print("item : " + str(change_item[1]), change_item[2], str(change_item[3]), str(change_item[4]),str(change_item[5]), str(change_item[6]))
            print("item info befor : " + str(change_item[1]))
            qty_info_list = []
            print("change_item[1]  : " + str(change_item[1]))
            if "\"{" in str(change_item[1]):
                cod = str(change_item[4]).replace(",", "|")
                qty_info_list = read_code(change_item[1], "", cod, "", "")[4]
            else:
                qty_info_list = load_list(change_item[1])
            it_info = change_qty(qty_info_list, change_item[2], str(change_item[3]), str(change_item[4]), str(change_item[5]),str(change_item[6]), str(change_item[7]))

            print("item info befor  : " + str(it_info))
            #while True:
            #    continue
            cursor.execute('UPDATE product SET more_info=? WHERE id=?', (it_info, change_item[0]))
                    
            cursor.execute("SELECT * FROM product WHERE id=?", (change_item[0],))
            it2 = cursor.fetchone()
                    
            print("item info updated : " + str(it2[12]))
            
            # Commit the changes to the database
            conn.commit()
        if payment_customer_required:
            app = UserManagementApp(self, old_cm_id)
            if app.user_details:
                self.custemr = app.user_details['User_id']
                cm_id = self.custemr
            name = app.user_details['User_name']
            phone_num = app.user_details['User_phone_num']
            print(app.user_details)
            
        for e_doc_info in ex_docs_info:
            ppp0 = 0
            ppp = e_doc_info[5] 
            for exp in payments_extra:
                if exp[7] == e_doc_info[0]:
                    if exp[1] != '':
                        if ppp != "":
                            ppp += ","
                        ppp += "(" + "," + ",-" +  str(exp[2]) + "," + str(exp[3]) + "," + date + "," + str(exp[5]) + "," + str(exp[6]) + "," + str(exp[7]) + ")"
                        ppp0 = 1
                        payment_open_drower = 1
            
            rows = cursor.execute("SELECT * FROM doc_table WHERE doc_barcode=?", (e_doc_info[0],)).fetchall()
            if rows and rows[0][4]:
                old_cm_id = rows[0][4]
            
            print("cmd old id = " + str(rows[0]) + " new id " + str(cm_id))
            if cm_id and old_cm_id != str(cm_id):
                #[each item [barcode, isitem, ispay, ex_item, ex_item_items, payments, ex_payment_count, ex_item_pric, ex_item_T_disc, ex_item_T_tax, ex_pid]
                cursor.execute('UPDATE doc_table SET customer_id=? WHERE doc_barcode=?', (cm_id, e_doc_info[0]))
                # Commit the changes to the database
                conn.commit()
            if Seller_id != None:
                #[each item [barcode, isitem, ispay, ex_item, ex_item_items, payments, ex_payment_count, ex_item_pric, ex_item_T_disc, ex_item_T_tax, ex_pid]
                cursor.execute('UPDATE doc_table SET Seller_id=? WHERE doc_barcode=?', (Seller_id, e_doc_info[0]))
                # Commit the changes to the database
                conn.commit()
            if e_doc_info[1]:
                #[each item [barcode, isitem, ispay, ex_item, ex_item_items, payments, ex_payment_count, ex_item_pric, ex_item_T_disc, ex_item_T_tax, ex_pid]
                cursor.execute('UPDATE doc_table SET item=?, qty=?, price=?, discount=?, tax=?, doc_updated_date=? WHERE doc_barcode=?', (e_doc_info[3], e_doc_info[4], e_doc_info[7], e_doc_info[8], e_doc_info[9], date, e_doc_info[0]))
                # Commit the changes to the database
                conn.commit()
            if e_doc_info[2] or ppp0:
                #todo if needed add pid in doc e_doc_info[10]
                cursor.execute('UPDATE doc_table SET payments=?, doc_updated_date=? WHERE doc_barcode=?', (ppp, date, e_doc_info[0]))
                # Commit the changes to the database
                conn.commit()
            slip_doc_code.append(e_doc_info[0])
        
        if payments_ != "" and price-disc == pid:
            print("custemer : " + str(self.custemr) + "isneded : " + str(payment_customer_required))
            
            cursor.execute('INSERT INTO upload_doc (doc_barcode, extension_barcode, user_id, customer_id, Seller_id, type, item, qty, price, discount, tax, payments, pid, doc_created_date, doc_expire_date, doc_updated_date) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (str(brcod), "extension_barcode", self.user[3], self.custemr, Seller_id, "Sale_item", item, float(items), price, disc, tax, payments_, T_pid, date, "doc_expire_date", date))
            cursor.execute('INSERT INTO doc_table (doc_barcode, extension_barcode, user_id, customer_id, Seller_id, type, item, qty, price, discount, tax, payments, pid, doc_created_date, doc_expire_date, doc_updated_date) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (str(brcod), "extension_barcode", self.user[3], self.custemr, Seller_id, "Sale_item", item, float(items), price, disc, tax, payments_, T_pid, date, "doc_expire_date", date))
                    
            # Commit the changes to the database
            conn.commit()
            slip_doc_code.append(brcod)
                        
        if payment_open_drower == 1:
            PrinterForm.open_drower(self, self.user)
         
        ApproveFrame(self, self.user, slip_doc_code, payments_extra, payment_print_slip)
                
        # call void         
        self.void_items()
>>>>>>> db9ae79 (adding seller)
