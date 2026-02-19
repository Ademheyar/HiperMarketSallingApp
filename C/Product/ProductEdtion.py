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

from C.API.Get import *
from C.API.API import *
from C.API.Set import *

from C.Product.selecttype import *


def is_float(value):
    try:
        print()
        float (value)
        return True
    except ValueError:
        return False

class ProductFullEditionForm(ttk.Notebook):
    def __init__(self, master, user, Shops):
        ttk.Notebook.__init__(self, master)
        self.master = master
        self.user_info = user
        self.Shops = Shops
        self.Shops_Names = [shop['Shop_name'] for shop in self.Shops]
        self.notebook_frame = self
        self.selected_path = []
        self.product_id = -1
        # Create the frame for the product details
        self.details_frame = tk.Frame(self.notebook_frame)
        self.details_frame.pack()
        
        self.notebook_frame.add(self.details_frame, text="Main info")


        # Create the widgets for the product details
        self.name_label = tk.Label(self.details_frame, text='Name:')
        self.name_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.E)
        self.name_entry = tk.Entry(self.details_frame)
        self.name_list = tk.Listbox(self.name_entry.master.master, width=30)
        self.main_name = ""
        self.name_entry.bind('<KeyRelease>', self.on_name_entry)
        self.name_entry.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)
        
        self.cost_label = tk.Label(self.details_frame, text='Cost:')
        self.cost_label.grid(row=3, column=0, padx=5, pady=5, sticky=tk.E)
        self.cost_entry = tk.Entry(self.details_frame)
        self.cost_entry.grid(row=3, column=1, padx=5, pady=5, sticky=tk.W)
        self.cost_entry.insert(0, "0")
        self.mark_label = tk.Label(self.details_frame, text='mark:')
        self.mark_label.grid(row=4, column=0, padx=5, pady=5, sticky=tk.E)
        self.mark_entry = tk.Entry(self.details_frame)
        self.mark_entry.grid(row=4, column=1, padx=5, pady=5, sticky=tk.W)
        self.mark_entry.insert(0, "0")
        self.price_label = tk.Label(self.details_frame, text='Price:')
        self.price_label.grid(row=5, column=0, padx=5, pady=5, sticky=tk.E)
        self.price_entry = tk.Entry(self.details_frame)
        self.price_entry.grid(row=5, column=1, padx=5, pady=5, sticky=tk.W)
        self.price_entry.insert(0, "0")
        self.tax_label = tk.Label(self.details_frame, text='Tax:')
        self.tax_label.grid(row=6, column=11, padx=5, pady=5, sticky=tk.E)
        self.tax_entry = tk.Entry(self.details_frame)
        self.tax_entry.grid(row=6, column=1, padx=5, pady=5, sticky=tk.W)
        self.tax_entry.insert(0, "0")
        
        self.description_label = tk.Label(self.details_frame, text='Description:')
        self.description_label.grid(row=7, column=0, padx=5, pady=5, sticky=tk.E)
        self.description_entry = tk.Entry(self.details_frame)
        self.description_entry.grid(row=7, column=1, padx=5, pady=5, sticky=tk.W)
        self.service_change_var = tk.IntVar()
        self.service_change_entry = tk.Checkbutton(self.details_frame, text='service', variable=self.service_change_var)
        self.service_change_entry.grid(row=8, column=0, padx=5, pady=5, sticky=tk.W)
        self.default_quantity_change_var = tk.IntVar()
        self.default_quantity_change_entry = tk.Checkbutton(self.details_frame, text='Default Quantity', variable=self.default_quantity_change_var)
        self.default_quantity_change_entry.grid(row=9, column=0, padx=5, pady=5, sticky=tk.W)
        self.active_var = tk.IntVar()
        self.active_checkbutton = tk.Checkbutton(self.details_frame, text='Active', variable=self.active_var)
        self.active_checkbutton.grid(row=10, column=0, padx=5, pady=5, sticky=tk.W)
        self.include_tax_var = tk.IntVar()
        self.include_tax_checkbutton = tk.Checkbutton(self.details_frame, text='Include Tax', variable=self.include_tax_var)
        self.include_tax_checkbutton.grid(row=11, column=0, padx=5, pady=5, sticky=tk.W)
        self.price_change_var = tk.IntVar()
        self.price_change_entry = tk.Checkbutton(self.details_frame, text='Price Change', variable=self.price_change_var)
        self.price_change_entry.grid(row=12, column=0, padx=5, pady=5, sticky=tk.W)
        
        # Create the frame for the product details
        self.Product_listinfo_frame = tk.Frame(self.notebook_frame)
        self.Product_listinfo_frame.pack_forget()
        self.notebook_frame.add(self.Product_listinfo_frame, text="Stock")
        
        self.List_Frame = tk.Frame(self.Product_listinfo_frame)
        self.List_Frame.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        
        self.item_List_canvas = tk.Canvas(self.List_Frame)
        self.item_List_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        
        self.item_List_yscrollbar = tk.Scrollbar(self.List_Frame, orient='vertical', command=self.item_List_canvas.yview)
        self.item_List_yscrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.item_List_xscrollbar = tk.Scrollbar(self.Product_listinfo_frame, orient='horizontal', command=self.item_List_canvas.xview)
        self.item_List_xscrollbar.pack(side=tk.TOP, fill=tk.X)
        
        self.item_List_canvas.configure(xscrollcommand=self.item_List_xscrollbar.set, yscrollcommand=self.item_List_yscrollbar.set)
        #self.New_item_contener_canvas.bind('<Configure>', lambda e: self.New_item_contener_canvas.configure(scrollregion=self.New_item_contener_canvas.bbox("all")))

        self.tab3_frame = tk.Frame(self.item_List_canvas)
        self.item_List_canvas.create_window((0, 0), window=self.tab3_frame, anchor=tk.NW)
        self.tab3_frame.bind('<Configure>', lambda e: self.item_List_canvas.configure(scrollregion=self.item_List_canvas.bbox("all")))

        # Create the list box
        self.more_info_label = tk.Entry(self.tab3_frame)
        self.more_info_label.grid(row=0, column=0, columnspan=4, sticky=tk.W)

        self.inventory = []
        
        
        self.tree = ttk.Treeview(self.tab3_frame, columns=
                                 ("Shop Name", "Code", "Color", "Size", "Barcode",
                                  "Qtyfirst", "Qty", "cdate", "update"))
        self.tree.grid(row=2, column=0, sticky=tk.E, columnspan=4)
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

        self.tree.bind('<<TreeviewSelect>>', self.new_stock_on_path_select)
        
        def cear_selection():
            self.selected_path = []
            self.show_selected_path_label.config(text=str(self.selected_path))
            
        self.Clear_info_button = tk.Button(self.tab3_frame, text='Clear Selected', command=cear_selection)
        self.Clear_info_button.grid(row=7, column=0, sticky=tk.W)
        
        self.remove_info_button = tk.Button(self.tab3_frame, text='Remove', command=self.remove_info)
        self.remove_info_button.grid(row=7, column=1, sticky=tk.W)
        
        self.show_selected_path_label = tk.Label(self.tab3_frame, text=str(self.selected_path))
        self.show_selected_path_label.grid(row=8, column=0, columnspan=3, sticky=tk.W)
        
        self.code_label = tk.Label(self.tab3_frame, text='Code:')
        self.code_label.grid(row=9, column=0, sticky=tk.W)
        self.code_entry = tk.Entry(self.tab3_frame)
        self.code_entry.grid(row=9, column=1, sticky=tk.W)

        
        self.color_label = tk.Label(self.tab3_frame, text='Color :')
        self.color_label.grid(row=10, column=0, sticky=tk.W)
        self.color_entry = tk.Entry(self.tab3_frame)
        self.color_entry.grid(row=10, column=1, sticky=tk.W)
        
        # for getting size
        
        self.get_size_frame = tk.Frame(self.tab3_frame)
        self.get_size_frame.grid(row=11, column=0, columnspan=3, sticky=tk.W)
        
        self.first_frame = tk.Frame(self.get_size_frame)
        self.first_frame.grid(row=0, column=0, sticky=tk.W)


        self.sizeing_type = tk.StringVar()  # Variable to store the selected sizing type
        self.sizeing_type.set("Select Sizing Type")
        
        sizing_options = ["Trouser Sizes", "Clothing Sizes", "Shoe Sizes"]

        self.sizing_var = tk.StringVar()
        self.sizing_var.set("Melty Select Size ")
        sizing_menu = tk.OptionMenu(self.first_frame, self.sizing_var, *sizing_options)
        sizing_menu.pack()

        self.create_form_button = tk.Button(self.first_frame, text="Create Form", command=self.create_sizes_form)
        self.create_form_button.pack(side=tk.BOTTOM)

        self.second_frame = tk.Frame(self.get_size_frame)
        self.second_frame.grid(row=0, column=1, sticky=tk.W)
        
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
        
        self.type_label = tk.Label(self.tab3_frame, text='Type:')
        self.type_label.grid(row=15, column=0, padx=5, pady=5, sticky=tk.E)
        type_frame = tk.Frame(self.tab3_frame)
        type_frame.grid(row=15, column=1, padx=5, pady=5, sticky=tk.W)
        # get nodes by stting
        self.type_entry = NodeSelectorApp(type_frame, self.user_info)
        self.type_entry.load("")
        
        self.single_price_label = tk.Label(self.tab3_frame, text='Single Price:')
        self.single_price_label.grid(row=16, column=0, sticky=tk.W)
        self.single_price_entry = tk.Entry(self.tab3_frame)
        self.single_price_entry.grid(row=16, column=1, sticky=tk.W)
        
        self.images_label = tk.Label(self.tab3_frame, text='Images:')
        self.images_label.grid(row=17, column=0, sticky=tk.W)
        self.images_entry = tk.Entry(self.tab3_frame)
        self.images_entry.grid(row=17, column=1, sticky=tk.W)
        
        self.add_info_button = tk.Button(self.tab3_frame, text='Add', command=lambda : self.add_info(0))
        self.add_info_button.grid(row=22, column=0, sticky=tk.W)
        
        self.change_info_button = tk.Button(self.tab3_frame, text='Change', command=lambda : self.add_info(1))
        self.change_info_button.grid(row=22, column=1, sticky=tk.W)
        
      
        self.add_button = tk.Button(self.details_frame, text='Add', command=self.add_product)
        self.add_button.grid(row=30, column=0, padx=5, pady=5, sticky=tk.W)
        self.cancle_button = tk.Button(self.details_frame, text='Cancle', command=lambda:self.destroy())
        self.cancle_button.grid(row=30, column=1, padx=5, pady=5, sticky=tk.W)


        # Create the frame for the user details
        self.doc_details_frame = tk.Frame(self.notebook_frame)
        self.doc_details_frame.pack_forget()
        self.notebook_frame.add(self.doc_details_frame, text="Doc info")

        self.l_frame = tk.Frame(self.doc_details_frame)
        self.l_frame.grid(row=0, column=0)


        # Create the listbox to display search results
        self.user_docinfo_listbox = ttk.Treeview(self.l_frame)        
        #self.user_docinfo_listbox.bind('<<TreeviewSelect>>', self.on_select)
        #self.user_docinfo_listbox.bind("<Button-1>", self.on_treeview_double_click)
        #self.listbox.grid_propagate(False)


        # Add vertical scrollbar
        tree_scrollbar_y = ttk.Scrollbar(self.l_frame, orient='vertical', command=self.user_docinfo_listbox.yview)
        self.user_docinfo_listbox.configure(yscrollcommand=tree_scrollbar_y.set)
        tree_scrollbar_y.pack(side='right', fill='y')

        # Add horizontal scrollbar
        tree_scrollbar_x = ttk.Scrollbar(self.l_frame, orient='horizontal', command=self.user_docinfo_listbox.xview)
        self.user_docinfo_listbox.configure(xscrollcommand=tree_scrollbar_x.set)
        tree_scrollbar_x.pack(side='bottom', fill='x', )

        # Set the size of the self.listbox widget
        self.user_docinfo_listbox.pack(side='top', fill='both', expand=True)
        self.user_docinfo_listbox['columns'] = ('doc_barcode', 'extension_barcode', 'user_id', 'customer_id', 'Type', 'Itmes', 'Qty', 'Paymen', 'price', 'disc', 'tax', 'doc_created_date', 'doc_expire_date', 'doc_updated_date')
        self.user_docinfo_listbox.heading("#0", text="ID")
        self.user_docinfo_listbox.column("#0", stretch=tk.NO, minwidth=25, width=50) 
        self.user_docinfo_listbox.heading("#1", text="doc_barcode")
        self.user_docinfo_listbox.column("#1", stretch=tk.NO, minwidth=25, width=100) 
        self.user_docinfo_listbox.heading("#2", text="extension_barcode")
        self.user_docinfo_listbox.column("#2", stretch=tk.NO, minwidth=25, width=100) 
        self.user_docinfo_listbox.heading("#3", text="user_id")
        self.user_docinfo_listbox.column("#3", stretch=tk.NO, minwidth=25, width=100) 
        self.user_docinfo_listbox.heading("#4", text="customer_id")
        self.user_docinfo_listbox.column("#4", stretch=tk.NO, minwidth=25, width=100) 
        self.user_docinfo_listbox.heading("#5", text="Type")
        self.user_docinfo_listbox.column("#5", stretch=tk.NO, minwidth=25, width=80) 
        self.user_docinfo_listbox.heading("#6", text="Itmes")
        self.user_docinfo_listbox.column("#6", stretch=tk.NO, minwidth=25, width=100) 
        self.user_docinfo_listbox.heading("#7", text="Qty")
        self.user_docinfo_listbox.column("#7", stretch=tk.NO, minwidth=25, width=100) 
        self.user_docinfo_listbox.heading("#8", text="price")
        self.user_docinfo_listbox.column("#8", stretch=tk.NO, minwidth=25, width=50) 
        self.user_docinfo_listbox.heading("#9", text="disc")
        self.user_docinfo_listbox.column("#9", stretch=tk.NO, minwidth=25, width=50) 
        self.user_docinfo_listbox.heading("#10", text="tax")
        self.user_docinfo_listbox.column("#10", stretch=tk.NO, minwidth=25, width=50) 
        self.user_docinfo_listbox.heading("#11", text="Payment")
        self.user_docinfo_listbox.column("#11", stretch=tk.NO, minwidth=25, width=100) 
        self.user_docinfo_listbox.heading("#12", text="doc_created_date")
        self.user_docinfo_listbox.column("#12", stretch=tk.NO, minwidth=25, width=100) 
        self.user_docinfo_listbox.heading("#13", text="doc_expire_date")
        self.user_docinfo_listbox.column("#13", stretch=tk.NO, minwidth=25, width=100) 
        self.user_docinfo_listbox.heading("#14", text="doc_updated_date")
        self.user_docinfo_listbox.column("#14", stretch=tk.NO, minwidth=25, width=100)

        self.start_value = datetime.datetime.now().strftime('%Y-%m-%d')
        self.end_value = self.start_value
        
        self.date_from_Entry = tk.Entry(self.l_frame)
        self.date_from_Entry.insert(0, self.start_value)
        self.date_from_Entry.pack()#grid(row=3, column=3)
        
        self.date_to_Entry = tk.Entry(self.l_frame)
        self.date_to_Entry.insert(0, self.start_value)
        self.date_to_Entry.pack()#grid(row=3, column=4)
        
        self.GetDate_button = tk.Button(self.l_frame, text="GetDate", font=("Arial", 12), command=self.fix_date)
        self.GetDate_button.pack()#grid(row=3, column=5, sticky="nsew")
        

        self.refresh_doc_button = tk.Button(self.l_frame, text='Refresh')
        self.refresh_doc_button.pack()#pack(side=tk.LEFT, padx=5, pady=5)

        # Create the search button
        self.print_button = tk.Button(self.l_frame, text="Print", command=self.perform_doc_print)
        self.print_button.pack()#.grid(row=2, column=0)
        self.total_doc_qty_label = tk.Label(self.l_frame, text="TOTAL QTY COUNT :")
        self.total_doc_qty_label.pack()#grid(row=1, column=0)
        
        #self.clear_product_details_widget()
       
        
    #
    #
    #
    # doc info
    #
    #
    #
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

    def perform_doc_print(self):
        item = self.user_docinfo_listbox.focus()  # Get the item that was clicked
        if item:
            item_text = self.user_docinfo_listbox.item(item, "values")  # Get the text values of the item
            id = self.user_docinfo_listbox.item(item, "text")
            barcode = item_text[0]
            doc_ = fetch_as_dict_list("SELECT * FROM doc_table WHERE doc_barcode=?", (barcode,))
            if doc_:
                doc_= doc_[0]
                answer = tk.messagebox.askquestion("Question", "Do you what to print "+str(barcode)+" ?")
                if answer == 'yes':
                    #print(str(doc_))
                    doc_edit_form = load_slip(doc_, id)
                    #print("don loding slip : \n\n" + str(doc_edit_form))
                    self.user = self.master.master.master.master.user
                    PrinterForm.print_slip(self, self.user_info, doc_edit_form, 1) # TODO chack in setting if paper cut allowed
         
    # Function to perform the search and display the results in the listbox
    def perform_doc_search(self, item_code):
        self.pyment_used = []
        start_value = self.date_from_Entry.get()
        end_value = self.date_to_Entry.get()
        
        
        df = fetch_as_dict_list("SELECT * FROM doc_table WHERE item LIKE ? AND strftime('%Y-%m-%d', doc_created_date) BETWEEN ? AND ?", ('%' + item_code + '%', start_value, end_value,))
        if df:
            df = dfp[0]
        print("doc search"+str(item_code)+"from"+str(start_value)+"to"+str(end_value)+" found "+str(len(df)))
        self.user_docinfo_listbox.delete(*self.user_docinfo_listbox.get_children())

        '''cur.execute("SELECT * FROM COUNT_SELL WHERE strftime('%Y-%m-%d', DATE) BETWEEN ? AND ?", (f'{self.date_from_Entry.get()}', f'{self.date_to_Entry.get()}',))
        results = cur.fetchall()
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
            '''ispayed = self.load_payment(index[11], self.date_from_Entry.get(), self.date_to_Entry.get()) # LOAD PYMENT AND IT TOTAL 
            if ispayed:
                count+=1
            #print("df : " + str(index)
            #print("df : " + str(index[12]))
            dateandtime = index[12].split(" ") if " " in index[12] else index[12].split("_")
            hour = dateandtime[1].split(":")[0] if ":" in dateandtime[1] else dateandtime[1].split("-")[0]
            date = dateandtime[0].split("-")
            day = date[2]
            month = date[1]
            year = date[0]
            vv.append([year, month, day, hour, float(index[8])-float(index[9])])

            
            id = self.listbox.item(item, "text")
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
                            print(str(self.center_notebook.tab(a, "text")))

        if len(vv) > 0:
            #print(" v : " + str(vv))
            self.graph_value, self.graph_value0, tilte = make_list(vv)
        
            #print("self.graph_value0 :" + str(self.graph_value0))
            draw_cart(int(self.style_var.get()), self.chart_canvas, self.next_button, self.prev_button, self.graph_value0, int(self.which_var.get()), 1, 0)
            draw_cart(int(self.style_var.get()), self.chart2_canvas, None, None, self.graph_value0, int(self.which_var.get()), 2, 0)
            self.display_products(self.graph_value0, int(self.which_var.get()))
      
        self.creat_info(count)'''
        self.total_doc_qty_label.config(text="TOTAL QTY COUNT : " + str(TQTY))
        
    #
    #
    #
    # Stock
    #
    #
    #
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
                if p["shop_name"] == self.master.master.shop_name_Combobox.get() and p["color"] == self.color_entry.get() and \
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
            if self.type_entry.get_value and len(self.type_entry.get_value) > 0:
                for type_ in self.type_entry.get_value:
                    new_type = json.dumps(type_)
                    found, self.nested_list = Add_new_on_nested(self.nested_list, [self.master.master.shop_name_Combobox.get(), self.code_entry.get(), self.color_entry.get(), v[0]], [self.bracode_entry.get(), new_type, self.single_price_entry.get(), v[1], v[1], "", self.images_entry.get(), "", ""])
            else:
                pass # sand messeg
            print("self.nested_list : " + str(self.nested_list))
            if found:
                self.add_info_(self.master.master.shop_name_Combobox.get(), self.code_entry.get(), self.color_entry.get(), v[0], self.bracode_entry.get(), v[1], v[1], "", "")
        txt = json.dumps(self.nested_list)
        self.more_info_label.delete(0, tk.END)
        self.more_info_label.insert(0, txt)

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

    def get_inventory_nested_list(self, text, code):
        print("get_inventory_nested_list text = "+str(text))
        if text:
            self.nested_list = json.loads(text) 
        self.update_tree()

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
                            barcode, type_, price, qtyfirst, qty, patern, imgs, cdate, update = ["", "", "", "", "", "", "", "", ""]
                            cvalue = value
                            
                            if len(cvalue) == 7:
                                barcode, qtyfirst, qty, patern, imgs, type_, update = value
                            elif len(cvalue) >= 9:
                                barcode, type_, price, qtyfirst, qty, patern, imgs, cdate, update = value
                            elif len(cvalue) == 4:
                                barcode, type_, price, qtyfirst, qty, update = value
                            
                            if(price == ""):
                                self.single_price_entry.delete(0, tk.END)
                                self.single_price_entry.insert(0, self.price_entry.get())
                            self.tree.insert(size_node, "end", text=barcode, values=(type_, price, qtyfirst, qty, patern, imgs, cdate, update))
            
    # Morinfo [barcode, type, single_price, fqty, qty, sock_patern, images, date, ""]
    def add_info_(self, shop_name, code, color, size, barcode, qtyfirst, qty, stock, img, cdate, update):
        p = {"shop_name": shop_name, "code": code, "color": color, "size": size, "barcode": barcode, "qtyfirst": qtyfirst, "qty": qty, "cdate": cdate, "update": update}
        self.inventory.append(p)
        self.update_tree()
        
    def remove_info(self):
        if not self.selected_path == []:        
            if self.type_entry.get_value and len(self.type_entry.get_value) > 0:
                for type_ in self.type_entry.get_value:
                    new_type = json.dumps(type_)
                    if self.selected_path == []:
                        self.selected_path = [self.master.master.shop_name_Combobox.get(), self.code_entry.get(), self.color_entry.get(), self.size_entry.get()]
                    found, self.nested_list = dele_list(self.nested_list, self.selected_path, [self.bracode_entry.get(), new_type, self.single_price_entry.get(), self.qty_entry.get(), self.qty_entry.get(), "", self.images_entry.get(), "", ""])
            else:
                found, self.nested_list = dele_list(self.nested_list, self.selected_path, [self.bracode_entry.get(), "", self.single_price_entry.get(), self.qty_entry.get(), self.qty_entry.get(), "", self.images_entry.get(), "", ""])
        self.more_info_label.delete(0, tk.END)
        self.more_info_label.insert(0, str(self.nested_list))
        self.update_tree()
        
    def add_info(self, do_what):
        if do_what == 0:
            self.selected_path = []
        found = 0 
        i = 0
        for p in self.inventory:
            if p["shop_name"] == self.master.master.shop_name_Combobox.get() and p["color"] == self.color_entry.get() and \
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
        
        if self.type_entry.get_value and len(self.type_entry.get_value) > 0:
            for type_ in self.type_entry.get_value:
                new_type = json.dumps(type_)
                if self.selected_path == []:
                    self.selected_path = [self.master.master.shop_name_Combobox.get(), self.code_entry.get(), self.color_entry.get(), self.size_entry.get()]
                found, self.nested_list = add_new_list(self.nested_list, self.selected_path, [self.bracode_entry.get(), new_type, self.single_price_entry.get(), self.qty_entry.get(), self.qty_entry.get(), "", self.images_entry.get(), "", ""], 1)
        else:
            pass # sand messeg
        print("self.nested_list : " + str(self.nested_list))
        if found:
            self.add_info_(self.master.master.shop_name_Combobox.get(), self.code_entry.get(), self.color_entry.get(), self.size_entry.get(), self.bracode_entry.get(), self.qty_entry.get(), self.qty_entry.get(), "", self.images_entry.get(), "", "")
            
            

        txt = json.dumps(self.nested_list)
        self.more_info_label.delete(0, tk.END)
        self.more_info_label.insert(0, txt)
        self.update_tree()
        
    def new_stock_on_path_select(self, event):
        item = self.tree.selection()[0]
        found_values = []
        found_vv = []
        parent_item = item
        while parent_item:
            txt = self.tree.item(parent_item, "text")
            value = self.tree.item(parent_item, "value")
            found_values.append(txt)
            if value and len(value) > 4:
                found_vv = value
            parent_item = self.tree.parent(parent_item)
            
        found_values.reverse()
        print("found_vv value : " + str(found_vv))
        if found_vv:
            found_values = found_values+list(found_vv)
        print("found value : " + str(found_values))
        if found_values:
            self.selected_path = found_values
            self.show_selected_path_label.config(text=str(self.selected_path))
            '''self.master.master.shop_name_Combobox.current(0)
            self.code_entry.delete(0, tk.END)
            self.color_entry.delete(0, tk.END)
            self.size_entry.delete(0, tk.END)
            self.bracode_entry.delete(0, tk.END)
            self.qty_entry.delete(0, tk.END)
            self.images_entry.delete(0, tk.END)
            for i, value in enumerate(found_values):
                if i == 0:
                    self.master.master.shop_name_Combobox.current(self.Shops_Names.index(value))
                if i == 1:
                    self.code_entry.insert(0, value)
                if i == 2:
                    self.color_entry.insert(0, value)
                if i == 3:
                    self.size_entry.insert(0, value)
                if i == 7:
                    self.qty_entry.insert(0, value)
                if i == 9:
                    self.bracode_entry.insert(0, value)
                if i == 10:
                    self.images_entry.insert(0, value)'''
        print("selected self.nested_list = "+str(self.nested_list))





    #
    #
    #
    # Others
    #
    #
    #
    
    # get all name that are semilar to new item
    def on_name_entry(self, event):
        query = self.name_entry.get()
        if query == "":
            self.name_list.place_forget()
            return
        
        products = search_n_c_b_products(query)
        if products:
            self.name_list.config(width=self.name_entry.winfo_width())
            self.name_list.place(x=self.name_entry.winfo_x(), y=self.name_entry.winfo_y()+self.name_entry.winfo_height()+25)
            self.name_list.delete(0, tk.END)
            for product in products:
                #TODO MAKE IT EASY BY ID
                #print("on_name_entry\n"+str(product[1]))
                self.name_list.insert(tk.END, f"{product[0]}  {product[1]}")
        else:
            self.name_list.place_forget()
            
    def clear_product_details_widget(self):
        # Clear the product details widgets
        self.name_entry.delete(0, tk.END)
        self.code_entry.delete(0, tk.END)
        #self.type_entry.delete(0, tk.END) self.type_entry
        #self.barcode_entry.delete(0, tk.END)
        #self.at_shop_entry.delete(0, tk.END)
        #self.quantity_entry.delete(0, tk.END)

        self.inventory = []
        self.nested_list = []
        # Clear the product tree
        self.tree.delete(*self.tree.get_children())
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
        self.tax_entry.insert(0, "0")
        self.default_quantity_change_var.set(1)
        self.active_var.set(1)
        

    # Define the function for adding a new product
    def add_product(self):
        # Get the values from the product details widgets
        # Get the values from the product details widgets
        at_shop = ""
        found_shop_items = []
        for s, shop in enumerate(self.Shops):
            print("Loop s ", s)
            print("Loop Shop ", shop['Shop_name'])
            print("Selected s ", self.master.master.shop_name_Combobox.current())
            print("Selected Shop ", self.master.master.shop_name_Combobox.get())
            if (shop['Shop_name'] == "" or (s == self.master.master.shop_name_Combobox.current() and self.master.master.shop_name_Combobox.get() == shop['Shop_name'])):
                at_shop = shop['Shop_Id']
                print(" Found ", at_shop)
                if shop['Shop_items']:
                    print("Shop items = ", shop['Shop_items'])
                    found_shop_items = json.loads(shop['Shop_items'])
                    print("Shop items --> ", found_shop_items)
                    
        name = self.name_entry.get()
        code = self.code_entry.get()
        typ = json.dumps(self.type_entry.get_value)
        barcode = ""
        #self.barcode_entry.get()
        # self.at_shop_entry.get()
        quantity = 0
        # self.quantity_entry.get()
        cost = float(self.cost_entry.get())
        tax = float(self.tax_entry.get())
        price = float(self.price_entry.get())
        include_tax = int(self.include_tax_var.get())
        price_change = int(self.price_change_var.get())
        more_info = json.dumps(self.nested_list)
        images = self.images_entry.get()
        description = self.description_entry.get()
        service = self.service_change_var.get()
        default_quantity = int(self.default_quantity_change_var.get())
        active = int(self.active_var.get())
            
        print(str([name, code, typ, barcode, at_shop, quantity, cost, tax, price, include_tax, price_change, more_info, images, description, service, default_quantity, active]))
        
        item = ""
        doc_type = ""
        
        brcod = ""

        # doc_code = "1"
        # Year:Month-docType 1 doccreateplatform 1 doc_numb
        #TODO make it create randim number so that ont to count
        date = datetime.datetime.now().strftime('%y-%m-%d')
        doc_code = datetime.datetime.now().strftime('%y:%m') + "-11"
        b = 0
        while True:
            ex_doc = cur.execute("SELECT * FROM upload_doc WHERE doc_barcode=?", (doc_code+str(b),)).fetchone()
            if ex_doc:
                b = random.randint(0, 10000)
            else:
                brcod = doc_code+str(b)
                break

        if self.add_button.cget("text") == "New" or self.add_button.cget("text") == "Add":        
            # Insert the new product into the database
            doc_type = "Add_Items"
            # Get the ID of the most recently added item
            cur.execute('INSERT INTO product (name, code, type, barcode, at_shop, quantity, cost, tax, price, include_tax, price_change, more_info, images, description, service, default_quantity, active) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (name, code, typ, barcode, at_shop, quantity, cost, tax, price, include_tax, price_change, more_info, images, description, service, default_quantity, active))
            cur.execute("SELECT last_insert_rowid()")
            new_item_id = cur.fetchone()[0]
            print("new_product_id : " + str(new_item_id) + " barcode : " + str(brcod))
            item += f"(:{new_item_id}:,:{name}:,:{code}:,:{typ}:,:{barcode}:,:{at_shop}:,:{quantity}:,:{cost}:,:{tax}:,:{price}:,:{include_tax}:,:{price_change}:,:{more_info}:,:{images}:,:{description}:,:{service}:,:{default_quantity}:,:{active}:)"
            print("item : " + str(item))
            # Commit the changes to the database
            conn.commit()
            found_shop_items.append([new_item_id, 1, date, date, date])
            ITEM = json.dumps(found_shop_items)
            print("ITEM : " + str(ITEM))
            print("at_shop : " + str(at_shop))
            cur.execute('UPDATE Shops SET Shop_items=? WHERE Shop_id=?', (ITEM, at_shop))
            for s, shop in enumerate(self.Shops):
                print("Loop s ", s)
                print("Loop Shop ", shop['Shop_name'])
                print("Selected s ", self.master.master.shop_name_Combobox.current())
                print("Selected Shop ", self.master.master.shop_name_Combobox.get())
                if (shop['Shop_name'] == "" or (s == self.master.master.shop_name_Combobox.current() and self.master.master.shop_name_Combobox.get() == shop['Shop_name'])):
                    at_shop = shop['Shop_Id']
                    print(" Found ", at_shop)
                    shop['Shop_items'] = ITEM
        elif self.product_id != -1:
            print("product_id : " + str(self.product_id) + " barcode : " + str(brcod))
            doc_type = "Update_Items"
            item += f"(:{self.product_id}:,:{name}:,:{code}:,:{typ}:,:{barcode}:,:{at_shop}:,:{quantity}:,:{cost}:,:{tax}:,:{price}:,:{include_tax}:,:{price_change}:,:{more_info}:,:{images}:,:{description}:,:{service}:,:{default_quantity}:,:{active}:)"
            print("item : " + str(item))
            # Update the product in the database
            cur.execute('UPDATE product SET name=?, code=?, type=?, barcode=?, at_shop=?, quantity=?, cost=?, tax=?, price=?, include_tax=?, price_change=?, more_info=?, images=?, description=?, service=?, default_quantity=?, active=? WHERE id=?', (name, code, typ, barcode, at_shop, quantity, cost, tax, price, include_tax, price_change, more_info, images, description, service, default_quantity, active, self.product_id))
        # Commit the changes to the database
        conn.commit()

        try:
            # Insert the record into the upload_doc table
            cur.execute('INSERT INTO upload_doc (doc_barcode, extension_barcode, user_id, customer_id, type, item, qty, price, discount, tax, payments, doc_created_date, doc_expire_date, doc_updated_date) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', ("23-200-" + str(brcod), "extension_barcode", self.user_info['id'], "", doc_type, item, 1, 0, 0, 0, "payments_", "doc_created_date", "doc_expire_date", "doc_updated_date"))

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
        self.master.master.Load_Shop_items() # refrash items
        self.destroy()

# Product Quick Edition Form
#  A form for quickly adding or editing multiple products at once.
#
class ProductQueckEditionForm(ttk.Notebook):
    def __init__(self, master, user, Shops):
        ttk.Notebook.__init__(self, master)
        self.master = master
        self.user_info = user
        self.Shops = Shops
        self.New_Item_Contener = []
        self.notebook_frame = self
        self.details_frame = tk.Frame(self)
        self.details_frame.pack(fill=tk.BOTH, expand=1)

        self.notebook_frame.add(self.details_frame, text="Add / Edit Multiple Items")

        self.List_Frame = tk.Frame(self.details_frame)
        self.List_Frame.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        
        self.New_item_contener_canvas = tk.Canvas(self.List_Frame)
        self.New_item_contener_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        
        self.New_item_contener_scrollbar = tk.Scrollbar(self.List_Frame, orient='vertical', command=self.New_item_contener_canvas.yview)
        self.New_item_contener_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.New_item_contener_xscrollbar = tk.Scrollbar(self.details_frame, orient='horizontal', command=self.New_item_contener_canvas.xview)
        self.New_item_contener_xscrollbar.pack(side=tk.TOP, fill=tk.X)
        
        self.New_item_contener_canvas.configure(xscrollcommand=self.New_item_contener_xscrollbar.set, yscrollcommand=self.New_item_contener_scrollbar.set)
        #self.New_item_contener_canvas.bind('<Configure>', lambda e: self.New_item_contener_canvas.configure(scrollregion=self.New_item_contener_canvas.bbox("all")))

        self.New_item_conteners_frame = tk.Frame(self.New_item_contener_canvas)
        self.New_item_contener_canvas.create_window((0, 0), window=self.New_item_conteners_frame, anchor=tk.NW)
        self.New_item_conteners_frame.bind('<Configure>', lambda e: self.New_item_contener_canvas.configure(scrollregion=self.New_item_contener_canvas.bbox("all")))

        
        # Create a header frame to keep packing consistent (pack header_frame into details_frame,
        # then use grid inside header_frame for neat alignment)
        header_frame = tk.Frame(self.details_frame)
        header_frame.pack(fill=tk.X, padx=5, pady=5)

        # Left: summary/status labels (use a status subframe and grid inside it)
        status_frame = tk.Frame(header_frame)
        status_frame.grid(row=0, column=0, sticky="w", padx=(0, 10))

        self.Count_label = tk.Label(status_frame, text='Count : 0')
        self.Count_label.grid(row=0, column=0, sticky="w", padx=4)
        self.QTY_label = tk.Label(status_frame, text='QTY : 0')
        self.QTY_label.grid(row=0, column=1, sticky="w", padx=4)
        self.Cost_label = tk.Label(status_frame, text='Cost : 0')
        self.Cost_label.grid(row=0, column=2, sticky="w", padx=4)
        self.After_label = tk.Label(status_frame, text='After : 0')
        self.After_label.grid(row=0, column=3, sticky="w", padx=4)

        # Right: payment widgets (use a labeled frame and grid inside it)
        self.payment_frame = tk.LabelFrame(header_frame, text="Payments", padx=5, pady=5)
        self.payment_frame.grid(row=0, column=1, sticky="e", padx=5)

        # Use StringVar so we can trace changes and validate
        self.credit_var = tk.StringVar(value="0")
        self.cash_var = tk.StringVar(value="0")
        self.card_var = tk.StringVar(value="0")

        self.credit_label = tk.Label(self.payment_frame, text="Credit amount:")
        self.credit_label.grid(row=0, column=0, sticky="w", padx=5, pady=2)
        self.credit_entry = tk.Entry(self.payment_frame, textvariable=self.credit_var, state='normal')
        self.credit_entry.grid(row=0, column=1, sticky="we", padx=5, pady=2)

        self.cash_label = tk.Label(self.payment_frame, text="Cash amount:")
        self.cash_label.grid(row=1, column=0, sticky="w", padx=5, pady=2)
        self.cash_entry = tk.Entry(self.payment_frame, textvariable=self.cash_var)
        self.cash_entry.grid(row=1, column=1, sticky="we", padx=5, pady=2)

        self.card_label = tk.Label(self.payment_frame, text="Card amount:")
        self.card_label.grid(row=2, column=0, sticky="w", padx=5, pady=2)
        self.card_entry = tk.Entry(self.payment_frame, textvariable=self.card_var)
        self.card_entry.grid(row=2, column=1, sticky="we", padx=5, pady=2)

        # Feedback label for validation
        self.payment_warn_label = tk.Label(self.payment_frame, text="", fg="red")
        self.payment_warn_label.grid(row=3, column=0, columnspan=2, sticky="w", padx=5)

        # Make payment entry column expand
        self.payment_frame.columnconfigure(1, weight=1)

        # internal guard to avoid recursive trace loops
        self._updating_payment_vars = False

        def _to_float(s):
            try:
                return float(s) if s not in ("", None) else 0.0
            except Exception:
                return 0.0

        def _get_total_cost_from_label():
            # Expected format set by update_multy_infor: 'Total Cost : {cost} Total Price : {price}'
            txt = ""
            try:
                txt += self.Cost_label.cget('text')
            except Exception:
                return 0.0
            try:
                if "Total Cost" in txt and "Total Price" in txt:
                    # extract between "Total Cost :" and "Total Price :"
                    start = txt.index("Total Cost") 
                    # find colon after Total Cost
                    colon = txt.index(":", start) + 1
                    end = txt.index("Total Price", colon)
                    val = txt[colon:end].strip()
                    return float(val)
                elif "Total Cost" in txt:
                    colon = txt.index(":") + 1
                    val = txt[colon:].strip()
                    return float(val)
            except Exception:
                return 0.0
            return 0.0

        def validate_payments(*args):
            # Avoid re-entrance
            if self._updating_payment_vars:
                return True
            self._updating_payment_vars = True
            try:
                cash = _to_float(self.cash_var.get())
                card = _to_float(self.card_var.get())
                total_cost = _get_total_cost_from_label()
                # Compute credit as: cost_label - cash - card (per request)
                computed_credit = total_cost - cash - card
                # Normalize small rounding errors
                computed_credit = round(computed_credit, 2)
                # Update credit var only if changed to avoid infinite loop
                current_credit = _to_float(self.credit_var.get())
                if current_credit != computed_credit:
                    # set as string
                    self.credit_var.set(str(computed_credit))
                # Validation: credit should not be negative
                if computed_credit >= 0:
                    self.payment_warn_label.config(text="")
                    ok = True
                else:
                    self.payment_warn_label.config(text="Error: Credit would be negative (cost - cash - card < 0)")
                    ok = False
                # Enable/disable process button to guide user
                if hasattr(self, 'Process_button'):
                    try:
                        self.Process_button.config(state='normal' if ok else 'disabled')
                    except Exception:
                        pass
                self.payments_valid = ok
                return ok
            finally:
                self._updating_payment_vars = False

        # trace changes
        try:
            self.cash_var.trace_add('write', validate_payments)
            self.card_var.trace_add('write', validate_payments)
            # credit_var is derived; still trace to revalidate if user edits it
            self.credit_var.trace_add('write', validate_payments)
        except Exception:
            self.cash_var.trace('w', validate_payments)
            self.card_var.trace('w', validate_payments)
            self.credit_var.trace('w', validate_payments)

        # Wrap existing add_product to enforce validation at call time.
        if hasattr(self, 'add_product'):
            _orig_add = self.add_product

            def _add_with_validation():
                if validate_payments():
                    return _orig_add()
                else:
                    tk.messagebox.showerror("Payment Error", "Invalid payments: credit would be negative.")
                    return

            self.add_product = _add_with_validation

        # run validation once initially
        validate_payments()

        # Add button (kept in details_frame)
        self.add_button = tk.Button(self.details_frame, text='Add', command=self.Add_New_Item)
        self.add_button.pack(side=tk.LEFT, padx=5, pady=5)
        self.Process_button = tk.Button(self.details_frame, text='Process', command=self.add_product)
        self.Process_button.pack(side=tk.RIGHT)
        def cancle():
            if hasattr(self.master.master, 'List_Frame_contaner_frame'):
                self.master.master.List_Frame_contaner_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            self.destroy()
        self.cancle_button = tk.Button(self.details_frame, text='Cancle', command=cancle)
        self.cancle_button.pack(side=tk.RIGHT)
        
        self.Add_New_Item()

    def Add_New_Item(self):
        
        New_item_contener_frame = tk.Frame(self.New_item_conteners_frame, highlightthickness=2, highlightbackground="black")
        New_item_contener_frame.pack(fill=tk.X, pady=10)
        
        def cancle_new_item(contener, i):
            self.New_Item_Contener.remove(self.New_Item_Contener[i])
            contener.destroy()
            self.update_multy_infor()

        def Clear_new_item(i):
            for j, item in enumerate(self.New_Item_Contener[i]):
                if j == 0 or j == 4:
                    continue
                elif j < 7:
                    item.delete(0, tk.END)
                else:
                    item.set('0')
            self.update_multy_infor()

        def on_name_entry(name_entry, name_list):
            query = name_entry.get()
            if query == "":
                name_list.place_forget()
                return
            
            products = search_n_c_b_products(query)
            if products:
                name_list.config(width=name_entry.winfo_width())
                name_list.place(x=name_entry.winfo_x(), y=name_entry.winfo_y()+name_entry.winfo_height()+25)
                name_list.delete(0, tk.END)
                for product in products:
                    #TODO MAKE IT EASY BY ID
                    #print("on_name_entry\n"+str(product[1]))
                    name_list.insert(tk.END, f"{product[0]}  {product[1]}")
            else:
                name_list.place_forget()
            self.update_multy_infor()
                
        cancle_button = tk.Button(New_item_contener_frame, text='Cancle', command=lambda con=New_item_contener_frame, on=len(self.New_Item_Contener):cancle_new_item(con, on))
        clear_button = tk.Button(New_item_contener_frame, text='Clear', command=lambda on=len(self.New_Item_Contener): Clear_new_item(on))
        Copy_button = tk.Button(New_item_contener_frame, text='Copy', command=self.Add_New_Item)
        
        # Create the widgets for the product details
        name_label = tk.Label(New_item_contener_frame, text='Name:')
        name_entry = tk.Entry(New_item_contener_frame)
        main_name = ""
        name_list = tk.Listbox(name_entry.master.master)
        name_entry.bind('<KeyRelease>', lambda e, n=name_list, i=name_entry: on_name_entry(i, n))

        type_label = tk.Label(New_item_contener_frame, text='Type:')
        type_frame = tk.Frame(New_item_contener_frame)
        # get nodes by stting
        type_entry = NodeSelectorApp(type_frame, self.user_info)
        type_entry.load("")
        
        code_label = tk.Label(New_item_contener_frame, text='CODE:')
        code_entry = tk.Entry(New_item_contener_frame)
        cost_label = tk.Label(New_item_contener_frame, text='Cost:')
        cost_entry = tk.Entry(New_item_contener_frame)
        cost_entry.insert(0, "0")
        cost_entry.bind('<KeyRelease>', lambda e: self.update_multy_infor())
        qty_label = tk.Label(New_item_contener_frame, text='Quantity:')
        qty_entry = tk.Entry(New_item_contener_frame)
        qty_entry.insert(0, "0")
        qty_entry.bind('<KeyRelease>', lambda e: self.update_multy_infor())
        price_label = tk.Label(New_item_contener_frame, text='Price:')
        price_entry = tk.Entry(New_item_contener_frame)
        price_entry.insert(0, "0")
        price_entry.bind('<KeyRelease>', lambda e: self.update_multy_infor())
        Total_label = tk.Label(New_item_contener_frame, text='Total cost: 0 \n Total Price: 0\n Total Profit: 0', justify=tk.LEFT)
        
        description_label = tk.Label(New_item_contener_frame, text='Description:')
        description_entry = tk.Entry(New_item_contener_frame)
        default_quantity_change_var = tk.IntVar()
        default_quantity_change_checkbutton = tk.Checkbutton(New_item_contener_frame, text='Default Quantity', variable=default_quantity_change_var)
        active_var = tk.IntVar()
        active_checkbutton = tk.Checkbutton(New_item_contener_frame, text='Active', variable=active_var)
        price_change_var = tk.IntVar()
        price_change_checkbutton = tk.Checkbutton(New_item_contener_frame, text='Price Change', variable=price_change_var)

        cancle_button.grid(row=0, column=0)
        clear_button.grid(row=1, column=0)
        Copy_button.grid(row=2, column=0)
        
        name_label.grid(row=0, column=1)
        name_entry.grid(row=1, column=1)
        type_label.grid(row=2, column=1)
        type_frame.grid(row=3, column=1)
        code_label.grid(row=0, column=2)
        code_entry.grid(row=1, column=2)
        qty_label.grid(row=2, column=2)
        qty_entry.grid(row=3, column=2)
        cost_label.grid(row=0, column=3)
        cost_entry.grid(row=1, column=3)
        price_label.grid(row=2, column=3)
        price_entry.grid(row=3, column=3)
        description_label.grid(row=0, column=4)
        description_entry.grid(row=1, column=4)
        Total_label.grid(row=2, column=4, rowspan=2)
        default_quantity_change_checkbutton.grid(row=2, column=7)
        price_change_checkbutton.grid(row=3, column=7)
        active_checkbutton.grid(row=0, column=7)
        
        self.New_Item_Contener.append([New_item_contener_frame, name_entry, code_entry, qty_entry, type_entry, cost_entry, price_entry, Total_label, description_entry, default_quantity_change_var, price_change_var, active_var])
        self.update_multy_infor()

    def update_multy_infor(self):
        qty = 0
        cost = 0
        price = 0
        for new_item in self.New_Item_Contener:
            if new_item[3].get() != '':
                try:
                    qty += float(new_item[3].get())
                    icost = float(new_item[3].get())*float(new_item[5].get())
                    iprice = float(new_item[3].get())*float(new_item[6].get())
                    if new_item[5].get() != '':
                        cost += icost
                    if new_item[5].get() != '':
                        price += iprice
                    new_item[7].config(text='Sum cost: '+str(icost)+' \n Sum Price: '+str(iprice)+'\n Sum Profit: '+str(iprice-icost))
                except Exception:
                    pass
        self.Count_label.config(text='Count : '+str(len(self.New_Item_Contener)))
        self.QTY_label.config(text='Total QTY : '+str(qty))
        self.credit_entry.delete(0, tk.END)
        self.credit_entry.insert(0, str(cost))
        self.Cost_label.config(text='Total Cost : '+str(cost)+ ' Total Price : '+str(price))
        self.After_label.config(text='Total Profit : '+str(price-cost))
        
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
        self.update_multy_infor()

    # Define the function for adding a new product
    def add_product(self):
        # Collect created items to build one doc entry at the end
        doc_items = []
        created_ids = []
        date_now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
        # determine a unique document barcode once
        base_doc_code = datetime.datetime.now().strftime('%y:%m') + "-11"
        suffix = datetime.datetime.now().strftime('%f')
        while True:
            candidate = base_doc_code + suffix
            ex_doc = fetch_as_dict_list("SELECT 1 FROM doc_table WHERE doc_barcode=?", (candidate,))
            if ex_doc:
                ex_doc = ex_doc[0]
                try:
                    suffix = str(int(suffix) + 1)
                except Exception:
                    suffix = '1'
            else:
                brcod = candidate
            break

        for new_item in self.New_Item_Contener:
            # Resolve shop and existing shop items
            at_shop = ""
            found_shop_items = []
            for s, shop in enumerate(self.Shops):
                if (shop.get('Shop_name', "") == "" or
                    (s == self.master.master.shop_name_Combobox.current() and
                    self.master.master.shop_name_Combobox.get() == shop.get('Shop_name', ""))):
                    at_shop = shop.get('Shop_Id')
                    if shop.get('Shop_items'):
                        try:
                            found_shop_items = json.loads(shop['Shop_items'])
                        except Exception:
                            found_shop_items = []

            # Read fields with safe fallbacks
            name = new_item[1].get() if hasattr(new_item[1], 'get') else ""
            code = new_item[2].get() if hasattr(new_item[2], 'get') else ""
            quantity = new_item[3].get() if hasattr(new_item[3], 'get') else "0"
            try:
                quantity_f = float(quantity) if quantity != '' else 0.0
            except Exception:
                quantity_f = 0.0
            typ = new_item[4].get_value if hasattr(new_item[4], 'get_value') else []
            barcode = ""
            try:
                barcode = new_item[4].get() if hasattr(new_item[4], 'get') else ""
            except Exception:
                barcode = ""
            
            try:
                cost = float(new_item[5].get()) if new_item[5].get() != '' else 0.0
            except Exception:
                cost = 0.0
            
            try:
                price = float(new_item[6].get()) if new_item[6].get() != '' else 0.0
            except Exception:
                price = 0.0
            include_tax = 1
            description = new_item[8].get() if hasattr(new_item[8], 'get') else ""
            try:
                default_quantity = int(new_item[9].get()) if new_item[9].get() != '' else 0
            except Exception:
                default_quantity = 0
            try:
                price_change = int(new_item[10].get()) if new_item[10].get() != '' else 0
            except Exception:
                price_change = 0
            try:
                active = int(new_item[11].get()) if new_item[11].get() != '' else 0
            except Exception:
                active = 0
            images = ""
            service = 0

            # Build more_info structure (keep compatible with existing format)
            if typ and len(typ) > 0:
                types_info = []
            for type_ in typ:
                new_type = json.dumps(type_)
                types_info.append([barcode, new_type, price, quantity_f, quantity_f, "", json.dumps([]), "", ""])
            else:
                types_info = [[barcode, json.dumps([]), price, quantity_f, quantity_f, "", json.dumps([]), "", ""]]

            more_info = json.dumps([[self.master.master.shop_name_Combobox.get(), [[code, [["DEF_COLOR", [["DEF_SIZE", types_info]]]]]]]])

            # Insert product row
            try:
                newidedproduct = Set_product(None, ['name', 'code', 'type', 'barcode', 'at_shop', 'quantity', 'cost', 'tax', 'price', 'include_tax', 'price_change', 'more_info', 'images', 'description', 'service', 'default_quantity', 'active'],[name, code, json.dumps(typ), barcode, at_shop, quantity_f, cost, 0.0, price, include_tax, price_change, more_info, images, description, service, default_quantity, active])
                new_item_id = newidedproduct['id']
                created_ids.append(newidedproduct['id'])
                # update shop items
                found_shop_items.append([new_item_id, 1, date_now, date_now, date_now])
                ITEM = json.dumps(found_shop_items)
                Update_Shop(None, self.user_info, ['Shop_items'], [ITEM], ['Shop_id'], [at_shop])
                # record for doc_table
                doc_items.append([new_item_id, code, "Barcode", name, "Color", "Size", cost, quantity_f, price, 0, more_info])
                
                #print("ITEM : " + str(ITEM))
                #print("at_shop : " + str(at_shop))
                Update_Documente(None, ['Shop_items'], [ITEM], ['Shop_id=?'], [at_shop])
                for s, shop in enumerate(self.Shops):
                    #print("Loop s ", s)
                    #print("Loop Shop ", shop['Shop_name'])
                    #print("Selected s ", self.master.master.shop_name_Combobox.current())
                    #print("Selected Shop ", self.master.master.shop_name_Combobox.get())
                    if (shop['Shop_name'] == "" or (s == self.master.master.shop_name_Combobox.current() and self.master.master.shop_name_Combobox.get() == shop['Shop_name'])):
                        at_shop = shop['Shop_Id']
                        #print(" Found ", at_shop)
                        shop['Shop_items'] = ITEM
        
            except Exception as e:
                print("Error inserting product:", e)

        # If no items created, skip doc insert
        if not doc_items:
            conn.commit()
            return

        # Compute totals for the doc entry
        count_new_items = sum(item[7] for item in doc_items)
        # item layout: [id, name, code, qty, cost, price, more_info]
        total_price = sum(item[8] * item[7] for item in doc_items)  # price * qty
        total_cost = sum(item[6] * item[7] for item in doc_items)   # cost * qty
        total_profit = total_price - total_cost

        # Determine user_id and customer_id
        user_id = ""
        if isinstance(getattr(self, 'user', None), dict):
            user_id = self.user.get('User_id', "")
        if not user_id and isinstance(getattr(self, 'user_info', None), dict):
            user_id = self.user_info.get('id', self.user_info.get('User_id', ""))
        customer_id = getattr(self, 'customer', "") or ""

        # Payment form: collect credit stock, cash stock, card stock
        payments_result = []
        try:
            credit_amt = float(self.credit_entry.get()) if self.credit_entry.get() not in ("", None) else 0.0
        except Exception:
            credit_amt = 0.0
        try:
            cash_amt = float(self.cash_entry.get()) if self.cash_entry.get() not in ("", None) else 0.0
        except Exception:
            cash_amt = 0.0
        try:
            card_amt = float(self.card_entry.get()) if self.card_entry.get() not in ("", None) else 0.0
        except Exception:
            card_amt = 0.0

        # payment = [pay_type, amount, ispay_pide, payment_method]
        xid = -1
        if credit_amt > 0:
            xid += 1
            payments_result.append([xid, "CREDITSTOCK", credit_amt, date_now, date_now, user_id, 1, "", "CREDITSTOCK"])
        if cash_amt > 0:
            xid += 1
            payments_result.append([xid, "CASHSTOCK", cash_amt, date_now, date_now, user_id, 1, "", "CASHSTOCK"])
        if card_amt > 0:
            xid += 1
            payments_result.append([xid, "CARDSTOCK", card_amt, date_now, date_now, user_id, 1, "", "CARDSTOCK"])
        payments_json = json.dumps(payments_result) if payments_result else json.dumps([])

        # Insert a single doc_table record representing this batch (store payments)
        try:
            Set_Document(None, ['doc_barcode', 'extension_barcode', 'At_Shop_Id', 'user_id', 'customer_id', 'Seller_id', 'type', 'item', 'qty', 'price', 'Profite', 'discount', 'tax', 'payments', 'pid', 'doc_created_date', 'doc_expire_date', 'doc_updated_date'], [brcod, "extension_barcode", at_shop, user_id, customer_id, "", "Stocked_Items", json.dumps(doc_items), count_new_items, total_price, total_profit, 0, 0, payments_json, "", date_now, date_now, date_now])
            
        except Exception as e:
            print("Error inserting doc_table:", e)
            

        # Clear the product details widgets
        #self.clear_product_details_widget()
        self.master.master.Load_Shop_items() # refrash items
        self.destroy()

