import tkinter as tk
from tkinter import ttk
import sqlite3
from D.Peymentsplit import PaymentForm
from D.GetVALUE import GetvalueForm

conn = sqlite3.connect("my_database.db")
cursor = conn.cursor()

class ApproveFrame(tk.Frame):
    def __init__(self, master, tree):

        tk.Frame.__init__(self, master)

        self.tree = tree

        # Create a new Toplevel window for the value form
        self.getvalue_form = tk.Toplevel(self.master)
        self.getvalue_form.title("Selector Form")

        # Calculate the center coordinates of the screen
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        x = (screen_width / 2) - (500 / 2)  # 500 is the width of the Payment Form window
        y = (screen_height / 2) - (500 / 2)  # 500 is the height of the Payment Form window

        # Set the position of the Payment Form window to center
        self.getvalue_form.geometry(f"{int(screen_width)}x{int(screen_height)}+{int(x)}+{int(y)}")

        # Create a listbox for the items
        self.list_items = tk.Listbox(self.getvalue_form)
        self.list_items.pack(side="left", fill="both", expand=True)

        # Create a frame for buttons and labels
        self.buttons_frame = tk.Frame(self.getvalue_form, bg="brown")
        self.buttons_frame.pack(side="left", fill="both", expand=True)

        # Create labels for the total items, price, discountmain_frame, tax, and total
        self.total_items_label = tk.Label(self.buttons_frame, text="Total Items : 0", bg="green", fg="white", font=("Arial", 15))
        self.total_items_label.grid(row=0, column=1, sticky="nsew")
        self.total_price_label = tk.Label(self.buttons_frame, text="Total Price : 0", bg="green", fg="white", font=("Arial", 15))
        self.total_price_label.grid(row=1, column=1, sticky="nsew")
        self.total_discount_label = tk.Label(self.buttons_frame, text="Total Discount : 0", bg="green", fg="white", font=("Arial", 15))
        self.total_discount_label.grid(row=2, column=1, sticky="nsew")
        self.total_tax_label = tk.Label(self.buttons_frame, text="Total Tax : 0", bg="green", fg="white", font=("Arial", 15))
        self.total_tax_label.grid(row=3, column=1, sticky="nsew")
        self.total_label = tk.Label(self.buttons_frame, text="Total : 0", bg="green", fg="white", font=("Arial", 15))
        self.total_label.grid(row=4, column=1, sticky="nsew")

        # Create an undo button
        self.undo_button = tk.Button(self.buttons_frame, text="Undo", bg="orange", fg="white", font=("Arial", 15), command=self.undo_item)
        self.undo_button.grid(row=5, column=1, sticky="nsew")

        # Create continue Button
        self.continue_button = ttk.Button(self.buttons_frame, text="Continue", command=self.getvalue_form.destroy)
        self.continue_button.grid(row=6, column=1, sticky="nsew")
        self.update_items()

    def undo_item(self):
        pass
    
    def call_manager(self):
        pass
    
    # Create the function to update the item list and the total labels
    def update_items(self):

        # Clear any existing items in the listbox
        self.list_items.delete(0, tk.END)

        total_items = 0
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
        self.total_tax_label.config(text=f"Total Tax : "  )