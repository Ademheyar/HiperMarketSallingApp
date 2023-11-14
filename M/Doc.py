import sqlite3
import tkinter as tk
from tkinter import ttk
<<<<<<< HEAD
=======
import tkinter as tk
from tkinter import ttk
import sqlite3
import shutil
import datetime
import atexit
>>>>>>> db9ae79 (adding seller)

import os, sys
current_dir = os.path.abspath(os.path.dirname(__file__))
MAIN_dir = os.path.join(current_dir, '..')
sys.path.append(MAIN_dir)
from D.docediterform import DocEditForm
from D.printer import PrinterForm
from C.slipe import load_slip
import os
# Create a connection to the SQLite database
data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data'))
db_path = os.path.join(data_dir, 'my_database.db')
conn = sqlite3.connect(db_path)
# Create a table to store the document records
cur = conn.cursor()

conn.commit()

<<<<<<< HEAD
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
        self.center_notebook.pack(side="top", fill="both", expand=True)

        self.home_tab = ttk.Frame(self.center_notebook)
        self.home_tab.grid()

        # Add tabs to the self.center_notebook
        self.center_notebook.add(self.home_tab, text='Documents')

        self.home_tab.grid_columnconfigure(0, weight=1)
        self.home_tab.grid_columnconfigure(1, weight=1)
        self.home_tab.grid_columnconfigure(2, weight=1)
        self.home_tab.grid_columnconfigure(3, weight=1)
        self.home_tab.grid_columnconfigure(4, weight=1)
        self.home_tab.grid_columnconfigure(5, weight=1)
        self.home_tab.grid_columnconfigure(6, weight=1)
        self.home_tab.grid_rowconfigure(0, weight=1)
        self.home_tab.grid_rowconfigure(1, weight=0)
        self.home_tab.grid_rowconfigure(2, weight=1)
        self.home_tab.grid_rowconfigure(3, weight=1)
        self.home_tab.grid_rowconfigure(4, weight=1)
        
        # Create the listbox to display search results
        self.listbox = ttk.Treeview(self.home_tab)        
=======
from D.Getdate import GetDateForm
from D.Chart.Chart import *

# Function to search for documents in the doc_table SQLite database table
def search_documents(doc_id=None, doc_type=None, doc_barcode=None, extension_barcode=None, 
                    item=None, user_id=None, customer_id=None, sold_item_info=None, discount=None, 
                    tax=None, date_from=None, date_to=None, doc_created_date=None, doc_expire_date=None, doc_updated_date=None):
    given = []
    # Build the SQL query based on the provided attributes
    query = 'SELECT * FROM doc_table WHERE'
    q, d = '', ''
    if doc_id is not None and doc_id is not '':
        q += f" AND id='{doc_id}'" if q != '' else f" id='{doc_id}'"
    if doc_type is not None and doc_type != '':
        q += f" AND type='{doc_type}'" if q != '' else f" type='{doc_type}'"
    if doc_barcode is not None and doc_barcode is not '':
        q += f" AND doc_barcode='{doc_barcode}'" if q != '' else f" doc_barcode='{doc_barcode}'"
    if extension_barcode is not None and extension_barcode is not '':
        q += f" AND extension_barcode='{extension_barcode}'" if q != '' else f" extension_barcode='{extension_barcode}'"
    if item is not None and item is not '':
        q += f" AND item LIKE ?" if q != '' else f" item LIKE ?"
        if given == None:
            given.append(f'%{item}%')
        else:
            given.append(f'%{item}%')
    if user_id is not None and user_id is not '':
        q += f" AND user_id='{user_id}'" if q != '' else f" user_id='{user_id}'"
    if customer_id is not None and customer_id is not '':
        q += f" AND customer_id='{customer_id}'" if q != '' else f" customer_id='{customer_id}'"
    if sold_item_info is not None and sold_item_info is not '':
        q += f" AND sold_item_info='{sold_item_info}'" if q != '' else f" sold_item_info='{sold_item_info}'"
    if discount is not None and discount is not '':
        q += f" AND discount='{discount}'" if q != '' else f" discount='{discount}'"
    if tax is not None and tax is not '':
        q += f" AND tax='{tax}'" if q != '' else f" tax='{tax}'"

    if doc_created_date is not None and doc_created_date:
        d += f" OR strftime('%Y-%m-%d', doc_created_date) BETWEEN ? AND ?" if d != '' else f" strftime('%Y-%m-%d', doc_created_date) BETWEEN ? AND ?"
        given.append(f'{date_from}')
        given.append(f'{date_to}')
    if doc_expire_date is not None and doc_expire_date:
        d += f" OR strftime('%Y-%m-%d', doc_expire_date) BETWEEN ? AND ?" if d != '' else f" strftime('%Y-%m-%d', doc_expire_date) BETWEEN ? AND ?"
        given.append(f'{date_from}')
        given.append(f'{date_to}')
    if doc_updated_date is not None and doc_updated_date:
        d += f" OR strftime('%Y-%m-%d', doc_updated_date) BETWEEN ? AND ?" if d != '' else f" strftime('%Y-%m-%d', doc_updated_date) BETWEEN ? AND ?"
        given.append(f'{date_from}')
        given.append(f'{date_to}')
    r = ''
    if q != '':
        if r != '':
            r += " AND (" + q + ")"
        else:
            r = q
    if d != '':
        if r != '':
            r += " AND (" + d + ")"
        else:
            r = d
    query += r
    #print(str([query, (*given,)])+"\n")
    # Execute the SQL query and return the results as a list of tuples
    cur.execute(query, (*given,))
    results = cur.fetchall()
    return results

class DocForm(tk.Frame):
    def __init__(self, master, user):
        tk.Frame.__init__(self, master)
        self.pyment_used = []
        self.user_info = user
        # Notebook widget - CENTER_NOTEBOK
        self.start_value = datetime.datetime.now().strftime('%Y-%m-%d')
        self.end_value = self.start_value
        
        self.center_notebook = ttk.Notebook(self)
        self.center_notebook.pack(side="top", fill="both", expand=True)

        self.Doc_tab = ttk.Frame(self.center_notebook)
        self.Doc_tab.grid()

        # Add tabs to the self.center_notebook
        self.center_notebook.add(self.Doc_tab, text='Documents')

        self.Doc_tab.grid_columnconfigure(0, weight=1)
        self.Doc_tab.grid_columnconfigure(1, weight=1)
        self.Doc_tab.grid_columnconfigure(2, weight=1)
        self.Doc_tab.grid_columnconfigure(3, weight=1)
        self.Doc_tab.grid_columnconfigure(4, weight=1)
        self.Doc_tab.grid_columnconfigure(5, weight=1)
        self.Doc_tab.grid_columnconfigure(6, weight=1)
        self.Doc_tab.grid_rowconfigure(0, weight=1)
        self.Doc_tab.grid_rowconfigure(1, weight=1)
        self.Doc_tab.grid_rowconfigure(2, weight=1)
        self.Doc_tab.grid_rowconfigure(3, weight=1)
        self.Doc_tab.grid_rowconfigure(4, weight=1)
        
        self.l_frame = tk.Frame(self.Doc_tab)
        self.l_frame.grid(row=0, column=0, rowspan=2, columnspan=7, sticky="nsew")

        # Create the listbox to display search results
        self.listbox = ttk.Treeview(self.l_frame)        
>>>>>>> db9ae79 (adding seller)
        self.listbox.bind('<<TreeviewSelect>>', self.on_select)
        self.listbox.bind("<Button-1>", self.on_treeview_double_click)
        #self.listbox.grid_propagate(False)


        # Add vertical scrollbar
<<<<<<< HEAD
        tree_scrollbar_y = ttk.Scrollbar(self.listbox, orient='vertical', command=self.listbox.yview)
=======
        tree_scrollbar_y = ttk.Scrollbar(self.l_frame, orient='vertical', command=self.listbox.yview)
>>>>>>> db9ae79 (adding seller)
        self.listbox.configure(yscrollcommand=tree_scrollbar_y.set)
        tree_scrollbar_y.pack(side='right', fill='y')

        # Add horizontal scrollbar
<<<<<<< HEAD
        tree_scrollbar_x = ttk.Scrollbar(self.listbox, orient='horizontal', command=self.listbox.xview)
        self.listbox.configure(xscrollcommand=tree_scrollbar_x.set)
        tree_scrollbar_x.pack(side='bottom', fill='x')

        # Set the size of the self.listbox widget
        self.listbox.grid(row=1, column=0, rowspan=4, sticky="nsew")
        self.get_columen()
        self.listbox.insert('', 'end', text="1", values=("1", "2", "3", "4","5", "6", "7", "8"))

        self.details_frame = tk.Frame(self.home_tab)
        self.details_frame.grid(row=0, column=0)
=======
        tree_scrollbar_x = ttk.Scrollbar(self.l_frame, orient='horizontal', command=self.listbox.xview)
        self.listbox.configure(xscrollcommand=tree_scrollbar_x.set)
        tree_scrollbar_x.pack(side='bottom', fill='x', )

        # Set the size of the self.listbox widget
        self.listbox.pack(side='top', fill='both', expand=True)
        self.get_columen()

        # Create the search button
        self.print_button = tk.Button(self.Doc_tab, text="Print", command=self.perform_print)
        self.print_button.grid(row=2, column=0)


        self.info_notebook = ttk.Notebook(self.Doc_tab)
        self.info_notebook.grid(row=3, column=0, rowspan=3, columnspan=7, sticky="nsew")

        self.details_frame = tk.Frame(self.Doc_tab)
        self.details_frame.grid(row=2, column=0, rowspan=4, sticky="nsew")
        
        # Add tabs to the self.center_notebook
        self.info_notebook.add(self.details_frame, text='Controler')
>>>>>>> db9ae79 (adding seller)

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

<<<<<<< HEAD
        # Create the label and entry for the document created date search
        self.doc_created_date_label = tk.Label(self.details_frame, text="Document Created Date:")
        self.doc_created_date_label.grid(row=2, column=3)
        self.doc_created_date_entry = tk.Entry(self.details_frame)
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
=======
        self.doc_created_date_var = tk.IntVar()
        self.doc_created_date_var.set(1)
        self.doc_created_date_Checkbutton = tk.Checkbutton(self.details_frame, text='Created Date', variable=self.doc_created_date_var)
        self.doc_created_date_Checkbutton.grid(row=2, column=3)

        self.doc_expire_date_var = tk.IntVar()
        self.doc_expire_date_var.set(1)
        self.doc_expire_date_Checkbutton = tk.Checkbutton(self.details_frame, text='Expire Date', variable=self.doc_expire_date_var)
        self.doc_expire_date_Checkbutton.grid(row=2, column=4)

        self.doc_updated_date_var = tk.IntVar()
        self.doc_updated_date_var.set(1)
        self.doc_updated_date_Checkbutton = tk.Checkbutton(self.details_frame, text='Updated Date', variable=self.doc_updated_date_var)
        self.doc_updated_date_Checkbutton.grid(row=2, column=5)
        
        self.date_from_Entry = tk.Entry(self.details_frame)
        self.date_from_Entry.insert(0, self.start_value)
        self.date_from_Entry.grid(row=3, column=3)
        
        self.date_to_Entry = tk.Entry(self.details_frame)
        self.date_to_Entry.insert(0, self.start_value)
        self.date_to_Entry.grid(row=3, column=4)
        
        self.GetDate_button = tk.Button(self.details_frame, text="GetDate", font=("Arial", 12), command=self.fix_date)
        self.GetDate_button.grid(row=3, column=5, sticky="nsew")
>>>>>>> db9ae79 (adding seller)

        # Create the search button
        self.search_button = tk.Button(self.details_frame, text="Search", command=self.perform_search)
        self.search_button.grid(row=3, column=6)

<<<<<<< HEAD
        # Create the search button
        self.print_button = tk.Button(self.details_frame, text="Print", command=self.perform_print)
        self.print_button.grid(row=4, column=1)
=======
        # Notebook widget - CENTER_NOTEBOK
        self.graph_value = {}
        self.graph_value0 = [["A", 10], ["B", 90], ["C", 50], ["D", 100], ["E", 65], ["F", 500], ["G", 1000], ["H", 85], ["I", 5]]

        
        self.home_tab = ttk.Frame(self.Doc_tab)
        self.home_tab.grid(row=6, column=0, columnspan=7, rowspan=3, sticky="nsew")
        
        # Add tabs to the self.center_notebook
        self.info_notebook.add(self.home_tab, text='Info')


        
        self.home_tab.grid_columnconfigure(0, weight=1)
        self.home_tab.grid_columnconfigure(1, weight=1)
        self.home_tab.grid_columnconfigure(2, weight=1)
        self.home_tab.grid_columnconfigure(3, weight=1)
        self.home_tab.grid_columnconfigure(4, weight=1)
        self.home_tab.grid_columnconfigure(5, weight=1)
        self.home_tab.grid_columnconfigure(6, weight=1)
        self.home_tab.grid_columnconfigure(7, weight=1)
        self.home_tab.grid_columnconfigure(8, weight=1)
        self.home_tab.grid_rowconfigure(0, weight=1)
        self.home_tab.grid_rowconfigure(1, weight=1)
        self.home_tab.grid_rowconfigure(2, weight=1)
        self.home_tab.grid_rowconfigure(3, weight=1)
        
        
        def on_style_selected(*args):
            draw_cart(int(self.style_var.get()), self.chart_canvas, self.next_button, self.prev_button, self.graph_value0, int(self.which_var.get()), 1, 0)
            draw_cart(int(self.style_var1.get()), self.chart2_canvas, self.next_button1, self.prev_button1, self.graph_value0, int(self.which_var.get()), 2, 0)
            self.display_products(self.graph_value0)

        self.chart_canvas = tk.Canvas(self.home_tab)
        self.chart_canvas.grid(row=0, column=0, columnspan=3, rowspan=3)
        
        self.chart2_canvas = tk.Canvas(self.home_tab)
        self.chart2_canvas.grid(row=0, column=3, columnspan=2, rowspan=3)
        
        self.product_list = tk.Listbox(self.home_tab, width=30)
        self.product_list.grid(row=0, column=5, columnspan=1, padx=1, pady=1, sticky=tk.N)
        

        # New listbox in the main frame
        self.list_items = tk.Listbox(self.home_tab, bg="yellow")
        self.list_items.grid(row=0, column=6, columnspan=1, padx=1, pady=1, sticky=tk.N)

        self.doc_total_unpaid = tk.Label(self.home_tab, text="Amount Unpid:", font=("Arial", 11))
        self.doc_total_unpaid.grid(row=1, column=5)
        self.doc_total_paid = tk.Label(self.home_tab, text="Amount pid:", font=("Arial", 12))
        self.doc_total_paid.grid(row=2, column=5)
        self.doc_total_ = tk.Label(self.home_tab, text="Totale :", font=("Arial", 15))
        self.doc_total_.grid(row=3, column=5)
        
        self.chart1_title = tk.Label(self.home_tab, text="TOTAL ITEM COUNT :")
        self.chart1_title.grid(row=3, column=0)
        
        self.which_var = tk.StringVar()
        self.which_var.set("1")
        self.which_var.trace("w", on_style_selected)
        self.which_dropdown = tk.OptionMenu(self.home_tab, self.which_var, "0", "1", "2", "3")
        self.which_dropdown.grid(row=4, column=0, sticky="nsew")
        
        self.style_var = tk.StringVar()
        self.style_var.set("1")
        self.style_var.trace("w", on_style_selected)
        self.style_dropdown = tk.OptionMenu(self.home_tab, self.style_var, "1", "2", "3", "4")
        self.style_dropdown.grid(row=4, column=1, sticky="nsew")
        
        self.next_button = tk.Button(self.home_tab, text="<", font=("Arial", 12))
        self.next_button.grid(row=4, column=2, sticky="nsew")
        self.prev_button = tk.Button(self.home_tab, text=">", font=("Arial", 12))
        self.prev_button.grid(row=4, column=3, sticky="nsew")
        
        self.chart1_total_title = tk.Label(self.home_tab, text="TOTAL ITEM COUNT :")
        self.chart1_total_title.grid(row=3, column=4)

        self.style_var1 = tk.StringVar()
        self.style_var1.set("2")
        self.style_var1.trace("w", on_style_selected)
        self.style_dropdown1 = tk.OptionMenu(self.home_tab, self.style_var1, "1", "2", "3", "4")
        self.style_dropdown1.grid(row=4, column=4, sticky="nsew")
        
        self.next_button1 = tk.Button(self.home_tab, text="<", font=("Arial", 12))
        self.next_button1.grid(row=4, column=5, sticky="nsew")
        self.prev_button1 = tk.Button(self.home_tab, text=">", font=("Arial", 12))
        self.prev_button1.grid(row=4, column=6, sticky="nsew")
        
    

        self.Report_tab = ttk.Frame(self.Doc_tab)
        self.Report_tab.grid(row=6, column=0, columnspan=7, rowspan=3, sticky="nsew")
        
        # Add tabs to the self.center_notebook
        self.info_notebook.add(self.Report_tab, text='Report')

        self.perform_search()

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
        

    def close_tab(self, t_id):
        self.center_notebook.forget(t_id)
        

    def on_select(self, event):
        pass
    
    def display_products(self, products, ind):
            self.product_list.delete(0, tk.END)
            for product in products[ind]:
                self.product_list.insert(tk.END, f"{product[0]}  {product[1]}")

    def add_value_to_nested_dict(self, nested_dict, keys, value):
        current_dict = nested_dict 
        for key in keys[:-1]:
            #print("key :" + str(key))
            if key not in current_dict or not isinstance(current_dict[key], dict):
                #print("create new ")
                current_dict[key] = {}
            cuttrnt_dict = current_dict[key]
        last_key = keys[-1]
        if last_key not in current_dict:
            #print("create value 1")
            current_dict[last_key] = value
        else:
            #print("create value 2")
            current_dict[last_key] = value
            
    def fix_date(self):
        v = GetDateForm(self, self.date_from_Entry.get(), self.date_to_Entry.get())
        self.start_value = str(v.start_value[0])+"-"+str(v.start_value[1])+"-"+str(v.start_value[2])
        #datetime.strftime(v.start_value, '%Y-%m-%d %H:%M:%S')
        self.end_value = str(v.end_value[0])+"-"+str(v.end_value[1])+"-"+str(v.end_value[2])
        #datetime.strftime(v.end_value, '%Y-%m-%d %H:%M:%S')
        #print("v.start_value :" + str(self.start_value))
        #print("v.end_value :" + str(self.end_value))
        self.date_from_Entry.delete(0, tk.END)
        self.date_to_Entry.delete(0, tk.END)
        self.date_from_Entry.insert(0, self.start_value)
        self.date_to_Entry.insert(0, self.end_value)
        self.perform_search()

    def show_info_form(self):
        # call the function in the main file to show the first frame
        self.master.master.show_frame("InfoForm")
        
    
>>>>>>> db9ae79 (adding seller)

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
    def on_treeview_double_click(self, event):
        item = self.listbox.focus()  # Get the item that was clicked
<<<<<<< HEAD
        print("in dubleclicked")
=======
        #print("in dubleclicked")
>>>>>>> db9ae79 (adding seller)
        item_text = self.listbox.item(item, "values")  # Get the text values of the item
        id = self.listbox.item(item, "text")

        if item:
            # Detect double-click
<<<<<<< HEAD
            print("Double-clicked item:", item_text)
=======
            #print("Double-clicked item:", item_text)
>>>>>>> db9ae79 (adding seller)

            # Add tabs to the self.center_notebook
            if item_text[0]:
                tab_exist = any(self.center_notebook.tab(tab_id, "text") == item_text[0] for tab_id in self.center_notebook.tabs())
                if not tab_exist:
                    test_tab = ttk.Frame(self.center_notebook)
                    self.center_notebook.add(test_tab, text=item_text[0])
                    # Create a close button and position it at the top next to the tab title
                    close_button1 = tk.Button(test_tab, text="X", command=lambda : self.close_tab(test_tab))
                    close_button1.pack(side="top", anchor="ne", padx=5, pady=2)
                    doc_edit_form = DocEditForm(test_tab, item_text, id)
                    doc_edit_form.pack(fill="both", expand=True)
                else:
                    for a in self.center_notebook.tabs():
<<<<<<< HEAD
                        print("Tab already exists!")
                        print(str(self.center_notebook.tab(a, "text")))
=======
                        #print("Tab already exists!")
                        #print(str(self.center_notebook.tab(a, "text")))
                        pass
>>>>>>> db9ae79 (adding seller)

    def close_tab(self, t_id):
        self.center_notebook.forget(t_id)
        

    def on_select(self, event):
        pass
    
    def perform_print(self):
        item = self.listbox.focus()  # Get the item that was clicked
<<<<<<< HEAD
        print("in dubleclicked")
        item_text = self.listbox.item(item, "values")  # Get the text values of the item
        id = self.listbox.item(item, "text")

        if item:
            # Detect double-click
            print("Double-clicked item:", item_text)

            # Add tabs to the self.center_notebook
            if item_text[0]:
                doc_edit_form = load_slip(item_text, id)
                print("don loding slip : \n\n" + str(doc_edit_form))
                self.user = self.master.master.master.master.user
                PrinterForm.print_slip(self, doc_edit_form, 1) # TODO chack in setting if paper cut allowed

    # Function to perform the search and display the results in the listbox
    def perform_search(self):
=======
        if item:
            item_text = self.listbox.item(item, "values")  # Get the text values of the item
            id = self.listbox.item(item, "text")
            barcode = item_text[0]
            doc_ = cur.execute("SELECT * FROM doc_table WHERE doc_barcode=?", (barcode,)).fetchone()
            if doc_:
                #print(str(doc_))
                doc_edit_form = load_slip(doc_, id)
                #print("don loding slip : \n\n" + str(doc_edit_form))
                self.user = self.master.master.master.master.user
                PrinterForm.print_slip(self, self.user_info, doc_edit_form, 1) # TODO chack in setting if paper cut allowed

    # Function to perform the search and display the results in the listbox
    def perform_search(self):
        self.pyment_used = []
>>>>>>> db9ae79 (adding seller)
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
<<<<<<< HEAD
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
=======
        

        # Perform the search and update the listbox with the results
        df = search_documents(doc_id, doc_type, doc_barcode, extension_barcode, item, user_id, customer_id,
                            sold_item_info, discount, tax, self.date_from_Entry.get(), self.date_to_Entry.get(), self.doc_created_date_var.get(), self.doc_expire_date_var.get(), self.doc_updated_date_var.get())
        self.listbox.delete(*self.listbox.get_children())
        #self.get_columen()
        vv = []
        for index in df:
            item = self.listbox.insert('', 'end', text=index[0], values=(index[1], index[2], index[3], index[4], index[5], index[6], index[7], index[8], index[9], index[10], index[11], index[12], index[13], index[14]))
            self.load_payment(index[11])
            #print("df : " + str(index)
            #print("df : " + str(index[12]))
            dateandtime = index[12].split(" ") if " " in index[12] else index[12].split("_")
            hour = dateandtime[1].split(":")[0] if ":" in dateandtime[1] else dateandtime[1].split("-")[0]
            date = dateandtime[0].split("-")
            day = date[2]
            month = date[1]
            year = date[0]
            vv.append([year, month, day, hour, float(index[8])-float(index[9])])
>>>>>>> db9ae79 (adding seller)
            item = self.listbox.insert('', 'end', text=index[0], values=(index[1], index[2], index[3], index[4], index[5], index[6], index[7], index[8], index[9], index[10], index[11], index[12], index[13], index[14]))
            '''id = self.listbox.item(item, "text")
            item_text = self.listbox.item(item, "values")

            if item:
                # Detect double-click
                print("Double-clicked item:", item_text)

                # Add tabs to the self.center_notebook
                if item_text[0]:
                    tab_exist = any(self.center_notebook.tab(tab_id, "text") == item_text[0] for tab_id in self.center_notebook.tabs())
                    if not tab_exist:
                        test_tab = ttk.Frame(self.center_notebook)
                        self.center_notebook.add(test_tab, text=item_text[0])
                        # Create a close button and position it at the top next to the tab title
                        close_button1 = tk.Button(test_tab, text="X", command=lambda : self.close_tab(test_tab))
                        close_button1.pack(side="top", anchor="ne", padx=5, pady=2)
                        doc_edit_form = DocEditForm(test_tab, item_text, id)
                    else:
                        for a in self.center_notebook.tabs():
                            print("Tab already exists!")
                            print(str(self.center_notebook.tab(a, "text")))'''

<<<<<<< HEAD
=======
        if len(vv) > 0:
            #print(" v : " + str(vv))
            self.graph_value, self.graph_value0, tilte = make_list(vv)
        
            #print("self.graph_value0 :" + str(self.graph_value0))
            draw_cart(int(self.style_var.get()), self.chart_canvas, self.next_button, self.prev_button, self.graph_value0, int(self.which_var.get()), 1, 0)
            draw_cart(int(self.style_var.get()), self.chart2_canvas, None, None, self.graph_value0, int(self.which_var.get()), 2, 0)
            self.display_products(self.graph_value0, int(self.which_var.get()))
      
        self.creat_info()
            
>>>>>>> db9ae79 (adding seller)
