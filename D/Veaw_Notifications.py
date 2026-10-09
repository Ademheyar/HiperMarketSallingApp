import tkinter as tk
import os

data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data'))
db_path = os.path.join(data_dir, 'my_database.db')

from D.Upload_ import UploadingForm

# TODO: user can change name, or password in this form
# TODO: user can add sub user depanding on it usertype
class Veaw_Notifications(tk.Frame):
    def __init__(self, master, User, Shops, app=None):
        palette = getattr(master.winfo_toplevel(), '_app_theme_palette', {})
        self.palette = palette
        tk.Frame.__init__(self, master, bg=palette.get('background', '#0b1726'))
        self.app = app or master
        self.Shops = Shops
        self.user = User
        background = palette.get('background', '#0b1726')
        surface = palette.get('surface', '#132238')
        self.row_color = surface
        self.text_color = palette.get('text', '#f8fafc')
        self.accent_color = palette.get('accent', '#2f80ed')

        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self._label0 = tk.Label(
            self, text="Notifications", font=("Segoe UI", 14, "bold"),
            bg=background, fg=self.text_color, anchor='w',
        )
        self._label0.grid(row=0, column=0, sticky='ew', padx=10, pady=(8, 4))

        self.List_Frame = tk.Frame(self, bg=background)
        self.List_Frame.grid(row=1, column=0, sticky='nsew')
        self.List_Frame.rowconfigure(0, weight=1)
        self.List_Frame.columnconfigure(0, weight=1)
        self.item_List_canvas = tk.Canvas(
            self.List_Frame, bg=background, highlightthickness=0,
        )
        self.item_List_canvas.grid(row=0, column=0, sticky='nsew')
        self.item_List_yscrollbar = tk.Scrollbar(
            self.List_Frame,
            orient='vertical',
            command=self.item_List_canvas.yview,
        )
        self.item_List_yscrollbar.grid(row=0, column=1, sticky='ns')
        self.item_List_canvas.configure(yscrollcommand=self.item_List_yscrollbar.set)
        self.Selected_item_Display_frame = tk.Frame(self.item_List_canvas, bg=background)
        self._items_window = self.item_List_canvas.create_window(
            (0, 0), window=self.Selected_item_Display_frame, anchor='nw',
        )
        self.Selected_item_Display_frame.bind(
            '<Configure>',
            lambda _event: self.item_List_canvas.configure(
                scrollregion=self.item_List_canvas.bbox('all'),
            ),
        )
        self.item_List_canvas.bind(
            '<Configure>',
            lambda event: self.item_List_canvas.itemconfigure(
                self._items_window, width=event.width,
            ),
        )

        self.Notifications_list = []
        self.Update_Notifications_list()
        self.Draw_Notifications_list()

    def Update_Notifications_list(self):
        for shop in self.Shops:
            self.Notifications_list.append([
                "Uplode",
                "Warning: " + shop.get('Shop_name', 'Shop') + " data is not uploaded",
            ])

    def Clear_N(self):
        for items in self.Selected_item_Display_frame.winfo_children():
            items.destroy()
            
    def Draw_Notifications_list(self):
        self.Clear_N()
        self._label0.config(text="Notifications (" + str(len(self.Notifications_list)) + ")")
        for i, Notification_list in enumerate(self.Notifications_list):
            ex_bar_frame = tk.Frame(
                self.Selected_item_Display_frame,
                bg=self.row_color,
                highlightthickness=1,
                highlightbackground=self.accent_color,
                padx=12,
                pady=10,
            )
            ex_bar_frame.grid(row=i, column=0, sticky="ew", padx=8, pady=4)
            ex_bar_frame.columnconfigure(0, weight=1)
            search_label = tk.Label(
                ex_bar_frame,
                text=Notification_list[1],
                font=("Segoe UI", 11),
                bg=self.row_color,
                fg=self.text_color,
                anchor='w',
            )
            search_label.grid(row=0, column=0, sticky="ew")
            if Notification_list[0] == "Uplode":
                update_button = tk.Button(
                    ex_bar_frame,
                    text="Update",
                    font=("Segoe UI", 10, "bold"),
                    bg=self.accent_color,
                    fg=self.text_color,
                    relief='flat',
                    command=lambda: UploadingForm(self.app, self.user, self.Shops),
                )
                update_button.grid(row=0, column=1, sticky="e", padx=(10, 0))
