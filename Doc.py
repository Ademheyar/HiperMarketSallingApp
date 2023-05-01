import sqlite3
import tkinter as tk
from tkinter import ttk

# Create a connection to the SQLite database
conn = sqlite3.connect('my_database.db')

# Create a table to store the document records
cur = conn.cursor()

conn.commit()
# Example usage:
# Add a new document record to the doc_table SQLite database table

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
        self.create_widgets()

    def show_doc_form(self):
        # call the function in the main file to show the first frame
        self.master.master.show_frame("DocForm")
        
    def create_widgets(self):
        # Create the listbox to display search results
        self.listbox = ttk.Treeview(self)
        self.listbox.grid_propagate(False)

        # Set the size of the self.listbox widget

        self.listbox.pack(side="left", fill="both", expand=True)
        self.get_columen()

        self.details_frame = tk.Frame(self)
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
        self.get_columen()
        for index in df:
            self.listbox.insert('', 'end', text=index[0], values=(index[1], index[2], index[3], index[4], index[5], index[6], index[7], index[8], index[9], index[10], index[11], index[12]))