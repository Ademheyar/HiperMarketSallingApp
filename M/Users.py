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

class UserForm(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)

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
        self.type_label = tk.Label(self.details_frame, text='TYPE:')
        self.type_entry = tk.Entry(self.details_frame)
        self.phone_num_label = tk.Label(self.details_frame, text='PHONE NUMBER:')
        self.phone_num_entry = tk.Entry(self.details_frame)
        self.email_label = tk.Label(self.details_frame, text='EMAIL:')
        self.email_entry = tk.Entry(self.details_frame)
        self.id_num_label = tk.Label(self.details_frame, text='ID Number:')
        self.id_num_entry = tk.Entry(self.details_frame)
        self.addres_label = tk.Label(self.details_frame, text='Addres:')
        self.addres_entry = tk.Entry(self.details_frame)
        self.acsess_label = tk.Label(self.details_frame, text='ACSSES:')
        self.acsess_entry = tk.Entry(self.details_frame)


        self.add_button = tk.Button(self.details_frame, text='Add', command=self.add_product)
        self.cancle_button = tk.Button(self.details_frame, text='Cancle', command=self.hide_add_product_forme)


        self.add_searchbutton = tk.Button(self.search_frame, text='Add New user', command=self.show_add_product_forme)
        self.add_searchbutton.pack(side=tk.LEFT, padx=5, pady=5)

        self.change_button = tk.Button(self.search_frame, text='Change', command=self.show_change_product_forme)
        self.change_button.pack(side=tk.LEFT, padx=5, pady=5)
        self.change_button.config(state=tk.DISABLED)

        self.delete_button = tk.Button(self.search_frame, text='Delete', command=self.delete_product)
        self.delete_button.pack(side=tk.LEFT, padx=5, pady=5)


        # Pack the widgets for the product details
        self.name_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.E)
        self.name_entry.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)
        self.type_label.grid(row=5, column=0, padx=5, pady=5, sticky=tk.E)
        self.type_entry.grid(row=5, column=1, padx=5, pady=5, sticky=tk.W)
        self.phone_num_label.grid(row=3, column=0, padx=5, pady=5, sticky=tk.E)
        self.phone_num_entry.grid(row=3, column=1, padx=5, pady=5, sticky=tk.W)
        self.email_label.grid(row=4, column=0, padx=5, pady=5, sticky=tk.E)
        self.email_entry.grid(row=4, column=1, padx=5, pady=5, sticky=tk.W)
        self.id_num_label.grid(row=2, column=0, padx=5, pady=5, sticky=tk.E)
        self.id_num_entry.grid(row=2, column=1, padx=5, pady=5, sticky=tk.W)
        self.addres_label.grid(row=1, column=0, padx=5, pady=5, sticky=tk.E)
        self.addres_entry.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)
        self.acsess_label.grid(row=6, column=0, padx=5, pady=5, sticky=tk.E)
        self.acsess_entry.grid(row=6, column=1, padx=5, pady=5, sticky=tk.W)

        self.add_button.grid(row=17, column=0, padx=5, pady=5, sticky=tk.W)
        self.cancle_button.grid(row=17, column=1, padx=5, pady=5, sticky=tk.W)
        self.update_product_listbox()

    def show_user_form(self):
        # call the function in the main file to show the first frame
        self.master.master.show_frame("UserForm")
        
    def search_products(search_text):
        
        # Search for the entered text in the addres, name, phone_num, and type fields of the product table
        cur.execute("SELECT * FROM product WHERE addres LIKE ? OR name LIKE ? OR phone_num LIKE ? OR type LIKE ?", 
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
        
    def clear_product_details_widget():
        # Clear the product details widgets
        self.name_entry.delete(0, tk.END)
        self.type_entry.delete(0, tk.END)
        self.phone_num_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)
        self.id_num_entry.delete(0, tk.END)
        self.addres_entry.delete(0, tk.END)
        self.acsess_entry.delete(0, tk.END)
        active_var.set(0)
        
    # Create the "Add New" button
    def show_add_product_forme(self):
        self.details_frame.pack(side=tk.RIGHT, fill=tk.Y, expand=False)

    def hide_add_product_forme(self):
        self.details_frame.forget()
        self.clear_product_details_widget()

    # Create the "Change" button
    def show_change_product_forme():
        self.details_frame.pack(side=tk.RIGHT, fill=tk.Y, expand=False)

    def on_select(self,event):
        if len(event.widget.curselection()) > 0:
            self.change_button.config(state=tk.NORMAL)
        else:
            self.change_button.config(state=tk.DISABLED)

    # Create the "Delete" button
    def delete_product():
        # TODO: Implement the addres to delete a product
        pass

    # Define the function for hiding the product details frame
    def hide_product_details_frame(self):
        pass
        # Hide the product details frame
        #product_details_frame.grid_remove()

        # Show the add product button
        #add_product_button.grid()

    # Define the function for updating the product listbox
    def update_product_listbox(self):
        # Clear the product listbox
        self.list_box.delete(*self.list_box.get_children())

        # Get the products from the database
        cur.execute('SELECT * FROM USERS')
        products = cur.fetchall()
        self.list_box['columns'] = ('Name', 'Type', 'Phone_Number', 'Id_Number', 'Email', 'Adress')
        self.list_box.heading("#0", text="ID")
        self.list_box.heading("#1", text="Name")
        self.list_box.heading("#2", text="Type")
        self.list_box.heading("#3", text="Phone_Number")
        self.list_box.heading("#4", text="Id_Number")
        self.list_box.heading("#4", text="Email")
        self.list_box.heading("#4", text="Adress")

        # Add the products to the product listbox
        for product in products:
            self.list_box.insert('', 'end', text=product[0], values=(product[1], product[2], product[3], product[4], product[5], product[6]))

        # Hide the product details frame
        self.hide_product_details_frame()
        self.change_button.config(state=tk.DISABLED)

    # Define the function for adding a new product
    def add_product():
        # Get the values from the product details widgets
        name = self.name_entry.get()
        typ = self.type_entry.get()
        email = self.email_entry.get()
        phone_num = self.phone_num_entry.get()
        id_num = self.id_num_entry.get()
        addres = self.addres_entry.get()
        acsess = self.acsess_entry.get()

        # Insert the new product into the database
        cur.execute('INSERT INTO USERS (name, type, addres, email, phone_num, id_num, adress, acsess) VALUES (?, ?, ?, ?, ?, ?, ?, ?)', (name, type, addres, email, phone_num, id_num, adress, acsess))
        
        # Commit the changes to the database
        conn.commit()
        
        # Clear the product details widgets
        clear_product_details_widget()
        
        # Update the product listbox
        update_product_listbox()

    # Define the function for changing an existing product
    def change_product():
        # Get the selected product from the listbox
        selected_product = product_listbox.curselection()
        
        if selected_product:
            # Get the values from the product details widgets
            name = self.name_entry.get()
            typ = self.type_entry.get()
            email = self.email_entry.get()
            phone_num = self.phone_num_entry.get()
            id_num = self.id_num_entry.get()
            addres = self.addres_entry.get()
            acsess = self.acsess_entry.get()

            # Get the ID of the selected product
            user_id = self.product_listbox.get(selected_product)[0]

            # Update the product in the database
            cur.execute('UPDATE USERS SET name=?, type=?, addres=?, email=?, phone_num=?, id_num=?, adress=?, acsess=?) WHERE id=?', (name, type, addres, email, phone_num, id_num, adress, acsess, user_id))

            # Commit the changes to the database
            conn.commit()

            # Clear the product details widgets
            clear_product_details_widget()
            # Update the product listbox
            update_product_listbox()

    # Define the function for deleting a product
    def delete_product():
        # Get the selected product from the listbox
        selected_product = self.product_listbox.curselection()
        
        if selected_product:
            # Get the ID of the selected product
            product_id = self.product_listbox.get(selected_product)[0]

            # Delete the product from the database
            cur.execute('DELETE FROM USERS WHERE id=?', (product_id,))

            # Commit the changes to the database
            conn.commit()

            # Clear the product details widgets
            clear_product_details_widget()

            # Update the product listbox
            update_product_listbox()

    # Define the function for showing the product details frame
    def show_product_details_frame():
        # Show the product details frame
        product_details_frame.grid(row=0, column=1, sticky='nsew')

        # Hide the add product button
        add_product_button.grid_remove()

        # Clear the product details widgets
        clear_product_details_widget()

    # Define the function for updating an existing product
    def update_product():
        # Get the values from the product details widgets
        name = self.name_entry.get()
        typ = self.type_entry.get()
        email = self.email_entry.get()
        phone_num = self.phone_num_entry.get()
        id_num = self.id_num_entry.get()
        addres = self.addres_entry.get()
        acsess = self.acsess_entry.get()

        # Update the product in the database
        cur.execute('UPDATE USERS SET name=?, type=?, addres=?, email=?, phone_num=?, id_num=?, adress=?, acsess=?) WHERE id=?', (name, type, addres, email, phone_num, id_num, adress, acsess, user_id))

        conn.commit()

        # Clear the product details widgets
        clear_product_details_widgets()

        # Update the product listbox
        update_product_listbox()

        # Hide the product details frame
        hide_product_details_frame()