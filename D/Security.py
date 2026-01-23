import tkinter as tk
from tkinter import ttk
import sqlite3, os
import json

data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data'))
db_path = os.path.join(data_dir, 'my_database.db')
conn = sqlite3.connect(db_path)
cur = conn.cursor()

from C.Sql3 import *
from C.List import *
from C.API.Get import *
from C.API.API import *
from C.Database.Set import *

from Frames.User.Select_User_Company_State import Select_User_Company_State_Frame
#from Login import Loging_Frame
from Frames.User.View_User import User_Info_Frame
from Frames.User.User_Forget_Info import User_Forget_Info_Frame
#from Frames.User.Select_User_Company_State import Select_User_Company_State_Frame

#from Frames.Company.View_Company import Company_Info_Frame
#from Frames.Company.Company_Forget_Info import Company_Forget_Info_Frame


class SecurityForm(tk.Toplevel):
    LAST_USER_FILE = os.path.join(data_dir, 'last_user.json')
    def __init__(self, master, title, whatfor="Please select your user account and enter your credentials"):
        # master is the parent window (can be a tk root or any widget)
        super().__init__(master)
        self.master = master
        
        self._credentials_shown = True

        # create a Toplevel window for the security form
        self.Security_form = self
        self.Security_form.Loged_User = None
        self.Security_form.resizable(False, False)
        self.Security_form.wm_iconbitmap('')
        self.Security_form.wm_title('')
        # make the frame bigger
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        width, height = 900, 600
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        self.Security_form.geometry(f"{width}x{height}+{int(x)}+{int(y)}")


        # Android-style dark blue color scheme
        bg_dark = "#0d47a1"      # Deep blue
        bg_light = "#1565c0"     # Darker blue
        accent_blue = "#1976d2"  # Medium blue
        text_light = "#ffffff"
        
        self.Security_form.configure(bg=bg_dark)

        # layout
        for r in range(9):
            self.Security_form.grid_rowconfigure(r, weight=1)
        for c in range(4):
            self.Security_form.grid_columnconfigure(c, weight=1)

        # load logged users from loged.txt
        self.load_logged_users()

        # load last/previous info
        self.last_info = self._load_last_info()

        # Instruction label on top with Android styling
        self.instruction_label = tk.Label(
            self.Security_form,
            text=whatfor,
            anchor="w",
            bg=bg_dark,
            fg=text_light,
            font=("Roboto", 14, "bold")
        )
        self.instruction_label.grid(row=0, column=1, columnspan=int(width/(len(whatfor)+1)), sticky="ew", padx=12, pady=(12, 8))

        # container for user buttons with horizontal scrolling
        self._create_user_buttons_container()

        # selection state
        self.selected_user_var = tk.StringVar(value="")

        # Credentials frame (hidden initially)
        self.credentials_frame = tk.Frame(self.Security_form, bg=bg_light)
        self.credentials_frame.grid(row=2, column=0, columnspan=4, sticky="ew", padx=8, pady=8)
        self._credentials_shown = True

        # Username entry
        username_label = tk.Label(
            self.credentials_frame,
            text='Username:',
            bg=bg_light,
            fg=text_light,
            font=("Roboto", 11)
        )
        username_label.grid(row=0, column=0, sticky=tk.W, padx=12, pady=8)
        
        self.entered_username_entry = tk.Entry(
            self.credentials_frame,
            bg="#ffffff",
            fg="#0d47a1",
            font=("Roboto", 11),
            relief=tk.FLAT,
            bd=2
        )
        self.entered_username_entry.grid(row=0, column=1, columnspan=2, sticky="ew", padx=12, pady=8)

        # Password entry
        password_label = tk.Label(
            self.credentials_frame,
            text='Password:',
            bg=bg_light,
            fg=text_light,
            font=("Roboto", 11)
        )
        password_label.grid(row=1, column=0, sticky=tk.W, padx=12, pady=8)
        
        self.entered_password_entry = tk.Entry(
            self.credentials_frame,
            show="*",
            bg="#ffffff",
            fg="#0d47a1",
            font=("Roboto", 11),
            relief=tk.FLAT,
            bd=2
        )
        self.entered_password_entry.grid(row=1, column=1, columnspan=2, sticky="ew", padx=12, pady=8)

        self.log_in_button = tk.Button(
            self.credentials_frame,
            text="Log In",
            command=self.log_in,
            bg=accent_blue,
            fg=text_light,
            font=("Roboto", 10, "bold"),
            relief=tk.FLAT,
            activebackground="#1565c0",
            activeforeground=text_light,
            padx=10,
            pady=8
        )
        self.log_in_button.grid(row=2, column=1, sticky="ew", padx=6, pady=8)
        #self.log_in_button.configure(state='disabled')

        cursor.execute("SELECT * FROM setting")
        b = cursor.fetchall()

        # Error list frame with vertical scrollbar
        self.master.Error_list_frame_canvas = tk.Canvas(
            self.Security_form,
            height=80,
            highlightthickness=0,
            bg=bg_light
        )
        self.master.Error_list_scrollbar = tk.Scrollbar(
            self.Security_form,
            orient="vertical",
            command=self.master.Error_list_frame_canvas.yview,
            bg=bg_dark,
            activebackground=accent_blue
        )
        self.master.Error_list_frame_canvas.configure(yscrollcommand=self.master.Error_list_scrollbar.set)

        self.master.Error_list_frame = tk.Frame(self.master.Error_list_frame_canvas, bg=bg_light)
        self.master.Error_list_frame_canvas.create_window((0, 0), window=self.master.Error_list_frame, anchor="nw")

        self.master.Error_list_frame_canvas.grid(row=7, column=0, columnspan=4, sticky="nsew")
        self.master.Error_list_scrollbar.grid(row=7, column=4, sticky="ns")

        self.master.Error_list_frame.bind(
            "<Configure>",
            lambda e: self.master.Error_list_frame_canvas.configure(
            scrollregion=self.master.Error_list_frame_canvas.bbox("all")
            )
        )
        
        # Link section
        self.master.link_entry = tk.Entry(
            self.Security_form,
            bg="#ffffff",
            fg="#0d47a1",
            font=("Roboto", 10),
            relief=tk.FLAT,
            bd=2
        )
        self.master.link_entry.insert(0, "http://localhost/HiperMarketSit/API/Get.php")
        self.master.link_entry.grid(row=8, column=0, columnspan=4, sticky="we", padx=12, pady=8)

        # Buttons with Android Material style
        self.link_button = tk.Button(
            self.Security_form,
            text="Check",
            command=lambda: islinked(self.master.link_entry.get()),
            bg=accent_blue,
            fg=text_light,
            font=("Roboto", 10, "bold"),
            relief=tk.FLAT,
            activebackground="#1565c0",
            activeforeground=text_light,
            padx=10,
            pady=8
        )
        self.link_button.grid(row=8, column=3, sticky="e", padx=6, pady=8)
        
        if whatfor == "Please select your user account and enter your credentials":
            btntext = "Close"
        else:
            btntext = "OK Skip"
        self.button_BACK_close = tk.Button(
            self.Security_form,
            text=btntext,
            command=self.close_fun,
            bg="#424242",
            fg=text_light,
            font=("Roboto", 10, "bold"),
            relief=tk.FLAT,
            activebackground="#616161",
            activeforeground=text_light,
            padx=10,
            pady=8
        )
        self.button_BACK_close.grid(row=8, column=4, sticky="e", padx=12, pady=8)

        # Links section
        self.forget_password_label = tk.Label(
            self.Security_form,
            text="Forgot Password?",
            fg="#64b5f6",
            bg=bg_dark,
            cursor="hand2",
            font=("Roboto", 10, "underline")
        )
        self.forget_password_label.grid(row=9, column=0, sticky="w", padx=12, pady=8)
        self.forget_password_label.bind("<Button-1>", self.forget_password_fuc)

        self.Create_new_label = tk.Label(
            self.Security_form,
            text="Create Account",
            fg="#64b5f6",
            bg=bg_dark,
            cursor="hand2",
            font=("Roboto", 10, "underline")
        )
        self.Create_new_label.grid(row=9, column=3, sticky="e", padx=12, pady=8)
        self.Create_new_label.bind("<Button-1>", self.Create_new_user)

        # Preselect current or previous if available
        preset_name = None
        if self.last_info.get('current'):
            cur.execute("SELECT User_name FROM USERS WHERE User_id=?", (self.last_info['current'],))
            res = cur.fetchone()
            if res:
                preset_name = res[0]
        elif self.last_info.get('previous'):
            cur.execute("SELECT User_name FROM USERS WHERE User_id=?", (self.last_info['previous'],))
            res = cur.fetchone()
            if res:
                preset_name = res[0]
        if preset_name:
            self.selected_user_var.set(preset_name)

        # render user buttons
        self._render_user_buttons()


        # modal
        self.attributes('-topmost', True)
        self.Security_form.transient(self.master)
        self.Security_form.grab_set()
        self.Security_form.focus_set()
        self.master.wait_window(self.Security_form)

        

    def load_logged_users(self):
        loged_path = os.path.join(data_dir, 'loged.txt')
        #print("Loading logged users from: " + loged_path)
        self.user_map = {}
        self.user_names = []
        if os.path.exists(loged_path):
            print("loged.txt found, loading users.")
            try:
                with open(loged_path, 'r', encoding='utf-8') as f:
                    #print("Reading loged.txt...")
                    for line in f:
                        line = line.strip()
                        if not line:
                            continue
                        parts = line.split(':', 1)
                        if len(parts) == 2:
                            print("Processing line: " + line)
                            user_id, user_name = parts
                            self.user_map[user_name] = user_id
                            self.user_names.append(user_name)
            except Exception:
                print("Error loading logged users from loged.txt")
                pass

    # instance-bound helper to update the logged-user list/file when a user logs in.
    # Use: self.update_logged_user("Alice", 5) or self.update_logged_user("Alice")
    def update_logged_user(self, user_name, user_id):
        #print("Updating logged user: " + user_name + (f", id: {user_id}" if user_id is not None else ""))
        if not user_name or user_id is None:
            return False  # cannot add without id
        
        # update in-memory structures
        if user_name not in self.user_map:
            self.user_names.append(user_name)
            self.user_map[user_name] = user_id

        # persist to file (simple id:name per line)
        try:
            #print("Writing logged users to loged.txt...")
            loged_path = os.path.join(data_dir, 'loged.txt')
            with open(loged_path, 'w', encoding='utf-8') as f:
                #print("Saving users...")
                for name, idv in self.user_map.items():
                    f.write(f"{idv}:{name}\n")
                #print("Users saved.")
                return True
        except Exception:
            return False
        
    def close_fun(self):
        if self.button_BACK_close['text'] == "Close" or self.button_BACK_close['text'] == "OK Skip":
            self.Security_form.destroy()
        else:
            self._hide_credentials_page() 
    
    def forget_password_fuc(self, event):
        # hide credentials frame and restore user selection canvas + scrollbar
        try:
            self.credentials_frame.grid_remove()
        except Exception:
            pass
        self.user_Forget_Info_Frame = User_Forget_Info_Frame(self.Security_form, self._hide_credentials_page, None)
        self.user_Forget_Info_Frame.grid(row=0, column=0, sticky="nsew")

        # disable login until a user is chosen again (existing handlers will enable it)
        try:
            self.log_in_button.configure(state='disabled')
        except Exception:
            pass
        self._credentials_shown = False
        self.button_BACK_close['text'] = "Back"

        # self.master.show_frame("User_Forget_Info_Frame")
        pass
      
    def Create_new_user(self, event):
       # we going to chack connection befor creating new user
        # islinked(self.master.link_entry.get())
        # create_frame = self.master.show_frame("User_Info_Frame")
        
        # hide credentials frame and restore user selection canvas + scrollbar
        try:
            self.credentials_frame.grid_remove()
        except Exception:
            pass
        
        self.user_Info_Frame = User_Info_Frame(self.Security_form, self._hide_credentials_page, None)
        self.user_Info_Frame.grid(row=0, column=0, sticky="nsew")

        # disable login until a user is chosen again (existing handlers will enable it)
        try:
            self.log_in_button.configure(state='disabled')
        except Exception:
            pass
        self._credentials_shown = False
        self.button_BACK_close['text'] = "Back"

    def log_in(self):
        entered_username = self.entered_username_entry.get()
        entered_password = self.entered_password_entry.get()
        link = self.master.link_entry.get()
        users = Get_User(link, ["User_name", "User_password"], [entered_username, entered_password])
        if users:
            for user in users:
                print("User : ", user)
                if not 'Id' in user:
                    lb = tk.Label(self.master.Error_list_frame, text="Online Login Secsesfull", fg="green")
                    lb.pack(side=tk.TOP, fill=tk.X, expand=True)
                    answer = tk.messagebox.askquestion("Question", "User Data found on online database. for more ifection use it is better to download user datas. Do you what to download user data?")
                    if answer == 'yes':
                        lb = tk.Label(self.master.Error_list_frame, text="Data Saved Will be Readen Online And Offline", bg="#3ce76f", fg="green")
                        lb.pack(side=tk.TOP, fill=tk.X, expand=True)
                        user = Add_Shop_data_From_list(user)
                    else:
                        lb = tk.Label(self.master.Error_list_frame, text="Data Will be Readen Online", bg="#c2e73c", fg="white")
                        lb.pack(side=tk.TOP, fill=tk.X, expand=True)
                else:     
                    lb = tk.Label(self.master.Error_list_frame, text="Offline Login Secsesfull", bg="#e7cb3c", fg="green")
                    lb.pack(side=tk.TOP, fill=tk.X, expand=True)
    
                select_User_Company_State_Frame = Select_User_Company_State_Frame(self.Security_form, self._hide_credentials_page, user)
                select_User_Company_State_Frame.grid(row=0, column=0, sticky="nsew")
                select_User_Company_State_Frame.User_data = user
                self.Security_form.Loged_User = user

                self.update_logged_user(user['User_name'], user['User_id'])
                
                
                # hide credentials frame and restore user selection canvas + scrollbar
                try:
                    self.credentials_frame.grid_remove()
                except Exception:
                    pass
                
                # disable login until a user is chosen again (existing handlers will enable it)
                try:
                    self.log_in_button.configure(state='disabled')
                except Exception:
                    pass
                self._credentials_shown = False
                self.button_BACK_close['text'] = "Back"
        else:
            tk.Label(self.master.Error_list_frame, text="Online Login Filed", bg="#e74c3c", fg="red").pack(side=tk.TOP, fill=tk.X, expand=True)
            tk.Label(self.master.Error_list_frame, text="User Name("+str(entered_username)+") Or Password Incorrect.", bg="#e74c3c", fg="white").pack(side=tk.TOP, fill=tk.X, expand=True)
    
    def _create_user_buttons_container(self):
        # Create a canvas + horizontal scrollbar and an internal frame to hold buttons.
        # This allows horizontal scrolling when there are more buttons than fit.
        self.user_buttons_canvas = tk.Canvas(self.Security_form, height=120, highlightthickness=0, bg="#0d47a1")
        self.user_buttons_scrollbar = tk.Scrollbar(self.Security_form, orient="horizontal", command=self.user_buttons_canvas.xview, bg="#0d47a1", activebackground="#1976d2", troughcolor="#0d47a1")
        self.user_buttons_canvas.configure(xscrollcommand=self.user_buttons_scrollbar.set)

        # internal frame inside canvas
        self.user_buttons_inner = tk.Frame(self.user_buttons_canvas, bg="#0d47a1")
        # Create window without width restriction so inner frame can expand horizontally
        self.user_buttons_canvas.create_window((0, 0), window=self.user_buttons_inner, anchor="nw")

        # grid the canvas + scrollbar into the parent grid cell
        #self.user_buttons_canvas.grid(row=1, column=0, columnspan=4, sticky="nsew")
        #self.user_buttons_scrollbar.grid(row=5, column=0, columnspan=4, sticky="nsew")

        # keep references for later
        self.user_buttons_frame = self.user_buttons_inner
        self.user_buttons_canvas.bind("<Configure>", self._on_buttons_canvas_configure)
        self.user_buttons_inner.bind("<Configure>", self._update_buttons_scrollregion)

    def _on_buttons_canvas_configure(self, event):
        # Called when canvas size changes; update scrollregion and optionally resize buttons for equal sizing.
        self._update_buttons_scrollregion()
        self._adjust_button_widths()

    def _update_buttons_scrollregion(self, event=None):
        try:
            self.user_buttons_canvas.configure(scrollregion=self.user_buttons_canvas.bbox("all") or (0, 0, 0, 0))
        except Exception:
            pass

    def _adjust_button_widths(self):
        # Attempt to make buttons equal width. If there are many columns, do not shrink too small.
        btns = [w for w in self.user_buttons_frame.winfo_children() if isinstance(w, tk.Button)]
        if not btns:
            return
        try:
            canvas_height = self.user_buttons_canvas.winfo_height() or 120
            # keep a reasonable char width based on canvas height and desired button pixel size
            # use a base pixel width and convert to char count (approx 7 px per char)
            base_pixel = 110
            char_width = max(8, int(base_pixel / 7))
            # calculate height based on canvas height
            button_height = max(2, int(canvas_height / 60))
            for b in btns:
                try:
                    b.configure(width=char_width, height=button_height)
                except Exception:
                    pass
            # update scrollregion after resizing
            self._update_buttons_scrollregion()
        except Exception:
            pass

    def _render_user_buttons(self):
        if len(self.user_names) == 0:
            return
        
        self._hide_credentials_page()
        print("Rendering user buttons...")
        print("User names: " + str(self.user_names))
        # clear existing
        for child in self.user_buttons_frame.winfo_children():
            child.destroy()

        # total buttons includes "New User"
        total = 1 + len(self.user_names)

        # Choose a fixed number of rows depending on total so layout becomes rows x columns
        # and expands horizontally (columns grow) so only horizontal scrolling is needed.
        if total <= 16:
            desired_rows = 2
        elif total <= 36:
            desired_rows = 6
        else:
            desired_rows = 8

        # Try to limit the number of rows so buttons don't get pushed below the visible canvas height.
        canvas_h = self.user_buttons_canvas.winfo_height() or 120
        button_pixel_est = 48  # estimated button height including padding
        max_rows_by_canvas = max(1, canvas_h // button_pixel_est)
        rows = (min(desired_rows, max_rows_by_canvas) if max_rows_by_canvas > 0 else desired_rows)

        cols = (total + rows) // rows  # ceil(total / rows)

        # create a list of names with "New User" first
        names = ["New User"] + self.user_names
        on_col = 0
        on_r = 0
        # create buttons and place them in a grid with fixed number of rows and variable columns
        for idx, name in enumerate(names):
            r = idx // rows       # row cycles 0..rows-1
            if on_r == desired_rows:
                r = on_r % rows
                on_col += 1
                on_r = 1
            else:
                r = on_r // rows
                on_r += 1
            c = on_col 
            if name == "New User":
                btn = tk.Button(self.user_buttons_frame, text=name, command=self._on_new_user_pressed,
                     bg="#1976d2", fg="#ffffff", activebackground="#1565c0", activeforeground="#ffffff")
                btn.grid(row=r, column=c, padx=6, pady=6, sticky="nsew")
            else:
                btn = tk.Button(self.user_buttons_frame, text=name, command=lambda n=name: self._on_user_button_pressed(n),
                     bg="#1976d2", fg="#ffffff", activebackground="#1565c0", activeforeground="#ffffff")
                btn.grid(row=r, column=c, padx=6, pady=6, sticky="nsew")
            for colsc in range(cols):
                self.user_buttons_frame.grid_columnconfigure(colsc, weight=1, minsize=80)
            for colsr in range(rows):
                self.user_buttons_frame.grid_rowconfigure(colsr, weight=1, minsize=48)
        
        # After creating buttons, update sizes and scrollregion
        self.user_buttons_frame.update_idletasks()
        # ensure inner frame requested width is preserved so horizontal scrollbar appears when needed
        self._update_buttons_scrollregion()
        self._adjust_button_widths()

    def _on_new_user_pressed(self):
        # when New User pressed, go to credential page and allow entering username/password
        self.selected_user_var.set("")
        self._show_credentials_page()
        self.button_BACK_close['text'] = "Back"
        self.entered_username_entry.configure(state='normal')
        self.entered_username_entry.delete(0, tk.END)
        self.log_in_button.configure(state='normal')
        self.entered_username_entry.focus_set()

    def _on_user_button_pressed(self, name):
        # when an existing user button is pressed, go to credential page and prefill username (readonly)
        self.selected_user_var.set(name)
        self._show_credentials_page()
        self.button_BACK_close['text'] = "Back"
        self.entered_username_entry.configure(state='normal')
        self.entered_username_entry.delete(0, tk.END)
        self.entered_username_entry.insert(0, name)
        self.entered_password_entry.delete(0, tk.END)
        self.entered_username_entry.configure(state='disabled')
        self.log_in_button.configure(state='normal')
        self.entered_password_entry.focus_set()

    def _select_user(self, name):
        # select without immediately showing credentials
        self.selected_user_var.set(name)
        self.button_BACK_close['text'] = "Back"
        self.entered_username_entry.configure(state='normal')
        self.entered_username_entry.delete(0, tk.END)
        self.entered_username_entry.insert(0, name)
        self.entered_username_entry.configure(state='disabled')
        self.log_in_button.configure(state='normal')

    def _load_last_info(self):
        try:
            if os.path.exists(self.LAST_USER_FILE):
                with open(self.LAST_USER_FILE, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception:
            pass
        return {'current': None, 'previous': None}

    def _save_last_info(self):
        try:
            with open(self.LAST_USER_FILE, 'w', encoding='utf-8') as f:
                json.dump(self.last_info, f)
        except Exception:
            pass

    def _use_last_logged(self):
        # set selection to last 'current' or 'previous' user if available and show credentials
        uid = self.last_info.get('current') or self.last_info.get('previous')
        if uid:
            cur.execute("SELECT User_name FROM USERS WHERE User_id=?", (uid,))
            r = cur.fetchone()
            if r:
                # behave like user button pressed
                self._on_user_button_pressed(r[0])

    def _show_credentials_page(self):
        if self._credentials_shown:
            return
        # hide user selection canvas so credential frame can be shown
        try:
            self.user_buttons_canvas.grid_remove()
        except Exception:
            pass
        # hide scrollbar as well if present
        try:
            if hasattr(self, "user_buttons_scrollbar") and self.user_buttons_scrollbar:
                self.user_buttons_scrollbar.grid_remove()
        except Exception:
            pass
        # place credentials_frame
        self.credentials_frame.grid(row=2, column=0, columnspan=4, sticky="ew", padx=8, pady=8)
        self._credentials_shown = True
        self.button_BACK_close['text'] = "Back"

    def _hide_credentials_page(self):
        # hide credentials frame and restore user selection canvas + scrollbar
        if not self._credentials_shown:
            return
        try:
            self.credentials_frame.grid_remove()
        except Exception:
            pass
        # restore canvas and scrollbar to their original grid positions
        try:
            self.user_buttons_canvas.grid(row=1, column=0, columnspan=4, sticky="nsew", padx=8, pady=(0, 0))
        except Exception:
            pass
        try:
            if hasattr(self, "user_buttons_scrollbar") and self.user_buttons_scrollbar:
                self.user_buttons_scrollbar.grid(row=3, column=0, columnspan=4, sticky="nsew", padx=8, pady=(0, 8))
        except Exception:
            pass
        # disable login until a user is chosen again (existing handlers will enable it)
        try:
            self.log_in_button.configure(state='disabled')
        except Exception:
            pass
        self._credentials_shown = False
        if self.instruction_label.cget("text") == "Please select your user account and enter your credentials":
            self.button_BACK_close['text'] = "Close"
        else:
            self.button_BACK_close['text'] = "OK Skip"

    def add_num(self, event=None):
        # validate and perform login
        selected = self.selected_user_var.get()
        # if New User (no selection) allow username from entry
        if not selected:
            username = self.entered_username_entry.get().strip()
            password = self.entered_password_entry.get()
            if not username:
                print("No username entered for new user mode")
                return
            cur.execute("SELECT * FROM USERS WHERE User_name=? AND User_password=?", (username, password))
        else:
            cur.execute("SELECT * FROM USERS WHERE User_name=? AND User_password=?", (selected, self.entered_password_entry.get()))

        users = cur.fetchall()
        if users:
           user = users[0]
           # optional role checks as before
           try:
               roles_field = user[11] if len(user) > 11 else ""
           except Exception:
               roles_field = ""
           if "IT" in roles_field or "Admin" in roles_field or "Worker" in roles_field:
               # update last/previous tracking
               try:
                   prev_current = self.last_info.get('current')
                   if prev_current and prev_current != user[0]:
                       self.last_info['previous'] = prev_current
                   self.last_info['current'] = user[0]
                   self._save_last_info()
               except Exception:
                   pass

               self.Loged_User = user
               self.Security_form.destroy()
               return

        # fallback: invalid credentials
        print("Invalid username or password")
        # keep window open for retry

def Security_get_user(self):
    secur = SecurityForm(self, "Hiper Market Login Security")
    if secur.Security_form.Loged_User == None:
        return False
    return True

def Chacke_Security(self, user, Shop, onlevel, Whatfor=""):
    # user: expected to be a dict-like object earlier in code; keep original logic but improve fallback
    print("Chacke_Security ", Whatfor)
    #print("load_shop_info user :"+str(user))
    #print("load_shop_info Shop :"+str(Shop))
    results = None
    self.User_work_shops = []
    
    # fallback to original logic used earlier (if user is dict-like)
    if user and isinstance(user, dict) and user.get('User_work_shop') and user.get('User_work_shop') != "" and Shop.get('Shop_Security_Levels'):
        User_work_shops = json.loads(user['User_work_shop'])
        for User_work_shop in User_work_shops:
            print("load_shop_info User_work_shop :"+str(User_work_shop))
            if User_work_shop[1] == Shop['Shop_name'] and User_work_shop[2] == Shop['Shop_brand_name']:
                Shop_Security_Levels = json.loads(Shop['Shop_Security_Levels'])
                print("load_shop_info Shop_Security_Levels :"+str(Shop_Security_Levels))
                try:
                    user_level = float(User_work_shop[3][0])
                except Exception:
                    user_level = 0.0
                
                try:
                    shop_required_level = float(Shop_Security_Levels[onlevel])
                except Exception:
                    shop_required_level = 0.0

                print("load_shop_info onlevel :"+str(onlevel))
                print("load_shop_info user_level :"+str(user_level))
                print("load_shop_info shop_required_level :"+str(shop_required_level))
                if user_level >= shop_required_level:
                    print("load_shop_info user_level level ok :"+str(user_level))
                    return True
                else:
                    print("load_shop_info user_level level not ok :"+str(user_level))
                    # request an elevated login (will allow selecting last/previous user or entering new)
                    secur = SecurityForm(self, "Security Elevation", Whatfor)
                    if secur.Security_form.Loged_User:
                        try:
                            workshops_json = secur.Security_form.Loged_User['User_work_shop']
                            if isinstance(workshops_json, str):
                                workshops = json.loads(workshops_json)
                                print("load_shop_info secur.Security_form.Loged_User workshops :"+str(workshops))
                                for workshop in workshops:
                                    shop_name = workshop[1]
                                    shop_brand = workshop[2]
                                    access_list = workshop[3]     
                                    print("load_shop_info secur.Security_form.Loged_User level not ok :"+str(access_list[0]))
                                    print("load_shop_info secur.Security_form.Loged_User shop_required_level level :"+str(shop_required_level))
                                    print("load_shop_info secur.Security_form.Loged_User onlevel :"+str(Shop_Security_Levels[onlevel]))
                                    if access_list[0] is not None and float(access_list[0]) >= float(shop_required_level) or str(access_list[0]) == str(Shop_Security_Levels[onlevel]):
                                        print("load_shop_info secur.Security_form.Loged_User level ok :"+str(access_list[0]))
                                        return True
                        except Exception as e:
                            print(f"Error parsing workshops: {e}")
                            logged_level = None  
                    print("load_shop_info secur.Security_form.Loged_User not found or level not ok")
                    return False  
    else:
        # fallback to original logic for non-dict user (legacy support)
        return False
    return False
