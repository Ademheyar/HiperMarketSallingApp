import tkinter as tk
from tkinter import ttk
import sqlite3
import shutil
import datetime
import os
import atexit
import sys
import random
import json
import ast

current_dir = os.path.abspath(os.path.dirname(__file__))
MAIN_dir = os.path.join(current_dir, '..')
sys.path.append(MAIN_dir)
from D.ChooseCustemr import UserManagementApp
from D.ChooseWorker import WorkerManagementApp
from D.searchbox import search_entry
from D.Peymentsplit import PaymentForm
from D.GetVALUE import GetvalueForm
from D.Showchartlists import ShowchartForm
from D.ApprovedDisplay import ApproveFrame
from M.Product import ProductForm
from D.iteminfo import *
from D.endday import EnddayForm
from D.Upload_ import UploadingForm
from D.user_info import UserInfoForm
from D.Veaw_Notifications import Veaw_Notifications
from D.printer import PrinterForm
from C.slipe import load_slip
from D.Doc.Loaddoc import *
from D.Security import *
from C.List import *


from C.API.Get import *
from C.API.Set import *

from Manager import ManageForm

data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data'))
db_path = os.path.join(data_dir, 'my_database.db')
conn = sqlite3.connect(db_path)
cursor = conn.cursor()


class DisplayFrame(tk.Frame):
    def __init__(self, master, Shops_info, user, User_Shops_List, Shops):
        tk.Frame.__init__(self, master)
        
        # Android-style dark blue color scheme
        self.bg_dark = "#0d47a1"      # Deep blue
        self.bg_light = "#1565c0"     # Darker blue
        self.accent_blue = "#1976d2"  # Medium blue
        self.text_light = "#ffffff"   # White text
        self.bg_darker = "#0a3d91"    # Even darker blue
        
        self.configure(bg=self.bg_dark)
        
        self.onDisplayFrame = ""
        self.user = user
        self.Shops_info = Shops_info
        self.Shops = Shops
        self.User_Shops_List = User_Shops_List
        self.Selected_Shop = ""
        self.Shop_Payment_Tools = []
        
        self.Selected_items = []
        self.items = []
        
       #print("Disktop user : " + str(self.user))
        self.custemr = ""
        self.chart_index = 0
        self.price = 0
        self.pid = 0
        self.pid_peyment = []
        self.ex_pid_peyment = []
        self.Loded_payment_buttons = []
        self.ex_items = []
        self.ex_doc = []
        self.tax = 0
        self.qty = 0
        self.disc = 0
        self.total = 0

        self.At_Shop_id = -1
        self.on_Shop = -1         
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        print("Display Frame Initialized with screen size: {}x{}".format(screen_width, screen_height))
        
        if Shops_info is None or user is None or User_Shops_List is None or Shops is None:
            if not Security_get_user(self):
                print("No user data found, closing application.")
                self.master.destroy()
                return
            else:
                self.grid(row=0, column=0, sticky="nsew")
                self.master.show_frame("Display_Frame")
          
            
        
        self.main_Notebook = ttk.Notebook(self)
        self.main_Notebook.pack(side="top", fill="both", expand=True)

        self.main_frame = tk.Frame(self.main_Notebook, bg=self.bg_dark)
        self.main_frame.grid()
        self.main_Notebook.add(self.main_frame, text='Sell')
        self.main_Notebook.bind("<<NotebookTabChanged>>", self.on_tab_selected)
        
        self.main_frame.columnconfigure((0, 1), weight=1)
        self.main_frame.columnconfigure(1, weight=0)
        self.main_frame.rowconfigure(0, weight=0)
        self.main_frame.rowconfigure(1, weight=2)
        self.main_frame.rowconfigure(2, weight=0)

        self.top_frame = tk.Frame(self.main_frame, height=int(screen_height * 0.70), bg=self.bg_light)
        self.top_frame.grid(row=0, column=0, columnspan=2, sticky="nsew")
        self.top_frame.columnconfigure((0), weight=0)
        self.top_frame.columnconfigure((5), weight=1)
        self.top_frame.rowconfigure((0), weight=1)

        self.search_label = tk.Label(self.top_frame, text="Search:", font=("Arial", 12), 
                                     bg=self.bg_light, fg=self.text_light)
        self.search_label.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        
        self.search_entry = search_entry(self.top_frame, self.Shops_info, self.user, self.Shops, font=("Arial", 12))
        self.search_entry.grid(row=0, column=1, columnspan=5, sticky="nsew", padx=5, pady=5)

        self.Calculter_button = ttk.Button(self.top_frame, text="Calcu\nF1", command=lambda: GetvalueForm(self, '0', ["Calculater"]))
        self.Calculter_button.grid(row=0, column=6, sticky="nsew", padx=2, pady=5)
        self.master.bind("<F1>", lambda _: GetvalueForm(self, '0', ["Calculater"]))
        
        self.Add_None_item_button = ttk.Button(self.top_frame, text="None\nF2", command=lambda: self.Create_Unowen_item())
        self.Add_None_item_button.grid(row=0, column=7, sticky="nsew", padx=2, pady=5)
        self.master.bind("<F2>", lambda _: self.Create_Unowen_item())

        self.midel_frame = tk.Frame(self.main_frame, bg=self.bg_dark)
        self.midel_frame.grid(row=1, column=0, sticky="nsew")
        
        self.extrnal_frame = tk.Frame(self.midel_frame, height=int(screen_height * 0.050), bg=self.bg_darker)
        self.extrnal_frame.pack(side="top", fill="x")

        self.Frame_contaner_frame = tk.Frame(self.midel_frame, bg=self.bg_dark)
        self.Frame_contaner_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.List_Frame_contaner_frame = tk.Frame(self.Frame_contaner_frame, bg=self.bg_dark)
        self.List_Frame_contaner_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.List_Frame = tk.Frame(self.List_Frame_contaner_frame, bg=self.bg_dark)
        self.List_Frame.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        
        self.item_List_canvas = tk.Canvas(self.List_Frame, bg=self.bg_dark, highlightthickness=0)
        self.item_List_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        
        self.item_List_yscrollbar = tk.Scrollbar(self.List_Frame, orient='vertical', 
                                                 command=self.item_List_canvas.yview, bg=self.bg_light)
        self.item_List_yscrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.item_List_xscrollbar = tk.Scrollbar(self.List_Frame_contaner_frame, orient='horizontal', 
                                                 command=self.item_List_canvas.xview, bg=self.bg_light)
        self.item_List_xscrollbar.pack(side=tk.TOP, fill=tk.X)
        
        self.item_List_canvas.configure(xscrollcommand=self.item_List_xscrollbar.set, 
                                       yscrollcommand=self.item_List_yscrollbar.set)

        self.Selected_item_Display_frame = tk.Frame(self.item_List_canvas, bg=self.bg_dark)
        self.item_List_canvas.create_window((0, 0), window=self.Selected_item_Display_frame, anchor=tk.NW)
        self.Selected_item_Display_frame.bind('<Configure>', lambda e: self.item_List_canvas.configure(scrollregion=self.item_List_canvas.bbox("all")))

        self.buttons_frame = tk.Frame(self.main_frame, bg=self.bg_darker)
        self.buttons_frame.grid(row=1, column=1, rowspan=1, sticky="nsew")

        self.buttons_frame.columnconfigure((0, 1, 2, 3), weight=1, minsize=int(self.buttons_frame.winfo_height() *0.1))
        self.buttons_frame.rowconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8, 9), weight=1, minsize=int(self.buttons_frame.winfo_height() *0.1))

        self.voidlist_button = ttk.Button(self.buttons_frame, text="Void\nF3", command=self.void_)
        self.voidlist_button.grid(row=0, column=0, sticky="nsew", padx=3, pady=3)
        self.master.bind("<F3>", lambda _: self.void_())
        
        self.prevlist_button = ttk.Button(self.buttons_frame, text="Prev\nF5", command=lambda: self.next_prev_chart("prev"))
        self.prevlist_button.grid(row=0, column=1, sticky="nsew", padx=3, pady=3)
        self.prevlist_button.config(state=tk.DISABLED)
        self.master.bind("<F5>", lambda _: self.next_prev_chart("prev"))
        
        self.activets_button = ttk.Button(self.buttons_frame, text="Activets\nF6", command=self.call_chartForm)
        self.activets_button.grid(row=0, column=2, sticky="nsew", padx=3, pady=3)
        self.master.bind("<F6>", lambda _: self.call_chartForm())
        
        self.newlist_button = ttk.Button(self.buttons_frame, text="New\nF7", command=self.new_chart)
        self.newlist_button.grid(row=0, column=3, sticky="nsew", padx=3, pady=3)
        self.master.bind("<F7>", lambda _: self.new_chart())
        
        self.payment_button = ttk.Button(self.buttons_frame, text="Payment\nF12", command=self.call_splitpayment)
        self.payment_button.grid(row=1, column=0, sticky="nsew", padx=3, pady=3)
        self.master.bind("<F12>", lambda _: self.call_splitpayment())
        
        self.endday_button = ttk.Button(self.buttons_frame, text="Cash Drawer\nCtrl+D", command=lambda: self.open_drower())
        self.endday_button.grid(row=1, column=1, sticky="nsew", padx=3, pady=3)
        
        self.update_button = ttk.Button(self.buttons_frame, text="update\nCtrl+U", command=lambda: self.Call_Uploading_Form())
        self.update_button.grid(row=1, column=2, sticky="nsew", padx=3, pady=3)

        self.total_frame = tk.Frame(self.main_frame, height=150, bg=self.bg_light)
        self.total_frame.grid(row=2, column=0, rowspan=2, columnspan=4, sticky="nsew")

        self.total_items_label = tk.Label(self.total_frame, text="Total Items : 0", font=("Arial", 12, "bold"), 
                                          bg=self.bg_light, fg=self.text_light)
        self.total_items_label.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        
        self.total_tax_label = tk.Label(self.total_frame, text="Total Tax : 0", font=("Arial", 12, "bold"), 
                                        bg=self.bg_light, fg=self.text_light)
        self.total_tax_label.grid(row=1, column=1, sticky="nsew", padx=5, pady=5)
        
        self.total_discount_label = tk.Label(self.total_frame, text="Item Discount : 0", font=("Arial", 12, "bold"), 
                                             bg=self.bg_light, fg=self.text_light)
        self.total_discount_label.grid(row=1, column=2, sticky="nsew", padx=5, pady=5)
        
        self.total_tdiscount_label = tk.Label(self.total_frame, text="Total Discount : 0", font=("Arial", 12, "bold"), 
                                              bg=self.bg_light, fg=self.text_light)
        self.total_tdiscount_label.grid(row=1, column=3, sticky="nsew", padx=5, pady=5)
        
        self.total_price_label = tk.Label(self.total_frame, text="Price Befor: 0", font=("Arial", 12, "bold"), 
                                          bg=self.bg_light, fg=self.text_light)
        self.total_price_label.grid(row=1, column=4, sticky="nsew", padx=5, pady=5)
        
        self.total_label = tk.Label(self.total_frame, text="Total After: 0", font=("Arial", 16, "bold"), 
                                    bg=self.bg_light, fg="#4dd0e1")
        self.total_label.grid(row=1, column=5, sticky="nsew", padx=5, pady=5)


        self.Veaw_Notifications_label = tk.Label(self.total_frame, text="Notifications", font=("Arial", 10, "bold"),
                                                 fg="#4dd0e1", bg=self.bg_light, cursor="hand2")
        self.Veaw_Notifications_label.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        self.Veaw_Notifications_label.bind("<Button-1>", lambda _: Veaw_Notifications(self, self.user, self.Shops))

        self.Loged_user_label = tk.Label(self.total_frame, text=str(self.user['User_name']), font=("Arial", 10, "bold"),
                                         fg="#4dd0e1", bg=self.bg_light, cursor="hand2")
        self.Loged_user_label.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
        self.Loged_user_label.bind("<Button-1>", lambda _: UserInfoForm(self, self.user))
        
        self.Shops_Names = [shop['Shop_name'] for shop in self.Shops]                            
        self.User_Shopes_Combobox = ttk.Combobox(self.total_frame, values=self.Shops_Names, width=10)
        self.User_Shopes_Combobox.grid(row=0, column=2, sticky="nsew", padx=5, pady=5)
        

        self.at_shop_name = ""
        if(len(self.Shops_Names) == 1):
            print("Only one shop found, selecting it by default.")
            print("Shop Name: ", self.Shops)
            self.At_Shop_id = self.Shops[0]['Shop_Id']
            at_shop_name = self.Shops[0]['Shop_name']
            self.on_Shop = 0
        else:
            pass
        
        self.At_Shop_label = tk.Label(self.total_frame, text=str(at_shop_name), font=("Arial", 10, "bold"),
                                      fg="#4dd0e1", bg=self.bg_light, cursor="hand2")
        self.At_Shop_label.grid(row=0, column=3, sticky="nsew", padx=5, pady=5)
        self.At_Shop_label.bind("<Button-1>", lambda _: UserInfoForm(self))

        self.Add_custemur_label = tk.Label(self.total_frame, text="+ Custumer", font=("Arial", 10, "bold"),
                                           fg="#4dd0e1", bg=self.bg_light, cursor="hand2")
        self.Add_custemur_label.grid(row=0, column=4, sticky="nsew", padx=5, pady=5)
        self.Add_custemur_label.bind("<Button-1>", lambda _: self.Add_Custumer())

        self.date_day_Label = tk.Label(self.total_frame, text="H:M D-M-Y :" , font=("Arial", 9, "bold"), 
                           width=20, bg=self.bg_light, fg=self.text_light)
        
        # Update the label with the current date/time every second
        def _update_datetime():
            now = datetime.datetime.now().strftime('%H:%M')
            self.date_day_Label.config(text=now + " D-M-Y :")
            self.date_day_Label.after(100, _update_datetime)
        _update_datetime()

        self.date_day_Label.grid(row=0, column=5, sticky="w", padx=2, pady=5)
        
        self.date_day_Spinbox = ttk.Spinbox(self.total_frame, from_=1, to=31, width=5)
        self.date_day_Spinbox.grid(row=0, column=6, sticky="w", padx=2, pady=5)
        self.date_day_Spinbox.set(str(datetime.datetime.now().strftime('%d')))
        
        self.date_month_Spinbox = ttk.Spinbox(self.total_frame, from_=1, to=13, width=5)
        self.date_month_Spinbox.grid(row=0, column=7, sticky="w", padx=2, pady=5)
        self.date_month_Spinbox.set(str(datetime.datetime.now().strftime('%m')))
        
        self.date_year_Spinbox = ttk.Spinbox(self.total_frame, from_=1990, width=5)
        self.date_year_Spinbox.grid(row=0, column=8, sticky="w", padx=2, pady=5)
        self.date_year_Spinbox.set(str(datetime.datetime.now().strftime('%Y')))

        self.manage_form = ManageForm(self.main_Notebook, self.user, self.Shops, self.Shops_info, self.on_Shop)
        
        if Chacke_Security(self, self.user, self.Shops[self.on_Shop], 26, f'User Has No Permission To Access MANAGE FRAME OR LOGIN AS ADMIN'):    
            self.manage_form.pack(side="top", fill="both", expand=True)
            self.main_Notebook.add(self.manage_form, text='MANAGE')
        
        self.max_backups = 4     # Maximum number of backup files to keep
        atexit.register(self.backup_database)
        
        
        # Security Check
        # THIS WILL CHECK IF THE USER HAS PERMISSION TO ACCESS THE DISPLAY FRAME
        # IF NOT, THE APPLICATION WILL CLOSE THE MASTER WINDOW
        # THE PERMISSION LEVEL IS SET TO 0 FOR DISPLAY FRAME ACCESS
        # ADJUST THE PERMISSION LEVEL AS NEEDED FOR DIFFERENT FRAMES 
        if not Chacke_Security(self, self.user, self.Shops[self.on_Shop], 0, "USER NEEDED PERMISSION OR LOGIN AS ADMIN"):
            
            self.master.destroy()
            return
        

        self.chackeqyu = Chacke_Security(self, self.user, self.Shops[self.on_Shop], 14, f'User Not allowed to Change QTY')
        self.chackeprice = Chacke_Security(self, self.user, self.Shops[self.on_Shop], 15, f'User Not allowed to Change Price')
        self.chakedisc = Chacke_Security(self, self.user, self.Shops[self.on_Shop], 16, f'User Not allowed to Give Discount')
        self.chacketype = Chacke_Security(self, self.user, self.Shops[self.on_Shop], 17, f'User Not allowed to Change ITEM TYPE')
        self.chaketotaldic = Chacke_Security(self, self.user, self.Shops[self.on_Shop], 18, f'User Not allowed to Change TOTALE Price OR Give TOTAL DISCOUNT')
        
        self.update_list_items()
        self.update_info()
        
        self.master.bind("<Escape>", self.change_focus)
        self.master.bind("<KeyPress-d>", self.crtl_d_focus)
        self.master.bind("<KeyPress-D>", self.crtl_d_focus)
        self.master.bind("<Up>", self.treeview_naigation)
        self.master.bind("<Down>", self.treeview_naigation)
        self.master.bind("<Delete>", self.Selectd_item_remove)
        self.selected_indexd = -1
        
        # IF THE USER HAS PERMISSION TO ACCESS PAYMENT TOOLS
        # THE PERMISSION LEVEL IS SET TO 1 FOR PAYMENT TOOLS ACCESS
        # ADJUST THE PERMISSION LEVEL AS NEEDED FOR DIFFERENT FEATURES
        if Chacke_Security(self, self.user, self.Shops[self.on_Shop], 1, 'LISTING PAYMENT TOOLS NEEDED ACCESS PERMISSION OR LOGIN AS ADMIN'):
            self.Load_payment_buttons()
        
        self.load()
            
    def Veaw_Notifications(self):
        pass
    
    def treeview_naigation(self, event):
        if not (event.keysym == "Up" or event.keysym == "Down"):
            self.focus_set()
            
        if len(self.Selected_item_Display_frame.winfo_children()):
            if self.selected_indexd == -1:
                self.selected_indexd = 0
            if self.selected_indexd > len(self.Selected_item_Display_frame.winfo_children()):
                self.selected_indexd = 0
            
            elif event.keysym == 'Up':
                self.Selected_item_Display_frame.winfo_children()[self.selected_indexd].configure(bg="SystemButtonFace")
                self.selected_indexd -= 1
            elif event.keysym == 'Down':
                self.Selected_item_Display_frame.winfo_children()[self.selected_indexd].configure(bg="SystemButtonFace")
                self.selected_indexd += 1
                
            if self.selected_indexd <= -1:
                self.selected_indexd = len(self.Selected_item_Display_frame.winfo_children())-1
            elif self.selected_indexd >= len(self.Selected_item_Display_frame.winfo_children()):
                self.selected_indexd = 0
                
            self.Selected_item_Display_frame.winfo_children()[self.selected_indexd].configure(bg="blue")

    def Selectd_item_remove(self, event):
        if not self.selected_indexd == -1:
            self.remove_item(self.selected_indexd, self.Selected_item_Display_frame.winfo_children()[self.selected_indexd])
        
    def crtl_d_focus(self, event):
        #print("crtl+D pressed " + str(event))
        if "Control" in str(event) or event.state == 14:
            self.open_drower()
            #print("crtl+D pressed " + str(event.state))
        
    def change_focus(self, event):
        self.search_entry.focus_set()
        
    # about Display control
    def call_manager(self):
        self.master.show_frame("ManageFrame")

    def exit(self):
        self.master.show_frame("LogingFrame")

    def create_payment_buttons(self):
        # Function to create payment buttons based on tools in the database
        for widget in self.Loded_payment_buttons:
            widget[2].destroy()
        self.Loded_payment_buttons = []
        cursor.execute("SELECT * FROM tools")
        rows = cursor.fetchall()
        buttons = []
        i = -1
        j = -1
        a = 0
        b = 0
        for widget in range(len(self.buttons_frame.winfo_children()) - 1):
            j += 1
            if b == 3:
                b = 0
                a += 1
                continue
            if len(self.buttons_frame.winfo_children()) - 1 == j + 1:
                a += 1
                b = 0

                readon = -1
                if self.Selected_Shop != "":
                    readon = self.Shops_Names.index(self.Selected_Shop)
                
                for spt, row in enumerate(self.Shop_Payment_Tools):
                    if readon != -1 and readon != spt:
                        continue
                    #print("creating row btn = " + str(row))
                    i += 1
                    if b > 3:
                        b = 0
                        a += 1
                    tool_name = row[0]
                    # Create a new button
                    
                    
                    payment_tool_type = row[1]
                    permission_level = {'CASH':2, 'CARD':3, 'CREADIT':4, 'CASHOUT':5, 'CASHIN':6, 'OTHER':7}
                    perm_level = permission_level.get(payment_tool_type, 6)
                    
                    if Chacke_Security(self, self.user, self.Shops[self.on_Shop], perm_level, f'User Not allowed to Use {payment_tool_type} Payment Tool'):
                        new_button = ttk.Button(self.buttons_frame, text=tool_name+"\nCtrl + "+str(row[3]), command=lambda r=str(row[3]), d=tool_name: self.Q_Payment(r, d))
                        new_button.bind("<Button-3>", lambda d=str(row[3]): self.Q_Payment(d, d.widget["text"].split("\n")[0]))
                        self.master.bind("<KeyPress-" + str(row[3]) + ">", lambda r=str(row[3]), d=tool_name, k=new_button: self.Q_Payment(r, d) if "Control" in str(r)else print(""))
                        new_button.grid(row=a, column=b, sticky="nsew")
                        self.Loded_payment_buttons.append([row[1], row[3], new_button])
                        b += 1
                break
            else:
                b += 1
                
    def Load_payment_buttons(self):
        self.Shop_Payment_Tools = []
        for Shop in self.Shops:
            if Shop and Shop['Shop_Payment_Tools'] and Shop['Shop_Payment_Tools'] != "":
                Shop_Payment_Tools = load_list(Shop['Shop_Payment_Tools'])
                for Shop_Payment_Tool in Shop_Payment_Tools:
                    self.Shop_Payment_Tools.append(Shop_Payment_Tool)
        self.create_payment_buttons()
    
    # chart
    # about chart btn   
    def update_chart(self):
        doc_created_date = "doc_created_date"
        doc_expire_date = "doc_expire_date"
        doc_updated_date = "doc_updated_date"
        AT_SHOP = "AT_SHOP"
        user_id = "user_id"
        customer_id = "customer_id"
        type = "type"
        ex_item = ""
        ex_pay = ""
        PRICE = 0
        Disc = 0
        TAX = 0
        States = "States"
        
        for ex in self.ex_items:
            ex_item += str(ex) + ","
        for ex in self.ex_pid_peyment:
            ex_pay += str(ex) + ","
        
        items = len(self.Selected_items)
        ITEM = json.dumps(self.Selected_items)
        
        if items > 0 or ex_item != "" or ex_pay != "":
            # Define the query to check if the ID exists in the table
            query = f"SELECT id FROM pre_doc_table WHERE id = {self.chart_index}"

            # Execute the query and fetch the results
            results = fetch_as_dict_list(query, ())
            # Check if the query returned a result
            if results and len(results) > 0:
                #print(str([doc_created_date, doc_expire_date, doc_updated_date, AT_SHOP, user_id, customer_id, type, ITEM, PRICE, Disc, TAX, States, ex_item, ex_pay]))
                # Insert the new product into the database
                #cursor.execute('UPDATE pre_doc_table SET doc_created_date=?, doc_expire_date=?, doc_updated_date=?, AT_SHOP=?, user_id=?, customer_id=?, type=?, ITEM=?, PRICE=?, Disc=?, TAX=?, States=?, exitems_doc_barcode=?, expayment_doc_barcode=? WHERE id=?', (doc_created_date, doc_expire_date, doc_updated_date, AT_SHOP, user_id, customer_id, type, ITEM, float(PRICE), float(Disc), float(TAX), States, ex_item, ex_pay, self.chart_index))

                #print(f"Record with ID {self.chart_index} has been UPDATE into the table\n\n1\n\n")                
                #print(str([doc_created_date, doc_expire_date, doc_updated_date, AT_SHOP, user_id, customer_id, type, ITEM, float(PRICE), float(Disc), float(TAX), States, self.chart_index, ex_item, ex_pay]))
                pass
            else:
                #print(f"Record with ID {self.chart_index} does not exist in the table\n\n2\n\n")
                #print(str([doc_created_date, doc_expire_date, doc_updated_date, AT_SHOP, user_id, customer_id, type, ITEM, PRICE, Disc, TAX, States, ex_item, ex_pay]))
                # Insert the new product into the database
                #cursor.execute('INSERT INTO pre_doc_table (id, doc_created_date, doc_expire_date, doc_updated_date, AT_SHOP, user_id, customer_id, type, ITEM, PRICE, Disc, TAX, States, exitems_doc_barcode, expayment_doc_barcode) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (self.chart_index, doc_created_date, doc_expire_date, doc_updated_date, AT_SHOP, user_id, customer_id, type, ITEM, float(PRICE), float(Disc), float(TAX), States, ex_item, ex_pay))

                #print(str(["doc_barcode", "extension_barcode", "user_id", "customer_id", "type", ITEM, Disc, TAX, "doc_created_date", "doc_expire_date", "doc_updated_date", ex_item, ex_pay]))
                pass
            # Commit the changes to the database
            #conn.commit()
            
    # this will
    def chack_list(self):
        total_discount = 0
        total_tax = 0
        total_qty = 0
        all_total_price = 0

        for a, selected_item in enumerate(self.Selected_items):
            #print("in update item: " + str(selected_item[0]))
            #print("in update item: " + str(selected_item[0]))
            #print("in update item: " + str(selected_item[6]))
            #print("in update item: " + str(selected_item[8]))

            qty = float(selected_item[7])
            price = float(selected_item[10])
            discount = float(selected_item[0]['values']['price']) - float(selected_item[10])
            tax = float(selected_item[10])
            total_price = float(selected_item[11])
            
            # Calculate the expected total price based on quantity, price, discount, and tax
            expected_total_price = qty * (price)  # - tax
            
            # Update the total price in the item if it doesn't match the expected value
            if total_price != expected_total_price:
                self.Selected_items[a][11] = expected_total_price
            
            # Update the price variable
            total_qty += qty
            total_discount += discount
            total_tax += tax
            all_total_price += expected_total_price
        
        return total_qty, total_discount, total_tax, all_total_price

   
    def update_info(self):
        total_qty, total_discount, total_tax, all_total_price = self.chack_list()
        self.total = (all_total_price - self.tax) - self.disc
        self.total_items_label.config(text="Total Items : " + str(total_qty))
        self.total_tax_label.config(text="Total Tax : " + str(self.tax))
        self.total_discount_label.config(text="Item Discount : " + str(total_discount))
        self.total_tdiscount_label.config(text="Total Discount : " + str(self.disc))
        self.total_price_label.config(text="Price Befor : " + str(all_total_price))
        self.total_label.config(text="Price After: " + str((all_total_price - self.tax) - self.disc))
        self.update_chart()
        
    
                
    def Get_next_seletion(self, inputs, item_list):
        shop = inputs[0].get()
        code = inputs[1].get()
        color = inputs[2].get()
        size = inputs[3].get()
        qty = inputs[4].get()
        barcode = inputs[5].cget('text')
        #print("item_list['item_list'] ", item_list)
        if item_list['item_list']:
            #print(str(item_list['item_list']))
            info_list = item_list['item_list']
            
            sv = [s[0] for s in info_list]
            inputs[0].config(values=sv)
                
            if shop == "":
                if self.Selected_Shop != "" and self.Selected_Shop in sv:
                   inputs[0].set(self.Selected_Shop)
                elif self.Shops_Names[0] in sv:
                    inputs[0].set(self.Shops_Names[0])
            else:
                for s in info_list:
                    #print("code s")
                    #print(str(s))
                    if s[0] in shop:
                        #print("code s0")
                       #print(str(s[0]))
                        v = [c[0] for c in s[1]]
                        inputs[1].config(values=v)
                        if len(v) == 1:
                            inputs[1].set(v[0])
                        break
            
            if code == "":
                for s in info_list:
                   #print("code s")
                   #print(str(s))
                    if s[0] in shop:
                       #print("code s0")
                       #print(str(s[0]))
                        v = [c[0] for c in s[1]]
                        inputs[1].config(values=v)
                        if len(v) == 1:
                            inputs[1].set(v[0])
                        inputs[1].event_generate("<<ComboboxSelected>>")
                        return
            else:
                found = 0
                for s in info_list:
                    if s[0] in shop:
                        for codes in s[1]:
                            if codes[0] == code:
                                v = [color[0] for color in codes[1]]
                                inputs[2].config(values=v)
                                if len(v) == 1:
                                    inputs[2].set(v[0])
                                found = 1
                                break
                        if found:
                            break
                    
            if color == "":
                for s in info_list:
                    if s[0] in shop:
                        for codes in s[1]:
                            if codes[0] == code:
                                v = [color[0] for color in codes[1]]
                                inputs[2].config(values=v)
                                if len(v) == 1:
                                    inputs[2].set(v[0])
                                inputs[2].event_generate("<<ComboboxSelected>>")
                                return
            else:
                found = 0
                for s in info_list:
                    if s[0] in shop:
                        for codes in s[1]:
                            if codes[0] == code:
                                for c in codes[1]:
                                    if c[0] == color:
                                        v = [s[0] for s in c[1]]
                                        inputs[3].config(values=v)
                                        if len(v) == 1:
                                            inputs[3].set(v[0])
                                        found = 1
                                        break
                            if found:
                                break
                    if found:
                        break
                    
            if size == "":
                for s in info_list:
                    if s[0] in shop:
                        for codes in s[1]:
                            if codes[0] == code:
                                for c in codes[1]:
                                    if c[0] == color:
                                        v = [s[0] for s in c[1]]
                                        inputs[3].config(values=v)
                                        if len(v) == 1:
                                            inputs[3].set(v[0])
                                        inputs[3].event_generate("<<ComboboxSelected>>")
                                        return
            else:
                found = 0
                for s in info_list:
                    if s[0] in shop:
                        for codes in s[1]:
                            if codes[0] == code:
                                for c in codes[1]:
                                    if c[0] == color:
                                        for s in c[1]:
                                            if s[0] == size:
                                                #inputs[4].set(1)
                                                inputs[4].master.winfo_children()[0].config(text="QTY Max is " + str(s[1][0][4]))
                                                inputs[5].config(text=s[1][0][5])
                                                found = 1
                                            break
                                    if found:
                                        break
                            if found:
                                break
                    if found:
                        break
                    
            if qty == "":
                for s in info_list:
                    if s[0] in shop:
                        for codes in s[1]:
                            if codes[0] == code:
                                for c in codes[1]:
                                    if c[0] == color:
                                        for s in c[1]:
                                            if s[0] == size:
                                                inputs[4].set(1)
                                                inputs[4].master.winfo_children()[0].config(text="QTY Max is " + str(s[1][0][4]))
                                                inputs[5].config(text=s[1][0][5])
                                                return
                                            
    def Update_selected_item_info(self, data, selected_item_info, new_item_Price_Spinbox, new_item_TPrice_Spinbox, index):
        self.Get_next_seletion(data, selected_item_info)
        # QTY
        if self.chackeqyu:
            self.Selected_items[index][7] = data[4].get()
        
        # price
        if self.chackeprice and self.chakedisc:
           self.Selected_items[index][10] = new_item_Price_Spinbox.get()
        else:
            new_item_Price_Spinbox.set(self.Selected_items[index][10])
        
        if self.chacketype:
            # shop
            self.Selected_items[index][12] = data[0].get()
            #code
            self.Selected_items[index][2] = data[1].get()
            # color
            self.Selected_items[index][5] = data[2].get()
            # size
            self.Selected_items[index][6] = data[3].get()
        
        if self.chaketotaldic:
            new_item_TPrice_Spinbox.set(str(float(data[4].get())*float(new_item_Price_Spinbox.get())))

        disc = ""
        if float(selected_item_info['values']['price'])-float(new_item_Price_Spinbox.get()) > 0:
            disc = " DISCOUNT " + str(float(selected_item_info['values']['price'])-float(new_item_Price_Spinbox.get()))
        data[6].config(text="Price " + str(selected_item_info['values']['price']) + disc)

        self.update_info()
    
    def remove_ex_items(self, ex_bar_frame, search_label):
        for i, selected_item in enumerate(self.Selected_items):
            if selected_item[13] == search_label.cget("text"):
                self.Selected_items.remove(selected_item)
        self.Update_Selected_item()
        ex_bar_frame.grid_forget()
                
    def Update_Selected_item(self):
        for items in self.Selected_item_Display_frame.winfo_children():
            items.destroy()
        ex_doc_ = []
        for it in self.extrnal_frame.winfo_children():
            it.grid_forget()
        
        #self.midel_frame
        for i, selected_item in enumerate(self.Selected_items):
           #print("selected_item ", selected_item)
            if not selected_item[14] in ex_doc_:
                ex_doc_.append(selected_item[14])
                ch = len(self.extrnal_frame.winfo_children())

                ex_bar_frame = tk.Frame(self.extrnal_frame, bg="green")
                ex_bar_frame.grid(row=0, column=ch, sticky="nsew")
                search_label = tk.Label(ex_bar_frame, text=selected_item[14], bg="green", fg="white", font=("Arial", 12))
                search_label.grid(row=0, column=0, sticky="nsew")
                    
                update_button = ttk.Button(ex_bar_frame, text="X", command=lambda: self.remove_ex_items(ex_bar_frame, search_label))
                update_button.grid(row=0, column=1, sticky="nsew")
                
            selected_item_info = selected_item[0]
           #print("selected_item_info |", selected_item_info)
           #print("selected_item ", selected_item)
            
            #if isinstance(selected_item_info, str):
            #    selected_item_info = ast.literal_eval(selected_item_info)
            item = [""]
            
            new_item_fram = tk.Frame(self.Selected_item_Display_frame, highlightthickness=2, highlightbackground="black")
            new_item_fram.grid(row=len(self.Selected_item_Display_frame.winfo_children()), column=0, pady=1, sticky=tk.EW)

            # TODO ADD IMAGE 

            new_item_name = tk.Label(new_item_fram, text=str(selected_item[4]), font=("Arial", 11))
            new_item_name.grid(row=0, column=1, columnspan=6, sticky="nsew")

            new_barcode_Label = tk.Label(new_item_fram, text=str("barcode"), font=("Arial", 7))
            new_barcode_Label.grid(row=1, column=1, columnspan=3, sticky="nsew")
            
            new_type_Label = tk.Label(new_item_fram, text=str(selected_item[15]), font=("Arial", 7))
            new_type_Label.grid(row=1, column=3, columnspan=3, sticky="nsew")
            
            new_item_QTY_fram = tk.Frame(new_item_fram)
            new_item_QTY_fram.grid(row=2, column=1, rowspan=2, sticky="nsew")
            
            new_item_QTY_Label = tk.Label(new_item_QTY_fram, text="QTY Max is " + str(selected_item[8]), font=("Arial", 8))
            new_item_QTY_Label.grid(row=1, column=1, sticky="nsew")
            new_item_QTY_Spinbox = ttk.Spinbox(new_item_QTY_fram, from_=0, to=100, width=10)
            new_item_QTY_Spinbox.grid(row=2, column=1, sticky="nsew")
            new_item_QTY_Spinbox.set(str(selected_item[7]))
            price_ = ""
            price_ = str(selected_item_info['values']['price'])
            disc = ""
            if float(selected_item_info['values']['price'])-float(selected_item[10]) > 0:
                disc = " DISCOUNT " + str(float(selected_item_info['values']['price'])-float(selected_item[10]))
            new_item_Price_Label = tk.Label(new_item_fram, text="Price " + price_ + disc, font=("Arial", 7))
            new_item_Price_Label.grid(row=2, column=2, sticky="nsew")
            new_item_Price_Spinbox = ttk.Spinbox(new_item_fram, from_=0, to=100, width=10)
            new_item_Price_Spinbox.grid(row=3, column=2, sticky="nsew")
            new_item_Price_Spinbox.set(str(selected_item[10]))

            new_item_Shop_Label = tk.Label(new_item_fram, text="Shop :" , font=("Arial", 7))
            new_item_Shop_Label.grid(row=2, column=3, sticky="nsew")
            new_item_Shop_Combobox = ttk.Combobox(new_item_fram, values=[], width=10)
            new_item_Shop_Combobox.grid(row=3, column=3, padx=5, pady=5, sticky=tk.W)
            new_item_Shop_Combobox.set(str(selected_item[13]))
            new_item_Code_Label = tk.Label(new_item_fram, text="Code :" , font=("Arial", 7))
            new_item_Code_Label.grid(row=2, column=4, sticky="nsew")
            new_item_Code_Combobox = ttk.Combobox(new_item_fram, values=[], width=10)
            new_item_Code_Combobox.grid(row=3, column=4, padx=5, pady=5, sticky=tk.W)
            new_item_Code_Combobox.set(str(selected_item[2]))
            new_item_Color_Label = tk.Label(new_item_fram, text="Color " , font=("Arial", 7))
            new_item_Color_Label.grid(row=2, column=5, sticky="nsew")
            new_item_Color_Combobox = ttk.Combobox(new_item_fram, values=[], width=10)
            new_item_Color_Combobox.grid(row=3, column=5, padx=5, pady=5, sticky=tk.W)
            new_item_Color_Combobox.set(str(selected_item[5]))
            new_item_Size_Label = tk.Label(new_item_fram, text="Size " , font=("Arial", 7))
            new_item_Size_Label.grid(row=2, column=6, sticky="nsew")
            new_item_Size_Combobox = ttk.Combobox(new_item_fram, values=[], width=10)
            new_item_Size_Combobox.grid(row=3, column=6, padx=5, pady=5, sticky=tk.W)
            new_item_Size_Combobox.set(str(selected_item[6]))
            
            new_exbarcode_Label = tk.Label(new_item_fram, text=str(selected_item[14]), font=("Arial", 7))
            new_exbarcode_Label.grid(row=1, column=7, sticky="nsew")
            
            del_button = ttk.Button(new_item_fram, text="x", command= lambda index=i, frame=new_item_fram: self.remove_item(index, frame))
            del_button.grid(row=0, column=7, sticky="nsew")
            # self.master.bind("<Delete>", lambda _: self.remove_item())
            
            new_item_TPrice_Label = tk.Label(new_item_fram, text="Total Price is " , font=("Arial", 13))
            new_item_TPrice_Label.grid(row=2, column=7, sticky="nsew")
            new_item_TPrice_Spinbox = ttk.Spinbox(new_item_fram, from_=0, to=100, width=10)
            new_item_TPrice_Spinbox.grid(row=3, column=7, sticky="nsew")
            new_item_TPrice_Spinbox.set(str(float(selected_item[7])*float(selected_item[8])))
            
            data = [new_item_Shop_Combobox, new_item_Code_Combobox, new_item_Color_Combobox, new_item_Size_Combobox, new_item_QTY_Spinbox, new_barcode_Label, new_item_Price_Label]

            self.Get_next_seletion(data, selected_item_info)
            

            new_item_Shop_Combobox.bind("<<ComboboxSelected>>", lambda  _, d=data, v=selected_item_info, p=new_item_Price_Spinbox, tp=new_item_TPrice_Spinbox, j=i: self.Update_selected_item_info(d, v, p, tp, j))
            new_item_Code_Combobox.bind("<<ComboboxSelected>>", lambda  _, d=data, v=selected_item_info, p=new_item_Price_Spinbox, tp=new_item_TPrice_Spinbox, j=i: self.Update_selected_item_info(d, v, p, tp, j))
            new_item_Color_Combobox.bind("<<ComboboxSelected>>", lambda  _, d=data, v=selected_item_info, p=new_item_Price_Spinbox, tp=new_item_TPrice_Spinbox, j=i: self.Update_selected_item_info(d, v, p, tp, j))
            new_item_Size_Combobox.bind("<<ComboboxSelected>>", lambda  _, d=data, v=selected_item_info, p=new_item_Price_Spinbox, tp=new_item_TPrice_Spinbox, j=i: self.Update_selected_item_info(d, v, p, tp, j))

            new_item_Shop_Combobox.bind("<<ComboboxClicked>>", lambda  _, d=data, v=selected_item_info, p=new_item_Price_Spinbox, tp=new_item_TPrice_Spinbox, j=i: self.Update_selected_item_info(d, v, p, tp, j))
            new_item_Code_Combobox.bind("<<ComboboxClicked>>", lambda  _, d=data, v=selected_item_info, p=new_item_Price_Spinbox, tp=new_item_TPrice_Spinbox, j=i: self.Update_selected_item_info(d, v, p, tp, j))
            new_item_Color_Combobox.bind("<<ComboboxClicked>>", lambda  _, d=data, v=selected_item_info, p=new_item_Price_Spinbox, tp=new_item_TPrice_Spinbox, j=i: self.Update_selected_item_info(d, v, p, tp, j))
            new_item_Size_Combobox.bind("<<ComboboxClicked>>", lambda  _, d=data, v=selected_item_info, p=new_item_Price_Spinbox, tp=new_item_TPrice_Spinbox, j=i: self.Update_selected_item_info(d, v, p, tp, j))

            new_item_Price_Spinbox.bind("<KeyRelease>", lambda  _, d=data, v=selected_item_info, p=new_item_Price_Spinbox, tp=new_item_TPrice_Spinbox, j=i: self.Update_selected_item_info(d, v, p, tp, j))
            new_item_QTY_Spinbox.bind("<KeyRelease>", lambda  _, d=data, v=selected_item_info, p=new_item_Price_Spinbox, tp=new_item_TPrice_Spinbox, j=i: self.Update_selected_item_info(d, v, p, tp, j))
            #new_item_TPrice_Spinbox.bind("<<KeyRelease>>", lambda  _, d=data, v=selected_item_info, p=new_item_Price_Spinbox, tp=new_item_TPrice_Spinbox, j=i: self.Update_selected_item_info(d, v, p, tp, j))

            new_item_Price_Spinbox.config(command= lambda d=data, v=selected_item_info, p=new_item_Price_Spinbox, tp=new_item_TPrice_Spinbox, j=i: self.Update_selected_item_info(d, v, p, tp, j))
            new_item_QTY_Spinbox.config(command= lambda  d=data, v=selected_item_info, p=new_item_Price_Spinbox, tp=new_item_TPrice_Spinbox, j=i: self.Update_selected_item_info(d, v, p, tp, j))
            #new_item_TPrice_Spinbox.bind(command= lambda d=data, v=selected_item_info, p=new_item_Price_Spinbox, tp=new_item_TPrice_Spinbox, j=i: self.Update_selected_item_info(d, v, p, tp, j))
        self.update_info()
        
    def update_list_items(self):
        # Define the SQL query to fetch the product information based on doc_created_date
        # Execute the query and fetch the results
        res = fetch_as_dict_list("SELECT * FROM pre_doc_table", ())
        if len(res) > 1 and hasattr(self, 'prevlist_button'):
            self.prevlist_button.config(state=tk.NORMAL)
            
        results = fetch_as_dict_list("SELECT * FROM pre_doc_table WHERE id=?", (self.chart_index,))
        
       #print("update_list_items" + str(results))
        
        # Clear the existing items in the list
        # Loop through the results and add each product to the list
        for result in results:
            self.pid_peyment = []
            self.ex_pid_peyment = []
            self.items = []
            self.ex_items = []
            self.Selected_items = []
            
            # Extract the item information from the database record
            self.chart_index = result[0]
            doc_created_date = result[1]
            doc_expire_date = result[2]
            doc_updated_date = result[3]
            AT_SHOP = result[4]
            user_id = result[5]
            customer_id = result[6]
            type = result[7]
            ITEM = result[8]
            PRICE = result[9]
            Disc = result[10]
            TAX = result[11]
            States = result[12]
            ex_item = result[13]
            ex_pay = result[14]
            
            if States != "States":
                self.chart_index += 1
                if self.chart_index == len(results) or self.chart_index < 0:
                    return
                else:
                    self.update_list_items()
            
            # Create a new item using the product information
            # from founded ITEM value fill this info
            #self.Selected_items = ast.literal_eval(ITEM)
            self.Selected_items = json.loads(ITEM)
            #ITEM = json.dumps(self.Selected_items)
 
        # Update the totals in the GUI
        #self.update_totals()
        self.Update_Selected_item()
        
    def next_prev_chart(self, towhere):
        if not Chacke_Security(self, self.user, self.Shops[self.on_Shop], 12, f'User Not allowed to Use Multy Order'):
            return
        #print("in prev func with" + towhere +"\n\n")
        results = fetch_as_dict_list("SELECT id FROM pre_doc_table", ())
        p = self.chart_index
        l = -1
        n = 0
        i = 0
        #print("self.chart_index == : " + str(self.chart_index))
        for r in results:
            if r[0] == self.chart_index:
                if towhere == "next":
                    a = Chacke_Security(self, self.user, self.Shops[self.on_Shop], 4)
                    if a:
                        if not i+1 >= len(results):
                            l = results[i+1][0]
                        else:
                            l = results[0][0]
                    break
                else:
                    a = Chacke_Security(self, self.user, self.Shops[self.on_Shop], 5)
                    if a:
                        if not i-1 < 0:
                            l = results[i-1][0]
                        elif len(results)-1 < 0:
                            l = 0
                        else:
                            l = results[len(results)-1][0]
                    break
            i += 1
        if l == -1:
            if len(results) > 0:
                l = results[0][0]
            else:
                l = self.chart_index
        self.chart_index = l
                    
        self.clear_items()
        #print("index : \n" + str(self.chart_index))
        self.update_list_items()
        
    # void btn
    def clear_items(self):
        for items in self.Selected_item_Display_frame.winfo_children():
            items.destroy()
            
        for it in self.extrnal_frame.winfo_children():
            it.grid_forget()
            
        # delete all items
        self.Selected_items = []
        
        self.pid_peyment = []
        self.ex_pid_peyment = []
        self.items = []
        self.ex_items = []
        self.custemr = ""
        self.disc = 0
        
    def call_chartForm(self):
        v = ShowchartForm(self)
        if v.value != self.chart_index:
            self.chart_index = v.value
            self.clear_items()
           #print("selected chart : "+ str(v.value))
            self.update_list_items()
            
    def new_chart(self):
        if len(self.Selected_items) > 0:
            if Chacke_Security(self, self.user, self.Shops[self.on_Shop], 10, f'User Not allowed to Use Multy Order'):
                index = 0
                while(True):
                    res = fetch_as_dict_list(f"SELECT id FROM pre_doc_table WHERE id = {index}", ())
                    if not res:
                        break
                    else:
                        index += 1
                self.chart_index = index
                self.clear_items()
                self.update_list_items()
                
    def remove_item(self, index, selected_frame):
        if Chacke_Security(self, self.user, self.Shops[self.on_Shop], 13, f'User Not allowed to Delete Items'):
            answer = tk.messagebox.askquestion("Question", "Do you whant to Delete "+str(self.Selected_items[index])+" items?")
            if answer == 'yes':
                self.selected_indexd = -1
                self.Selected_items.remove(self.Selected_items[index])
                selected_frame.destroy()
                self.Update_Selected_item()
                
    
            
    def void_(self):
        if Chacke_Security(self, self.user, self.Shops[self.on_Shop], 11, f'User Not allowed to Use Multy Order'):
            answer = tk.messagebox.askquestion("Question", "Do you whant to void order?")
            if answer == 'yes':
                 # call void         
                self.void_items()
            
    def void_items(self):
        self.clear_items()
        # delete this list on db
        Update_table_database("DELETE FROM pre_doc_table WHERE id=?", (self.chart_index,))
        # self.update_info() will be called in next_prev_chart 
        self.next_prev_chart("prev")
        
    # about add item btn
    def Create_Unowen_item(self):
        if not Chacke_Security(self, self.user, self.Shops[self.on_Shop], 8, f'User Not allowed to Create Uknown Item'):
            return
        # get item info
        #id = GetvalueForm(self, '1', "Enter Item ID")
        #name = GetvalueForm(self, 'Item Name', "Enter Item Name")
        itempriceandcost = GetvalueForm(self, '0', ["Enter Item Price", "How much cost?"])
        
        if itempriceandcost == None or itempriceandcost.value == [] or len(itempriceandcost.value) <= 0:
            return
        
        uitemprice = itempriceandcost.value[0]
        if len(itempriceandcost.value) == 2:
            uitemcost = itempriceandcost.value[1]
        
        self.add_item({
            'type': 'UnKNOWN',
            'values': {'id': -1, 'name': 'Unknown Item', 'price': uitemprice, 'cost': uitemcost, 'include_tax': False, 'more_info': ''},
            'item_list':[], 'extra_data': [],
        })
        
    # this will add item to the list
    def add_item(self, item_info):
       #print("item_info = " + str(item_info))
        if (item_info['type'] == "UnKNOWN"):
            items = item_info['values']
            # selected_data = Id, code, color, size, qty, left, barcode, extr
            
            # in chake_action we will chack if item is in the list or not
            # id, code, barcode, name, color, size, qty, price, disc, includetax, total_price, shop, extr

            value = [str(items['id']), "Unkown_Code", "Unkown_barcode", items['name'], "Unkown_Color", "Unkown_size", 1, items['price'], items['price']-self.disc, items['include_tax'], items['price'], self.Shops_Names[0], ""]
            self.Selected_items.append([item_info, str(value[0]), value[1], value[2], value[3], value[4], value[5], value[6], value[7], "", value[8], value[9], value[10], value[11], value[12], ""])        

        if (item_info['type'] == "ITEM"):
            for data in item_info['extra_data']:
                shop = self.Shops_Names
                if self.Selected_Shop != "":
                    shop = [self.Selected_Shop]
                items, doc, selected_type, barcode, shop_name, code, color, size, qty = \
                     item_info['values'], None, item_info['type'], data[6], data[0], data[1], data[2], data[3], data[4]
                if data[7] != []:
                    for t, typ in enumerate(data[7]):                            
                        QTY = int(typ[1])
                        PRICE = int(typ[2])
                        value = [str(items['id']), code, barcode, items['name'], color, size, float(QTY), PRICE, self.disc, items['include_tax'], float(QTY)*float(PRICE), shop_name, ""]
                        self.Selected_items.append([item_info, str(value[0]), value[1], value[2], value[3], value[4], value[5], value[6], value[7], data[5], PRICE, value[9], value[10], value[11], value[12], typ[0]])
                else:
                    value = [str(items['id']), code, barcode, items['name'], color, size, float(qty), items['price'], self.disc, items['include_tax'], float(qty)*float(items['price']), shop_name, '']
                    self.Selected_items.append([item_info, str(value[0]), value[1], value[2], value[3], value[4], value[5], value[6], value[7], data[5], item_info['values']['price'], value[9], value[10], value[11], value[12], ""])
                self.disc = 0
        
        if(item_info['type'] == 'ACTIONS'):
           #print("item_info['values'] " + str(item_info['values']))
           #print("item_info['values'][6] " + str(item_info['values'][6]))
           #print("item_info['values'][6][1] " + str(item_info['values'][6][1]))
            for action in item_info['values'][6][1]:
                self.Selected_items.append(action)
                
        if (item_info['type'] == "DOCUMENT"):
            items = json.loads(item_info['values']['item'])
            for item in items:
                it = fetch_as_dict_list("SELECT * FROM product WHERE id=?", 
                                (item[0],))[0]
                if it:
                    doc_item_info = {'values': it, 'type': 'DOCUMENT', 'item_list':[]}
                    #print("items===========%%%%%%% = " + str(it))
                   #print("items===========%%%%%%% = " + str(item))
                   #print("doc_item_info ===========%%%%%%% = " + str(doc_item_info))
                    # TODO: last empty one is type find it
                    typ = ""
                    if len(item) > 11:
                        typ = item[11]
                    qtyleft = "??"
                    self.Selected_items.append([doc_item_info, str(item[0]), item[1], item[2], item[3], item[5], item[6], item[7], item[8], qtyleft, item[8], item[10], 0, item[4], item_info['values']['doc_barcode'], typ]) 
                else:
                    pass
        
        self.Update_Selected_item()
        
    def add_payment(self, items, doc, selected_type, barcode):
        if not barcode in self.ex_pid_peyment:
            self.ex_pid_peyment.append(barcode)
        if (selected_type == "DOCUMENT"):
            for item in items:
                if len(item) == 6:   
                    item.append(1)
                if len(item) == 7:
                    item.append(barcode)
                if len(item) >= 7:
                    item[7] = barcode
               #print("doc barcode = "+ str(barcode))
               #print("doc payment = "+ str(item))
                self.pid_peyment.append(item)
       #print("add_payment self.pid_peyment = " + str(self.pid_peyment))

    


    def get_ex_doc_items(self, item_info):
        self.add_item(item_info)
        self.qty = 0

    def get_ex_doc_payments(self, item_info):
       #print("items===========%%%%%%% = " + str(item_info))
        b = json.loads(item_info['values']['payments'])
       #print("items===========%%%%%%% = " + str(b))
        self.add_payment(b, item_info['values'], "DOCUMENT", item_info['values']['doc_barcode'])
        self.qty = 0

    # about settings
    def open_drower(self):
        if Chacke_Security(self, self.user, self.Shops[self.on_Shop], 8, f'User Need Permetion To Open Cash Drower'):
           PrinterForm.open_drower(self, self.user)

    # Function called when a payment button is clicked to make quike payment
    # it will get value from user if price is same to pid or give it will prosess payment
    def Q_Payment(self, event, text):
       #print("alt + " + str(text))
        p = 0
        for pid in self.pid_peyment:
            p += float(pid[2])
        i = GetvalueForm(self, str(self.total-p), ["Make " + str(text) + " Peyment"])
        if i and i.value[0] and i.value[0] > 0:
            self.pid_peyment.append([len(self.pid_peyment), str(text), str(i.value[0]), "", "", "", "", ""])
            p += float(i.value[0])
        if p > 0 and p >= self.total:
           #print("call_payment self.pid_peyment = " + str(self.pid_peyment))
            self.process_payment()
                     
    # splitpayment btn
    def call_splitpayment(self):
        if len(self.Selected_items) > 0 or len(self.pid_peyment) > 0:
            PaymentForm(self)
        else:
           print("no list ", len(self.Selected_items))
    
    # about payment
    def process_payment(self):
        
        
        if Chacke_Security(self, self.user, self.Shops[self.on_Shop], 22, f'User Not allowed to Sell'):
           #print("user "+str(self.user))
            answer = tk.messagebox.askquestion("Question", "do you whant to continue?")
            if answer != 'yes':
                return
            # GET COPY OF ALL GIVEN INFO
            list_items_copy = self.Selected_items
            todaydate = str(datetime.datetime.now().strftime('%Y')) + "-"+str(datetime.datetime.now().strftime('%m')) + "-"+str(datetime.datetime.now().strftime('%d'))
            givendate = self.date_year_Spinbox.get() + "-"+self.date_month_Spinbox.get() + "-"+self.date_day_Spinbox.get()

            if todaydate != givendate:
                answer = tk.messagebox.askquestion("Question", "Given date "+givendate+" and today date "+todaydate+" Is Not Same Wolde You Like To Fixe It?")
                if answer == 'yes':
                    self.date_day_Spinbox.set(str(datetime.datetime.now().strftime('%d')))
                    self.date_month_Spinbox.set(str(datetime.datetime.now().strftime('%m')))
                    self.date_year_Spinbox.set(str(datetime.datetime.now().strftime('%Y')))
            givendate = self.date_year_Spinbox.get() + "-"+self.date_month_Spinbox.get() + "-"+self.date_day_Spinbox.get()
            today_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
            date = givendate + " " + datetime.datetime.now().strftime('%H:%M')

            payments_extra = []
            extra_payment_needs = []
            
            Seller_id = None
            payment_item_required = 0
            payment_open_drower = 0
            payment_print_slip = 1
            payment_customer_required = 0
            payment_enable = 0
            payment_change_allowed = 0
            payment_mark_pad = 0
            
            item_tobechanged = []
            
            
            brcod = ""

            # doc_code = "1"
            # Year:Month-docType 1 doccreateplatform 1 doc_numb
            #TODO make it create randim number so that ont to count
            # create a mostly-unique doc barcode using timestamp (avoids needing extra imports)
            doc_code = datetime.datetime.now().strftime('%y:%m') + "-11"
            # use current microseconds as suffix to reduce collisions
            suffix = datetime.datetime.now().strftime('%f')
            while True:
                candidate = doc_code + suffix
                # use existing cursor 'cur'
                ex_doc = cur.execute("SELECT * FROM doc_table WHERE doc_barcode=?", (candidate,)).fetchone()
                if ex_doc:
                    # fallback: increment numeric suffix until unique
                    try:
                        suffix = str(int(suffix) + 1)
                    except Exception:
                        suffix = '1'
                else:
                    brcod = candidate
                    break
            # ex_item = [each item [barcode, isitem, ispay, ex_item, ex_item_items, payments, ex_payment_count, ex_item_pric, ex_item_T_disc, ex_item_T_tax, ex_pid]
            ex_docs_info = []

            
            payments_ = []
            pay_index = 0
            itemforslip = ""
            item = "" # item found
            new_items = [] # item found
            count_new_items = 0 # itme counted
            price = 0 # new items price
            pid = 0   # for new items pid
            T_pid = 0 # for all pid 
            def_pid = 0# for cash with no item pid or credit
            T_disc = 0  # for total new items dics
            tax = 0  # tax
            T_tax = 0  # tax 
            change = 0
            
            doc_found = []
           #print("brcod :" + str(brcod))
            #print("count sold items :" + str(len(list_items_copy.get_children())))
           #print("sold list_items_copy :" + str(list_items_copy))
            for iv in list_items_copy:
               #print("self.ex_items :" + str(self.ex_items))
               #print("iv[11] :" + str(iv[11]))
               #print("len(iv) :" + str(len(iv)))
                if len(iv) >= 15:
                    found_index = next((i for i, d in enumerate(doc_found) if d["Barcode"] == iv[15]), -1)
                    if found_index:
                        selected_item_info = {
                            "Barcode" : iv[15],
                            'payments_' : [],
                            'pay_index' : 0,
                            'itemforslip' : "",
                            'item' : "",
                            'new_items' : [],
                            'count_new_items' : 0,
                            'price' : 0,
                            'Cost' : 0,
                            'Profite' : 0,
                            'pid' : 0,
                            'T_pid' : 0,
                            'def_pid' : 0,
                            'disc' : 0,
                            'Tdisc' : 0,
                            'T_disc' : 0,
                            'tax' : 0,
                            'T_tax' : 0,
                            'change' : ""
                        }
                        doc_found.append(selected_item_info)
                        found_index = len(doc_found) -1 

                   #print("found_index :" + str(found_index))
                   #print(str(iv[1]))
                   #print("item id " + str(iv[0]['values']['id']) + " to item")
                    if iv[0]['values']['id'] == -1:
                        # TODO : add type here
                        disc = float(iv[0]['values']['price'])-float(iv[10])
                        itl = [iv[1], iv[2], iv[3], iv[4], iv[13], iv[5], iv[6], iv[7], iv[10], disc, iv[11], (iv[0]['values']['cost'])]
                        
                        doc_found[found_index]['count_new_items'] += float(iv[7])
                        doc_found[found_index]['price'] += float(iv[7])*float(iv[10])
                        doc_found[found_index]['Cost'] = (iv[0]['values']['cost'])
                        doc_found[found_index]['Profite'] += (float(iv[10]) - (iv[0]['values']['cost']))*float(iv[7])
                        doc_found[found_index]['Tdisc'] += disc
                        doc_found[found_index]['tax'] += float(iv[10])
                        doc_found[found_index]['new_items'].append(itl)
                    
                       #print("adding " + str(iv) + " to item")
                       #print("adding " + str(iv) + " to item")
                       #print("adding " + str(iv[7]) + " to item_tobechanged")
                    else:
                        it = fetch_as_dict_list("SELECT * FROM product WHERE id=?", (iv[0]['values']['id'],))
                       #print("item it " + str(it) + " to item")
                        if it:
                            it = it[0]
                            # TODO : add type here
                            disc = float(iv[0]['values']['price'])-float(iv[10])
                            itl = [iv[1], iv[2], iv[3], iv[4], iv[13], iv[5], iv[6], iv[7], iv[10], disc, iv[11], (iv[0]['values']['cost'])]
                            
                            doc_found[found_index]['count_new_items'] += float(iv[7])
                            doc_found[found_index]['price'] += float(iv[7])*float(iv[10])
                            doc_found[found_index]['Cost'] = (iv[0]['values']['cost'])
                            doc_found[found_index]['Profite'] += (float(iv[10]) - (iv[0]['values']['cost']))*float(iv[7])
                            doc_found[found_index]['Tdisc'] += disc
                            doc_found[found_index]['tax'] += float(iv[10])
                            doc_found[found_index]['new_items'].append(itl)
                        
                           #print("adding " + str(it) + " to item")
                           #print("adding " + str(iv) + " to item")
                           #print("adding " + str(iv[7]) + " to item_tobechanged")
                            
                            item_tobechanged.append([iv[1], iv[0]['values']['more_info'], 0, str(iv[13]), str(iv[2]), str(iv[5]),str(iv[6]), str(iv[7])])            
                        else:
                            # message there is proplame on item change_item
                            erroritemsearchanswer = tk.messagebox.askquestion("Question", "There is proplame finding On one of Item Do you whant to continue?")
                            if erroritemsearchanswer != 'yes':
                                    return                  
                   #print("\n\n sold items collect :" + str(doc_found[found_index]['new_items'])+"\n\n")
                    
           #print("\n\n items collect than doc_found :" + str(doc_found)+"\n\n")
            p = 0
            while p < len(self.pid_peyment):
               #print("self.pid_peyment:" + str(self.pid_peyment))
               #print("self.ex_pid_peyment:" + str(self.ex_pid_peyment))
               #print("self.pid_peyment[p]:" + str(self.pid_peyment[p]))
                if len(self.pid_peyment[p]) > 7:  
                   #print("\n\n items collect than self.pid_peyment[p][7] :" + str(self.pid_peyment[p][7])+"\n\n")
                    found_index = next((i for i, d in enumerate(doc_found) if d["Barcode"] == self.pid_peyment[p][7]), -1)
                    if found_index:
                        selected_item_info = {
                            "Barcode" : self.pid_peyment[p][7],
                            'payments_' : [],
                            'pay_index' : 0,
                            'itemforslip' : "",
                            'item' : "",
                            'new_items' : [],
                            'count_new_items' : 0,
                            'price' : 0,
                            'pid' : 0,
                            'T_pid' : 0,
                            'def_pid' : 0,
                            'disc' : 0,
                            'Tdisc' : 0,
                            'T_disc' : 0,
                            'tax' : 0,
                            'T_tax' : 0,
                            'Profite' : 0,
                            'change' : ""
                        }
                        doc_found.append(selected_item_info)
                        found_index = len(doc_found) -1 
                    doc_found[found_index]['pay_index'] += 1
                   #print("self.pid_peyment[p]:" + str(self.pid_peyment[p]))
                    rows = 0
                    for r in self.Shop_Payment_Tools:
                        if r[0] == self.pid_peyment[p][1]:
                            rows = r
                            break
                    if rows:
                       #print("rows:" + str(rows))
                       #print("price-disc "+str(doc_found[found_index]['price']-doc_found[found_index]['Tdisc']) + ":pid " + str(doc_found[found_index]['pid']) + ":def_pid " + str(def_pid))
                        c = float(self.pid_peyment[p][2])
                       #print("c:" + str(c))
                        # "Tool Name", "Tool Method", "Tool ID", "Tool Short cut", "Tool Acsess key", "Tool enabel", "Tool Quick_pay","Tool Markpad", "Tool Customer_required", "Tool Open_drower", "Tool#printslip"
                        if rows[5] == '1': # chack if enabled
                            payment_enable += 1
                        if rows[7] == '1' and payment_mark_pad == 0: # chack if enabled
                            payment_mark_pad = 1
                        if rows[8] == '1' and payment_customer_required == 0: # chack if enabled
                            payment_customer_required = 1
                        if rows[9] == '1' and payment_open_drower == 0: # chack if enabled
                            payment_open_drower = 1
                        if rows[10] == '1' and payment_print_slip == 0: # chack if enabled
                            payment_print_slip = 1
                        '''if rows[11] == 1 and payment_change_allowed == 0: # chack if enabled
                            payment_change_allowed = 1
                        if rows[11] == 1 and payment_item_required == 0: # chack if enabled
                            payment_item_required = 1'''
                        if not rows[6]:
                            doc_found[found_index]['price'] += c
                            doc_found[found_index]['def_pid'] += c
                        
                        if doc_found[found_index]['price']-doc_found[found_index]['Tdisc'] == doc_found[found_index]['pid']:
                            if doc_found[found_index]['price']-doc_found[found_index]['Tdisc'] == 0:
                                doc_found[found_index]['payments_'].append([str(doc_found[found_index]['pay_index']), str(self.pid_peyment[p][1]), str(self.pid_peyment[p][2]), date, date, self.user['User_name'], str(rows[4]), str(self.pid_peyment[p][3]), rows[1]])
                            else:
                                payments_extra.append([str(doc_found[found_index]['pay_index']), str(self.pid_peyment[p][1]), str(self.pid_peyment[p][2]), date, date, self.user['User_name'], str(rows[4]), str(self.pid_peyment[p][3]), rows[1]])
                            #doc_found[found_index]['payments_'].append([str(doc_found[found_index]['pay_index']), str(self.pid_peyment[p][1]), str(c), date, date, self.user['User_name'], str(rows[4]), str(self.pid_peyment[p][3]), rows[1]])
                        else:
                            if doc_found[found_index]['pid'] + c > doc_found[found_index]['price']-doc_found[found_index]['Tdisc']:
                                pr = (doc_found[found_index]['price']-doc_found[found_index]['disc']) # item price
                                pl = pr-doc_found[found_index]['pid']     # price left to pay
                                if c > pl:
                                    e = c - pl
                                    payments_extra.append([str(doc_found[found_index]['pay_index']), str(self.pid_peyment[p][1]), str(e), date, date, self.user['User_name'], str(rows[4]), str(self.pid_peyment[p][3]), rows[1]])
                                    #doc_found[found_index]['payments_'].append([str(doc_found[found_index]['pay_index']), str(self.pid_peyment[p][1]), str(c), date, date, self.user['User_name'], str(rows[4]), str(self.pid_peyment[p][3]), rows[1]])
                                    c = pl # taking only what pied
                                else:
                                    c = pl
                            if rows[6]:
                               #print("pid+c ")
                                doc_found[found_index]['T_pid'] += float(self.pid_peyment[p][2])
                                doc_found[found_index]['pid'] += c
                            doc_found[found_index]['payments_'].append([str(doc_found[found_index]['pay_index']), str(self.pid_peyment[p][1]), str(c), date, date, self.user['User_name'], str(rows[4]), str(self.pid_peyment[p][3]), rows[1]])
                self.pid_peyment.remove(self.pid_peyment[p])
               #print("\n\n payments_ pid collect :" + str(doc_found[found_index]['payments_'])+"\n\n")
               #print("\n\n payments_extra pid collect :" + str(payments_extra)+"\n\n")
                
           #print("\n\n payments collect than doc_found :" + str(doc_found)+"\n\n")
            
                
            f_user_s = cursor.execute("SELECT * FROM setting WHERE User_id=?", (int(self.user['User_id']),)).fetchall()
            #print("f_user_s "+str(f_user_s))
            Seller_id = None

            for px, extra_payment in enumerate(payments_extra):
               #print("--extra_payment = " + str(extra_payment))
                c = float(extra_payment[2])
                l = 0 # doc found 
                while c > 0 and l == 0:
                    for i, d in enumerate(doc_found):
                       #print("--Barcode = " + str(d['Barcode']))
                       #print("--item = " + str(d['new_items']))
                       #print("--payments_ : " + str(d['payments_']))
                        if d['price']-d['Tdisc'] != d['pid']:
                            if d['pid'] + c > d['price']-d['Tdisc']:
                                pr = (d['price']-d['disc']) # item price
                                pl = pr-d['pid']     # price left to pay
                                if c > pl:
                                    e = c - pl
                                    # payments_extra.append([str(d['pay_index']), str(self.pid_peyment[p][1]), str(e), date, date, self.user['User_name'], str(rows[10]), str(self.pid_peyment[p][3])])
                                    payments_extra[px][2] = str(e)
                                    c = pl # taking only what pied
                                else:
                                    c = pl
                            doc_found[i]['pay_index'] += 1
                            doc_found[i]['pid'] += c
                            doc_found[i]['payments_'].append([str(doc_found[i]['pay_index']), str(extra_payment[1]), str(c), extra_payment[3], date, extra_payment[5], extra_payment[6], extra_payment[7]])
                            l += 1
                       #print("--payments_ : " + str(d['payments_']))
                    if c > 0:
                        doc_found[0]['pay_index'] += 1
                        if extra_payment[7] == "":
                            
                            doc_found[0]['payments_'].append([str(doc_found[0]['pay_index']), "Change", str(-c), extra_payment[3], date, extra_payment[5], extra_payment[6], extra_payment[7]])
                        else:
                            doc_found[0]['payments_'].append([str(doc_found[0]['pay_index']), "", str(-c), extra_payment[3], date, extra_payment[5], extra_payment[6], extra_payment[7]])
                        c = 0
            newitems = []
            for i, d in enumerate(doc_found):
                if d['Barcode'] == '':
                    newitems = d['new_items']
                    
            for i, d in enumerate(doc_found):
               #print("--Barcode = " + str(d['Barcode']))
                if d['Barcode'] != '':
                    fdoc = fetch_as_dict_list("SELECT * FROM doc_table WHERE doc_barcode=?", (d['Barcode'],))
                   #print("fdoc " + str(fdoc) + " to item")
                    if fdoc:
                        fdoc = fdoc[0]
                        items = json.loads(fdoc['item'])
                        for item in items:
                            it = fetch_as_dict_list("SELECT * FROM product WHERE id=?", (item[0],))
                            itemqty = item[7]
                            if it:
                                it = it[0]
                                for olditem in d['new_items']:
                                    if olditem[0] == item[0]:
                                        if olditem[7] < item[7]:
                                            itemqty -= olditem[7]
                                            if itemqty <= 0:
                                                break;
                                                
                                '''for exitem in newitems :
                                    if exitem[0] == item[0]:                                            
                                        if exitem[7] < item[7]:
                                            itemqty -= exitem[7]
                                            if itemqty <= 0:
                                                break;'''
                                if itemqty > 0:
                                    item_tobechanged.append([item[0], it['more_info'], 1, str(item[4]), str(item[1]), str(item[5]),str(item[6]), str(itemqty)])
                                    #print("--removeing all old qty = " + str([item[1], it['more_info'], 0, str(item[4]), str(item[1]), str(item[5]),str(item[6]), str(item[7])]))

            if f_user_s and f_user_s[0] and f_user_s[0][5]:
               #print("opning worker dialog")
                app = WorkerManagementApp(self, str(brcod), float(count_new_items))
                if app.user_details:
                   #print("app.user_details['User_id'] "+str(app.user_details['User_id']))
                    Seller_id = app.user_details['User_id']
                else:
                    return
           #print("--item_tobechanged : " + str(item_tobechanged))
            
            name = ""
            phone_num = ""
            cm_id = None
            old_cm_id = None
                            
            slip_doc_code = []
            '''while True:
                continue'''
           #print("item_tobechanged  : " + str(item_tobechanged))
            for change_item in item_tobechanged:
               #print("item : " + str(change_item[1]), change_item[2], str(change_item[3]), str(change_item[4]),str(change_item[5]), str(change_item[6]))
               #print("item info befor : " + str(change_item[1]))
                qty_info_list = []
               #print("change_item[1]  : " + str(change_item[1]))
                if change_item[1]:
                    qty_info_list = json.loads(change_item[1])
               #print("qty_info_list[1]  : " + str(qty_info_list))
                it_info = change_qty(qty_info_list, change_item[2], str(change_item[3]), str(change_item[4]), str(change_item[5]),str(change_item[6]), str(change_item[7]))

                if not it_info:
                        # message there is proplame on item change_item
                        erroriteminfoanswer = tk.messagebox.askquestion("Question", "There is Proplame On one Item Do you whant to continue?")
                        if erroriteminfoanswer != 'yes':
                                return
                                
               #print("item info befor  : " + str(it_info))
                #while True:
                #    continue
                Update_Producte(None, self.user, ['more_info'], [json.dumps(it_info)], ['id'], [change_item[0]])
                #cursor.execute('UPDATE product SET more_info=? WHERE id=?', (json.dumps(it_info), change_item[0]))

                
                it2 = fetch_as_dict_list('SELECT * FROM product WHERE id=?', (str(change_item[0]),))
                if it2 and not len(it2) == 0:
                    for i3, it3 in enumerate(self.Shops_info['Shop_items']):
                        if it3[0]['id'] == it2[0]['id']:
                            self.Shops_info['Shop_items'][i3][0] = it2[0]
                            break
                #print("item info updated : " + str(it2[0]['more_info']))
                
                # Commit the changes to the database
                conn.commit()
                
            if payment_customer_required:
                if self.custemr == "" or not self.app:
                    self.Add_Custumer()
                cm_id = self.custemr
                name = self.app.user_details['User_name']
                phone_num = self.app.user_details['User_phone_num']
               #print(self.app.user_details)

                
            for i, d in enumerate(doc_found):
               #print("--item = " + str(d['item']))
               #print("--payments_ : " + str(d['payments_']))
                if d['payments_'] == [] and payments_extra != []:
                    d['payments_'] = payments_extra
                    payments_extra = []
                    
                if d['payments_'] != [] or float(d['count_new_items']) != 0:
                        if d["Barcode"] != "":
                               #print("d[Barcode] = " + str(d["Barcode"]))
                                # Get_Document(None, self.user, ['doc_barcode'], [d["Barcode"]])
                                rows = fetch_as_dict_list("SELECT * FROM doc_table WHERE doc_barcode=?", (d["Barcode"],))
                                # cursor.execute("SELECT * FROM doc_table WHERE doc_barcode=?", (d["Barcode"],)).fetchall()
                                if rows and rows[0]['customer_id']: # if doc found
                                    old_cm_id = rows[0]['customer_id']
                                
                               #print("cmd old id = " + str(rows[0]) + " new id " + str(cm_id))
                                if cm_id and old_cm_id != str(cm_id):
                                    #[each item [barcode, isitem, ispay, ex_item, ex_item_items, payments, ex_payment_count, ex_item_pric, ex_item_T_disc, ex_item_T_tax, ex_pid]
                                    Update_Documente(None, self.user, ['customer_id'], [cm_id], ['doc_barcode'], [d["Barcode"]])

                                    # cursor.execute('UPDATE doc_table SET customer_id=? WHERE doc_barcode=?', (cm_id, d["Barcode"]))
                                    # Commit the changes to the database
                                    # conn.commit()
                                if Seller_id != None:
                                    #[each item [barcode, isitem, ispay, ex_item, ex_item_items, payments, ex_payment_count, ex_item_pric, ex_item_T_disc, ex_item_T_tax, ex_pid]
                                    Update_Documente(None, self.user, ['Seller_id'], [Seller_id], ['doc_barcode'], [d["Barcode"]])
                                    # cursor.execute('UPDATE doc_table SET Seller_id=? WHERE doc_barcode=?', (Seller_id, d["Barcode"]))
                                    # Commit the changes to the database
                                    # conn.commit()
                                    
                                if d['payments_']:
                                    #todo if needed add pid in doc e_doc_info[10]
                                    Update_Documente(None, self.user, ['pid', 'payments', 'doc_updated_date'], [str(d['pid']), json.dumps(d['payments_']), today_date], ['doc_barcode'], [d["Barcode"]])
                                    # cursor.execute('UPDATE doc_table SET pid=?, payments=?, doc_updated_date=? WHERE doc_barcode=?', (str(d['pid']), json.dumps(d['payments_']), today_date, d["Barcode"]))
                                    # Commit the changes to the database
                                    #conn.commit()

                                #[each item [barcode, isitem, ispay, ex_item, ex_item_items, payments, ex_payment_count, ex_item_pric, ex_item_T_disc, ex_item_T_tax, ex_pid]
                                Update_Documente(None, self.user, ['item', 'qty', 'price', 'Profite', 'discount', 'tax', 'doc_updated_date'], [json.dumps(d['new_items']), float(d['count_new_items']), d['price'], d['Profite'], d['Tdisc'], d['tax'], today_date], ['doc_barcode'], [d["Barcode"]])
                                # cursor.execute('UPDATE doc_table SET item=?, qty=?, price=?, Profite=?, discount=?, tax=?, doc_updated_date=? WHERE doc_barcode=?', (json.dumps(d['new_items']), float(d['count_new_items']), d['price'], d['Profite'], d['Tdisc'], d['tax'], today_date, d["Barcode"]))
                                # Commit the changes to the database
                                # conn.commit()
                                
                                slip_doc_code.append(d["Barcode"])
                        elif d["Barcode"] == "":
                               #print("custemer : " + str(self.custemr) + "isneded : " + str(payment_customer_required))
                                # TODO: chacke if self.At_Shop_Id is selected if not make user selecte one
                                Set_Document(None, ["doc_barcode", "extension_barcode", "At_Shop_Id", "user_id", "customer_id", "Seller_id", "type", "item", "qty", "price", "discount", "tax", "payments", "pid", "doc_created_date", "doc_expire_date", "doc_updated_date"], [str(brcod), "extension_barcode", self.At_Shop_id, self.user['User_id'], self.custemr, Seller_id, "Sale_item", json.dumps(d['new_items']), float(d['count_new_items']), d['price'], d['Tdisc'], d['tax'], json.dumps(d['payments_']), d['T_pid'], date, date, today_date])
                                #cursor.execute('INSERT INTO upload_doc (doc_barcode, extension_barcode, At_Shop_Id, user_id, customer_id, Seller_id, type, item, qty, price, discount, tax, payments, pid, doc_created_date, doc_expire_date, doc_updated_date) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (str(brcod), "extension_barcode", self.At_Shop_id, self.user['User_id'], self.custemr, Seller_id, "Sale_item", json.dumps(d['new_items']), float(d['count_new_items']), d['price'], d['Tdisc'], d['tax'], json.dumps(d['payments_']), d['T_pid'], date, date, today_date))
                                #cursor.execute('INSERT INTO doc_table (doc_barcode, extension_barcode, At_Shop_Id, user_id, customer_id, Seller_id, type, item, qty, price, Profite, discount, tax, payments, pid, doc_created_date, doc_expire_date, doc_updated_date) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (str(brcod), "extension_barcode", self.At_Shop_id, self.user['User_id'], self.custemr, Seller_id, "Sale_item", json.dumps(d['new_items']), float(d['count_new_items']), d['price'], d['Profite'], d['Tdisc'], d['tax'], json.dumps(d['payments_']), d['T_pid'], date, date, today_date))
                                # Commit the changes to the database
                                #conn.commit()
                                slip_doc_code.append(brcod)
                                
            # call void         
            self.void_items()
            self.manage_form.doc_form.load_documents(slip_doc_code)
            
            if payment_open_drower == 1:
               PrinterForm.open_drower(self, self.user)
             #TODO: MAKE IT SEND SELECTEd SHOP
            ApproveFrame(self, self.user, self.Shops[0], slip_doc_code, payments_extra, payment_print_slip)




                


    def Add_Custumer(self):
        if Chacke_Security(self, self.user, self.Shops[self.on_Shop], 21, f'User Not allowed to Search for Custumers'):
            self.app = UserManagementApp(self, "", self.user, self.Shops, self.on_Shop)
            if self.app.user_details:
                self.custemr = self.app.user_details['User_id']
                self.Add_custemur_label.config(text=self.app.user_details['User_name'])
            else:
                self.Add_custemur_label.config(text="+ Custumer")
        


    # loading all setting 
    def load_setting(self):
        setting = Get_Setting(self.user, ["User_id"], [self.user['User_id']])
       
        if not setting or len(setting) == 0:
            Set_Setting(self.user, ["User_id", "barcode_count", "printer"], [self.user['User_id'], 0, ""])
        else:
            #print("sitting : " + str(b))
            pass
        

    # display buttons profermans
    def load(self):
        self.master.show_frame("DisplayFrame")
        self.load_setting()
        #ApproveFrame(self, [])

    def on_tab_selected(self, event):
        selected_tab = self.main_Notebook.index(self.main_Notebook.select())
        if selected_tab == 1:
            a = Chacke_Security(self, self.user, self.Shops[self.on_Shop], 12)
            if not a:
                self.main_Notebook.select(0)

    # Function to perform the backup
    def backup_database(self):
        # Database file paths
        database_file = 'data/my_database.db'
        backup_folder = 'backup/'
        max_backups = self.max_backups
        # Create the backup folder if it doesn't exist
        os.makedirs(backup_folder, exist_ok=True)
        
        # List existing backup files
        existing_backups = sorted(os.listdir(backup_folder))
        
        # Delete oldest backups if exceeding the maximum allowed
        if len(existing_backups) >= max_backups:
            num_backups_to_delete = len(existing_backups) - max_backups + 1
            for i in range(num_backups_to_delete):
                file_to_delete = os.path.join(backup_folder, existing_backups[i])
                os.remove(file_to_delete)
               #print("Deleted old backup:", file_to_delete)
        
        # Create a backup file name
        backup_file = os.path.join(backup_folder, 'backup_' + datetime.datetime.now().strftime('%Y-%m-%d_%H-%M') + '.db')
        
        # Connect to the database
        conn = sqlite3.connect(database_file)
        
        try:
            # Create a backup by copying the database file
            shutil.copy2(database_file, backup_file)
           #print("Backup created successfully:", backup_file)
        except IOError as e:
           print("Error creating backup:", str(e))
        finally:
            # Close the database connection
            conn.close()
            
    def Call_Uploading_Form(self):
        if Chacke_Security(self, self.user, self.Shops[self.on_Shop], 25, f'User Not allowed to Upload Documents'):
            UploadingForm(self, self.user, self.Shops)

    
