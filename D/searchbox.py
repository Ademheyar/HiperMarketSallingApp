import tkinter as tk
from tkinter import ttk
import sqlite3
import os
import sys
current_dir = os.path.abspath(os.path.dirname(__file__))
MAIN_dir = os.path.join(current_dir, '..')
sys.path.append(MAIN_dir)
from D.ItemSelector import ItemSelectorWidget
import os
from D.Doc.Loaddoc import *
from C.List import *

data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data'))
db_path = os.path.join(data_dir, 'my_database.db')
conn = sqlite3.connect(db_path)

class search_entry(ttk.Entry):
    def __init__(self, *args, **kwargs):
        ttk.Entry.__init__(self, *args, **kwargs)
        self.var = self["textvariable"]
        if self.var == '':
            self.var = self["textvariable"] = tk.StringVar()
        self.var.trace('w', self.changed)
        self.bind("<Up>", self.treeview_naigation)
        self.bind("<Down>", self.treeview_naigation)
        self.bind("<Return>", self.select)
        self.bind("<Escape>", lambda _: self.var.set(''))

        # Connect to database
        self.cursor = conn.cursor()
        
        # Initialize search type
        self.search_type = ""
        self.lb_up = False
        
         
    def treeview_naigation(self, event):
        print("treeview_naigation :" + str(self.lb.selection()))
        if not (event.keysym == "Up" or event.keysym == "Down"):
            self.focus_set()
        elif len(self.lb.selection()) == 0:
            print("focus on entry")
            self.lb.focus_set()
            self.lb.selection_set(self.lb.get_children()[0])
            
        elif event.keysym == 'Up':
            self.lb.selection_set(self.lb.prev(self.lb.selection()[0]))
            self.lb.configure(yscrollcommand=20)
        elif event.keysym == 'Down':
            self.lb.selection_set(self.lb.next(self.lb.selection()[0]))
            self.lb.configure(yscrollcommand=10)
            
    def changed(self, name, index, mode):
        if self.var.get() == '':
            self.lb.destroy()
            self.lb_up = False
        else:
            words = self.comparison()
            if words:
                if not self.lb_up:
                    w = self.grid_size()[0]
                    h = self.grid_size()[1]
                    self.lb = ttk.Treeview(self.master.master, columns=("", "", "", ""))
                    self.lb.bind("<Double-Button-1>", self.select)
                    self.lb.bind("<Return>", self.select)
                    #self.lb.bind("<Up>", self.treeview_naigation)
                    #self.lb.bind("<Down>", self.treeview_naigation)
                    self.lb.bind("<KeyPress>", self.treeview_naigation)
                    # width=w, height=5
                    self.lb.heading("#0", text="", anchor=tk.W)
                    self.lb.column("#0", minwidth=10, width=50)
                    self.lb.heading("#1", text="", anchor=tk.W)
                    self.lb.column("#1", minwidth=10, width=80) 
                    self.lb.heading("#2", text="", anchor=tk.W)
                    self.lb.column("#2", minwidth=10, width=100) 
                    self.lb.heading("#3", text="", anchor=tk.W)
                    self.lb.column("#3", minwidth=50, stretch=tk.YES)  
                    self.lb.heading("#4", text="", anchor=tk.W)
                    self.lb.column("#4", minwidth=50, stretch=tk.YES) 
                    self.lb.place(x=self.winfo_x(), y=self.winfo_y()+self.winfo_height()+25)
                    self.lb_up = True
                self.lb.delete(*self.lb.get_children())
                w = 0
                n_w = 0
                d_w = 0
                while w < len(words):
                    name_leng = len(str(words[w+3])) * 10
                    date_leng = len(str(words[w+4])) * 10
                    if n_w < name_leng:
                        self.lb.column("#3", width=name_leng)
                        n_w = name_leng
                    if d_w < name_leng:
                        self.lb.column("#4", width=date_leng)
                        d_w = name_leng
                    self.lb.insert("", "end", text=str(words[w]), values=(str(words[w+1]), str(words[w+2]), str(words[w+3]), str(words[w+4])))
                    if w+5 < len(words):
                        w += 5
                        continue
                    else:
                        break
            else:
                if self.lb_up:
                    self.lb.destroy()
                    self.lb_up = False

    def comparison(self):
        query = self.var.get()
        print("word: " + str(query) + " search_type: " + str(self.search_type))
        
        if query:

            results = []
            unique_item_results = set()  # To store unique results
            unique_results = set()  # To store unique results
            self.cursor.execute("SELECT * FROM product WHERE more_info LIKE ?",
                                (f"%{query}%",))
            for row in self.cursor.fetchall():
                result = (row[0], "ITEM", row[2], row[1], row[9])
                if row[0] not in unique_item_results:
                    unique_item_results.add(row[0])
                    results.extend(result)
                    unique_results.add(result)
            

            '''for row in self.cursor.fetchall():
                #print("row[2]  : " + str(row))
                qty_info_list = []
                #print("row[12]  : " + str(row[12]))
                if "\"{" in str(row[12]):
                    cod = str(row[4]).replace(",", "\\")
                    qty_info_list = read_code(row[12], "", cod, "", "")[4]
                else:
                    qty_info_list = load_list(row[12])
                for s in qty_info_list:
                    for c in s[1]:
                        if query.upper() in c[0].upper():
                            result = (row[0], "ITEM", c[0], row[1], row[9])
                            if row[0] not in unique_item_results:
                                results.extend(result)
                                unique_item_results.add(row[0])
                                unique_results.add(result)
                #result = (row[0], "ITEM", c[0], row[1], row[9])
                #if result not in unique_results:
                   # results.extend(result)
                    #unique_results.add(result)'''
            
            self.cursor.execute("SELECT * FROM product WHERE name LIKE ? OR code LIKE ? OR type LIKE ?",
                                (f"%{query}%", f"%{query}%", f"%{query}%"))
            
            for row in self.cursor.fetchall():
                result = (row[0], "ITEM", row[2], row[1], row[9])
                if row[0] not in unique_item_results:
                    unique_item_results.add(row[0])
                    results.extend(result)
                    unique_results.add(result)
            

            self.cursor.execute("SELECT * FROM doc_table WHERE doc_barcode LIKE ?", (f"%{query}%",))

            for row in self.cursor.fetchall():
                result = (row[0], "DOCUMENT", row[1], row[4], row[13])
                if result not in unique_results:
                    results.extend(result)
                    unique_results.add(result)
            print("results: " + str(len(results)) + " query: " + str(query))
            return results
        else:
            return []

    def select(self, _):
        if self.lb_up:
            selected_id = self.lb.item(self.lb.selection()[0])['text']
            selected_type = self.lb.item(self.lb.selection()[0])['values'][0]
            selected_item = self.lb.item(self.lb.selection()[0])['values'][2]
            print("selected_type : " + str(selected_type))
            if (selected_type == "DOCUMENT"):
                selected_item = self.lb.item(self.lb.selection()[0])['values'][1]
            if self.search_type == "":
                selected_id = self.lb.item(self.lb.selection()[0])['text']
            elif self.search_type == "barcode":
                selected_id = self.lb.item(self.lb.selection()[0])['text']
            elif self.search_type == "code":
                selected_id = self.lb.item(self.lb.selection()[0])['text']
            elif self.search_type == "type":
                selected_id = self.lb.item(self.lb.selection()[0])['text']
            self.lb.destroy()
            self.lb_up = False
            self.icursor(tk.END)
            self.update_search_results(selected_id, selected_item, selected_type)

    def update_search_results(self, selected_id, selected_item, selected_type):
        #self.list_items.delete(0, tk.END)
        result = None
        print("selected_type : " + str(selected_type))
        if self.search_type == "":
            self.search_type = "id"
        if (selected_type == "ITEM"):
            self.cursor.execute("SELECT * FROM product WHERE "+ self.search_type+ "=?", (selected_id,))
            result = self.cursor.fetchone()
            self.search_type = ""
            if result:
                self.var.set(str(result[0]) + "   " + str(result[2]) + "   " + str(result[1]))
                qty = 0
                if hasattr(self.master.master.master.master, 'qty'):
                    qty = self.master.master.master.master.qty
                print("selected_type2 : " + str(selected_item))
                a = ItemSelectorWidget(self, result[2], result[12], result[16], qty)
                self.wait_window(a.getvalue_form)
                print("ret : " + str(a.selected_items))
                print("info : " + str(result))
                for t in a.selected_items:
                    p = self
                    while(True):
                        if hasattr(p, 'add_item'):
                            break
                        else:
                            p = p.master
                            
                    p.add_item(result, None, selected_type, t[4][0], t[0], t[1], t[2], t[3], t[5])
                #column_name = tree.column("#1", "heading")
                for a in self.master.master.master.master.list_items.get_children():
                    self.master.master.master.master.list_items.item(a)['values'][2] = "000"
                    print("item : " + str(self.master.master.master.master.list_items.item(a)))
                self.master.master.master.master.qty = 0
                self.master.master.master.master.update_info()
        if (selected_type == "DOCUMENT"):
            self.cursor.execute("SELECT * FROM doc_table WHERE "+ self.search_type+ "=?", (selected_id,))
            result = self.cursor.fetchone()
            self.search_type = ""
            if result:
                self.master.master.master.master.get_ex_doc_items(result[1])
                self.master.master.master.master.get_ex_doc_payments(result[1])
                self.master.master.master.master.update_info()
        self.var.set("")
