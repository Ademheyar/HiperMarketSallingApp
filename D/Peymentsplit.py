import tkinter as tk
from tkinter import ttk
import sqlite3, os

data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data'))
db_path = os.path.join(data_dir, 'my_database.db')
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

class PaymentForm(tk.Tk):
    def __init__(self, master):
        self.master = master
        self.ex_pid = []
        self.left = 0
        # create a Toplevel window for the payment form
        self.payment_form = tk.Toplevel(self.master)
        self.payment_form.title("Payment Split Form")

        # calculate the center coordinates of the screen
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        x = (screen_width / 2) - (500 / 2)  # 500 is the width of the Payment Form window
        y = (screen_height / 2) - (500 / 2)  # 500 is the height of the Payment Form window

        # set the position of the Payment Form window to center
        self.payment_form.geometry(f"500x500+{int(x)}+{int(y)}")
        
        # New frame at the top of the main frame
        self.top_extantion_frame = tk.Frame(self.payment_form, bg="white", height=screen_height * 0.10, width=screen_width)
        self.top_extantion_frame.grid(row=0, column=0, sticky="nsew", columnspan=4)
        
        # New frame at the top of the main frame
        self.top_frame = tk.Frame(self.payment_form, bg="red", height=screen_height * 0.10, width=screen_width)
        self.top_frame.grid(row=1, column=0, sticky="nsew", columnspan=4)

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
        print("row = " + str(rows))
        self.search_entry.grid(row=0, column=1, sticky="nsew", columnspan=2)
        options = []
        for row in rows:
            options.append(row[1])
        # set the list of options
        self.search_entry['values'] = options
        #combo_box['values'] = options
        self.get_extantion_barcode = tk.Entry(self.top_frame, width=15, font=("Arial", 12))
        self.get_extantion_barcode.grid(row=0, column=3, sticky="nsew")

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
        self.list_payment = ttk.Treeview(self.payment_form, columns=("Peyment Type", "Paid", "Paid Date", "Updated Date", "User", "Paid", "Extantion Bracodes"))
        self.list_payment.grid(row=0, column=0, columnspan=4, sticky="nsew")
        self.list_payment.heading("#0", text="ID", anchor=tk.W)
        self.list_payment.column("#0", stretch=tk.NO, width=50)
        self.list_payment.heading("#1", text="Peyment Type", anchor=tk.W)
        self.list_payment.column("#1", stretch=tk.NO, width=250)
        self.list_payment.heading("#2", text="Paid", anchor=tk.W)
        self.list_payment.column("#2", stretch=tk.NO, width=50)
        self.list_payment.heading("#3", text="Paid Date", anchor=tk.W)
        self.list_payment.column("#3", stretch=tk.NO, width=50)
        self.list_payment.heading("#4", text="Updated Date", anchor=tk.W)
        self.list_payment.column("#4", stretch=tk.NO, width=250)
        self.list_payment.heading("#5", text="User", anchor=tk.W)
        self.list_payment.column("#5", stretch=tk.NO, width=250)
        self.list_payment.heading("#6", text="Paid", anchor=tk.W)
        self.list_payment.column("#6", stretch=tk.NO, width=250)
        self.list_payment.heading("#7", text="Extantion Bracodes", anchor=tk.W)
        self.list_payment.column("#7", stretch=tk.NO, width=250)
        self.list_payment.grid(row=2, column=0, sticky="nsew", rowspan=2, columnspan=4)

        # New frame next to list_items in the main frame
        self.midel_frame = tk.Frame(self.payment_form, height=int(screen_height * 0.90))
        self.midel_frame.grid(row=4, column=0, sticky="nsew", columnspan=4)

        self.total_items_label = tk.Label(self.midel_frame, text="Price : " + str(self.master.total))
        self.total_items_label.grid(row=0, column=0, sticky="nsew")
        self.Price_label = tk.Label(self.midel_frame, text="Price : " + str(self.master.total), font=("Arial", 12))
        self.Price_label.grid(row=0, column=1, sticky="nsew")
        self.After_Price_label = tk.Label(self.midel_frame, text="Price After discount : " + str(self.master.disc))
        self.After_Price_label.grid(row=1, column=0, sticky="nsew")
        self.Amount_pide_form_label = tk.Label(self.midel_frame, text="Amount Pide : " + str(self.master.pid))
        self.Amount_pide_form_label.grid(row=1, column=1, sticky="nsew")
        self.Amount_Left_form_label = tk.Label(self.midel_frame, text="Amount : ", font=("Arial", 15))
        self.Amount_Left_form_label.grid(row=2, column=0, sticky="nsew")
        
        self.continue_btn = tk.Button(self.midel_frame, text="Continue", command=self.continue_pyment)
        self.continue_btn.grid(row=4, column=0, sticky="nsew", columnspan=2)

        self.close_btn = tk.Button(self.midel_frame, text="Close", command=self.payment_form.destroy)
        self.close_btn.grid(row=4, column=2, sticky="nsew", columnspan=2)

        # show the Payment Form window
        self.payment_form.transient(self.master)
        self.payment_form.grab_set()
        self.update_info()
        self.master.wait_window(self.payment_form)
        
    def continue_pyment(self):
        #self.master.pid_peyment.clear()
        # TODO: SHOW MSG DIALOG IF PAYMENT IS LESS THAN PID
        print("self.master.pid_peyment = " + str(self.master.pid_peyment))
        if self.left <= 0:

            self.master.process_payment()
            self.payment_form.destroy()

    def update_info(self):
        self.list_payment.delete(*self.list_payment.get_children())
        
        pid_i = 0
        for pay_pid in self.master.pid_peyment:
            p1, p2,  p3, p4, p5, p6, p7 = ['','','','','','','']
            print("pay_pid : " +  str(len(pay_pid)))
            if len(pay_pid) > 1 and pay_pid[1]:
                p1 =  pay_pid[1]
            if len(pay_pid) > 2  and pay_pid[2]:
                p2 =  pay_pid[2]
            if len(pay_pid) > 3 and pay_pid[3]:
                p3 =  pay_pid[3]
            if len(pay_pid) > 4 and pay_pid[4]:
                p4 =  pay_pid[4]
            if len(pay_pid) > 5 and pay_pid[5]:
                p5 =  pay_pid[5]
            if len(pay_pid) > 6 and pay_pid[6]:
                p6 =  pay_pid[6]
            if len(pay_pid) > 7 and pay_pid[7]:
                p7 =  pay_pid[7]
                #self.master.ex_pid_peyment
                if not pay_pid[7] in self.ex_pid:
                    self.ex_pid.append(pay_pid[7])
                    ch = len(self.top_extantion_frame.winfo_children())

                    ex_bar_frame = tk.Frame(self.top_extantion_frame, bg="green")
                    ex_bar_frame.grid(row=0, column=ch, sticky="nsew")
                    search_label = tk.Label(ex_bar_frame, text=pay_pid[7], bg="green", fg="white", font=("Arial", 12))
                    search_label.grid(row=0, column=0, sticky="nsew")
                    update_button = tk.Button(ex_bar_frame, text="X", bg="red", fg="white", font=("Arial", 12), command=lambda: self.remove_ex_items(ex_bar_frame, search_label))
                    update_button.grid(row=0, column=1, sticky="nsew")
            pid_i += float(p2)
            print("Amount Pide+ : " +str(pid_i)+"  "+ str(float(p2)))
            self.list_payment.insert("", 'end', text=pay_pid[0], values=(p1, p2,  p3, p4, p5, p6, p7))
        total_qty, total_discount, total_tax, all_total_price = self.master.chack_list()
        total = (all_total_price - self.master.tax) - self.master.disc
        self.master.pid = pid_i
        print("Amount Pide : " + str(self.master.pid))
        print("Amount total : " + str(total))
        
        self.total_items_label.config(text="Total Items : " + str(total_qty))
        self.Price_label.config(text="Total Price : " + str(all_total_price))
        self.After_Price_label.config(text="Price After discount :" + str(total))
        self.Amount_pide_form_label.config(text="Total Pide Amount : " + str(self.master.pid))
        self.get_amount_entry.delete(0, tk.END)
        
        self.left = total - self.master.pid
        if self.left <= 0:
            self.Amount_Left_form_label.config(text="Change : " + str(total - self.master.pid))
            self.get_amount_entry.insert(0, "0")
            self.continue_btn.config(state=tk.NORMAL)
        else:
            self.Amount_Left_form_label.config(text="Left : " + str(total - self.master.pid))
            self.get_amount_entry.insert(0, str(total - self.master.pid))
            self.continue_btn.config(state=tk.DISABLED)
        

    def remove_ex_items(self, ex_bar_frame, search_label):
        p1 = 0
        while p1 < len(self.master.pid_peyment):
            if len(self.master.pid_peyment[p1]) > 7 and self.master.pid_peyment[p1][7]:
                print(str(search_label.cget("text"))+"search_label pay_pid[7] = " + str(self.master.pid_peyment[p1][7]))
                if str(self.master.pid_peyment[p1][7]) == search_label.cget("text"):
                    self.master.pid_peyment.remove(self.master.pid_peyment[p1])
                else:
                    p1+=1
                    
        for ex in self.master.ex_pid_peyment:
            if str(ex) == search_label.cget("text"):
                self.master.ex_pid_peyment.remove(ex)
                ex_bar_frame.grid_forget()

        self.update_info()
        
    def add_payment(self):
        if self.selected_value.get() == '':
            print("payment not selected")
        else:
            if self.get_amount_entry.get() == '':
                print("amount not given")
            else:
                self.list_payment.insert("", 'end', text="", values=(self.selected_value.get(), self.get_amount_entry.get(), self.get_extantion_barcode.get()))
                self.master.pid_peyment.append(["", self.selected_value.get(), self.get_amount_entry.get(), self.get_extantion_barcode.get()])
                self.master.pid = self.master.pid + float(self.get_amount_entry.get())
                self.update_info()
            
    def remove_payment(self):
        for a in self.list_payment.selection():
            aa = self.list_payment.item(a)["values"]
            t = self.list_payment.item(a)["text"]
            p1 = 0
            while p1 < len(self.master.pid_peyment):
                print("payment not selected ,"+str(self.master.pid_peyment[p1]))
                print("payment not selected ."+str(aa))
                if len(aa) == 7 and len(self.master.pid_peyment[p1]) == 8 and str(t) == str(self.master.pid_peyment[p1][0]) and str(aa[0]) == str(self.master.pid_peyment[p1][1]) and \
                   str(aa[1]) == str(self.master.pid_peyment[p1][2]) and str(aa[2]) == str(self.master.pid_peyment[p1][3]) and \
                   str(aa[3]) == str(self.master.pid_peyment[p1][4]) and str(aa[4]) == str(self.master.pid_peyment[p1][5]) and \
                   str(aa[5]) == str(self.master.pid_peyment[p1][6]) and str(aa[6]) == str(self.master.pid_peyment[p1][7]):
                    self.master.pid_peyment.remove(self.master.pid_peyment[p1])
                    break
                elif len(aa) == 7 and len(self.master.pid_peyment[p1]) == 4 and str(t) == str(self.master.pid_peyment[p1][0]) and str(aa[0]) == str(self.master.pid_peyment[p1][1]) and \
                   str(aa[1]) == str(self.master.pid_peyment[p1][2]) and str(aa[2]) == str(self.master.pid_peyment[p1][3]):
                    self.master.pid_peyment.remove(self.master.pid_peyment[p1])
                    break
                else:
                    p1+=1
            aa = self.list_payment.delete(a)
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
