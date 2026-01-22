import tkinter as tk
from tkinter import ttk
import sqlite3

import json
# Connect to the database or create it if it does not exist

import os

from D.Security import Chacke_Security
data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data'))
db_path = os.path.join(data_dir, 'my_database.db')
conn = sqlite3.connect(db_path)
cur = conn.cursor()

conn.commit()

from C.List import *
from C.Sql3 import *

class ToolForm(tk.Frame):
    def __init__(self, master, User, Shops, on_Shop):
        tk.Frame.__init__(self, master)
        self.Selected_Shop = ""
        self.user = self.User = User
        self.Shops = Shops
        self.on_Shop = on_Shop
        self.Shop_Payment_Tools = []
        
        # Create the search bar
        # Create the frame for the search bar and buttons
        self.search_frame = tk.Frame(self)
        self.search_frame.pack(side=tk.TOP, padx=5, pady=5)

        # create a StringVar to represent the search box
        self.search_var = tk.StringVar()
        self.search_entry = tk.Entry(self.search_frame, textvariable=self.search_var)
        self.search_entry.pack(side=tk.LEFT, padx=5, pady=5)

        if Chacke_Security(self, self.user, self.Shops[self.on_Shop], 32, f'User Has No Permission To Access Search Tools OR LOGIN AS ADMIN'):                        
            self.search_entry.bind('<KeyRelease>', self.update_search_results)
                
            # bind the update_search_results function to the search box
            self.search_var.trace("w", self.update_search_results)

        # Create the list box
        self.list_box = ttk.Treeview(self)
        self.list_box.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.list_box.bind('<<TreeviewSelect>>', self.on_select)

        # Create the frame for the product details
        self.details_frame = tk.Frame(self.list_box)
        self.details_frame.pack_forget()
        self.selected_shop_id = ""
        self.selected_shop_name = ""
        self.selected_id = ""
        self.main_name = ""
        # Create the widgets for the product details
        self.name_label = tk.Label(self.details_frame, text='Tool Name :')
        self.name_entry = tk.Entry(self.details_frame)
        self.name_entry.bind('<KeyRelease>', lambda: self.on_name_entry)
        self.type_label = tk.Label(self.details_frame, text='Tool Method :')
        self.type_entry = ttk.Combobox(self.details_frame,
                           values=('CASH', 'CARD', 'CREADIT', 'CASHOUT', 'CASHIN', 'OTHER'),
                           state='readonly')
        # self.type_entry.set('')   no default selected; remove this line if you want a default
        self.code_label = tk.Label(self.details_frame, text='Tool ID :')
        self.code_entry = tk.Entry(self.details_frame)
        self.short_key_label = tk.Label(self.details_frame, text='Tool Short cut :')
        self.short_key_entry = tk.Entry(self.details_frame)
        self.acsess_label = tk.Label(self.details_frame, text='Tool Acsess key :')
        self.acsess_entry = tk.Entry(self.details_frame)
        self.enable_label = tk.IntVar()
        self.enable_entry = tk.Checkbutton(self.details_frame, text='Tool enabel :', variable=self.enable_label)
        self.quick_pay_label = tk.IntVar()
        self.quick_pay_entry = tk.Checkbutton(self.details_frame, text='Tool Quick payment :', variable=self.quick_pay_label)
        self.markaspad_label = tk.IntVar()
        self.markaspad_entry = tk.Checkbutton(self.details_frame, text='Tool Mark Pad :', variable=self.markaspad_label)
        self.customer_required_label = tk.IntVar()
        self.customer_required_entry = tk.Checkbutton(self.details_frame, text='Tool Customer Required :', variable=self.customer_required_label)
        self.open_drower_label = tk.IntVar()
        self.open_drower_entry = tk.Checkbutton(self.details_frame, text='Tool Open Cahs Drawer:', variable=self.open_drower_label)
        self.print_slip_label = tk.IntVar()
        self.print_slip_entry = tk.Checkbutton(self.details_frame, text='Tool Print Receiipt:', variable=self.print_slip_label)
        self.change_allowed_label = tk.IntVar()
        self.change_allowed_entry = tk.Checkbutton(self.details_frame, text='Change Allowed:', variable=self.change_allowed_label)
        self.add_button = tk.Button(self.details_frame, text='Add', command=self.add_tool)
        self.cancle_button = tk.Button(self.details_frame, text='Cancle', command=self.hide_add_forme)
        
        self.add_new_button = tk.Button(self.search_frame, text='Add New', command=self.show_add_forme)
        self.add_new_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.change_button = tk.Button(self.search_frame, text='Change', command=self.show_change_forme)
        self.change_button.pack(side=tk.LEFT, padx=5, pady=5)
        self.change_button.config(state=tk.DISABLED)

        self.delete_button = tk.Button(self.search_frame, text='Delete', command=self.delete_tool)
        self.delete_button.pack(side=tk.LEFT, padx=5, pady=5)
        self.delete_button.config(state=tk.DISABLED)
        if not Chacke_Security(self, self.user, self.Shops[self.on_Shop], 38, f'User Has No Permission To Add New Tools OR LOGIN AS ADMIN'):                        
            self.add_new_button.config(state=tk.DISABLED)
        if not Chacke_Security(self, self.user, self.Shops[self.on_Shop], 39, f'User Has No Permission To Change Tools OR LOGIN AS ADMIN'):                        
            self.change_button.config(state=tk.DISABLED)
        if not Chacke_Security(self, self.user, self.Shops[self.on_Shop], 51, f'User Has No Permission To Delete Tools OR LOGIN AS ADMIN'):                        
            self.delete_button.config(state=tk.DISABLED)

        # Pack the widgets for the product details
        self.name_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.E)
        self.name_entry.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)
        self.code_label.grid(row=1, column=0, padx=5, pady=5, sticky=tk.E)
        self.code_entry.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)
        self.type_label.grid(row=2, column=0, padx=5, pady=5, sticky=tk.E)
        self.type_entry.grid(row=2, column=1, padx=5, pady=5, sticky=tk.W)
        self.short_key_label.grid(row=3, column=0, padx=5, pady=5, sticky=tk.E)
        self.short_key_entry.grid(row=3, column=1, padx=5, pady=5, sticky=tk.W)
        self.acsess_label.grid(row=4, column=0, padx=5, pady=5, sticky=tk.E)
        self.acsess_entry.grid(row=4, column=1, padx=5, pady=5, sticky=tk.W)
        #self.enable_label.grid(row=5, column=0, padx=5, pady=5, sticky=tk.E)
        self.enable_entry.grid(row=5, column=1, padx=5, pady=5, sticky=tk.W)
        #self.quick_pay_label.grid(row=6, column=0, padx=5, pady=5, sticky=tk.W)
        self.quick_pay_entry.grid(row=6, column=1, padx=5, pady=5, sticky=tk.W)
        self.markaspad_entry.grid(row=11, column=1, padx=5, pady=5, sticky=tk.W)
        #self.customer_required_label.grid(row=7, column=0, padx=5, pady=5, sticky=tk.W)
        self.customer_required_entry.grid(row=7, column=1, padx=5, pady=5, sticky=tk.W)
        #self.print_slip_label.grid(row=8, column=0, padx=5, pady=5, sticky=tk.E)
        self.open_drower_entry.grid(row=10, column=1, padx=5, pady=5, sticky=tk.W)
        self.print_slip_entry.grid(row=8, column=1, padx=5, pady=5, sticky=tk.W)
        #self.change_allowed_label.grid(row=9, column=0, padx=5, pady=5, sticky=tk.W)
        self.change_allowed_entry.grid(row=9, column=1, padx=5, pady=5, sticky=tk.W)
        #self.open_drower_label.grid(row=10, column=0, padx=5, pady=5, sticky=tk.E)
        #self.markaspad_label.grid(row=11, column=0, padx=5, pady=5, sticky=tk.E)
        
        self.add_button.grid(row=12, column=0, padx=5, pady=5, sticky=tk.W)
        self.cancle_button.grid(row=12, column=1, padx=5, pady=5, sticky=tk.W)
        self.update_tool_listbox()
        
    def show_tools_form(self):
        # call the function in the main file to show the first frame
        self.master.master.show_frame("ToolForm")
    
    def clear_tool_details_widget(self):
        # Clear the product details widgets
        self.name_entry.delete(0, tk.END)
        self.code_entry.delete(0, tk.END)
        self.type_entry.set('')
        self.short_key_entry.delete(0, tk.END)
        self.acsess_entry.delete(0, tk.END)
        self.enable_label.set(0)
        self.quick_pay_label.set(0)
        self.customer_required_label.set(0)
        self.print_slip_label.set(0)
        self.change_allowed_label.set(0)
        self.markaspad_label.set(0)
        self.open_drower_label.set(0)
        
    # Create the "Add New" button
    def show_add_forme(self):
        self.clear_tool_details_widget()
        self.on_name_entry(None)
        self.details_frame.pack(side=tk.RIGHT, fill=tk.Y, expand=False)
        
    def hide_add_forme(self):
        self.clear_tool_details_widget()
        self.details_frame.forget()

    # Create the "Change" button
    def show_change_forme(self):
        selected_product = self.list_box.selection()
        if selected_product:
            # Get the ID of the selected product
            # "Tool Name", "Tool Method", "Tool ID", "Tool Short cut", "Tool Acsess key", "Tool enabel", "Tool Quick_pay","Tool Markpad", "Tool Customer_required", "Tool Open_drower", "Tool Printslip"
            shop_id = self.list_box.item(selected_product)['text']
            shop_name, list_id, name, typ, code, short_key, acsess, enable, \
                quick_pay, markaspad, customer_required, open_drower, print_slip, change_allowed = self.list_box.item(selected_product)['values']
            self.selected_shop_id = shop_id
            self.selected_shop_name = shop_name
            self.selected_id = list_id
            
            # Clear the current text
            # than add new one
            self.name_entry.delete(0, "end")
            self.name_entry.insert(0, name)
            self.main_name = name
            self.code_entry.delete(0, "end")
            self.code_entry.insert(0, code)
            self.type_entry.set(typ)
            self.short_key_entry.delete(0, "end")
            self.short_key_entry.insert(0, short_key)
            self.acsess_entry.delete(0, "end")
            self.acsess_entry.insert(0, acsess)
            self.enable_label.set(int(enable))
            self.quick_pay_label.set(int(quick_pay))
            self.customer_required_label.set(int(customer_required))
            self.print_slip_label.set(int(print_slip))
            self.change_allowed_label.set(int(change_allowed))
            self.open_drower_label.set(int(open_drower))
            self.markaspad_label.set(int(markaspad))
            self.add_button.config(text="Update")
            # Commit the changes to the database
            conn.commit()
            self.details_frame.pack(side=tk.RIGHT, fill=tk.Y, expand=False)
    
    def search_tools(self, search_text):        
        # Search for the entered text in the code, name, short_key, and type fields of the product table
        results = []
        for Shop_Payment_Tool in self.Shop_Payment_Tools:
            if search_text in str(Shop_Payment_Tool):
                results.append(Shop_Payment_Tool)
        return results

    def Add_tool_listbox(self, results):
        print("update_search :"+str(results))
        self.list_box['columns'] = ("Shop ID", "Shop Name", "Tool Name", "Tool Method", "Tool ID", "Tool Short cut", "Tool Acsess key", "Tool enabel", "Tool Quick_pay","Tool Markpad", "Tool Customer_required", "Tool Open_drower", "Tool Printslip")
        self.list_box.heading("#0", text="Shop ID")
        self.list_box.heading("#1", text="Shop Name")
        self.list_box.heading("#2", text="Tool Name")
        self.list_box.heading("#3", text="Tool Method")
        self.list_box.heading("#4", text="Tool ID")
        self.list_box.heading("#5", text="Tool Short cut")
        self.list_box.heading("#6", text="Tool Acsess key")
        self.list_box.heading("#7", text="Tool enabel")
        self.list_box.heading("#8", text="Tool Quick_pay")
        self.list_box.heading("#9", text="Tool Markpad")
        self.list_box.heading("#10", text="Tool Customer_required")
        self.list_box.heading("#11", text="Tool Open_drower")
        self.list_box.heading("#12", text="Tool Printslip")

        # Add the products to the product listbox
        for product in results:
            self.list_box.insert('', 'end', text=product[0], values=(product[1], product[2], product[3], product[4], product[5], product[6], product[7], product[8], product[9], product[10], product[11], product[12], product[13], product[14]))
        self.master.master.master.master.create_payment_buttons()

    # create a function to update the search results whenever the search box changes
    def update_search_results(self, *args):
        # get the search string from the search box
        search_str = self.search_var.get()
        
        # search for products based on the search string
        results = self.search_tools(search_str) 
        # clear the current items in the list box
        self.list_box.delete(*self.list_box.get_children())
        self.Add_tool_listbox(results)
        
    # Define the function for updating the product listbox
    def update_tool_listbox(self):
        # Clear the product listbox
        self.list_box.delete(*self.list_box.get_children())
        self.Shop_Payment_Tools = []
        results = []
        for s, shop in enumerate(self.Shops):
            if self.Selected_Shop != "" and shop['Shop_name'] != self.Selected_Shop:
                continue

            Shop = fetch_as_dict_list(cur, "SELECT * FROM Shops WHERE Shop_id=? AND Shop_name=? AND Shop_brand_name=?", 
                                (str(shop['Shop_id']), str(shop['Shop_name']), str(shop['Shop_brand_name'])))
            if Shop and Shop[0] and Shop[0]['Shop_Payment_Tools'] and Shop[0]['Shop_Payment_Tools'] != "":
                print("Shop[0]['Shop_Payment_Tools'] ", Shop[0]['Shop_Payment_Tools'])
                Shop_Payment_Tools = load_list(Shop[0]['Shop_Payment_Tools'])
                
                # Add the products to the product listbox
                for Shop_Payment_Tool in Shop_Payment_Tools:
                    self.Shop_Payment_Tools.append(Shop_Payment_Tool)
                    results.append([shop['Shop_id'], shop['Shop_name']] + [len(self.Shop_Payment_Tools)-1] + Shop_Payment_Tool)
        self.Add_tool_listbox(results)
        # Hide the product details frame
        self.hide_add_forme()
        self.change_button.config(state=tk.DISABLED)

    # Define the function for adding a new product
    def add_tool(self):
        # Get the values from the product details widgets
        #self.selected_shop_id = shop_id
        #self.selected_shop_name = shop_name
        #self.selected_id = list_id

        name = self.name_entry.get()
        code = self.code_entry.get()
        # get combobox selection (value). If empty, try current index as fallback
        typ = self.type_entry.get().strip()
        if not typ:
            idx = self.type_entry.current()
            if idx != -1:
                vals = self.type_entry['values']
            try:
                typ = vals[idx]
            except Exception:
                typ = ''
        short_key = self.short_key_entry.get()
        acsess = self.acsess_entry.get()
        enable = self.enable_label.get()
        quick_pay = self.quick_pay_label.get()
        customer_required = self.customer_required_label.get()
        print_slip = self.print_slip_label.get()
        change_allowed = self.change_allowed_label.get()
        open_drower = self.open_drower_label.get()
        markaspad = self.markaspad_label.get()
        for s, shop in enumerate(self.Shops):
            Shop_Payment_Tools = []
            if self.Selected_Shop != "" and shop['Shop_name'] != self.Selected_Shop:
                continue
            if shop:
                if shop['Shop_Payment_Tools'] and shop['Shop_Payment_Tools'] != "":
                    Shop_Payment_Tools = load_list(shop['Shop_Payment_Tools']) 
                
                if self.add_button.cget("text") == "New":
                    # "Tool Name", "Tool Method", "Tool ID", "Tool Short cut", "Tool Acsess key", "Tool enabel", "Tool Quick_pay","Tool Markpad", "Tool Customer_required", "Tool Open_drower", "Tool Printslip"
                    Shop_Payment_Tools.append([name, typ, code, short_key, acsess, enable, quick_pay , markaspad, customer_required, open_drower, print_slip, change_allowed])
                    cur.execute("UPDATE Shops SET Shop_Payment_Tools=? WHERE Shop_id=? AND Shop_name=? AND Shop_brand_name=?", 
                                    (json.dumps(Shop_Payment_Tools), str(shop['Shop_id']), str(shop['Shop_name']), str(shop['Shop_brand_name'])))
                    # Commit the changes to the database
                    conn.commit()
                    self.master.master.master.master.Shop_Payment_Tools = Shop_Payment_Tools
                else:
                    Shop0 = fetch_as_dict_list(cur, "SELECT * FROM Shops WHERE Shop_id=? AND Shop_name=?", 
                                        (str(self.selected_shop_id), str(self.selected_shop_name)))
                    if Shop0 and Shop0[0] and Shop0[0]['Shop_Payment_Tools'] and Shop0[0]['Shop_Payment_Tools'] != "":
                        
                        Shop_Payment_Tools = load_list(Shop0[0]['Shop_Payment_Tools'])

                        if int(self.selected_id) <= len(Shop_Payment_Tools):
                            # "Tool Name", "Tool Method", "Tool ID", "Tool Short cut", "Tool Acsess key", "Tool enabel", "Tool Quick_pay","Tool Markpad", "Tool Customer_required", "Tool Open_drower", "Tool Printslip"
                            Shop_Payment_Tools[int(self.selected_id)] = [name, typ, code, short_key, acsess, enable, quick_pay , markaspad, customer_required, open_drower, print_slip, change_allowed]

                        print("Shop_Payment_Tools ", Shop_Payment_Tools)
                        cur.execute("UPDATE Shops SET Shop_Payment_Tools=? WHERE Shop_id=? AND Shop_name=? AND Shop_brand_name=?", 
                                    (json.dumps(Shop_Payment_Tools), str(shop['Shop_id']), str(shop['Shop_name']), str(shop['Shop_brand_name'])))
                        # Commit the changes to the database
                        conn.commit()
                        self.master.master.master.master.Shop_Payment_Tools = Shop_Payment_Tools
                                
        self.master.master.master.master.create_payment_buttons()
        # Update the product listbox
        self.update_tool_listbox()
        
    # Define the function for deleting a product
    def delete_tool(self):
        # Get the selected product from the listbox
        selected_product = self.list_box.selection()
        
        if selected_product:
            # Determine shop id/name and index from the selected item (robust to small variations)
            shop_id_text = self.list_box.item(selected_product)['text']
            values = self.list_box.item(selected_product)['values']
            # values is expected like: (shop_name, list_id, name, typ, ...)
            idx = None
            try:
                idx = int(values[1])               # preferred: list_id at values[1]
            except Exception:
                try:
                    idx = int(values[2])           # fallback: maybe index is at values[2]
                except Exception:
                    idx = None

            if idx is None:
                # couldn't determine index, abort deletion
                pass
            else:
                # Find matching shop in self.Shops and remove the tool at idx
                for s, shop in enumerate(self.Shops):
                    if self.Selected_Shop != "" and shop['Shop_name'] != self.Selected_Shop:
                        continue
                    if str(shop['Shop_id']) != str(shop_id_text):
                        continue
                    # load existing tools
                    Shop_Payment_Tools = []
                    if shop and shop.get('Shop_Payment_Tools') and shop['Shop_Payment_Tools'] != "":
                        Shop_Payment_Tools = json.loads(shop['Shop_Payment_Tools'])
                    # remove if index valid
                    try:
                        if 0 <= int(idx) < len(Shop_Payment_Tools):
                            Shop_Payment_Tools.pop(int(idx))
                            cur.execute("UPDATE Shops SET Shop_Payment_Tools=? WHERE Shop_id=? AND Shop_name=? AND Shop_brand_name=?",
                                        (json.dumps(Shop_Payment_Tools), str(shop['Shop_id']), str(shop['Shop_name']), str(shop['Shop_brand_name'])))
                            conn.commit()
                            self.master.master.master.master.Shop_Payment_Tools = Shop_Payment_Tools
                    except Exception:
                        # ignore errors and continue
                        pass
                    break
            # Clear the product details widgets
            self.clear_tool_details_widget()

            self.master.master.master.master.create_payment_buttons()
            # Update the product listbox
            self.update_tool_listbox()












    def on_name_entry(self, event):
        cur.execute('SELECT * FROM tools')
        products = cur.fetchall()
        for product in products:
            if product[1] == self.name_entry.get():
                self.add_button.config(text="Update")    
                return
        if self.main_name == self.name_entry.get() and not self.main_name == "":
            self.add_button.config(text="Update")
        else:
            self.add_button.config(text="New")

    
        

     

    def on_select(self, event):
        print("onselect")
        if len(event.widget.selection()) > 0:
            self.change_button.config(state=tk.NORMAL)
            self.delete_button.config(state=tk.NORMAL)
        else:
            self.change_button.config(state=tk.DISABLED)
            self.delete_button.config(state=tk.DISABLED)

