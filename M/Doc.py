import sqlite3
import tkinter as tk
from tkinter import ttk
import tkinter as tk
from tkinter import ttk
import sqlite3
import shutil
import datetime
import atexit

import json
import ast

import os, sys
current_dir = os.path.abspath(os.path.dirname(__file__))
MAIN_dir = os.path.join(current_dir, '..')
sys.path.append(MAIN_dir)
from D.docediterform import DocEditForm
from D.printer import PrinterForm
from C.slipe import load_slip

from C.API import *
from C.API.Get import *
from C.API.Set import *

from C.List import *

import os
# Create a connection to the SQLite database
data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data'))
db_path = os.path.join(data_dir, 'my_database.db')

from D.Getdate import GetDateForm
from D.Chart.Chart import *
import re

class DocForm(tk.Frame):
    def __init__(self, master, user, shop):
        tk.Frame.__init__(self, master)
        self.pyment_used = []
        self.shop = shop
        self.user_info = user
        # Notebook widget - CENTER_NOTEBOK
        self.start_value = datetime.datetime.now().strftime('%Y-%m-%d')
        self.end_value = self.start_value
        
        self.center_notebook = ttk.Notebook(self)
        self.center_notebook.pack(side="top", fill="both", expand=True)


        self.Frame_contaner_frame = tk.Frame(self.center_notebook)
        self.Frame_contaner_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.List_Frame_contaner_frame = tk.Frame(self.Frame_contaner_frame)
        self.List_Frame_contaner_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.List_Frame = tk.Frame(self.List_Frame_contaner_frame)
        self.List_Frame.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        
        self.item_List_canvas = tk.Canvas(self.List_Frame)
        self.item_List_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        
        self.item_List_yscrollbar = tk.Scrollbar(self.List_Frame, orient='vertical', command=self.item_List_canvas.yview)
        self.item_List_yscrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.item_List_xscrollbar = tk.Scrollbar(self.List_Frame_contaner_frame, orient='horizontal', command=self.item_List_canvas.xview)
        self.item_List_xscrollbar.pack(side=tk.TOP, fill=tk.X)
        
        self.item_List_canvas.configure(xscrollcommand=self.item_List_xscrollbar.set, yscrollcommand=self.item_List_yscrollbar.set)
        #self.New_item_contener_canvas.bind('<Configure>', lambda e: self.New_item_contener_canvas.configure(scrollregion=self.New_item_contener_canvas.bbox("all")))

        self.Selected_item_Display_frame = tk.Frame(self.item_List_canvas)
        self.item_List_canvas.create_window((0, 0), window=self.Selected_item_Display_frame, anchor=tk.NW)
        self.Selected_item_Display_frame.bind('<Configure>', lambda e: self.item_List_canvas.configure(scrollregion=self.item_List_canvas.bbox("all")))

        
        self.Doc_tab = ttk.Frame(self.Selected_item_Display_frame)
        self.Doc_tab.grid()

        # Add tabs to the self.center_notebook
        self.center_notebook.add(self.Frame_contaner_frame, text='Documents')

        self.Doc_tab.grid_columnconfigure(0, weight=1)
        self.Doc_tab.grid_columnconfigure(1, weight=1)
        self.Doc_tab.grid_columnconfigure(2, weight=1)
        self.Doc_tab.grid_columnconfigure(3, weight=1)
        self.Doc_tab.grid_columnconfigure(4, weight=1)
        self.Doc_tab.grid_columnconfigure(5, weight=1)
        self.Doc_tab.grid_columnconfigure(6, weight=1)
        self.Doc_tab.grid_columnconfigure(7, weight=1)
        self.Doc_tab.grid_columnconfigure(8, weight=1)
        self.Doc_tab.grid_rowconfigure(0, weight=1)
        self.Doc_tab.grid_rowconfigure(1, weight=1)
        self.Doc_tab.grid_rowconfigure(2, weight=1)
        self.Doc_tab.grid_rowconfigure(3, weight=1)
        self.Doc_tab.grid_rowconfigure(4, weight=1)
        self.Doc_tab.grid_rowconfigure(5, weight=1)
        self.Doc_tab.grid_rowconfigure(6, weight=1)




        
        self.details_frame = tk.Frame(self.Doc_tab)
        self.details_frame.grid(row=0, column=0, rowspan=5, sticky="nsew")
        
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

        # Create the label and entry for the sold item info search
        self.sold_item_info_label = tk.Label(self.details_frame, text="Sold Item Info:")
        self.sold_item_info_label.grid(row=0, column=5)
        self.sold_item_info_entry = tk.Entry(self.details_frame)
        self.sold_item_info_entry.grid(row=1, column=5)


        # Create the label and entry for the discount search
        self.discount_label = tk.Label(self.details_frame, text="Discount:")
        self.discount_label.grid(row=0, column=6)
        self.discount_entry = tk.Entry(self.details_frame)
        self.discount_entry.grid(row=1, column=6)
        
        
        # Create the label and entry for the user ID search
        user_info = fetch_as_dict_list('SELECT * FROM USERS', ())  
        # prepare names lists with a blank first entry for null selection
        self.user_names = [''] + [u['User_name'] for u in user_info] if user_info else ['']
        self.customer_names = [''] + [u['User_name'] for u in user_info] if user_info else ['']

        # maps including blank -> ''
        self.user_map = {'': ''}
        self.customer_map = {'': ''}
        if user_info:
            for u in user_info:
                if u['User_id'] is None:
                    uid = u['Id']
                else:
                    uid = u['User_id']
                self.user_map[u['User_name']] = str(uid)
                self.customer_map[u['User_name']] = str(uid)

        self.user_id_var = tk.StringVar()    # will store the actual user_id (used by perform_search via .get())
        self.user_name_var = tk.StringVar()  # displayed in the combobox

        self.user_combobox = ttk.Combobox(self.details_frame, textvariable=self.user_name_var, values=self.user_names, state='readonly')
        self.user_combobox.grid(row=3, column=0)

        # Combobox for User ID (shows user_name but stores user_id)
        self.user_id_label = tk.Label(self.details_frame, text="User ID:")
        self.user_id_label.grid(row=2, column=0)

        def _on_user_selected(event=None):
            name = self.user_name_var.get()
            self.user_id_var.set(self.user_map.get(name, ''))

        self.user_combobox.bind('<<ComboboxSelected>>', _on_user_selected)

        # Set default selection:
        # If self.user_info matches a user, select it; otherwise leave blank (index 0)
        try:
            default_idx = 0
            if self.user_info:
                # if dict with User_name or User_id try to match
                if isinstance(self.user_info, dict):
                    uname = self.user_info.get('User_name')
                    if uname and uname in self.user_names:
                        default_idx = self.user_names.index(uname)
                    else:
                        uid = str(self.user_info.get('User_id', ''))
                        for name, idv in self.user_map.items():
                            if idv == uid and name in self.user_names:
                                default_idx = self.user_names.index(name)
                                break
            else:
                # self.user_info might be a plain name or id
                s = str(self.user_info)
                if s in self.user_names:
                    default_idx = self.user_names.index(s)
                else:
                    for name, idv in self.user_map.items():
                        if idv == s and name in self.user_names:
                            default_idx = self.user_names.index(name)
                            break
            self.user_combobox.current(default_idx)
            self.user_name_var.set(self.user_names[default_idx])
            self.user_id_var.set(self.user_map.get(self.user_names[default_idx], ''))
        except Exception:
            # fallback: leave blank selection
            try:
                self.user_combobox.current(0)
                self.user_name_var.set('')
                self.user_id_var.set('')
            except Exception:
                pass

        # Keep compatibility with other code using self.user_id_entry.get()
        self.user_id_entry = self.user_id_var


        # Create the label and entry for the customer ID search
        self.customer_id_label = tk.Label(self.details_frame, text="Customer ID:")
        self.customer_id_label.grid(row=2, column=1)

        self.customer_id_var = tk.StringVar()    # will store the actual customer_id (used by perform_search via .get())
        self.customer_name_var = tk.StringVar()  # displayed in the combobox
        self.customer_combobox = ttk.Combobox(self.details_frame, textvariable=self.customer_name_var, values=self.customer_names, state='readonly')
        self.customer_combobox.grid(row=3, column=1)
        # Combobox for Customer ID (shows customer_name but stores customer_id) 

        def _on_customer_selected(event=None):
            name = self.customer_name_var.get()
            self.customer_id_var.set(self.customer_map.get(name, ''))

        self.customer_combobox.bind('<<ComboboxSelected>>', _on_customer_selected)
        # TODO: Set default selection if available
        # Keep the original attribute name so other code calling self.customer_id_entry.get() continues to work.
        self.customer_id_entry = self.customer_id_var

        # Create the label and entry for the tax search
        self.seller_id_label = tk.Label(self.details_frame, text="Seller ID:")
        self.seller_id_label.grid(row=2, column=2)
        self.seller_id_entry = tk.Entry(self.details_frame)
        self.seller_id_entry.grid(row=3, column=2)

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

        # Create the search button
        self.search_button = tk.Button(self.details_frame, text="Search", command=self.perform_search)
        self.search_button.grid(row=2, column=6)

        # Create the search button
        self.print_button = tk.Button(self.details_frame, text="Print", command=self.perform_print)
        self.print_button.grid(row=3, column=6)
        self.delet_button = tk.Button(self.details_frame, text="Delet", command=self.perform_delet)
        self.delet_button.grid(row=3, column=7)

        self.total_info = tk.Label(self.details_frame, text="TOTAL DOC : 0\nITEMS : 0 COUNTED\nGrand Total : 0", font=("Arial", 11))
        self.total_info.grid(row=0, column=8, rowspan=2)


        self.info_notebook = ttk.Notebook(self.Doc_tab)
        self.info_notebook.grid(row=5, column=0, rowspan=5, columnspan=7, sticky="nsew")
                

        # Notebook widget - CENTER_NOTEBOK
        self.graph_value = {}
        self.graph_value0 = [["A", 10], ["B", 90], ["C", 50], ["D", 100], ["E", 65], ["F", 500], ["G", 1000], ["H", 85], ["I", 5]]

        self.perform_search()

    def creat_info(self, user_id, vv, collected_values, count_doc, count_items, counted, itemsProfit):
        user_name = user_id
        if user_id is None or user_id == '':
            user_name = "All Users"
        else:

            user_info = fetch_as_dict_list('SELECT * FROM USERS WHERE User_id=?', (str(user_id)))  
            if user_info:
                user = user_info[0]['User_name']
                user_name = user + " Sales Info"
            else:
                user_info = fetch_as_dict_list('SELECT * FROM USERS WHERE Id=?', (str(user_id)))  
                if user_info:
                    user_name = user_info[0]['User_name']

        self.home_tab = ttk.Frame(self.Doc_tab)
        self.home_tab.grid(row=6, column=0, columnspan=7, rowspan=3, sticky="nsew")
        
        # Add tabs to the self.center_notebook
        self.info_notebook.add(self.home_tab, text= user_name)
        
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

        
        self.listtotals_tab = ttk.Frame(self.home_tab)
        # moved listtotals_tab to top of home_tab (row 0) and push other widgets down
        self.listtotals_tab.grid(row=0, column=0, columnspan=7, rowspan=5, sticky="nsew")

        Frame_contaner_frame = tk.Frame(self.listtotals_tab)
        Frame_contaner_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        List_Frame_contaner_frame = tk.Frame(Frame_contaner_frame)
        List_Frame_contaner_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        List_Frame = tk.Frame(List_Frame_contaner_frame)
        List_Frame.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        
        item_List_canvas = tk.Canvas(List_Frame)
        item_List_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        
        item_List_yscrollbar = tk.Scrollbar(List_Frame, orient='vertical', command=item_List_canvas.yview)
        item_List_yscrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        item_List_xscrollbar = tk.Scrollbar(List_Frame_contaner_frame, orient='horizontal', command=item_List_canvas.xview)
        item_List_xscrollbar.pack(side=tk.TOP, fill=tk.X)
        
        item_List_canvas.configure(xscrollcommand=item_List_xscrollbar.set, yscrollcommand=item_List_yscrollbar.set)
        #New_item_contener_canvas.bind('<Configure>', lambda e: New_item_contener_canvas.configure(scrollregion=New_item_contener_canvas.bbox("all")))

        Selected_item_Display_frame = tk.Frame(item_List_canvas)
        item_List_canvas.create_window((0, 0), window=Selected_item_Display_frame, anchor=tk.NW)
        Selected_item_Display_frame.bind('<Configure>', lambda e: item_List_canvas.configure(scrollregion=item_List_canvas.bbox("all")))


        # Create the listbox to display search results
        self.listtotalsbox = ttk.Treeview(Selected_item_Display_frame)        
        self.listtotalsbox.bind('<<TreeviewSelect>>', self.on_select)
        # self.listtotalsbox.bind("<Button-1>", self.on_treeview_double_click)

        collected_by = ''
        collected_value = 0
        if collected_values['years'] is not None and len(collected_values['years']) > 1:
            collected_value = collected_values['years']
            self.listtotalsbox.heading("#0", text='Years')
            collected_by = 'Years'
        elif collected_values['months'] is not None and len(collected_values['months']) > 1:
            collected_value = collected_values['months']
            self.listtotalsbox.heading("#0", text='Months')
            collected_by = 'Months'
        elif collected_values['days'] is not None and len(collected_values['days']) > 1:
            collected_value = collected_values['days']
            self.listtotalsbox.heading("#0", text='Days')
            collected_by = 'Days'
        elif collected_values['hours'] is not None and len(collected_values['hours']) > 1:
            collected_value = collected_values['hours']
            self.listtotalsbox.heading("#0", text='Hours')
            collected_by = 'Hours'
        elif collected_values['minutes'] is not None and len(collected_values['minutes']) > 0:
            collected_value = collected_values['minutes']
            self.listtotalsbox.heading("#0", text='Minutes')
            collected_by = 'Minutes'
        
        if collected_value is not None and collected_value != 0:
            for cv in (collected_value):
                index0_value = cv[0]
                ivs = []
                if cv[1] is not None:
                    iv = []                   
                    for columindex, vi in enumerate(cv[1]):
                        # pay_type, float(pay_pid), ispay_pide
                        pay_type = vi[0]
                        self.listtotalsbox['columns'] = [f"#{i}" for i in range(len(self.listtotalsbox['columns'])+1)]
                        self.listtotalsbox.heading(f"#{columindex+1}", text=pay_type)
                        self.listtotalsbox.column(f"#{columindex+1}", width=100)  

                        pay_pid = float(vi[1])
                        ispay_pid = vi[2]
                        if ispay_pid:
                            iv.append(pay_pid)
                    ivs.append(iv)

                # flatten ivs to numeric values and compute Totale
                flat = []
                for entry in ivs:
                    if isinstance(entry, (list, tuple)):
                        for v in entry:
                            try:
                                flat.append(float(v))
                            except Exception:
                                flat.append(0.0)
                    else:
                        try:
                            flat.append(float(entry))
                        except Exception:
                            flat.append(0.0)
                totale = sum(flat)
                # build values: each column from flat plus final "Totale" column
                values = tuple([round(v, 2) for v in flat] + [round(totale, 2)])
                self.listtotalsbox.insert('', 'end', text=index0_value, values=values)
        
        # Set the size of the self.listbox widget
        self.listtotalsbox.pack(side='top', fill='both', expand=False)

        def on_style_selected(*args):
            draw_cart(int(self.style_var.get()), self.chart_canvas, self.graph_value0, int(self.which_var.get()), 1, 0)
            draw_cart(int(self.style_var1.get()), self.chart2_canvas, self.graph_value0, int(self.which_var.get()), 2, 0)
            self.display_products(self.graph_value0)

        # self.total_doc_ITEM_counted = tk.Label(self.home_tab, text="TOTAL DOC : 0 ITEMS : 0 COUNTED", font=("Arial", 11))
        # self.total_doc_ITEM_counted.grid(row=5, column=0)
        
        # New listbox in the main frame
        self.list_items = tk.Listbox(self.home_tab)
        self.list_items.grid(row=5, column=0, rowspan=7, columnspan=1, sticky=tk.N)

        # Summary labels
        # Column 2 Counteing
        # self.doc_payedtotal_counted = tk.Label(self.home_tab, text="Items Counted : ", font=("Arial", 11))
        # self.doc_payedtotal_counted.grid(row=6, column=2)

        # Column 2 CashIn 
        
        self.Total_Cash_paid_doc = tk.Label(self.home_tab, text="Cash pid :", font=("Arial", 11))
        self.Total_Cash_paid_doc.grid(row=6, column=1)

        self.Total_Card_paid_doc = tk.Label(self.home_tab, text="Card pid :", font=("Arial", 11))
        self.Total_Card_paid_doc.grid(row=7, column=1)

        self.Total_Card_IN_doc = tk.Label(self.home_tab, text="Card pid : 0.00", font=("Arial", 11))
        self.Total_Card_IN_doc.grid(row=8, column=1)

        self.Total_paid_doc = tk.Label(self.home_tab, text="Total pid:", font=("Arial", 11))
        self.Total_paid_doc.grid(row=10, column=1)

        # Column 4 CashOut
        self.Total_Cash_Outs_doc = tk.Label(self.home_tab, text="Cash Outs: 0.00", font=("Arial", 11))
        self.Total_Cash_Outs_doc.grid(row=6, column=2)

        self.Total_Card_Outs_doc = tk.Label(self.home_tab, text="Card Outs : 0.00", font=("Arial", 11))
        self.Total_Card_Outs_doc.grid(row=7, column=2)
        # ensure accumulator exists (do not reset each shop iteration)
        if not hasattr(self, '_accumulated_expenses'):
            self._accumulated_expenses = 0.0

        for shop in self.shop:
            # if self.Selected_Shop and shop.get('Shop_name') != self.Selected_Shop:
            #    continue
            if not shop:
                continue
            self._accumulated_expenses = 0.0
            print("Processing shop:", shop.get('Shop_name', 'Unknown'))
            shop_exp = []
            if shop.get('Shop_Expenses'):
                print("Shop Expenses data:", str(shop.get('Shop_Expenses')))
                try:
                    shop_exp = json.loads(shop.get('Shop_Expenses'))
                except Exception:
                    shop_exp = []

            # compute shop expenses falling inside current date range (prorated per-day for monthly/yearly/etc.)
            def _parse_date(s):
                if not s:
                    return None
                s = str(s).strip()
                s0 = s.split(" ")[0].split("_")[0]
                parts = re.findall(r'\d+', s0)
                # Accept YYYY-MM-DD or DD-MM-YYYY (3 parts)
                if len(parts) >= 3:
                    try:
                        if len(parts[0]) == 4:
                            y, m, d = parts[0], parts[1], parts[2]
                        else:
                            d, m, y = parts[0], parts[1], parts[2]
                        return datetime.date(int(y), int(m), int(d))
                    except Exception:
                        return None
                # Accept Year-Month or Month-Year (2 parts) -> treat as first day of month
                if len(parts) == 2:
                    try:
                        # detect which part is year (4 digits) else guess
                        if len(parts[0]) == 4:
                            y, m = parts[0], parts[1]
                        elif len(parts[1]) == 4:
                            m, y = parts[0], parts[1]
                        else:
                            # fallback: if first part > 31 assume it's year
                            if int(parts[0]) > 31:
                                y, m = parts[0], parts[1]
                            else:
                                m, y = parts[0], parts[1]
                        return datetime.date(int(y), int(m), 1)
                    except Exception:
                        return None
                # single token that looks like a year or unknown -> fail
                return None

            def _to_float(x):
                try:
                    if x is None:
                        return 0.0
                    s = str(x)
                    s = re.sub(r'[^\d\.\-]', '', s)
                    return float(s) if s != '' else 0.0
                except Exception:
                    return 0.0

            def _add_months(d, months):
                y = d.year + (d.month - 1 + months) // 12
                m = (d.month - 1 + months) % 12 + 1
                day = min(d.day, [31,
                                  29 if (y % 4 == 0 and (y % 100 != 0 or y % 400 == 0)) else 28,
                                  31, 30, 31, 30, 31, 31, 30, 31, 30, 31][m - 1])
                return datetime.date(y, m, day)

            def _add_years(d, years):
                try:
                    return datetime.date(d.year + years, d.month, d.day)
                except Exception:
                    return datetime.date(d.year + years, d.month, 28)

            def _period_end_for(current_start, freq, interval):
                # returns the end date (inclusive) of the period that starts at current_start
                if 'day' in freq:
                    return current_start + datetime.timedelta(days=interval - 1)
                if 'week' in freq:
                    return current_start + datetime.timedelta(days=7 * interval - 1)
                if 'month' in freq:
                    next_start = _add_months(current_start, interval)
                    return next_start - datetime.timedelta(days=1)
                if 'year' in freq:
                    next_start = _add_years(current_start, interval)
                    return next_start - datetime.timedelta(days=1)
                # unknown freq treated as single-day occurrence
                return current_start

            shop_daily_total = 0.0
            exp = None
            # shop_exp is a list of expense records: [name, desc, amount, category, start_date, resp, notes, freq_combo, isrepeats, interval, end_date]
            for i_exp, exp in enumerate(shop_exp):
                try:
                    print(f"[SHOP:{shop.get('Shop_name','?')}] Expense #{i_exp} raw: {repr(exp)}")
                    amount = _to_float(exp[2]) if len(exp) > 2 else 0.0
                    start_date = _parse_date(exp[4]) if len(exp) > 4 else None
                    freq = str(exp[7]).lower() if len(exp) > 7 and exp[7] is not None else ""
                    is_repeat = exp[8] if len(exp) > 8 else False
                    interval = int(exp[9]) if len(exp) > 9 and str(exp[9]).isdigit() else 1
                    end_date = _parse_date(exp[10]) if len(exp) > 10 else None

                    print(f"  parsed -> amount: {amount}, start_date: {start_date}, freq: '{freq}', is_repeat: {is_repeat}, interval: {interval}, end_date: {end_date}")

                    # parse user range; if parsing fails, use open-ended range so expenses without explicit end_date are still considered
                    try:
                        range_start = _parse_date(self.date_from_Entry.get())
                        range_end = _parse_date(self.date_to_Entry.get())
                    except Exception as e:
                        print("  error parsing user date range:", e)
                        range_start = None
                        range_end = None

                    # If the user didn't provide a start or end date, treat the range as open-ended:
                    # missing start -> very early date, missing end -> far future date.
                    if range_start is None:
                        range_start = datetime.date.min
                    if range_end is None:
                        range_end = datetime.date.max

                    # expense must have a valid start_date to be processed
                    if start_date is None:
                        print("  skipping expense: missing expense start_date ->", start_date)
                        continue

                    # overall active window for expense
                    # if expense has no explicit end_date treat it as unbounded -> we'll clamp to user's range_end
                    active_start = max(start_date, range_start)
                    active_end = range_end if end_date is None else min(end_date, range_end)
                    print(f"  active window: {active_start} .. {active_end}")
                    if active_start > active_end:
                        print("  no overlap between expense active window and user range; skipping")
                        continue

                    # determine boolean repeat flag robustly:
                    is_repeat_flag = False
                    try:
                        srep = str(is_repeat).strip().lower()
                        if srep in ("1", "true", "yes"):
                            is_repeat_flag = True
                        elif srep in ("0", "false", "no", ""):
                            is_repeat_flag = False
                        else:
                            # if explicit repeat not set but freq clearly indicates repeating and no end date given,
                            # assume it should repeat
                            if any(k in freq for k in ("day", "week", "month", "year")) and end_date is None:
                                is_repeat_flag = True
                    except Exception:
                        if any(k in freq for k in ("day", "week", "month", "year")) and end_date is None:
                            is_repeat_flag = True
                    print(f"  is_repeat_flag evaluated to: {is_repeat_flag}")

                    # Non-repeating: treat as a single occurrence on start_date (count if it falls into user's range)
                    if not is_repeat_flag:
                        # If start_date falls inside user's range, count it once.
                        if start_date >= range_start and start_date <= range_end:
                            shop_daily_total += amount
                            print(f"  non-repeating expense counted full amount: {amount}")
                        else:
                            print("  non-repeating expense start_date outside range; not counted")
                        print(f"[SHOP:{shop.get('Shop_name','?')}] shop_daily_total after non-repeating expense: {shop_daily_total}")
                        continue

                    # Repeating: iterate occurrences and prorate per overlap days
                    occurrence = start_date
                    print(f"  repeating expense. starting iterations from: {occurrence}")
                    # fast-forward occurrence to first occurrence that could overlap active_start
                    if 'day' in freq:
                        step = datetime.timedelta(days=interval)
                        if occurrence < active_start:
                            diff = (active_start - occurrence).days
                            skips = diff // interval
                            print(f"    fast-forward days: skip {skips} intervals")
                            occurrence = occurrence + step * skips
                            while occurrence + step - datetime.timedelta(days=1) < active_start:
                                occurrence += step
                                print(f"      bump occurrence -> {occurrence}")
                    elif 'week' in freq:
                        step = datetime.timedelta(weeks=interval)
                        if occurrence < active_start:
                            diff = (active_start - occurrence).days
                            skips = diff // (7 * interval)
                            print(f"    fast-forward weeks: skip {skips} intervals")
                            occurrence = occurrence + step * skips
                            while occurrence + step - datetime.timedelta(days=1) < active_start:
                                occurrence += step
                                print(f"      bump occurrence -> {occurrence}")
                    elif 'month' in freq:
                        if occurrence < active_start:
                            # step forward by whole intervals until the period that can overlap active_start is reached
                            # use iterative bumping to avoid overshooting the previous period that still overlaps active_start
                            while _add_months(occurrence, interval) - datetime.timedelta(days=1) < active_start:
                                occurrence = _add_months(occurrence, interval)
                                print(f"    bump occurrence -> {occurrence}")
                    elif 'year' in freq:
                        if occurrence < active_start:
                            # similar safe loop for yearly intervals
                            while _add_years(occurrence, interval) - datetime.timedelta(days=1) < active_start:
                                occurrence = _add_years(occurrence, interval)
                                print(f"    bump occurrence -> {occurrence}")
                    else:
                        # unknown freq -> if start_date in range, count once
                        if start_date >= active_start and start_date <= active_end:
                            shop_daily_total += amount
                            print(f"    unknown freq counted once: {amount}")
                        else:
                            print("    unknown freq and out of range; not counted")
                        continue

                    # walk occurrences until beyond active_end
                    occ_index = 0
                    print(f"  iterating occurrences from {occurrence} to {active_end}")
                    while occurrence <= active_end:
                        occ_index += 1
                        period_start = occurrence
                        period_end = _period_end_for(period_start, freq, interval)
                        # clamp to overall active window
                        overlap_start = max(period_start, active_start)
                        overlap_end = min(period_end, active_end)
                        print(f"    occurrence #{occ_index}: period {period_start}..{period_end}, overlap {overlap_start}..{overlap_end}")
                        if overlap_start <= overlap_end:
                            days_in_period = (period_end - period_start).days + 1
                            overlap_days = (overlap_end - overlap_start).days + 1
                            if days_in_period <= 0:
                                # safety fallback
                                add_amt = amount * (overlap_days / 1.0)
                                shop_daily_total += add_amt
                                print(f"      safety add {add_amt} (overlap_days {overlap_days})")
                            else:
                                add_amt = amount * (overlap_days / float(days_in_period))
                                shop_daily_total += add_amt
                                print(f"      prorated add {add_amt} (overlap_days {overlap_days} / days_in_period {days_in_period})")
                        else:
                            print("      no overlap for this occurrence")
                        # advance to next occurrence
                        if 'day' in freq:
                            occurrence = occurrence + datetime.timedelta(days=interval)
                        elif 'week' in freq:
                            occurrence = occurrence + datetime.timedelta(weeks=interval)
                        elif 'month' in freq:
                            occurrence = _add_months(occurrence, interval)
                        elif 'year' in freq:
                            occurrence = _add_years(occurrence, interval)
                        else:
                            break
                    print(f"[SHOP:{shop.get('Shop_name','?')}] shop_daily_total after repeating expense: {shop_daily_total}")
                except Exception as e:
                    print(f"  exception processing expense #{i_exp}: {e}")
                    continue

            def _fix_two_digit_year(raw_str, parsed_date):
                if not parsed_date or not raw_str:
                    return parsed_date
                try:
                    tok = str(raw_str).strip().split(" ")[0].split("_")[0]
                    parts = re.findall(r'\d+', tok)
                    if len(parts) >= 3:
                        # parts assumed [day, month, year] or [year, month, day]; detect which by value sizes
                        # prefer the branch that produced parsed_date already; if the last token has 2 digits, treat as two-digit year
                        ytoken = parts[2]
                        if len(ytoken) == 2:
                            yy = int(ytoken)
                            cutoff = datetime.date.today().year % 100
                            if yy <= cutoff:
                                year = 2000 + yy
                            else:
                                year = 1900 + yy
                            # determine day/month ordering used by _parse_date: parsed_date gives us month/day we can reuse
                            # Here assume parts[0]=day, parts[1]=month (most common "DD-MM-YY")
                            d = int(parts[0])
                            m = int(parts[1])
                            return datetime.date(year, m, d)
                except Exception:
                    pass
                return parsed_date
            if not exp or not isinstance(exp, (list, tuple)):
                print(f"  skipping invalid expense format: {repr(exp)}")
                continue

            # apply fixes to both start_date and end_date where appropriate
            start_date = _fix_two_digit_year(exp[4] if len(exp) > 4 else None, start_date)
            end_date = _fix_two_digit_year(exp[10] if len(exp) > 10 else None, end_date)
            print(f"[SHOP:{shop.get('Shop_name','?')}] shop_daily_total after processing expenses: {shop_daily_total}")

            # accumulate across shops so final label (updated each iteration) ends up with total of all shops processed
            self._accumulated_expenses += shop_daily_total

            # display current accumulated total (will end up as the full total after the loop finishes)
            print(self._accumulated_expenses)
            txt = "Expenses : -" + str(round(self._accumulated_expenses, 2))
            self.Total_Expense_doc = tk.Label(self.home_tab, text=txt, font=("Arial", 11))
            self.Total_Expense_doc.grid(row=8, column=3)

        self.Total_Out_doc = tk.Label(self.home_tab, text="Total Out:", font=("Arial", 11))
        self.Total_Out_doc.grid(row=10, column=2)


        self.doc_totalprofit_ = tk.Label(self.home_tab, text="Totale Profit :", font=("Arial", 11))
        self.doc_totalprofit_.grid(row=6, column=3)
        self.doc_totalprofit_afterout = tk.Label(self.home_tab, text="Totale Profit After Outs :", font=("Arial", 11))
        self.doc_totalprofit_afterout.grid(row=7, column=3)
        self.doc_total_afterout = tk.Label(self.home_tab, text="Totale Pid After Outs :", font=("Arial", 11))
        self.doc_total_afterout.grid(row=8, column=3)

        # Column 5 Stock
        self.Total_Cash_Stock_doc = tk.Label(self.home_tab, text="Cash Stock:", font=("Arial", 11))
        self.Total_Cash_Stock_doc.grid(row=6, column=4)

        self.Total_Card_Stock_doc = tk.Label(self.home_tab, text="Card Stock:", font=("Arial", 11))
        self.Total_Card_Stock_doc.grid(row=7, column=4)

        self.Total_Credit_Stock_doc = tk.Label(self.home_tab, text="Credit Stock:", font=("Arial", 11))
        self.Total_Credit_Stock_doc.grid(row=8, column=4)

        self.Total_Stock_doc = tk.Label(self.home_tab, text="Total Stock:", font=("Arial", 11))
        self.Total_Stock_doc.grid(row=10, column=4)

        self.Total_Unpaid_doc = tk.Label(self.home_tab, text="Amount Unpaid:", font=("Arial", 11))
        self.Total_Unpaid_doc.grid(row=10, column=5)
        self.doc_total_ = tk.Label(self.home_tab, text="Totale :", font=("Arial", 15))
        self.doc_total_.grid(row=10, column=5)
        self.doc_gtotal_ = tk.Label(self.home_tab, text="GRAND Totale :", font=("Arial", 15))
        self.doc_gtotal_.grid(row=10, column=5)

        self.doc_endday_btn = tk.Button(self.home_tab, text="End Day", font=("Arial", 12), command=self.perform_endday)
        self.doc_endday_btn.grid(row=9, column=5, sticky="nsew")        
        
        
        self.product_list = tk.Listbox(self.home_tab, width=30)
        self.product_list.grid(row=5, column=6, rowspan=7, columnspan=1, sticky=tk.N)
        

        self.chart_canvas = tk.Canvas(self.home_tab)
        self.chart_canvas.grid(row=13, column=0, columnspan=3, rowspan=3)
        
        self.chart2_canvas = tk.Canvas(self.home_tab)
        self.chart2_canvas.grid(row=13, column=3, columnspan=2, rowspan=3)

        
        self.which_var = tk.StringVar()
        self.which_var.set("1")
        self.which_var.trace("w", on_style_selected)
        self.which_dropdown = tk.OptionMenu(self.home_tab, self.which_var, "0", "1", "2", "3")
        self.which_dropdown.grid(row=16, column=0, sticky="nsew")
        
        self.style_var = tk.StringVar()
        self.style_var.set("1")
        self.style_var.trace("w", on_style_selected)
        self.style_dropdown = tk.OptionMenu(self.home_tab, self.style_var, "1", "2", "3", "4")
        self.style_dropdown.grid(row=16, column=1, sticky="nsew")
        
        self.next_button = tk.Button(self.home_tab, text="<", font=("Arial", 12))
        self.next_button.grid(row=16, column=2, sticky="nsew")
        self.prev_button = tk.Button(self.home_tab, text=">", font=("Arial", 12))
        self.prev_button.grid(row=16, column=3, sticky="nsew")
        
        
        self.style_var1 = tk.StringVar()
        self.style_var1.set("2")
        self.style_var1.trace("w", on_style_selected)
        self.style_dropdown1 = tk.OptionMenu(self.home_tab, self.style_var1, "1", "2", "3", "4")
        self.style_dropdown1.grid(row=16, column=4, sticky="nsew")
        
        self.next_button1 = tk.Button(self.home_tab, text="<", font=("Arial", 12))
        self.next_button1.grid(row=16, column=5, sticky="nsew")
        self.prev_button1 = tk.Button(self.home_tab, text=">", font=("Arial", 12))
        self.prev_button1.grid(row=16, column=6, sticky="nsew")
        
        if len(vv) > 0:
            self.graph_value, self.graph_value0, tilte = make_list(vv)
            #print("self.graph_value0 :" + str(self.graph_value0))
            draw_cart(self.chart_canvas, self.graph_value0, int(self.which_var.get()), 1)
            draw_cart(self.chart2_canvas, self.graph_value0, int(self.which_var.get()), 2)
            self.display_products(self.graph_value0, int(self.which_var.get()))
            #print(" v : " + str(vv))

        self.list_items.delete(0, tk.END)
        pid = 0

        unpid = 0
        # cashout = 0
        # cardout = 0
        total = 0 
        Gtotal = 0
        Payment_methods = {'CASH': 0.0, 'CARD': 0.0, 'CREADIT': 0.0, 'CREDITSTOCK': 0.0, 'CASHSTOCK': 0.0, 'CARDSTOCK': 0.0, 'UNPAID': 0.0, 'CARDOUT': 0.0, 'CASHOUT': 0.0, 'CASHIN': 0.0, 'OTHER': 0.0}
        # Payment_methods [CASH, CARD, CREADIT, UNPAID, CASHOUT, CASHIN, CREDITSTOCK, Cash Stock, Card Stock, OTHER]
        for pay in self.pyment_used:
            # pay expected: [pay_type, amount, ispay_pide, payment_method]
            try:
                pay_type = pay[0]
            except Exception:
                pay_type = ""
            try:
                amount = float(pay[1])
            except Exception:
                amount = 0.0
            try:
                ispay_flag = float(pay[2])
            except Exception:
                # fallback: treat as paid
                ispay_flag = 1.0
            try:
                method = str(pay[3]) if len(pay) > 3 and pay[3] is not None else ""
            except Exception:
                method = ""

            # determine method key (normalize)
            m = method.upper()
            key = 'OTHER'
            if ispay_flag == 0 or 'UNPAID' in m:
                key = 'UNPAID'
                unpid += amount
                self.list_items.insert(tk.END, [pay_type, amount, method])
            
            elif 'CREDITSTOCK' in m:
                key = 'CREDITSTOCK'
                total += amount
                Gtotal += amount

            elif 'CASHSTOCK' in m:
                key = 'CASHSTOCK'
                total += amount
                Gtotal += amount

            elif 'CARDSTOCK' in m:
                key = 'CARDSTOCK'
                total += amount
                Gtotal += amount
            
            elif ispay_flag < 0 or 'CASHOUT' in m:
                key = 'CASHOUT' # replaced for cashout += amount
                total -= amount
                self.list_items.insert(tk.END, [pay_type, amount, method])
            
            elif ispay_flag < 0 or 'CARDOUT' in m:
                key = 'CARDOUT' # replaced for cardout -= amount
                total -= amount
                self.list_items.insert(tk.END, [pay_type, amount, method])

            elif ('CASH' in m and 'CASHOUT' not in m) or 'CASH' in pay_type.upper():
                key = 'CASH'
                pid += amount
                total += amount
                Gtotal += amount
                self.list_items.insert(tk.END, [pay_type, amount, method])

            elif ('CARD' in m or 'VISA' in m or 'MASTERCARD' in m) or 'CARD' in pay_type.upper():
                key = 'CARD'
                pid += amount
                total += amount
                Gtotal += amount
                self.list_items.insert(tk.END, [pay_type, amount, method])

            elif 'CREDIT' in m or 'CREADIT' in m:
                key = 'CREADIT'
                total += amount
                Gtotal += amount
                self.list_items.insert(tk.END, [pay_type, amount, method])

            elif 'CASHIN' in m:
                key = 'CASHIN'
                pid += amount
                total += amount
                Gtotal += amount
                self.list_items.insert(tk.END, [pay_type, amount, method])

            else:
                # default/fallback: consider as paid
                key = 'OTHER'
                total += amount
                Gtotal += amount
                self.list_items.insert(tk.END, [m, amount, method])

            Payment_methods.setdefault(key, 0.0)
            Payment_methods[key] += amount

        # Update summary labels (rounded)
        self.total_info.config(text="TOTAL DOC : " + str(count_doc) + "\nITEMS : " + str(count_items) + " COUNTED\nGrand Total : " + str(format(round(Gtotal, 2), ".2f")))
        self.Total_Cash_paid_doc.config(text="Cash paid : " + str(format(round(Payment_methods.get('CASH', 0.0), 2), ".2f")))
        self.Total_Card_paid_doc.config(text="Card paid : " + str(format(round(Payment_methods.get('CARD', 0.0), 2), ".2f")))
        self.Total_paid_doc.config(text="Total Paid : " + str(format(round(pid, 2), ".2f")))

        if round(Payment_methods.get('CASHOUT', 0.0), 2) != 0:
            self.Total_Cash_Outs_doc.config(text="Cash Outs: " + str(format(round(Payment_methods.get('CASHOUT', 0.0), 2), ".2f")), bg="red")
        
        if round(Payment_methods.get('CARDOUT', 0.0), 2) != 0:
            self.Total_Card_Outs_doc.config(text="Card Outs : " + str(format(round(Payment_methods.get('CARDOUT', 0.0), 2), ".2f")), bg="red")
            
        TOTALOUT = round(Payment_methods.get('CASHOUT', 0.0), 2) + round(Payment_methods.get('CARDOUT', 0.0), 2) + self._accumulated_expenses
        if TOTALOUT != 0:
            self.Total_Out_doc.config(text="Total Out : " + str(format(TOTALOUT, ".2f")), bg="red")
        
        self.doc_totalprofit_.config(text="Total Profit : " + str(format(round(itemsProfit, 2), ".2f")))
        
        if round(itemsProfit, 2)-TOTALOUT < 0:
            self.doc_totalprofit_afterout.config(text="Total Profit After Outs : " + str(format(round(itemsProfit, 2)-TOTALOUT, ".2f")), bg="red")
        else:
            self.doc_totalprofit_afterout.config(text="Total Profit After Outs : " + str(format(round(itemsProfit, 2)-TOTALOUT, ".2f")))
        self.doc_total_afterout.config(text="Total After Outs : " + str(format(round(pid, 2)-TOTALOUT, ".2f")))

        self.doc_total_.config(text="Total : " + str(format(round(total, 2), ".2f")))
        

        self.Total_Cash_Stock_doc.config(text="Cash Stock: " + str(format(round(Payment_methods.get('CASHSTOCK', 0.0), 2), ".2f")))
        self.Total_Card_Stock_doc.config(text="Card Stock : " + str(format(round(Payment_methods.get('CARDSTOCK', 0.0), 2), ".2f")))
        self.Total_Credit_Stock_doc.config(text="Credit Sock : " + str(format(round(Payment_methods.get('CREDITSTOCK', 0.0), 2), ".2f")))
 
        self.Total_Stock_doc.config(text="Total Sock : " + str(format(round(Payment_methods.get('CASHSTOCK', 0.0), 2) + round(Payment_methods.get('CARDSTOCK', 0.0), 2) + round(Payment_methods.get('CREDITSTOCK', 0.0), 2), ".2f")))

        
        
        # self.Total_Card_Outs_doc.config(text="Card Outs : " + str(round(Payment_methods.get('CREADIT', cardout), 2)))
        self.Total_Unpaid_doc.config(text="Amount UnPaid : " + str(format(round(Payment_methods.get('UNPAID', unpid), 2), ".2f")))
        self.doc_gtotal_.config(text="GRAND Totale : " + str(format(round(Gtotal, 2), ".2f")))

        #tk.Label(self.info_tab, text=" :"+str(pay[1])).pack()
      
    def perform_endday(self):
        # Implement end day logic here
        # create top level window for end day confirmation
        top = tk.Toplevel(self.master, bg="white")
        top.title("End Day Confirmation")
        top.geometry("500x300")  # Set a fixed size for the window
        top.resizable(False, False)  # Prevent resizing
        
        # Create a frame for better layout
        frame = tk.Frame(top, bg="white")
        frame.pack(padx=20, pady=20)


        # Show summary of today's totals for confirmation
        tk.Label(frame, text="", bg="white", font=("Arial", 14, "bold")).pack(pady=10)
        tk.Label(frame, text='Cash        :        ' + self.Total_Cash_paid_doc.cget("text").split(": ")[1], bg="white", font=("Arial", 12)).pack(pady=5)
        tk.Label(frame, text='Card        :        ' + self.Total_Card_paid_doc.cget("text").split(": ")[1], bg="white", font=("Arial", 12)).pack(pady=5)
        tk.Label(frame, text="             ----------------", bg="white", font=("Arial", 14)).pack(pady=5)
        tk.Label(frame, text='            :        ' + str(float(self.Total_paid_doc.cget("text").split(": ")[1])), bg="white", font=("Arial", 16)).pack(pady=5)
        tk.Label(frame, text='Cash Outs   :        ' + str(float(self.Total_Cash_Outs_doc.cget("text").split(": ")[1]) + float(self.Total_Card_Outs_doc.cget("text").split(": ")[1])), bg="white", fg="red", font=("Arial", 12, "bold")).pack(pady=5)
        tk.Label(frame, text='Total       :        ' + str(float(self.Total_paid_doc.cget("text").split(": ")[1]) - float(self.Total_Cash_Outs_doc.cget("text").split(": ")[1]) - float(self.Total_Card_Outs_doc.cget("text").split(": ")[1])), bg="white", font=("Arial", 16)).pack(pady=5)
        tk.Label(frame, text="Total Profit: " + self.doc_totalprofit_.cget("text"), bg="white", font=("Arial", 10)).pack(pady=5)
    
    def load_payment(self, p_text, from_d, to_d):
        try:
            load_payment = json.loads(p_text)
        except Exception as e:
            print("Error occurred while loading payment data:", str(e))
            return  # Stop loading if there's an error
        print("load_payment : ", load_payment)
        index = 0
        new_payement_made = []
        for p, item in enumerate(load_payment):
            print("item ;" + str(item))
            #for each items+
            payment_method = ""
            pay_id = item[0]
            pay_type = item[1]
            pay_pid = item[2]
            pay_pid_date = item[3]
            pay_updated_date = item[4]
            pay_user = item[5]
            ispay_pide = item[6]
            if len(item) > 8:
                payment_method = item[8]
            else:
                Shop_Payment_Tools = []
                for Shop in self.master.master.master.master.Shops:
                    if Shop and Shop['Shop_Payment_Tools'] and Shop['Shop_Payment_Tools'] != "":
                        Shop_Payment_Toolscp = json.loads(Shop['Shop_Payment_Tools'])
                        for Shop_Payment_Tool in Shop_Payment_Toolscp:
                            Shop_Payment_Tools.append(Shop_Payment_Tool)
                print("searching payment method for type :" + str(Shop_Payment_Tools))
                for r in Shop_Payment_Tools:
                    print("checking payment method for type :", r)
                    if r[0] == pay_type:
                        print("matching payment method for type :" + pay_type)
                        if r:
                            print("found payment method :" + str(r))
                            payment_method = r[1]
                        else:
                            payment_method = "OTHER"
                            print("not found payment method for type : other")
                        break
            print("pay_pid " + str(pay_pid))
            #print("date : " + str(pay_pid_date))
            #print("udate : " + str(pay_updated_date))
            splitedate = pay_pid_date.split(" ")[0].split("-")
            fd = from_d.split("-")
            td = to_d.split("-")
            day = ""
            print("splitedate[2]" + splitedate[2])
            if len(splitedate[2]) > 2:
                for q, v in enumerate(splitedate[2]):
                    if q == 2:
                        break
                    day += v
            else:
                day = splitedate[2]
            print("day " + day)
            start_d = datetime.datetime(int(''.join([d for d in str(fd[0]) if d.isdigit()])), int(''.join([d for d in str(fd[1]) if d.isdigit()])), int(''.join([d for d in str(fd[2]) if d.isdigit()])))
            end_d = datetime.datetime(int(''.join([d for d in str(td[0]) if d.isdigit()])), int(''.join([d for d in str(td[1]) if d.isdigit()])), int(''.join([d for d in str(td[2]) if d.isdigit()])))
            chacke_d = datetime.datetime(int(''.join([d for d in str(splitedate[0]) if d.isdigit()])), int(''.join([d for d in str(splitedate[1]) if d.isdigit()])), int(''.join([d for d in str(day) if d.isdigit()])))
            price = item[1]
            found = 0
            print("pay_pid " + str(pay_pid))
            if start_d <= chacke_d <= end_d:
                for pay in self.pyment_used:
                    if pay[0] == pay_type and pay[2] == ispay_pide:
                        found = 1
                        pay[1] += float(pay_pid)
                        break
                if found == 0:
                    print("new payment :" + str([pay_type, pay_pid, ispay_pide]))
                    self.pyment_used.append([pay_type, float(pay_pid), ispay_pide, payment_method])
                new_found = 0
                for pay in new_payement_made:
                    if pay[0] == pay_type and pay[2] == ispay_pide:
                        new_found = 1
                        pay[1] += float(pay_pid)
                        break
                if new_found == 0:
                    new_payement_made.append([pay_type, float(pay_pid), ispay_pide, payment_method])
                index += 1
        return index, new_payement_made
        
    def close_tab(self, t_id):
        self.center_notebook.forget(t_id)
        

    def on_select(self, event):
        pass
    
    def display_products(self, products, ind):
            self.product_list.delete(0, tk.END)
            if products:
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
        #print("in dubleclicked")
        item_text = self.listbox.item(item, "values")  # Get the text values of the item
        id = self.listbox.item(item, "text")

        if item:
        # Detect double-click
            print("Double-clicked item:", item_text)

            # Add tabs to the self.center_notebook
            if item_text[0]:
                tab_exist = any(self.center_notebook.tab(tab_id, "text") == item_text[0] for tab_id in self.center_notebook.tabs())
                if not tab_exist:
                    MAIN_test_tab = ttk.Frame(self.center_notebook)
                    self.center_notebook.add(MAIN_test_tab, text=item_text[0])
                    test_tab = tk.Frame(MAIN_test_tab)
                    test_tab.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
                    # Create a close button and position it at the top next to the tab title
                    close_button1 = tk.Button(test_tab, text="X", command=lambda : self.close_tab(MAIN_test_tab))
                    close_button1.pack(side="top", anchor="ne", padx=5, pady=2)
                    doc_edit_form = DocEditForm(test_tab, self.master.master.master.master.Shops_info, self.user_info, self.master.master.master.master.Shops, item_text, item_text[0])
                    doc_edit_form.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
                else:
                    for a in self.center_notebook.tabs():
                        print("Tab already exists!")
                        print(str(self.center_notebook.tab(a, "text")))

    def close_tab(self, t_id):
        self.center_notebook.forget(t_id)
        

    def on_select(self, event):
        pass
    
    def perform_delet(self):
        item = self.listbox.focus()  # Get the item that was clicked
        if item:
            item_text = self.listbox.item(item, "values")  # Get the text values of the item
            id = self.listbox.item(item, "text")
            barcode = item_text[0]
            answer = tk.messagebox.askquestion("Question", "Do you what to delete "+str(barcode)+" ?")
            if answer == 'yes':
                # Delete the product from the database
                Update_table_database('DELETE FROM doc_table WHERE doc_barcode=?', (barcode,))
                
    def perform_print(self):
        item = self.listbox.focus()  # Get the item that was clicked
        if item:
            item_text = self.listbox.item(item, "values")  # Get the text values of the item
            doc_id = self.listbox.item(item, "text")
            barcode = item_text[0]
            doc_ = fetch_as_dict_list("SELECT * FROM doc_table WHERE doc_barcode=?", (barcode,))[0]
            if doc_:
                answer = tk.messagebox.askquestion("Question", "Do you what to print "+str(barcode)+" ?")
                if answer == 'yes':
                    #print(str(doc_))
                    doc_edit_form = load_slip(doc_, doc_id)
                    print("don loding slip : \n\n" + str(doc_edit_form))
                    self.user = self.master.master.master.master.user
                    # TODO: Make It send selected shop to print_slip
                    PrinterForm.print_slip(self, self.user_info, self.shop[0], doc_edit_form, 1) # TODO chack in setting if paper cut allowed

    # Function to perform the search and display the results in the listbox
    def perform_search(self):
        # Ensure any leftover direct attributes are removed
        for name in ('listdocs_tab', 'home_tab', 'T_tab', 'Report_tab'):
            if hasattr(self, name):
                try:
                    getattr(self, name).destroy()
                except Exception:
                    pass
                try:
                    delattr(self, name)
                except Exception:
                    pass
        

        self.listdocs_tab = ttk.Frame(self.Doc_tab)
        self.listdocs_tab.grid(row=5, column=0, columnspan=7, rowspan=5, sticky="nsew")
        
        # Add tabs to the self.center_notebook
        self.info_notebook.add(self.listdocs_tab, text='List Docs')

        # Create the listbox to display search results
        self.listbox = ttk.Treeview(self.listdocs_tab)        
        self.listbox.bind('<<TreeviewSelect>>', self.on_select)
        self.listbox.bind("<Button-1>", self.on_treeview_double_click)
        #self.listbox.grid_propagate(False)


        # Add vertical scrollbar
        tree_scrollbar_y = ttk.Scrollbar(self.listdocs_tab, orient='vertical', command=self.listbox.yview)
        self.listbox.configure(yscrollcommand=tree_scrollbar_y.set)
        tree_scrollbar_y.pack(side='right', fill='y')

        # Add horizontal scrollbar
        tree_scrollbar_x = ttk.Scrollbar(self.listdocs_tab, orient='horizontal', command=self.listbox.xview)
        self.listbox.configure(xscrollcommand=tree_scrollbar_x.set)
        tree_scrollbar_x.pack(side='bottom', fill='x', )

        # Set the size of the self.listbox widget
        self.listbox.pack(side='top', fill='both', expand=True)
        self.get_columen()
        
        self.pyment_used = []
        # Get the search criteria from the entry boxes
        doc_id = self.doc_id_entry.get()
        doc_type = self.doc_type_entry.get()
        doc_barcode = self.doc_barcode_entry.get()
        extension_barcode = self.extension_barcode_entry.get()
        item = self.item_entry.get()
        sold_item_info = self.sold_item_info_entry.get()
        discount = self.discount_entry.get()
        user_id = self.user_id_entry.get()
        customer_id = self.customer_id_entry.get()
        seller_id = self.seller_id_entry.get()

        # Perform the search and update the listbox with the results
        newdoc = search_documents(doc_id, doc_type, doc_barcode, extension_barcode, item, user_id, customer_id,
                            sold_item_info, discount, seller_id, self.date_from_Entry.get(), self.date_to_Entry.get(), self.doc_created_date_var.get(), self.doc_expire_date_var.get(), self.doc_updated_date_var.get())
        self.listbox.delete(*self.listbox.get_children())
        self.Add_New_documents(newdoc)

    def Add_New_documents(self, newdocs):
        print(" newdocs : ", str(newdocs))
        # Ensure any leftover direct attributes are removed
        for name in ('home_tab', 'T_tab', 'Report_tab'):
            if hasattr(self, name):
                try:
                    getattr(self, name).destroy()
                except Exception:
                    pass
                try:
                    delattr(self, name)
                except Exception:
                    pass
        

        vv = []
        count = 0
        count_items = 0
        itemsProfit = 0
        collecte_minutes = []
        was_on_minute = 0
        collecte_hours = []
        was_on_hour = 0
        collecte_days = []
        was_on_day = 0
        collecte_months = []
        was_on_month = 0
        collecte_years = []
        was_on_year = 0
        collected_values = {}
        is_paid, new_payement_made = None, None
        
        for index in newdocs:
            
            ispayed = False
            try:
                is_paid, new_payement_made = self.load_payment(index['payments'], self.date_from_Entry.get(), self.date_to_Entry.get()) # LOAD PYMENT AND IT TOTAL
                items = json.loads(index['item'])
            except Exception as e:
                print("Error loading payment or items:", str(e))
                items = []
                new_payement_made = []
            print("New payment made: ", new_payement_made)
            if index['type'] == "Sale_item":
                for item in items:
                    itemProfit = 0
                    print("item for profit calcute : " + str(item))
                    if len(item) > 11:
                        # we will calcute the profit here will get the cost price from the pid
                        # item[8] = sale price
                        # item[12] = cost price
                        # item[7] = qty
                        print("item for profit item[8] : " + str(item[8]))
                        print("item for profit item[11] : " + str(item[11]))
                        print("item for profit item[7] : " + str(item[7]))
                        itemProfit += (float(item[8])-float(item[11]))* float(item[7])
                    else:
                        # this will calculate for older versuion without cost price in item list
                        # we will calcute the profit here will get the cost price from the pid
                        # item[8] = sale price
                        # item[0] = pid
                        # item[7] = qty
                        if not item[0] == "" or not item[0] == None or not str(item[0]) == "-1":
                            it = fetch_as_dict_list( "SELECT * FROM product WHERE id=?", (item[0],))
                            if it and len(item) > 8:
                                it = it[0]
                                print("item for profit item[8] : " + str(item[8]))
                                print("item for profit it['cost'] : " + str(it['cost']))
                                print("item for profit item[7] : " + str(item[7]))
                                itemProfit += (float(item[8])-float(it['cost']))* float(item[7])
                            else:
                                itemProfit += 0
                        else:
                            itemProfit += 0
                        while True:
                            continue
                    print("item for profit itemProfit : " + str(itemProfit))
                    itemsProfit += itemProfit
                    print("item for itemsProfit : " + str(itemsProfit))
                    count_items += len(items)
                    if ispayed:
                        count+=1
            #print("newdoc : " + str(index)
            #print("newdoc : " + str(index['doc_created_date']))
            raw = index.get('doc_created_date') if isinstance(index, dict) else None
            if not raw or str(raw).strip() == "":
                now = datetime.datetime.now()
                dateandtime = [now.strftime('%Y-%m-%d'), now.strftime('%H:%M:%S')]
            else:
                s = str(raw).strip()
                # try common separators first
                if " " in s:
                    parts = s.split(" ")
                elif "_" in s:
                    parts = s.split("_")
                else:
                    parts = [s]

                # normalize: find a date-like part and a time-like part
                if len(parts) >= 2:
                    date_part = parts[0].strip()
                    time_part = parts[1].strip()
                    # if parts swapped (time in first part), fix it
                    if ":" in date_part and not ("-" in date_part or "/" in date_part):
                        dateandtime = [datetime.datetime.now().strftime('%Y-%m-%d'), date_part]
                    else:
                        if date_part == "":
                            date_part = datetime.datetime.now().strftime('%Y-%m-%d')
                        if time_part == "":
                            time_part = "00:00:00"
                        dateandtime = [date_part, time_part]
                else:
                    token = parts[0].strip()
                    if ":" in token:
                        # token looks like a time only
                        dateandtime = [datetime.datetime.now().strftime('%Y-%m-%d'), token]
                    elif "-" in token or "/" in token:
                        # token looks like a date only
                        dateandtime = [token, "00:00:00"]
                    else:
                        # unknown format -> fallback to now
                        now = datetime.datetime.now()
                        dateandtime = [now.strftime('%Y-%m-%d'), now.strftime('%H:%M:%S')]

            Time = dateandtime[1] if len(dateandtime) > 1 and dateandtime[1] else "00:00:00"

            # MINUTE
            minute = Time.split(":")[1] if ":" in Time else Time.split("-")[1]
            existing_minutes = [h[0] for h in collecte_minutes]
            if was_on_minute == 0:
                was_on_minute = minute
                collecte_minutes.append([minute, new_payement_made])
            elif minute not in existing_minutes:
                collecte_minutes.append([minute, new_payement_made])
            else:
                idx = existing_minutes.index(minute)
                prev_payments = collecte_minutes[idx][1]
                for i, npu in enumerate(new_payement_made):
                    if npu[0] in [ppu[0] for ppu in prev_payments]:
                        npuidx = [ppu[0] for ppu in prev_payments].index(npu[0])
                        prev_payments[npuidx][1] += npu[1]
                    else:
                        prev_payments.append([npu[0], npu[1], npu[2]])
                collecte_minutes[idx][1] += prev_payments
            was_on_minute = minute
            
            # HOUR
            hour = Time.split(":")[0] if ":" in Time else Time.split("-")[0]
            existing_hours = [h[0] for h in collecte_hours]
            if was_on_hour == 0:
                was_on_hour = hour
                collecte_hours.append([hour, new_payement_made])
            elif hour not in existing_hours:
                collecte_hours.append([hour, new_payement_made])
            else:
                idx = existing_hours.index(hour)
                prev_payments = collecte_hours[idx][1]
                for i, npu in enumerate(new_payement_made):
                    if npu[0] in [ppu[0] for ppu in prev_payments]:
                        npuidx = [ppu[0] for ppu in prev_payments].index(npu[0])
                        prev_payments[npuidx][1] += npu[1]
                    else:
                        prev_payments.append([npu[0], npu[1], npu[2]])
                collecte_hours[idx][1] = prev_payments
            was_on_hour = hour
            
            # DAY
            Date = dateandtime[0].split("-")
            day = Date[2]
            existing_days = [d[0] for d in collecte_days]
            if was_on_day == 0:
                was_on_day = day
                collecte_days.append([day, new_payement_made])
            elif day not in existing_days:
                collecte_days.append([day, new_payement_made])
            else:
                idx = existing_days.index(day)
                prev_payments = collecte_days[idx][1]
                for i, npu in enumerate(new_payement_made):
                    if npu[0] in [ppu[0] for ppu in prev_payments]:
                        npuidx = [ppu[0] for ppu in prev_payments].index(npu[0])
                        prev_payments[npuidx][1] += npu[1]
                    else:
                        prev_payments.append([npu[0], npu[1], npu[2]])
                collecte_days[idx][1] = prev_payments
            was_on_day = day

            # MONTH
            month = Date[1]
            existing_months = [m[0] for m in collecte_months]
            if was_on_month == 0:
                was_on_month = month
                collecte_months.append([month, new_payement_made])
            elif month not in existing_months:
                collecte_months.append([month, new_payement_made])
            else:
                idx = existing_months.index(month)
                prev_payments = collecte_months[idx][1]
                for i, npu in enumerate(new_payement_made):
                    if npu[0] in [ppu[0] for ppu in prev_payments]:
                        npuidx = [ppu[0] for ppu in prev_payments].index(npu[0])
                        prev_payments[npuidx][1] += npu[1]
                    else:
                        prev_payments.append([npu[0], npu[1], npu[2]])
                collecte_months[idx][1] = prev_payments
            was_on_month = month

            # YEAR
            year = Date[0]
            existing_years = [y[0] for y in collecte_years]
            if was_on_year == 0:
                was_on_year = year
                collecte_years.append([year, new_payement_made])
            elif year not in existing_years:
                collecte_years.append([year, new_payement_made])
            else:
                idx = existing_years.index(year)
                prev_payments = collecte_years[idx][1]
                for i, npu in enumerate(new_payement_made):
                    if npu[0] in [ppu[0] for ppu in prev_payments]:
                        npuidx = [ppu[0] for ppu in prev_payments].index(npu[0])
                        prev_payments[npuidx][1] += npu[1]
                    else:
                        prev_payments.append([npu[0], npu[1], npu[2]])
                collecte_years[idx][1] = prev_payments
            was_on_year = year

            vv.append([year, month, day, hour, minute, float(index['price'])-float(index['discount'])])
            item = self.listbox.insert('', 'end', text=index['id'], values=(index['doc_barcode'], index['extension_barcode'], index['At_Shop_Id'], index['user_id'], index['Seller_id'], index['customer_id'], index['pid'], index['qty'], index['price'], index['discount'], index['tax'], index['doc_created_date'], index['doc_expire_date'], index['doc_updated_date'], index['item'],  index['payments']))
            id = self.listbox.item(item, "text")
            item_text = self.listbox.item(item, "values")

        collected_values = {
            'minutes': collecte_minutes,
            'hours': collecte_hours,
            'days': collecte_days,
            'months': collecte_months,
            'years': collecte_years
        }
        print("collected_values : " + str(collected_values))
        
        user_id = self.user_id_entry.get()
        self.creat_info(user_id, vv, collected_values, len(self.listbox.get_children()), count_items, count, itemsProfit)





        # Add tabs to the self.center_notebook
        
        self.T_tab = ttk.Frame(self.Doc_tab)
        self.T_tab.grid(row=8, column=0, columnspan=7, rowspan=3, sticky="nsew")
        
        self.TLs_items = tk.Listbox(self.T_tab, bg="yellow")
        self.TLs_items.grid(row=0, column=0, columnspan=5)
        self.TL_items = tk.Listbox(self.T_tab, bg="yellow")
        self.TL_items.grid(row=5, column=0, columnspan=5)

        self.info_notebook.add(self.T_tab, text='IN')

        results = []#fetch_as_dict_list("SELECT * FROM COUNT_SELL WHERE strftime('%Y-%m-%d', DATE) BETWEEN ? AND ?", (f'{self.date_from_Entry.get()}', f'{self.date_to_Entry.get()}',))
        
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
        #self.get_columen()

        self.Report_tab = ttk.Frame(self.Doc_tab)
        self.Report_tab.grid(row=8, column=0, columnspan=7, rowspan=3, sticky="nsew")
        
        # Add tabs to the self.center_notebook
        self.info_notebook.add(self.Report_tab, text='Report')

        self.TLs_items.delete(0, tk.END)
        self.TL_items.delete(0, tk.END)

    def load_documents(self, doc_barcodes):
        docs = self.get_documents(doc_barcodes)
        self.Add_New_documents(docs)
    
    def get_documents(self, doc_barcodes):
        docs = []
        for doc_barcode in doc_barcodes:
            doc = fetch_as_dict_list( "SELECT * FROM doc_table WHERE doc_barcode=?", (doc_barcode,))
            if doc:
                docs.append(doc[0])
        return docs
