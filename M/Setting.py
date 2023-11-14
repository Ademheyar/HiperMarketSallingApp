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
from D.Getdefsize import ButtonEntryApp
from C.List import *
from D.printer import *

# Connect to the database or create it if it does not exist

import os
data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data'))
db_path = os.path.join(data_dir, 'my_database.db')
conn = sqlite3.connect(db_path)
cur = conn.cursor()

conn.commit()

import tkinter as tk
from D.Getdate import GetDateForm
from D.Chart.Chart import *
from D.Product.PrintPriceTag import PrintPriceTagFrame

from C.Product.selecttype import *

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
    
    print(query+"\n")
    # Execute the SQL query and return the results as a list of tuples
    cur.execute(query, (*given,))
    results = cur.fetchall()
    return results
# Example node hierarchy

class SettingForm(tk.Frame):
    def __init__(self, master, user):
        tk.Frame.__init__(self, master)
        self.master = master
        self.Product_notebook = ttk.Notebook(self)
        self.Product_notebook.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.nested_list = []
        self.user_info = None
        self.user = user
        
        # Create the frame for the product details Product_stting_frame
        self.Product_list_frame = tk.Frame(self.Product_notebook)
        self.Product_list_frame.pack()
        self.Product_notebook.add(self.Product_list_frame, text="Products Setting")

        # Create the frame for the search bar and buttons
        self.search_frame = tk.Frame(self.Product_list_frame)
        self.search_frame.pack(fill=tk.BOTH, padx=5, pady=5)
        
        self.inventory = []
        self.selected_type_path = None
        self.selected_type_path_parent = None
        self.tree = ttk.Treeview(self.search_frame, columns=
                                 ("Shop Name", "Code", "Color", "Size", "Barcode",
                                  "Qtyfirst", "Qty", "cdate", "update"))
        self.tree.grid(row=0, column=0, sticky=tk.E, columnspan=4)
        self.tree.bind('<<TreeviewSelect>>', self.on_path_select)
        #self.tree.pack(side=tk.LEFT, expand=True)
        self.tree.heading("#0", text="Shop Name", anchor=tk.W)
        self.tree.column("#0", stretch=tk.NO, minwidth=25, width=125)
        self.tree.heading("#1", text="Code", anchor=tk.W)
        self.tree.column("#1", stretch=tk.NO, minwidth=25, width=125)
        self.tree.heading("#2", text="Color", anchor=tk.W)
        self.tree.column("#2", stretch=tk.NO, minwidth=25, width=125)
        self.tree.heading("#3", text="Size", anchor=tk.W)
        self.tree.column("#3", stretch=tk.NO, minwidth=25, width=125)
        self.tree.heading("#4", text="Barcode", anchor=tk.W)
        self.tree.column("#4", stretch=tk.NO, minwidth=25, width=125)
        self.tree.heading("#5", text="Qtyfirst", anchor=tk.W)
        self.tree.column("#5", stretch=tk.NO, minwidth=25, width=125)
        self.tree.heading("#6", text="Qty", anchor=tk.W)
        self.tree.column("#6", stretch=tk.NO, minwidth=25, width=125)
        self.tree.heading("#7", text="cdate", anchor=tk.W)
        self.tree.column("#7", stretch=tk.NO, minwidth=25, width=125)
        self.tree.heading("#8", text="update", anchor=tk.W)
        self.tree.column("#8", stretch=tk.NO, minwidth=25, width=125)

        
        self.selected_label = tk.Label(self.search_frame, text='No selected')
        self.selected_label.grid(row=5, column=0, sticky=tk.E)
        
        self.type_value_label = tk.Label(self.search_frame, text='new value')
        self.type_value_label.grid(row=6, column=0, sticky=tk.E)
        self.type_value_entry = tk.Entry(self.search_frame)
        self.type_value_entry.grid(row=6, column=1, sticky=tk.E)

        self.add_new_button = tk.Button(self.search_frame, text='Add New', command=self.add_new_value)
        self.add_new_button.grid(row=7, column=0, sticky=tk.E)
        self.dele_type_button = tk.Button(self.search_frame, text='DELETE', command=self.dele_selected)
        self.dele_type_button.grid(row=7, column=1, sticky=tk.E)
        self.cear_button = tk.Button(self.search_frame, text='clear', command=self.clear_selected_path)
        self.cear_button.grid(row=8, column=0, sticky=tk.E)
        self.change_button = tk.Button(self.search_frame, text='Done', command=self.convert_to_text)
        self.change_button.grid(row=8, column=1, sticky=tk.E)
        
        self.types_label = tk.Label(self.search_frame, text='No value')
        self.types_label.grid(row=8, column=0, sticky=tk.E)


        
        self.Remamber_printer_int = tk.IntVar()
       
        self.Remamber_printer_entry = tk.Checkbutton(self.search_frame, text='Remamber Printer Choice', variable=self.Remamber_printer_int, command=self.chacke_remaber_printer)
        self.Remamber_printer_entry.grid(row=8, column=0, sticky=tk.E)


        self.ask_seller_int = tk.IntVar()
       
        self.ask_seller_entry = tk.Checkbutton(self.search_frame, text='ask seller', variable=self.ask_seller_int, command=self.chacke_ask_seller)
        self.ask_seller_entry.grid(row=9, column=0, sticky=tk.E)
        
        self.load_setting()




        
        
        self.list_box = ttk.Treeview(self.Product_list_frame)
        #self.list_box.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.list_box.bind('<<TreeviewSelect>>', self.on_select)

        self.list_box['columns'] = ("ID", "Name", "code", "type", "barcode", "at_shop", "quantity", "cost", "tax", "price", "include_tax", "price_change", "more_info", "images", "description", "service", "default_quantity", "active")
        self.list_box.column("#0", minwidth=0, width=0) 
        self.list_box.heading("#1", text="ID")
        self.list_box.heading("#2", text="Name")
        self.list_box.heading("#3", text="code")
        self.list_box.heading("#4", text="type")
        self.list_box.heading("#5", text="barcode")
        self.list_box.heading("#6", text="at_shop")
        self.list_box.heading("#7", text="quantity")
        self.list_box.heading("#8", text="cost")
        self.list_box.heading("#9", text="tax")
        self.list_box.heading("#10", text="price")
        self.list_box.heading("#11", text="include_tax")
        self.list_box.heading("#12", text="price_change")
        self.list_box.heading("#13", text="more_info")
        self.list_box.heading("#14", text="images")
        self.list_box.heading("#15", text="description")
        self.list_box.heading("#16", text="service")
        self.list_box.heading("#17", text="default_quantity")
        self.list_box.heading("#18", text="active")

        # Create the search bar

        # create a StringVar to represent the search box
        self.search_var = tk.StringVar()
        self.search_entry = tk.Entry(self.Product_list_frame, textvariable=self.search_var)
        self.search_entry.bind('<KeyRelease>', self.update_search_results)
        self.search_entry.pack(side=tk.LEFT, padx=5, pady=5)
            
        # bind the update_search_results function to the search box
        self.search_var.trace("w", self.update_search_results)
        # Create the list box
        
        # Add vertical scrollbar
        tree_scrollbar_y = ttk.Scrollbar(self.list_box, orient='vertical', command=self.list_box.yview)
        self.list_box.configure(yscrollcommand=tree_scrollbar_y.set)
        tree_scrollbar_y.pack(side='right', fill='y')

        # Add horizontal scrollbar
        tree_scrollbar_x = ttk.Scrollbar(self.list_box, orient='horizontal', command=self.list_box.xview)
        self.list_box.configure(xscrollcommand=tree_scrollbar_x.set)
        tree_scrollbar_x.pack(side='bottom', fill='x')

        self.notebook_frame = ttk.Notebook(self.list_box)
        self.notebook_frame.pack_forget()
        
        # Create the frame for the product details
        self.details_frame = tk.Frame(self.notebook_frame)
        self.details_frame.pack()
        self.notebook_frame.add(self.details_frame)


        # Create the widgets for the product details
        self.name_label = tk.Label(self.details_frame, text='Name:')
        self.name_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.E)
        self.name_entry = tk.Entry(self.details_frame)
        self.main_name = ""
        self.name_entry.bind('<KeyRelease>', lambda: self.on_name_entry)
        self.name_entry.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)

        self.type_label = tk.Label(self.details_frame, text='Type:')
        self.type_label.grid(row=2, column=0, padx=5, pady=5, sticky=tk.E)
        type_frame = tk.Frame(self.details_frame)
        type_frame.grid(row=2, column=1, padx=5, pady=5, sticky=tk.W)
        # get nodes by stting
        self.type_entry = NodeSelectorApp(type_frame, self.user)
        
        self.description_label = tk.Label(self.details_frame, text='Description:')
        self.description_label.grid(row=3, column=0, padx=5, pady=5, sticky=tk.E)
        self.description_entry = tk.Entry(self.details_frame)
        self.description_entry.grid(row=3, column=1, padx=5, pady=5, sticky=tk.W)
        self.service_change_var = tk.IntVar()
        self.service_change_entry = tk.Checkbutton(self.details_frame, text='service', variable=self.service_change_var)
        self.service_change_entry.grid(row=5, column=0, padx=5, pady=5, sticky=tk.W)
        self.default_quantity_change_var = tk.IntVar()
        self.default_quantity_change_entry = tk.Checkbutton(self.details_frame, text='Default Quantity', variable=self.default_quantity_change_var)
        self.default_quantity_change_entry.grid(row=6, column=0, padx=5, pady=5, sticky=tk.W)
        self.active_var = tk.IntVar()
        self.active_checkbutton = tk.Checkbutton(self.details_frame, text='Active', variable=self.active_var)
        self.active_checkbutton.grid(row=7, column=0, padx=5, pady=5, sticky=tk.W)

        # Create the frame for the product details
        self.tab2_frame = tk.Frame(self.notebook_frame)
        self.tab2_frame.pack_forget()
        self.notebook_frame.add(self.tab2_frame)

        self.cost_label = tk.Label(self.tab2_frame, text='Cost:')
        self.cost_label.grid(row=1, column=0, padx=5, pady=5, sticky=tk.E)
        self.cost_entry = tk.Entry(self.tab2_frame)
        self.cost_entry.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)
        self.cost_entry.insert(0, "0")
        self.mark_label = tk.Label(self.tab2_frame, text='mark:')
        self.mark_label.grid(row=2, column=0, padx=5, pady=5, sticky=tk.E)
        self.mark_entry = tk.Entry(self.tab2_frame)
        self.mark_entry.grid(row=2, column=1, padx=5, pady=5, sticky=tk.W)
        self.mark_entry.insert(0, "0")
        self.price_label = tk.Label(self.tab2_frame, text='Price:')
        self.price_label.grid(row=3, column=0, padx=5, pady=5, sticky=tk.E)
        self.price_entry = tk.Entry(self.tab2_frame)
        self.price_entry.grid(row=3, column=1, padx=5, pady=5, sticky=tk.W)
        self.price_entry.insert(0, "0")
        self.include_tax_var = tk.IntVar()
        self.include_tax_checkbutton = tk.Checkbutton(self.tab2_frame, text='Include Tax', variable=self.include_tax_var)
        self.include_tax_checkbutton.grid(row=4, column=0, padx=5, pady=5, sticky=tk.W)
        self.tax_label = tk.Label(self.tab2_frame, text='Tax:')
        self.tax_label.grid(row=5, column=0, padx=5, pady=5, sticky=tk.E)
        self.tax_entry = tk.Entry(self.tab2_frame)
        self.tax_entry.grid(row=5, column=1, padx=5, pady=5, sticky=tk.W)
        self.tax_entry.insert(0, "0")
        self.price_change_var = tk.IntVar()
        self.price_change_entry = tk.Checkbutton(self.tab2_frame, text='Price Change', variable=self.price_change_var)
        self.price_change_entry.grid(row=6, column=0, padx=5, pady=5, sticky=tk.W)
        
        # Create the frame for the product details
        self.tab3_frame = tk.Frame(self.notebook_frame)
        self.tab3_frame.pack_forget()
        self.notebook_frame.add(self.tab3_frame)

        # Create the list box
        self.more_info_label = tk.Entry(self.tab3_frame)
        self.more_info_label.grid(row=0, column=0, columnspan=4, sticky=tk.W)



        self.remove_info_button = tk.Button(self.tab3_frame, text='Remove', command=self.remove_info)
        self.remove_info_button.grid(row=7, column=0, sticky=tk.W)
        
        self.shop_name_label = tk.Label(self.tab3_frame, text='At Shop :')
        self.shop_name_label.grid(row=8, column=0, sticky=tk.W)
        self.shop_name_entry = tk.Entry(self.tab3_frame, )
        self.shop_name_entry.grid(row=8, column=1, sticky=tk.W)
        
        self.code_label = tk.Label(self.tab3_frame, text='Code:')
        self.code_label.grid(row=9, column=0, sticky=tk.W)
        self.code_entry = tk.Entry(self.tab3_frame)
        self.code_entry.grid(row=9, column=1, sticky=tk.W)

        
        self.color_label = tk.Label(self.tab3_frame, text='Color :')
        self.color_label.grid(row=10, column=0, sticky=tk.W)
        self.color_entry = tk.Entry(self.tab3_frame)
        self.color_entry.grid(row=10, column=1, sticky=tk.W)
        
        # for getting size
        
        self.sizeing_type_label = tk.Label(self.tab3_frame, text="Select Sizing Type:")
        self.sizeing_type_label.grid(row=11, column=0, sticky=tk.W)
        self.get_size_frame = tk.Frame(self.tab3_frame)
        self.get_size_frame.grid(row=11, column=1, sticky=tk.W)
        
        self.first_frame = tk.Frame(self.get_size_frame)
        self.first_frame.grid(row=0, column=0, sticky=tk.W)

        self.second_frame = tk.Frame(self.get_size_frame)
        self.second_frame.grid(row=0, column=1, sticky=tk.W)

        self.sizeing_type = tk.StringVar()  # Variable to store the selected sizing type
        self.sizeing_type.set("Select Sizing Type")
        
        sizing_options = ["Trouser Sizes", "Clothing Sizes", "Shoe Sizes"]

        self.sizing_var = tk.StringVar()
        self.sizing_var.set("Select Size Type")
        sizing_menu = tk.OptionMenu(self.first_frame, self.sizing_var, *sizing_options)
        sizing_menu.pack()

        self.create_form_button = tk.Button(self.first_frame, text="Create Form", command=self.create_sizes_form)
        self.create_form_button.pack(side=tk.LEFT)

        self.form_frame = tk.Frame(self.second_frame)  # Frame to hold the form entries
        self.form_frame.pack(pady=10)

        self.form_entries = []  # List to store the form entries
        


    
        self.size_label = tk.Label(self.tab3_frame, text='Size :')
        self.size_label.grid(row=12, column=0, sticky=tk.W)
        self.size_entry = tk.Entry(self.tab3_frame)
        self.size_entry.grid(row=12, column=1, sticky=tk.W)

        self.qty_label = tk.Label(self.tab3_frame, text='Quantity:')
        self.qty_label.grid(row=13, column=0, sticky=tk.W)
        self.qty_entry = tk.Entry(self.tab3_frame)
        self.qty_entry.grid(row=13, column=1, sticky=tk.W)
        self.bracode_label = tk.Label(self.tab3_frame, text='Barcode : ')
        self.bracode_label.grid(row=14, column=0, sticky=tk.W)
        self.bracode_entry = tk.Entry(self.tab3_frame)
        self.bracode_entry.grid(row=14, column=1, sticky=tk.W)
        
        self.images_label = tk.Label(self.tab3_frame, text='Images:')
        self.images_label.grid(row=15, column=0, sticky=tk.W)
        self.images_entry = tk.Entry(self.tab3_frame)
        self.images_entry.grid(row=15, column=1, sticky=tk.W)
        
        self.add_info_button = tk.Button(self.tab3_frame, text='Add', command=self.add_info)
        self.add_info_button.grid(row=22, column=0, sticky=tk.W)
      
        self.add_button = tk.Button(self.details_frame, text='Add', command=self.add_product)
        self.add_button.grid(row=30, column=0, padx=5, pady=5, sticky=tk.W)
        self.cancle_button = tk.Button(self.details_frame, text='Cancle', command=self.hide_add_product_forme)
        self.cancle_button.grid(row=30, column=1, padx=5, pady=5, sticky=tk.W)





        # Create the frame for the product details
        self.Product_listinfo_frame = tk.Frame(self.Product_notebook)
        self.Product_listinfo_frame.pack()
        self.Product_notebook.add(self.Product_listinfo_frame, text="Products Info")
        
        self.Product_listinfo_frame.grid_columnconfigure(0, weight=5)
        self.Product_listinfo_frame.grid_columnconfigure(1, weight=5)
        self.Product_listinfo_frame.grid_columnconfigure(2, weight=5)
        self.Product_listinfo_frame.grid_columnconfigure(3, weight=5)
        self.Product_listinfo_frame.grid_columnconfigure(4, weight=5)
        self.Product_listinfo_frame.grid_columnconfigure(5, weight=5)
        self.Product_listinfo_frame.grid_columnconfigure(6, weight=5)
        self.Product_listinfo_frame.grid_columnconfigure(7, weight=5)
        self.Product_listinfo_frame.grid_rowconfigure(0, weight=5)
        self.Product_listinfo_frame.grid_rowconfigure(1, weight=5)
        self.Product_listinfo_frame.grid_rowconfigure(2, weight=5)
        self.Product_listinfo_frame.grid_rowconfigure(3, weight=5)
        self.Product_listinfo_frame.grid_rowconfigure(4, weight=5)
        self.Product_listinfo_frame.grid_rowconfigure(5, weight=5)
        self.Product_listinfo_frame.grid_rowconfigure(6, weight=5)
        self.Product_listinfo_frame.grid_rowconfigure(7, weight=5)
        
        def on_style_selected(*args):
            draw_cart(int(self.style_var.get()), self.chart_canvas, self.next_button, self.prev_button, self.graph_value0, int(self.which_var.get()), 1, 0)
            draw_cart(int(self.style_var1.get()), self.chart2_canvas, self.next_button1, self.prev_button1, self.graph_value0, int(self.which_var.get()), 2, 0)
            self.display_products(self.graph_value0, int(self.which_var.get()))

        self.chart_canvas = tk.Canvas(self.Product_listinfo_frame)
        self.chart_canvas.grid(row=0, column=0, columnspan=3, sticky="nsew")
        
        self.chart2_canvas = tk.Canvas(self.Product_listinfo_frame)
        self.chart2_canvas.grid(row=0, column=4, columnspan=3, sticky="nsew")
        
        self.chart1_title = tk.Label(self.Product_listinfo_frame, text="TOTAL ITEM COUNT :")
        self.chart1_title.grid(row=1, column=0, columnspan=3)
        
        self.which_var = tk.StringVar()
        self.which_var.set("0")
        self.which_var.trace("w", on_style_selected)
        self.which_dropdown = tk.OptionMenu(self.Product_listinfo_frame, self.which_var, "0", "1", "2", "3")
        self.which_dropdown.grid(row=2, column=0, sticky="nsew")
        
        self.style_var = tk.StringVar()
        self.style_var.set("1")
        self.style_var.trace("w", on_style_selected)
        self.style_dropdown = tk.OptionMenu(self.Product_listinfo_frame, self.style_var, "1", "2", "3", "4")
        self.style_dropdown.grid(row=2, column=1, sticky="nsew")
        
        self.next_button = tk.Button(self.Product_listinfo_frame, text="<", font=("Arial", 12))
        self.next_button.grid(row=2, column=2, sticky="nsew")
        self.prev_button = tk.Button(self.Product_listinfo_frame, text=">", font=("Arial", 12))
        self.prev_button.grid(row=2, column=3, sticky="nsew")
        
        self.chart1_total_title = tk.Label(self.Product_listinfo_frame, text="TOTAL ITEM COUNT :")
        self.chart1_total_title.grid(row=1, column=4, columnspan=3)

        self.style_var1 = tk.StringVar()
        self.style_var1.set("2")
        self.style_var1.trace("w", on_style_selected)
        self.style_dropdown1 = tk.OptionMenu(self.Product_listinfo_frame, self.style_var1, "1", "2", "3", "4")
        self.style_dropdown1.grid(row=2, column=4, sticky="nsew")
        
        self.next_button1 = tk.Button(self.Product_listinfo_frame, text="<", font=("Arial", 12))
        self.next_button1.grid(row=2, column=5, sticky="nsew")
        self.prev_button1 = tk.Button(self.Product_listinfo_frame, text=">", font=("Arial", 12))
        self.prev_button1.grid(row=2, column=6, sticky="nsew")
        
        self.product_list = tk.Listbox(self.Product_listinfo_frame, width=30)
        self.product_list.grid(row=3, column=0, columnspan=2, sticky="nsew")
        
        self.details_frame = tk.Frame(self.Product_listinfo_frame)
        self.details_frame.grid(row=3, column=5, columnspan=3)
        

        
        #self.fix_date()
        # Create the label and entry for the document ID search
        self.total_item_label = tk.Label(self.details_frame, text="TOTAL ITEM COUNT :")
        self.total_item_label.grid(row=0, column=0)
        self.total_qty_label = tk.Label(self.details_frame, text="TOTAL QTY COUNT :")
        self.total_qty_label.grid(row=1, column=0)
        self.total_cost_label = tk.Label(self.details_frame, text="TOTAL COST :")
        self.total_cost_label.grid(row=2, column=0)
        self.total_sale_label = tk.Label(self.details_frame, text="TOTAL AFTER SALE :")
        self.total_sale_label.grid(row=3, column=0)

        
        # Pack the widgets for the product tab2
        #self.update_product_listbox()
        #
        #self.Item_To_Update()


    def chacke_remaber_printer(self):
        print("chacke_remaber_printer")
        if int(self.Remamber_printer_int.get()):
            b = cur.execute("SELECT * FROM setting WHERE User_id = ?", (self.user[0],)).fetchall()
            print("user " + str(self.user[0]) + " found " +str(b))
            printers = list_available_printers()
            if b and len(b) > 0 and b[0][3] == "" or not b:
                dialog = PrinterSelectionDialog(self, printers)
                self.wait_window(dialog)
                selected_printer = dialog.selected_printer
                if selected_printer:
                    if dialog.issave.get():
                        if b:
                            cur.execute('UPDATE setting SET printer=?, Get_printer=? WHERE User_id=?', ("", int(self.ask_seller_int.get()), self.user[0]))
                            # Commit the changes to the database
                            conn.commit()
                        else:
                            cur.execute('INSERT INTO setting (User_id, Get_printer, printer) VALUES (?, ?, ?, ?)', (self.user[0], int(self.ask_seller_int.get()), selected_printer))
                            # Commit the changes to the database
                            conn.commit()                    
        else:
            cur.execute('UPDATE setting SET printer=?, Get_printer=? WHERE User_id=?', ("t", int(self.ask_seller_int.get()), self.user[0]))
            # Commit the changes to the database
            conn.commit()
                
    def load_setting(self):
        #print("load sitting of : " + str(self.user))
        cur.execute("SELECT * FROM setting WHERE User_id = ?", (self.user[0],))
        sittings = cur.fetchall()
        if sittings:
            print("sitting2 : " + str(sittings))
            for sitting in sittings:
                if sitting[1] == self.user[0]:
                    self.load_type_info(sitting[4])
                    if sitting[5]:
                        self.ask_seller_int.set(int(sitting[5]))
                    if sitting[6]:
                        self.Remamber_printer_int.set(int(sitting[6]))
            
    def chacke_ask_seller(self):
        print("going to make seller ask or not...")
        cur.execute('UPDATE setting SET Get_seller=? WHERE user_id=?', (int(self.ask_seller_int.get()), self.user[0]))
        # Commit the changes to the database
        conn.commit()

        
    def show_Setting_Form(self):
        # call the function in the main file to show the first frame
        self.master.master.show_frame("SettingForm")
        
    def load_type_info(self, text):
        #print("loading type setting : " + str(text))
        if text and text != "":
            qty_info_list = load_list(text)
            def sub(ls, parent):
                for l in ls:
                    n = self.tree.insert(parent, "end", text=l[0])
                    sub(l[1], n)
            if qty_info_list:
                sub(qty_info_list, "")

    def dele_selected(self):
        item = self.tree.selection()[0]
        parent_item = self.tree.parent(item)
        self.tree.delete(item)
        self.selected_type_path = self.tree.parent(parent_item)
        txt = self.tree.item(self.selected_type_path, "text")
        self.load_path(parent_item, txt)

    def on_path_select(self, event):
        item = self.tree.selection()[0]
        parent_item = self.tree.parent(item)
        self.selected_type_path_parent = self.tree.parent(item)
        self.selected_type_path = item
        txt = self.tree.item(item, "text")
        self.load_path(parent_item, txt)
        
    def load_path(self, parent_item, text):
        while parent_item:
            text += " " + self.tree.item(parent_item, "text")
            parent_item = self.tree.parent(parent_item)
        self.selected_label.config(text=text)

    def clear_selected_path(self):
        self.selected_type_path = None
        self.selected_label.config(text="")
        
    
    def add_new_value(self):
        if self.selected_type_path:
            self.selected_type_path = self.tree.insert(self.selected_type_path, "end", text=self.type_value_entry.get())
        else:
            self.selected_type_path = self.tree.insert("", "end", text=self.type_value_entry.get())
        self.load_path(self.selected_type_path, "")
        
    # Create the "Change" button
    def build_nested_list(self, item):
        children = self.tree.get_children(item)
        if len(children) > 0:
            nested_list = []
            for child in children:
                child_text = self.tree.item(child, "text")
                nested_list.append([child_text, self.build_nested_list(child)])
            return nested_list
        else:
            return []
        
    def convert_to_text(self):
        nested_list = []
        for item in self.tree.get_children():
            child_text = self.tree.item(item, "text")
            nested_list.append([child_text, self.build_nested_list(item)])
        text = str(nested_list)
        self.types_label.config(text=text)
        cur.execute('UPDATE setting SET Items_type=? WHERE user_name=?', (text, self.user[3]))
        # Commit the changes to the database
        conn.commit()



    
    def create_sizes_form(self):
        selected_type = self.sizing_var.get()
        if selected_type == "Select Sizing Type":
            return

        self.form_frame.destroy()  # Clear previous form entries

        self.form_frame = tk.Frame(self.second_frame)
        self.form_frame.pack(pady=10)

        self.form_entries = []  # Reset the list of form entries

        sizes_label = tk.Label(self.form_frame, text="Enter Quantities for the Sizes:")
        sizes_label.pack()

        sizes_text = tk.Text(self.form_frame, height=5, width=40)
        sizes_text.pack()

        sizes = []
        if selected_type == "Trouser Sizes":
            sizes = [str(size) + ":0" for size in range(21, 46)]
        elif selected_type == "Clothing Sizes":
            sizes = ["XS:0", "S:0", "M:0", "L:0", "XL:0", "2XL:0", "3XL:0", "4XL:0", "5XL:0"]
        elif selected_type == "Shoe Sizes":
            sizes = [str(size) + ":0" for size in range(1, 13)] + [str(a) + ":0" for a in range(30, 45)]

        for size in sizes:
            sizes_text.insert(tk.END, size + ", ")

        done_button = tk.Button(self.form_frame, text="Done", command=lambda: self.generate_list(selected_type, sizes_text.get("1.0", tk.END)))
        done_button.pack()

    def generate_list(self, sizing_type, sizes):
        sizes_list = sizes.strip().split(",")  # Split the entered sizes by comma
        sizes_list = [size.strip() for size in sizes_list]  # Remove leading/trailing whitespaces

        self.result = []
        for size in sizes_list:
            size_parts = size.split(":")
            if len(size_parts) == 2:
                size_value = size_parts[0].strip()
                quantity = size_parts[1].strip()
                if quantity != "0":
                    self.result.append([size_value, quantity])
                    
        for v in self.result:
            found = 0 
            i = 0
            for p in self.inventory:
                if p["shop_name"] == self.shop_name_entry.get() and p["color"] == self.color_entry.get() and \
                p["size"] == v[0]:
                    if p["barcode"] == self.bracode_entry.get() and p["qtyfirst"] == v[1] and \
                        p["qty"] == v[1]:
                        print("issame!!!" + str(p)) # TODO: show same earror
                        #    cdate#    update
                    else:
                        self.inventory[i]["barcode"] = self.bracode_entry.get()
                        self.inventory[i]["qty"] = v[1]
                    found = 1
                else:
                    found = 0
                i += 1
            # TODO add stock pathern in this new list
            found, self.nested_list = add_new_list(self.nested_list, self.shop_name_entry.get() + "|" + self.code_entry.get() + "|" + self.color_entry.get() + "|" + v[0], [self.bracode_entry.get(), v[1], v[1], "", self.images_entry.get(), "", ""])
            if found:
                self.add_info_(self.shop_name_entry.get(), self.code_entry.get(), self.color_entry.get(), v[0], self.bracode_entry.get(), v[1], v[1], "", "")
        txt = self.get_inventory_nested_list_text()
        self.more_info_label.delete(0, tk.END)
        self.more_info_label.insert(0, txt)

        
        
    def Item_To_Update(self):
        #self.info_tab = None
        # Notebook widget - CENTER_NOTEBOK

        self.Item_To_Update_tab = ttk.Frame(self.Product_notebook)
        self.Item_To_Update_tab.grid()

        # Add tabs to the self.center_notebook
        self.Product_notebook.add(self.Item_To_Update_tab, text='Item_To_Update')

        self.Item_To_Update_tab.grid_columnconfigure(0, weight=5)
        self.Item_To_Update_tab.grid_columnconfigure(1, weight=5)
        self.Item_To_Update_tab.grid_columnconfigure(2, weight=5)
        self.Item_To_Update_tab.grid_columnconfigure(3, weight=5)
        self.Item_To_Update_tab.grid_columnconfigure(4, weight=5)
        self.Item_To_Update_tab.grid_columnconfigure(5, weight=5)
        self.Item_To_Update_tab.grid_columnconfigure(6, weight=5)
        self.Item_To_Update_tab.grid_rowconfigure(0, weight=5)
        self.Item_To_Update_tab.grid_rowconfigure(1, weight=5)
        self.Item_To_Update_tab.grid_rowconfigure(2, weight=5)
        self.Item_To_Update_tab.grid_rowconfigure(3, weight=5)
        self.Item_To_Update_tab.grid_rowconfigure(4, weight=5)
        
        self.Item_To_Update_tab_details_frame = tk.Frame(self.Item_To_Update_tab)
        self.Item_To_Update_tab_details_frame.grid(row=0, column=0, columnspan=6)

        
        # Create the label and entry for the document expire date search
        self.Item_To_Update_tab_date_entry = tk.Label(self.Item_To_Update_tab_details_frame, text="Document Updated Date:")
        self.Item_To_Update_tab_date_entry.grid(row=2, column=5)
        self.Item_To_Update_tab_entry = tk.Entry(self.Item_To_Update_tab_details_frame)
        self.Item_To_Update_tab_entry.grid(row=3, column=5)

        # Create the search button
        self.Item_To_Update_tab_search_button = tk.Button(self.Item_To_Update_tab_details_frame, text="Search", command=self.perform_search)
        self.Item_To_Update_tab_search_button.grid(row=3, column=6)

        # Create the search button
        self.Item_To_Update_tab_print_button = tk.Button(self.Item_To_Update_tab_details_frame, text="Print", command=self.perform_print)
        self.Item_To_Update_tab_print_button.grid(row=4, column=1)

        self.Item_To_Update_tab_upload_button = tk.Button(self.Item_To_Update_tab_details_frame, text="Refresh", bg="red", fg="white", font=("Arial", 12), command=lambda: self.perform_search_Item_size_chack())
        self.Item_To_Update_tab_upload_button.grid(row=4, column=2)


        # Create the listbox to display search results
        self.Item_To_Update_tab_listbox = ttk.Treeview(self.Item_To_Update_tab)        
        self.Item_To_Update_tab_listbox.bind('<<TreeviewSelect>>', self.on_select)
        #self.listbox.bind("<Button-1>", self.on_treeview_double_click)
        #self.listbox.grid_propagate(False)


        # Add vertical scrollbar
        tree_scrollbar_y = ttk.Scrollbar(self.Item_To_Update_tab_listbox, orient='vertical', command=self.Item_To_Update_tab_listbox.yview)
        self.Item_To_Update_tab_listbox.configure(yscrollcommand=tree_scrollbar_y.set)
        tree_scrollbar_y.pack(side='right', fill='y')

        # Add horizontal scrollbar
        tree_scrollbar_x = ttk.Scrollbar(self.Item_To_Update_tab_listbox, orient='horizontal', command=self.Item_To_Update_tab_listbox.xview)
        self.Item_To_Update_tab_listbox.configure(xscrollcommand=tree_scrollbar_x.set)
        tree_scrollbar_x.pack(side='bottom', fill='x')

        # Set the size of the self.listbox widget
        self.Item_To_Update_tab_listbox.grid(row=1, column=0, rowspan=3, columnspan=5, sticky="nsew")
        self.get_columen_()
        
        # New listbox in the main frame
        self.Item_To_Update_tab_list_items = tk.Listbox(self.Item_To_Update_tab, bg="yellow", height=17)
        self.Item_To_Update_tab_list_items.grid(row=1, column=5, rowspan=2, sticky="nsew")
        '''self.doc_total_unpaid = tk.Label(self.home_tab, text="Amount Unpid:", font=("Arial", 11))
        self.doc_total_unpaid.grid(row=3, column=5)
        self.doc_total_paid = tk.Label(self.home_tab, text="Amount pid:", font=("Arial", 12))
        self.doc_total_paid.grid(row=4, column=5)
        self.doc_total_ = tk.Label(self.home_tab, text="Totale :", font=("Arial", 15))
        self.doc_total_.grid(row=5, column=5)'''

        # show the Payment Form window
















        
    def get_columen_(self):
        self.Item_To_Update_tab_listbox['columns'] = ('doc_barcode', 'extension_barcode', 'user_id', 'customer_id', 'Type', 'Itmes', 'Qty', 'Paymen', 'price', 'disc', 'tax', 'doc_created_date', 'doc_expire_date', 'doc_updated_date')
        self.Item_To_Update_tab_listbox.heading("#0", text="ID")
        self.Item_To_Update_tab_listbox.column("#0", stretch=tk.NO, minwidth=25, width=50) 
        self.Item_To_Update_tab_listbox.heading("#1", text="doc_barcode")
        self.Item_To_Update_tab_listbox.column("#1", stretch=tk.NO, minwidth=25, width=100) 
        self.Item_To_Update_tab_listbox.heading("#2", text="extension_barcode")
        self.Item_To_Update_tab_listbox.column("#2", stretch=tk.NO, minwidth=25, width=100) 
        self.Item_To_Update_tab_listbox.heading("#3", text="user_id")
        self.Item_To_Update_tab_listbox.column("#3", stretch=tk.NO, minwidth=25, width=100) 
        self.Item_To_Update_tab_listbox.heading("#4", text="customer_id")
        self.Item_To_Update_tab_listbox.column("#4", stretch=tk.NO, minwidth=25, width=100) 
        self.Item_To_Update_tab_listbox.heading("#5", text="Type")
        self.Item_To_Update_tab_listbox.column("#5", stretch=tk.NO, minwidth=25, width=80) 
        self.Item_To_Update_tab_listbox.heading("#6", text="Itmes")
        self.Item_To_Update_tab_listbox.column("#6", stretch=tk.NO, minwidth=25, width=100) 
        self.Item_To_Update_tab_listbox.heading("#7", text="Qty")
        self.Item_To_Update_tab_listbox.column("#7", stretch=tk.NO, minwidth=25, width=100) 
        self.Item_To_Update_tab_listbox.heading("#8", text="price")
        self.Item_To_Update_tab_listbox.column("#8", stretch=tk.NO, minwidth=25, width=50) 
        self.Item_To_Update_tab_listbox.heading("#9", text="disc")
        self.Item_To_Update_tab_listbox.column("#9", stretch=tk.NO, minwidth=25, width=50) 
        self.Item_To_Update_tab_listbox.heading("#10", text="tax")
        self.Item_To_Update_tab_listbox.column("#10", stretch=tk.NO, minwidth=25, width=50) 
        self.Item_To_Update_tab_listbox.heading("#11", text="Payment")
        self.Item_To_Update_tab_listbox.column("#11", stretch=tk.NO, minwidth=25, width=100) 
        self.Item_To_Update_tab_listbox.heading("#12", text="doc_created_date")
        self.Item_To_Update_tab_listbox.column("#12", stretch=tk.NO, minwidth=25, width=100) 
        self.Item_To_Update_tab_listbox.heading("#13", text="doc_expire_date")
        self.Item_To_Update_tab_listbox.column("#13", stretch=tk.NO, minwidth=25, width=100) 
        self.Item_To_Update_tab_listbox.heading("#14", text="doc_updated_date")
        self.Item_To_Update_tab_listbox.column("#14", stretch=tk.NO, minwidth=25, width=100) 

    def perform_search_Item_size_chack(self):
        cur.execute('SELECT * FROM product')
        item = cur.fetchall()
        for it in item:
            print("item["+str(it[0])+"]  : " + str(it[12]))
            qty_info_list = []
            if "\"{" in str(it[12]):
                qty_info_list = read_code(it[12], "", str(it[2]), "", "")[4]
            else:
                qty_info_list = load_list(it[12])
            
            def sub_list(ls):
                main_name = []
                for l in ls:
                    if len(l) > 2:
                        # chacke size has problame
                        if float(l[2]) < 0:
                            self.Item_To_Update_tab_listbox.insert("", 'end', text="Size", values=(it[1], it[2], it[3], it[4], it[5], it[6], it[7], it[8], it[9], it[10], it[11], it[12], it[13], it[14]))
                        
                    elif len(l) == 2:
                        #main_name.append(l[0])
                        sub_list(l[1])
            sub_list(qty_info_list)
                
    
    def perform_print(self):
        # todo make it print by catagory
        print_slip = "Name   |  code    |       "
        for item in self.Item_To_Update_tab_listbox.get_children():
            item_text = self.Item_To_Update_tab_listbox.item(item, "values")
            print_slip += item_text[0] + "  :  " + item_text[1] + "\n"
        self.user = self.master.user
        PrinterForm.print_slip(self, print_slip, 1) # TODO chack in setting if paper cut allowed

    def perform_search(self):
        self.pyment_used = []
        # Get the search criteria from the entry boxes
        doc_id = self.doc_id_entry.get()
        doc_type = self.type_entry.get_value  #"self.doc_type_entry.get()"
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
                    print("new payment :" + str([pay_type, pay_pid]))
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
        
    def display_products(self, products, ind):
            self.product_list.delete(0, tk.END)
            for product in products[ind]:
                self.product_list.insert(tk.END, f"{product[0]}  {product[1]}")
                
    def format_price(self, price):
        suffixes = ['Hundred', 'Thousand', 'Million', 'Billion']
        suffic_index = 0
        nprice = price
        while nprice >= 1000 and suffic_index < len(suffixes):
            nprice /= 1000
            suffic_index += 1
        if suffic_index == 0:
            formatted_price = "{:,.0f} {}".format(nprice *100, suffixes[suffic_index])
        else:
            formatted_price = "{:,.2f} {}".format(nprice, suffixes[suffic_index])
        return formatted_price

    def add_info_(self, shop_name, code, color, size, barcode, qtyfirst, qty, stock, img, cdate, update):
        p = {"shop_name": shop_name, "code": code, "color": color, "size": size, "barcode": barcode, "qtyfirst": qtyfirst, "qty": qty, "cdate": cdate, "update": update}
        self.inventory.append(p)
        self.update_tree()

    def get_unique_shop_names(self):
        return list(set([p["shop_name"] for p in self.inventory]))

    def get_unique_codes_for_shop_name(self, shop_name):
        return list(set([p["code"] for p in self.inventory if p["shop_name"] == shop_name]))

    def get_unique_colors_for_shop_name(self, shop_name, code):
        return list(set([p["color"] for p in self.inventory if p["shop_name"] == shop_name and p["code"] == code]))

    def get_sizes_for_shop_name_and_color(self, shop_name, code, color):
        return list(set([p["size"] for p in self.inventory if p["shop_name"] == shop_name and p["code"] == code and p["color"] == color]))

    def get_barcode_and_qty_for_shop_name_and_color_and_size(self, shop_name, code, color, size):
        for p in self.inventory:
            if p["shop_name"] == shop_name and p["code"] == code and p["color"] == color and p["size"] == size:
                return (p["barcode"], p["qtyfirst"], p["qty"], p["cdate"], p["update"])
        return (None, None)
    
    def chang_to_list(self, vs_info):
        '''a_u_list = []
        t = vs_info.replace("\"", "") + ","
        main_info = t.split("},")
        for m in range(len(main_info)-1):
            main_value = main_info[m].split(",(")
            shop_name = main_value[0].replace("{", "")
            shop = [shop_name]
            shop_node = []
            t = main_value[1].replace(")", "") + ","
            f_info = t.split(">,")
            for c in range(len(f_info)-1):
                f_value = f_info[c].split(",[")
                color_txt = f_value[0].replace("<", "")
                color = [color_txt]
                color_node = []
                t = f_value[1].replace("]", "") + ","
                s_info = t.split("|,")
                for s in range(len(s_info)-1):
                    s_value = s_info[s].split(", ")
                    s_n = []
                    for s_v in s_value:
                        s_n.append(s_v.replace("|", ""))
                    color_node.append(s_n)
                color.append(color_node)
                shop_node.append(color)
            shop.append(shop_node)
            a_u_list.append(shop)
        return a_u_list'''

    def chang_to_text(self, a_u_list):
        '''vs_info = "\""
        si = 0
        for s in a_u_list:
            si += 1
            vs_info += '{'
            vs_info += s[0]
            vs_info += ',('
            ci = 0
            for c in s[1]:
                ci += 1
                vs_info += '<'
                vs_info += c[0]
                vs_info += ',['
                sei = 0
                for se in c[1]:
                    vs_info += '|'
                    sei += 1
                    for j in range(len(se)):
                        vs_info += se[j]
                        if j < len(se)-1:
                            vs_info += ', '
                    if sei < len(c[1])-1:
                        vs_info += ',|'
                    else:
                        vs_info += '|'
                vs_info += ']'
                if ci < len(s[1])-1:
                    vs_info += ',>'
                else:
                    vs_info += '>'
            vs_info += ')'
            if si < len(a_u_list)-1:
                vs_info += ',}'
            else:
                vs_info += '}'
        vs_info += "\""
        return vs_info'''
    
    def add_product_from_nested_list(self, nested_list):
        for s in nested_list:
            if not s:
                break
            shop_name, nested_items = s
            color, nested_items2 = nested_items
            size, nested_items3 = nested_items2
            print("shop name : " + shop_name)
            print("shop nested_item : " + str(nested_items))
            barcode, qtyfirst, qty, cdate, update = nested_items3
            self.add_info_(shop_name, color, size, barcode, qtyfirst, qty, cdate, update)
    
    def get_inventory_nested_list(self, text, code):
        '''nested_list = []
        unique_shop_names = self.get_unique_shop_names()
        for shop_name in unique_shop_names:
            shop_node = [shop_name]
            unique_colors = self.get_unique_colors_for_shop_name(shop_name)
            shop_subnode = []
            for color in unique_colors:
                color_nodes = [color]
                sizes = self.get_sizes_for_shop_name_and_color(shop_name, color)
                color_subnodes = []
                for size in sizes:
                    barcode, qtyfirst, qty, cdate, update = self.get_barcode_and_qty_for_shop_name_and_color_and_size(shop_name, color, size)
                    color_subnodes.append([size, barcode, qtyfirst, qty, cdate, update])
                color_nodes.append(color_subnodes)
                shop_subnode.append(color_nodes)
            shop_node.append(shop_subnode)
            nested_list.append(shop_node)
        return nested_list'''
        if "\"{" in str(text):
            self.nested_list = read_code(text, "", str(code), "", "")[4]
        else:
            self.nested_list = load_list(text) 

    def get_inventory_nested_list_text(self): # change tree vew nested list to text
        '''vs_info = '\"'
        unique_shop_names = self.get_unique_shop_names()
        s = 0
        for shop_name in unique_shop_names:
            vs_info += '{'
            vs_info += shop_name + ',('
            unique_colors = self.get_unique_colors_for_shop_name(shop_name)
            c = 0
            for color in unique_colors:
                vs_info += '<'
                vs_info += color + ',['
                sizes = self.get_sizes_for_shop_name_and_color(shop_name, color)
                i = 0
                for size in sizes:
                    vs_info += '|' 
                    vs_info += size + ','
                    v, n, m, g, y = self.get_barcode_and_qty_for_shop_name_and_color_and_size(shop_name, color, size)
                    vs_info += str(v + "," + n + "," + m + "," + g + "," + y)
                    if i < len(sizes)-1:
                        vs_info += '|,'
                    else:
                        vs_info += '|'
                    i += 1
                vs_info += ']'
                if c < len(unique_colors)-1:
                    vs_info += '>,'
                else:
                    vs_info += '>'
                c += 1 
            vs_info += ')'
            if s < len(unique_shop_names)-1:
                vs_info += '},'
            else:
                vs_info += '}'
            s += 1
        vs_info += '\"'
        return vs_info'''
        return str(self.nested_list)
    
    def update_tree(self):
        self.tree.delete(*self.tree.get_children())
        print("gount tot add tree ")
        for shop in self.nested_list:
            print("shop")
            shop_name_node = self.tree.insert("", "end", text=shop[0])
            for code in shop[1]:
                print("code")
                code_node = self.tree.insert(shop_name_node, "end", text=code[0])
                for color in code[1]:
                    color_node = self.tree.insert(code_node, "end", text=color[0])
                    for size in color[1]:
                        size_node = self.tree.insert(color_node, "end", text=size[0])
                        for value in size[1]:
                            print("value : " + str(value))
                            barcode, qtyfirst, qty, patern, imgs, cdate, update = value
                            if barcode and qtyfirst and qty and cdate and update:
                                self.tree.insert(size_node, "end", text=value[0], values=(barcode, qtyfirst, qty, cdate, update))
                            else:
                                self.tree.insert(size_node, "end", text=value[0])
                            
    def remove_info(self):
        """self.more_info_label = tk.Label(self.tab3_frame, text='More Info:')
        self.more_info_label.grid(row=1, column=0, sticky=tk.E)

        self.list_box2 = ttk.Treeview(self.tab3_frame)
        self.list_box2.grid(row=2, column=0, sticky=tk.E)

        self.shop_name_entry = tk.Entry(self.tab3_frame)
        self.color_label = tk.Label(self.tab3_frame, text='Price Change:')
        self.color_label.grid(row=8, column=0, sticky=tk.E)
        self.color_entry = tk.Entry(self.tab3_frame)
        self.color_entry.grid(row=8, column=1, sticky=tk.E)
        self.size_label = tk.Label(self.tab3_frame, text='Price Change:')
        self.size_label.grid(row=9, column=0, sticky=tk.E)
        self.size_entry = tk.Entry(self.tab3_frame)
        self.size_entry.grid(row=9, column=1, sticky=tk.E)
        self.qty_label = tk.Label(self.tab3_frame, text='Quantity:')
        self.qty_label.grid(row=10, column=0, sticky=tk.E)
        self.qty_entry = tk.Entry(self.tab3_frame)
        self.qty_entry.grid(row=10, column=1, sticky=tk.E)
        self.bracode_label = tk.Label(self.tab3_frame, text='Barcode : ')
        self.bracode_label.grid(row=11, column=0, sticky=tk.E)
        self.bracode_entry = tk.Entry(self.tab3_frame)
        self.bracode_entry.grid(row=11, column=1, sticky=tk.E)
        for a in self.tree.get_children():
            self.tree.delete(a)
            for a in self.list_items.selection():
            self.list_items.delete(a)
        self.update_info()
        self.update_info()
        """
        found = 0 
        i = 0
        for a in self.tree.selection():
            print(str(self.tree.item(a)))
            for p in self.inventory:
                if p["shop_name"] == self.shop_name_entry.get() and p["color"] == self.color_entry.get() and \
                p["size"] == self.size_entry.get():
                    if p["barcode"] == self.bracode_entry.get() and p["qtyfirst"] == self.qty_entry.get() and \
                        p["qty"] == self.qty_entry.get():
                        print("issame!!!" + str(p)) # TODO: show same earror
                        #    cdate#    update
                    else:
                        self.inventory[i]["barcode"] = self.bracode_entry.get()
                        self.inventory[i]["qty"] = self.qty_entry.get()
                    found = 1
                else:
                    found = 0
                i += 1
            self.tree.delete(a)
        
        found, self.nested_list = dele_list(self.nested_list, self.shop_name_entry.get() + "|" + self.code_entry.get() + "|" + self.color_entry.get() + "|" + self.size_entry.get() , [self.bracode_entry.get(), self.qty_entry.get(), self.qty_entry.get(), "", self.images_entry.get(), "", ""])
        txt = self.get_inventory_nested_list_text()
        #l = self.get_inventory_nested_list()
        #print("list : " + str(l))
        #txt = self.chang_to_text(l)
        #print("list : " + str(txt))
        #le = self.chang_to_list(txt)
        #print("le :" + str(le))
        self.more_info_label.delete(0, tk.END)
        self.more_info_label.insert(0, txt)
        
    def add_info(self):
        """self.more_info_label = tk.Label(self.tab3_frame, text='More Info:')
        self.more_info_label.grid(row=1, column=0, sticky=tk.E)

        self.list_box2 = ttk.Treeview(self.tab3_frame)
        self.list_box2.grid(row=2, column=0, sticky=tk.E)

        self.shop_name_entry = tk.Entry(self.tab3_frame)
        self.color_label = tk.Label(self.tab3_frame, text='Price Change:')
        self.color_label.grid(row=8, column=0, sticky=tk.E)
        self.color_entry = tk.Entry(self.tab3_frame)
        self.color_entry.grid(row=8, column=1, sticky=tk.E)
        self.size_label = tk.Label(self.tab3_frame, text='Price Change:')
        self.size_label.grid(row=9, column=0, sticky=tk.E)
        self.size_entry = tk.Entry(self.tab3_frame)
        self.size_entry.grid(row=9, column=1, sticky=tk.E)
        self.qty_label = tk.Label(self.tab3_frame, text='Quantity:')
        self.qty_label.grid(row=10, column=0, sticky=tk.E)
        self.qty_entry = tk.Entry(self.tab3_frame)
        self.qty_entry.grid(row=10, column=1, sticky=tk.E)
        self.bracode_label = tk.Label(self.tab3_frame, text='Barcode : ')
        self.bracode_label.grid(row=11, column=0, sticky=tk.E)
        self.bracode_entry = tk.Entry(self.tab3_frame)
        self.bracode_entry.grid(row=11, column=1, sticky=tk.E)
        """
        found = 0 
        i = 0
        for p in self.inventory:
            if p["shop_name"] == self.shop_name_entry.get() and p["color"] == self.color_entry.get() and \
               p["size"] == self.size_entry.get():
                if p["barcode"] == self.bracode_entry.get() and p["qtyfirst"] == self.qty_entry.get() and \
                    p["qty"] == self.qty_entry.get():
                    print("issame!!!" + str(p)) # TODO: show same earror
                    #    cdate#    update
                else:
                    self.inventory[i]["barcode"] = self.bracode_entry.get()
                    self.inventory[i]["qty"] = self.qty_entry.get()
                found = 1
            else:
                found = 0
            i += 1

        #{'shop_name': '1', 'color': '2', 'size': '3', 'barcode': '4', 'qtyfirst': '4', 'qty': '4', 'cdate': '', 'update': ''}
                #return (p["barcode"], p["qtyfirst"], p["qty"], p["cdate"], p["update"])
        found, self.nested_list = add_new_list(self.nested_list, self.shop_name_entry.get() + "|" + self.code_entry.get() + "|" + self.color_entry.get() + "|" + self.size_entry.get() , [self.bracode_entry.get(), self.qty_entry.get(), self.qty_entry.get(), "", self.images_entry.get(), "", ""])
        print("self.nested_list : " + str(self.nested_list))
        if found:
            self.add_info_(self.shop_name_entry.get(), self.code_entry.get(), self.color_entry.get(), self.size_entry.get(), self.bracode_entry.get(), self.qty_entry.get(), self.qty_entry.get(), "", self.images_entry.get(), "", "")
            
            

        txt = self.get_inventory_nested_list_text()
        #l = self.get_inventory_nested_list()
        #print("list : " + str(l))
        #txt = self.chang_to_text(l)
        #print("list : " + str(txt))
        #le = self.chang_to_list(txt)
        #print("le :" + str(le))
        self.more_info_label.delete(0, tk.END)
        self.more_info_label.insert(0, txt)
        

        
    
    # Create the "Delete" button
    
    # Define the function for deleting a product
    def delete_product(self):
        # Get the selected product from the listbox
        for selected_product in self.list_box.selection():
            # Get the ID of the selected product
            product_id = self.list_box.item(selected_product)['text']
            # Delete the product from the database
            cur.execute('DELETE FROM product WHERE id=?', (int(product_id),))


            # Clear the product details widgets
            self.clear_product_details_widget()

            # Update the product listbox
            self.update_product_listbox()

    def get_item_by_code(self, item_code):
        self.cursor.execute("SELECT * FROM product WHERE code=?", (item_code,))
        result = self.cursor.fetchone()
        return result
    
    def update_item_info(self, id, code, it_info):
        pass




    
    def search_products(self, search_text):
        # Search for the entered text in the code, name, barcode, and type fields of the product table
        cur.execute("SELECT * FROM product WHERE code LIKE ? OR name LIKE ? OR barcode LIKE ? OR type LIKE ?", 
                    ('%' + search_text + '%', '%' + search_text + '%', '%' + search_text + '%', '%' + search_text + '%'))
        results = cur.fetchall()
        return results

    # create a function to update the search results whenever the search box changes
    def update_search_results(self, *args):
        # get the search string from the search box
        search_str = self.search_var.get()
        
        # search for products based on the search string
        products = self.search_products(search_str)
        
        # clear the current items in the list box
        self.list_box.delete(*self.list_box.get_children())

        # Add the products to the product listbox
        for product in products:
            self.list_box.insert('', 'end', values=(product[0], product[1], product[2], product[3], product[4], product[5], product[6],product[7], product[8], product[9], product[10], product[11], product[12], product[13],product[14], product[15], product[16], product[17]))
        
    # Define the function for updating the product listbox
    def update_product_listbox(self):
        # Clear the product listbox
        self.list_box.delete(*self.list_box.get_children())
        # Get the products from the database
        cur.execute('SELECT * FROM product')
        products = cur.fetchall()
        items = 0
        TQTY = 0
        Tprice = 0
        Tcost = 0
        vv = []
        item = cur.fetchall()
        for product in products:
            self.list_box.insert('', 'end', values=(product[0], product[1], product[2], product[3], product[4], product[5], product[6],product[7], product[8], product[9], product[10], product[11], product[12], product[13],product[14], product[15], product[16], product[17]))
            chacksize = 0
            cost = float(product[7])
            price = float(product[9])
            qty_info_list = []
            if "\"{" in str(product[12]):
                qty_info_list = read_code(product[12], "", str(product[2]), "", "")[4]
            else:
                qty_info_list = load_list(product[12])
            items += 1
            qty = 0
            def sub_list(ls, qty):
                main_name = []
                for l in ls:
                    if len(l) > 2:
                        qty += float(l[2])
                    elif len(l) == 2:
                        #main_name.append(l[0])
                        qty = sub_list(l[1], qty)
                return qty
            qty = sub_list(qty_info_list, qty)
            vv.append([str(product[0]), float(price)])
            # TODO make user choosh in which name, code, id
            if qty > 0:
                #print("Calculating : " + "qty " + str(qty) + "*" + str(price) + " price = " + str(qty*price) + "  AND QTY * " + str(cost) + " Cost = " + str(qty*cost))
                #print("equal Tprice : " + str(Tprice) + " Cost :" + str(Tcost))
                Tprice += qty*price
                Tcost += qty*cost
                TQTY += qty
        if len(vv) > 0:
            self.graph_value, self.graph_value0, tilte = make_list(vv)
        
            print("pself.graph_value0 :" + str(self.graph_value0))
            draw_cart(int(self.style_var.get()), self.chart_canvas, self.next_button, self.prev_button, self.graph_value0, int(self.which_var.get()), 1, 0)
            draw_cart(int(self.style_var.get()), self.chart2_canvas, None, None, self.graph_value0, int(self.which_var.get()), 1, 0)
            self.display_products(self.graph_value0, int(self.which_var.get()))
            
        self.total_item_label.config(text="TOTAL ITEM COUNT : " + str(items))
        self.total_qty_label.config(text="TOTAL QTY COUNT : " + str(TQTY))
        self.total_cost_label.config(text="TOTAL COST : " + str(Tcost) + "  (" +str(self.format_price(Tcost)) + ")" )
        self.total_sale_label.config(text="TOTAL AFTER SALE : " + str(Tprice) + "  (" +str(self.format_price(Tprice)) + ")")

        # Hide the product details frame
        self.hide_add_product_forme()
        self.change_button.config(state=tk.DISABLED)








    def on_select(self, event):
        if len(event.widget.selection()) > 0:
            self.change_button.config(state=tk.NORMAL)
            self.delete_button.config(state=tk.NORMAL)
        else:
            self.change_button.config(state=tk.DISABLED)
            self.delete_button.config(state=tk.DISABLED)

    def on_name_entry(self, event):
        cur.execute('SELECT * FROM product')
        products = cur.fetchall()
        for product in products:
            #TODO MAKE IT EASY BY ID
            #print("on_name_entry\n"+str(product[1]))
            if product[1] == self.name_entry.get():
                self.add_button.config(text="Update")    
                return
        if self.main_name == self.name_entry.get() and not self.main_name == "":
            self.add_button.config(text="Update")
        else:
            self.add_button.config(text="New")

    def clear_product_details_widget(self):
        # Clear the product details widgets
        self.name_entry.delete(0, tk.END)
        self.code_entry.delete(0, tk.END)
        #self.type_entry.delete(0, tk.END) self.type_entry
        #self.barcode_entry.delete(0, tk.END)
        #self.at_shop_entry.delete(0, tk.END)
        #self.quantity_entry.delete(0, tk.END)

        self.inventory = []
        # Clear the product tree
        self.tree.delete(*self.tree.get_children())
        self.shop_name_entry.delete(0, tk.END)
        self.color_entry.delete(0, tk.END)
        self.size_entry.delete(0, tk.END)
        self.qty_entry.delete(0, tk.END)
        self.bracode_entry.delete(0, tk.END)

        
        self.cost_entry.delete(0, tk.END)
        self.tax_entry.delete(0, tk.END)
        self.price_entry.delete(0, tk.END)
        self.include_tax_var.set(0)
        self.price_change_var.set(0)
        self.more_info_label.delete(0, tk.END)
        self.images_entry.delete(0, tk.END)
        self.description_entry.delete(0, tk.END)
        self.service_change_var.set(0)
        self.default_quantity_change_var.set(0)
        self.active_var.set(0)

        self.qty_entry.insert(0, "0")
        self.size_entry.insert(0, "Def_size")
        self.color_entry.insert(0, "Def_color")
        self.code_entry.insert(0, "Def_code")
        self.shop_name_entry.insert(0, "SHOP_NAME") # todo add shop name


    # Create the "Add New" button
    # Define the function for showing the product details frame
   
    def hide_add_product_forme(self):
        self.clear_product_details_widget()
        # Hide the add product button
        self.notebook_frame.pack_forget()

    
    # Define the function for deleting a product
    def delete_product(self):
        # Get the selected product from the listbox
        selected_product = self.list_box.selection()

        if selected_product:
            # Get the ID of the selected product
            product_id = self.list_box.item(selected_product)['values'][0]
        
            # Delete the product from the database
            cur.execute('DELETE FROM product WHERE id=?', (product_id,))

            # Commit the changes to the database
            conn.commit()
            # Update the product listbox
            self.update_product_listbox()

    # Define the function for adding a new product
    def add_product(self):
        # Get the values from the product details widgets
        # Get the values from the product details widgets
        name = self.name_entry.get()
        code = self.code_entry.get()
        typ = self.type_entry.get_value
        barcode = ""
        #self.barcode_entry.get()
        at_shop = ""
        # self.at_shop_entry.get()
        quantity = 0
        # self.quantity_entry.get()
        cost = float(self.cost_entry.get())
        tax = float(self.tax_entry.get())
        price = float(self.price_entry.get())
        include_tax = int(self.include_tax_var.get())
        price_change = int(self.price_change_var.get())
        more_info = self.more_info_label.get()
        images = self.images_entry.get()
        description = self.description_entry.get()
        service = self.service_change_var.get()
        default_quantity = int(self.default_quantity_change_var.get())
        active = int(self.active_var.get())
            
        print(str([name, code, typ, barcode, at_shop, quantity, cost, tax, price, include_tax, price_change, more_info, images, description, service, default_quantity, active]))
        
        item = ""
        doc_type = ""
        brcod = 0
        cur.execute("SELECT * FROM setting WHERE user_name=?", (self.master.master.master.master.user,))
        b = cur.fetchone()
        if not len(b)<= 0:
            brcod = b[2] # getting barcode
        brcod += 1
        if self.add_button.cget("text") == "New":        
            # Insert the new product into the database
            doc_type = "Add_Items"
            # Get the ID of the most recently added item
            cur.execute('INSERT INTO product (name, code, type, barcode, at_shop, quantity, cost, tax, price, include_tax, price_change, more_info, images, description, service, default_quantity, active) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (name, code, typ, barcode, at_shop, quantity, cost, tax, price, include_tax, price_change, more_info, images, description, service, default_quantity, active))
            cur.execute("SELECT last_insert_rowid()")
            new_item_id = cur.fetchone()[0]
            print("new_product_id : " + str(new_item_id) + " barcode : " + str(brcod))
            item += f"(:{new_item_id}:,:{name}:,:{code}:,:{typ}:,:{barcode}:,:{at_shop}:,:{quantity}:,:{cost}:,:{tax}:,:{price}:,:{include_tax}:,:{price_change}:,:{more_info}:,:{images}:,:{description}:,:{service}:,:{default_quantity}:,:{active}:)"
            print("item : " + str(item))
        else:
            product_id = int(self.list_box.item(self.list_box.selection())['values'][0])
            print("product_id : " + str(product_id) + " barcode : " + str(brcod))
            doc_type = "Update_Items"
            item += f"(:{product_id}:,:{name}:,:{code}:,:{typ}:,:{barcode}:,:{at_shop}:,:{quantity}:,:{cost}:,:{tax}:,:{price}:,:{include_tax}:,:{price_change}:,:{more_info}:,:{images}:,:{description}:,:{service}:,:{default_quantity}:,:{active}:)"
            print("item : " + str(item))
            # Update the product in the database
            cur.execute('UPDATE product SET name=?, code=?, type=?, barcode=?, at_shop=?, quantity=?, cost=?, tax=?, price=?, include_tax=?, price_change=?, more_info=?, images=?, description=?, service=?, default_quantity=?, active=? WHERE id=?', (name, code, typ, barcode, at_shop, quantity, cost, tax, price, include_tax, price_change, more_info, images, description, service, default_quantity, active, product_id))
        # Commit the changes to the database
        conn.commit()

        try:
            # Insert the record into the upload_doc table
            cur.execute('INSERT INTO upload_doc (doc_barcode, extension_barcode, user_id, customer_id, type, item, qty, price, discount, tax, payments, doc_created_date, doc_expire_date, doc_updated_date) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', ("23-200-" + str(brcod), "extension_barcode", self.master.master.master.master.user, self.master.master.master.master.custemr, doc_type, item, 1, 0, 0, 0, "payments_", "doc_created_date", "doc_expire_date", "doc_updated_date"))

            # Commit the changes to the database
            conn.commit()
            
            print("Data inserted successfully into the upload_doc table.")
        except Exception as e:
            print("Error occurred while inserting data into the upload_doc table:")
            print(str(e))


        # Commit the changes to the database
        conn.commit()

        # Clear the product details widgets
        self.clear_product_details_widget()
        
        # Update the product listbox
        self.update_product_listbox()
