import tkinter as tk
from tkinter import ttk
import sqlite3, os, sys
import datetime

current_dir = os.path.abspath(os.path.dirname(__file__))
MAIN_dir = os.path.join(current_dir, '..')
sys.path.append(MAIN_dir)
#from M.Display import DisplayFrame

from D.searchbox import search_entry
from D.ChooseCustemr import UserManagementApp
from D.iteminfo import *
from D.docediterform import DocEditForm
from D.printer import PrinterForm
from C.slipe import load_slip
from D.Upload_ import UploadingForm

# Create a connection to the SQLite database
data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data'))
db_path = os.path.join(data_dir, 'my_database.db')


from C.API.Get import *
from C.API.API import *
from C.API.Set import *


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
    
    #print(query+"\n")
    # Execute the SQL query and return the results as a list of tuples
    Update_table_database(query, (*given,))
    results = cur.fetchall()
    return results
    
# set the position of the Payment Form window to center
        # TODO: list z report for current day and history z reports for pev days but in notbook 
        # TODO: TO Print dayly, weekly, monthly and yearly report as user whats
        
class EnddayForm(tk.Tk):
    def __init__(self, master):
        self.master = master
        self.pyment_used = []
        
        self.info_tab = None
        # calculate the center coordinates of the screen
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        x = (screen_width / 2) - (300 / 2)  # 500 is the width of the Payment Form window
        y = (screen_height / 2) - (300 / 2)  # 500 is the height of the Payment Form window

        # create a Toplevel window for the payment form
        self.getvalue_form = tk.Toplevel(self.master)
        self.getvalue_form.geometry("%dx%d+0+0" % (screen_width, screen_height))
        self.getvalue_form.title("endday Form")

        # Notebook widget - CENTER_NOTEBOK
        self.center_notebook = ttk.Notebook(self.getvalue_form)
        self.center_notebook.pack(side="top", fill="both", expand=True)


        self.home_tab = ttk.Frame(self.center_notebook)
        self.home_tab.grid()

        # Add tabs to the self.center_notebook
        self.center_notebook.add(self.home_tab, text='Documents')

        self.home_tab.grid_columnconfigure(0, weight=5)
        self.home_tab.grid_columnconfigure(1, weight=5)
        self.home_tab.grid_columnconfigure(2, weight=5)
        self.home_tab.grid_columnconfigure(3, weight=5)
        self.home_tab.grid_columnconfigure(4, weight=5)
        self.home_tab.grid_columnconfigure(5, weight=5)
        self.home_tab.grid_columnconfigure(6, weight=5)
        self.home_tab.grid_rowconfigure(0, weight=5)
        self.home_tab.grid_rowconfigure(1, weight=5)
        self.home_tab.grid_rowconfigure(2, weight=5)
        self.home_tab.grid_rowconfigure(3, weight=5)
        self.home_tab.grid_rowconfigure(4, weight=5)
        
        self.details_frame = tk.Frame(self.home_tab)
        self.details_frame.grid(row=0, column=0, columnspan=6)

        # Create the label and entry for the document ID search
        self.doc_id_label = tk.Label(self.details_frame, text="Document ID:")
        self.doc_id_label.grid(row=0, column=0)
        self.doc_id_entry = tk.Entry(self.details_frame)
        self.doc_id_entry.grid(row=1, column=0)

        # Create the label and entry for the document type search
        self.doc_type_label = tk.Label(self.details_frame, text="Document Type:")
        self.doc_type_label.grid(row=0, column=1)
        self.doc_type_entry = tk.Entry(self.details_frame)
        self.doc_type_entry.grid(row=1, column=1)

        # Create the label and entry for the document barcode search
        self.doc_barcode_label = tk.Label(self.details_frame, text="Document Barcode:")
        self.doc_barcode_label.grid(row=0, column=2)
        self.doc_barcode_entry = tk.Entry(self.details_frame)
        self.doc_barcode_entry.grid(row=1, column=2)

        # Create the label and entry for the extension barcode search
        self.extension_barcode_label = tk.Label(self.details_frame, text="Extension Barcode:")
        self.extension_barcode_label.grid(row=0, column=3)
        self.extension_barcode_entry = tk.Entry(self.details_frame)
        self.extension_barcode_entry.grid(row=1, column=3)

        # Create the label and entry for the item search
        self.item_label = tk.Label(self.details_frame, text="Item:")
        self.item_label.grid(row=0, column=4)
        self.item_entry = tk.Entry(self.details_frame)
        self.item_entry.grid(row=1, column=4)

        # Create the label and entry for the user ID search
        self.user_id_label = tk.Label(self.details_frame, text="User ID:")
        self.user_id_label.grid(row=0, column=5)
        self.user_id_entry = tk.Entry(self.details_frame)
        self.user_id_entry.grid(row=1, column=5)

        # Create the label and entry for the customer ID search
        self.customer_id_label = tk.Label(self.details_frame, text="Customer ID:")
        self.customer_id_label.grid(row=0, column=6)
        self.customer_id_entry = tk.Entry(self.details_frame)
        self.customer_id_entry.grid(row=1, column=6)

        # Create the label and entry for the sold item info search
        self.sold_item_info_label = tk.Label(self.details_frame, text="Sold Item Info:")
        self.sold_item_info_label.grid(row=2, column=0)
        self.sold_item_info_entry = tk.Entry(self.details_frame)
        self.sold_item_info_entry.grid(row=3, column=0)

        # Create the label and entry for the discount search
        self.discount_label = tk.Label(self.details_frame, text="Discount:")
        self.discount_label.grid(row=2, column=1)
        self.discount_entry = tk.Entry(self.details_frame)
        self.discount_entry.grid(row=3, column=1)

        # Create the label and entry for the tax search
        self.tax_label = tk.Label(self.details_frame, text="Tax:")
        self.tax_label.grid(row=2, column=2)
        self.tax_entry = tk.Entry(self.details_frame)
        self.tax_entry.grid(row=3, column=2)

        # Create the label and entry for the document created date search
        self.doc_created_date_label = tk.Label(self.details_frame, text="Document Created Date:")
        self.doc_created_date_label.grid(row=2, column=3)
        self.doc_created_date_entry = tk.Entry(self.details_frame)
        self.doc_created_date_entry.insert(0, datetime.datetime.now().strftime('%Y-%m-%d'))
        self.doc_created_date_entry.grid(row=3, column=3)

        # Create the label and entry for the document expire date search
        self.doc_expire_date_label = tk.Label(self.details_frame, text="Document Expire Date:")
        self.doc_expire_date_label.grid(row=2, column=4)
        self.doc_expire_date_entry = tk.Entry(self.details_frame)
        self.doc_expire_date_entry.grid(row=3, column=4)
       

        # Create the label and entry for the document expire date search
        self.doc_updated_date_entry = tk.Label(self.details_frame, text="Document Updated Date:")
        self.doc_updated_date_entry.grid(row=2, column=5)
        self.doc_updated_date_entry = tk.Entry(self.details_frame)
        self.doc_updated_date_entry.grid(row=3, column=5)

        # Create the search button
        self.search_button = tk.Button(self.details_frame, text="Search", command=self.perform_search)
        self.search_button.grid(row=3, column=6)

        # Create the search button
        self.print_button = tk.Button(self.details_frame, text="Print", command=self.perform_print)
        self.print_button.grid(row=4, column=1)

        self.upload_button = tk.Button(self.details_frame, text="Upload", bg="red", fg="white", font=("Arial", 12), command=lambda: UploadingForm(self))
        self.upload_button.grid(row=4, column=2)


        # Create the listbox to display search results
        self.listbox = ttk.Treeview(self.home_tab)        
        self.listbox.bind('<<TreeviewSelect>>', self.on_select)
        #self.listbox.bind("<Button-1>", self.on_treeview_double_click)
        #self.listbox.grid_propagate(False)


        # Add vertical scrollbar
        tree_scrollbar_y = ttk.Scrollbar(self.listbox, orient='vertical', command=self.listbox.yview)
        self.listbox.configure(yscrollcommand=tree_scrollbar_y.set)
        tree_scrollbar_y.pack(side='right', fill='y')

        # Add horizontal scrollbar
        tree_scrollbar_x = ttk.Scrollbar(self.listbox, orient='horizontal', command=self.listbox.xview)
        self.listbox.configure(xscrollcommand=tree_scrollbar_x.set)
        tree_scrollbar_x.pack(side='bottom', fill='x')

        # Set the size of the self.listbox widget
        self.listbox.grid(row=1, column=0, rowspan=3, columnspan=5, sticky="nsew")
        self.get_columen()
        
        # New listbox in the main frame
        self.list_items = tk.Listbox(self.home_tab, bg="yellow", height=17)
        self.list_items.grid(row=1, column=5, rowspan=2, sticky="nsew")
        self.doc_total_unpaid = tk.Label(self.home_tab, text="Amount Unpid:", font=("Arial", 11))
        self.doc_total_unpaid.grid(row=3, column=5)
        self.doc_total_paid = tk.Label(self.home_tab, text="Amount pid:", font=("Arial", 12))
        self.doc_total_paid.grid(row=4, column=5)
        self.doc_total_ = tk.Label(self.home_tab, text="Totale :", font=("Arial", 15))
        self.doc_total_.grid(row=5, column=5)


        # show the Payment Form window
        self.perform_search()
        self.getvalue_form.transient(self.master)
        self.getvalue_form.grab_set()
        self.master.wait_window(self.getvalue_form)
        
    def show_doc_form(self):
        # call the function in the main file to show the first frame
        self.master.master.show_frame("DocForm")
        
    def get_columen(self):
        self.listbox['columns'] = ('doc_barcode', 'extension_barcode', 'user_id', 'customer_id', 'Type', 'Itmes', 'Qty', 'Paymen', 'price', 'disc', 'tax', 'doc_created_date', 'doc_expire_date', 'doc_updated_date')
        self.listbox.heading("#0", text="ID")
        self.listbox.column("#0", stretch=tk.NO, minwidth=25, width=50) 
        self.listbox.heading("#1", text="doc_barcode")
        self.listbox.column("#1", stretch=tk.NO, minwidth=25, width=100) 
        self.listbox.heading("#2", text="extension_barcode")
        self.listbox.column("#2", stretch=tk.NO, minwidth=25, width=100) 
        self.listbox.heading("#3", text="user_id")
        self.listbox.column("#3", stretch=tk.NO, minwidth=25, width=100) 
        self.listbox.heading("#4", text="customer_id")
        self.listbox.column("#4", stretch=tk.NO, minwidth=25, width=100) 
        self.listbox.heading("#5", text="Type")
        self.listbox.column("#5", stretch=tk.NO, minwidth=25, width=80) 
        self.listbox.heading("#6", text="Itmes")
        self.listbox.column("#6", stretch=tk.NO, minwidth=25, width=100) 
        self.listbox.heading("#7", text="Qty")
        self.listbox.column("#7", stretch=tk.NO, minwidth=25, width=100) 
        self.listbox.heading("#8", text="price")
        self.listbox.column("#8", stretch=tk.NO, minwidth=25, width=50) 
        self.listbox.heading("#9", text="disc")
        self.listbox.column("#9", stretch=tk.NO, minwidth=25, width=50) 
        self.listbox.heading("#10", text="tax")
        self.listbox.column("#10", stretch=tk.NO, minwidth=25, width=50) 
        self.listbox.heading("#11", text="Payment")
        self.listbox.column("#11", stretch=tk.NO, minwidth=25, width=100) 
        self.listbox.heading("#12", text="doc_created_date")
        self.listbox.column("#12", stretch=tk.NO, minwidth=25, width=100) 
        self.listbox.heading("#13", text="doc_expire_date")
        self.listbox.column("#13", stretch=tk.NO, minwidth=25, width=100) 
        self.listbox.heading("#14", text="doc_updated_date")
        self.listbox.column("#14", stretch=tk.NO, minwidth=25, width=100) 

        #self.listbox.heading("#0", text="CODE", anchor=tk.W)
        #self.listbox.heading("#1", text="BARCODE", anchor=tk.W)
        #self.listbox.column("#1", stretch=tk.NO, minwidth=25, width=100)   
    def creat_info(self):
        self.list_items.delete(0, tk.END)
        unpid = 0
        pid = 0
        for pay in self.pyment_used:
            #print("creating lable : " + str(pay[0]+" :"+str(pay[1])))
            self.list_items.insert(tk.END, [pay[0], pay[1]])
            pid += pay[1]
        self.doc_total_unpaid.config(text="Amount UnPide : " + str(unpid))
        self.doc_total_paid.config(text="Amount Pide : " + str(pid))
        self.doc_total_.config(text="Total : " + str(pid + unpid))
        #tk.Label(self.info_tab, text=" :"+str(pay[1])).pack()
        
        

    def close_tab(self, t_id):
        self.center_notebook.forget(t_id)
        

    def on_select(self, event):
        pass
    
    # Function to perform the search and display the results in the listbox
    def perform_search(self):
        self.pyment_used = []
        # Get the search criteria from the entry boxes
        doc_id = self.doc_id_entry.get()
        doc_type = self.doc_type_entry.get()
        doc_barcode = self.doc_barcode_entry.get()
        extension_barcode = self.extension_barcode_entry.get()
        item = self.item_entry.get()
        user_id = self.user_id_entry.get()
        customer_id = self.customer_id_entry.get()
        sold_item_info = self.sold_item_info_entry.get()
        discount = self.discount_entry.get()
        tax = self.tax_entry.get()
        doc_created_date = self.doc_created_date_entry.get()
        doc_expire_date = self.doc_expire_date_entry.get()
        doc_updated_date = self.doc_updated_date_entry.get()

        # Perform the search and update the listbox with the results
        df = search_documents(doc_id, doc_type, doc_barcode, extension_barcode, item, user_id, customer_id,
                            sold_item_info, discount, tax, doc_created_date, doc_expire_date, doc_updated_date)
        self.listbox.delete(*self.listbox.get_children())
        #self.get_columen()
        for index in df:
            #print("df : " + str(index))
            item = self.listbox.insert('', 'end', text=index[0], values=(index[1], index[2], index[3], index[4], index[5], index[6], index[7], index[8], index[9], index[10], index[11], index[12], index[13], index[14]))
            #  payment
            self.load_payment(index[11])
        
        self.creat_info()
            
    def load_payment(self, p_text):
        #print("tiems : " + str(p_text))
        if ")" in str(p_text) or ")," in str(p_text):
            items_lists = (p_text + ",").split("),")
            index = 0
            for p in range(len(items_lists)-1):
                item = items_lists[p].split(",")
                #print("item ;" + str(item))
                #for each items+
                pay_id = item[0].replace("(", "")
                pay_type = item[1]
                pay_pid = item[2]
                pay_pid_date = item[3].replace(",", "")
                pay_updated_date = item[4].replace(",", "")
                pay_user = item[5].replace(",", "")
                
                price = item[1]
                found = 0
                for pay in self.pyment_used:
                    if pay[0] == pay_type:
                        found = 1
                        pay[1] += float(pay_pid)
                        break
                if found == 0:
                    #print("new payment :" + str([pay_type, pay_pid]))
                    self.pyment_used.append([pay_type, float(pay_pid)])
                index += 1

        elif "," in str(p_text):
            items_lists = self.items[10].split(",")
            index = 0
            for p in range(len(items_lists)-1):
                item = items_lists[p].split(" = ")
                #print("item :" + str(item))
                #for each items
                name = item[0].replace("(:", "")
                price = item[1]
                #print("list : " + str([name, price]))
                
                index += 1
        else:
            item = str(p_text).split(" = ")
            #print("item :" + str(item))
            if len(item) > 1:
                name = item[0].replace("(:", "")
                price = item[1]
                self.list_payment.insert("", 'end', text="0", values=(name, price, self.created_date, self.created_date, self.created_user))
        
            
