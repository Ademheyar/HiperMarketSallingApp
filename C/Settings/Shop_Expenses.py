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
from turtle import title

current_dir = os.path.abspath(os.path.dirname(__file__))
MAIN_dir = os.path.join(os.path.join(current_dir, '..'), '..')
sys.path.append(MAIN_dir)

data_dir = os.path.abspath(os.path.join(MAIN_dir, 'data'))
db_path = os.path.join(data_dir, 'my_database.db')

from D.Getdefsize import ButtonEntryApp
from C.List import *

from C.API.Get import *
from D.printer import *
from D.GetVALUE import GetvalueForm
# Connect to the database or create it if it does not exist

from C.List import *
from D.Getdate import GetDateForm
from D.Chart.Chart import *

from C.Product.selecttype import *

class ExpensesForm(tk.Frame):
    """Frame to list, search and edit the shop expenses."""
    def __init__(self, master, User, Shops):
        tk.Frame.__init__(self, master)
        self.selected_shop_filter = ""
        self.user = User
        self.shops = Shops
        self.shop_expenses = []  # flattened list of (shop_id, shop_name, shop_brand, index, expense_list)

        # Create the search bar frame and widgets
        self.search_frame = tk.Frame(self)
        self.search_frame.pack(side=tk.TOP, padx=5, pady=5)
        self.search_var = tk.StringVar()
        self.search_entry = tk.Entry(self.search_frame, textvariable=self.search_var)
        self.search_entry.pack(side=tk.LEFT, padx=5, pady=5)
        self.search_entry.bind('<KeyRelease>', self.update_search_results)
        self.search_var.trace_add("write", lambda *a: self.update_search_results())

        # Frame that will contain the canvas and scrollbars
        self.canvas_container = tk.Frame(self)
        self.canvas_container.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.list_container = tk.Frame(self.canvas_container)
        self.list_container.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Frame that holds the canvas (so we can hide/show easily)
        self.canvas_frame = tk.Frame(self.list_container)
        self.canvas_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        # Canvas for scrolling the inner frame
        self.item_canvas = tk.Canvas(self.canvas_frame)
        self.item_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

        self.canvas_v_scroll = tk.Scrollbar(self.canvas_frame, orient='vertical', command=self.item_canvas.yview)
        self.canvas_v_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        self.canvas_h_scroll = tk.Scrollbar(self.list_container, orient='horizontal', command=self.item_canvas.xview)
        self.canvas_h_scroll.pack(side=tk.TOP, fill=tk.X)

        self.item_canvas.configure(xscrollcommand=self.canvas_h_scroll.set, yscrollcommand=self.canvas_v_scroll.set)

        # Inner frame placed inside the canvas
        self.canvas_inner_frame = tk.Frame(self.item_canvas)
        self._inner_window = self.item_canvas.create_window((0, 0), window=self.canvas_inner_frame, anchor=tk.NW)
        self.canvas_inner_frame.bind('<Configure>', lambda _: self.item_canvas.configure(scrollregion=self.item_canvas.bbox("all")))
        self.item_canvas.bind('<Configure>', lambda e: self.item_canvas.itemconfigure(self._inner_window, width=e.width))

        # Frame inside inner frame to hold treeview and its scrollbars
        self.tree_frame = tk.Frame(self.canvas_inner_frame)
        self.tree_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Treeview for expenses
        self.tree = ttk.Treeview(self.tree_frame, show='headings')

        # configure treeview scroll commands
        self.tree_v_scroll = ttk.Scrollbar(self.tree_frame, orient='vertical', command=self.tree.yview)
        self.tree_h_scroll = ttk.Scrollbar(self.tree_frame, orient='horizontal', command=self.tree.xview)
        self.tree.configure(yscrollcommand=self.tree_v_scroll.set, xscrollcommand=self.tree_h_scroll.set)

        # pack tree and scrollbars inside the tree_frame
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.tree_v_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree_h_scroll.pack(side=tk.BOTTOM, fill=tk.X)

        # Columns: keep hidden shop identifiers at the end to make editing/deleting reliable
        self.tree['columns'] = ("Index", "Title", "Amount", "Category", "Date", "Ref", "Description", "ShopID", "ShopName", "ShopBrand")
        self.tree.heading("Index", text="ID")
        self.tree.heading("Title", text="Title")
        self.tree.heading("Amount", text="Amount")
        self.tree.heading("Category", text="Category")
        self.tree.heading("Date", text="Date")
        self.tree.heading("Ref", text="Ref")
        self.tree.heading("Description", text="Description")
        # hide shop id/name/brand columns visually (keep them in values for logic)
        self.tree.column("ShopID", width=0, stretch=False)
        self.tree.column("ShopName", width=0, stretch=False)
        self.tree.column("ShopBrand", width=0, stretch=False)
        # allow other columns to expand and also enable horizontal scrolling by giving reasonable minwidths
        self.tree.column("Title", width=200, minwidth=100, stretch=True)
        self.tree.column("Description", width=300, minwidth=100, stretch=True)
        self.tree.column("Amount", width=100, minwidth=60, stretch=False)
        self.tree.column("Category", width=120, minwidth=80, stretch=False)
        self.tree.column("Date", width=100, minwidth=80, stretch=False)
        self.tree.column("Ref", width=120, minwidth=80, stretch=False)

        self.tree.bind('<<TreeviewSelect>>', self.on_select)

        # Details / edit frame
        self.details_frame = tk.Frame(self)
        self.selected_shop_id = ""
        self.selected_shop_name = ""
        self.selected_shop_brand = ""
        self.selected_id = None

        # Form frame inside details
        self.form_frame = tk.Frame(self.details_frame)
        # Fields: Title (name), Description (code), Amount (typ), Category (short_key), Date (access), Ref (Times)
        self.title_label = tk.Label(self.form_frame, text='Title:')
        self.title_entry = tk.Entry(self.form_frame)
        self.title_entry.bind('<KeyRelease>', self.on_title_entry)

        self.description_label = tk.Label(self.form_frame, text='Description:')
        self.description_entry = tk.Entry(self.form_frame)

        self.amount_label = tk.Label(self.form_frame, text='Amount:')
        self.amount_entry = tk.Entry(self.form_frame)

        self.category_label = tk.Label(self.form_frame, text='Category:')
        self.category_var = tk.StringVar()
        self.category_combo = ttk.Combobox(self.form_frame, textvariable=self.category_var,
                    values=['Rent', 'Salary', 'Utilities', 'Supplies', 'Maintenance', 'Other'], width=20)
        self.category_combo.set('Other')

        self.date_label = tk.Label(self.form_frame, text='Date (YYYY-MM-DD):')
        self.date_entry = tk.Entry(self.form_frame)
        self.date_entry.insert(0, datetime.date.today().strftime('%Y-%m-%d'))
        self.date_today_btn = tk.Button(self.form_frame, text='Today',
                command=lambda: (self.date_entry.delete(0, tk.END),
                self.date_entry.insert(0, datetime.date.today().strftime('%Y-%m-%d'))))

        self.ref_label = tk.Label(self.form_frame, text='Receipt / Ref:')
        self.ref_entry = tk.Entry(self.form_frame)

        self.notes_label = tk.Label(self.form_frame, text='Notes:')
        self.notes_entry = tk.Entry(self.form_frame, width=40)

        # Recurrence widgets (kept but not required for search/edit)
        self.recur_frame = tk.Frame(self.form_frame, bd=0)
        self.repeats_var = tk.IntVar(value=0)

        def _toggle_repeats():
            state = tk.NORMAL if self.repeats_var.get() else tk.DISABLED
            self.freq_combo.config(state=state)
            self.interval_spin.config(state=state)
            self.end_entry.config(state=state)
            self.end_today_btn.config(state=state)

        self.repeats_check = tk.Checkbutton(self.recur_frame, text='Repeats', variable=self.repeats_var,
                    command=_toggle_repeats)
        self.interval_var = tk.IntVar(value=1)
        self.interval_spin = tk.Spinbox(self.recur_frame, from_=1, to=365, width=4, textvariable=self.interval_var, state=tk.DISABLED)
        self.freq_var = tk.StringVar(value='Monthly')
        self.freq_combo = ttk.Combobox(self.recur_frame, textvariable=self.freq_var,
                    values=['Daily', 'Weekly', 'Monthly', 'Yearly'], state=tk.DISABLED, width=10)
        self.end_label = tk.Label(self.recur_frame, text='End:')
        self.end_entry = tk.Entry(self.recur_frame, width=12, state=tk.DISABLED)
        self.end_today_btn = tk.Button(self.recur_frame, text='Today',
                    command=lambda: (self.end_entry.delete(0, tk.END),
                    self.end_entry.insert(0, datetime.date.today().strftime('%Y-%m-%d'))),
                    state=tk.DISABLED)

        # Layout
        self.form_frame.grid_columnconfigure(0, weight=0, pad=4)
        self.form_frame.grid_columnconfigure(1, weight=1)
        self.title_label.grid(row=0, column=0, sticky=tk.E, padx=5, pady=4)
        self.title_entry.grid(row=0, column=1, sticky=tk.W+tk.E, padx=5, pady=4)
        self.description_label.grid(row=1, column=0, sticky=tk.E, padx=5, pady=4)
        self.description_entry.grid(row=1, column=1, sticky=tk.W+tk.E, padx=5, pady=4)
        self.amount_label.grid(row=2, column=0, sticky=tk.E, padx=5, pady=4)
        self.amount_entry.grid(row=2, column=1, sticky=tk.W, padx=5, pady=4)
        self.category_label.grid(row=3, column=0, sticky=tk.E, padx=5, pady=4)
        self.category_combo.grid(row=3, column=1, sticky=tk.W, padx=5, pady=4)
        self.date_label.grid(row=4, column=0, sticky=tk.E, padx=5, pady=4)
        self.date_entry.grid(row=4, column=1, sticky=tk.W, padx=(5,2), pady=4)
        self.date_today_btn.grid(row=4, column=2, sticky=tk.W, padx=(2,5), pady=4)
        self.ref_label.grid(row=5, column=0, sticky=tk.E, padx=5, pady=4)
        self.ref_entry.grid(row=5, column=1, sticky=tk.W+tk.E, padx=5, pady=4)
        self.notes_label.grid(row=6, column=0, sticky=tk.NE, padx=5, pady=4)
        self.notes_entry.grid(row=6, column=1, sticky=tk.W+tk.E, padx=5, pady=4)
        self.recur_frame.grid(row=7, column=0, columnspan=3, sticky=tk.W, padx=5, pady=(6,2))
        self.repeats_check.grid(row=0, column=0, sticky=tk.W, padx=(0,8))
        tk.Label(self.recur_frame, text='Every').grid(row=0, column=1, sticky=tk.W)
        self.interval_spin.grid(row=0, column=2, sticky=tk.W, padx=(4,8))
        self.freq_combo.grid(row=0, column=3, sticky=tk.W, padx=(0,6))
        self.end_label.grid(row=0, column=4, sticky=tk.W)
        self.end_entry.grid(row=0, column=5, sticky=tk.W, padx=(4,4))
        self.end_today_btn.grid(row=0, column=6, sticky=tk.W)

        self.form_frame.grid(row=0, column=0, padx=5, pady=5, sticky=tk.N+tk.S+tk.E+tk.W)

        # Action buttons
        self.add_button = tk.Button(self.details_frame, text='New', command=self.add_tool)
        self.cancel_button = tk.Button(self.details_frame, text='Cancel', command=self.hide_add_form)
        self.add_button.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.cancel_button.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)

        self.add_new_button = tk.Button(self.search_frame, text='Add Expense', command=self.show_add_form)
        self.add_new_button.pack(side=tk.LEFT, padx=5, pady=5)
        self.change_button = tk.Button(self.search_frame, text='Change', command=self.show_change_form, state=tk.DISABLED)
        self.change_button.pack(side=tk.LEFT, padx=5, pady=5)
        self.delete_button = tk.Button(self.search_frame, text='Delete', command=self.delete_tool, state=tk.DISABLED)
        self.delete_button.pack(side=tk.LEFT, padx=5, pady=5)

        # initial load
        self.update_tool_listbox()

    def clear_tool_details_widget(self):
        self.title_entry.delete(0, tk.END)
        self.description_entry.delete(0, tk.END)
        self.amount_entry.delete(0, tk.END)
        self.category_combo.set('Other')
        self.date_entry.delete(0, tk.END)
        self.date_entry.insert(0, datetime.date.today().strftime('%Y-%m-%d'))
        self.ref_entry.delete(0, tk.END)
        self.notes_entry.delete(0, tk.END)
        self.selected_id = None
        self.selected_shop_id = ""
        self.selected_shop_name = ""
        self.selected_shop_brand = ""
        self.add_button.config(text="New")

    def show_add_form(self):
        self.clear_tool_details_widget()
        # hide the list area (canvas_frame)
        self.canvas_frame.pack_forget()
        self.details_frame.pack(side=tk.RIGHT, fill=tk.Y, expand=True)

    def hide_add_form(self):
        self.clear_tool_details_widget()
        self.details_frame.pack_forget()
        # show the list area again
        self.canvas_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    def show_change_form(self):
        sel = self.tree.selection()
        if not sel:
            return

        # hide the list area and show details
        self.canvas_frame.pack_forget()
        vals = self.tree.item(sel[0])['values']
        self.change_expense = vals
        # values mapped: Index, Title, Amount, Category, Date, Ref, Description, ShopID, ShopName, ShopBrand, ... (extra fields may exist)
        # populate form
        # title_entry, code, typ, short_key, acsess, ref, notes, freq_combo, isrepeats, interval, end_date
        self.title_entry.delete(0, tk.END); self.title_entry.insert(0, vals[0])
        self.description_entry.delete(0, tk.END); self.description_entry.insert(0, vals[1])
        self.amount_entry.delete(0, tk.END); self.amount_entry.insert(0, vals[2])
        self.category_combo.set(vals[3])
        self.date_entry.delete(0, tk.END); self.date_entry.insert(0, vals[4])
        self.ref_entry.delete(0, tk.END); self.ref_entry.insert(0, vals[5] if len(vals) > 5 else "")
        self.notes_entry.delete(0, tk.END); self.notes_entry.insert(0, vals[6] if len(vals) > 6 else "")
        self.freq_combo.set(vals[7] if len(vals) > 7 else "")
        self.repeats_check.deselect() if vals[8] == 0 else self.repeats_check.select()

        self.interval_var.set(int(vals[9]) if len(vals) > 9 else 1)
        self.end_entry.delete(0, tk.END); self.end_entry.insert(0, vals[10] if len(vals) > 10 else "")

        self.add_button.config(text="Update")
        self.details_frame.pack(side=tk.RIGHT, fill=tk.Y, expand=False)


    def search_tools(self, search_text):
        # case-insensitive substring search across title, description, amount, category
        s = (search_text or "").strip().lower()
        results = []
        for shop in self.shops:
            if self.selected_shop_filter and shop.get('Shop_name') != self.selected_shop_filter:
                continue
            if not shop:
                continue
            shop_exp = []
            if shop.get('Shop_Expenses'):
                try:
                    shop_exp = json.loads(shop['Shop_Expenses'])
                except Exception:
                    shop_exp = []
            for idx, exp in enumerate(shop_exp):
                # exp expected as [name, description, typ, short_key, acsess, ref, notes, freq_combo, isrepeats, interval, end_date]
                name = str(exp[0]) if len(exp) > 0 else ""
                description = str(exp[1]) if len(exp) > 1 else ""
                typ = str(exp[2]) if len(exp) > 2 else ""
                short_key = str(exp[3]) if len(exp) > 3 else ""
                acsess = str(exp[4]) if len(exp) > 4 else ""
                ref = str(exp[5]) if len(exp) > 5 else ""
                notes = str(exp[6]) if len(exp) > 6 else ""
                freq_combo = str(exp[7]) if len(exp) > 7 else ""
                isrepeats = str(exp[8]) if len(exp) > 8 else ""
                interval = str(exp[9]) if len(exp) > 9 else ""
                end_date = str(exp[10]) if len(exp) > 10 else ""

                hay = " ".join([name, description, typ, short_key, acsess, ref, notes, freq_combo, isrepeats, interval, end_date]).lower()
                if s == "" or s in hay:
                    results.append((name, description, typ, short_key, acsess, ref, notes, freq_combo, isrepeats, interval, end_date,
                                    shop.get('Shop_Id'), shop.get('Shop_name'), shop.get('Shop_brand_name')))
        return results

    def Add_tool_listbox(self, results):
        # clear and insert
        self.tree.delete(*self.tree.get_children())
        for r in results:
            values = (r)
            self.tree.insert('', 'end', values=values)

    def update_search_results(self, *args):
        search_str = self.search_var.get()
        results = self.search_tools(search_str)
        self.Add_tool_listbox(results)
        # when searching, hide details pane
        self.hide_add_form()
        self.change_button.config(state=tk.DISABLED)
        self.delete_button.config(state=tk.DISABLED)

    def update_tool_listbox(self):
        # rebuild the list from shops
        results = self.search_tools("")  # empty -> all
        self.Add_tool_listbox(results)
        self.hide_add_form()
        self.change_button.config(state=tk.DISABLED)
        self.delete_button.config(state=tk.DISABLED)

    def add_tool(self):
        name = self.title_entry.get().strip()
        description = self.description_entry.get().strip()
        amount = self.amount_entry.get().strip()
        typ = self.amount_entry.get().strip()
        short_key = self.category_combo.get().strip()
        date = self.date_entry.get().strip()
        ref = self.ref_entry.get().strip()
        notes = self.notes_entry.get().strip()
        freq_combo = self.freq_var.get().strip()
        interval = self.interval_var.get() if self.repeats_var.get() else 0
        end_date = self.end_entry.get().strip() if self.repeats_var.get() else ""
        isrepeats = self.repeats_var.get()
        # determine target shop: prefer selected_shop_filter, else if only one shop use it, otherwise add to all
        target_shops = []
        if self.selected_shop_filter:
            target_shops = [s for s in self.shops if s.get('Shop_name') == self.selected_shop_filter]
        elif len(self.shops) == 1:
            target_shops = [self.shops[0]]
        else:
            # default: add to all shops (behaviour retained)
            target_shops = self.shops

        for shop in target_shops:
            shop_exp = []
            if shop.get('Shop_Expenses'):
                try:
                    shop_exp = json.loads(shop['Shop_Expenses'])
                except Exception:
                    shop_exp = []
            if self.add_button.cget("text") == "New":
                shop_exp.append([name, description, typ, short_key, date, ref, notes, freq_combo, isrepeats, interval, end_date])
                # update DB and local shops list
                print("Adding expense to shop:", shop.get('Shop_name'))
                cur.execute("UPDATE Shops SET Shop_Expenses=? WHERE Shop_id=? AND Shop_name=? AND Shop_brand_name=?",
                            (json.dumps(shop_exp), str(shop.get('Shop_Id')), str(shop.get('Shop_name')), str(shop.get('Shop_brand_name'))))
                conn.commit()
                shop['Shop_Expenses'] = json.dumps(shop_exp)
            else:
                print("Updating existing expense")
                for idx, exp in enumerate(shop_exp):
                    # exp expected as [name, description, typ, short_key, date, ref, notes, freq_combo, isrepeats, interval, end_date]
                    print("matching expense:", exp)
                    print("against:", self.change_expense)
                    if str(self.change_expense[0]) == str(exp[0]) and str(self.change_expense[1]) == str(exp[1]) and str(self.change_expense[2]) == str(exp[2]) and str(self.change_expense[4]) == str(exp[4]):
                        
                        print("Updating shop expenses:", shop_exp)
                        shop_exp[idx] = [name, description, typ, short_key, date, ref, notes, freq_combo, isrepeats, interval, end_date]
                        # update DB and local shops list
                        cur.execute("UPDATE Shops SET Shop_Expenses=? WHERE Shop_id=? AND Shop_name=? AND Shop_brand_name=?",
                                        (json.dumps(shop_exp), str(shop.get('Shop_Id')), str(shop.get('Shop_name')), str(shop.get('Shop_brand_name'))))
                        conn.commit()
                        shop['Shop_Expenses'] = json.dumps(shop_exp)
                        break

        self.update_tool_listbox()

    def delete_tool(self):
        sel = self.tree.selection()
        if not sel:
            return
        vals = self.tree.item(sel[0])['values']
        title = vals[0]
        description = str(vals[1])
        amount = str(vals[2])
        date = str(vals[4])
        # find the shop dict
        for shop in self.shops:
            shop_exp = []
            if shop.get('Shop_Expenses'):
                try:
                    shop_exp = json.loads(shop['Shop_Expenses'])
                except Exception:
                    shop_exp = []
            # find matching expense entry
            for idx, exp in enumerate(shop_exp):
                # exp expected as [name, description, typ, short_key, acsess, ref, notes, freq_combo, isrepeats, interval, end_date]
                if title == str(exp[0]) and description == str(exp[1]) and amount == str(exp[2]) and date == str(exp[3]):
                    # delete this entry
                    shop_exp.pop(idx)
                    cur.execute("UPDATE Shops SET Shop_Expenses=? WHERE Shop_id=? AND Shop_name=? AND Shop_brand_name=?",
                                (json.dumps(shop_exp), str(shop.get('Shop_Id')), str(shop.get('Shop_name')), str(shop.get('Shop_brand_name'))))
                    conn.commit()
                    shop['Shop_Expenses'] = json.dumps(shop_exp)

        self.update_tool_listbox()

    def on_title_entry(self, event):
        # simple helper: if name matches existing in tools table, switch to Update else New
        cur.execute('SELECT * FROM tools')
        products = cur.fetchall()
        for product in products:
            if product[1] == self.title_entry.get():
                self.add_button.config(text="Update")
                return
        if self.selected_id is not None and self.title_entry.get() != "":
            self.add_button.config(text="Update")
        else:
            self.add_button.config(text="New")

    def on_select(self, event):
        if len(event.widget.selection()) > 0:
            self.change_button.config(state=tk.NORMAL)
            self.delete_button.config(state=tk.NORMAL)
