#import win32print
import tkinter as tk
from tkinter import ttk
import sqlite3, os

data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data'))
db_path = os.path.join(data_dir, 'my_database.db')
conn = sqlite3.connect(db_path)
cursor = conn.cursor()
printer_name = ""

class PrinterForm(tk.Tk):
    def __init__(self, master):
        self.master = master
        
    def load_printer(self):
        cursor.execute("SELECT * FROM setting WHERE user_name = ?", (self.user,))
        b = cursor.fetchall()
        if len(b) >= 0:
            if b[0][3] == "":
                print("sitting : " + str(b))
                printer_name = "EPSON TM-T88V Receipt"
                # TODO MAKE USER CHOOSE PRINTER
            else:
                printer_name = b[0][3] # getting printer
        return printer_name
                
    def open_drower(self):
        printer_name = PrinterForm.load_printer(self)
        print("printer : " + str(printer_name))
        # Prepare the printer properties
        '''
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
            '''
    
    def print_slip(self, text, cut):
        printer_name = PrinterForm.load_printer(self)
        print("printer : " + str(printer_name))
        # Prepare the printer properties
        '''
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
    
                for _ in range(20): # TODO get how how mach space to live befor cuting to change 20 ranges
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
            '''
    
    def print_text_with_dialog(self, text):
        # Load the saved printer driver choice
        '''
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
            '''
        pass
