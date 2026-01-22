import tkinter as tk
from tkinter import ttk
import sqlite3, os

data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data'))
db_path = os.path.join(data_dir, 'my_database.db')
conn = sqlite3.connect(db_path)
cursor = conn.cursor

from D.Upload_ import UploadingForm

# TODO: user can change name, or password in this form
# TODO: user can add sub user depanding on it usertype
class Veaw_Notifications(tk.Tk):
    def __init__(self, master, User, Shops):
        self.master = master
        self.Shops = Shops
        self.user = User
        # create a Toplevel window for the payment form
        self.getvalue_form = tk.Toplevel(self.master)
        self.getvalue_form.title("Notification ")

        # calculate the center coordinates of the screen
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        x = (screen_width / 2) - (300 / 2)  # 500 is the width of the Payment Form window
        y = (screen_height / 2) - (300 / 2)  # 500 is the height of the Payment Form window
        
        self._label0 = tk.Label(self.getvalue_form, text="Notification", font=("Arial", 14))
        self._label0.grid(row=0, column=0, columnspan=2, padx=10, pady=10)
        
        self.Shops_Names = [shop['Shop_name'] for shop in self.Shops]                            
        self.User_Shopes_Combobox = ttk.Combobox(self.getvalue_form, values=self.Shops_Names, width=10)
        self.User_Shopes_Combobox.grid(row=1, column=0, columnspan=2, sticky="nsew")
        #self.User_Shopes_Combobox.bind("<Button-1>",lambda _: self.Add_Custumer())
        self.at_shop_name = ""
        if(len(self.Shops_Names) == 1):
            self.At_Shop_id = self.Shops[0]['Shop_id']
            at_shop_name = self.Shops[0]['Shop_name']
            self.on_Shop = 0
        else:
            #self.At_Shop_id = -1
            #self.on_Shop = -1    
            pass # TODO: if user works more than one shop make user choose in which shop is it right now
                

        self.midel_frame = tk.Frame(self.getvalue_form)
        self.midel_frame.grid(row=2, column=0, columnspan=2, padx=10, pady=10)
        
        self.Frame_contaner_frame = tk.Frame(self.midel_frame)
        self.Frame_contaner_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.List_Frame_contaner_frame = tk.Frame(self.Frame_contaner_frame)
        self.List_Frame_contaner_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.List_Frame = tk.Frame(self.List_Frame_contaner_frame)
        self.List_Frame.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        
        self.item_List_canvas = tk.Canvas(self.List_Frame)
        self.item_List_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        
        self.item_List_yscrollbar = tk.Scrollbar(self.List_Frame, orient='vertical', command=self.item_List_canvas.yview)
        self.item_List_yscrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.item_List_xscrollbar = tk.Scrollbar(self.List_Frame_contaner_frame, orient='horizontal', command=self.item_List_canvas.xview)
        self.item_List_xscrollbar.pack(side=tk.TOP, fill=tk.X)
        
        self.item_List_canvas.configure(xscrollcommand=self.item_List_xscrollbar.set, yscrollcommand=self.item_List_yscrollbar.set)
        #self.New_item_contener_canvas.bind('<Configure>', lambda e: self.New_item_contener_canvas.configure(scrollregion=self.New_item_contener_canvas.bbox("all")))

        self.Selected_item_Display_frame = tk.Frame(self.item_List_canvas)
        self.item_List_canvas.create_window((0, 0), window=self.Selected_item_Display_frame, anchor=tk.NW)
        self.Selected_item_Display_frame.bind('<Configure>', lambda e: self.item_List_canvas.configure(scrollregion=self.item_List_canvas.bbox("all")))

        
        self.logout_button = tk.Button(self.getvalue_form, text="Done", bg="red", fg="white", font=("Arial", 12))
        self.logout_button.grid(row=4, column=0)
        self.logout_button = tk.Button(self.getvalue_form, text="Clear", bg="red", fg="white", font=("Arial", 12))
        self.logout_button.grid(row=4, column=1)

        self.Notifications_list = []
        # Loade Notifications
        self.Update_Notifications_list()
        # Draw_Notifications_list
        self.Draw_Notifications_list()

        
        # show the Payment Form window
        self.getvalue_form.transient(self.master)
        self.getvalue_form.grab_set()
        self.master.wait_window(self.getvalue_form)

    def Update_Notifications_list(self):
        # chacke all shops if there are connected before
        # this will chacke if shop is created and if not uploded its data to cloude
        for shop in self.Shops:
            if shop['Shop_name'] == self.User_Shopes_Combobox.get() or self.User_Shopes_Combobox.get() == "None" or self.User_Shopes_Combobox.get() == "":
                print("shope", shop)
                print("shop['Shop_online_id']", shop['Shop_online_id'])
                self.Notifications_list.append(["Uplode", "Worrning "+ shop['Shop_name']+" data is not uploded"])

    def Clear_N(self):
        for items in self.Selected_item_Display_frame.winfo_children():
            items.destroy()
            
    def Draw_Notifications_list(self):
        self.Clear_N()
        self.master.Veaw_Notifications_label.config(text="Notifications " + str(len(self.Notifications_list)))
        for i, Notification_list in enumerate(self.Notifications_list):
            print("selected_item ", Notification_list)
            ex_bar_frame = tk.Frame(self.Selected_item_Display_frame, highlightthickness=2, highlightbackground="black")
            ex_bar_frame.grid(row=i, column=0, sticky="nsew")
            search_label = tk.Label(ex_bar_frame, text=Notification_list[1], font=("Arial", 12))
            search_label.grid(row=0, column=0, sticky="nsew")
            if Notification_list[0] == "Uplode":
                update_button = tk.Button(ex_bar_frame, text="update", font=("Arial", 12), command=lambda: UploadingForm(self.master, self.user, self.Shops))
                update_button.grid(row=0, column=2, sticky="nsew")
