import tkinter as tk
from tkinter import ttk
import sqlite3
conn = sqlite3.connect("my_database.db")
cursor = conn.cursor()

class PaymentForm(tk.Tk):
    def __init__(self, master):
        self.master = master
        
        # create a Toplevel window for the payment form
        self.payment_form = tk.Toplevel(self.master)
        self.payment_form.title("Payment Form")

        # calculate the center coordinates of the screen
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        x = (screen_width / 2) - (500 / 2)  # 500 is the width of the Payment Form window
        y = (screen_height / 2) - (500 / 2)  # 500 is the height of the Payment Form window

        # set the position of the Payment Form window to center
        self.payment_form.geometry(f"500x500+{int(x)}+{int(y)}")

        self.manage_form_label = tk.Label(self.payment_form, text="Payment Split Form")
        self.manage_form_label.grid(row=0, column=0, sticky="nsew")

        # New frame at the top of the main frame
        self.top_frame = tk.Frame(self.payment_form, bg="red", height=screen_height * 0.10, width=screen_width)
        self.top_frame.grid(row=1, column=0, sticky="nsew", columnspan=2)

        # Create a label and an entry widget for the search box
        self.search_label = tk.Label(self.top_frame, text="Search:", width=int(self.top_frame.winfo_width() * 0.10), bg="red", fg="white", font=("Arial", 12))
        self.search_label.grid(row=0, column=0, sticky="nsew")
        # create a variable to store the selected value
        self.selected_value = tk.StringVar()

        cursor.execute("SELECT * FROM tools")
        rows = cursor.fetchall()
        # create the combo box
        self.search_entry = ttk.Combobox(self.top_frame, width=20, font=("Arial", 12), textvariable=self.selected_value)
        #tk.Entry
        self.search_entry.grid(row=0, column=1, sticky="nsew", columnspan=2)
        for row in rows:
            self.search_entry['values'] = row[1]
        # set the list of options
        #combo_box['values'] = options

        # set the default value
        #combo_box.current(0)
        self.search_label = tk.Label(self.top_frame, text="Amount:", bg="red", fg="white", font=("Arial", 12))
        self.search_label.grid(row=1, column=0, sticky="nsew")
        self.get_amount_entry = tk.Entry(self.top_frame, width=15, font=("Arial", 12))
        self.get_amount_entry.grid(row=1, column=1, sticky="nsew")

        # Create 4 button widgets and grid(row=0, column=0, sticky="nsew")
        self.button3 = tk.Button(self.top_frame, text="Add", bg="red", fg="white", font=("Arial", 12), command=self.add_payment)
        self.button3.grid(row=1, column=2, sticky="nsew")
        self.button4 = tk.Button(self.top_frame, text="remove", bg="red", fg="white", font=("Arial", 12), command=self.remove_payment)
        self.button4.grid(row=1, column=3, sticky="nsew")

        # New listbox in the main frame
        self.list_items = tk.Listbox(self.payment_form, bg="yellow", height=17)
        self.list_items.grid(row=2, column=0, sticky="nsew", rowspan=2, columnspan=2)

        # New frame next to list_items in the main frame
        self.midel_frame = tk.Frame(self.payment_form, bg="blue", height=int(screen_height * 0.90))
        self.midel_frame.grid(row=4, column=0, sticky="nsew", columnspan=2)

        
        
        
        self.Price_label = tk.Label(self.midel_frame, text="Price : " + str(self.master.price))
        self.Price_label.grid(row=0, column=0, sticky="nsew")
        self.price_A_disc_form_label = tk.Label(self.midel_frame, text="Price After discount : " + str(self.master.disc))
        self.price_A_disc_form_label.grid(row=1, column=0, sticky="nsew")
        self.Amount_pide_form_label = tk.Label(self.midel_frame, text="Amount Pide : " + str(self.master.pid))
        self.Amount_pide_form_label.grid(row=2, column=0, sticky="nsew")
        self.Total_form_label = tk.Label(self.midel_frame, text="TOTAL : " + str(self.master.total))
        self.Total_form_label.grid(row=3, column=0, sticky="nsew")
        
        self.close_btn = tk.Button(self.midel_frame, text="Continue", command=self.continue_pyment)
        self.close_btn.grid(row=4, column=0, sticky="nsew")

        self.close_btn = tk.Button(self.midel_frame, text="Close", command=self.payment_form.destroy)
        self.close_btn.grid(row=4, column=1, sticky="nsew")

        # show the Payment Form window
        self.payment_form.transient(self.master)
        self.payment_form.grab_set()
        self.update_info()
        self.master.wait_window(self.payment_form)

    def continue_pyment(self):
        self.master.pid_peyment.clear()
        for a in self.list_items.get(0, tk.END):
            self.master.pid_peyment.append(a)
        print("self.master.pid_peyment = " + str(self.master.pid_peyment))
        self.master.process_payment()
        self.payment_form.destroy()

    def update_info(self):
        print("Amount price : " + str(self.master.price))
        self.Price_label.config(text="2Price : " + str(self.master.price))
        self.Amount_pide_form_label.config(text="Amount Pide : " + str(self.master.pid))
        self.price_A_disc_form_label.config(text="Price After discount : " + str(self.master.price - self.master.disc))
        self.Total_form_label.config(text="TOTAL : " + str(self.master.price - self.master.disc - self.master.pid))
        print("Amount Pide : " + str(self.master.pid))
        self.Amount_pide_form_label.config(text="Amount Pide : " + str(self.master.pid))
        self.Total_form_label.config(text="TOTAL : " + str(self.master.pid - self.master.price - self.master.disc))

    def add_payment(self):
        if self.selected_value.get() == '':
            print("payment not selected")
        else:
            if self.get_amount_entry.get() == '':
                print("amount not given")
            else:
                self.list_items.insert(tk.END, self.selected_value.get()+ " = " + self.get_amount_entry.get())
                self.master.pid = 0
                for a in self.list_items.get(0, tk.END):
                    print(int(a.split(' = ')[1]))
                    self.master.pid = self.master.pid + int(a.split(' = ')[1])
                self.update_info()
            
    def remove_payment(self):
        index = self.list_items.curselection()[0]
        self.list_items.delete(index)
        self.master.pid = 0
        for a in self.list_items.get(0, tk.END):
            print(int(a.split(' = ')[1]))
            self.master.pid = self.master.pid + int(a.split(' = ')[1])
        self.update_info()

    def hide_all_manager(self):
        self.hide_all_frames()
        self.master.show_frame("DisplayFrame")

    def show_frame(self, frame_name):
        # hide all frames except the one to be shown
        for name, frame in self.menuframes.items():
            if name == frame_name:
                frame.pack(side="top", fill="both", expand=True)
            else:
                frame.pack_forget()

    def hide_all_frames(self):
        self.info_frame.pack_forget()
        self.doc_frame.pack_forget()
        self.product_frame.pack_forget()
        self.stock_frame.pack_forget()
        self.report_frame.pack_forget()
        self.user_frame.pack_forget()
        self.tools_frame.pack_forget()
        self.main_frame.pack_forget()

    #def show_info_form(self):

    def show_report_form(self):
        self.hide_all_frames()
        self.report_frame.pack()

    def show_setting_form(self):
        # implement this function to show the Setting Form when the Setting button is clicked
        pass

    def show_about_form(self):
        # implement this function to show the About Form when the About button is clicked
        pass
