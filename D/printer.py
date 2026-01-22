import win32print
import tkinter as tk
from tkinter import ttk
import sqlite3, os
from tkinter import simpledialog

import json
import ast

data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data'))
db_path = os.path.join(data_dir, 'my_database.db')
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

printer_name = ""
def list_available_printers():
    printers = []
    #'''
    printer_info = win32print.EnumPrinters(win32print.PRINTER_ENUM_LOCAL, None, 1)
    for printer in printer_info:
        printers.append(printer[2])
    #'''
    return printers


class PrinterSelectionDialog(tk.Toplevel):
    def __init__(self, master, printers):
        super().__init__(master)
        self.printers = printers
        self.selected_printer = None
        self.title("Select Printer")
        self.geometry("300x200")
        self.initUI()

    def initUI(self):
        label = tk.Label(self, text="Select a Printer:")
        label.pack(pady=10)
        
        self.printer_var = tk.StringVar()
        self.printer_var.set(self.printers[0] if self.printers else "")
        
        printer_menu = tk.OptionMenu(self, self.printer_var, *self.printers)
        printer_menu.pack(pady=10)

        
        self.issave = tk.IntVar()
        self.change_entry = tk.Checkbutton(self, text='REMAMBER MY CHOICE', variable=self.issave)
        self.change_entry.pack(pady=10)
        
        select_button = tk.Button(self, text="Select", command=self.select_printer)
        select_button.pack(pady=10)

    def select_printer(self):
        self.selected_printer = self.printer_var.get()
        self.destroy()

class PrinterForm(tk.Tk):
    def __init__(self, master):
        self.master = master

    def list_available_printers(self):
        printers = []
        #'''
        printer_info = win32print.EnumPrinters(win32print.PRINTER_ENUM_LOCAL, None, 1)
        for printer in printer_info:
            printers.append(printer[2])  # Extract printer names from the tuple
        #'''
        return printers

    def choose_printer(self):
        printers = self.list_available_printers()
        dialog = PrinterSelectionDialog(self, printers)
        self.wait_window(dialog)
        selected_printer = dialog.selected_printer
        if selected_printer:
            return selected_printer
        else:
            return "AnyDesk Printer"
    
    def load_printer(self, user_info):
        selected_printer = "DEFALUET"
        printers = list_available_printers()
        print("user " + str(user_info) + "found ")
        cursor.execute("SELECT * FROM setting WHERE User_id = ?", (int(user_info['User_id']),))
        b = cursor.fetchall()
        print("user " + str(user_info['User_name']) + "found " +str(b))
        if b and len(b) > 0 and b[0][3] != "" and b[0][3] in printers:
            selected_printer = b[0][3] # getting printer
        else:
            print("sitting : " + str(b))
            dialog = PrinterSelectionDialog(self, printers)
            self.wait_window(dialog)
            selected_printer = dialog.selected_printer
            if selected_printer:
                if dialog.issave.get():
                    if b:
                        cursor.execute('UPDATE setting SET printer=? WHERE User_id=?', (selected_printer, user_info['User_id']))
                        pass
                    else:
                        cursor.execute('INSERT INTO setting (User_id, printer) VALUES (?, ?)', (self.user['User_id'], selected_printer))
                        pass
                    # Commit the changes to the database
                    conn.commit()
        return selected_printer
                
    def open_drower(self, user_info):
        printer_name = PrinterForm.load_printer(self, user_info)
        print("printer : " + str(printer_name))
        # Prepare the printer properties
        #'''
        printer_props = {
            "DesiredAccess": win32print.PRINTER_ALL_ACCESS,
            "PrinterName": printer_name,
            "Attributes": win32print.PRINTER_ATTRIBUTE_DIRECT,
        }

        # Open the printer and get a handle to it
        print("Open the printer and get a handle to it\n")
        printer_handle = win32print.OpenPrinter(printer_name)
        try:
            print("Prepare the document info\n")
            # Prepare the document info
            doc_info = ('print', None, 'RAW')
            
            print("Start the print job\n")
            # Start the print job
            try:
                job_handle = win32print.StartDocPrinter(printer_handle, 1, doc_info)
            except Exception as e:
                print("Error starting document: " + str(e))
                return


            try:
                print("Start a new page\n")
                # Start a new page
                win32print.StartPagePrinter(printer_handle)
                
                # Send a command to open the cash drawer
                # Adjust the command based on the printer and cash drawer model
                print("Send a command to open the cash drawer\n")
                print("You may need to adjust the command based on the printer model\n")
                cash_drawer_command = b'\x1B\x70\x00\x19\xFA'
                win32print.WritePrinter(printer_handle, cash_drawer_command)

            finally:
                print("End the print job\n")
                # End the print job
                win32print.EndDocPrinter(printer_handle)

        finally:
            print("Close the printer handle\n")
            # Close the printer handle
            win32print.ClosePrinter(printer_handle)
            # '''
    
    def print_slip(self, user, at_shop, text, cut):
        printer_name = PrinterForm.load_printer(self, user)
        if printer_name == "":
            return
        hight = 5
        if at_shop and at_shop['Shop_Slip_Settings']:
            sittings = json.loads(at_shop['Shop_Slip_Settings'])
            hight = sittings[0][1]
        print("printer : " + str(hight))
        print("printer : " + str(printer_name))
        # Prepare the printer properties
        #'''
        printer_props = {
            "DesiredAccess": win32print.PRINTER_ALL_ACCESS,
            "PrinterName": printer_name,
            "Attributes": win32print.PRINTER_ATTRIBUTE_DIRECT,
        }

        # Open the printer and get a handle to it
        print("Open the printer and get a handle to it\n")
        printer_handle = win32print.OpenPrinter(printer_name)
        try:
            print("Prepare the document info\n")
            # Prepare the document info
            doc_info = ('print', None, 'RAW')
            
            print("Start the print job\n")
            # Start the print job
            job_handle = win32print.StartDocPrinter(printer_handle, 1, doc_info)

            try:
                print("Start a new page\n")
                # Start a new page
                win32print.StartPagePrinter(printer_handle)
                
                print("Send the text to the printer\n")
                # Send the text to the printer
                win32print.WritePrinter(printer_handle, text.encode("utf-8"))
    
                for _ in range(int(hight)):
                    paper_cut_where = b'\x0A'
                    win32print.WritePrinter(printer_handle, paper_cut_where)

                if cut:
                    # Send a paper-cut command to the printer
                    # You may need to adjust the command based on the printer model
                    print("Send a paper-cut command to the printere\n")
                    print("You may need to adjust the command based on the printer model\n")
                    paper_cut_command = b'\x1D\x56\x01'
                    win32print.WritePrinter(printer_handle, paper_cut_command)
            finally:
                print("End the print job\n")
                # End the print job
                win32print.EndDocPrinter(printer_handle)

        finally:
            print("Close the printer handle\n")
            # Close the printer handle
            win32print.ClosePrinter(printer_handle)
            # '''
    
    def print_text_with_dialog(self, text):
        # Load the saved printer driver choice
        #'''
        with open('printer.txt', 'r') as f:
            printer_name = f.read().strip()
        # Get the default printer name
        #printer_name = win32print.GetDefaultPrinter()

        # Prepare the printer properties
        printer_props = {
            "DesiredAccess": win32print.PRINTER_ALL_ACCESS,
            "PrinterName": printer_name,
            "Attributes": win32print.PRINTER_ATTRIBUTE_DIRECT,
        }

        # Open the printer and get a handle to it
        print("Open the printer and get a handle to it\n")
        printer_handle = win32print.OpenPrinter(printer_name)
        try:
            print("Prepare the document info\n")
            # Prepare the document info
            doc_info = ('print', None, 'RAW')
            
            print("Start the print job\n")
            # Start the print job
            job_handle = win32print.StartDocPrinter(printer_handle, 1, doc_info)

            try:
                print("Start a new page\n")
                # Start a new page
                win32print.StartPagePrinter(printer_handle)
                
                print("Send the text to the printer\n")
                # Send the text to the printer
                twiths = (text + ".\n.\n")
                win32print.WritePrinter(printer_handle, twiths.encode("utf-8"))


     
                # Send a paper-cut command to the printer
                # You may need to adjust the command based on the printer model
                print("Send a paper-cut command to the printere\n")
                print("You may need to adjust the command based on the printer model\n")
                paper_cut_command = b'\x1D\x56\x01'
                win32print.WritePrinter(printer_handle, paper_cut_command)

                # Send a command to open the cash drawer
                # Adjust the command based on the printer and cash drawer model
                print("Send a command to open the cash drawer\n")
                print("You may need to adjust the command based on the printer model\n")
                cash_drawer_command = b'\x1B\x70\x00\x19\xFA'
                win32print.WritePrinter(printer_handle, cash_drawer_command)

            finally:
                print("End the print job\n")
                # End the print job
                win32print.EndDocPrinter(printer_handle)

        finally:
            print("Close the printer handle\n")
            # Close the printer handle
            win32print.ClosePrinter(printer_handle)
           # '''
        pass
