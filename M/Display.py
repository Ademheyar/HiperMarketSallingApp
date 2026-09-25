import tkinter as tk
from tkinter import ttk, filedialog
from PIL import Image, ImageTk
import os, shutil
import sqlite3
import shutil
import datetime
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
from M.Setting import Appelication_SettingForm
from D.printer import PrinterForm
from C.slipe import load_slip
from D.Doc.Loaddoc import *
from D.Security import *
from C.List import *
from M.Actions import ActionsForm

from D.docediterform import DocEditForm

from C.API.Get import *
from C.API.API import *
from C.API.Set import *

from C.Manager import ManageForm

data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data'))
db_path = os.path.join(data_dir, 'my_database.db')


class DisplayFrame(tk.Frame):
    def __init__(self, master, Shops_info, user, User_Shops_List, Shops):
        tk.Frame.__init__(self, master)
        
        self.onDisplayFrame = "" # to show this is manin display


        self.homemaster = self
        while(True):
            if hasattr(self.homemaster, 'onDisplayFrame'):
                break
            else:
                self.homemaster = self.homemaster.master
        #print("self.User_data : ", self.User_data)

        self.MainApplication = self
        while(True):
            if hasattr(self.MainApplication, 'MainApplication_root'):
                break
            else:
                self.MainApplication = self.MainApplication.master
        
        self.Shops = Shops
        # this will hold documant that are searched from doc.py file 
        self.Todays_docs = []
        
        self.bg_dark = "#0d47a1"      # Deep blue
        self.bg_light = "#1565c0"     # Darker blue
        self.accent_blue = "#1976d2"  # Medium blue
        self.text_light = "#ffffff"   # White text
        self.bg_darker = "#0a3d91"    # Even darker blue
        self.button_style = {"font": ("Arial", 11, "bold"), "bg": self.accent_blue, "fg": self.text_light, "activebackground": self.bg_light, "activeforeground": self.text_light, "relief": tk.FLAT, "bd": 0}
        
        self.homemaster = self
        self.configure(bg=self.bg_dark)
        
        self.user = user
        self.Shops_info = Shops_info
        self.User_Shops_List = User_Shops_List
        self.Selected_Shop = ""
        self.Shop_Payment_Tools = []
        self.Selected_items = []
        self.items = []
        
       #print("Disktop user : " + str(self.user))
        self.custemr = "" # for holding user or costumer name
        self.app = None # for holding user or costumer name
        self.chart_index = None
        self.price = 0
        self.pid = 0
        self.creadit = 0
        self.tax = 0
        self.qty = 0
        self.disc = 0
        self.total = 0
        self.pid_peyment = []
        self.ex_pid_peyment = []
        self.Loded_payment_buttons = []
        self.ex_items = []
        self.ex_doc = []

        self.At_Shop_id = -1
        self.on_Shop = -1         
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        #print("Display Frame Initialized with screen size: {}x{}".format(screen_width, screen_height))
        
        if Shops_info is None or user is None or User_Shops_List is None or Shops is None:
            #print("Critical data missing (Shops_info, user, User_Shops_List, or Shops)")
            if not Security_get_user(self):
                #print("No user data found, closing application.")
                self.master.destroy()
                return
            else:
                self.grid(row=0, column=0, sticky="nsew")
                #print("User data loaded successfully")

        self.Shops_Names = [shop['Shop_name'] for shop in self.Shops]
        self.Shops_brands = [shop['Shop_brand_name'] for shop in self.Shops]

        
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

        
        self.DFsearch_entry = search_entry(self.top_frame, self.Shops_info, self.user, self.Shops, font=("Arial", 12))
        self.DFsearch_entry.grid(row=0, column=2, columnspan=4, sticky="nsew", padx=1, pady=1)


        self.Calculter_button = tk.Button(self.top_frame, text="Calcu\nF1", command=lambda: GetvalueForm(self, '0', ["Calculater"]), **self.button_style)
        self.Calculter_button.grid(row=0, column=0, sticky="nsew", padx=2, pady=5)
        self.master.bind("<F1>", lambda _: GetvalueForm(self, '0', ["Calculater"]))
        
        self.Add_None_item_button = tk.Button(self.top_frame, text="None\nF2", command=lambda: DocEditForm.Create_Unowen_item(self), **self.button_style)
        self.Add_None_item_button.grid(row=0, column=1, sticky="nsew", padx=2, pady=5)
        self.master.bind("<F2>", lambda _: DocEditForm.Create_Unowen_item(self))
        
        self.activets_button = tk.Button(self.top_frame, text="Activets\nF6", command=self.call_chartForm, **self.button_style)
        self.activets_button.grid(row=0, column=9, sticky="nsew", padx=1, pady=1)
        self.master.bind("<F6>", lambda _: self.call_chartForm())
        
        self.payment_button = tk.Button(self.top_frame, text="Payment\nF10", command=self.call_splitpayment, **self.button_style)
        self.payment_button.grid(row=0, column=10, sticky="nsew", padx=1, pady=1)
        self.master.bind("<F10>", lambda _: self.call_splitpayment())
        
        self.endday_button = tk.Button(self.top_frame, text="Cash Drawer\nCtrl+D", command=lambda: self.open_drower(), **self.button_style)
        self.endday_button.grid(row=0, column=11, sticky="nsew", padx=1, pady=1)
        
        self.update_button = tk.Button(self.top_frame, text="Update\nCtrl+U", command=lambda: self.Call_Uploading_Form()) #, **self.button_style)
        self.update_button.grid(row=0, column=12, sticky="nsew", padx=1, pady=1)
        
        self.Endday_button = tk.Button(self.top_frame, text="End Day\nCtrl+E", command=lambda: self.manage_form.doc_form.perform_endday(), **self.button_style)
        self.Endday_button.grid(row=0, column=13, sticky="nsew", padx=1, pady=1)
        
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
                                                 command=self.item_List_canvas.yview, bg=self.bg_light, activebackground=self.accent_blue)
        self.item_List_yscrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.item_List_xscrollbar = tk.Scrollbar(self.List_Frame_contaner_frame, orient='horizontal', 
                                                 command=self.item_List_canvas.xview, bg=self.bg_light, activebackground=self.accent_blue)
        self.item_List_xscrollbar.pack(side=tk.TOP, fill=tk.X)
        
        self.item_List_canvas.configure(xscrollcommand=self.item_List_xscrollbar.set, 
                                       yscrollcommand=self.item_List_yscrollbar.set)

        self.Selected_item_Display_frame = tk.Frame(self.item_List_canvas, bg=self.bg_dark)
        self.window_id = self.item_List_canvas.create_window((0, 0), window=self.Selected_item_Display_frame, anchor=tk.NW)

        def resize(event):
            screen_width = self.winfo_screenwidth()
            screen_height = self.winfo_screenheight()
                
            self.item_List_canvas.configure(scrollregion=self.item_List_canvas.bbox("all"))
            self.item_List_canvas.itemconfig(self.window_id, width=screen_width-(screen_width/4))
        self.Selected_item_Display_frame.bind('<Configure>', resize)

        self.side_frame = tk.Frame(self.main_frame, bg=self.bg_darker)
        self.side_frame.grid(row=1, column=1, rowspan=1, sticky="nsew")
        
        self.buttons_frame = tk.LabelFrame(self.side_frame, text="Payment Tools", height=150, bg=self.bg_light, padx=5, pady=5)
        self.buttons_frame.pack(side="top", fill="both", expand=True)

        self.buttons_frame.columnconfigure((0, 1, 2, 3, 4, 5, 6), weight=1, minsize=int(self.buttons_frame.winfo_height() *0.1))
        self.buttons_frame.rowconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8, 9), weight=1, minsize=int(self.buttons_frame.winfo_height() *0.1))


        self.total_frame = tk.Frame(self.side_frame, height=150, bg=self.bg_light, highlightthickness=2, highlightbackground=self.bg_dark)
        self.total_frame.pack(side="bottom", fill="both", expand=False)

        self.total_frame.columnconfigure((0, 1, 2, 3), weight=1, minsize=int(self.total_frame.winfo_height() *0.1))
        self.total_frame.rowconfigure((0, 1, 2, 3, 4, 5, 6), weight=1, minsize=int(self.total_frame.winfo_height() *0.1))
        
        self.prevlist_button = tk.Button(self.total_frame, text="<<<\nF4", command=lambda: self.next_prev_chart("prev"), **self.button_style)
        self.prevlist_button.grid(row=0, column=0, sticky="nsew")
        #self.prevlist_button.config(state=tk.DISABLED)

        self.barcode_label = tk.Label(self.total_frame, text="Barcode", font=("Arial", 12, "bold"), bg=self.bg_light, fg=self.text_light)
        self.barcode_label.grid(row=0, column=1, columnspan=5, sticky="nsew", padx=5, pady=5)
        
        self.nextlist_button = tk.Button(self.total_frame, text="New\nF7", command=lambda : self.next_prev_chart("Next"), **self.button_style)
        self.nextlist_button.grid(row=0, column=6, sticky="nsew")
        #self.nextlist_button.config(state=tk.DISABLED)
        self.master.bind("<F4>", lambda _: self.next_prev_chart("Prev"))
        self.master.bind("<F3>", lambda _: self.void_())
        self.master.bind("<F5>", lambda _: self.next_prev_chart("Next"))
        self.master.bind("<F7>", lambda _: self.new_chart(1))


        tk.Label(self.total_frame, text="Total Items : ", font=("Arial", 12, "bold"), bg=self.bg_light, fg=self.text_light).grid(row=1, column=0, columnspan=3, sticky="nsew", padx=5, pady=5)
        self.total_items_label = tk.Label(self.total_frame, text="0", font=("Arial", 12, "bold"), bg=self.bg_light, fg=self.text_light)
        self.total_items_label.grid(row=1, column=3, columnspan=2, sticky="nsew", padx=5, pady=5)
        
        tk.Label(self.total_frame, text="Total Tax : ", font=("Arial", 12, "bold"), bg=self.bg_light, fg=self.text_light).grid(row=2, column=0, columnspan=3, sticky="nsew", padx=5, pady=5)
        self.total_tax_label = tk.Label(self.total_frame, text="Total Tax : 0", font=("Arial", 12, "bold"), bg=self.bg_light, fg=self.text_light)
        self.total_tax_label.grid(row=2, column=3, columnspan=2, sticky="nsew", padx=5, pady=5)
        
        tk.Label(self.total_frame, text="Item Discount : ", font=("Arial", 12, "bold"),  bg=self.bg_light, fg=self.text_light).grid(row=3, column=0, columnspan=3, sticky="nsew", padx=5, pady=5)
        self.total_discount_label = tk.Label(self.total_frame, text="0", font=("Arial", 12, "bold"),  bg=self.bg_light, fg=self.text_light)
        self.total_discount_label.grid(row=3, column=3, columnspan=2, sticky="nsew", padx=5, pady=5)
        
        tk.Label(self.total_frame, text="Total Discount : ", font=("Arial", 12, "bold"),  bg=self.bg_light, fg=self.text_light).grid(row=4, column=0, columnspan=3, sticky="nsew", padx=5, pady=5)
        self.total_tdiscount_label = tk.Label(self.total_frame, text="0", font=("Arial", 12, "bold"),  bg=self.bg_light, fg=self.text_light)
        self.total_tdiscount_label.grid(row=4, column=3, columnspan=2, sticky="nsew", padx=5, pady=5)
        
        tk.Label(self.total_frame, text="Price Befor: ", font=("Arial", 12, "bold"),  bg=self.bg_light, fg=self.text_light).grid(row=5, column=0, columnspan=3, sticky="nsew", padx=5, pady=5)
        self.total_price_label = tk.Label(self.total_frame, text="0", font=("Arial", 12, "bold"),  bg=self.bg_light, fg=self.text_light)
        self.total_price_label.grid(row=5, column=3, columnspan=2, sticky="nsew", padx=5, pady=5)
        
        tk.Label(self.total_frame, text="Total After: ", font=("Arial", 16, "bold"),bg=self.bg_light, fg="#4dd0e1").grid(row=6, column=0, columnspan=3, sticky="nsew", padx=5, pady=5)
        self.total_label = tk.Label(self.total_frame, text="0", font=("Arial", 16, "bold"),bg=self.bg_light, fg="#4dd0e1")
        self.total_label.grid(row=6, column=3, columnspan=2, sticky="nsew", padx=5, pady=5)





        self.manage_form = ManageForm(self.main_Notebook, self.user, self.Shops, self.Shops_info, self.on_Shop)
        
        self.bottum_frame = tk.Frame(self.main_frame, height=150, bg=self.bg_light)
        self.bottum_frame.grid(row=2, column=0, rowspan=2, columnspan=4, sticky="nsew")

        self.bottum_frame.columnconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8), weight=1, minsize=int(self.bottum_frame.winfo_height() *0.1))
        self.bottum_frame.rowconfigure((0), weight=1, minsize=int(self.bottum_frame.winfo_height() *0.1))
        
        self.Veaw_Notifications_label = tk.Label(self.bottum_frame, text="Notifications", font=("Arial", 10, "bold"),
                                                 fg="#4dd0e1", bg=self.bg_light, cursor="hand2")
        self.Veaw_Notifications_label.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        self.Veaw_Notifications_label.bind("<Button-1>", lambda _: Veaw_Notifications(self, self.user, self.Shops))

        self.Loged_user_label = tk.Label(self.bottum_frame, text=str(self.user['User_name']), font=("Arial", 10, "bold"),
                                         fg="#4dd0e1", bg=self.bg_light, cursor="hand2")
        self.Loged_user_label.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
        self.Loged_user_label.bind("<Button-1>", lambda _: UserInfoForm(self, self.user))
                              
        self.User_Shopes_Combobox = ttk.Combobox(self.bottum_frame, values=self.Shops_Names, width=10)
        self.User_Shopes_Combobox.grid(row=0, column=2, sticky="nsew", padx=5, pady=5)
        

        self.at_shop_name = ""
        self.Shop_brand_name = self.Shops[0]['Shop_brand_name']
        if(len(self.Shops_Names) == 1):
            #print("Only one shop found, selecting it by default.")
            #print("Shop Name: ", self.Shops)
            Shop_brand_name = self.Shops[0]['Shop_brand_name']
            self.At_Shop_id = self.Shops[0]['Shop_Id']
            at_shop_name = self.Shops[0]['Shop_name']
            self.on_Shop = 0
        else:
            pass
        
        self.At_Shop_label = tk.Label(self.bottum_frame, text=str(at_shop_name), font=("Arial", 10, "bold"),
                                      fg="#4dd0e1", bg=self.bg_light, cursor="hand2")
        self.At_Shop_label.grid(row=0, column=3, sticky="nsew", padx=5, pady=5)
        self.At_Shop_label.bind("<Button-1>", lambda _: UserInfoForm(self))

        self.Add_custemur_label = tk.Label(self.bottum_frame, text="+ Custumer", font=("Arial", 10, "bold"),
                                           fg="#4dd0e1", bg=self.bg_light, cursor="hand2")
        self.Add_custemur_label.grid(row=0, column=4, sticky="nsew", padx=5, pady=5)
        self.Add_custemur_label.bind("<Button-1>", lambda _: self.Add_Custumer())

        self.date_day_Label = tk.Label(self.bottum_frame, text="H:M D-M-Y :" , font=("Arial", 9, "bold"), 
                           width=20, bg=self.bg_light, fg=self.text_light)
        
        # Update the label with the current date/time every second
        def _update_datetime():
            now = datetime.datetime.now().strftime('%H:%M')
            self.date_day_Label.config(text=now + " D-M-Y :")
            self.date_day_Label.after(100, _update_datetime)
        _update_datetime()

        self.date_day_Label.grid(row=0, column=5, sticky="w", padx=2, pady=5)
        
        self.date_day_Spinbox = ttk.Spinbox(self.bottum_frame, from_=1, to=31, width=5)
        self.date_day_Spinbox.grid(row=0, column=6, sticky="w", padx=2, pady=5)
        self.date_day_Spinbox.set(str(datetime.datetime.now().strftime('%d')))
        
        self.date_month_Spinbox = ttk.Spinbox(self.bottum_frame, from_=1, to=13, width=5)
        self.date_month_Spinbox.grid(row=0, column=7, sticky="w", padx=2, pady=5)
        self.date_month_Spinbox.set(str(datetime.datetime.now().strftime('%m')))
        
        self.date_year_Spinbox = ttk.Spinbox(self.bottum_frame, from_=1990, width=5)
        self.date_year_Spinbox.grid(row=0, column=8, sticky="w", padx=2, pady=5)
        self.date_year_Spinbox.set(str(datetime.datetime.now().strftime('%Y')))
    
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
        
        self.next_prev_chart("Next") # load the prev item will staring if there is 
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
        
        self.appleication_frame = tk.Frame(self.main_Notebook, bg=self.bg_dark)
        self.appleication_frame.grid()
        self.main_Notebook.add(self.appleication_frame, text='Appelication Settings')
        self.appleication_form = Appelication_SettingForm(self.appleication_frame, self.user, self.Shops)
        self.appleication_form.pack(side="top", fill="both", expand=True)
        
        self.load()
            
    def Veaw_Notifications(self):
        pass
    
    def Load_Shop_items(self):
        self.Shops_info['Shop_items'] = []
        for s, shop in enumerate(self.Shops):
            #print("Loop Shop ", shop['Shop_name'])
            #print("Selected Shop ", self.shop_name_Combobox.get())
            #print("Shop items = ", shop['Shop_items'])
            FOUND = []
            if shop['Shop_items'] and (shop['Shop_name'] == "" or s == self.User_Shopes_Combobox.current() or self.User_Shopes_Combobox.current() == ""):
                found_shop_items = json.loads(shop['Shop_items'])
                #print("Shop items --> ", found_shop_items)
                if found_shop_items:
                    for item in found_shop_items:
                        #print('item -- > ', item)
                        if not item[0] in FOUND:
                            FOUND.append(item[0])
                        value = fetch_as_dict_list(self.Link, 'SELECT * FROM product WHERE id=?', (str(item[0]),))
                        #print("Shop items value --> ", value[0])
                        if value and not len(value) == 0:
                            self.Shops_info['Shop_items'].append([value[0], [], "", "", "", "", "", "", "", "", "", "", ""])
                            
                            #print('items = ', self.master.master.master.master.Shops_info['Shop_items'])
                            #print("self.master.master.master.master.Shops_in['Shop_items'] = ", len(self.master.master.master.master.Shops_info['Shop_items']))
                    #while True:
                        #continue
        
        for i, item in enumerate(self.Shops_info['Shop_items']):
            product = selected_item = item[0]
            self.Shops_info['Shop_items'][i][1] = json.loads(product['more_info'])
            itemstypes = []
            def sub_list(ls, itemtypes):
                if(isinstance(ls, list)):
                    for l in ls:
                        if len(l) > 4 and l[4] != ""and l[4] != " ":
                            if l[1] != '' or l[1] != "":
                                try:
                                    #print("add ing = ", l[1])
                                    itemtypes.append(json.loads(l[1]))
                                except:
                                    #print("error while loading item type = ", l[1])
                                    pass
                        elif len(l) == 2:
                            #print("going deep = ", l[1])
                            sub_list(l[1], itemtypes)
            #print("sanding typrs = ", self.Shops_info['Shop_items'][i][1])
            sub_list(self.Shops_info['Shop_items'][i][1], self.itemtypes)
        
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
        if not self.selected_indexd == -1 and (0 >= self.selected_indexd < len(self.Selected_item_Display_frame.winfo_children())):
            self.remove_item(self.selected_indexd, self.Selected_item_Display_frame.winfo_children()[self.selected_indexd])
    
    def crtl_d_focus(self, event):
        #print("crtl+D pressed " + str(event))
        if "Control" in str(event) or event.state == 14:
            self.open_drower()
            #print("crtl+D pressed " + str(event.state))
        
    def change_focus(self, event):
        self.DFsearch_entry.focus_set()
        
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
        
        buttons = []
        j = 0
        i = -1
        for widget in range(len(self.buttons_frame.winfo_children())):
            j = 0
        a = 0
        b = 0
        for spt, row in enumerate(self.Shop_Payment_Tools):
            #print("creating row btn = " + str(row))
            i += 1
            if b > 3:
                b = 0
                a += 1
            tool_name = row[0]
            # Create a new button
                    
                    
            payment_tool_type = row[1]
            permission_level = {'CASH':2, 'CARD':3, 'CREADIT':4, 'CASHOUT':5, 'CASHIN':6, 'OTHER':7}
            perm_level = permission_level.get(payment_tool_type, 7)
                    
            if Chacke_Security(self, self.user, self.Shops[self.on_Shop], perm_level, f'User Not allowed to Use {payment_tool_type} Payment Tool'):
                new_button = tk.Button(self.buttons_frame, text=tool_name+"\nCtrl + "+str(row[3]), command=lambda r=str(row[3]), d=tool_name, t=payment_tool_type: self.Q_Payment(r, d, t), **self.button_style)
                new_button.bind("<Button-3>", lambda d=str(row[3]), t=payment_tool_type: self.Q_Payment(d, d.widget["text"].split("\n")[0], t))
                self.master.bind("<KeyPress-" + str(row[3]) + ">", lambda r=str(row[3]), d=tool_name, k=new_button, t=payment_tool_type: self.Q_Payment(r, d, t) if "Control" in str(r)else r)
                if payment_tool_type == "CASH":
                    self.master.bind("<F12>", lambda r=str(row[3]), d=tool_name, k=new_button, t=payment_tool_type: self.Q_Payment(r, d, t))
                new_button.grid(row=a, column=b, sticky="nsew", padx=2, pady=5)
                self.Loded_payment_buttons.append([row[1], row[3], new_button])
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
        
        if str(self.chart_index).isdigit() and (items > 0 or ex_item != "" or ex_pay != ""):
            # Define the query to check if the ID exists in the table
            results = fetch_as_dict_list(self.Link, "SELECT * FROM pre_doc_table", ())
            
            if self.chart_index >= 0 and self.chart_index < len(results):
                idid = int(results[self.chart_index]['id'])
                Update_table_database('UPDATE pre_doc_table SET doc_created_date=?, doc_expire_date=?, doc_updated_date=?, AT_SHOP=?, user_id=?, customer_id=?, type=?, ITEM=?, PRICE=?, Disc=?, TAX=?, States=?, exitems_doc_barcode=?, expayment_doc_barcode=? WHERE id=?', (doc_created_date, doc_expire_date, doc_updated_date, AT_SHOP, user_id, customer_id, type, ITEM, float(PRICE), float(Disc), float(TAX), States, ex_item, ex_pay, idid))
            else:
                Update_table_database('INSERT INTO pre_doc_table (doc_created_date, doc_expire_date, doc_updated_date, AT_SHOP, user_id, customer_id, type, ITEM, PRICE, Disc, TAX, States, exitems_doc_barcode, expayment_doc_barcode) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (doc_created_date, doc_expire_date, doc_updated_date, AT_SHOP, user_id, customer_id, type, ITEM, float(PRICE), float(Disc), float(TAX), States, ex_item, ex_pay))

    # this will
    def chack_list(self):
        total_discount = 0
        total_tax = 0
        total_qty = 0
        all_total_price = 0

        for b, selected_items in enumerate(self.Selected_items):
            for a, selected_item in enumerate(selected_items[0]):
                #print("in update item: " + str(selected_item[0]))
                #print("in update item: " + str(selected_item[0]))
                #print("in update item: " + str(selected_item[6]))
                #print("in update item: " + str(selected_item[8]))

                qty = float(selected_item[7])
                price = float(selected_item[10])
                discount = float(selected_item[0]['values']['price']) - float(selected_item[10])
                tax = float(selected_item[10])
                total_price = qty * price  # float(selected_item[11])
                
                # Calculate the expected total price based on quantity, price, discount, and tax
                expected_total_price = qty * (price)  # - tax
                
                # Update the total price in the item if it doesn't match the expected value
                if total_price != expected_total_price:
                    self.Selected_items[b][a][11] = expected_total_price
                
                # Update the price variable
                total_qty += qty
                total_discount += discount
                total_tax += tax
                all_total_price += expected_total_price
        
        return total_qty, total_discount, total_tax, all_total_price

   
    def update_info(self):
        total_qty, total_discount, total_tax, all_total_price = self.chack_list()
        self.total = (all_total_price - self.tax) - self.disc
        self.total_items_label.config(text=str(total_qty))
        self.total_tax_label.config(text=str(self.tax))
        self.total_discount_label.config(text=str(total_discount))
        self.total_tdiscount_label.config(text=str(self.disc))
        self.total_price_label.config(text=str(all_total_price))
        self.total_label.config(text=str((all_total_price - self.tax) - self.disc))
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
                                            
    def Update_selected_item_info(self, data, selected_item_info, new_item_Price_Spinbox, new_item_TPrice_Spinbox, index, a):
        self.Get_next_seletion(data, selected_item_info)
        print("index ", index)
        print("a ", a)
        
        print("self.Selected_items ", self.Selected_items)
        
        print("self.Selected_items["+str(index)+ "]/" +str(len(self.Selected_items[index])-1) +" ", self.Selected_items[index])
        
        print("self.Selected_items["+str(index)+ "]/" +str(len(self.Selected_items[index])-1) +"]["+str(a)+ "]/" +str(len(self.Selected_items[index][0])-1) +"] ", self.Selected_items[index][a])
        # QTY
        if self.chackeqyu:
            self.Selected_items[index][0][a][7] = str(data[4].get())
        
        # price
        if self.chackeprice and self.chakedisc:
           self.Selected_items[index][0][a][10] = str(new_item_Price_Spinbox.get())
        else:
            new_item_Price_Spinbox.set(self.Selected_items[index][0][a][10])
        
        if self.chacketype:
            # shop
            self.Selected_items[index][0][a][12] = str(data[0].get())
            #code
            self.Selected_items[index][0][a][2] = str(data[1].get())
            # color
            self.Selected_items[index][0][a][5] = str(data[2].get())
            # size
            self.Selected_items[index][0][a][6] = str(data[3].get())
        
        if self.chaketotaldic:
            new_item_TPrice_Spinbox.set(str(float(data[4].get())*float(new_item_Price_Spinbox.get())))

        disc = ""
        if float(selected_item_info['values']['price'])-float(new_item_Price_Spinbox.get()) > 0:
            disc = " DISCOUNT " + str(float(selected_item_info['values']['price'])-float(new_item_Price_Spinbox.get()))
        data[6].config(text="Price " + str(selected_item_info['values']['price']) + disc)

        self.update_info()
    
    def remove_ex_items(self, ex_bar_frame, search_label):
        for i, selected_items in enumerate(self.Selected_items):
            for i, selected_item in enumerate(self.Selected_items[0]):
                #print("selected_item[14] ", selected_item[14])
                #print("search_label.cget(text) ", search_label.cget("text"))
                if selected_item[14] == search_label.cget("text"):
                    #print("removed ")
                    
                    self.Selected_items.remove(selected_item)
        
        ex_bar_frame.grid_forget()
        self.Update_Selected_item() # it keep loading old
                
    def Update_Selected_item(self):
        for items in self.Selected_item_Display_frame.winfo_children():
            items.destroy()
        ex_doc_ = []
        for it in self.extrnal_frame.winfo_children():
            it.grid_forget()
        if len(self.Selected_items):
            voidlist_button = tk.Button(self.extrnal_frame, text="Void\nF3", command=self.void_, **self.button_style)
            voidlist_button.grid(row=0, column=0, sticky="nsew", padx=1, pady=1)
        
        #self.midel_frame
        for sis, selected_items in enumerate(self.Selected_items):
            item = [""]
            colors=[]
            new_itemgroup_fram = tk.Frame(self.Selected_item_Display_frame, highlightthickness=2, highlightbackground=self.accent_blue, bg=self.bg_darker)
            new_itemgroup_fram.pack(side="top", fill=tk.X, expand=True)


            new_itemgroup_fram.columnconfigure((0, 1, 2, 3, 4, 5, 6, 7), weight=1, minsize=int(new_itemgroup_fram.winfo_height() *0.1))
            new_itemgroup_fram.rowconfigure((0, 1, 2, 3), weight=1, minsize=int(new_itemgroup_fram.winfo_height() *0.1))
            
            self.group_rate = 0
            self.group_image_frame = tk.Frame(new_itemgroup_fram, bg=self.bg_dark)
            self.group_image_frame.grid(row=0, column=0, rowspan=5, sticky="nsew")

            self.group_image_avatarlabel = tk.Label(self.group_image_frame, bg=self.bg_dark)
            self.group_image_avatarlabel.pack()
            self.group_image_avatarlabel.bind("<Button-1>", lambda _: self.change_Brand_image())
            color = "Def_Color"
            if colors:
                colors = colors[0]
            groupimg = Image.open(MAIN_dir+"\\data\\Icon\\no_Product_Image.jpg").resize((100, 100))
            #print("selected_items ", selected_items)

            imgname = "ActionImage.jpg" if selected_items[1] == 'ACTIONS' else 'ProductImage.jpg'
            code = ""
              
            if os.path.exists(MAIN_dir+"\\data\\Products\\"+ str(selected_items[3]) + "\\"+imgname):
                groupimg = Image.open(MAIN_dir+"\\data\\Products\\"+ str(selected_items[3]) + "\\"+ str(color) + "\\"+imgname).resize((100, 100))
            elif imgname == "ActionImage.jpg":
                groupimg = Image.open(MAIN_dir+"\\data\\Icon\\no_Action_Image.jpg").resize((100, 100))
                
            groupimg = ImageTk.PhotoImage(groupimg)
            self.group_image_avatarlabel.config(image=groupimg)
            self.group_image_avatarlabel.image = groupimg
            
            new_group_name = tk.Label(new_itemgroup_fram, text=str(selected_items[2]), font=("Arial", 8, "bold"), bg=self.bg_darker, fg=self.text_light)
            new_group_name.grid(row=0, column=1, columnspan=2, sticky="nsew")        

            
            closegroup_button = tk.Button(new_itemgroup_fram, text="✕", command= lambda index=sis, frame=new_itemgroup_fram: self.remove_item(index, frame), **self.button_style)
            closegroup_button.grid(row=0, column=7, sticky="nsew", padx=2, pady=2)

            new_item_holder_fram = tk.Frame(new_itemgroup_fram, highlightthickness=2, highlightbackground=self.accent_blue, bg=self.bg_darker)
            new_item_holder_fram.grid(row=1, column=1, columnspan=6, sticky="nsew", padx=2, pady=2)
            
            # list all commen items in the group
            for si, selected_item in enumerate(selected_items[0]):
                #print("selected_item ", selected_item)
                selected_item_info = selected_item[0]
                
                new_item_fram = tk.Frame(new_item_holder_fram, bg=self.bg_darker)
                new_item_fram.pack(side="top", fill=tk.X, expand=True)

                if imgname == "ActionImage.jpg":
                    self.Product_rate = 0
                    product_image_frame = tk.Frame(new_item_fram, bg=self.bg_dark)
                    product_image_frame.grid(row=0, column=0, rowspan=2, sticky="nsew")

                    product_image_avatarlabel = tk.Label(product_image_frame, bg=self.bg_dark)
                    product_image_avatarlabel.pack()
                    product_image_avatarlabel.bind("<Button-1>", lambda _: self.change_Brand_image())
                    color = "Def_Color"
                    if colors:
                        colors = colors[0]
                    img = Image.open(MAIN_dir+"\\data\\Icon\\no_Product_Image.jpg").resize((70, 70))
                    if os.path.exists(MAIN_dir+"\\data\\Products\\"+ str(selected_item_info['values']['barcode']) + "\\ProfileImage.jpg"):
                        img = Image.open(MAIN_dir+"\\data\\Products\\"+ str(selected_item_info['values']['barcode']) + "\\"+ str(color) + "\\ProductImage.jpg").resize((100, 100))

                    img = ImageTk.PhotoImage(img)
                    product_image_avatarlabel.config(image=img)
                    product_image_avatarlabel.image = img

                   
                if not selected_item[14] in ex_doc_:
                    ex_doc_.append(selected_item[14])
                    ch = len(self.extrnal_frame.winfo_children())+1

                    ex_bar_frame = tk.Frame(self.extrnal_frame, bg=self.accent_blue)
                    ex_bar_frame.grid(row=0, column=ch, sticky="nsew", padx=2, pady=2)
                    search_label = tk.Label(ex_bar_frame, text=selected_item[14], bg=self.accent_blue, fg=self.text_light, font=("Arial", 10, "bold"))
                    search_label.grid(row=0, column=0, sticky="nsew", padx=5, pady=3)
                    if not selected_item[14] == "" and str(selected_item[14]) in str(self.Todays_docs):
                        Undo_button = tk.Button(ex_bar_frame, text="Undo", command=lambda: self.remove_ex_items(ex_bar_frame, search_label), **self.button_style)
                        Undo_button.grid(row=0, column=1, sticky="nsew", padx=2, pady=3)
                    update_button = tk.Button(ex_bar_frame, text="✕", command=lambda: self.remove_ex_items(ex_bar_frame, search_label), **self.button_style)
                    update_button.grid(row=0, column=2, sticky="nsew", padx=2, pady=3)
            
                new_item_selecter_fram = tk.Frame(new_item_fram, bg=self.bg_darker)
                new_item_selecter_fram.columnconfigure((0, 1, 2, 3, 4, 5, 6), weight=1, minsize=int(new_item_selecter_fram.winfo_height() *0.1))
                new_item_selecter_fram.rowconfigure((0, 1), weight=1, minsize=int(new_item_selecter_fram.winfo_height() *0.1))
                if imgname == "ActionImage.jpg":
                    new_item_selecter_fram.grid(row=0, column=1, rowspan=2, sticky="nsew")
                else:
                    new_item_selecter_fram.grid(row=0, column=0, rowspan=2, sticky="nsew")
                    
                new_item_QTY_Label = tk.Label(new_item_selecter_fram, text="QTY Max is " + str(selected_item[8]), font=("Arial", 8), bg=self.bg_darker, fg=self.text_light)
                new_item_QTY_Label.grid(row=0, column=1, sticky="nsew")
                
                new_item_QTY_Spinbox = ttk.Spinbox(new_item_selecter_fram, from_=0, to=100, width=10)
                new_item_QTY_Spinbox.grid(row=1, column=1, sticky="nsew")
                new_item_QTY_Spinbox.set(str(selected_item[7]))
                price_ = ""
                price_ = str(selected_item_info['values']['price'])
                disc = ""
                if float(selected_item_info['values']['price'])-float(selected_item[10]) > 0:
                    disc = " DISCOUNT " + str(float(selected_item_info['values']['price'])-float(selected_item[10]))
                new_item_Price_Label = tk.Label(new_item_selecter_fram, text="Price " + price_ + disc, font=("Arial", 8), bg=self.bg_darker, fg=self.text_light)
                new_item_Price_Label.grid(row=0, column=2, sticky="nsew")

                new_item_Price_Spinbox = ttk.Spinbox(new_item_selecter_fram, from_=0, to=100, width=10)
                new_item_Price_Spinbox.grid(row=1, column=2, sticky="nsew")
                new_item_Price_Spinbox.set(str(selected_item[10]))
                
                new_item_name = tk.Label(new_item_selecter_fram, text=str(selected_item[4]), font=("Arial", 12, "bold"), bg=self.bg_darker, fg=self.text_light)
                new_item_name.grid(row=0, column=3, columnspan=3, sticky="nsew")

                new_barcode_Label = tk.Label(new_item_selecter_fram, text=str("barcode"), font=("Arial", 8), bg=self.bg_darker, fg=self.text_light)
                new_barcode_Label.grid(row=0, column=6, columnspan=2, sticky="nsew")
                
                new_type_Label = tk.Label(new_item_selecter_fram, text=str(selected_item[15]), font=("Arial", 8), bg=self.bg_darker, fg=self.text_light)
                new_type_Label.grid(row=0, column=8, columnspan=2, sticky="nsew")
                
                new_exbarcode_Label = tk.Label(new_item_selecter_fram, text=str(selected_item[14]), font=("Arial", 8), bg=self.bg_darker, fg=self.text_light)
                new_exbarcode_Label.grid(row=0, column=8, sticky="nsew")
                
                new_item_Shop_Combobox = ttk.Combobox(new_item_selecter_fram, values=[], width=10)
                new_item_Shop_Combobox.grid(row=1, column=3, padx=5, pady=5, sticky=tk.W)
                new_item_Shop_Combobox.set(str(selected_item[13]))
                
                new_item_Code_Combobox = ttk.Combobox(new_item_selecter_fram, values=[], width=10)
                new_item_Code_Combobox.grid(row=1, column=4, padx=5, pady=5, sticky=tk.W)
                new_item_Code_Combobox.set(str(selected_item[2]))
                
                new_item_Color_Combobox = ttk.Combobox(new_item_selecter_fram, values=[], width=10)
                new_item_Color_Combobox.grid(row=1, column=5, padx=5, pady=5, sticky=tk.W)
                new_item_Color_Combobox.set(str(selected_item[5]))
                
                new_item_Size_Combobox = ttk.Combobox(new_item_selecter_fram, values=[], width=10)
                new_item_Size_Combobox.grid(row=1, column=6, padx=5, pady=5, sticky=tk.W)
                new_item_Size_Combobox.set(str(selected_item[6]))
                
                new_item_TPrice_Spinbox = ttk.Spinbox(new_item_selecter_fram, from_=0, to=100, width=10)
                new_item_TPrice_Spinbox.grid(row=1, column=7, sticky="nsew")
                new_item_TPrice_Spinbox.set(str(float(selected_item[7])*float(selected_item[10])))
                
                del_button = tk.Button(new_item_selecter_fram, text="-", command= lambda index=sis, subindex=si, frame=new_item_fram: self.remove_subitem(index, subindex, frame), **self.button_style)
                del_button.grid(row=1, column=8, sticky="nsew", padx=2, pady=2)
                def list_subitem(index, subindex):
                    new_items = []
                    for e in range(int(self.Selected_items[index][0][subindex][7])- 1 if int(self.Selected_items[index][0][subindex][7]) > 1 else int(self.Selected_items[index][0][subindex][7])):
                        new_item = [n for n in self.Selected_items[index][0][subindex]]
                        new_item[7] = 1
                        self.Selected_items[index][0].append(new_item)
                    self.Update_Selected_item() 
                    
                    
                list_button = tk.Button(new_item_selecter_fram, command= lambda index=sis, subindex=si: list_subitem(index, subindex), **self.button_style)
                list_button.grid(row=1, column=9, sticky="nsew", padx=2, pady=2)
                list_button.config( text="+" if selected_item[7] == 1 or selected_item[7] == '1' else "V")
                    
                # self.master.bind("<Delete>", lambda _: self.remove_item())
                
                
                data = [new_item_Shop_Combobox, new_item_Code_Combobox, new_item_Color_Combobox, new_item_Size_Combobox, new_item_QTY_Spinbox, new_barcode_Label, new_item_Price_Label]

                self.Get_next_seletion(data, selected_item_info)
                

                new_item_Shop_Combobox.bind("<<ComboboxSelected>>", lambda  _, d=data, v=selected_item_info, p=new_item_Price_Spinbox, tp=new_item_TPrice_Spinbox, j=sis, k=si: self.Update_selected_item_info(d, v, p, tp, j, k))
                new_item_Code_Combobox.bind("<<ComboboxSelected>>", lambda  _, d=data, v=selected_item_info, p=new_item_Price_Spinbox, tp=new_item_TPrice_Spinbox, j=sis, k=si: self.Update_selected_item_info(d, v, p, tp, j, k))
                new_item_Color_Combobox.bind("<<ComboboxSelected>>", lambda  _, d=data, v=selected_item_info, p=new_item_Price_Spinbox, tp=new_item_TPrice_Spinbox, j=sis, k=si: self.Update_selected_item_info(d, v, p, tp, j, k))
                new_item_Size_Combobox.bind("<<ComboboxSelected>>", lambda  _, d=data, v=selected_item_info, p=new_item_Price_Spinbox, tp=new_item_TPrice_Spinbox, j=sis, k=si: self.Update_selected_item_info(d, v, p, tp, j, k))

                new_item_Shop_Combobox.bind("<<ComboboxClicked>>", lambda  _, d=data, v=selected_item_info, p=new_item_Price_Spinbox, tp=new_item_TPrice_Spinbox, j=sis, k=si: self.Update_selected_item_info(d, v, p, tp, j, k))
                new_item_Code_Combobox.bind("<<ComboboxClicked>>", lambda  _, d=data, v=selected_item_info, p=new_item_Price_Spinbox, tp=new_item_TPrice_Spinbox, j=sis, k=si: self.Update_selected_item_info(d, v, p, tp, j, k))
                new_item_Color_Combobox.bind("<<ComboboxClicked>>", lambda  _, d=data, v=selected_item_info, p=new_item_Price_Spinbox, tp=new_item_TPrice_Spinbox, j=sis, k=si: self.Update_selected_item_info(d, v, p, tp, j, k))
                new_item_Size_Combobox.bind("<<ComboboxClicked>>", lambda  _, d=data, v=selected_item_info, p=new_item_Price_Spinbox, tp=new_item_TPrice_Spinbox, j=sis, k=si: self.Update_selected_item_info(d, v, p, tp, j, k))

                new_item_Price_Spinbox.bind("<KeyRelease>", lambda  _, d=data, v=selected_item_info, p=new_item_Price_Spinbox, tp=new_item_TPrice_Spinbox, j=sis, k=si: self.Update_selected_item_info(d, v, p, tp, j, k))
                new_item_QTY_Spinbox.bind("<KeyRelease>", lambda  _, d=data, v=selected_item_info, p=new_item_Price_Spinbox, tp=new_item_TPrice_Spinbox, j=sis, k=si: self.Update_selected_item_info(d, v, p, tp, j, k))
                #new_item_TPrice_Spinbox.bind("<<KeyRelease>>", lambda  _, d=data, v=selected_item_info, p=new_item_Price_Spinbox, tp=new_item_TPrice_Spinbox, j=sis, k=si: self.Update_selected_item_info(d, v, p, tp, j, k))

                new_item_Price_Spinbox.config(command= lambda d=data, v=selected_item_info, p=new_item_Price_Spinbox, tp=new_item_TPrice_Spinbox, j=sis, k=si: self.Update_selected_item_info(d, v, p, tp, j, k))
                new_item_QTY_Spinbox.config(command= lambda  d=data, v=selected_item_info, p=new_item_Price_Spinbox, tp=new_item_TPrice_Spinbox, j=sis, k=si: self.Update_selected_item_info(d, v, p, tp, j, k))
                #new_item_TPrice_Spinbox.bind(command= lambda d=data, v=selected_item_info, p=new_item_Price_Spinbox, tp=new_item_TPrice_Spinbox, j=sis, k=si: self.Update_selected_item_info(d, v, p, tp, j, k))

        self.update_info()
        
    def update_list_items(self):
        # Define the SQL query to fetch the product information based on doc_created_date
        # Execute the query and fetch the results
        results = fetch_as_dict_list(self.Link, "SELECT * FROM pre_doc_table", ())
        
        # Clear the existing items in the list
        # Loop through the results and add each product to the list
        
        
        self.barcode_label.config(text=str(self.chart_index))
        
        if self.chart_index > -1 and self.chart_index < len(results):
            result = results[self.chart_index]
            self.pid_peyment = []
            self.ex_pid_peyment = []
            self.items = []
            self.ex_items = []
            self.Selected_items = []
            
            # Extract the item information from the database record
            #self.chart_index = result['id']
            doc_created_date = result['doc_created_date']
            doc_expire_date = result['doc_expire_date']
            doc_updated_date = result['doc_updated_date']
            AT_SHOP = result['AT_SHOP']
            user_id = result['user_id']
            customer_id = result['customer_id']
            type = result['type']
            ITEM = result['ITEM']
            PRICE = result['PRICE']
            Disc = result['Disc']
            TAX = result['TAX']
            States = result['States']
            ex_item = result['exitems_doc_barcode']
            ex_pay = result['expayment_doc_barcode']
            
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
        results = fetch_as_dict_list(self.Link, "SELECT id FROM pre_doc_table", ())

        if len(results) > 1 and hasattr(self, 'prevlist_button'):
            self.prevlist_button.config(state=tk.NORMAL)
            #self.prevlist_button.config(state=tk.DISABLED)
        
        if results and self.chart_index == None: 
            self.chart_index = len(results)-1
        
        else:
            if towhere == "Next":
                a = Chacke_Security(self, self.user, self.Shops[self.on_Shop], 4)
                if len(results) == 0 and not ':' in str(self.chart_index):
                    self.chart_index = 0
                elif a:
                    #print("going to next ")
                    if str(self.chart_index).isdigit() and self.chart_index < 0 or not str(self.chart_index).isdigit() and ':' in str(self.chart_index): # chack if it is document id
                        #print("going to doc ", len(self.Todays_docs))
                        
                        #print("doc")
                        for index, value in enumerate(self.Todays_docs):
                            if value['doc_barcode'] == str(self.chart_index):
                                self.chart_index = len(results)-1 if len(results) > 0 else 0
                                break
                                
                            if value['doc_barcode'] == self.chart_index:
                                if index+1 >= 0 and index+1 <= len(self.Todays_docs)-1:
                                    self.chart_index = self.Todays_docs[index+1]['doc_barcode']
                                else:
                                    self.chart_index = len(results)-1 if len(results) > 0 else self.Todays_docs[len(self.Todays_docs)-1]['doc_barcode'] if len(self.Todays_docs) > 0  else 0
                                break
                        if not str(self.chart_index).isdigit() and ':' in str(self.chart_index):
                            rows = fetch_as_dict_list(self.Link, "SELECT * FROM doc_table WHERE doc_barcode=?", (self.chart_index,))
                            if rows:
                                rows = rows[0]
                                selected_item_info = {'values': rows, 'type': 'DOCUMENT'}
                                self.barcode_label.config(text=str(self.chart_index))
                                self.get_ex_doc_items(selected_item_info)
                                self.get_ex_doc_payments(selected_item_info)
                        if str(self.chart_index).isdigit() or len(self.Todays_docs) > 0 and self.chart_index == self.Todays_docs[len(self.Todays_docs)-1]['doc_barcode']:
                            if  len(results) > 0:
                                self.nextlist_button.config(state=tk.NORMAL)
                                self.nextlist_button.config(text=">>>\nF5")
                            else:
                                self.nextlist_button.config(state=tk.NORMAL)
                                self.nextlist_button.config(text="New\nF7")
                        
                    
                    elif self.chart_index+1 == len(results):
                        self.chart_index = len(results)
                        #print("new chart")
                        self.nextlist_button.config(text="New\nF7")
                        self.new_chart(1)
                        return
                    elif self.chart_index+1 <= len(results)-1:
                        #print("cahrt")
                        self.nextlist_button.config(state=tk.NORMAL)
                        self.chart_index += 1
                        if self.chart_index == len(results)-1:
                            self.nextlist_button.config(text="New\nF7")
                        else:
                            self.nextlist_button.config(text=">>>\nF5")
            else:
                a = Chacke_Security(self, self.user, self.Shops[self.on_Shop], 5)
                if a:
                    #print("going to prev")
                    if str(self.chart_index).isdigit() and self.chart_index-1 < 0 or not str(self.chart_index).isdigit() and ':' in str(self.chart_index): # chack if it is document id
                        #print("going to doc ", len(self.Todays_docs))
                        #print("doc")
                        self.nextlist_button.config(state=tk.NORMAL)
                        self.nextlist_button.config(text=">>>\nF5")
                        if self.chart_index == 0:
                            self.chart_index =  self.Todays_docs[len(self.Todays_docs)-1]['doc_barcode']
                        else:
                            for index, value in enumerate(self.Todays_docs):
                                if value['doc_barcode'] == self.chart_index:
                                    if index-1 >= 0 and index-1 <= len(self.Todays_docs)-1:
                                        self.chart_index = self.Todays_docs[index-1]['doc_barcode']
                                    else:
                                        self.chart_index  = len(results)-1 if len(results) > 0 else self.Todays_docs[len(self.Todays_docs)-1]['doc_barcode'] if len(self.Todays_docs) > 0  else 0
                                        if self.chart_index == len(results)-1:
                                            self.nextlist_button.config(text="New\nF7")
                                    break
                        if not str(self.chart_index).isdigit() and ':' in str(self.chart_index):
                            rows = fetch_as_dict_list(self.Link, "SELECT * FROM doc_table WHERE doc_barcode=?", (self.chart_index,))
                            if rows:
                                rows = rows[0]
                                selected_item_info = {'values': rows, 'type': 'DOCUMENT'}
                                self.barcode_label.config(text=str(self.chart_index))
                                self.get_ex_doc_items(selected_item_info)
                                self.get_ex_doc_payments(selected_item_info)
                                
                    else:
                        self.nextlist_button.config(state=tk.NORMAL)
                        self.chart_index -= 1
                        #print("prev doc ", self.chart_index)
                        if self.chart_index == len(results)-1:
                            self.nextlist_button.config(text="New\nF7")
                        else:
                            self.nextlist_button.config(text=">>>\nF5")
        self.barcode_label.config(text=str(self.chart_index))
        
        if str(self.chart_index).isdigit():            
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
        self.custemr = "" # for holding user or costumer name
        self.app = None # for holding user or costumer name
        self.Add_custemur_label.config(text="+ Custumer")
        self.disc = 0
        
        self.price = 0
        self.pid = 0
        self.creadit = 0
        self.tax = 0
        self.qty = 0
        self.disc = 0
        self.total = 0
        
    def call_chartForm(self):
        v = ShowchartForm(self)
        if v.value != self.chart_index:
            self.chart_index = v.value
            self.clear_items()
           #print("selected chart : "+ str(v.value))
            self.update_list_items()
            
    def new_chart(self, on):
        if len(self.Selected_items) > 0:
            if Chacke_Security(self, self.user, self.Shops[self.on_Shop], 10, f'User Not allowed to Use Multy Order'):
                res = fetch_as_dict_list(f"SELECT id FROM pre_doc_table", ())
                if on == 1:
                    self.chart_index = len(res)
                    #print("new chart")
                    self.nextlist_button.config(text="New\nF7")
                self.clear_items()
                self.update_list_items()
                
    def remove_item(self, index, selected_frame):
        if Chacke_Security(self, self.user, self.Shops[self.on_Shop], 13, f'User Not allowed to Delete Items'):
            items = ""
            for b, selected_item in enumerate(self.Selected_items[index][0]):
                #tax = float(selected_item[10])
                #total_price = qty * price  # float(selected_item[11])
                items += "QTY " + str(selected_item[7]) + " price " + str(selected_item[10]) +" discount " +  str(float(selected_item[0]['values']['price']) - float(selected_item[10])) + "\n"
            answer = tk.messagebox.askquestion("Question", str(items) + "\nDo you whant to Delete those items?")
            if answer == 'yes':
                self.selected_indexd = -1
                self.Selected_items.remove(self.Selected_items[index])
                selected_frame.destroy()
                self.Update_Selected_item()
                
    def remove_subitem(self, index, subindex, selected_frame):
        if Chacke_Security(self, self.user, self.Shops[self.on_Shop], 13, f'User Not allowed to Delete Items'):
            items = "QTY " + str(self.Selected_items[index][0][subindex][7]) + " price " + str(self.Selected_items[index][0][subindex][10]) +" discount " +  str(float(self.Selected_items[index][0][subindex][0]['values']['price']) - float(self.Selected_items[index][0][subindex][10])) + "\n"
            answer = tk.messagebox.askquestion("Question", str(items) + "\nDo you whant to Delete items?")
            if answer == 'yes':
                self.selected_indexd = -1
                if len(self.Selected_items[index][0]) == 1:
                    self.Selected_items.remove(self.Selected_items[index])
                else:
                    self.Selected_items[index][0].remove(self.Selected_items[index][0][subindex])
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
        results = fetch_as_dict_list(self.Link, "SELECT * FROM pre_doc_table", ())
        if self.chart_index >= 0 and self.chart_index < len(results):
            idid = int(results[self.chart_index]['id'])
            # delete this list on db
            Update_table_database("DELETE FROM pre_doc_table WHERE id=?", (idid,))
        if self.chart_index == 0:
            # self.update_info() will be called in next_prev_chart 
            self.next_prev_chart("Next")
        else:
            self.next_prev_chart("Prev")
            
    # this will add item to the list
    def add_item(self, item_info):
        #print("item_info = " + str(item_info))
        if (item_info['type'] == "UnKNOWN"):
            items = item_info['values']
            # selected_data = Id, code, color, size, qty, left, barcode, extr
            
            # in chake_action we will chack if item is in the list or not
            # id, code, barcode, name, color, size, qty, price, disc, includetax, total_price, shop, extr

            shopname = "Unknown Shop"
            code = "Unknown Code"
            color = "Unknown Color"
            size = "Unknown Size"
            
            # finde similar item in the list that has same price and cost
            for item in self.Shops_info['Shop_items']:
                # if item price and cost are in range of the unknown item price and cost +- 50% we will consider it as similar item
                if isinstance(item, list):
                    item = item[0]
                #print('item ', item)
                #print("item price ", item['price'], "item cost ", item['cost'], "uitemprice ", uitemprice, "uitemcost ", uitemcost)
                #print("item price range ", float(uitemprice) - float(uitemprice)/2, " - ", float(uitemprice) + float(uitemprice)/2 )
                uitemprice = float(items['price'])
                uitemcost = float(items['cost'])
                if ((float(item['cost']) > uitemprice/3 and float(item['cost']) <= (float(uitemcost) + float(uitemcost)/2)) and float(item['cost']) < uitemprice or  float(item['cost']) >= uitemprice/3 and(float(item['cost']) <= float(uitemprice))  ) and ((float(item['price']) >= float(uitemprice)) and (float(item['price']) <= float(uitemprice)) ):
                    # change this item name to unknown item and add it to the list
                    item_type = json.loads(item['more_info']) if item['more_info'] else {}
                    if not item_type == {}:
                        # get types shop name, code, color, size, extra data if item_type has it like [shops [codes [[colors ...[[sizes[extra data[],...],...],...],...],...],...],...]
                        def get_type_info(item_type, path):
                            #print("item_type ", item_type)
                            if len(item_type) == 2 and isinstance(item_type[0], str) and isinstance(item_type[1], list):
                                new_path = get_type_info(item_type[1], path + [item_type[0]])
                                if new_path:
                                    return new_path
                            elif isinstance(item_type[0], list):
                                new_path = get_type_info(item_type[0], path)
                                if new_path:
                                    return new_path
                            elif len(item_type) > 4:
                                if float(item_type[4]) > 0:
                                    #print("path ", path)
                                    path = path + [float(item_type[4])]
                                    return path
                            return None
                        path = get_type_info(item_type, [])
                        if path:
                            #print("path2 ", path)
                            shopname = path[0]
                            code = path[1]
                            color = path[2]
                            size = path[3]
                            qtylaft = path[4] if len(path) > 4 else 1
                            item_info = {'type': "ITEM", 'values': item, 'extra_data': [], 'item_list': []}
                            value = [str(item['id']), item['code'], item['barcode'], items['name'], color, size, 1, qtylaft, items['price']-self.disc, item['include_tax'], items['price'], shopname, ""]
                            #                                                                                                            value[7] Qty left
                            self.Selected_items.append([[[item_info, str(value[0]), value[1], value[2], value[3], value[4], value[5], value[6], value[7], "", value[8], value[9], value[10], value[11], value[12], ""]], "ITEM", 'Unknown Item', item['barcode']])        
                            self.Update_Selected_item()
                            return
        
            # if not similar item found we will add the unknown item to the list with unknown shop and code and color and size
            # msg box to ask if user want to add this item to the shop items list with this info
            tk.messagebox.askquestion("Warning", "This item is not in the shop items list, do you want to add it to the shop items list with this info? \n\n Shop Name: " + shopname + "\n Code: " + code + "\n Color: " + color + "\n Size: " + size)
            

        if (item_info['type'] == "ITEM"):
            for data in item_info['extra_data']:
                shop = self.Shops_Names
                if self.Selected_Shop != "":
                    shop = [self.Selected_Shop]
                items, doc, selected_type, barcode, shop_name, code, color, size, qty = \
                     item_info['values'], None, item_info['type'], data[6], data[0], data[1], data[2], data[3], data[4]
                
                # chacke if qty lefte is less than 0 or not
                # change this item name to unknown item and add it to the list
                item_type = json.loads(items['more_info']) if items['more_info'] else {}
                if not item_type == {}:
                    # get types shop name, code, color, size, extra data if item_type has it like [shops [codes [[colors ...[[sizes[extra data[],...],...],...],...],...],...],...]
                    def get_type_info(item_type, path):
                        #print("item_type ", item_type)
                        if len(item_type) == 2 and isinstance(item_type[0], str) and isinstance(item_type[1], list):
                            new_path = get_type_info(item_type[1], path + [item_type[0]])
                            if new_path:
                                return new_path
                        elif isinstance(item_type[0], list):
                            new_path = get_type_info(item_type[0], path)
                            if new_path:
                                return new_path
                        elif len(item_type) > 4:
                            if float(item_type[4]) > 0:
                                if float(item_type[4])-float(qty) >= 0:
                                    path = path + [qty]
                                    #print("path ", path)
                                    return path
                                else:
                                    path = path + [float(item_type[4])]
                                    #print("path ", path)
                                    return path
                        return None
                    path = get_type_info(item_type, [])
                    if path:
                        #print("path2 ", path)
                        #print("shop_name ", shop_name, "code ", code, "color ", color, "size ", size)
                        if not (path[0] == shop_name and path[1] == code and path[2] == color and path[3] == size):
                            ask = tk.messagebox.askquestion("Warning", "Selected Items Size, Color or Code Out of Stockd or will be out of stock, do you want to add it to the shop items list with this info? \n\n Shop Name: " + path[0] + "\n Code: " + path[1] + "\n Color: " + path[2] + "\n Size: " + path[3])
                            if ask == 'yes':
                                shopname = path[0]
                                code = path[1]
                                color = path[2]
                                size = path[3]
                                nqty = float(qty)-path[4]
                                qty = path[4]
                                item_info = {'type': "ITEM", 'values': items, 'extra_data': [], 'item_list': []}
                                value = [str(items['id']), items['code'], items['barcode'], items['name'], color, size, qty, items['price'], items['price']-self.disc, items['include_tax'], items['price'], shopname, ""]
                                self.Selected_items.append([[[item_info, str(value[0]), value[1], value[2], value[3], value[4], value[5], value[6], value[7], "", value[8], value[9], value[10], value[11], value[12], ""]], "ITEM", items['name'], items['barcode']])           
                        else:
                            qty = float(qty)-float(path[4])
                            if data[7] != []:
                                for t, typ in enumerate(data[7]):                            
                                    QTY = int(typ[1])
                                    PRICE = int(typ[2])
                                    value = [str(items['id']), code, barcode, items['name'], color, size, float(QTY), PRICE, self.disc, items['include_tax'], float(QTY)*float(PRICE), shop_name, ""]
                                    self.Selected_items.append([[[item_info, str(value[0]), value[1], value[2], value[3], value[4], value[5], value[6], value[7], data[5], PRICE, value[9], value[10], value[11], value[12], typ[0]]], "ITEM", items['name'], barcode])
                            else:
                                value = [str(items['id']), code, barcode, items['name'], color, size, float(path[4]), items['price'], self.disc, items['include_tax'], float(qty)*float(items['price']), shop_name, '']
                                self.Selected_items.append([[[item_info, str(value[0]), value[1], value[2], value[3], value[4], value[5], value[6], value[7], data[5], item_info['values']['price'], value[9], value[10], value[11], value[12], ""]], "ITEM", items['name'], barcode])                        
                            
                            if qty <= 0:
                                continue

                # finde similar item in the list that has same price and cost
                for item in self.Shops_info['Shop_items']:
                    # if item price and cost are in range of the unknown item price and cost +- 50% we will consider it as similar item
                    if isinstance(item, list):
                        item = item[0]
                    #print('item ', item)
                    #print("item price ", item['price'], "item cost ", item['cost'], "uitemprice ", uitemprice, "uitemcost ", uitemcost)
                    #print("item price range ", float(uitemprice) - float(uitemprice)/2, " - ", float(uitemprice) + float(uitemprice)/2 )
                    uitemprice = float(items['price'])
                    uitemcost = float(items['cost'])
                    if (float(item['price']) == float(uitemprice) and float(item['cost']) >= float(uitemcost) - float(uitemcost)/2 and float(item['cost']) <= float(uitemcost) + float(uitemcost)/2):
                        # change this item name to unknown item and add it to the list
                        item_type = json.loads(item['more_info']) if item['more_info'] else {}
                        if not item_type == {}:
                            # get types shop name, code, color, size, extra data if item_type has it like [shops [codes [[colors ...[[sizes[extra data[],...],...],...],...],...],...],...]
                            def get_type_info(item_type, path):
                                #print("item_type ", item_type)
                                if len(item_type) == 2 and isinstance(item_type[0], str) and isinstance(item_type[1], list):
                                    new_path = get_type_info(item_type[1], path + [item_type[0]])
                                    if new_path:
                                        return new_path
                                elif isinstance(item_type[0], list):
                                    new_path = get_type_info(item_type[0], path)
                                    if new_path:
                                        return new_path
                                elif len(item_type) > 4:
                                    if float(item_type[4]) > 0 and float(item_type[4]) - float(qty) >= 0:
                                        path = path + [qty]
                                        #print("path ", path)
                                        return path
                                return None
                            path = get_type_info(item_type, [])
                            if path:
                                ask = tk.messagebox.askquestion("Warning", "This item is out of stock, but we found similar item in the shop items list with this info: \n\n Shop Name: " + path[0] + "\n Code: " + path[1] + "\n Color: " + path[2] + "\n Size: " + path[3] + "\n\n Do you want to add this similar item to the list instead?")
                                if ask == 'yes':
                                    shopname = path[0]
                                    code = path[1]
                                    color = path[2]
                                    size = path[3]
                                    item_info = {'type': "ITEM", 'values': item, 'extra_data': [], 'item_list': []}
                                    value = [str(item['id']), item['code'], item['barcode'], 'Unknown Item', color, size, path[4], items['price'], items['price']-self.disc, item['include_tax'], items['price'], shopname, ""]
                                    self.Selected_items.append([[[item_info, str(value[0]), value[1], value[2], value[3], value[4], value[5], value[6], value[7], "", value[8], value[9], value[10], value[11], value[12], ""]], "ITEM", items['name'], barcode])        
                                    break
                                else:
                                    if data[7] != []:
                                        for t, typ in enumerate(data[7]):                            
                                            QTY = int(typ[1])
                                            PRICE = int(typ[2])
                                            value = [str(items['id']), code, barcode, items['name'], color, size, float(QTY), PRICE, self.disc, items['include_tax'], float(QTY)*float(PRICE), shop_name, ""]
                                            self.Selected_items.append([[[item_info, str(value[0]), value[1], value[2], value[3], value[4], value[5], value[6], value[7], data[5], PRICE, value[9], value[10], value[11], value[12], typ[0]]], "ITEM", items['name'], barcode])
                                    else:
                                        value = [str(items['id']), code, barcode, items['name'], color, size, float(path[4]), items['price'], self.disc, items['include_tax'], float(qty)*float(items['price']), shop_name, '']
                                        self.Selected_items.append([[[item_info, str(value[0]), value[1], value[2], value[3], value[4], value[5], value[6], value[7], data[5], item_info['values']['price'], value[9], value[10], value[11], value[12], ""]], "ITEM", items['name'], barcode])                        
                                    break

                self.disc = 0
        if(item_info['type'] == 'ACTIONS'):
            print("chacking for  ", len(item_info['values']))
            self.Action_code = item_info['values'][0]
            Action_label  = item_info['values'][1]
            From_Date = item_info['values'][3]
            TO_Date = item_info['values'][4]
            
            ifSelected_items = item_info['values'][5]
            # TODO : Do if by profit or totale price
            '''ifProduct_Make_price = actions[5][2]
            ifProduct_Make_Total_price = actions[5][3]
            ifProduct_Make_Discount = actions[5][4]
            ifProduct_Make_Total_Disc = actions[5][5]'''
            
            doSelected_items = item_info['values'][6]
            
            '''doProduct_Make_price = actions[6][2]
            doProduct_Make_Total_price = actions[6][3]'''
            
            print("chacking for ifSelected_items ", ifSelected_items)
            print("chacking for doSelected_items ", doSelected_items)
            
            if not ifSelected_items[1] or len(ifSelected_items[1]) == 0 or not ActionsForm.chack_for_Action(self.Selected_items, ifSelected_items[1]) == None:
                print("Done chalckeing for action ")
                #print("self.Selected_items0 ", self.Selected_items)
                self.Selected_items.append([doSelected_items[1], "ACTIONS", item_info['values'][1], item_info['values'][0]])
                #print("self.Selected_items1 ", self.Selected_items)
                
            
            

                
        if (item_info['type'] == "DOCUMENT"):
            self.Selected_items = []
            items = json.loads(item_info['values']['item'])
            for item in items:
                it = fetch_as_dict_list(self.Link, "SELECT * FROM product WHERE id=?", (item[0],))[0]
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
                    self.Selected_items.append([[[doc_item_info, str(item[0]), item[1], item[2], item[3], item[5], item[6], item[7], item[8], qtyleft, item[8], item[10], 0, item[4], item_info['values']['doc_barcode'], typ]], "ITEM", item[1], item[2]]) 
                else:
                    pass
        
        self.Update_Selected_item()
        
    def add_payment(self, items, doc, selected_type, barcode):
        if not barcode in self.ex_pid_peyment:
            self.ex_pid_peyment.append(barcode)
        if (selected_type == "DOCUMENT"):
            #print("add_payment self.pid_peyment = " + str(self.pid_peyment))
            for item in items:
                if len(item) == 6:   
                    item.append(1)
                if len(item) == 7:
                    item.append(barcode)
                if len(item) >= 7 and (item[7] == "" or item[7] == None):
                    item[7] = barcode
                #print("doc barcode = "+ str(barcode))
                #print("doc payment = "+ str(item))
                #print("doc payment[0] = "+ str(item[0]))
                # this is for old vistion that use the first index ad number not for type
                # in new version we need the payment type so we useing index 0
                payment_tool_type = item[0]
                if item[0].isdigit():
                    # if it is old v we will get it by searching
                    rows = fetch_as_dict_list(self.Link, "SELECT * FROM tools", ())
                    for spt, row in enumerate(self.Shop_Payment_Tools):
                        if row[0] == item[1]:
                            payment_tool_type = row[1]
                item[0] = payment_tool_type
                if payment_tool_type == "CREADIT":
                    self.creadit += float(item[2])
                self.pid_peyment.append(item)
           

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
    def Q_Payment(self, event, text, payment_type):
        #print("Q_Payment + " + str(text) + " payment_type " + str(payment_type))
        p = 0
        for pid in self.pid_peyment:
            p += float(pid[2])

        t = self.total-p
        if t <= 0 and not self.creadit == 0:
            #print("self.creadit "+str(self.creadit))
            t = self.creadit
        i = GetvalueForm(self, str(t), ["Make " + str(text) + " Peyment"])
        if i and i.value and len(i.value) and i.value[0] > 0:
            self.pid_peyment.append([payment_type, str(text), str(i.value[0]), "", "", "", "", ""])
            p += float(i.value[0])
            if t <= 0 and self.creadit == 0:
                self.creadit -= float(i.value[0])
        if p > 0 and p >= self.total:
            #print("call_payment self.pid_peyment = " + str(self.pid_peyment))
            
            todaydate = str(datetime.datetime.now().strftime('%Y')) + "-"+str(datetime.datetime.now().strftime('%m')) + "-"+str(datetime.datetime.now().strftime('%d'))
            givendate = self.date_year_Spinbox.get() + "-"+self.date_month_Spinbox.get() + "-"+self.date_day_Spinbox.get()

            if todaydate != givendate:
                answer = tk.messagebox.askquestion("Question", "Given date "+givendate+" and today date "+todaydate+" Is Not Same Wolde You Like To Fixe It?")
                if answer == 'yes':
                    self.date_day_Spinbox.set(str(datetime.datetime.now().strftime('%d')))
                    self.date_month_Spinbox.set(str(datetime.datetime.now().strftime('%m')))
                    self.date_year_Spinbox.set(str(datetime.datetime.now().strftime('%Y')))
            
            slip_doc_code = DocEditForm.process_payment(self,givendate, self.user, self.custemr, self.Shops, self.on_Shop, self.Shops_info, self.Selected_items, self.pid_peyment)

            # call void         
            self.void_items()
            self.manage_form.doc_form.load_documents(slip_doc_code)
            


    # splitpayment btn
    def call_splitpayment(self):
        if len(self.Selected_items) > 0 or len(self.pid_peyment) > 0:
            PaymentForm(self, self.user, self.Shops)
        else:
            #print("item ", len(self.Selected_items))
            #print("payment ", len(self.pid_peyment))
            pass
    
    

    def Add_Custumer(self):
        if Chacke_Security(self, self.user, self.Shops[self.on_Shop], 21, f'User Not allowed to Search for Custumers'):
            self.app = UserManagementApp(self, "", self.user, self.Shops, self.on_Shop)
            if self.app.user_details:
                #print("selected user == ", self.app.user_details)
                self.custemr = self.app.user_details['User_id']
                self.Add_custemur_label.config(text=self.app.user_details['User_name'])
            else:
                #print("user not selected")
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
        self.load_setting()

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
            #print("Error creating backup:", str(e))
            pass
        finally:
            # Close the database connection
            conn.close()
            
    def Call_Uploading_Form(self):
        if Chacke_Security(self, self.user, self.Shops[self.on_Shop], 25, f'User Not allowed to Upload Documents'):
            UploadingForm(self, self.user, self.Shops)

    
