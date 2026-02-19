import tkinter as tk
from tkinter import ttk
import sqlite3, os

data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data'))
db_path = os.path.join(data_dir, 'my_database.db')
from D.Security import *

# TODO: user can change name, or password in this form
# TODO: user can add sub user depanding on it usertype
class UserInfoForm(tk.Tk):
    def __init__(self, master, User):
        self.master = master
        
        # create a Toplevel window for the payment form
        self.getvalue_form = tk.Toplevel(self.master)
        self.getvalue_form.title("endday Form")

        # calculate the center coordinates of the screen
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        x = (screen_width / 2) - (300 / 2)  # 500 is the width of the Payment Form window
        y = (screen_height / 2) - (300 / 2)  # 500 is the height of the Payment Form window

        ''' set the position of the Payment Form window to center
        #self.getvalue_form.geometry(f"300x400+{int(x)}+{int(y)}")
        #self.getvalue_form.grid_rowconfigure(0, weight=1)
        self.getvalue_form.grid_rowconfigure(1, weight=1)
        self.getvalue_form.grid_rowconfigure(2, weight=1)
        self.getvalue_form.grid_rowconfigure(3, weight=1)
        self.getvalue_form.grid_rowconfigure(4, weight=1)
        self.getvalue_form.grid_columnconfigure(0, weight=1)
        self.getvalue_form.grid_columnconfigure(1, weight=1)
        self.getvalue_form.grid_columnconfigure(2, weight=1)
        self.getvalue_form.grid_columnconfigure(3, weight=1)'''
        
        def logout_fun():
            self.master.grid_remove()
            self.getvalue_form.destroy()
            Security_get_user(self.master)
        
        self._label0 = tk.Label(self.getvalue_form, text="Loged User Informations", font=("Arial", 14))
        self._label0.grid(row=0, column=2, padx=10, pady=10)
        
        self.User_Name_label = tk.Label(self.getvalue_form, text="User Name : " + User['User_name'], font=("Arial", 14))
        self.User_Name_label.grid(row=2, column=0, padx=10, pady=10)
        self.User_Type_label = tk.Label(self.getvalue_form, text="User Type : ", font=("Arial", 14))
        self.User_Type_label.grid(row=3, column=0, padx=10, pady=10)
        self.User_State_label = tk.Label(self.getvalue_form, text="User State : ", font=("Arial", 14))
        self.User_State_label.grid(row=4, column=0, padx=10, pady=10)
        self.User_Shops_label = tk.Label(self.getvalue_form, text="User Shops : ", font=("Arial", 14))
        self.User_Shops_label.grid(row=5, column=0, padx=10, pady=10)
        
        self.logout_button = tk.Button(self.getvalue_form, text="Log Out", bg="red", fg="white", font=("Arial", 12), command=lambda : logout_fun())
        self.logout_button.grid(row=7, column=2)

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
