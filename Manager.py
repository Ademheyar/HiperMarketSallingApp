import tkinter as tk
from tkinter import ttk
from D.Security import Chacke_Security
from M.Doc import DocForm
from M.Product import ProductForm
from M.Actions import ActionsForm
from M.Users import UserForm
from M.Tools import ToolForm
from M.Setting import SettingForm

class ManageForm(ttk.Frame):
    def __init__(self, master, user, Shops, Shops_info, on_Shop):
        ttk.Frame.__init__(self, master)
        self.master = master
        self.user = user
        self.Shops = Shops
        self.on_Shop = on_Shop
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        self.manuframes = {}
        
        self.manage_form = ttk.Frame(self, height=screen_height, width=screen_width)
        self.manage_form.pack(side="top", fill="both", expand=True)

        # create left pane with manage_menus form
        self.left_pane = ttk.Frame(self.manage_form, width=200, height=500)
        self.left_pane.pack(side="left", fill="y")

        self.manage_menus_label = ttk.Label(self.left_pane, text="Manage Menus")
        self.manage_menus_label.pack()
        
        if Chacke_Security(self, self.user, self.Shops[self.on_Shop], 27, f'User Has No Permission To Access DOC FRAME OR LOGIN AS ADMIN'):                        
            self.doc_form = DocForm(self.manage_form, self.user, self.Shops)
            self.manuframes["DocForm"] = self.doc_form

            # create buttons in manage_menus form
            self.doc_btn = ttk.Button(self.left_pane, text="Doc", command=self.doc_form.show_doc_form)
            self.doc_btn.pack(side="top", fill="both", expand=True)
        
        if Chacke_Security(self, self.user, self.Shops[self.on_Shop], 28, f'User Has No Permission To Access PRODUCT FRAME OR LOGIN AS ADMIN'):                        
            self.Product_form = ProductForm(self.manage_form, self.user, self.Shops, self.on_Shop)
            self.manuframes["ProductFrame"] = self.Product_form

            self.product_btn = ttk.Button(self.left_pane, text="Product", command= lambda : self.show_frame("ProductFrame"))
            self.product_btn.pack(side="top", fill="both", expand=True)
        
        if Chacke_Security(self, self.user, self.Shops[self.on_Shop], 29, f'User Has No Permission To Access USER FRAME OR LOGIN AS ADMIN'):                        
            self.user_Form = UserForm(self.manage_form, user)
            self.manuframes["UserForm"] = self.user_Form

            self.user_btn = ttk.Button(self.left_pane, text="User", command=self.user_Form.show_user_form)
            self.user_btn.pack(side="top", fill="both", expand=True)

        if Chacke_Security(self, self.user, self.Shops[self.on_Shop], 30, f'User Has No Permission To Access TOOLS FRAME OR LOGIN AS ADMIN'):                        
            self.tool_form = ToolForm(self.manage_form, user, Shops, self.on_Shop)
            self.manuframes["ToolForm"] = self.tool_form
            self.tools_btn = ttk.Button(self.left_pane, text="Tools", command=self.tool_form.show_tools_form)
            self.tools_btn.pack(side="top", fill="both", expand=True)
        
        if Chacke_Security(self, self.user, self.Shops[self.on_Shop], 31, f'User Has No Permission To Access ACTIONS FRAME OR LOGIN AS ADMIN'):                        
            self.Actions_Form = ActionsForm(self.manage_form, user, Shops, Shops_info)
            self.manuframes["ActionsForm"] = self.Actions_Form

            self.Action_btn = ttk.Button(self.left_pane, text="Promotions &\n Action", command=self.Actions_Form.show_product_form)
            self.Action_btn.pack(side="top", fill="both", expand=True)
    
        if Chacke_Security(self, self.user, self.Shops[self.on_Shop], 54, f'User Has No Permission To Access SETTING FRAME OR LOGIN AS ADMIN'):                        
            self.setting_form = SettingForm(self.manage_form, user, Shops)
            self.manuframes["SettingForm"] = self.setting_form
            
            self.setting_btn = ttk.Button(self.left_pane, text="Setting", command=self.setting_form.show_Setting_Form)
            self.setting_btn.pack(side="top", fill="both", expand=True)

    def hide_all_manager(self):
        self.master.show_frame("DisplayFrame")
        #self.main_frame.configure(height=self.screen_height, width=self.screen_width)

    def show_frame(self, frame_name):
        # hide all frames except the one to be shown
        for frame in self.manuframes.values():
            if frame:
                frame.pack_forget()
        if frame_name == "ProductFrame" and not self.manuframes[frame_name]:
            self.manuframes[frame_name] = ProductForm(self.manage_form, self.user, self.Shops)
        self.manuframes[frame_name].pack(side="top", fill="both", expand=True)

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
