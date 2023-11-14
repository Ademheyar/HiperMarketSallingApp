import tkinter as tk
from tkinter import ttk
import sqlite3
import os
import sys
current_dir = os.path.abspath(os.path.dirname(__file__))
MAIN_dir = os.path.join(current_dir, '..')
sys.path.append(MAIN_dir)
from D.searchbox import search_entry
from D.Peymentsplit import PaymentForm
from D.GetVALUE import GetvalueForm
from D.Showchartlists import ShowchartForm
from M.Product import ProductForm
from D.iteminfo import *
<<<<<<< HEAD
=======
from C.slipe import load_slip
>>>>>>> db9ae79 (adding seller)
from D.endday import EnddayForm
from D.Upload_ import UploadingForm
from D.user_info import UserInfoForm
from D.printer import PrinterForm

<<<<<<< HEAD
conn = sqlite3.connect("my_database.db")
cursor = conn.cursor()

class ApproveFrame(tk.Frame):
    def __init__(self, master, tree, slip, print_slip, user):
        tk.Frame.__init__(self, master)
        self.slip = slip
        self.print_slip = print_slip
        self.tree = tree
        self.user = user

=======

data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data'))
db_path = os.path.join(data_dir, 'my_database.db')
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

class ApproveFrame(tk.Frame):
    def __init__(self, master, user, slips, left, print_slip):
        tk.Frame.__init__(self, master)
        self.slips = []
        self.print_slip = print_slip
        self.left = left
        self.user = user
        slip = ""
        for barcode in slips:
            doc_ = cursor.execute("SELECT * FROM doc_table WHERE doc_barcode=?", (barcode,)).fetchone()
            if doc_:
                print(str(doc_))
                slip = load_slip(doc_, 0) #TODO GET ID
                self.slips.append([barcode, slip])
                print(str(slip))
                
>>>>>>> db9ae79 (adding seller)
        # Create a new Toplevel window for the value form
        self.getvalue_form = tk.Toplevel(self.master)
        self.getvalue_form.title("Selector Form")
        self.getvalue_form.columnconfigure((0), weight=1)
<<<<<<< HEAD
        self.getvalue_form.columnconfigure((1,2,3), weight=1)
        self.getvalue_form.rowconfigure((0,1,2,3,4), weight=1)
=======
        self.getvalue_form.columnconfigure((1,2,3, 4, 5, 6, 7, 8, 9, 10), weight=1)
        self.getvalue_form.rowconfigure((0,1,2,3,4, 5), weight=1)
>>>>>>> db9ae79 (adding seller)
        
        # Calculate the center coordinates of the screen
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        x = (screen_width / 2) - (500 / 2)  # 500 is the width of the Payment Form window
        y = (screen_height / 2) - (500 / 2)  # 500 is the height of the Payment Form window

        # Set the position of the Payment Form window to center
        self.getvalue_form.geometry(f"{int(screen_width)}x{int(screen_height)}+{int(0)}+{int(0)}")

        # Create a listbox for the items
<<<<<<< HEAD
        self.total_tax_label = tk.Label(self.getvalue_form, text=slip, font=("Arial", 10))
        self.total_tax_label.grid(row=0, column=0, rowspan=5)
        
        '''self.list_items = tk.Listbox(self.getvalue_form)
        self.list_items.grid(row=0, column=0, rowspan=4, sticky="nsew")
        #.pack(side="left", fill="both", expand=True)

        # Create a frame for buttons and labels
        self.info_frame = tk.Frame(self.getvalue_form)
        self.info_frame.grid(row=4, column=0, sticky="nsew")
        #.pack(side="left", fill="both", expand=True)
        self.info_frame.columnconfigure((0, 1), weight=0)
        self.info_frame.rowconfigure((0, 1, 2, 3), weight=1)
        

        # Create labels for the total items, price, discountmain_frame, tax, and total
        self.total_type_label = tk.Label(self.info_frame, text="Total Items : 0", font=("Arial", 15))
        self.total_type_label.grid(row=0, column=0, sticky="nsew")
        self.total_items_label = tk.Label(self.info_frame, text="Total Items : 0", font=("Arial", 15))
        self.total_items_label.grid(row=1, column=0, sticky="nsew")
        self.total_price_label = tk.Label(self.info_frame, text="Total Price : 0", font=("Arial", 15))
        self.total_price_label.grid(row=1, column=1, sticky="nsew")
        self.total_discount_label = tk.Label(self.info_frame, text="Total Discount : 0", font=("Arial", 15))
        self.total_discount_label.grid(row=2, column=0, sticky="nsew")
        self.total_tax_label = tk.Label(self.info_frame, text="Total Tax : 0", font=("Arial", 15))
        self.total_tax_label.grid(row=2, column=1, sticky="nsew")
        self.total_label = tk.Label(self.info_frame, text="Total : 0", font=("Arial", 25))
        self.total_label.grid(row=3, column=0, sticky="nsew")'''

        # Create a frame for buttons and labels
=======
        
>>>>>>> db9ae79 (adding seller)
        self.buttons_frame = tk.Frame(self.getvalue_form)
        self.buttons_frame.grid(row=0, column=1, columnspan=3, rowspan=5, sticky="nsew")
        #.pack(side="left", fill="both", expand=True)
        self.buttons_frame.columnconfigure((0, 1, 2, 3, 4, 5), weight=1)
        self.buttons_frame.rowconfigure((0, 1, 2, 3, 4, 5, 6), weight=1)
        
<<<<<<< HEAD
        self.label1 = tk.Label(self.buttons_frame, text="change : 0", font=("Arial", 25))
        self.label1.grid(row=0, column=2, columnspan=3, sticky="nsew")
                         
        self.label2 = tk.Label(self.buttons_frame, text="How Would the Customer like their receipt?", font=("Arial", 20))
        self.label2.grid(row=1, column=2, columnspan=4, sticky="nsew")
        
        # Create an undo button
        self.print_button = tk.Button(self.buttons_frame, text="print", font=("Arial", 15), command= self.print_item)
        self.print_button.grid(row=2, column=1, columnspan=2, sticky="nsew")
=======
        self.prev_slip = tk.Button(self.getvalue_form, text="<<", font=("Arial", 15), command= self.get_prev_slip)
        self.prev_slip.grid(row=0, column=0, sticky="nsew")
        

        self.on_barid = tk.Label(self.getvalue_form, text=str(len(self.slips)-2), font=("Arial", 25))
        self.on_barid.grid(row=0, column=1, sticky="nsew")

        self.next_slip = tk.Button(self.getvalue_form, text=">>", font=("Arial", 15), command= self.get_next_slip)
        self.next_slip.grid(row=0, column=2, sticky="nsew")
        
        self.on_slip = tk.Label(self.getvalue_form, text=slip, font=("Arial", 10))
        self.on_slip.grid(row=1, column=0, columnspan=5, rowspan=4, sticky="nsew")

        
        self.label1 = tk.Label(self.getvalue_form, text="change : 0", font=("Arial", 25))
        self.label1.grid(row=5, column=0, columnspan=3, sticky="nsew")

        # Create a frame for buttons and labels
        self.buttons_frame = tk.Frame(self.getvalue_form)
        self.buttons_frame.grid(row=0, column=5, columnspan=3, rowspan=5, sticky="nsew")
        #.pack(side="left", fill="both", expand=True)
        self.buttons_frame.columnconfigure((0, 1, 2, 3, 4, 5), weight=1)
        self.buttons_frame.rowconfigure((0, 1, 2, 3, 4, 5, 6), weight=1)
        
        
        self.label2 = tk.Label(self.buttons_frame, text="How Would the Customer like their receipt?", font=("Arial", 20))
        self.label2.grid(row=1, column=4, columnspan=4, sticky="nsew")
        
        # Create an undo button
        self.print_button = tk.Button(self.buttons_frame, text="print", font=("Arial", 15), command= lambda:self.print_item(None))
        self.print_button.grid(row=5, column=4, sticky="nsew")
        self.print_button.focus_set()
>>>>>>> db9ae79 (adding seller)
        
        # Create an undo button
        self.undo_button = tk.Button(self.buttons_frame, text="Undo", font=("Arial", 15), command= lambda: self.undo_item)
        self.undo_button.grid(row=6, column=5, sticky="nsew")

        # Create continue Button
        self.continue_button = ttk.Button(self.buttons_frame, text="Continue", command=self.getvalue_form.destroy)
        self.continue_button.grid(row=6, column=4, sticky="nsew")
        #self.update_items()
<<<<<<< HEAD
        
    def print_item(self):
        print("printing : " + str(self.print_slip) + "splip : " + str(self.slip))
        if self.print_slip == 1:
            PrinterForm.print_slip(self, self.slip, 1) # TODO chack in setting if paper cut allowed
=======
        self.get_next_slip()
        self.getvalue_form.bind("<Return>", self.print_item)
        self.getvalue_form.bind("<Escape>", self.exit)

    def exit(self, event):
        self.getvalue_form.destroy()
        
    def change_focus(self, event):
        self.print_button.focus_set()
        
    def get_next_slip(self):
        i = 0;
        if self.on_barid.cget('text') != "":
            i = int(self.on_barid.cget('text'))
        if not i+1 >= len(self.slips):
            i += 1
            self.on_barid.config(text=str(i))
            self.on_slip.config(text=str(self.slips[i][1]))
        else:
            i = 0
            self.on_barid.config(text=str(i))
            self.on_slip.config(text=str(self.slips[i][1]))
            
    def get_prev_slip(self):
        i = 0;
        if self.on_barid.cget('text') != "":
            i = int(self.on_barid.cget('text'))
        if not i-1 < 0:
            i -= 1
            self.on_barid.config(text=str(i))
            self.on_slip.config(text=str(self.slips[i][1]))
        else:
            i = len(self.slips)-1
            self.on_barid.config(text=str(i))
            self.on_slip.config(text=str(self.slips[i][1]))
            
    def print_item(self, a):
        print("printing : " + str(self.print_slip) + "splip : " + str(self.on_barid.cget('text')))
        if self.print_slip == 1:
            PrinterForm.print_slip(self, self.user, self.on_slip.cget('text'), 1) # TODO chack in setting if paper cut allowed
>>>>>>> db9ae79 (adding seller)
    
    def undo_item(self):
        pass
    
    def call_manager(self):
        pass
    
    # Create the function to update the item list and the total labels
    def update_items(self):

        # Clear any existing items in the listbox
        self.list_items.delete(0, tk.END)

        '''total_items = 0
        total_discount = 0
        total_price = 0

        # Populate the listbox with sold items
        for i in self.tree.get_children():
            item = self.tree.item(i)['values']
            total_items += 1
            total_discount += float(item[8])
            total_price += float(item[7])*float(item[6])-float(item[8])
            # price X qty = total
            self.list_items.insert(tk.END, "(" + str(item[7]) + " x " + str(item[6]) + ") - " + str(item[8]) + " = "  + str(float(item[7])*float(item[6])-float(item[8])))

        # Update the labels with the calculated values
        self.total_items_label.config(text=f"Total Items: " + str(total_items) )
        self.total_discount_label.config(text=f"Total Discount: " + str(total_discount) )
        self.total_label.config(text=f"Total Price: " + str(total_price) )
        self.total_tax_label.config(text=f"Total Tax : "  )'''
