import tkinter as tk
from tkinter import ttk, filedialog
import sqlite3
import json

from PIL import Image, ImageTk

# Connect to the database or create it if it does not exist

import os, shutil
data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data'))
db_path = os.path.join(data_dir, 'my_database.db')
import os, sys
current_dir = os.path.abspath(os.path.dirname(__file__))
MAIN_dir = os.path.join(current_dir, '..')
sys.path.append(MAIN_dir)
from D.docediterform import DocEditForm
from D.printer import PrinterForm
from C.slipe import load_slip

from D.ApprovedDisplay import ApproveFrame
from C.API import *
from C.API.Get import *
from C.API.Set import *

class UserForm(tk.Frame):
    def __init__(self, parent, user_info, shop):
        
        
        self.bg_dark = "#0d47a1"      # Deep blue
        self.bg_light = "#1565c0"     # Darker blue
        self.accent_blue = "#1976d2"  # Medium blue
        self.text_light = "#ffffff"   # White text
        self.bg_darker = "#0a3d91"    # Even darker blue
        self.button_style = {"font": ("Arial", 11, "bold"), "bg": self.accent_blue, "fg": self.text_light, "activebackground": self.bg_light, "activeforeground": self.text_light, "relief": tk.FLAT, "bd": 0}


        tk.Frame.__init__(self, parent, bg=self.bg_dark)
        self.user_info = user_info
        self.shop = shop
        self.homemaster = self
        while(True):
            if hasattr(self.homemaster, 'onDisplayFrame'):
                break
            else:
                self.homemaster = self.homemaster.master
        #print("self.User_data : ", self.User_data)

        self.MainApplication = self
        while(True):
            if hasattr(self.MainApplication, 'MainApplication_root'):
                break
            else:
                self.MainApplication = self.MainApplication.master
        
        self.config( bg=self.bg_dark)
        # Create the search bar
        # Create the frame for the search bar and buttons
        self.search_frame = tk.Frame(self, bg=self.bg_dark)
        self.search_frame.pack(side=tk.TOP, padx=5, pady=5)

        # create a StringVar to represent the search box
        self.search_var = tk.StringVar()
        self.search_entry = tk.Entry(self.search_frame, textvariable=self.search_var)
        #self.search_entry.bind('<KeyRelease>', self.update_search_results)
        self.search_entry.pack(side=tk.LEFT, padx=5, pady=5)
            
        # bind the update_search_results function to the search box
        self.search_var.trace("w", self.update_search_results)


        self.userlist_box_Frame = tk.Frame(self, bg=self.bg_dark)
        self.userlist_box_Frame.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        
        # Create the list box
        self.list_box = ttk.Treeview(self.userlist_box_Frame)
        self.list_box.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.list_box.bind('<<TreeviewSelect>>', self.on_select)
        
        self.item_List_yscrollbar = tk.Scrollbar(self.list_box, orient='vertical', command=self.list_box.yview, bg=self.bg_light, activebackground=self.accent_blue)
        self.item_List_yscrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.item_List_xscrollbar = tk.Scrollbar(self.list_box, orient='horizontal', command=self.list_box.xview, bg=self.bg_light, activebackground=self.accent_blue)
        self.item_List_xscrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.list_box.configure(xscrollcommand=self.item_List_xscrollbar.set, yscrollcommand=self.item_List_yscrollbar.set)


        self.userinfo_notebook = ttk.Notebook(self.list_box)
        self.userinfo_notebook.pack_forget()
        self.nested_list = []

        # Create the frame for the user details
        self.details_frame = tk.Frame(self.userinfo_notebook, bg=self.bg_dark)
        self.details_frame.pack()
        self.userinfo_notebook.add(self.details_frame, text="info")

        # Create the widgets for the user details
        self.User_image_frame = tk.Label(self.details_frame, bg=self.bg_dark)
        self.User_image_frame.bind("<Button-1>", lambda _: self.change_User_image())
        
        self.name_label = tk.Label(self.details_frame, text='Name:', bg=self.bg_dark, fg=self.text_light)
        self.name_entry = tk.Entry(self.details_frame)
        self.main_name = ""
        self.name_entry.bind('<KeyRelease>', lambda: self.on_name_entry)
        self.type_label = tk.Label(self.details_frame, text='TYPE:', bg=self.bg_dark, fg=self.text_light)
        self.type_entry = tk.Entry(self.details_frame)
        self.phone_num_label = tk.Label(self.details_frame, text='PHONE NUMBER:', bg=self.bg_dark, fg=self.text_light)
        self.phone_num_entry = tk.Entry(self.details_frame)
        self.email_label = tk.Label(self.details_frame, text='EMAIL:', bg=self.bg_dark, fg=self.text_light)
        self.email_entry = tk.Entry(self.details_frame)
        self.id_num_label = tk.Label(self.details_frame, text='ID Number:', bg=self.bg_dark, fg=self.text_light)
        self.id_num_entry = tk.Entry(self.details_frame)
        self.gender_label = tk.Label(self.details_frame, text='Gender :', bg=self.bg_dark, fg=self.text_light)
        self.gendert_var = tk.StringVar()  # gender selecter
        self.gender_Combobox = ttk.Combobox(self.details_frame, textvariable=self.gendert_var, values=["MALE", "FEMALE", "Prefer Not to Say"], state='readonly')
        self.acsess_label = tk.Label(self.details_frame, text='ACSSES:', bg=self.bg_dark, fg=self.text_light)
        self.acsess_entry = tk.Entry(self.details_frame)

        self.f_and_lname_label = tk.Label(self.details_frame, text='First and Last Name :', bg=self.bg_dark, fg=self.text_light)
        self.fname_entry = tk.Entry(self.details_frame)
        self.lname_entry = tk.Entry(self.details_frame)
        self.name_label = tk.Label(self.details_frame, text='User Name :', bg=self.bg_dark, fg=self.text_light)
        self.name_entry = tk.Entry(self.details_frame)
        self.cuntry_label = tk.Label(self.details_frame, text='Country :', bg=self.bg_dark, fg=self.text_light)
        self.cuntry_var = tk.StringVar()  # country selecter
        self.cuntry_Combobox = ttk.Combobox(self.details_frame, textvariable=self.cuntry_var, values=sorted(self.MainApplication.COUNTRIES_WITH_CITIES.keys()), state='readonly')
        self.cuntry_var.trace('w', lambda name, index, mode: cuntry_changed())
        self.cuntry_label.grid(row=7, column=0, padx=5, pady=5, sticky=tk.W)
        self.cuntry_Combobox.grid(row=7, column=1, padx=5, pady=5, sticky=tk.W)

        
        self.city_label = tk.Label(self.details_frame, text='City :', bg=self.bg_dark, fg=self.text_light)
        self.city_var = tk.StringVar()  # country selecter
        self.city_Combobox = ttk.Combobox(self.details_frame, textvariable=self.city_var, values=self.MainApplication.COUNTRIES_WITH_CITIES.get(self.cuntry_var.get(), []), state='readonly')
        def  cuntry_changed():
            self.city_Combobox['values'] = self.MainApplication.COUNTRIES_WITH_CITIES.get(self.cuntry_var.get(), [])
            self.city_var.set(str(self.MainApplication.COUNTRIES_WITH_CITIES.get(self.cuntry_var.get(), [])[0] if len(self.MainApplication.COUNTRIES_WITH_CITIES.get(self.cuntry_var.get(), [])) else "") )
        self.city_label.grid(row=8, column=0, padx=5, pady=5, sticky=tk.W)
        self.city_Combobox.grid(row=8, column=1, padx=5, pady=5, sticky=tk.W)
        
        self.phone_num_label = tk.Label(self.details_frame, text='Phone No :', bg=self.bg_dark, fg=self.text_light)
        self.phone_num_entry = tk.Entry(self.details_frame)
        self.email_label = tk.Label(self.details_frame, text='Email :', bg=self.bg_dark, fg=self.text_light)
        self.email_entry = tk.Entry(self.details_frame)
        self.id_num_label = tk.Label(self.details_frame, text='Id No :', bg=self.bg_dark, fg=self.text_light)
        self.id_num_entry = tk.Entry(self.details_frame)
        self.home_no_label = tk.Label(self.details_frame, text='Home No :', bg=self.bg_dark, fg=self.text_light)
        self.home_no_entry = tk.Entry(self.details_frame)
        self.type_label = tk.Label(self.details_frame, text='Type :', bg=self.bg_dark, fg=self.text_light)
        self.type_entry = tk.Entry(self.details_frame)
        self.password_num_label = tk.Label(self.details_frame, text='Password :', bg=self.bg_dark, fg=self.text_light)
        # mask password by default
        self.password_num_entry = tk.Entry(self.details_frame, show='*', bg=self.bg_dark, fg=self.text_light)

        # Checkbox to toggle password visibility
        self.show_password_var = tk.IntVar(value=0)
        def _toggle_password_visibility():
            if self.show_password_var.get():
                self.password_num_entry.config(show='')
            else:
                self.password_num_entry.config(show='*')
        self.show_password_cb = tk.Checkbutton(self.details_frame, text='Show Password', variable=self.show_password_var, command=_toggle_password_visibility)
        # place the checkbox (same row as password, different column)
        self.about_label = tk.Label(self.details_frame, text='About :', bg=self.bg_dark, fg=self.text_light)
        self.about_entry = tk.Entry(self.details_frame)
        
        self.WorkAt_var = tk.StringVar()  # displayed in the combobox
        self.WorkAt = []
        # Combobox for User ID (shows user_name but stores user_id)
        self.WorkAt_label = tk.Label(self.details_frame, text='Work At : ', bg=self.bg_dark, fg=self.text_light)
        self.WorkAt_Combobox = ttk.Combobox(self.details_frame, textvariable=self.WorkAt_var, values=self.WorkAt, state='readonly')
        
        
        self.work_shop_label = tk.Label(self.details_frame, text=':', bg=self.bg_dark, fg=self.text_light)
        self.work_shop_entry = tk.Label(self.details_frame)

        
        self.shops_label = tk.Label(self.details_frame, text=' :', bg=self.bg_dark, fg=self.text_light)
        self.shops_entry = tk.Entry(self.details_frame)
        
        self.acsess_label = tk.Label(self.details_frame, text=':', bg=self.bg_dark, fg=self.text_light)
        self.acsess_entry = tk.Entry(self.details_frame)
        

        self.add_button = tk.Button(self.details_frame, text='Add', command=self.add_user, **self.button_style)
        self.cancle_button = tk.Button(self.details_frame, text='Cancle', command=self.hide_user_details_frame, **self.button_style)




        # Create the frame for the user details
        self.doc_details_frame = tk.Frame(self.userinfo_notebook, bg=self.bg_dark)
        self.doc_details_frame.pack()
        self.userinfo_notebook.add(self.doc_details_frame, text="Doc info")

        self.user_docinfo_Frame = tk.Frame(self.doc_details_frame, bg=self.bg_dark)
        self.user_docinfo_Frame.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        
        # Create the list box
        self.user_docinfo_listbox = ttk.Treeview(self.user_docinfo_Frame)
        self.user_docinfo_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.user_docinfo_listbox.bind('<<TreeviewSelect>>', self.on_select)
        
        # Set the size of the self.listbox widget
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
        
        self.item_List_yscrollbar = tk.Scrollbar(self.user_docinfo_listbox, orient='vertical', command=self.user_docinfo_listbox.yview, bg=self.bg_light, activebackground=self.accent_blue)
        self.item_List_yscrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.item_List_xscrollbar = tk.Scrollbar(self.user_docinfo_listbox, orient='horizontal', command=self.user_docinfo_listbox.xview, bg=self.bg_light, activebackground=self.accent_blue)
        self.item_List_xscrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.user_docinfo_listbox.configure(xscrollcommand=self.item_List_xscrollbar.set, yscrollcommand=self.item_List_yscrollbar.set)



        # Create the search button
        self.print_button = tk.Button(self.user_docinfo_Frame, text="Veiw Doc", command=self.perform_veiw)
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
        
        
        self.User_image_frame.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)
        
        self.f_and_lname_label.grid(row=1, column=0, padx=5, pady=5, sticky=tk.E)
        self.fname_entry.grid(row=1, column=1, columnspan=2, padx=5, pady=5, sticky=tk.E)
        self.lname_entry.grid(row=1, column=4, columnspan=2, padx=5, pady=5, sticky=tk.W)
        
        self.name_label.grid(row=2, column=0, padx=5, pady=5, sticky=tk.E)
        self.name_entry.grid(row=2, column=1, columnspan=2, padx=5, pady=5, sticky=tk.W)
        self.gender_label.grid(row=2, column=4, padx=5, pady=5, sticky=tk.E)
        self.gender_Combobox.grid(row=2, column=5, columnspan=2, padx=5, pady=5, sticky=tk.W)
        
        self.cuntry_label.grid(row=3, column=0, padx=5, pady=5, sticky=tk.E)
        self.cuntry_Combobox.grid(row=3, column=1, columnspan=2, padx=5, pady=5, sticky=tk.W)
        self.city_label.grid(row=3, column=4, padx=5, pady=5, sticky=tk.E)
        self.city_Combobox.grid(row=3, column=5, columnspan=2, padx=5, pady=5, sticky=tk.W)
        
        self.home_no_label.grid(row=4, column=0, padx=5, pady=5, sticky=tk.E)
        self.home_no_entry.grid(row=4, column=1, columnspan=2, padx=5, pady=5, sticky=tk.W)
        self.id_num_label.grid(row=4, column=4, padx=5, pady=5, sticky=tk.E)
        self.id_num_entry.grid(row=4, column=5, columnspan=2, padx=5, pady=5, sticky=tk.W)
        
        self.phone_num_label.grid(row=5, column=0, padx=5, pady=5, sticky=tk.E)
        self.phone_num_entry.grid(row=5, column=1, columnspan=2, padx=5, pady=5, sticky=tk.W)
        self.email_label.grid(row=5, column=4, padx=5, pady=5, sticky=tk.E)
        self.email_entry.grid(row=5, column=5, columnspan=2, padx=5, pady=5, sticky=tk.W)
        
        self.type_label.grid(row=6, column=0, padx=5, pady=5, sticky=tk.E)
        self.type_entry.grid(row=6, column=1, columnspan=2, padx=5, pady=5, sticky=tk.W)
        self.password_num_label.grid(row=6, column=4, padx=5, pady=5, sticky=tk.E)
        self.password_num_entry.grid(row=6, column=5, columnspan=2, padx=5, pady=5, sticky=tk.W)
        self.show_password_cb.grid(row=6, column=6, padx=5, pady=5, sticky=tk.W)
        
        self.about_label.grid(row=7, column=0, padx=5, pady=5, sticky=tk.E)
        self.about_entry.grid(row=7, column=1, columnspan=2, padx=5, pady=5, sticky=tk.W)
        self.acsess_label.grid(row=7, column=5, padx=5, pady=5, sticky=tk.E)
        self.acsess_entry.grid(row=7, column=6, padx=5, pady=5, sticky=tk.W)
        
        self.shops_label.grid(row=8, column=0, padx=5, pady=5, sticky=tk.E)
        self.shops_entry.grid(row=8, column=1, padx=5, pady=5, sticky=tk.W)
        self.WorkAt_Combobox.grid(row=8, column=5, columnspan=5, sticky="nsew")
        self.WorkAt_label.grid(row=8, column=6, columnspan=5, sticky=tk.W)

        self.add_button.grid(row=13, column=0, padx=5, pady=5, sticky=tk.W)
        self.cancle_button.grid(row=13, column=1, padx=5, pady=5, sticky=tk.W)
        self.update_user_listbox()

    def on_name_entry(self, event):
        users = fetch_as_dict_list(self.homemaster.Link, 'SELECT * FROM Users', ())
        for user in users:
            #print("on_name_entry\n"+str(user['User_name']))
            if user['User_name'] == self.name_entry.get():
                self.add_button.config(text="Update")    
                return
        if self.main_name == self.name_entry.get() and not self.main_name == "":
            self.add_button.config(text="Update")
        else:
            self.add_button.config(text="New")
    def perform_veiw(self):
        item = self.user_docinfo_listbox.focus()  # Get the item that was clicked
        if item:
            item_text = self.user_docinfo_listbox.item(item, "values")  # Get the text values of the item
            id = self.user_docinfo_listbox.item(item, "text")
            barcode = item_text[0]
            doc_ = fetch_as_dict_list(self.homemaster.Link, "SELECT * FROM doc_table WHERE doc_barcode=?", (barcode,))[0]
            if doc_:
                 #TODO: MAKE IT SEND SELECTEd SHOP
                ApproveFrame(self, self.user_info, self.shop[0], [barcode], [], 1)
                '''answer = tk.messagebox.askquestion("Question", "Do you what to print "+str(barcode)+" ?")
                if answer == 'yes':
                    #print(str(doc_))
                    doc_edit_form = load_slip(doc_, doc_id)
                    #print("don loding slip : \n\n" + str(doc_edit_form))
                    self.user = self.master.master.master.master.user
                    # TODO: Make It send selected shop to print_slip
                    PrinterForm.print_slip(self, self.user_info, self.shop[0], doc_edit_form, 1) # TODO chack in setting if paper cut allowed'''
        
    def perform_print(self):
        item = self.user_docinfo_listbox.focus()  # Get the item that was clicked
        if item:
            item_text = self.user_docinfo_listbox.item(item, "values")  # Get the text values of the item
            id = self.user_docinfo_listbox.item(item, "text")
            barcode = item_text[0]
            doc_ = fetch_as_dict_list(self.homemaster.Link, "SELECT * FROM doc_table WHERE doc_barcode=?", (barcode,))
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
        results = fetch_as_dict_list(self.homemaster.Link, "SELECT * FROM Users WHERE User_name LIKE ? OR User_address LIKE ? OR User_id_pp_num LIKE ? OR User_phone_num LIKE ? OR User_email LIKE ? OR User_type LIKE ? OR User_access LIKE ?", 
                    ('%' + search_text + '%','%' + search_text + '%','%' + search_text + '%','%' + search_text + '%','%' + search_text + '%','%' + search_text + '%','%' + search_text + '%'))
        
        
        return results
    
    # Function to perform the search and display the results in the listbox
    def perform_search(self, customer_id):
        # Get the search text from the search entry
        search_text = self.search_var.get()
        
        # Search for users based on the search text
        users = self.search_users(search_text)
        
        # Update the listbox with the search results
        self.update_results(users)

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
            #print("update_results\n"+str(user))
            self.list_box.insert('', 'end', text=user['User_id'], values=(user['User_fname'], user['User_Lname'], user['User_name'], user['User_gender'], user['User_country'], user['User_phone_num'], user['User_email'], user['User_address']))

        # Hide the user details frame
        self.hide_user_details_frame()
        self.change_button.config(state=tk.DISABLED)
        
    def clear_user_details_widget(self):
        # Clear the user details widgets
        
        self.fname_entry.delete(0, "end")
        self.lname_entry.delete(0, "end")
        self.name_entry.delete(0, "end")
        self.gendert_var.set("")
        self.cuntry_var.set("")
        self.city_var.set("")
        self.phone_num_entry.delete(0, "end")
        self.email_entry.delete(0, "end")
        self.home_no_entry.delete(0, "end")
        self.id_num_entry.delete(0, "end")
        self.type_entry.delete(0, "end")
        self.password_num_entry.delete(0, "end")
        self.about_entry.delete(0, "end")
        self.shops_entry.delete(0, "end")
        self.WorkAt_var.set("")
        self.WorkAt = []
        self.WorkAt_Combobox.config(value=self.WorkAt)
        self.acsess_entry.delete(0, "end")
        
        self.load_User_image()
        
        
    # Create the "Add New" button
    def show_user_details_frame(self):
        self.clear_user_details_widget()
        self.on_name_entry(None)
        self.userinfo_notebook.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
    def hide_user_details_frame(self):
        self.clear_user_details_widget()
        self.userinfo_notebook.pack_forget()

    def change_User_image(self):
        if not self.name_entry.get() == "":
            file_source = filedialog.askopenfilename(filetypes=[("Image Files", "*.png *.jpg *.jpeg")])
            dest_folder = MAIN_dir+"\\data\\Users\\" + str(self.name_entry.get())
            imag_file_name  = "ProfileImage.jpg"
            # make sur folder is there
            os.makedirs(dest_folder, exist_ok=True)
            # join name and folder path
            dest_full_path = os.path.join(dest_folder, imag_file_name)
            # copy it to dest folder
            shutil.copy2(file_source, dest_full_path)
            self.load_User_image()
        else:
            tk.messagebox.askquestion("Worring", "User Name Is not Given!!")
        
    def load_User_image(self):
        if not self.name_entry.get() == "" and os.path.exists(MAIN_dir+"\\data\\Users\\" + str(self.name_entry.get()) + "\\ProfileImage.jpg"):
            img = Image.open(MAIN_dir+"\\data\\Users\\" + str(self.name_entry.get()) + "\\ProfileImage.jpg").resize((100, 100))
            img = ImageTk.PhotoImage(img)
            self.User_image_frame.config(image=img)
            self.User_image_frame.image = img
        else:
            new_img = Image.open(MAIN_dir+"\\data\\Icon\\no_Profile_image.jpg").resize((100, 100))
            new_img = ImageTk.PhotoImage(new_img)
            self.User_image_frame.config(image=new_img)
            self.User_image_frame.image = new_img
        
   # Create the "Change" button
    def show_change_forme(self):
        selected_user = self.list_box.selection()
        if selected_user:
            # Get the ID of the selected user
            user_id = self.list_box.item(selected_user)['text']

            # Delete the user from the database
            users = fetch_as_dict_list(self.homemaster.Link, 'SELECT * FROM Users WHERE User_id=?', (user_id,))

            #print("name : " + str(users))
            if users:
                id = users[0]['User_id']
                User_fname = users[0]['User_fname']
                User_Lname = users[0]['User_Lname']
                User_name = str(users[0]['User_fname'])[0] + str(users[0]['User_Lname'])[0] + " " +users[0]['User_fname']
                # loade image
                self.load_User_image() # chacke if there is image for the user by its name



                
                User_gender = users[0]['User_gender']
                User_country = users[0]['User_country']
                User_phone_num = users[0]['User_phone_num']
                User_email = users[0]['User_email']
                User_address = users[0]['User_address']
                User_home_no = users[0]['User_home_no']
                User_id_pp_num = users[0]['User_id_pp_num']
                User_type = users[0]['User_type']
                User_password = users[0]['User_password']
                User_about = users[0]['User_about']
                User_shop = users[0]['User_shop']
                User_work_shop = users[0]['User_work_shop']
                User_likes = users[0]['User_likes']
                User_following_shop = users[0]['User_following_shop']
                User_favoraite_items = users[0]['User_favoraite_items']
                User_rate = users[0]['User_rate']
                User_access = users[0]['User_access']

                # Clear the current text
                # than add new one
                self.fname_entry.delete(0, "end")
                self.fname_entry.insert(0, str(User_fname))
                self.lname_entry.delete(0, "end")
                self.lname_entry.insert(0, str(User_Lname))
                self.name_entry.delete(0, "end")
                self.name_entry.insert(0, str(User_name))
                self.gendert_var.set(str(User_gender))
                self.cuntry_var.set(str(User_country))
                self.phone_num_entry.delete(0, "end")
                self.phone_num_entry.insert(0, str(User_phone_num))
                self.email_entry.delete(0, "end")
                self.email_entry.insert(0, str(User_email))
                self.city_var.set(str(User_address))
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
                wus = []
                try:
                    if User_work_shop:
                        #print('User_work_shop ', User_work_shop)
                        wus = json.loads(User_work_shop)
                except json.JSONDecodeError:
                    wus = []
                self.WorkAt = []
                for shop in wus:
                    workform = "Custumer"
                    if str(shop[3][0]) == "0":
                        workform = "Worker"
                    if int(shop[3][0]) > 0 and int(shop[3][0]) < 5:
                        workform = "Seller"
                    if int(shop[3][0]) > 4 and int(shop[3][0]) < 8:
                        workform = "SuperViser"
                    if str(shop[3][0]) == "9":
                        workform = "Manager"
                    if str(shop[3][0]) == "10":
                        workform = "Owner"
                        
                    self.WorkAt.append(workform + " Of " + str(shop[1]) + str(shop[2]))
                if wus == []:
                    self.WorkAt.append("Custumer")
                    
                self.WorkAt_var.set(self.WorkAt[0])
                self.WorkAt_Combobox.config(value=self.WorkAt)
                
                self.acsess_entry.delete(0, "end")
                self.acsess_entry.insert(0, str(User_access))
                
                self.add_button.config(text="Update")
                self.userinfo_notebook.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
                #newdoc = search_documents(doc_id, doc_type, doc_barcode, extension_barcode, item, user_name, customer_name,
                #            sold_item_info, discount, seller_id, self.date_from_Entry.get(), self.date_to_Entry.get(), self.doc_created_date_var.get(), self.doc_expire_date_var.get(), self.doc_updated_date_var.get())
                
                newdocs = search_documents("", "", "", "", "", "", User_name,
                            "", "", "", "", "", "", "", "")
                if newdocs:
                    self.user_docinfo_listbox.delete(*self.user_docinfo_listbox.get_children())
                    for index in newdocs:
                        item = self.user_docinfo_listbox.insert('', 'end', text=index['id'], values=(index['doc_barcode'], index['extension_barcode'], index['At_Shop_Id'], index['user_id'], index['Seller_id'], index['customer_id'], index['pid'], index['qty'], index['price'], index['discount'], index['tax'], index['doc_created_date'], index['doc_expire_date'], index['doc_updated_date'], index['item'],  index['payments']))
                self.load_User_image()


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
        users = fetch_as_dict_list(self.homemaster.Link, 'SELECT * FROM USERS', ())
        self.update_results(users)
        
    # Define the function for adding a new user
    def add_user(self):
        # Get the values from the user details widgets
        User_fname = self.fname_entry.get()
        User_Lname = self.lname_entry.get()
        User_name = str(self.fname_entry.get())[0] + str(self.lname_entry.get())[0] + " " +self.fname_entry.get()
        User_gender = self.gendert_var.get()
        User_country = self.cuntry_var.get()
        User_phone_num = self.phone_num_entry.get()
        User_email = self.email_entry.get()
        User_address = self.city_var.get()
        User_home_no = self.home_no_entry.get()
        User_id_pp_num = self.id_num_entry.get()
        User_type = self.type_entry.get()
        User_password = self.password_num_entry.get()
        User_about = self.about_entry.get()
        User_shop = self.shops_entry.get()
        User_access = self.acsess_entry.get()
        self.load_User_image()
        if self.add_button.cget("text") == "New":        
            # Insert the new user into the database
            User_likes = ""
            User_following_shop = ""
            User_favoraite_items = ""
            User_rate = ""
            Set_User(None, ['User_fname', 'User_Lname', 'User_name', 'User_gender', 'User_country', 'User_phone_num', 'User_email', 'User_address', 'User_home_no', 'User_type', 'User_password', 'User_about', 'User_shop', 'User_likes', 'User_following_shop', 'User_favoraite_items', 'User_rate', 'User_access'], [User_fname, User_Lname, User_name, User_gender, User_country, User_phone_num, User_email, User_address, User_home_no, User_type, User_password, User_about, User_shop, User_likes, User_following_shop, User_favoraite_items, User_rate, User_access])
              
        else:
            user_id = int(self.list_box.item(self.list_box.selection())['text'])
            #print("user_id : " + str(user_id))
            # UPDATE the new user into the database
            Update_User(None, self.user_info, ['User_fname', 'User_Lname', 'User_name', 'User_gender', 'User_country', 'User_phone_num', 'User_email', 'User_address', 'User_home_no', 'User_id_pp_num', 'User_type', 'User_password', 'User_about', 'User_shop', 'User_access'], [User_fname, User_Lname, User_name, User_gender, User_country, User_phone_num, User_email, User_address, User_home_no, User_id_pp_num, User_type, User_password, User_about, User_shop, User_access], ['User_id'], [user_id])
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
