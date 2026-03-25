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
from C.slipe import load_slip
from D.endday import EnddayForm
from D.Upload_ import UploadingForm
from D.user_info import UserInfoForm
from D.printer import PrinterForm

from C.API.Get import *
from C.API.API import *
from C.API.Set import *


data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data'))
db_path = os.path.join(data_dir, 'my_database.db')


class ApproveFrame(tk.Frame):
    def __init__(self, master, user, shops, slips, left, print_slip):
        tk.Frame.__init__(self, master)
        self.slips = []
        self.print_slip = print_slip
        self.left = left
        self.shops = shops
        self.user = user
        self.count_printed = 0
        # Android-style dark blue color scheme
        self.bg_dark = "#0d47a1"      # Deep blue
        self.bg_light = "#1565c0"     # Darker blue
        self.accent_blue = "#1976d2"  # Medium blue
        self.text_light = "#ffffff"   # White text
        self.bg_darker = "#0a3d91"    # Even darker blue
        
        slip = ""
        for barcode in slips:
            doc_ = fetch_as_dict_list("SELECT * FROM doc_table WHERE doc_barcode=?", (barcode,))
            if doc_:
                doc_ = doc_[0]
                print(str(doc_))
                slip = load_slip(doc_, 0) #TODO GET ID
                self.slips.append([barcode, slip])
                print(str(slip))
                
        # Create a new Toplevel window for the value form
        self.getvalue_form = tk.Toplevel(self.master)
        self.getvalue_form.title("Selector Form")
        self.getvalue_form.columnconfigure((0), weight=1)
        self.getvalue_form.columnconfigure((1,2,3, 4, 5, 6, 7, 8, 9, 10), weight=1)
        self.getvalue_form.rowconfigure((0,1,2,3,4, 5), weight=1)
        
        # Calculate the center coordinates of the screen
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        x = (screen_width / 2) - (500 / 2)  # 500 is the width of the Payment Form window
        y = (screen_height / 2) - (500 / 2)  # 500 is the height of the Payment Form window

        # Set the position of the Payment Form window to center
        self.getvalue_form.geometry(f"{int(screen_width)}x{int(screen_height)}+{int(0)}+{int(0)}")

        # Create a listbox for the items
        
        self.buttons_frame = tk.Frame(self.getvalue_form)
        self.buttons_frame.grid(row=0, column=1, columnspan=3, rowspan=5, sticky="nsew")
        #.pack(side="left", fill="both", expand=True)
        self.buttons_frame.columnconfigure((0, 1, 2, 3, 4, 5), weight=1)
        self.buttons_frame.rowconfigure((0, 1, 2, 3, 4, 5, 6), weight=1)
        
        self.prev_slip = tk.Button(self.getvalue_form, text="<<", font=("Arial", 15), command= self.get_prev_slip)
        self.prev_slip.grid(row=0, column=0, sticky="nsew")
        

        self.on_barid = tk.Label(self.getvalue_form, text=str(len(self.slips)-2), font=("Arial", 25))
        self.on_barid.grid(row=0, column=1, sticky="nsew")

        self.next_slip = tk.Button(self.getvalue_form, text=">>", font=("Arial", 15), command= self.get_next_slip)
        self.next_slip.grid(row=0, column=2, sticky="nsew")
        
        self.midel_frame = tk.Frame(self.getvalue_form)
        self.midel_frame.grid(row=1, column=0, columnspan=5, rowspan=4, sticky="nsew")
        
        self.extrnal_frame = tk.Frame(self.midel_frame, height=int(screen_height * 0.050), bg=self.bg_darker)
        self.extrnal_frame.pack(side="top", fill="x")

        self.Frame_contaner_frame = tk.Frame(self.midel_frame, bg=self.bg_dark)
        self.Frame_contaner_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.List_Frame_contaner_frame = tk.Frame(self.Frame_contaner_frame, bg=self.bg_dark)
        self.List_Frame_contaner_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.List_Frame = tk.Frame(self.List_Frame_contaner_frame, bg=self.bg_dark)
        self.List_Frame.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        
        self.item_List_canvas = tk.Canvas(self.List_Frame, bg=self.bg_dark, highlightthickness=0)
        self.item_List_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        
        self.item_List_yscrollbar = tk.Scrollbar(self.List_Frame, orient='vertical', 
                                                 command=self.item_List_canvas.yview, bg=self.bg_light)
        self.item_List_yscrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.item_List_xscrollbar = tk.Scrollbar(self.List_Frame_contaner_frame, orient='horizontal', 
                                                 command=self.item_List_canvas.xview, bg=self.bg_light)
        self.item_List_xscrollbar.pack(side=tk.TOP, fill=tk.X)
        
        self.item_List_canvas.configure(xscrollcommand=self.item_List_xscrollbar.set, 
                                       yscrollcommand=self.item_List_yscrollbar.set)

        self.resipt_fram = tk.Frame(self.item_List_canvas, bg='white')
        self.item_List_canvas.create_window((0, 0), window=self.resipt_fram, anchor=tk.NW)
        self.resipt_fram.bind('<Configure>', lambda e: self.item_List_canvas.configure(scrollregion=self.item_List_canvas.bbox("all")))
        

        
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
        
        # Create an undo button
        self.undo_button = tk.Button(self.buttons_frame, text="Undo", font=("Arial", 15), command= lambda: self.undo_item)
        self.undo_button.grid(row=6, column=5, sticky="nsew")

        # Create continue Button
        self.continue_button = ttk.Button(self.buttons_frame, text="Continue", command=self.getvalue_form.destroy)
        self.continue_button.grid(row=6, column=4, sticky="nsew")
        #self.update_items()
        self.get_next_slip()
        self.getvalue_form.bind("<Return>", self.print_item)
        self.getvalue_form.bind("<Escape>", self.exit)

    def exit(self, event):
        self.getvalue_form.destroy()
        
    def change_focus(self, event):
        self.print_button.focus_set()
        
    def set_slip_lines(self, text):
        #active_var = tk.IntVar()
        #active_checkbutton = tk.Checkbutton(New_item_contener_frame, text='Active', variable=active_var)
        
        for items in self.resipt_fram.winfo_children():
            items.destroy()
        lines = text.split("\n")
        for l in lines:
            tk.Label(self.resipt_fram, text=l, font=("Arial", 10), bg='white').pack()
        
    def get_next_slip(self):
        i = 0;
        if self.on_barid.cget('text') != "":
            i = int(self.on_barid.cget('text'))
        if not i+1 >= len(self.slips):
            i += 1
            self.on_barid.config(text=str(i))
            self.set_slip_lines(str(self.slips[i][1]))
        else:
            i = 0
            self.on_barid.config(text=str(i))
            self.set_slip_lines(str(self.slips[i][1]))
            
    def get_prev_slip(self):
        i = 0;
        if self.on_barid.cget('text') != "":
            i = int(self.on_barid.cget('text'))
        if not i-1 < 0:
            i -= 1
            self.on_barid.config(text=str(i))
            self.set_slip_lines(str(self.slips[i][1]))
        else:
            i = len(self.slips)-1
            self.on_barid.config(text=str(i))
            self.set_slip_lines(str(self.slips[i][1]))
            
    def print_item(self, a):
        #print("printing : " + str(self.print_slip) + "splip : " + str(self.on_barid.cget('text')))
        answer = None
        if self.count_printed > 0:
            answer = tk.messagebox.askquestion("Question", "Slip orady printed " + str(self.count_printed+1)+ " times do you whant to print more?")
        if self.print_slip == 1 and (answer == None or answer == 'yes'):
            self.count_printed += 1
            on_slip = ""
            for items in self.resipt_fram.winfo_children():
                on_slip += items.cget('text') + "\n"
            if on_slip != "":
                PrinterForm.print_slip(self, self.user, self.shops, on_slip, 1) # TODO chack in setting if paper cut allowed
    
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
