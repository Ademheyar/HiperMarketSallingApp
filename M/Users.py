import tkinter as tk
from tkinter import ttk
import sqlite3
import json

# Connect to the database or create it if it does not exist

import os
data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data'))
db_path = os.path.join(data_dir, 'my_database.db')
import os, sys
current_dir = os.path.abspath(os.path.dirname(__file__))
MAIN_dir = os.path.join(current_dir, '..')
sys.path.append(MAIN_dir)
from D.docediterform import DocEditForm
from D.printer import PrinterForm
from C.slipe import load_slip

from C.API.Get import *
from C.API.API import *
from C.API.Set import *

class UserForm(tk.Frame):
    def __init__(self, parent, user_info):
        tk.Frame.__init__(self, parent)
        self.user_info = user_info
        # Create the search bar
        # Create the frame for the search bar and buttons
        self.search_frame = tk.Frame(self)
        self.search_frame.pack(side=tk.TOP, padx=5, pady=5)

        # create a StringVar to represent the search box
        self.search_var = tk.StringVar()
        self.search_entry = tk.Entry(self.search_frame, textvariable=self.search_var)
        #self.search_entry.bind('<KeyRelease>', self.update_search_results)
        self.search_entry.pack(side=tk.LEFT, padx=5, pady=5)
            
        # bind the update_search_results function to the search box
        self.search_var.trace("w", self.update_search_results)


        # Create the list box
        self.list_box = ttk.Treeview(self)
        self.list_box.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.list_box.bind('<<TreeviewSelect>>', self.on_select)

        self.userinfo_notebook = ttk.Notebook(self.list_box)
        self.userinfo_notebook.pack_forget()
        self.nested_list = []

        # Create the frame for the user details
        self.details_frame = tk.Frame(self.userinfo_notebook)
        self.details_frame.pack()
        self.userinfo_notebook.add(self.details_frame, text="info")

        # Create the widgets for the user details
        self.name_label = tk.Label(self.details_frame, text='Name:')
        self.name_entry = tk.Entry(self.details_frame)
        self.main_name = ""
        self.name_entry.bind('<KeyRelease>', lambda: self.on_name_entry)
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
        
        self.f_and_lname_label = tk.Label(self.details_frame, text='First and Last Name :')
        self.fname_entry = tk.Entry(self.details_frame)
        self.lname_entry = tk.Entry(self.details_frame)
        self.name_label = tk.Label(self.details_frame, text='User Name :')
        self.name_entry = tk.Entry(self.details_frame)
        self.gender_label = tk.Label(self.details_frame, text='Gender :')
        self.gender_entry = tk.Entry(self.details_frame)
        self.cuntry_label = tk.Label(self.details_frame, text='Cuntry :')
        self.cuntry_entry = tk.Entry(self.details_frame)
        self.phone_num_label = tk.Label(self.details_frame, text='Phone No :')
        self.phone_num_entry = tk.Entry(self.details_frame)
        self.email_label = tk.Label(self.details_frame, text='Email :')
        self.email_entry = tk.Entry(self.details_frame)
        self.addres_label = tk.Label(self.details_frame, text='Adress :')
        self.addres_entry = tk.Entry(self.details_frame)
        self.id_num_label = tk.Label(self.details_frame, text='Id No :')
        self.id_num_entry = tk.Entry(self.details_frame)
        self.home_no_label = tk.Label(self.details_frame, text='Home No :')
        self.home_no_entry = tk.Entry(self.details_frame)
        self.type_label = tk.Label(self.details_frame, text='Type :')
        self.type_entry = tk.Entry(self.details_frame)
        self.password_num_label = tk.Label(self.details_frame, text='Password :')
        # mask password by default
        self.password_num_entry = tk.Entry(self.details_frame, show='*')

        # Checkbox to toggle password visibility
        self.show_password_var = tk.IntVar(value=0)
        def _toggle_password_visibility():
            if self.show_password_var.get():
                self.password_num_entry.config(show='')
            else:
                self.password_num_entry.config(show='*')
        self.show_password_cb = tk.Checkbutton(self.details_frame, text='Show Password', variable=self.show_password_var, command=_toggle_password_visibility)
        # place the checkbox (same row as password, different column)
        self.show_password_cb.grid(row=10, column=2, padx=5, pady=5, sticky=tk.W)
        self.about_label = tk.Label(self.details_frame, text='About :')
        self.about_entry = tk.Entry(self.details_frame)
        
        self.shops_label = tk.Label(self.details_frame, text='Shop :')
        self.shops_entry = tk.Entry(self.details_frame)
        self.work_shop_label = tk.Label(self.details_frame, text='Work Shop :')
        self.work_shop_entry = tk.Label(self.details_frame)
        self.acsess_label = tk.Label(self.details_frame, text='ACSSES :')
        self.acsess_entry = tk.Entry(self.details_frame)
        self.pimg_label = tk.Label(self.details_frame, text='Image :')
        self.pimg_entry = tk.Entry(self.details_frame)
        

        self.add_button = tk.Button(self.details_frame, text='Add', command=self.add_user)
        self.cancle_button = tk.Button(self.details_frame, text='Cancle', command=self.hide_user_details_frame)




        # Create the frame for the user details
        self.doc_details_frame = tk.Frame(self.userinfo_notebook)
        self.doc_details_frame.pack()
        self.userinfo_notebook.add(self.doc_details_frame, text="Doc info")

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

        # Create the search button
        self.print_button = tk.Button(self.userinfo_notebook, text="Print", command=self.perform_print)
        self.print_button.pack()#.grid(row=2, column=0)


        self.add_searchbutton = tk.Button(self.search_frame, text='Add New user', command=self.show_user_details_frame)
        self.add_searchbutton.pack(side=tk.LEFT, padx=5, pady=5)

        self.change_button = tk.Button(self.search_frame, text='Change', command=self.show_change_forme)
        self.change_button.pack(side=tk.LEFT, padx=5, pady=5)
        self.change_button.config(state=tk.DISABLED)

        self.delete_button = tk.Button(self.search_frame, text='Delete', command=self.delete_user)
        self.delete_button.pack(side=tk.LEFT, padx=5, pady=5)
        self.delete_button.config(state=tk.DISABLED)


        # Pack the widgets for the user details
        self.f_and_lname_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.E)
        self.fname_entry.grid(row=0, column=1, padx=5, pady=5, sticky=tk.E)
        self.lname_entry.grid(row=0, column=2, padx=5, pady=5, sticky=tk.W)
        self.name_label.grid(row=1, column=0, padx=5, pady=5, sticky=tk.E)
        self.name_entry.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)
        self.gender_label.grid(row=2, column=0, padx=5, pady=5, sticky=tk.E)
        self.gender_entry.grid(row=2, column=1, padx=5, pady=5, sticky=tk.W)
        self.cuntry_label.grid(row=3, column=0, padx=5, pady=5, sticky=tk.E)
        self.cuntry_entry.grid(row=3, column=1, padx=5, pady=5, sticky=tk.W)
        self.phone_num_label.grid(row=4, column=0, padx=5, pady=5, sticky=tk.E)
        self.phone_num_entry.grid(row=4, column=1, padx=5, pady=5, sticky=tk.W)
        self.email_label.grid(row=5, column=0, padx=5, pady=5, sticky=tk.E)
        self.email_entry.grid(row=5, column=1, padx=5, pady=5, sticky=tk.W)
        self.addres_label.grid(row=6, column=0, padx=5, pady=5, sticky=tk.E)
        self.addres_entry.grid(row=6, column=1, padx=5, pady=5, sticky=tk.W)
        self.id_num_label.grid(row=7, column=0, padx=5, pady=5, sticky=tk.E)
        self.id_num_entry.grid(row=7, column=1, padx=5, pady=5, sticky=tk.W)
        self.home_no_label.grid(row=8, column=0, padx=5, pady=5, sticky=tk.E)
        self.home_no_entry.grid(row=8, column=1, padx=5, pady=5, sticky=tk.W)
        self.type_label.grid(row=9, column=0, padx=5, pady=5, sticky=tk.E)
        self.type_entry.grid(row=9, column=1, padx=5, pady=5, sticky=tk.W)
        self.password_num_label.grid(row=10, column=0, padx=5, pady=5, sticky=tk.E)
        self.password_num_entry.grid(row=10, column=1, padx=5, pady=5, sticky=tk.W)
        self.about_label.grid(row=11, column=0, padx=5, pady=5, sticky=tk.E)
        self.about_entry.grid(row=11, column=1, padx=5, pady=5, sticky=tk.W)
        self.shops_label.grid(row=12, column=0, padx=5, pady=5, sticky=tk.E)
        self.shops_entry.grid(row=12, column=1, padx=5, pady=5, sticky=tk.W)
        self.work_shop_label.grid(row=13, column=0, padx=5, pady=5, sticky=tk.E)
        self.work_shop_entry.grid(row=13, column=1, padx=5, pady=5, sticky=tk.W)
        self.acsess_label.grid(row=14, column=0, padx=5, pady=5, sticky=tk.E)
        self.acsess_entry.grid(row=14, column=1, padx=5, pady=5, sticky=tk.W)
        self.pimg_label.grid(row=15, column=0, padx=5, pady=5, sticky=tk.E)
        self.pimg_entry.grid(row=15, column=1, padx=5, pady=5, sticky=tk.W)

        self.add_button.grid(row=17, column=0, padx=5, pady=5, sticky=tk.W)
        self.cancle_button.grid(row=17, column=1, padx=5, pady=5, sticky=tk.W)
        self.update_user_listbox()

    def on_name_entry(self, event):
        users = fetch_as_dict_list('SELECT * FROM Users', ())
        for user in users:
            print("on_name_entry\n"+str(user['User_name']))
            if user['User_name'] == self.name_entry.get():
                self.add_button.config(text="Update")    
                return
        if self.main_name == self.name_entry.get() and not self.main_name == "":
            self.add_button.config(text="Update")
        else:
            self.add_button.config(text="New")
            
    def perform_print(self):
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

    def show_user_form(self):
        # call the function in the main file to show the first frame
        self.master.master.show_frame("UserForm")
        
    def search_users(self, search_text):
        
        # Search for the entered text in the code, name, short_key, and type fields of the user table
        results = fetch_as_dict_list("SELECT * FROM Users WHERE User_name LIKE ? OR User_address LIKE ? OR User_id_pp_num LIKE ? OR User_phone_num LIKE ? OR User_email LIKE ? OR User_type LIKE ? OR User_access LIKE ?", 
                    ('%' + search_text + '%','%' + search_text + '%','%' + search_text + '%','%' + search_text + '%','%' + search_text + '%','%' + search_text + '%','%' + search_text + '%'))
        
        
        return results
    
    # Function to perform the search and display the results in the listbox
    def perform_search(self, customer_id):
        self.pyment_used = []
        

        # Perform the search and update the listbox with the results
        results = fetch_as_dict_list('SELECT * FROM doc_table WHERE customer_id=?',(customer_id,))
        
        
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
        for index in df:
            item = self.user_docinfo_listbox.insert('', 'end', text=index[0], values=(index[1], index[2], index[3], index[4], index[5], index[6], index[7], index[8], index[9], index[10], index[11], index[12], index[13], index[14]))
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
        
    # create a function to update the search results whenever the search box changes
    def update_search_results(self, *args):
        # get the search string from the search box
        search_str = self.search_var.get()
        
        # search for users based on the search string
        users = self.search_users(search_str)
        self.update_results(users)
        
    def update_results(self, users):
        # Clear the user listbox
        self.list_box.delete(*self.list_box.get_children())
        self.list_box['columns'] = ('Name', 'Type', 'Phone_Number', 'Id_Number', 'Email', 'Adress')
        self.list_box.heading("#0", text="ID")
        self.list_box.heading("#1", text="Name")
        self.list_box.heading("#2", text="Type")
        self.list_box.heading("#3", text="Phone_Number")
        self.list_box.heading("#4", text="Id_Number")
        self.list_box.heading("#4", text="Email")
        self.list_box.heading("#4", text="Adress")

        
        # Add the users to the user listbox
        for user in users:
            self.list_box.insert('', 'end', text=user[0], values=(user[1], user[2], user[3], user[4], user[5], user[6]))

        # Hide the user details frame
        self.hide_user_details_frame()
        self.change_button.config(state=tk.DISABLED)
        
    def clear_user_details_widget(self):
        # Clear the user details widgets
        
        self.fname_entry.delete(0, "end")
        self.lname_entry.delete(0, "end")
        self.name_entry.delete(0, "end")
        self.gender_entry.delete(0, "end")
        self.cuntry_entry.delete(0, "end")
        self.phone_num_entry.delete(0, "end")
        self.email_entry.delete(0, "end")
        self.addres_entry.delete(0, "end")
        self.home_no_entry.delete(0, "end")
        self.id_num_entry.delete(0, "end")
        self.type_entry.delete(0, "end")
        self.password_num_entry.delete(0, "end")
        self.about_entry.delete(0, "end")
        self.shops_entry.delete(0, "end")
        self.work_shop_entry.config(text="")
        self.acsess_entry.delete(0, "end")
        self.pimg_entry.delete(0, "end")

    # Create the "Add New" button
    def show_user_details_frame(self):
        self.clear_user_details_widget()
        self.on_name_entry(None)
        self.userinfo_notebook.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
    def hide_user_details_frame(self):
        self.clear_user_details_widget()
        self.userinfo_notebook.pack_forget()

    # Create the "Change" button
    def show_change_forme(self):
        selected_user = self.list_box.selection()
        if selected_user:
            # Get the ID of the selected user
            user_id = self.list_box.item(selected_user)['text']

            # Delete the user from the database
            Update_table_database('SELECT * FROM Users WHERE User_id=?', (user_id,))
            users = cur.fetchall()

            print("name : " + str(users))
            if users:
                id, User_fname, User_Lname, User_name, User_gender, User_country, User_phone_num, User_email, User_address, \
                    User_home_no, User_id_pp_num, User_type, User_password, User_about, User_shop, User_work_shop, User_likes, User_following_shop, User_favoraite_items, User_rate, User_access, User_pimg = users[0]
                # Clear the current text
                # than add new one
                self.fname_entry.delete(0, "end")
                self.fname_entry.insert(0, str(User_fname))
                self.lname_entry.delete(0, "end")
                self.lname_entry.insert(0, str(User_Lname))
                self.name_entry.delete(0, "end")
                self.name_entry.insert(0, str(User_name))
                self.gender_entry.delete(0, "end")
                self.gender_entry.insert(0, str(User_gender))
                self.cuntry_entry.delete(0, "end")
                self.cuntry_entry.insert(0, str(User_country))
                self.phone_num_entry.delete(0, "end")
                self.phone_num_entry.insert(0, str(User_phone_num))
                self.email_entry.delete(0, "end")
                self.email_entry.insert(0, str(User_email))
                self.addres_entry.delete(0, "end")
                self.addres_entry.insert(0, str(User_address))
                self.home_no_entry.delete(0, "end")
                self.home_no_entry.insert(0, str(User_home_no))
                self.id_num_entry.delete(0, "end")
                self.id_num_entry.insert(0, str(User_id_pp_num))
                self.type_entry.delete(0, "end")
                self.type_entry.insert(0, str(User_type))
                self.password_num_entry.delete(0, "end")
                self.password_num_entry.insert(0, str(User_password))
                self.about_entry.delete(0, "end")
                self.about_entry.insert(0, str(User_about))
                self.shops_entry.delete(0, "end")
                self.shops_entry.insert(0, str(User_shop))
                self.work_shop_entry.config(text="")
                wus = []
                try:
                    wus = json.loads(User_work_shop)
                except json.JSONDecodeError:
                    wus = []
                self.work_shop_entry.config(text="")
                for shop in wus:
                    self.work_shop_entry.config(text=self.work_shop_entry.cget("text") + "Shop Name " + str(shop[1]) + " Shop Brand " + str(shop[2]) + " User Level " + str(shop[3])+";\n")
                self.acsess_entry.delete(0, "end")
                self.acsess_entry.insert(0, str(User_access))
                self.pimg_entry.delete(0, "end")
                self.pimg_entry.insert(0, str(User_pimg))
                
                self.perform_search(id, )
                self.add_button.config(text="Update")
                # Commit the changes to the database
                conn.commit()
                self.userinfo_notebook.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    def on_select(self, event):
        if len(event.widget.selection()) > 0:
            self.change_button.config(state=tk.NORMAL)
            self.delete_button.config(state=tk.NORMAL)
        else:
            self.change_button.config(state=tk.DISABLED)
            self.delete_button.config(state=tk.DISABLED)

    # Define the function for updating the user listbox
    def update_user_listbox(self):
        # Get the users from the database
        #Update_table_database('SELECT * FROM USERS')
        users = []#cur.fetchall()
        self.update_results(users)
        
    # Define the function for adding a new user
    def add_user(self):
        # Get the values from the user details widgets
        User_fname = self.fname_entry.get()
        User_Lname = self.lname_entry.get()
        User_name = self.name_entry.get()
        User_gender = self.gender_entry.get()
        User_country = self.cuntry_entry.get()
        User_phone_num = self.phone_num_entry.get()
        User_email = self.email_entry.get()
        User_address = self.addres_entry.get()
        User_home_no = self.home_no_entry.get()
        User_id_pp_num = self.id_num_entry.get()
        User_type = self.type_entry.get()
        User_password = self.password_num_entry.get()
        User_about = self.about_entry.get()
        User_shop = self.shops_entry.get()
        User_work_shop = self.work_shop_entry.cget("text")
        User_access = self.acsess_entry.get()
        User_pimg =  self.pimg_entry.get()
        
        if self.add_button.cget("text") == "New":        
            # Insert the new user into the database
            User_likes = ""
            User_following_shop = ""
            User_favoraite_items = ""
            User_rate = ""
            Update_table_database('INSERT INTO Users(User_fname, User_Lname, User_name, User_gender, User_country, User_phone_num, User_email, User_address, User_home_no, User_type, User_password, User_about, User_shop, User_work_shop, User_likes, User_following_shop, User_favoraite_items, User_rate, User_access, User_pimg) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',(User_fname, User_Lname, User_name, User_gender, User_country, User_phone_num, User_email, User_address, User_home_no, User_type, User_password, User_about, User_shop, User_work_shop, User_likes, User_following_shop, User_favoraite_items, User_rate, User_access, User_pimg))
              
        else:
            item_id = int(self.list_box.item(self.list_box.selection())['text'])
            print("item_id : " + str(item_id))
            # UPDATE the new user into the database
            Update_table_database('UPDATE Users SET User_fname=?, User_Lname=?, User_name=?, User_gender=?, User_country=?, User_phone_num=?, User_email=?, User_address=?, User_home_no=?, User_id_pp_num=?, User_type=?, User_password=?, User_about=?, User_shop=?, User_work_shop=?, User_access=?, User_pimg=? WHERE User_id=?', (User_fname, User_Lname, User_name, User_gender, User_country, User_phone_num, User_email, User_address, User_home_no, User_id_pp_num, User_type, User_password, User_about, User_shop, User_work_shop, User_access, User_pimg, item_id))
        
        # Commit the changes to the database
        conn.commit()

        # Clear the user details widgets
        self.clear_user_details_widget()
        
        # Update the user listbox
        self.update_user_listbox()

    # Define the function for deleting a user
    def delete_user(self):
        # Get the selected user from the listbox
        selected_user = self.list_box.selection()

        if selected_user:
            # Get the ID of the selected user
            user_id = int(self.list_box.item(self.list_box.selection())['text'])
        
            # Delete the user from the database
            Update_table_database('DELETE FROM Users WHERE User_id=?', (user_id,))

            # Commit the changes to the database
            conn.commit()
            # Update the user listbox
            self.update_user_listbox()
