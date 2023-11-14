import tkinter as tk
from tkinter import ttk
import sqlite3, os

data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data'))
db_path = os.path.join(data_dir, 'my_database.db')
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

class GetvalueForm(tk.Tk):
    def __init__(self, master, txt, title):
        self.master = master
        self.value = None
        self.first = True
        # create a Toplevel window for the payment form
        self.getvalue_form = tk.Toplevel(self.master)
        self.getvalue_form.title(title)

        # calculate the center coordinates of the screen
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        x = (screen_width / 2) - (300 / 2)  # 500 is the width of the Payment Form window
        y = (screen_height / 2) - (300 / 2)  # 500 is the height of the Payment Form window

        # set the position of the Payment Form window to center
        self.getvalue_form.geometry(f"300x400+{int(x)}+{int(y)}")
        self.getvalue_form.grid_rowconfigure(0, weight=1)
        self.getvalue_form.grid_rowconfigure(1, weight=1)
        self.getvalue_form.grid_rowconfigure(2, weight=1)
        self.getvalue_form.grid_rowconfigure(3, weight=1)
        self.getvalue_form.grid_rowconfigure(4, weight=1)
        self.getvalue_form.grid_columnconfigure(0, weight=1)
        self.getvalue_form.grid_columnconfigure(1, weight=1)
        self.getvalue_form.grid_columnconfigure(2, weight=1)
        self.getvalue_form.grid_columnconfigure(3, weight=1)

        self.include_var = tk.StringVar()
        self.get_amount_entry = tk.Entry(
            self.getvalue_form, textvariable=self.include_var, width=15, font=("Arial", 15), justify="right"
        )
        self.get_amount_entry.insert(0, txt)
        self.get_amount_entry.grid(row=0, column=0, sticky="nsew", columnspan=4)

        # Create 4 button widgets and grid(row=0, column=0, sticky="nsew")
        self.button1 = tk.Button(
            self.getvalue_form, text="7", font=("Arial", 15), command=lambda: self.add_num(None, "7")
        )
        self.button1.grid(row=1, column=0, sticky="nsew")
        self.button2 = tk.Button(
            self.getvalue_form, text="8", font=("Arial", 15), command=lambda: self.add_num(None, "8")
        )
        self.button2.grid(row=1, column=1, sticky="nsew")
        self.button3 = tk.Button(
            self.getvalue_form, text="9", font=("Arial", 15), command=lambda: self.add_num(None, "9")
        )
        self.button3.grid(row=1, column=2, sticky="nsew")
        self.button4 = tk.Button(
            self.getvalue_form, text="clean", font=("Arial", 15), command=lambda: self.add_num(None, "clean")
        )
        self.button4.grid(row=1, column=3, sticky="nsew")

        self.button5 = tk.Button(
            self.getvalue_form, text="4", font=("Arial", 15), command=lambda: self.add_num(None, "4")
        )
        self.button5.grid(row=2, column=0, sticky="nsew")
        self.button6 = tk.Button(
            self.getvalue_form, text="5", font=("Arial", 15), command=lambda: self.add_num(None, "5")
        )
        self.button6.grid(row=2, column=1, sticky="nsew")
        self.button7 = tk.Button(
            self.getvalue_form, text="6", font=("Arial", 15), command=lambda: self.add_num(None, "6")
        )
        self.button7.grid(row=2, column=2, sticky="nsew")
        self.button8 = tk.Button(
            self.getvalue_form, text="+", font=("Arial", 15), command=lambda: self.add_num(None, "")
        )
        self.button8.grid(row=2, column=3, sticky="nsew")

        self.button9 = tk.Button(
            self.getvalue_form, text="1", font=("Arial", 15), command=lambda: self.add_num(None, "1")
        )
        self.button9.grid(row=3, column=0, sticky="nsew")
        self.button10 = tk.Button(
            self.getvalue_form, text="2", font=("Arial", 15), command=lambda: self.add_num(None, "2")
        )
        self.button10.grid(row=3, column=1, sticky="nsew")
        self.button11 = tk.Button(
            self.getvalue_form, text="3", font=("Arial", 15), command=lambda: self.add_num(None, "3")
        )
        self.button11.grid(row=3, column=2, sticky="nsew")
        self.button12 = tk.Button(
            self.getvalue_form, text="-", font=("Arial", 15), command=lambda: self.add_num(None, "")
        )
        self.button12.grid(row=3, column=3, sticky="nsew")

        self.button13 = tk.Button(
            self.getvalue_form, text="0", font=("Arial", 15), command=lambda: self.add_num(None,"0")
        )
        self.button13.grid(row=4, column=0, sticky="nsew")
        self.button14 = tk.Button(
            self.getvalue_form, text=".", font=("Arial", 15), command=lambda: self.add_num(None, ".")
        )
        self.button14.grid(row=4, column=1, sticky="nsew")
        self.button15 = tk.Button(
            self.getvalue_form, text="enter", font=("Arial", 15), command=lambda: self.add_num(None,"enter")
        )
        self.button15.grid(row=4, column=2, sticky="nsew")
        self.close_btn = tk.Button(
            self.getvalue_form, text="Close", command=lambda: self.getvalue_form.destroy()
        )
        self.close_btn.grid(row=4, column=3, sticky="nsew")

        # show the Payment Form window
        self.getvalue_form.transient(self.master)
        self.getvalue_form.grab_set()
        self.getvalue_form.focus_set()
        self.getvalue_form.bind("<KeyPress>", lambda event: self.add_num(event, ""))
        self.getvalue_form.transient(self.master)
        self.master.wait_window(self.getvalue_form)

    def add_num(self, event, text):
        # Get the current value of the Entry widget
        current_value = self.include_var.get()
        if event and text == "":
            text = event.keysym
        print("text : " + str(text))

        if text in ["clean", "Escape"]:
            # Clear the Entry widget
            if not self.include_var.get() == "":
                self.include_var.set("")
                self.get_amount_entry.delete(0, 'end')
            elif text == "Escape":
                self.getvalue_form.destroy()
        elif text == "BackSpace":
            self.get_amount_entry.delete(len(self.get_amount_entry.get())-1, 'end')
        elif text == "":
            # Do nothing if the button is "+", "-", "0", ".", or "enter"
            pass
        elif text in ["Return", "KP_Enter", "enter"]:
            try:
                # Attempt to convert the current value to a float
                self.value = float(current_value)
                # Call the give_value method to set self.vv and destroy the Toplevel window
                self.getvalue_form.destroy()
            except ValueError:
                # If the current value cannot be converted to a float, do nothing
                pass
        elif "." in current_value and text == "." or "0" == current_value and text == "0":
            # Do nothing if the current value already contains a decimal point
            pass
        else:
            # Append the button text to the current value of the Entry widget
            if text >= '0' and text <= '9' or text == ".":
                if self.first:
                    self.include_var.set("")
                    current_value = ""
                    self.first = False
                self.include_var.set(current_value + text)
