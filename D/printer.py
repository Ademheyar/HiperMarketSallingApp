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
        '''with open('printer.txt', 'r') as f:
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

# Example usage
text_to_print = \
"032753 P=150 B=100 | 022018 P=0 B=170\n" \
"022024 P=0 B=220 | 018363 P=140 B=1 480\n" \
"016518 P=125 B=125 | 017733 P=180 B=320\n" \
"022157 P=50 B=110 | 017844 P=200 B=300\n" \
"018201 P=100 B=80 | 018220 P=50 B=90\n" \
"018264 P=100 B=150 | 018435 P=100 B=150\n" \
"018464 P=50 B=100 | 018527 P=130 B=180\n" \
"018624 P=100 B=150 | 018732 P=50 B=200\n" \
"018733 P=150 B=650 | 018824 P=100 B=120\n" \
"018892 | 018967 P=100 B=150\n" \
"019371 P=70 B=70 | 019400 P=260 B=220\n" \
"019410 P=50 B=130 | 019493 P=100 B=250\n" \
"019528 P=100 B=120 | 019541 P=200 B=500\n" \
"019596 P=100 B=80 | 019640 P=120 B=130\n" \
"019776 P=100 B=350 | 019801 P=80 B=200\n" \
"019847 P=70 B=100 | 019891 P=100 B=130\n" \
"020102 P=200 B=400 | 020156 P=100 B=180\n" \
"020273 P=100 B=150 | 021037 P=50 B=220\n" \
"020360 P=100 B=200 | 020416 P=80 B=100\n" \
"020461 P=130 B=200 | 020498 \n" \
"020544 P=60 B=90 | 020595 P=100 B=150\n" \
"020630 P=70 B=70 | 020677 P=50 B=100\n" \
"020682 P=100 B=260 |020899 P=200 B=200\n" \
"021104 P=50 B=230 | 021115 P=100 B=200\n" \
"021125 P=50 B=0 | 021227 P=50 B=150\n" \
"021320 P=140 B=110 | 021329 P=50 B=130\n" \
"021507 P=100 B=150 | 021639 P=165 B=135\n" \
"021996 P=250 B=0 | 025901 P=100 B=280\n" \
"022158 P=50 B=110 | 022219 P=100 B=130\n" \
"022233 P=200 B=200 | 022280 P=50 B=200\n" \
"022335 P=50 B=330 | 023150 P=80 B=380\n" \
"035617 P=50 B=1 380 | 024521 P=60 B=115\n" \
"024538 P=100 B=200 | 024945 P=50 B=180\n" \
"025095 P=300 B=0 | 025213 P=100 B=150\n" \
"025765 P=50 B=330 | 026257 P=100 B=200\n" \
"027115 P=100 B=200 | 018892 P=100 B=340\n" \
"027472 P=150 B=430 | 027506 P=200 B=320\n" \
"027551 P=150 B=310 | 028488 P=200 B=230\n" \
"028589 P=300 B=770 | 028789 P=200 B=300\n" \
"030096 P=100 B=150 | 030306 P=150 B=230\n" \
"031398 P=100 B=80 | 031453 P=50 B=250\n" \
"031911 P=100 B=240 | 032078 P=160 B=600\n" \
"032102 P=200 B=260 | 033173 P=100 B=150\n" \
"033637 P=50 B=150 | 034266 P=50 B=390\n" \
              "thank you for shoping with us\n"\
              "thank you for shoping with us\n"\
              "thank you for shoping with us\n"\
              "thank you for shoping with us\n"\
              "thank you for shoping with us\n"

# Call the function to print the text with the printer driver dialog
#print_text_with_dialog(text_to_print)
