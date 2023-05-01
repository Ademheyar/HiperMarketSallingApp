import tkinter as tk
from tkinter import ttk
from Manger.Info import InfoForm
from Manger.Doc import DocForm
from Manger.Product import ProductForm
from Manger.Users import UserForm
from Manger.Tools import ToolForm

class ManageForm(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
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

        self.info_Form = InfoForm(self.manage_form)
        self.manuframes["InfoForm"] = self.info_Form

        self.doc_form = DocForm(self.manage_form)
        self.manuframes["DocForm"] = self.doc_form

        self.Product_form = ProductForm(self.manage_form)
        self.manuframes["ProductFrame"] = self.Product_form
        
        self.user_Form = UserForm(self.manage_form)
        self.manuframes["UserForm"] = self.user_Form

        self.tool_form = ToolForm(self.manage_form)
        self.manuframes["ToolForm"] = self.tool_form

        # create buttons in manage_menus form
        self.info_btn = tk.Button(self.left_pane, text="Info", command=InfoForm(self.manage_form).show_info_form)
        self.info_btn.pack()

        self.doc_btn = tk.Button(self.left_pane, text="Doc", command=DocForm(self.manage_form).show_doc_form)
        self.doc_btn.pack()

        self.product_btn = tk.Button(self.left_pane, text="Product", command=ProductForm(self.manage_form).show_product_form)
        self.product_btn.pack()

        #self.report_btn = tk.Button(self.left_pane, text="Report", command=self.show_report_form)
        #self.report_btn.pack()

        self.user_btn = tk.Button(self.left_pane, text="User", command=UserForm(self.manage_form).show_user_form)
        self.user_btn.pack()

        self.tools_btn = tk.Button(self.left_pane, text="Tools", command=ToolForm(self.manage_form).show_tools_form)
        self.tools_btn.pack()

        self.setting_btn = tk.Button(self.left_pane, text="Setting", command=self.show_setting_form)
        self.setting_btn.pack()

        self.about_btn = tk.Button(self.left_pane, text="About", command=self.show_about_form)
        self.about_btn.pack()

        self.close_btn = tk.Button(self.left_pane, text="Close", command=self.hide_all_manager)
        self.close_btn.pack()

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
