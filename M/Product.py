import tkinter as tk
from tkinter import ttk
import sqlite3

# Connect to the database or create it if it does not exist

import os
data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data'))
db_path = os.path.join(data_dir, 'my_database.db')
conn = sqlite3.connect(db_path)
cur = conn.cursor()

conn.commit()

import tkinter as tk

class ProductForm(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)

        # Create the search bar
        # Create the frame for the search bar and buttons
        self.search_frame = tk.Frame(self)
        self.search_frame.pack(side=tk.TOP, padx=5, pady=5)

        # create a StringVar to represent the search box
        search_var = tk.StringVar()
        self.search_entry = tk.Entry(self.search_frame, textvariable=search_var)
        self.search_entry.pack(side=tk.LEFT, padx=5, pady=5)
            
        # bind the update_search_results function to the search box
        search_var.trace("w", self.update_search_results)
        
        self.add_new_button = tk.Button(self.search_frame, text='Add New product', command=self.show_add_product_forme)
        self.add_new_button.pack(side=tk.LEFT, padx=5, pady=5)
        self.change_button = tk.Button(self.search_frame, text='Change', command=self.show_change_product_forme)
        self.change_button.pack(side=tk.LEFT, padx=5, pady=5)
        self.change_button.config(state=tk.DISABLED)
        self.delete_button = tk.Button(self.search_frame, text='Delete', command=self.delete_product)
        self.delete_button.pack(side=tk.LEFT, padx=5, pady=5)

        # Create the list box
        self.list_box = ttk.Treeview(self)
        self.list_box.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.list_box.bind('<<ListboxSelect>>', self.on_select)

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
        self.name_entry.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)
        self.code_label = tk.Label(self.details_frame, text='Code:')
        self.code_label.grid(row=1, column=0, padx=5, pady=5, sticky=tk.E)
        self.code_entry = tk.Entry(self.details_frame)
        self.code_entry.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)
        self.type_label = tk.Label(self.details_frame, text='Type:')
        self.type_label.grid(row=2, column=0, padx=5, pady=5, sticky=tk.E)
        self.type_entry = tk.Entry(self.details_frame)
        self.type_entry.grid(row=2, column=1, padx=5, pady=5, sticky=tk.W)
        
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
        self.mark_label = tk.Label(self.tab2_frame, text='mark:')
        self.mark_label.grid(row=2, column=0, padx=5, pady=5, sticky=tk.E)
        self.mark_entry = tk.Entry(self.tab2_frame)
        self.mark_entry.grid(row=2, column=1, padx=5, pady=5, sticky=tk.W)
        self.price_label = tk.Label(self.tab2_frame, text='Price:')
        self.price_label.grid(row=3, column=0, padx=5, pady=5, sticky=tk.E)
        self.price_entry = tk.Entry(self.tab2_frame)
        self.price_entry.grid(row=3, column=1, padx=5, pady=5, sticky=tk.W)
        self.include_tax_var = tk.IntVar()
        self.include_tax_checkbutton = tk.Checkbutton(self.tab2_frame, text='Include Tax', variable=self.include_tax_var)
        self.include_tax_checkbutton.grid(row=4, column=0, padx=5, pady=5, sticky=tk.W)
        self.tax_label = tk.Label(self.tab2_frame, text='Tax:')
        self.tax_label.grid(row=5, column=0, padx=5, pady=5, sticky=tk.E)
        self.tax_entry = tk.Entry(self.tab2_frame)
        self.tax_entry.grid(row=5, column=1, padx=5, pady=5, sticky=tk.W)
        self.price_change_var = tk.IntVar()
        self.price_change_entry = tk.Checkbutton(self.tab2_frame, text='Price Change', variable=self.price_change_var)
        self.price_change_entry.grid(row=6, column=0, padx=5, pady=5, sticky=tk.W)
        
        # Create the frame for the product details
        self.tab3_frame = tk.Frame(self.notebook_frame)
        self.tab3_frame.pack_forget()
        self.notebook_frame.add(self.tab3_frame)

        # Create the list box
        self.more_info_label = tk.Label(self.tab3_frame, text='More Info:')
        self.more_info_label.grid(row=1, column=0, sticky=tk.E)

        self.inventory = []
        self.tree = ttk.Treeview(self.tab3_frame, columns=("Shop Name", "Color", "Size", "Barcode", "Qtyfirst", "Qty", "cdate", "update"))
        self.tree.grid(row=2, column=0, sticky=tk.E, columnspan=4)
        self.tree.heading("#0", text="Shop Name", anchor=tk.W)
        self.tree.column("#0", stretch=tk.NO, minwidth=25, width=125)
        self.tree.heading("#1", text="Color", anchor=tk.W)
        self.tree.column("#1", stretch=tk.NO, minwidth=25, width=125)
        self.tree.heading("#2", text="Size", anchor=tk.W)
        self.tree.column("#2", stretch=tk.NO, minwidth=25, width=125)
        self.tree.heading("#3", text="Barcode", anchor=tk.W)
        self.tree.column("#3", stretch=tk.NO, minwidth=25, width=125)
        self.tree.heading("#4", text="Qtyfirst", anchor=tk.W)
        self.tree.column("#4", stretch=tk.NO, minwidth=25, width=125)
        self.tree.heading("#5", text="Qty", anchor=tk.W)
        self.tree.column("#5", stretch=tk.NO, minwidth=25, width=125)
        self.tree.heading("#6", text="cdate", anchor=tk.W)
        self.tree.column("#6", stretch=tk.NO, minwidth=25, width=125)
        self.tree.heading("#7", text="update", anchor=tk.W)
        self.tree.column("#7", stretch=tk.NO, minwidth=25, width=125)

        self.shop_name_label = tk.Label(self.tab3_frame, text='At Shop :')
        self.shop_name_label.grid(row=7, column=0, sticky=tk.E)
        self.shop_name_entry = tk.Entry(self.tab3_frame)
        self.shop_name_entry.grid(row=7, column=1, sticky=tk.E)
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
        
        
        self.add_info_button = tk.Button(self.tab3_frame, text='Add', command=self.add_info)
        self.add_info_button.grid(row=22, column=0, sticky=tk.E)
        self.remove_info_button = tk.Button(self.tab3_frame, text='Remove', command=self.remove_info)
        self.remove_info_button.grid(row=22, column=1, sticky=tk.E)
      
        # Create the frame for the product details
        self.tab4_frame = tk.Frame(self.notebook_frame)
        self.tab4_frame.pack_forget()
        self.notebook_frame.add(self.tab4_frame)

        self.images_label = tk.Label(self.tab4_frame, text='Images:')
        self.images_label.grid(row=25, column=0, padx=5, pady=5, sticky=tk.E)
        self.images_entry = tk.Entry(self.tab4_frame)
        self.images_entry.grid(row=25, column=1, padx=5, pady=5, sticky=tk.W)

        self.add_button = tk.Button(self.details_frame, text='Add', command=self.add_product)
        self.add_button.grid(row=30, column=0, padx=5, pady=5, sticky=tk.W)
        self.cancle_button = tk.Button(self.details_frame, text='Cancle', command=self.hide_add_product_forme)
        self.cancle_button.grid(row=30, column=1, padx=5, pady=5, sticky=tk.W)

        # Pack the widgets for the product tab2
        self.update_product_listbox()

    def add_info_(self, shop_name, color, size, barcode, qtyfirst, qty, cdate, update):
        p = {"shop_name": shop_name, "color": color, "size": size, "barcode": barcode, "qtyfirst": qtyfirst, "qty": qty, "cdate": cdate, "update": update}
        self.inventory.append(p)
        self.update_tree()

    def get_unique_shop_names(self):
        return list(set([p["shop_name"] for p in self.inventory]))

    def get_unique_colors_for_shop_name(self, shop_name):
        return list(set([p["color"] for p in self.inventory if p["shop_name"] == shop_name]))

    def get_sizes_for_shop_name_and_color(self, shop_name, color):
        return list(set([p["size"] for p in self.inventory if p["shop_name"] == shop_name and p["color"] == color]))

    def get_barcode_and_qty_for_shop_name_and_color_and_size(self, shop_name, color, size):
        for p in self.inventory:
            if p["shop_name"] == shop_name and p["color"] == color and p["size"] == size:
                return (p["barcode"], p["qtyfirst"], p["qty"], p["cdate"], p["update"])
        return (None, None)
    
    def chang_to_list(self, vs_info):
        a_u_list = []
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
        return a_u_list

    def chang_to_text(self, a_u_list):
        vs_info = "\""
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
        return vs_info
    
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
    
    def get_inventory_nested_list(self):
        nested_list = []
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
        return nested_list

    def get_inventory_nested_list_text(self): # change tree vew nested list to text
        vs_info = '\"'
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
        return vs_info
    
    def update_tree(self):
        self.tree.delete(*self.tree.get_children())
        unique_shop_names = self.get_unique_shop_names()
        for shop_name in unique_shop_names:
            shop_name_node = self.tree.insert("", "end", text=shop_name)
            
            unique_colors = self.get_unique_colors_for_shop_name(shop_name)
            for color in unique_colors:
                color_node = self.tree.insert(shop_name_node, "end", text=color)
                sizes = self.get_sizes_for_shop_name_and_color(shop_name, color)
                for size in sizes:
                    barcode, qtyfirst, qty, cdate, update = self.get_barcode_and_qty_for_shop_name_and_color_and_size(shop_name, color, size)
                    if barcode and qtyfirst and qty and cdate and update:
                        self.tree.insert(color_node, "end", text=size, values=(barcode, qtyfirst, qty, cdate, update))
                    else:
                        self.tree.insert(color_node, "end", text=size)
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
        
        txt = self.get_inventory_nested_list_text()
        #l = self.get_inventory_nested_list()
        #print("list : " + str(l))
        #txt = self.chang_to_text(l)
        #print("list : " + str(txt))
        #le = self.chang_to_list(txt)
        #print("le :" + str(le))
        self.more_info_label.config(text=txt)
        
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

        if not found:
            self.add_info_(self.shop_name_entry.get(), self.color_entry.get(), self.size_entry.get(), self.bracode_entry.get(), self.qty_entry.get(), self.qty_entry.get(), "", "")

        txt = self.get_inventory_nested_list_text()
        #l = self.get_inventory_nested_list()
        #print("list : " + str(l))
        #txt = self.chang_to_text(l)
        #print("list : " + str(txt))
        #le = self.chang_to_list(txt)
        #print("le :" + str(le))
        self.more_info_label.config(text=txt)
        
        
    def show_product_form(self):
        # call the function in the main file to show the first frame
        self.master.master.show_frame("ProductFrame")
        
    def search_products(search_text):
        
        # Search for the entered text in the code, name, barcode, and type fields of the product table
        cur.execute("SELECT * FROM product WHERE code LIKE ? OR name LIKE ? OR barcode LIKE ? OR type LIKE ?", 
                    ('%' + search_text + '%', '%' + search_text + '%', '%' + search_text + '%', '%' + search_text + '%'))
        results = cur.fetchall()
        
        return results
        

    # create a function to update the search results whenever the search box changes
    def update_search_results(*args):
        # get the search string from the search box
        search_str = search_var.get()
        
        # search for products based on the search string
        results = search_products(search_str)
        
        # clear the current items in the list box
        self.list_box.delete(*self.list_box.get_children())
        self.list_box['columns'] = ('Name', 'Code', 'Type', 'Price')
        self.list_box.heading("#0", text="ID")
        self.list_box.heading("#1", text="Name")
        self.list_box.heading("#2", text="Code")
        self.list_box.heading("#3", text="Type")
        self.list_box.heading("#4", text="Price")

        # Add the products to the product listbox
        for product in products:
            self.list_box.insert('', 'end', text=product[0], values=(product[1], product[2], product[3], product[9]))
            

        
    def clear_product_details_widget(self):
        # Clear the product details widgets
        self.name_entry.delete(0, tk.END)
        self.code_entry.delete(0, tk.END)
        self.type_entry.delete(0, tk.END)
        #self.barcode_entry.delete(0, tk.END)
        #self.at_shop_entry.delete(0, tk.END)
        #self.quantity_entry.delete(0, tk.END)
        self.cost_entry.delete(0, tk.END)
        self.tax_entry.delete(0, tk.END)
        self.price_entry.delete(0, tk.END)
        self.include_tax_var.set(0)
        self.price_change_var.set(0)
        self.more_info_label['text'] = ""
        self.images_entry.delete(0, tk.END)
        self.description_entry.delete(0, tk.END)
        self.service_change_var.set(0)
        self.default_quantity_change_var.set(0)
        self.active_var.set(0)
        
    # Create the "Add New" button
    def show_add_product_forme(self):
        self.notebook_frame.pack(side=tk.RIGHT, fill=tk.Y, expand=False)

    def hide_add_product_forme(self):
        self.notebook_frame.pack_forget()
        self.clear_product_details_widget()

    # Create the "Change" button
    def show_change_product_forme():
        self.notebook_frame.pack(side=tk.RIGHT, fill=tk.Y, expand=False)

    def on_select(event):
        if len(event.widget.curselection()) > 0:
            self.change_button.config(state=tk.NORMAL)
        else:
            self.change_button.config(state=tk.DISABLED)

    # Create the "Delete" button
    
    # Define the function for deleting a product
    def delete_product(self):
        # Get the selected product from the listbox
        for selected_product in self.list_box.selection():
            # Get the ID of the selected product
            product_id = self.list_box.item(selected_product)['text']
            # Delete the product from the database
            cur.execute('DELETE FROM product WHERE id=?', (int(product_id),))

            # Commit the changes to the database
            conn.commit()

            # Clear the product details widgets
            self.clear_product_details_widget()

            # Update the product listbox
            self.update_product_listbox()

    # Define the function for hiding the product details frame
    def hide_product_details_frame(self):
        pass
        # Hide the product details frame
        #product_details_frame.grid_remove()

        # Show the add product button
        #add_product_button.grid()
    def get_item_by_code(self, item_code):
        self.cursor.execute("SELECT * FROM product WHERE code=?", (item_code,))
        result = self.cursor.fetchone()
        return result
    
    def update_item_info(self, id, code, it_info):
        pass

    # Define the function for updating the product listbox
    def update_product_listbox(self):
        # Clear the product listbox
        self.list_box.delete(*self.list_box.get_children())

        # Get the products from the database
        cur.execute('SELECT * FROM product')
        products = cur.fetchall()
        self.list_box['columns'] = ('Name', 'Code', 'Type', 'Price')
        self.list_box.heading("#0", text="ID")
        self.list_box.heading("#1", text="Name")
        self.list_box.heading("#2", text="Code")
        self.list_box.heading("#3", text="Type")
        self.list_box.heading("#4", text="Price")

        # Add the products to the product listbox
        for product in products:
            self.list_box.insert('', 'end', text=product[0], values=(product[1], product[2], product[3], product[9]))
            

        # Hide the product details frame
        self.hide_product_details_frame()
        self.change_button.config(state=tk.DISABLED)

    # Define the function for adding a new product
    def add_product(self):
        # Get the values from the product details widgets
        name = self.name_entry.get()
        code = self.code_entry.get()
        typ = self.type_entry.get()
        barcode = 0
        #self.barcode_entry.get()
        at_shop = 0
        # self.at_shop_entry.get()
        quantity = 0
        # self.quantity_entry.get()
        cost = self.cost_entry.get()
        tax = self.tax_entry.get()
        price = self.price_entry.get()
        include_tax = self.include_tax_var.get()
        price_change = self.price_change_var.get()
        more_info = self.more_info_label['text']
        images = self.images_entry.get()
        description = self.description_entry.get()
        service = self.service_change_var.get()
        default_quantity = self.default_quantity_change_var.get()
        active = self.active_var.get()
        
        
        print(str([name, code, typ, barcode, at_shop, quantity, cost, tax, price, include_tax, price_change, more_info, images, description, service, default_quantity, active]))
        # Insert the new product into the database
        cur.execute('INSERT INTO product (name, code, type, barcode, at_shop, quantity, cost, tax, price, include_tax, price_change, more_info, images, description, service, default_quantity, active) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (name, code, typ, barcode, at_shop, quantity, cost, tax, price, include_tax, price_change, more_info, images, description, service, default_quantity, active))
        
        # Commit the changes to the database
        conn.commit()
        
        # Clear the product details widgets
        self.clear_product_details_widget()
        
        # Update the product listbox
        self.update_product_listbox()

    # Define the function for changing an existing product
    def change_product():
        # Get the selected product from the listbox
        selected_product = self.product_listbox.curselection()
        
        if selected_product:
            # Get the values from the product details widgets
            name = self.name_entry.get()
            code = self.code_entry.get()
            type = self.type_entry.get()
            barcode = self.barcode_entry.get()
            at_shop = self.at_shop_entry.get()
            quantity = self.quantity_entry.get()
            cost = self.cost_entry.get()
            tax = self.tax_entry.get()
            price = self.price_entry.get()
            include_tax = self.include_tax_var.get()
            price_change = self.price_change_entry.get()
            more_info = self.more_info_entry.get()
            images = self.images_entry.get()
            description = self.description_entry.get()
            service = self.service_entry.get()
            default_quantity = self.default_quantity_entry.get()
            active = self.active_var.get()

            # Get the ID of the selected product
            product_id = self.product_listbox.get(selected_product)[0]

            # Update the product in the database
            cur.execute('UPDATE product SET name=?, code=?, type=?, barcode=?, at_shop=?, quantity=?, cost=?, tax=?, price=?, include_tax=?, price_change=?, more_info=?, images=?, description=?, service=?, default_quantity=?, active=? WHERE id=?', (name, code, type, barcode, at_shop, quantity, cost, tax, price, include_tax, price_change, more_info, images, description, service, default_quantity, active, product_id))

            # Commit the changes to the database
            conn.commit()

            # Clear the product details widgets
            self.clear_product_details_widget()
            # Update the product listbox
            self.update_product_listbox()
    # Define the function for showing the product details frame
    def show_product_details_frame():
        # Show the product details frame
        self.product_details_frame.grid(row=0, column=1, sticky='nsew')

        # Hide the add product button
        self.add_product_button.grid_remove()

        # Clear the product details widgets
        self.clear_product_details_widget()

    # Define the function for updating an existing product
    def update_product():
        # Get the values from the product details widgets
        name = self.name_entry.get()
        code = self.code_entry.get()
        type = self.type_entry.get()
        barcode = self.barcode_entry.get()
        at_shop = self.at_shop_entry.get()
        quantity = self.quantity_entry.get()
        cost = self.cost_entry.get()
        tax = self.tax_entry.get()
        price = self.price_entry.get()
        include_tax = self.include_tax_var.get()
        price_change = self.price_change_entry.get()
        more_info = self.more_info_entry.get()
        images = self.images_entry.get()
        description = self.description_entry.get()
        service = self.service_entry.get()
        default_quantity = self.default_quantity_entry.get()
        active = active_var.get()

        # Update the product in the database
        cur.execute('UPDATE product SET name=?, code=?, type=?, barcode=?, at_shop=?, quantity=?, cost=?, tax=?, price=?, include_tax=?, price_change=?, more_info=?, images=?, description=?, service=?, default_quantity=?, active=? WHERE id=?', (name, code, type, barcode, at_shop, quantity, cost, tax, price, include_tax, price_change, more_info, images, description, service, default_quantity, active, selected_product_id))
        conn.commit()

        # Clear the product details widgets
        clear_product_details_widgets()

        # Update the product listbox
        self.update_product_listbox()

        # Hide the product details frame
        hide_product_details_frame()