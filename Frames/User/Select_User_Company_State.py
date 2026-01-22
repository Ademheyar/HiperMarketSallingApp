import tkinter as tk
from tkinter import ttk
import sqlite3
import json

# Connect to the database or create it if it does not exist

import os
import os, sys
current_dir = os.path.abspath(os.path.dirname(__file__))
MAIN_dir = os.path.join(os.path.join(current_dir, '..'), '..')
sys.path.append(MAIN_dir)

data_dir = os.path.join(MAIN_dir, 'data')
db_path = os.path.join(data_dir, 'my_database.db')
conn = sqlite3.connect(db_path)
cur = conn.cursor()

conn.commit()

from C.List import *
# from D.docediterform import DocEditForm
from D.printer import PrinterForm
from C.slipe import load_slip
# from M.Display import DisplayFrame

from C.Sql3 import *
from C.API.Get import *
from C.API.API import *
from C.Database.Set import *

from Frames.Company.View_Company import Company_Info_Frame
from Frames.Company.Company_Forget_Info import Company_Forget_Info_Frame
from Frames.Company.Request_Company import Request_Company_Frame


class Select_User_Company_State_Frame(tk.Frame):
    def __init__(self, parent, Canceal_callback, User_data):
        tk.Frame.__init__(self, parent, bg="#0d47a1")  # Set background to deep blue
        self.Canceal_callback = Canceal_callback
        self.User_data = User_data
        self.Shops = []
        
        # print("self.User_data : ", self.User_data)

        self.found_shops = []
        self.found_Shops_result = []
        
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        
        # create the container frame to hold the other frames
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        # create the first frame and add it to the container
        self.frames = {}

        self.display_frame = None

        # create the second frame and add it to the container
        select_User_Company_State_Frame = tk.Frame(self, bg="#0d47a1", height=screen_height, width=screen_width)
        
        self.details_frame = tk.Frame(select_User_Company_State_Frame, bg="#1565c0", height=screen_height, width=screen_width)
        self.details_frame.place(relx=0.5, rely=0.5, anchor="center")

        self.frames["Select_User_Company_State_Frame"] = select_User_Company_State_Frame
        
        def callbackhomefunction():
            self.show_frame("Select_User_Company_State_Frame")
            
        company_Info_Frame = Company_Info_Frame(self, callbackhomefunction, self.User_data, None)
        self.frames["Company_Info_Frame"] = company_Info_Frame
        
        company_Forget_Info_Frame = Company_Forget_Info_Frame(self, callbackhomefunction, self.User_data, None)
        self.frames["Company_Forget_Info_Frame"] = company_Forget_Info_Frame
        
        # Create a label and an entry widget for the search box
        self.company_name_label = tk.Label(self.details_frame, text='Company Name :', bg="#1565c0", fg="#ffffff")
        self.company_name_entry = tk.Entry(self.details_frame, bg="#1976d2", fg="#ffffff")
        
        self.company_brandname_label = tk.Label(self.details_frame, text='Company Brand Name :', bg="#1565c0", fg="#ffffff")
        self.company_brandname_entry = tk.Entry(self.details_frame, bg="#1976d2", fg="#ffffff")
        self.Search_button = tk.Button(self.details_frame, text='Search', command=self.Search_shops, bg="#1976d2", fg="#ffffff")
        
        # * New frame next to list_items in the main frame
        self.selecte_work_midel_frame = tk.Frame(self.details_frame, bg="#1565c0")
        self.selecte_work_midel_frame.grid(row=1, column=0, columnspan=2 , sticky="nsew")
        
        self.selecte_work_extrnal_frame = tk.Frame(self.selecte_work_midel_frame, bg="#1565c0")
        self.selecte_work_extrnal_frame.pack(side="top", fill="x")

        self.selecte_work_Frame_contaner_frame = tk.Frame(self.selecte_work_midel_frame, bg="#1565c0")
        self.selecte_work_Frame_contaner_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.selecte_work_List_Frame_contaner_frame = tk.Frame(self.selecte_work_Frame_contaner_frame, bg="#1565c0")
        self.selecte_work_List_Frame_contaner_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.selecte_work_List_Frame = tk.Frame(self.selecte_work_List_Frame_contaner_frame, bg="#1565c0")
        self.selecte_work_List_Frame.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        
        self.selecte_work_item_List_canvas = tk.Canvas(self.selecte_work_List_Frame, bg="#0d47a1")
        self.selecte_work_item_List_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        
        self.selecte_work_item_List_yscrollbar = tk.Scrollbar(self.selecte_work_List_Frame, orient='vertical', command=self.selecte_work_item_List_canvas.yview)
        self.selecte_work_item_List_yscrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.selecte_work_item_List_xscrollbar = tk.Scrollbar(self.selecte_work_List_Frame_contaner_frame, orient='horizontal', command=self.selecte_work_item_List_canvas.xview)
        self.selecte_work_item_List_xscrollbar.pack(side=tk.TOP, fill=tk.X)
        
        self.selecte_work_item_List_canvas.configure(xscrollcommand=self.selecte_work_item_List_xscrollbar.set, yscrollcommand=self.selecte_work_item_List_yscrollbar.set)

        self.selecte_work_Selected_item_Display_frame = tk.Frame(self.selecte_work_item_List_canvas, bg="#1565c0")
        self.selecte_work_item_List_canvas.create_window((0, 0), window=self.selecte_work_Selected_item_Display_frame, anchor=tk.NW)
        self.selecte_work_Selected_item_Display_frame.bind('<Configure>', lambda e: self.selecte_work_item_List_canvas.configure(scrollregion=self.selecte_work_item_List_canvas.bbox("all")))

        self.search_shops_midel_frame = tk.Frame(self.details_frame, bg="#1565c0")
        
        self.search_shops_extrnal_frame = tk.Frame(self.search_shops_midel_frame, bg="#1565c0")
        self.search_shops_extrnal_frame.pack(side="top", fill="x")

        self.search_shops_Frame_contaner_frame = tk.Frame(self.search_shops_midel_frame, bg="#1565c0")
        self.search_shops_Frame_contaner_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.search_shops_List_Frame_contaner_frame = tk.Frame(self.search_shops_Frame_contaner_frame, bg="#1565c0")
        self.search_shops_List_Frame_contaner_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.search_shops_List_Frame = tk.Frame(self.search_shops_List_Frame_contaner_frame, bg="#1565c0")
        self.search_shops_List_Frame.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        
        self.search_shops_item_List_canvas = tk.Canvas(self.search_shops_List_Frame, bg="#0d47a1")
        self.search_shops_item_List_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        
        self.search_shops_item_List_yscrollbar = tk.Scrollbar(self.search_shops_List_Frame, orient='vertical', command=self.search_shops_item_List_canvas.yview)
        self.search_shops_item_List_yscrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.search_shops_item_List_xscrollbar = tk.Scrollbar(self.search_shops_List_Frame_contaner_frame, orient='horizontal', command=self.search_shops_item_List_canvas.xview)
        self.search_shops_item_List_xscrollbar.pack(side=tk.TOP, fill=tk.X)
        
        self.search_shops_item_List_canvas.configure(xscrollcommand=self.search_shops_item_List_xscrollbar.set, yscrollcommand=self.search_shops_item_List_yscrollbar.set)

        self.search_shops_Selected_item_Display_frame = tk.Frame(self.search_shops_item_List_canvas, bg="#1565c0")
        self.search_shops_item_List_canvas.create_window((0, 0), window=self.search_shops_Selected_item_Display_frame, anchor=tk.NW)
        self.search_shops_Selected_item_Display_frame.bind('<Configure>', lambda e: self.search_shops_item_List_canvas.configure(scrollregion=self.search_shops_item_List_canvas.bbox("all")))

        def show_request():
            self.company_name_label.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W) 
            self.company_name_entry.grid(row=0, column=2, padx=5, pady=5, sticky=tk.W)
            self.company_brandname_label.grid(row=0, column=3, padx=5, pady=5, sticky=tk.W)
            self.company_brandname_entry.grid(row=0, column=4, padx=5, pady=5, sticky=tk.W) 
            self.Search_button.grid(row=0, column=5, padx=6, pady=5, sticky=tk.W)              
            self.search_shops_midel_frame.grid(row=1, column=3, columnspan=2, sticky="nsew")
            self.Send_requestshow_button.grid_remove()
            self.Send_requesthid_button.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
    
        def hide_request():
            self.Search_button.grid_remove()
            self.company_brandname_entry.grid_remove()
            self.company_brandname_label.grid_remove()
            self.company_name_entry.grid_remove()
            self.company_name_label.grid_remove()               
            self.search_shops_midel_frame.grid_remove()
            self.Send_requestshow_button.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
            self.Send_requesthid_button.grid_remove()
        
        self.Send_requestshow_button = tk.Button(self.details_frame, text='Request To Shop', command=show_request, bg="#1976d2", fg="#ffffff")
        self.Send_requestshow_button.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.Send_requesthid_button = tk.Button(self.details_frame, text='Done Requesting', command=hide_request, bg="#1976d2", fg="#ffffff")
        
        self.main_name = ""
        self.Msg_label = tk.Label(self.details_frame, text="Company Not Found!", fg="red", bg="#1565c0")
        self.Found_User_id_var = tk.StringVar()
        
        self.Create_Own_shop_button = tk.Button(self.details_frame, text='Create New Shop', command=lambda:self.show_frame("Company_Info_Frame"), bg="#1976d2", fg="#ffffff")
        
        self.cancle_button = tk.Button(self.details_frame, text='Cancle', command=self.canceal_callback, bg="#1976d2", fg="#ffffff")

        self.Create_Own_shop_button.grid(row=17, column=0, padx=5, pady=5, sticky=tk.W)
        self.cancle_button.grid(row=17, column=3, padx=5, pady=5, sticky=tk.W)
        
        self.update_user_work_shop()
        
    def canceal_callback(self):
        self.Canceal_callback()
        self.master.Loged_User = None
        self.destroy()

    def show_frame(self, frame_name):
        self.frames["Company_Info_Frame"].User_data = self.User_data
        
        # hide all frames except the one to be shown
        for frame in self.frames.values():
            frame.grid_remove()
        self.frames[frame_name].grid()
          
    def update_user_work_shop(self):
        #print("update_user_work_shop ")
        User_work_shops = []
        if self.User_data and not self.User_data['User_work_shop'] == None and not self.User_data['User_work_shop'] == 'None':
            try:
                User_work_shops = json.loads(self.User_data['User_work_shop'])
            except:
                try:
                    User_work_shops = load_list(self.User_data['User_work_shop'])
                except:
                    print("user_work_shop json, load_list can not read it")
                    pass  
        #print("User_work_shops ", User_work_shops)
        
        Shops = []
        if User_work_shops:
            for Shop in User_work_shops:
                s = fetch_as_dict_list(cur, "SELECT * FROM Shops WHERE Shop_id=? AND Shop_name=? AND Shop_brand_name=?", 
                        (str(Shop[0]), str(Shop[1]), str(Shop[2])))
                if s:
                    Shops.append(s[0])
                    #print("s : " + str(s))
                    #print("Shops : " + str(Shops))  
                
        def login(i):
            for frame in self.frames.values():
                try:
                    frame.grid_remove()
                except:
                    pass
                Shops_info = {'Selected_Shop': Shops[i], 'Shops': Shops, 'User': self.User_data, 'User_Shops_List': User_work_shops, 'Shop_items': [], 'Shop_Actions': ""}
                if not self.master.title == "Security Elevation":
                    self.master.master.user = self.User_data
                    self.master.master.Shops_info = Shops_info
                    self.master.master.Shops = Shops
                    self.master.master.User_Shops_List = User_work_shops
                    self.master.master.load()
                    self.master.destroy()
                    #self.master.tklevelwin.destroy()
            
        for items in self.selecte_work_Selected_item_Display_frame.winfo_children():
            items.destroy()
            
        self.show_frame("Select_User_Company_State_Frame")
        if len(User_work_shops): 
            for i, User_work_shop in enumerate(User_work_shops):
                new_item_fram = tk.Frame(self.selecte_work_Selected_item_Display_frame, highlightthickness=2, highlightbackground="black", bg="#0d47a1")
                new_item_fram.grid(row=len(self.selecte_work_Selected_item_Display_frame.winfo_children()), column=0, pady=1, sticky=tk.W)

                new_item_name = tk.Label(new_item_fram, text=str(User_work_shop[1]), font=("Arial", 11), bg="#0d47a1", fg="#ffffff")
                new_item_name.grid(row=0, column=1, columnspan=6, sticky="nsew")

                new_item_brandname = tk.Label(new_item_fram, text=str(User_work_shop[2]), font=("Arial", 11), bg="#0d47a1", fg="#ffffff")
                new_item_brandname.grid(row=1, column=1, columnspan=6, sticky="nsew")
                
                a = fetch_as_dict_list(cur, "SELECT * FROM Shops", ())
                find_shop_in_sysdb = fetch_as_dict_list(cur, "SELECT * FROM Shops WHERE Shop_name=? AND Shop_brand_name=?", 
                    (str(User_work_shop[1]), str(User_work_shop[2])))
                    
            def Get_Shop_Data(index, frame, uws):
                Link = self.master.link_entry.get()
                shop_result = Get_Shop(Link, self.User_data['User_name'], self.User_data['User_password'], uws[1], uws[2])
                if shop_result:
                    if shop_result == []:
                        Whiting_Label = tk.Label(frame, text="Online Login Failed", font=("Arial", 11), bg="#0d47a1", fg="#ffffff")
                        Whiting_Label.grid(row=1, column=7, columnspan=6, sticky="nsew")
                    else:
                        answer = tk.messagebox.askquestion("Question", "Shop Data found on online database. Do you want to download data?")
                        if answer == 'yes':
                            Add_Shop_data_From_list(shop_result[0])
                            Whiting_Label = tk.Label(frame, text="Online Login Successful", font=("Arial", 11), bg="#0d47a1", fg="#ffffff")
                            Whiting_Label.grid(row=1, column=7, columnspan=6, sticky="nsew")
                            self.update_user_work_shop()
                        else:
                            Whiting_Label = tk.Label(frame, text="Data Not Found. Login Online", font=("Arial", 11), bg="#0d47a1", fg="#ffffff")
                            Whiting_Label.grid(row=1, column=7, columnspan=6, sticky="nsew")
                else:
                    Whiting_Label = tk.Label(frame, text="API Error", font=("Arial", 11), bg="#0d47a1", fg="#ffffff")
                    Whiting_Label.grid(row=1, column=7, columnspan=6, sticky="nsew")
                    
            if not find_shop_in_sysdb:
                getshopdb_button = tk.Button(new_item_fram, text="Get Shop Data", font=("Arial", 12), command= lambda index=i, frame=new_item_fram, uws=User_work_shop: Get_Shop_Data(index, frame, uws), bg="#1976d2", fg="#ffffff")
                getshopdb_button.grid(row=0, column=7, sticky="e")
            elif User_work_shop[3] and User_work_shop[3][0] == -2:
                Aggried_button = tk.Button(new_item_fram, text="Aggreed", font=("Arial", 12), command= lambda index=i, frame=new_item_fram: self.remove_item(index, frame), bg="#1976d2", fg="#ffffff")
                Aggried_button.grid(row=0, column=7, sticky="e")
            elif User_work_shop[3] and User_work_shop[3][0] == -1:
                Whiting_Cancle_button = tk.Button(new_item_fram, text="Cancel", font=("Arial", 12), command= lambda index=i, frame=new_item_fram: cancle_witting_respond(index, frame), bg="#1976d2", fg="#ffffff")
                Whiting_Cancle_button.grid(row=0, column=7, sticky="e")
                Whiting_Label = tk.Label(new_item_fram, text="Waiting For Respond", font=("Arial", 11), bg="#0d47a1", fg="#ffffff")
                Whiting_Label.grid(row=1, column=7, columnspan=6, sticky="nsew")
                
            elif User_work_shop[3] and User_work_shop[3][0] == 0:
                Enable_button = tk.Button(new_item_fram, text="Enable", font=("Arial", 12), command= lambda index=i, frame=new_item_fram: self.remove_item(index, frame), bg="#1976d2", fg="#ffffff")
                Enable_button.grid(row=0, column=7, sticky="e")
            elif User_work_shop[3] and User_work_shop[3][0] == 1:
                LogIn_button = tk.Button(new_item_fram, text="Customer", font=("Arial", 12), command= lambda index=i, frame=new_item_fram: self.remove_item(index, frame), bg="#1976d2", fg="#ffffff")
                LogIn_button.grid(row=0, column=7, sticky="e")
            else:
                LogIn_button = tk.Button(new_item_fram, text="LogIn", font=("Arial", 12), command= lambda j=i: login(j), bg="#1976d2", fg="#ffffff")
                LogIn_button.grid(row=0, column=7, sticky="e")
    def update_search_shops(self):        
        for items in self.search_shops_Selected_item_Display_frame.winfo_children():
            items.destroy()
            
        for i, search_result in enumerate(self.found_shops):
            print("search_result ", search_result)
            
            new_item_fram = tk.Frame(self.search_shops_Selected_item_Display_frame, highlightthickness=2, highlightbackground="black")
            new_item_fram.grid(row=len(self.search_shops_Selected_item_Display_frame.winfo_children()), column=0, pady=1, sticky=tk.W)

            # TODO ADD IMAGE 
            def remove_item(index, frame):
                if self.found_Shops_result:
                    Shops = self.found_Shops_result[index]
                    print("company_name : " + str(Shops['Shop_name']))
                    print("company_brandname : " + str(Shops['Shop_brand_name']))
                    print("Shop_workers : " + str(Shops['Shop_workers']))
                    
                    Shop_workers = []
                    if Shop_workers == None or Shop_workers == 'None':
                        Shop_workers =json.loads(Shops['Shop_workers'])
                    found_worker_inshop = 0
                    for sw, Shop_worker in enumerate(Shop_workers):
                        if Shop_worker[0] == self.User_data['User_id']:
                            found_worker_inshop = 1
                            Shop_workers[sw] = [self.User_data['User_id'], self.User_data['User_fname'] + " "+ self.User_data['User_Lname'], self.User_data['User_name'], "WORKER", Shops['Shop_name'], Shops['Shop_brand_name'], -2]
                    # e.g [2, 'Abdul Kedir', 'AK Abdul', 'OWNER', 'BELLEMA FASHION', 'ADOT', '10']        
                    if found_worker_inshop == 0:
                        print("self.User_data : ", self.User_data)
                        Shop_workers.append([self.User_data['User_id'], self.User_data['User_fname'] + " "+ self.User_data['User_Lname'], self.User_data['User_name'], "WORKER", Shops['Shop_name'], Shops['Shop_brand_name'], -2])
                        cur.execute('UPDATE Shops SET Shop_workers=? WHERE Shop_id=?', (json.dumps(Shop_workers), Shops['Shop_id']))
                        # Commit the changes to the database
                        conn.commit()
                    
                    User_work_shops = []
                    if self.User_data and not self.User_data['User_work_shop'] == None and not self.User_data['User_work_shop'] == 'None':                            
                        try:
                            User_work_shops = json.loads(self.User_data['User_work_shop'])
                        except:
                            try:
                                User_work_shops = load_list(self.User_data['User_work_shop'])
                            except:
                                print("user_work_shop json, load_list can not read it")
                                pass  
                    found_shop_inworkes = 0
                    for uws, User_work_shop in enumerate(User_work_shops):
                        if User_work_shop[0] == Shops['Shop_id']:
                            found_shop_inworkes = 1
                            User_work_shops[uws] = [Shops['Shop_id'], Shops['Shop_name'], Shops['Shop_brand_name'], -1]
                            
                    if found_shop_inworkes == 0:
                        User_work_shops.append([Shops['Shop_id'], Shops['Shop_name'], Shops['Shop_brand_name'], [-1]])
                        cur.execute('UPDATE Users SET User_work_shop=? WHERE User_id=?', (json.dumps(User_work_shops), self.User_data['User_id']))
                        # Commit the changes to the database
                        conn.commit()
                        self.User_data['User_work_shop'] = json.dumps(User_work_shops)
                        
                    self.update_user_work_shop()
                    
            new_item_name = tk.Label(new_item_fram, text=str(search_result['Shop_name']), font=("Arial", 11))
            new_item_name.grid(row=0, column=1, columnspan=6, sticky="nsew")

            new_item_brandname = tk.Label(new_item_fram, text=str(search_result['Shop_brand_name']), font=("Arial", 11))
            new_item_brandname.grid(row=1, column=1, columnspan=6, sticky="nsew")


            ask_button = tk.Button(new_item_fram, text="Ask", font=("Arial", 12), command= lambda index=i, frame=new_item_fram: remove_item(index, frame))
            ask_button.grid(row=0, column=7, sticky="e")
            
            #send_button = tk.Button(new_item_fram, text="Send", font=("Arial", 12), command= lambda index=i, frame=new_item_fram: remove_item(index, frame))
            #send_button.grid(row=0, column=7, sticky="nsew")
        
    def Search_shops(self):
        # Get the values from the user details widgets
        company_name = self.company_name_entry.get()
        company_brandname = self.company_brandname_entry.get()
        self.found_Shops_result = fetch_as_dict_list(cur, 'SELECT * FROM Shops', ()) # WHERE Shop_name=? AND Shop_brand_name=?', (company_name, company_brandname))
        if self.found_Shops_result:
            print("company_name : " + str(company_name))
            print("company_brandname : " + str(company_brandname))
            for shop in self.found_Shops_result:
                print("Shop_workers : " + str(shop['Shop_workers']))
                if shop['Shop_name'] == company_name and shop['Shop_brand_name'] == company_brandname:
                    self.found_shops.append(shop)
                    self.Msg_label.grid(row=1, column=2, padx=5, pady=5, sticky=tk.W)
                    self.Msg_label.config(text="Company Found!", fg="Green")
            if len(self.found_shops) == 0:                
                self.Msg_label.grid(row=1, column=2, padx=5, pady=5, sticky=tk.W)
                self.Msg_label.config(text="Company Not Found!", fg="red")
            self.update_search_shops()
                    
    def clear_user_details_widget(self):
        self.company_name_entry.delete(0, "end")
        self.company_brandname_entry.delete(0, "end")
        
    # Define the function for adding a new user
    def Send_user(self):
        # Get the values from the user details widgets
        company_name = self.company_name_entry.get()
        company_brandname = self.company_brandname_entry.get()
        if company_name == "" or company_brandname == "":
           pass
        '''
        else:
            
                
            if self.Send_button.cget("text") == "Send":
                
            else:
                self.Msg_label.grid_remove()
                self.Send_button.config(text="Send")
        '''
        
    def forget_password_fuc(self, event):
        print("forget_password_fuc")
        pass
      
    def Create_new_user(self, event):
        print("Create_new_user")
        pass
      
    def update_combobox_values(self):
        #print("ss "+ str([";"] + [name[0] for name in self.node_hierarchy]))
        pass #self.node_combobox["values"] = [";"] + [name[0] for name in self.node_hierarchy]


    def log_in(self):
        entered_username = self.username_entry.get()
        entered_password = self.password_entry.get()

        cursor.execute("SELECT * FROM USERS WHERE User_name=? AND User_password=?", (entered_username, entered_password))
        users = cursor.fetchall()
         
        if users:
           for user in users:
              if "IT" in user[11] or "Admin" in user[11] or "Worker" in user[11]:
                  #print("User : " + str(user))
                  #print("User11 : " + str(user[15]))
                  error_label = tk.Label(self.logging_box, text="Login Secsesfull", font=("Helvetica", 18), bg="#e74c3c", fg="green")
                  error_label.pack(pady=20)
                  self.master.display_frame = DisplayFrame(self.master, user)
                  self.master.display_frame.grid(row=0, column=0, sticky="nsew")
                  self.master.frames["DisplayFrame"] = self.master.display_frame
                  self.master.frames["DisplayFrame"].user = user
                  self.master.frames["DisplayFrame"].load()
        else:
            error_label = tk.Label(self.logging_box, text="Login failed", font=("Helvetica", 18), bg="#e74c3c", fg="#ffffff")
            error_label.pack(pady=20)
    
    def show_first_frame(self):
        # call the function in the main file to show the first frame
        self.master.show_frame("DisplayFrame")
    def on_name_entry(self, event):
        cur.execute('SELECT * FROM Users')
        users = cur.fetchall()
        for user in users:
            print("on_name_entry\n"+str(user[1]))
            if user[1] == self.name_entry.get():
                self.add_button.config(text="Update")    
                return
        if self.main_name == self.name_entry.get() and not self.main_name == "":
            self.add_button.config(text="Update")
        else:
            self.add_button.config(text="New")
            
    def perform_print(self):
        item = self.user_docinfo_listbox.focus()  # Get the item that was clicked
        if item:
            item_text = self.user_docinfo_listbox.item(item, "values")  # Get the text values of the item
            id = self.user_docinfo_listbox.item(item, "text")
            barcode = item_text[0]
            doc_ = cur.execute("SELECT * FROM doc_table WHERE doc_barcode=?", (barcode,)).fetchone()
            if doc_:
                answer = tk.messagebox.askquestion("Question", "Do you what to print "+str(barcode)+" ?")
                if answer == 'yes':
                    #print(str(doc_))
                    doc_edit_form = load_slip(doc_, id)
                    #print("don loding slip : \n\n" + str(doc_edit_form))
                    self.user = self.master.master.master.master.user
                    PrinterForm.print_slip(self, self.user_info, doc_edit_form, 1) # TODO chack in setting if paper cut allowed

