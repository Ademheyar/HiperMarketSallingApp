import tkinter as tk
from tkinter import ttk
<<<<<<< HEAD
from Info import InfoForm
=======
>>>>>>> db9ae79 (adding seller)
from M.Doc import DocForm
from M.Product import ProductForm
from M.Users import UserForm
from M.Tools import ToolForm
<<<<<<< HEAD

class ManageForm(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.master = master
=======
from M.Setting import SettingForm

class ManageForm(tk.Frame):
    def __init__(self, master, user):
        tk.Frame.__init__(self, master)
        self.master = master
        self.user = user
>>>>>>> db9ae79 (adding seller)
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        self.manuframes = {}
        
        self.manage_form = tk.Frame(self, bg="gray", height=screen_height, width=screen_width)
        self.manage_form.pack(side="top", fill="both", expand=True)

        # create left pane with manage_menus form
        self.left_pane = tk.Frame(self.manage_form, bg="gray", width=200, height=500)
        self.left_pane.pack(side="left", fill="y")

        self.manage_menus_label = tk.Label(self.left_pane, text="Manage Menus")
        self.manage_menus_label.pack()

<<<<<<< HEAD
        self.info_Form = InfoForm(self.manage_form)
        self.manuframes["InfoForm"] = self.info_Form

        self.doc_form = DocForm(self.manage_form)
        self.manuframes["DocForm"] = self.doc_form

        self.Product_form = ProductForm(self.manage_form)
=======
        self.doc_form = DocForm(self.manage_form, self.user)
        self.manuframes["DocForm"] = self.doc_form

        self.Product_form = ProductForm(self.manage_form, user)
>>>>>>> db9ae79 (adding seller)
        self.manuframes["ProductFrame"] = self.Product_form
        
        self.user_Form = UserForm(self.manage_form)
        self.manuframes["UserForm"] = self.user_Form

        self.tool_form = ToolForm(self.manage_form)
        self.manuframes["ToolForm"] = self.tool_form

<<<<<<< HEAD
        # create buttons in manage_menus form
        self.info_btn = tk.Button(self.left_pane, text="Info", command=InfoForm(self.manage_form).show_info_form)
        self.info_btn.pack(side="top", fill="both", expand=True)

        self.doc_btn = tk.Button(self.left_pane, text="Doc", command=DocForm(self.manage_form).show_doc_form)
        self.doc_btn.pack(side="top", fill="both", expand=True)

        self.product_btn = tk.Button(self.left_pane, text="Product", command=ProductForm(self.manage_form).show_product_form)
=======
        self.setting_form = SettingForm(self.manage_form, user)
        self.manuframes["SettingForm"] = self.setting_form

        # create buttons in manage_menus form
        self.doc_btn = tk.Button(self.left_pane, text="Doc", command=self.doc_form.show_doc_form)
        self.doc_btn.pack(side="top", fill="both", expand=True)

        self.product_btn = tk.Button(self.left_pane, text="Product", command=self.Product_form.show_product_form)
>>>>>>> db9ae79 (adding seller)
        self.product_btn.pack(side="top", fill="both", expand=True)

        #self.report_btn = tk.Button(self.left_pane, text="Report", command=self.show_report_form)
        #self.report_btn.pack(side="top", fill="both", expand=True)

        self.user_btn = tk.Button(self.left_pane, text="User", command=UserForm(self.manage_form).show_user_form)
        self.user_btn.pack(side="top", fill="both", expand=True)

        self.tools_btn = tk.Button(self.left_pane, text="Tools", command=ToolForm(self.manage_form).show_tools_form)
        self.tools_btn.pack(side="top", fill="both", expand=True)

<<<<<<< HEAD
        self.setting_btn = tk.Button(self.left_pane, text="Setting", command=self.show_setting_form)
=======
        self.setting_btn = tk.Button(self.left_pane, text="Setting", command=self.setting_form.show_Setting_Form)
>>>>>>> db9ae79 (adding seller)
        self.setting_btn.pack(side="top", fill="both", expand=True)

        self.about_btn = tk.Button(self.left_pane, text="About", command=self.show_about_form)
        self.about_btn.pack(side="top", fill="both", expand=True)

        self.close_btn = tk.Button(self.left_pane, text="Close", command=self.hide_all_manager)
        self.close_btn.pack(side="top", fill="both", expand=True)

        # create frames for each form

        self.report_frame = tk.Frame(self.manage_form, bg="white", width=500, height=500)
        self.report_label = tk.Label(self.report_frame, text="Report Form")
        self.report_label.pack()    
        
        # create main manage_form
        self.main_frame = tk.Frame(self.manage_form, bg="white", width=500, height=500)
        self.main_frame.pack(side="left", fill="both", expand=True)

        self.manage_form_label = tk.Label(self.main_frame, text="Manage Form")
        self.manage_form_label.pack()

        # make the window full screen and fixed
        self.main_frame.pack_forget()
        #self.show_frame("InfoForm")

    def hide_all_manager(self):
        self.master.show_frame("DisplayFrame")
        #self.main_frame.configure(height=self.screen_height, width=self.screen_width)

    def show_frame(self, frame_name):
        # hide all frames except the one to be shown
        for frame in self.manuframes.values():
            frame.pack_forget()
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
