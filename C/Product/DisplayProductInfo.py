import tkinter as tk
from tkinter import ttk
import sqlite3
import shutil
import datetime
import os
import atexit
import sys
import json
import ast


current_dir = os.path.abspath(os.path.dirname(__file__))
MAIN_dir = os.path.join(os.path.join(current_dir, '..'), '..')
sys.path.append(MAIN_dir)
from C.List import *

from D.Getdefsize import ButtonEntryApp
from C.List import *
from D.printer import *
from D.GetVALUE import GetvalueForm
# Connect to the database or create it if it does not exist

from C.List import *
from D.Getdate import GetDateForm
from D.Chart.Chart import *

from C.Product.selecttype import *
from D.Getdefsize import ButtonEntryApp
from C.List import *

from D.Getdate import GetDateForm
from D.Chart.Chart import *

from C.Product.selecttype import *

# Connect to the database or create it if it does not exist


from C.API.Get import *
from C.API.API import *
from C.API.Set import *



def is_float(value):
    try:
        print()
        float (value)
        return True
    except ValueError:
        return False
    

class ProductFullInfoForm(ttk.Notebook):
    def __init__(self, master, user, Shops, given_value):
        # Modern battery/energy-inspired color scheme
        bg_dark = "#1a1a2e"      # Dark navy
        bg_medium = "#16213e"    # Medium navy
        accent_green = "#0f3460" # Deep blue-green
        accent_yellow = "#e94560" # Energy red
        text_light = "#eaeaea"   # Light gray
        text_secondary = "#b0b0b0" # Secondary text
        
        ttk.Notebook.__init__(self, master)
        self.master = master
        self.user_info = user
        self.Shops = Shops
        self.Shops_Names = [shop['Shop_name'] for shop in self.Shops]
        self.given_value = given_value
        self.notebook_frame = self
        
        
        self.Product_listinfo_frame = ttk.Frame(self.notebook_frame)#, bg=bg_dark)
        self.Product_listinfo_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.notebook_frame.add(self.Product_listinfo_frame, text="Products Info")
        
        self.List_Frame = ttk.Frame(self.Product_listinfo_frame)#, bg=bg_dark)
        self.List_Frame.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        
        self.item_List_canvas = tk.Canvas(self.List_Frame, bg=bg_dark, highlightthickness=0)
        self.item_List_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        
        self.item_List_yscrollbar = ttk.Scrollbar(self.List_Frame, orient='vertical', command=self.item_List_canvas.yview) #, bg=bg_medium)
        self.item_List_yscrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.item_List_xscrollbar = ttk.Scrollbar(self.Product_listinfo_frame, orient='horizontal', command=self.item_List_canvas.xview) #, bg=bg_medium)
        self.item_List_xscrollbar.pack(side=tk.TOP, fill=tk.X)
        
        self.item_List_canvas.configure(xscrollcommand=self.item_List_xscrollbar.set, yscrollcommand=self.item_List_yscrollbar.set)

        self.item_List_frame = ttk.Frame(self.item_List_canvas)#, bg=bg_dark)
        self.item_List_canvas.create_window((0, 0), window=self.item_List_frame, anchor=tk.NW)
        self.item_List_frame.bind('<Configure>', lambda e: self.item_List_canvas.configure(scrollregion=self.item_List_canvas.bbox("all")))

        self.chart_canvas_Frame = tk.Frame(self.item_List_frame, bg=bg_dark, relief='sunken', bd=2)
        self.chart_canvas_Frame.grid(row=1, column=0, columnspan=3, sticky="nsew", padx=5, pady=5)
        
        self.product_list = tk.Listbox(self.item_List_frame, selectmode=tk.SINGLE, width=30, bg=bg_medium, fg=text_light, font=("Arial", 10), highlightbackground=accent_green)
        self.product_list.grid(row=6, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)

        self.details_frame = ttk.Frame(self.item_List_frame) # , bg=bg_dark, relief='raised', bd=1)
        self.details_frame.grid(row=6, column=2, columnspan=3, padx=10, pady=10, sticky="nsew")
        
        self.total_item_label = ttk.Label(self.details_frame, text="TOTAL ITEM COUNT :") # , bg=bg_dark, fg=accent_yellow, font=("Arial", 11, "bold"))
        self.total_item_label.grid(row=0, column=0, sticky="w", pady=5, padx=10)
        self.total_qty_label = ttk.Label(self.details_frame, text="TOTAL QTY COUNT :") #, bg=bg_dark, fg=text_light, font=("Arial", 11, "bold"))
        self.total_qty_label.grid(row=1, column=0, sticky="w", pady=5, padx=10)
        self.total_cost_label = ttk.Label(self.details_frame, text="TOTAL COST :") #, bg=bg_dark, fg=accent_yellow, font=("Arial", 11, "bold"))
        self.total_cost_label.grid(row=2, column=0, sticky="w", pady=5, padx=10)
        self.total_sale_label = ttk.Label(self.details_frame, text="TOTAL AFTER SALE :") # , bg=bg_dark, fg=accent_green, font=("Arial", 11, "bold"))
        self.total_sale_label.grid(row=3, column=0, sticky="w", pady=5, padx=10)

        self.update_product_listbox()
        self.Item_To_Update()
    #
    #
    #
    # Product info
    #
    #
    #

    # Display Totals on list box
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

    # Define the function for updating the product listbox
    def update_product_listbox(self):
        # Clear the product listbox
        # Get the products from the database
        print("self.given_value ", self.given_value)
        '''items = 0
        TQTY = 0
        Tprice = 0
        Tcost = 0
        vv = []
        item = cur.fetchall()
        for product in self.given_value:
            chacksize = 0
            cost = float(product['cost'])
            price = float(product['price'])
            print("info : "+str(product['more_info']))
            qty_info_list = json.loads(product['more_info'])
            print("qty_info_list : "+str(qty_info_list))
            items += 1
            qty = 0
            def sub_list(ls, qty):
                comen_qty = 0
                if(isinstance(ls, list)):
                    for l in ls:
                        if len(l) > 4 and l[4] != ""and l[4] != " ":
                            print("l[4] : "+str(l[4]))
                            ischar = any(char.isalpha() for char in l[4])
                            if not ischar and (isinstance(float(l[4]), float) or isinstance(int(l[4]), int)):
                                print("isfloat : "+str(l[4]))
                                if comen_qty == 0:
                                    comen_qty = float(l[4])
                                # TODO: FOR 2ps and more than one ps what to do
                                qty += float(l[4])
                        elif len(l) == 2:
                            #main_name.append(l[0])
                            qty = sub_list(l[1], qty)
                return qty
            qty = sub_list(qty_info_list, qty)
            print("qty : ", str(qty))
            vv.append([str(product['id']), float(price), str(product['name'])])
            # TODO make user choosh in which name, code, id
            if qty > 0:
                print("Calculating : " + "qty " + str(qty) + "*" + str(price) + " price = " + str(qty*price) + "  AND QTY * " + str(cost) + " Cost = " + str(qty*cost))
                print("equal Tprice : " + str(Tprice) + " Cost :" + str(Tcost))
                Tprice += qty*price
                Tcost += qty*cost
                TQTY += qty'''
        if len(self.given_value[4]) > 0:
            self.graph_value, self.graph_value0, tilte = make_list(self.given_value[4])
            # clear chart_canvas_Frame
            # self.chart_canvas_Frame : give main fram to display
            # self.graph_value0 : give value to compare
            #  : tall wiche value to use
            #  : give style of chart 1: streag line 2: circle 3: line 
            draw_cart(self.chart_canvas_Frame, self.graph_value0, 1, 1)
            draw_cart(self.chart_canvas_Frame, self.graph_value0, 1, 2)
            
            self.display_products(self.graph_value0, 0)
            
        self.total_item_label.config(text="TOTAL ITEM COUNT : " + str(self.given_value[0]))
        self.total_qty_label.config(text="TOTAL QTY COUNT : " + str(self.given_value[1]))
        self.total_cost_label.config(text="TOTAL COST : " + str(self.given_value[3]) + "  (" +str(self.format_price(self.given_value[3])) + ")" )
        self.total_sale_label.config(text="TOTAL AFTER SALE : " + str(self.given_value[2]) + "  (" +str(self.format_price(self.given_value[2])) + ")")

    #
    #
    #
    # doc info
    #
    #
    #
    
    def Item_To_Update(self):
        #self.info_tab = None
        # Notebook widget - CENTER_NOTEBOK

        self.Item_To_Update_tab = ttk.Frame(self.notebook_frame)
        self.Item_To_Update_tab.grid()

        # Add tabs to the self.center_notebook
        self.notebook_frame.add(self.Item_To_Update_tab, text='Out Of Stocks')

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

    def on_select(self, event):
        if len(event.widget.selection()) > 0:
            pass
        
    def perform_search_Item_size_chack(self):
        print("self.given_value ", self.given_value)
        item = cur.fetchall()
        for it in self.given_value:
            print("info : "+str(it['more_info']))
            qty_info_list = json.loads(it['more_info'])
            print("qty_info_list : "+str(qty_info_list))
            def sub_list(ls):
                comen_qty = 0
                for l in ls:
                    if len(l) > 4:
                        print("l[4] : "+str(l[4]))
                        if isinstance(float(l[4]), float) or isinstance(int(l[4]), int):
                            if float(l[4]) < 0:
                                self.Item_To_Update_tab_listbox.insert("", 'end', text="Size", values=(it[1], it[2], it[3], it[4], it[5], it[6], it[7], it[8], it[9], it[10], it[11], it[12], it[13], it[14]))
                    elif len(l) == 4:
                        sub_list(l[1])
                return qty
            sub_list(qty_info_list)

            
            
    # Function to perform the search and display the results in the listbox
    def perform_doc_search(self, item_code):
        self.pyment_used = []
        start_value = self.date_from_Entry.get()
        end_value = self.date_to_Entry.get()
        
        df = fetch_as_dict_list("SELECT * FROM doc_table WHERE item LIKE ? AND strftime('%Y-%m-%d', doc_created_date) BETWEEN ? AND ?", ('%' + item_code + '%', start_value, end_value,))
        
        
        print("doc search"+str(item_code)+"from"+str(start_value)+"to"+str(end_value)+" found "+str(len(df)))
        self.user_docinfo_listbox.delete(*self.user_docinfo_listbox.get_children())

        '''results = fetch_as_dict_list("SELECT * FROM COUNT_SELL WHERE strftime('%Y-%m-%d', DATE) BETWEEN ? AND ?", (f'{self.date_from_Entry.get()}', f'{self.date_to_Entry.get()}',))
        
        l = []
        
        for result in results:
            f = 0
            self.TLs_items.insert(tk.END, [result[0], result[1], result[2], result[3], result[4]])
            for item in l:
                #print("item"+str(item))
                if item[1] == result[1]:
                    item[3] += result[4]
                    f = 1
            if f == 0:
                l.extend([[len(l), result[1], result[2], result[4]]])
        for ls in l:
            self.TL_items.insert(tk.END, ls)
        #self.get_columen()'''
        vv = []
        count = 0
        TQTY = 0
        for index in df:
            item = self.user_docinfo_listbox.insert('', 'end', text=index[0], values=(index[1], index[2], index[3], index[4], index[5], index[6], index[7], index[8], index[9], index[10], index[11], index[12], index[13], index[14]))
            TQTY += 1
            
        self.total_doc_qty_label.config(text="TOTAL QTY COUNT : " + str(TQTY))

    def perform_doc_print(self):
        item = self.user_docinfo_listbox.focus()  # Get the item that was clicked
        if item:
            item_text = self.user_docinfo_listbox.item(item, "values")  # Get the text values of the item
            id = self.user_docinfo_listbox.item(item, "text")
            barcode = item_text[0]
            doc_ = fetch_as_dict_list("SELECT * FROM doc_table WHERE doc_barcode=?", (barcode,))
            if doc_:
                answer = tk.messagebox.askquestion("Question", "Do you what to print "+str(barcode)+" ?")
                if answer == 'yes':
                    #print(str(doc_))
                    doc_edit_form = load_slip(doc_, id)
                    #print("don loding slip : \n\n" + str(doc_edit_form))
                    self.user = self.master.master.master.master.user
                    PrinterForm.print_slip(self, self.user_info, doc_edit_form, 1) # TODO chack in setting if paper cut allowed
            
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

        
    
        
    

    
