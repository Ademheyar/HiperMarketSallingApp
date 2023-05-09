import sqlite3
import tkinter as tk
from tkinter import ttk

import os, sys
current_dir = os.path.abspath(os.path.dirname(__file__))
MAIN_dir = os.path.join(current_dir, '..')
sys.path.append(MAIN_dir)
from D.docediterform import DocEditForm
import os
# Create a connection to the SQLite database
data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data'))
db_path = os.path.join(data_dir, 'my_database.db')
conn = sqlite3.connect(db_path)
# Create a table to store the document records
cur = conn.cursor()

conn.commit()

tab_titles = []

# Function to search for documents in the doc_table SQLite database table
def search_documents(doc_id=None, doc_type=None, doc_barcode=None, extension_barcode=None, 
                    item=None, user_id=None, customer_id=None, sold_item_info=None, discount=None, 
                    tax=None, doc_created_date=None, doc_expire_date=None, doc_updated_date=None):
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
        query += f" AND item='{item}'"
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
        query += f" AND doc_created_date='{doc_created_date}'"
    if doc_expire_date is not None and doc_expire_date is not '':
        query += f" AND doc_expire_date='{doc_expire_date}'"
    if doc_updated_date is not None and doc_updated_date is not '':
        query += f" AND doc_updated_date='{doc_updated_date}'"
    
    print(query+"\n")
    # Execute the SQL query and return the results as a list of tuples
    cur.execute(query)
    results = cur.fetchall()
    return results
    
class DocForm(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        
        # Notebook widget - CENTER_NOTEBOK
        self.center_notebook = ttk.Notebook(self)
        self.center_notebook.pack()


        self.home_tab = ttk.Frame(self.center_notebook)

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
        
        # Create the listbox to display search results
        self.listbox = ttk.Treeview(self.home_tab)        
        self.listbox.bind('<<TreeviewSelect>>', self.on_select)
        self.listbox.bind("<Button-1>", self.on_treeview_double_click)
        self.listbox.grid_propagate(False)

        # Set the size of the self.listbox widget
        self.listbox.pack(side="left", fill="both", expand=True)
        self.get_columen()
        self.listbox.insert('', 'end', text="1", values=("1", "2", "3", "4","5", "6", "7", "8"))

        self.details_frame = tk.Frame(self.home_tab)
        self.details_frame.pack(side="right", fill="both", expand=True)

        # Create the label and entry for the document ID search
        self.doc_id_label = tk.Label(self.details_frame, text="Document ID:")
        self.doc_id_label.pack()
        self.doc_id_entry = tk.Entry(self.details_frame)
        self.doc_id_entry.pack()

        # Create the label and entry for the document type search
        self.doc_type_label = tk.Label(self.details_frame, text="Document Type:")
        self.doc_type_label.pack()
        self.doc_type_entry = tk.Entry(self.details_frame)
        self.doc_type_entry.pack()

        # Create the label and entry for the document barcode search
        self.doc_barcode_label = tk.Label(self.details_frame, text="Document Barcode:")
        self.doc_barcode_label.pack()
        self.doc_barcode_entry = tk.Entry(self.details_frame)
        self.doc_barcode_entry.pack()

        # Create the label and entry for the extension barcode search
        self.extension_barcode_label = tk.Label(self.details_frame, text="Extension Barcode:")
        self.extension_barcode_label.pack()
        self.extension_barcode_entry = tk.Entry(self.details_frame)
        self.extension_barcode_entry.pack()

        # Create the label and entry for the item search
        self.item_label = tk.Label(self.details_frame, text="Item:")
        self.item_label.pack()
        self.item_entry = tk.Entry(self.details_frame)
        self.item_entry.pack()

        # Create the label and entry for the user ID search
        self.user_id_label = tk.Label(self.details_frame, text="User ID:")
        self.user_id_label.pack()
        self.user_id_entry = tk.Entry(self.details_frame)
        self.user_id_entry.pack()

        # Create the label and entry for the customer ID search
        self.customer_id_label = tk.Label(self.details_frame, text="Customer ID:")
        self.customer_id_label.pack()
        self.customer_id_entry = tk.Entry(self.details_frame)
        self.customer_id_entry.pack()

        # Create the label and entry for the sold item info search
        self.sold_item_info_label = tk.Label(self.details_frame, text="Sold Item Info:")
        self.sold_item_info_label.pack()
        self.sold_item_info_entry = tk.Entry(self.details_frame)
        self.sold_item_info_entry.pack()

        # Create the label and entry for the discount search
        self.discount_label = tk.Label(self.details_frame, text="Discount:")
        self.discount_label.pack()
        self.discount_entry = tk.Entry(self.details_frame)
        self.discount_entry.pack()

        # Create the label and entry for the tax search
        self.tax_label = tk.Label(self.details_frame, text="Tax:")
        self.tax_label.pack()
        self.tax_entry = tk.Entry(self.details_frame)
        self.tax_entry.pack()

        # Create the label and entry for the document created date search
        self.doc_created_date_label = tk.Label(self.details_frame, text="Document Created Date:")
        self.doc_created_date_label.pack()
        self.doc_created_date_entry = tk.Entry(self.details_frame)
        self.doc_created_date_entry.pack()

        # Create the label and entry for the document expire date search
        self.doc_expire_date_label = tk.Label(self.details_frame, text="Document Expire Date:")
        self.doc_expire_date_label.pack()
        self.doc_expire_date_entry = tk.Entry(self.details_frame)
       

        # Create the label and entry for the document expire date search
        self.doc_updated_date_entry = tk.Label(self.details_frame, text="Document Updated Date:")
        self.doc_updated_date_entry.pack()
        self.doc_updated_date_entry = tk.Entry(self.details_frame)

        # Create the search button
        self.search_button = tk.Button(self.details_frame, text="Search", command=self.perform_search)
        self.search_button.pack()

    def show_doc_form(self):
        # call the function in the main file to show the first frame
        self.master.master.show_frame("DocForm")
        
    def get_columen(self):
        self.listbox['columns'] = ('Type', 'doc_barcode', 'extension_barcode', 'Itmes', 'user_id', 'customer_id', 'price', 'disc', 'tax', 'doc_created_date', 'doc_expire_date', 'doc_updated_date')
        self.listbox.heading("#0", text="ID")
        self.listbox.column("#0", stretch=tk.NO, minwidth=25, width=50) 
        self.listbox.heading("#1", text="Type")
        self.listbox.column("#1", stretch=tk.NO, minwidth=25, width=80) 
        self.listbox.heading("#2", text="doc_barcode")
        self.listbox.column("#2", stretch=tk.NO, minwidth=25, width=100) 
        self.listbox.heading("#3", text="extension_barcode")
        self.listbox.column("#3", stretch=tk.NO, minwidth=25, width=100) 
        self.listbox.heading("#4", text="Itmes")
        self.listbox.column("#4", stretch=tk.NO, minwidth=25, width=100) 
        self.listbox.heading("#5", text="user_id")
        self.listbox.column("#5", stretch=tk.NO, minwidth=25, width=100) 
        self.listbox.heading("#6", text="customer_id")
        self.listbox.column("#6", stretch=tk.NO, minwidth=25, width=100) 
        self.listbox.heading("#7", text="price")
        self.listbox.column("#7", stretch=tk.NO, minwidth=25, width=50) 
        self.listbox.heading("#8", text="disc")
        self.listbox.column("#8", stretch=tk.NO, minwidth=25, width=50) 
        self.listbox.heading("#9", text="tax")
        self.listbox.column("#9", stretch=tk.NO, minwidth=25, width=50) 
        self.listbox.heading("#10", text="doc_created_date")
        self.listbox.column("#10", stretch=tk.NO, minwidth=25, width=100) 
        self.listbox.heading("#11", text="doc_expire_date")
        self.listbox.column("#11", stretch=tk.NO, minwidth=25, width=100) 
        self.listbox.heading("#12", text="doc_updated_date")
        self.listbox.column("#12", stretch=tk.NO, minwidth=25, width=100) 

        #self.listbox.heading("#0", text="CODE", anchor=tk.W)
        #self.listbox.heading("#1", text="BARCODE", anchor=tk.W)
        #self.listbox.column("#1", stretch=tk.NO, minwidth=25, width=100)   
    def on_treeview_double_click(self, event):
        item = self.listbox.focus()  # Get the item that was clicked
        print("in dubleclicked")
        item_text = self.listbox.item(item, "values")  # Get the text values of the item

        if item:
            # Detect double-click
            print("Double-clicked item:", item_text)

            # Add tabs to the self.center_notebook
            if item_text[1]:
                if item_text[1] not in tab_titles:
                    tab_titles.append(item_text[1])
                    test_tab = ttk.Frame(self.center_notebook)
                    self.center_notebook.add(test_tab, text=item_text[1])
                    doc_edit_form = DocEditForm(test_tab)
                    doc_edit_form.pack(fill="both", expand=True)
                    # Create a close button and position it at the top next to the tab title
                    close_button1 = tk.Button(test_tab, text="X")
                    close_button1.pack(side="top", anchor="ne", padx=5, pady=2)
                    close_button1.bind("<Button-1>", lambda event: self.close_tab(event, test_tab))
                else:
                    print("Tab already exists!")

    def close_tab(self, tab_id):
        self.center_notebook.forget(tab_id)

    def on_select(self, event):
        pass

    # Function to perform the search and display the results in the listbox
    def perform_search(self):
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
        print("df : " + str(df))
        self.listbox.delete(*self.listbox.get_children())
        #self.get_columen()
        for index in df:
            self.listbox.insert('', 'end', text=index[0], values=(index[1], index[2], index[3], index[4], index[5], index[6], index[7], index[8], index[9], index[10], index[11], index[12]))