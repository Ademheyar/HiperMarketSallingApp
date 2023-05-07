import tkinter as tk
from tkinter import ttk
import sqlite3, os

data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data'))
db_path = os.path.join(data_dir, 'my_database.db')
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

class EnddayForm(tk.Tk):
    def __init__(self, master):
        self.master = master
        
        
        # create a Toplevel window for the payment form
        self.getvalue_form = tk.Toplevel(self.master)
        self.getvalue_form.title("endday Form")

        # calculate the center coordinates of the screen
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        x = (screen_width / 2) - (300 / 2)  # 500 is the width of the Payment Form window
        y = (screen_height / 2) - (300 / 2)  # 500 is the height of the Payment Form window

        # set the position of the Payment Form window to center
        # TODO: list z report for current day and history z reports for pev days but in notbook 
        # TODO: TO Print dayly, weekly, monthly and yearly report as user whats
        
        # show the Payment Form window
        self.getvalue_form.transient(self.master)
        self.getvalue_form.grab_set()
        self.master.wait_window(self.getvalue_form)

    def add_num(self, text):
        # Get the current value of the Entry widget
        current_value = self.include_var.get()
        
        if text == "clean":
            # Clear the Entry widget
            self.include_var.set("")
            self.username_entry.delete(0)
        elif text == "":
            # Do nothing if the button is "+", "-", "0", ".", or "enter"
            pass
        elif text == "enter":
            try:
                # Attempt to convert the current value to a float
                self.value = float(current_value)
                # Call the give_value method to set self.vv and destroy the Toplevel window
                self.getvalue_form.destroy()
            except ValueError:
                # If the current value cannot be converted to a float, do nothing
                pass
        elif "." in current_value and text == ".":
            # Do nothing if the current value already contains a decimal point
            pass
        else:
            # Append the button text to the current value of the Entry widget
            self.include_var.set(current_value + text)
