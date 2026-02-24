from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import tempfile
import os
import win32print
import tkinter as tk
from tkinter.simpledialog import Dialog

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

def generate_pdf(pdf_path):
    c = canvas.Canvas(pdf_path, pagesize=letter)

    # Add your content to the PDF here
    c.drawString(100, 700, "Product Name: Sample Product")
    c.drawString(100, 680, "Price: $10.99")
    # ... Add more content as needed

    c.save()

def print_pdf(pdf_path, printer_name):
    printer_handle = win32print.OpenPrinter(printer_name)

    try:
        win32print.StartDocPrinter(printer_handle, 1, ("PDF Document", None, "RAW"))
        win32print.StartPagePrinter(printer_handle)

        with open(pdf_path, "rb") as f:
            
            pdf_data = f.read()
        print(str(pdf_data))
        #win32print.WritePrinter(printer_handle, pdf_data)  # Remove len(pdf_data)

        win32print.EndPagePrinter(printer_handle)
        win32print.EndDocPrinter(printer_handle)
    finally:
        win32print.ClosePrinter(printer_handle)


def main():
    # Get available printer names
    printer_names = [printer[2] for printer in win32print.EnumPrinters(2)]

    if not printer_names:
        print("No printers available.")
        return

    # Display the printer selection dialog
    root = tk.Tk()
    dialog = PrinterDialog(root, printer_names)
    root.mainloop()
    
    if dialog.result:
        # Generate a temporary PDF file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
            temp_pdf_path = temp_file.name

        generate_pdf(temp_pdf_path)

        # Print the generated PDF using the selected printer
        print_pdf(temp_pdf_path, dialog.result)

        os.remove(temp_pdf_path)  # Clean up the temporary PDF file

if __name__ == "__main__":
    main()
