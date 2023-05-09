import tkinter as tk
from tkinter import ttk

class DocEditForm(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)

        # Child frame 1 - TOP_FORM
        top_form = tk.Frame(self)
        top_form.grid(row=0, column=0, columnspan=3, sticky="nsew")

        top_form.grid_columnconfigure(0, weight=5)
        top_form.grid_columnconfigure(1, weight=5)
        top_form.grid_columnconfigure(2, weight=5)
        top_form.grid_columnconfigure(3, weight=5)
        top_form.grid_columnconfigure(4, weight=5)
        top_form.grid_columnconfigure(5, weight=5)
        top_form.grid_columnconfigure(6, weight=5)
        top_form.grid_rowconfigure(0, weight=5)
        top_form.grid_rowconfigure(1, weight=5)
        top_form.grid_rowconfigure(2, weight=5)
        
        # Label "Number" and Entry
        label_number = tk.Label(top_form, text="Number")
        label_number.grid(row=0, column=0)
        entry_number = tk.Entry(top_form)
        entry_number.grid(row=0, column=1)

        # Label "Data" and Entry
        label_data = tk.Label(top_form, text="Data")
        label_data.grid(row=0, column=4)
        entry_data = tk.Entry(top_form)
        entry_data.grid(row=0, column=5)

        # Checkbox "Paid"
        checkbox_paid = tk.Checkbutton(top_form, text="Paid")
        checkbox_paid.grid(row=0, column=6)

        # Label "External Doc" and Entry
        label_external_doc = tk.Label(top_form, text="External Document")
        label_external_doc.grid(row=1, column=0)
        entry_external_doc = tk.Entry(top_form)
        entry_external_doc.grid(row=1, column=1)

        # Label "Due Date" and Entry
        label_due_date = tk.Label(top_form, text="Due Date")
        label_due_date.grid(row=1, column=4)
        entry_due_date = tk.Entry(top_form)
        entry_due_date.grid(row=1, column=5)

        # Label "Customer" and Entry
        label_customer = tk.Label(top_form, text="Customer")
        label_customer.grid(row=2, column=0)
        entry_customer = tk.Entry(top_form)
        entry_customer.grid(row=2, column=1)

        # Button
        button = tk.Button(top_form, text="Button")
        button.grid(row=2, column=4)

        # Label "Stock Date" and Entry
        label_stock_date = tk.Label(top_form, text="Stock Date")
        label_stock_date.grid(row=2, column=5)
        entry_stock_date = tk.Entry(top_form)
        entry_stock_date.grid(row=2, column=6)



        
        # Child frame 2 - SEARCH_FORM
        search_form = tk.Frame(self)
        search_form.grid(row=1, column=0, rowspan=4, sticky="nsew")

        # Child frame 3 - CENTER_FORM
        center_form = tk.Frame(self)
        center_form.grid(row=1, column=1, rowspan=3, columnspan=2, sticky="nsew")

        # Child frame 4 - INFO_FORM
        info_form = tk.Frame(self)
        info_form.grid(row=4, column=1, columnspan=3, sticky="nsew")

        # Configure column and row weights
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=1)
        self.grid_rowconfigure(4, weight=1)

        # Notebook widget - CENTER_NOTEBOK
        center_notebook = ttk.Notebook(center_form)
        center_notebook.pack(fill="both", expand=True)

        # Tab 1 - Items
        items_tab = tk.Frame(center_notebook)
        center_notebook.add(items_tab, text="Items")

        # Tab 2 - Payment
        payment_tab = tk.Frame(center_notebook)
        center_notebook.add(payment_tab, text="Payment")

# Create the root window
root = tk.Tk()

# Create an instance of the DocEditForm and display it in the root window
doc_edit_form = DocEditForm(root)
doc_edit_form.pack(fill="both", expand=True)

# Start the Tkinter event loop
root.mainloop()