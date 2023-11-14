import tkinter as tk
from tkinter import ttk
import sqlite3
import os
import sys
current_dir = os.path.abspath(os.path.dirname(__file__))
MAIN_dir = os.path.join(os.path.join(current_dir, '..'), '..')
sys.path.append(MAIN_dir)
from D.searchbox import search_entry
from D.Peymentsplit import PaymentForm
from D.GetVALUE import GetvalueForm
from D.Showchartlists import ShowchartForm
from D.iteminfo import *
from C.slipe import load_slip
from D.endday import EnddayForm
from D.Upload_ import UploadingForm
from D.user_info import UserInfoForm


db_path = os.path.join(MAIN_dir, 'my_database.db')
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

import tkinter as tk
from tkinter import filedialog, messagebox
#from reportlab.lib.pagesizes import letter
#from reportlab.pdfgen import canvas
import barcode
#from barcode.writer import ImageWriter
#from PIL import Image, ImageTk
import io
#import win32print

#from reportlab.pdfgen import canvas as reportlab_canvas
from PyPDF2 import PdfWriter
from fpdf import FPDF
#from PIL import ImageGrab
#import fitz  # PyMuPDF
import tkinter as tk
from tkinter import filedialog
from tkinter.simpledialog import askstring, Dialog
#from PIL import Image, ImageTk, ImageGrab  # Import ImageGrab
#import win32print
#import win32api  # Corrected impor
import tempfile
import os

#from reportlab.pdfgen import canvas

class PrinterDialog(Dialog):
    def __init__(self, parent, printers):
        self.printers = printers
        super().__init__(parent)

    def body(self, master):
        self.result = None
        tk.Label(master, text="Select a printer:").pack()
        self.printer_var = tk.StringVar()
        self.printer_var.set(self.printers[0])  # Default printer
        self.printer_menu = tk.OptionMenu(master, self.printer_var, *self.printers)
        self.printer_menu.pack()

    def apply(self):
        self.result = self.printer_var.get()

class PrintPriceTagFrame(tk.Toplevel):
    def __init__(self, master):
        tk.Toplevel.__init__(self, master)
        self.slips = []
        self.print_slip = ""
        self.left = ""
        self.user = ""
        slip = ""
        self.barcode_type_map = {
            "EAN8": barcode.get_barcode_class('ean8'),
            "EAN13": barcode.get_barcode_class('ean13'),
            "UPC_A": barcode.get_barcode_class('upca'),
            "CODE39": barcode.Code39,
            "CODE128": barcode.get_barcode_class('code128')
            #"CODE93": barcode.get_barcode_class('code93')
            #"I2OF5": barcode.get_barcode_class('i2of5'),
            #"MSI": barcode.get_barcode_class('msi')
        }

        self.show_border = tk.BooleanVar()
        self.show_border.set(True)
        
        self.product_data = []
        self.current_product = 0
        # Create a new Toplevel window for the value form
        self.getvalue_form = self
        self.getvalue_form.title("PrintPriceTag Form")
        self.getvalue_form.columnconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8, 9), weight=1)
        self.getvalue_form.rowconfigure((0,1,2,3,4, 5, 6, 7, 8, 9), weight=1)
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        x = (screen_width / 2) - (500 / 2)  # 500 is the width of the Payment Form window
        y = (screen_height / 2) - (500 / 2)  # 500 is the height of the Payment Form window

        # Set the position of the Payment Form window to center
        self.getvalue_form.geometry(f"{int(screen_width)}x{int(screen_height)}+{int(0)}+{int(0)}")

        self.buttons_frame = tk.Frame(self.getvalue_form, bg="red")
        self.buttons_frame.grid(row=0, column=0, rowspan=10, sticky="nsew")
        #.pack(side="left", fill="both", expand=True)
        self.buttons_frame.columnconfigure((0, 1, 2, 3), weight=0)
        self.buttons_frame.rowconfigure((0, 1, 2, 3, 4, 5, 7, 8, 9, 10), weight=0)
        self.buttons_frame.rowconfigure((6), weight=1)
        # search code
        self.top_frame = tk.Frame(self.buttons_frame)
        self.top_frame.grid(row=0, column=0, columnspan=4, sticky="nsew")
        self.top_frame.columnconfigure((0), weight=1)
        self.top_frame.rowconfigure((0), weight=1)
        self.search_entry = search_entry(self.top_frame, font=("Arial", 12))
        self.search_entry.grid(row=0, column=0, sticky="nsew")
        
        tk.Label(self.buttons_frame, text="Display", font=("Arial", 10)).grid(row=1, column=1, pady=5, sticky=tk.W)
        self.service_change_var = tk.IntVar()
        self.product_name_Check = tk.Checkbutton(self.buttons_frame, text='product name', variable=self.service_change_var)
        self.product_name_Check.grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        self.product_name_entry = tk.Entry(self.buttons_frame)
        self.product_name_entry.insert(0, "8")  # Set default name size
        self.product_name_entry.grid(row=2, column=1, padx=5, pady=5, sticky=tk.W)
        self.product_code_Check = tk.Checkbutton(self.buttons_frame, text='code', variable=self.service_change_var)
        self.product_code_Check.grid(row=2, column=2, padx=5, pady=5, sticky=tk.W)
        self.product_code_entry = tk.Entry(self.buttons_frame)
        self.product_code_entry.insert(0, "8")  # Set default name size
        self.product_code_entry.grid(row=2, column=3, padx=5, pady=5, sticky=tk.W)
        self.product_price_Check = tk.Checkbutton(self.buttons_frame, text='price', variable=self.service_change_var)
        self.product_price_Check.grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)
        self.product_price_entry = tk.Entry(self.buttons_frame)
        self.product_price_entry.insert(0, "8")  # Set default price size
        self.product_price_entry.grid(row=3, column=1, padx=5, pady=5, sticky=tk.W)
        self.product_tax_Check = tk.Checkbutton(self.buttons_frame, text='Tax inclusive price', variable=self.service_change_var)
        self.product_tax_Check.grid(row=3, column=2, padx=5, pady=5, sticky=tk.W)
        self.product_tax_entry = tk.Entry(self.buttons_frame)
        self.product_tax_entry.insert(0, "8")  # Set default price size
        self.product_tax_entry.grid(row=3, column=3, padx=5, pady=5, sticky=tk.W)
        self.product_barcode_Check = tk.Checkbutton(self.buttons_frame, text='Barcode', variable=self.service_change_var)
        self.product_barcode_Check.grid(row=4, column=0, padx=5, pady=5, sticky=tk.W)
        self.product_barcode_entry = tk.Entry(self.buttons_frame)
        self.product_barcode_entry.insert(0, "40")  # Set default barcode size
        self.product_barcode_entry.grid(row=4, column=1, padx=5, pady=5, sticky=tk.W)
        self.product_borders_Check = tk.Checkbutton(self.buttons_frame, text='Borders', variable=self.service_change_var)
        self.product_borders_Check.grid(row=4, column=2, padx=5, pady=5, sticky=tk.W)
        self.product_borders_entry = tk.Entry(self.buttons_frame)
        self.product_borders_entry.grid(row=4, column=3, padx=5, pady=5, sticky=tk.W)
        self.product_borders_entry.insert(0, "2")  # Set default price size
        self.product_after_discount_Check = tk.Checkbutton(self.buttons_frame, text='after discount', variable=self.service_change_var)
        self.product_after_discount_Check.grid(row=5, column=0, padx=5, pady=5, sticky=tk.W)
        self.product_after_discount_entry = tk.Entry(self.buttons_frame)
        self.product_after_discount_entry.grid(row=5, column=1, padx=5, pady=5, sticky=tk.W)
        self.product_after_discount_entry.insert(0, "2")  # Set default price size
        self.product_size_color_Check = tk.Checkbutton(self.buttons_frame, text='show size and color', variable=self.service_change_var)
        self.product_size_color_Check.grid(row=5, column=2, padx=5, pady=5, sticky=tk.W)
        self.product_size_color_entry = tk.Entry(self.buttons_frame)
        self.product_size_color_entry.grid(row=5, column=3, padx=5, pady=5, sticky=tk.W)
        self.product_size_color_entry.insert(0, "2")  # Set default price size

        # list box
        # New listbox in the main frame
        self.list_items = ttk.Treeview(self.buttons_frame, columns=("CODE", "BARCODE", "ITEM Name", "QTY", "WAS", "NOW", "TAX", "COLOR", "SIZE", "AT SHOP"))
        #self.list_items.grid_propagate(False)

        
        # Add vertical scrollbar
        tree_scrollbar_y = ttk.Scrollbar(self.list_items, orient='vertical', command=self.list_items.yview)
        self.list_items.configure(yscrollcommand=tree_scrollbar_y.set)
        tree_scrollbar_y.pack(side='right', fill='y')

        # Add horizontal scrollbar
        tree_scrollbar_x = ttk.Scrollbar(self.list_items, orient='horizontal', command=self.list_items.xview)
        self.list_items.configure(xscrollcommand=tree_scrollbar_x.set)
        tree_scrollbar_x.pack(side='bottom', fill='x')

        self.list_items.grid(row=6, column=0, columnspan=4, rowspan=4, sticky="nsew")
        self.list_items.heading("#0", text="Id", anchor=tk.W)
        self.list_items.column("#0", stretch=tk.NO, minwidth=0, width=0)   
        self.list_items.heading("#1", text="CODE", anchor=tk.W)
        self.list_items.column("#1", stretch=tk.NO, minwidth=25, width=50)
        self.list_items.heading("#2", text="BARCODE", anchor=tk.W)
        self.list_items.column("#2", stretch=tk.NO, minwidth=25, width=100)
        self.list_items.heading("#3", text="ITEM Name", anchor=tk.W)
        self.list_items.column("#3", stretch=tk.NO, minwidth=25, width=125)
        self.list_items.heading("#4", text="COLOR", anchor=tk.W)
        self.list_items.column("#4", stretch=tk.NO, minwidth=25, width=100)
        self.list_items.heading("#5", text="SIZE", anchor=tk.W)
        self.list_items.column("#5", stretch=tk.NO, minwidth=25, width=50)
        self.list_items.heading("#6", text="QTY", anchor=tk.W)
        self.list_items.column("#6", stretch=tk.NO, minwidth=25, width=50)
        self.list_items.heading("#7", text="PRICE", anchor=tk.W)
        self.list_items.column("#7", stretch=tk.NO, minwidth=25, width=50)
        self.list_items.heading("#8", text="NOW", anchor=tk.W)
        self.list_items.column("#8", stretch=tk.NO, minwidth=25, width=50)
        self.list_items.heading("#9", text="TAX", anchor=tk.W)
        self.list_items.column("#9", stretch=tk.NO, minwidth=25, width=50)
        self.list_items.heading("#10", text="AT SHOP", anchor=tk.W)
        self.list_items.column("#10", stretch=tk.NO, minwidth=25, width=50)
        
        self.display_frame = tk.Frame(self.getvalue_form, bg="green")
        self.display_frame.grid(row=0, column=1, columnspan=8, rowspan=10, sticky="nsew")
        self.display_frame.columnconfigure((0, 1, 2, 3, 4, 5), weight=0)
        self.display_frame.rowconfigure((0, 1, 2, 3, 4, 5, 6, 8, 9, 10), weight=0)
        self.display_frame.rowconfigure((7), weight=1)
        
        tk.Label(self.display_frame, text="Paper Size", font=("Arial", 8)).grid(row=0, column=0, pady=5, sticky=tk.W)
        self.barcode_size_entry = tk.Entry(self.display_frame)
        self.barcode_size_entry.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.barcode_size_entry.insert(0, "60")  # Set default price size

        tk.Label(self.display_frame, text="Pag hight", font=("Arial", 8)).grid(row=0, column=1, pady=5, sticky=tk.W)
        self.Pag_hight_entry = tk.Entry(self.display_frame)
        self.Pag_hight_entry.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)
        self.Pag_hight_entry.insert(0, "80")  # Set default price size

        tk.Label(self.display_frame, text="pag Width", font=("Arial", 8)).grid(row=0, column=2, pady=5, sticky=tk.W)
        self.Pag_width_entry = tk.Entry(self.display_frame)
        self.Pag_width_entry.grid(row=1, column=2, padx=5, pady=5, sticky=tk.W)
        self.Pag_width_entry.insert(0, "220")  # Set default barcode size

        tk.Label(self.display_frame, text="Column", font=("Arial", 8)).grid(row=0, column=3, pady=5, sticky=tk.W)
        self.product_num_columns_entry = tk.Entry(self.display_frame)
        self.product_num_columns_entry.grid(row=1, column=3, padx=5, pady=5, sticky=tk.W)
        self.product_num_columns_entry.insert(0, "2")  # Set default price size
        
        tk.Label(self.display_frame, text="Top", font=("Arial", 8)).grid(row=2, column=0, pady=5, sticky=tk.W)
        self.borders_top_entry = tk.Entry(self.display_frame)
        self.borders_top_entry.grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)
        self.borders_top_entry.insert(0, "1")  # Set default price size

        tk.Label(self.display_frame, text="Bottom", font=("Arial", 8)).grid(row=2, column=1, pady=5, sticky=tk.W)
        self.borders_bottom_entry = tk.Entry(self.display_frame)
        self.borders_bottom_entry.grid(row=3, column=1, padx=5, pady=5, sticky=tk.W)
        self.borders_bottom_entry.insert(0, "1")  # Set default price size

        tk.Label(self.display_frame, text="Left", font=("Arial", 8)).grid(row=2, column=2, pady=5, sticky=tk.W)
        self.borders_left_entry = tk.Entry(self.display_frame)
        self.borders_left_entry.grid(row=3, column=2, padx=5, pady=5, sticky=tk.W)
        self.borders_left_entry.insert(0, "1")  # Set default price size

        tk.Label(self.display_frame, text="Right", font=("Arial", 8)).grid(row=2, column=3, pady=5, sticky=tk.W)
        self.product_borders_entry = tk.Entry(self.display_frame)
        self.product_borders_entry.grid(row=3, column=3, padx=5, pady=5, sticky=tk.W)

        tk.Label(self.display_frame, text="gap_columen", font=("Arial", 8)).grid(row=4, column=0, pady=5, sticky=tk.W)
        self.borders_gap_columen_entry = tk.Entry(self.display_frame)
        self.borders_gap_columen_entry.grid(row=5, column=0, padx=5, pady=5, sticky=tk.W)
        self.borders_gap_columen_entry.insert(0, "14")  # Set default price size

        tk.Label(self.display_frame, text="gap_row", font=("Arial", 8)).grid(row=4, column=1, pady=5, sticky=tk.W)
        self.borders_gap_row_entry = tk.Entry(self.display_frame)
        self.borders_gap_row_entry.grid(row=5, column=1, padx=5, pady=5, sticky=tk.W)
        self.borders_gap_row_entry.insert(0, "1")  # Set default price size
        
        tk.Label(self.display_frame, text="Column hight", font=("Arial", 8)).grid(row=4, column=2, pady=5, sticky=tk.W)
        self.product_bordersH_entry = tk.Entry(self.display_frame)
        self.product_bordersH_entry.grid(row=5, column=2, padx=5, pady=5, sticky=tk.W)
        self.product_bordersH_entry.insert(0, "70")  # Set default price size

        tk.Label(self.display_frame, text="Column Width", font=("Arial", 8)).grid(row=4, column=3, pady=5, sticky=tk.W)
        self.product_bordersW_entry = tk.Entry(self.display_frame)
        self.product_bordersW_entry.grid(row=5, column=3, padx=5, pady=5, sticky=tk.W)
        self.product_bordersW_entry.insert(0, "100")  # Set default barcode size
        
        pdf_CONT_frame = tk.Frame(self.display_frame)
        pdf_CONT_frame.grid(row=6, column=0, columnspan=4, sticky="nsew")
        
        self.label = tk.Label(pdf_CONT_frame, text="Type:")
        self.label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.barcode_type_var = tk.StringVar()
        self.barcode_type_choices = [
            "EAN8", "EAN13", "UCC", "UPC_E", "UPC_A", "CODE39", "CODE128", "CODE93", "I2OF5", "MSI"
        ]
        self.barcode_type_var.set("UPC_A")
        self.barcode_type_dropdown = tk.OptionMenu(pdf_CONT_frame, self.barcode_type_var, *self.barcode_type_choices)
        self.barcode_type_dropdown.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        
        self.PreViwe_slip = tk.Button(pdf_CONT_frame, text="PreViwe", font=("Arial", 15), command= self.show_PreViwe)
        self.PreViwe_slip.grid(row=0, column=2, sticky="nsew")
        
        self.print_button = ttk.Button(pdf_CONT_frame, text="Print", command=self.getvalue_form.destroy)
        self.print_button.grid(row=0, column=3, sticky="nsew")
        
        self.generate_button = tk.Button(pdf_CONT_frame, text="Generate Price Tag", command=self.generate_price_tag)
        self.generate_button.grid(row=0, column=4, padx=5, pady=5)
        
        self.preview_button = tk.Button(pdf_CONT_frame, text="Print PDF", command=self.print_pdf)
        self.preview_button.grid(row=0, column=5, padx=5, pady=5)

        self.new_button = tk.Button(pdf_CONT_frame, text="new", command=self.new_list)
        self.new_button.grid(row=0, column=6, padx=5, pady=5)


        
        pdf_frame = tk.Frame(self.display_frame)
        pdf_frame.grid(row=7, column=0, columnspan=4, rowspan=3, sticky="nsew")
        pdf_frame.columnconfigure((0, 1, 2, 3), weight=1)
        pdf_frame.columnconfigure((0), weight=0)
        pdf_frame.rowconfigure((0, 1, 2), weight=1)
        pdf_frame.rowconfigure((3), weight=0)
        
        self.canvas_width = 800
        self.canvas_height = 600
        
        self.canvas = tk.Canvas(pdf_frame, bg="gray")
        self.canvas.grid(row=0, column=1, columnspan=2, rowspan=2, sticky="nsew")
        
        self.vertical_scrollbar = tk.Scrollbar(pdf_frame, orient=tk.VERTICAL, command=self.canvas.yview)
        self.vertical_scrollbar.grid(row=0, column=0, rowspan=3, sticky="nsew")
        self.canvas.configure(yscrollcommand=self.vertical_scrollbar.set)

        self.horizontal_scrollbar = tk.Scrollbar(pdf_frame, orient=tk.HORIZONTAL, command=self.canvas.xview)
        self.horizontal_scrollbar.grid(row=3, column=1, columnspan=3, sticky="nsew")
        self.canvas.configure(xscrollcommand=self.horizontal_scrollbar.set)
        
        self.pdf_document = None
        self.current_page_num = 0
        self.img_references = []
        self.pdf_path = ""
        
        self.getvalue_form.bind("<Return>", self.print_item)
        self.getvalue_form.bind("<Escape>", self.exit)
        
    def add_item(self, items, doc, selected_type, barcode, shop_name, color, size, qty):
        if (selected_type == "ITEM"):
            self.list_items.insert("", "end", text=str(items[0]), values=(items[2], barcode, items[1], color, size, float(qty), items[9], "0", items[10], shop_name))
    
    def show_PreViwe(self):
        text = ""
        page_width = 100
        page_hight = 35

        top = 5
        bottom = 5
        left = 5
        right = 5

        qty = 4
        columns = 2
        on_column = 1
        rows = qty/columns
        on_row = 1
        
        columns_width = 25
        row_hight = 11

        
        columns_spacing = 0
        row_spacing = 5

        x = 0
        y = 0
        b = 2 # for border 
        
        border = 1

        column_counted = 1
        count = 0
        
        shop_name =  "this is shop name space"
        name = "this is name space"
        code = "this is code space"
        p1 = "this is was price space"
        p2 = "this is now price space"
        barcode = "this is barcode space"
        size = "this is barcode space"
        color = "this is barcode space"
        
        for ph in range(page_hight):
            for pw in range(page_width):
                if pw == 0 or  pw == page_width-1:
                    text += '|'
                    continue
                if ph == 0 or ph == page_hight-1:
                    text += '-'
                    continue
                if ph == top*on_row and (pw > left*on_column and pw < (left*on_column)+columns_width) or \
                    ph == (top*on_row)+row_hight and (pw > left*on_column and pw < (left*on_column)+columns_width):
                    text += '.'
                    continue
                if pw == left*on_column and (ph > (top*on_row) and ph < (top*on_row)+row_hight) or \
                   pw == (left*on_column)+columns_width and (ph > (top*on_row) and ph < (top*on_row)+row_hight):
                    text += ':'
                    continue
                if pw > left*on_column+1+x and pw < (left*on_column)+columns_width-1-x and \
                   ph > top*on_row+1+y and ph < (top*on_row)+row_hight-1-y:
                    if ph == top*on_row+2 and pw-(left*on_column)-b < len(shop_name):
                        text += shop_name[pw-(left*on_column)-b]
                    elif ph == top*on_row+3 and pw-(left*on_column)-b < len(name):
                        text += name[pw-(left*on_column)-b]
                    elif ph == top*on_row+4 and pw-(left*on_column)-b < len(code):
                        text += code[pw-(left*on_column)-b]
                    elif ph == top*on_row+5 and pw-(left*on_column)-b < len(p1):
                        text += p1[pw-(left*on_column)-b]
                    elif ph == top*on_row+6 and pw-(left*on_column)-b < len(p2):
                        text += p2[pw-(left*on_column)-b]
                    elif ph == top*on_row+7 and pw-(left*on_column)-b < len(barcode):
                        text += barcode[pw-(left*on_column)-b]
                    elif ph == top*on_row+8 and pw-(left*on_column)-b < len(size):
                        text += size[pw-(left*on_column)-b]
                    elif ph == top*on_row+9 and pw-(left*on_column)-b < len(color):
                        text += color[pw-(left*on_column)-b]
                    else:
                        text += " "
                    continue
                text += " "
            text += '\n'
        ''' ---------------------------------------------------------
        |        ...................                              |
        |        .                 .                              |
        |        .                 .                              |
        |        .                 .                              |
        |        .                 .                              |
        |        .                 .                              |
        |        .                 .                              |
        |        ...................                              |
                                                                  |
        for i in self.list_items.get_children():
            item = self.list_items.item(i)['values']
            id = self.list_items.item(i)['text']
            text += str(item[9]) + "0\n" # shop name
            text += str(item[0]) + "1\n" # code
            text += str(item[2]) + "3\n" # name
            text += str(item[3]) + "4\n" # color
            text += str(item[4]) + "5\n" # size
            
            text += str(item[5]) + "6\n" # qty
            
            text += str(item[6]) + "7\n"
            text += str(item[7]) + "8\n"
            text += str(item[8]) + "9\n"
            text += str(item[1]) + "2\n" # barcode
            text += "\n"'''
        self.on_slip.config(text=text)
        
    def exit(self, event):
        self.getvalue_form.destroy()
        
    def change_focus(self, event):
        self.print_button.focus_set()
        
            
    def get_prev_slip(self):
        i = 0;
        '''if self.on_barid.cget('text') != "":
            i = int(self.on_barid.cget('text'))
        if not i-1 < 0:
            i -= 1
            self.on_barid.config(text=str(i))
            self.on_slip.config(text=str(self.slips[i][1]))
        else:
            i = len(self.slips)-1
            self.on_barid.config(text=str(i))
            self.on_slip.config(text=str(self.slips[i][1]))'''
            
    def print_item(self, a):
        print("printing : " + str(self.print_slip) + "splip : " + str(self.on_barid.cget('text')))
        '''if self.print_slip == 1:
            PrinterForm.print_slip(self, self.on_slip.cget('text'), 1) # TODO chack in setting if paper cut allowed'''
    
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

    def open_pdf(self):
        file_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])

        if file_path:
            self.pdf_path = file_path
            self.load_pdf(file_path)

    def load_pdf(self, file_path):
        if self.pdf_document:
            self.pdf_document.close()
        '''
        self.pdf_document = fitz.open(file_path)
        self.current_page_num = 0
        self.display_pages()
        #'''

    def display_pages(self):
        if not self.pdf_document:
            return
        '''
        self.canvas.delete("all")
        self.img_references = []
        X, Y = 0, 10
        canvas_height = 0
        canvas_width = 0

        for page_num in range(self.pdf_document.page_count):
            page = self.pdf_document.load_page(page_num)
            image = page.get_pixmap(matrix=fitz.Matrix(2, 2))

            img = Image.frombytes("RGB", [image.width, image.height], image.samples)
            img = ImageTk.PhotoImage(img)

            x = 0 #(self.canvas_width - img.width()) // 2  # Center horizontally
            y = Y
            Y = y + img.height()
            
            self.canvas.create_image(x, y, anchor=tk.NW, image=img)
            self.img_references.append(img)

            canvas_height = max(canvas_height, y + img.height())
            canvas_width = max(canvas_width, x + img.width())

        self.canvas.configure(scrollregion=(0, 0, canvas_width, canvas_height))
        #'''

    def print_pdf(self):
        if not self.pdf_document:
            return
        '''
        available_printers = win32print.EnumPrinters(2)
        printer_names = [printer[2] for printer in available_printers]

        if printer_names:
            dialog = PrinterDialog(self.root, printer_names)
            printer_name = dialog.result

            if printer_name:
                printer_handle = win32print.OpenPrinter(printer_name)

                try:
                    win32print.StartDocPrinter(printer_handle, 1, ("PDF Document", None, "RAW"))
                    win32print.StartPagePrinter(printer_handle)

                    for img_ref in self.img_references:
                        img_data = self.get_photo_image_data(img_ref)
                        win32print.WritePrinter(printer_handle, img_data, len(img_data))

                    win32print.EndPagePrinter(printer_handle)
                    win32print.EndDocPrinter(printer_handle)
                finally:
                    win32print.ClosePrinter(printer_handle)
        #'''

    def get_photo_image_data(self, photo_image):
        # Render the PhotoImage on a Canvas widget
        canvas = tk.Canvas(self.root, width=photo_image.width(), height=photo_image.height())
        canvas.create_image(0, 0, anchor=tk.NW, image=photo_image)
        '''
        # Take a screenshot of the canvas
        bbox=canvas.winfo_rootx()
        screenshot = ImageGrab.grab(bbox, canvas.winfo_rooty(),
                                     canvas.winfo_rootx() + canvas.winfo_width(),
                                     canvas.winfo_rooty() + canvas.winfo_height())
        
        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp_file:
            screenshot.save(temp_file, format="png")
            temp_filename = temp_file.name
        
        with open(temp_filename, "rb") as f:
            img_data = f.read()

        os.remove(temp_filename)
        return img_data
        #'''

                    
    def new_list(self):
        self.product_data=[]
    
    def generate_price_tag(self):
        if len(self.list_items.get_children()):
            pdf_path = "price_tags.pdf"
            '''
            c = reportlab_canvas.Canvas(pdf_path, pagesize=letter)
            page_width, page_height = int(self.Pag_width_entry.get()), int(self.Pag_hight_entry.get())
            if int(self.Pag_width_entry.get())+ int(self.Pag_hight_entry.get()) > 0:
                c = reportlab_canvas.Canvas(pdf_path, pagesize=(page_width, page_height))

            num_columns = int(self.product_num_columns_entry.get())
            on_columns = 0
            self.tk_images = []  # Add this line in the __init__ method
            
            barcode_size = float(self.barcode_size_entry.get()) if self.barcode_size_entry.get() else 25
            price_size = float(self.product_price_entry.get()) if self.product_price_entry.get() else 8
            name_size = float(self.product_name_entry.get()) if self.product_name_entry.get() else 8
            
            # Define spacing and dimensions
            price_tag_width = int(self.product_bordersW_entry.get())
            price_tag_height = int(self.product_bordersH_entry.get())
            columns_spacing = int(self.borders_gap_columen_entry.get())# gap bettwen columens
            row_spacing = int(self.borders_gap_row_entry.get())# gap bettwen rows
            bottom = int(self.borders_bottom_entry.get())# gap bettwen bottom
            left = int(self.borders_left_entry.get())# gap bettwen left
            top = int(self.borders_top_entry.get())# gap bettwen top
            
            border_width = 2  # Border width
            border_color = "black"

            x_offset = 1
            y_offset = 1

            current_page_height = page_height  # Initialize with the page height            
            for product_idx, product in enumerate(self.list_items.get_children()):
                i = self.list_items.item(product)
                print(str(self.list_items.item(product)))
                iv = i['values']
                id = i['text']
                code, barcode_, item_name,color_,size, qty, price, price_after, tax, shop_name = iv
                qty = int(float(qty))
                print(str(item_name) + "item anem / price = " + str(price))
                #TODO: change barcode size
                if barcode_ == "":
                    barcode_ = "00000000000"
                for idx, i in enumerate(range(qty)):
                    # Calculate row and column for grid
                    row = on_columns // num_columns
                    column = on_columns % num_columns
                    
                    max_barcode_width = int(price_tag_width - 2 * columns_spacing)
                    max_barcode_height = int(price_tag_height - row_spacing)
                    
                    x_position = left + column * (price_tag_width + columns_spacing)
                    y_position = top + row * (price_tag_height + row_spacing)
                    
                    # Draw border around each individual price tag
                    c.rect(
                        x_position, y_position,
                        price_tag_width, price_tag_height,
                        stroke=1, fill=0
                    )

                    # Draw other elements within the price tag box
                    c.setFont("Helvetica", name_size)
                    c.drawString(
                        x_position + border_width,
                        y_position + (price_tag_height-name_size)-border_width,
                        "Product: " + item_name
                    )

                    c.setFont("Helvetica", price_size)
                    c.drawString(
                        x_position + border_width,
                        y_position + ((price_tag_height-name_size)-border_width)-price_size,
                        "Price: " + price
                    )

                    # Generate and draw barcode (modify this part based on your barcode rendering logic)
                    barcode_type = self.barcode_type_map.get(self.barcode_type_var.get(), barcode.Code39)
                    # barcode_image = barcode_type(product['barcode'], writer=ImageWriter(), add_checksum=False).render()
                    barcode_image = barcode.Code39(barcode_, writer=ImageWriter(), add_checksum=False).render()

                    


                    barcode_height = min(int(25), max_barcode_height)
                    barcode_width = int(barcode_image.width * (barcode_height / barcode_image.height))

                    barcode_x = x_position + border_width
                    barcode_y = y_position + 2
                    # Save the resized barcode image as a temporary file
                    temp_barcode_path = "temp_barcode.png"
                    barcode_image.save(temp_barcode_path)

                    # Draw the barcode image from the temporary file
                    c.drawImage(temp_barcode_path, barcode_x, barcode_y, width=barcode_width, height=barcode_height)
                    # Check if there's enough space for the new row on the current page
                    
                    on_columns += 1
                    
                    x_position += price_tag_width
                    if on_columns == num_columns:
                        x_position = 0
                        on_columns = 0
                        y_position += price_tag_height
                        
                        # Calculate the height of the current row
                        row_height = y_position + price_tag_height
                        if row_height + y_position + price_tag_height >= page_height:
                            row_height = 0  # Reset the current page height
                            c.showPage()  # Create a new page

            c.save()
            #'''
            messagebox.showinfo("Info", f"PDF saved successfully as {pdf_path}")
            self.pdf_path = pdf_path
            self.load_pdf(pdf_path)
        else:
            messagebox.showwarning("Warning", "No products to preview!")

if __name__ == "__main__":
    root = tk.Tk()
    app = PrintPriceTagFrame(root)
    root.mainloop()

