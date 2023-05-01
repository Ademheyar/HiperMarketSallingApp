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
class ToolForm(tk.Frame):
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

        # Create the list box
        self.list_box = ttk.Treeview(self)
        self.list_box.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.list_box.bind('<<ListboxSelect>>', self.on_select)

        # Create the frame for the product details
        self.details_frame = tk.Frame(self.list_box)
        self.details_frame.pack_forget()

        # Create the widgets for the product details
        self.name_label = tk.Label(self.details_frame, text='Name:')
        self.name_entry = tk.Entry(self.details_frame)
        self.code_label = tk.Label(self.details_frame, text='Code:')
        self.code_entry = tk.Entry(self.details_frame)
        self.type_label = tk.Label(self.details_frame, text='Type:')
        self.type_entry = tk.Entry(self.details_frame)
        self.short_key_label = tk.Label(self.details_frame, text='short_key:')
        self.short_key_entry = tk.Entry(self.details_frame)
        self.acsess_label = tk.Label(self.details_frame, text='acsess:')
        self.acsess_entry = tk.Entry(self.details_frame)
        self.enable_label = tk.IntVar()
        self.enable_entry = tk.Checkbutton(self.details_frame, text='enable:', variable=self.enable_label)
        self.quick_pay_label = tk.IntVar()
        self.quick_pay_entry = tk.Checkbutton(self.details_frame, text='Quick payment:', variable=self.quick_pay_label)
        self.customer_required_label = tk.IntVar()
        self.customer_required_entry = tk.Checkbutton(self.details_frame, text='Customer Required:', variable=self.customer_required_label)
        self.print_slip_label = tk.IntVar()
        self.print_slip_entry = tk.Checkbutton(self.details_frame, text='Print Receiipt:', variable=self.print_slip_label)
        self.change_allowed_label = tk.IntVar()
        self.change_allowed_entry = tk.Checkbutton(self.details_frame, text='Change Allowed:', variable=self.change_allowed_label)
        self.markaspad_label = tk.IntVar()
        self.markaspad_entry = tk.Checkbutton(self.details_frame, text='mark As pad:', variable=self.markaspad_label)
        self.open_drower_label = tk.IntVar()
        self.open_drower_entry = tk.Checkbutton(self.details_frame, text='Open cahs Drawer:', variable=self.open_drower_label)
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
        #self.customer_required_label.grid(row=7, column=0, padx=5, pady=5, sticky=tk.W)
        self.customer_required_entry.grid(row=7, column=1, padx=5, pady=5, sticky=tk.W)
        #self.print_slip_label.grid(row=8, column=0, padx=5, pady=5, sticky=tk.E)
        self.print_slip_entry.grid(row=8, column=1, padx=5, pady=5, sticky=tk.W)
        #self.change_allowed_label.grid(row=9, column=0, padx=5, pady=5, sticky=tk.W)
        self.change_allowed_entry.grid(row=9, column=1, padx=5, pady=5, sticky=tk.W)
        #self.open_drower_label.grid(row=10, column=0, padx=5, pady=5, sticky=tk.E)
        self.open_drower_entry.grid(row=10, column=1, padx=5, pady=5, sticky=tk.W)
        #self.markaspad_label.grid(row=11, column=0, padx=5, pady=5, sticky=tk.E)
        self.markaspad_entry.grid(row=11, column=1, padx=5, pady=5, sticky=tk.W)
        
        self.add_button.grid(row=12, column=0, padx=5, pady=5, sticky=tk.W)
        self.cancle_button.grid(row=12, column=1, padx=5, pady=5, sticky=tk.W)
        self.update_tool_listbox()


    def show_tools_form(self):
        # call the function in the main file to show the first frame
        self.master.master.show_frame("ToolForm")
        
    def search_products(search_text):
        
        # Search for the entered text in the code, name, short_key, and type fields of the product table
        cur.execute("SELECT * FROM tools WHERE code LIKE ? OR name LIKE ? OR short_key LIKE ? OR type LIKE ?", 
                    ('%' + search_text + '%', '%' + search_text + '%', '%' + search_text + '%', '%' + search_text + '%'))
        results = cur.fetchall()
        
        return results
        

    # create a function to update the search results whenever the search box changes
    def update_search_results(*args):
        # get the search string from the search box
        search_str = self.search_var.get()
        
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
        
    def clear_tool_details_widget(self):
        # Clear the product details widgets
        self.name_entry.delete(0, tk.END)
        self.code_entry.delete(0, tk.END)
        self.type_entry.delete(0, tk.END)
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
        self.details_frame.pack(side=tk.RIGHT, fill=tk.Y, expand=False)
    def hide_add_forme(self):
        self.details_frame.forget()
        self.clear_details_widget()

    # Create the "Change" button
    def show_change_forme(self):
        self.details_frame.pack(side=tk.RIGHT, fill=tk.Y, expand=False)

    def on_select(self, event):
        if len(event.widget.curselection()) > 0:
            self.change_button.config(state=tk.NORMAL)
            self.delete_button.config(state=tk.NORMAL)
        else:
            self.change_button.config(state=tk.DISABLED)
            self.delete_button.config(state=tk.DISABLED)

    # Create the "Delete" button
    def delete_product():
        # TODO: Implement the code to delete a product
        pass

    # Define the function for hiding the product details frame
    def hide_product_details_frame(self):
        pass
        # Hide the product details frame
        #product_details_frame.grid_remove()

        # Show the add product button
        #add_product_button.grid()

    # Define the function for updating the product listbox
    def update_tool_listbox(self):
        # Clear the product listbox
        self.list_box.delete(*self.list_box.get_children())

        # Get the products from the database
        cur.execute('SELECT * FROM tools')
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
    def add_tool(self):
        # Get the values from the product details widgets
        name = self.name_entry.get()
        code = self.code_entry.get()
        typ = self.type_entry.get()
        short_key = self.short_key_entry.get()
        acsess = self.acsess_entry.get()
        enable = self.enable_label.get()
        quick_pay = self.quick_pay_label.get()
        customer_required = self.customer_required_label.get()
        print_slip = self.print_slip_label.get()
        change_allowed = self.change_allowed_label.get()
        open_drower = self.open_drower_label.get()
        markaspad = self.markaspad_label.get()

        # Insert the new product into the database
        cur.execute('INSERT INTO tools (name, code, type, short_key, acsess, enabel, quick_pay, customer_required, printslip, change_allowed, markpad, open_drower) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (name, code, typ, short_key, acsess, enable, quick_pay , customer_required, print_slip, change_allowed, markaspad, open_drower))
        
        # Commit the changes to the database
        conn.commit()

        # Clear the product details widgets
        self.clear_tool_details_widget()
        
        # Update the product listbox
        self.update_tool_listbox()

    # Define the function for changing an existing product
    def change_product():
        # Get the selected product from the listbox
        selected_product = product_listbox.curselection()
        
        if selected_product:
            # Get the values from the product details widgets
            name = self.name_entry.get()
            code = self.code_entry.get()
            type = self.type_entry.get()
            short_key = self.short_key_entry.get()
            acsess = self.acsess_entry.get()
            enable = self.enable_label.get()
            open_drower = self.open_drower_label.get()
            print_slip = self.print_slip_label.get()
            markaspad = self.markaspad_label.get()


            # Get the ID of the selected product
            product_id = product_listbox.get(selected_product)[0]

            # Update the product in the database
            cur.execute('UPDATE tools SET name=?, code=?, type=?, short_key=?, acsess=?, enable=?, open_drower=?, print_slip=?, markaspad=?, include_print_slip=?, markaspad_change=?, more_info=?, images=?, description=?, service=?, default_enable=?, active=? WHERE id=?', (name, code, type, short_key, acsess, enable, open_drower, print_slip, markaspad, include_print_slip, markaspad_change, more_info, images, description, service, default_enable, active, product_id))

            # Commit the changes to the database
            conn.commit()

            # Clear the product details widgets
            clear_tool_details_widget()
            # Update the product listbox
            update_tool_listbox()

    # Define the function for deleting a product
    def delete_tool():
        # Get the selected product from the listbox
        selected_product = product_listbox.curselection()
        
        if selected_product:
            # Get the ID of the selected product
            product_id = product_listbox.get(selected_product)[0]

            # Delete the product from the database
            cur.execute('DELETE FROM tools WHERE id=?', (product_id,))

            # Commit the changes to the database
            conn.commit()

            # Clear the product details widgets
            clear_tool_details_widget()

            # Update the product listbox
            update_tool_listbox()

    # Define the function for showing the product details frame
    def show_product_details_frame():
        # Show the product details frame
        product_details_frame.grid(row=0, column=1, sticky='nsew')

        # Hide the add product button
        add_product_button.grid_remove()

        # Clear the product details widgets
        clear_tool_details_widget()

    # Define the function for updating an existing product
    def update_product():
        # Get the values from the product details widgets
        name = self.name_entry.get()
        code = self.code_entry.get()
        type = self.type_entry.get()
        short_key = self.short_key_entry.get()
        acsess = self.acsess_entry.get()
        enable = self.enable_label.get()
        open_drower = self.open_drower_label.get()
        print_slip = self.print_slip_label.get()
        

        # Update the product in the database
        cur.execute('UPDATE tools SET name=?, code=?, type=?, short_key=?, acsess=?, enable=?, open_drower=?, print_slip=?, markaspad=?, include_print_slip=?, markaspad_change=?, more_info=?, images=?, description=?, service=?, default_enable=?, active=? WHERE id=?', (name, code, type, short_key, acsess, enable, open_drower, print_slip, markaspad, include_print_slip, markaspad_change, more_info, images, description, service, default_enable, active, selected_product_id))
        conn.commit()

        # Clear the product details widgets
        self.clear_tool_details_widgets()

        # Update the product listbox
        self.update_tool_listbox()

        # Hide the product details frame
        self.hide_product_details_frame()