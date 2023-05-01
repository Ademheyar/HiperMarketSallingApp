import tkinter as tk
import sqlite3
from ItemSelector import ItemSelectorWidget
from tkinter import ttk

class search_entry(ttk.Entry):
    def __init__(self, *args, **kwargs):
        ttk.Entry.__init__(self, *args, **kwargs)
        self.var = self["textvariable"]
        if self.var == '':
            self.var = self["textvariable"] = tk.StringVar()
        self.var.trace('w', self.changed)
        self.bind("<Return>", self.select)
        self.bind("<Escape>", lambda _: self.var.set(''))

        # Connect to database
        self.conn = sqlite3.connect('my_database.db')
        self.cursor = self.conn.cursor()
        
        # Initialize search type
        self.search_type = "name"
        self.lb_up = False

    def changed(self, name, index, mode):
        if self.var.get() == '':
            self.lb.destroy()
            self.lb_up = False
        else:
            words = self.comparison()
            if words:
                if not self.lb_up:
                    self.lb = tk.Listbox(width=self["width"], height=5)
                    self.lb.bind("<Double-Button-1>", self.select)
                    self.lb.bind("<Return>", self.select)
                    self.lb.place(x=self.winfo_x(), y=self.winfo_y()+self.winfo_height())
                    self.lb_up = True
                self.lb.delete(0, tk.END)
                for w in words:
                    self.lb.insert(tk.END,w)
            else:
                if self.lb_up:
                    self.lb.destroy()
                    self.lb_up = False

    
    def select(self, _):
        if self.lb_up:
            selected_item = self.lb.get(tk.ACTIVE)
            self.var.set(selected_item)
            self.lb.destroy()
            self.lb_up = False
            self.icursor(tk.END)
            self.update_search_results(selected_item)

    def update_search_results(self, selected_item):
        #self.list_items.delete(0, tk.END)
        if self.search_type == "name":
            self.cursor.execute("SELECT * FROM product WHERE name=?", (selected_item,))
        elif self.search_type == "barcode":
            self.cursor.execute("SELECT * FROM product WHERE barcode=?", (selected_item,))
        elif self.search_type == "code":
            self.cursor.execute("SELECT * FROM product WHERE code=?", (selected_item,))
        elif self.search_type == "type":
            self.cursor.execute("SELECT * FROM product WHERE type=?", (selected_item,))
        result = self.cursor.fetchone()

        if result:
            a = ItemSelectorWidget(self, result[12], result[16], self.master.master.master.qty)
            print("ret : " + str([a.selected_shop.get(), a.selected_color.get(), a.selected_size.get(), a.selected_qty.get()]))
            print("info : " + str(result))
            self.master.master.master.list_items.insert("", "end", text=result[0], values=(result[2], a.selected_barcode.get(), result[1], a.selected_shop.get(), a.selected_color.get(), a.selected_size.get(), a.selected_qty.get(), result[9], self.master.master.master.disc, result[10],float(a.selected_qty.get())*float(result[9])))
            #column_name = tree.column("#1", "heading")
            for a in self.master.master.master.list_items.get_children():
                self.master.master.master.list_items.item(a)['values'][2] = "000"
                print("item : " + str(self.master.master.master.list_items.item(a)))
            self.master.master.master.qty = 0
            self.master.master.master.update_info()

    def comparison(self):
        query = self.var.get()
        if query:
            if self.search_type == "name":
                self.cursor.execute("SELECT * FROM product WHERE name LIKE ?", (f"%{query}%",))
            elif self.search_type == "barcode":
                self.cursor.execute("SELECT * FROM product WHERE barcode LIKE ?", (f"%{query}%",))
            elif self.search_type == "code":
                self.cursor.execute("SELECT * FROM product WHERE code LIKE ?", (f"%{query}%",))
            elif self.search_type == "type":
                self.cursor.execute("SELECT * FROM product WHERE type LIKE ?", (f"%{query}%",))
                
            results = []
            for row in self.cursor.fetchall():
                results.append(row[1])  #TODO: add price to
            return results
        else:
            return []