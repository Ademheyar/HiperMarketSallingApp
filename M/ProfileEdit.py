"""Modal dialog that lets a signed-in user edit their own account details."""
import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as tkmessagebox

from C.API.Set import Update_User
from M.ProfileIcons import icon_label

DIALOG_BG = '#0b1726'
CARD_BG = '#132238'
FIELD_BG = '#1c2f4a'
BORDER = '#22344f'
TEXT = '#f8fafc'
MUTED = '#8fa3bd'
ACCENT = '#2f80ed'
ACCENT_DARK = '#1c65c9'


EDITABLE_FIELDS = (
    ('User_fname', 'First name', False),
    ('User_Lname', 'Last name', False),
    ('User_phone_num', 'Phone number', False),
    ('User_email', 'Email', False),
    ('User_address', 'Location', False),
    ('User_about', 'About', False),
    ('User_password', 'Password', True),
)


class ProfileEditDialog(tk.Toplevel):
    """Small form for editing the signed-in user's profile fields."""

    def __init__(self, master, user, link='', on_saved=None):
        tk.Toplevel.__init__(self, master)
        self.user = user or {}
        self.link = link
        self.on_saved = on_saved
        self.entries = {}

        self.title('Edit Profile')
        self.configure(bg=DIALOG_BG)
        self.transient(master)
        self.resizable(False, False)

        self._build()
        self._centre_on(master)
        self.grab_set()
        self.bind('<Escape>', lambda _event: self.destroy())

    def _build(self):
        header = tk.Frame(self, bg=DIALOG_BG)
        header.pack(fill='x', padx=22, pady=(20, 6))
        icon_label(header, 'edit', 20, ACCENT, DIALOG_BG).pack(side='left', padx=(0, 10))
        tk.Label(header, text='Edit Profile', bg=DIALOG_BG, fg=TEXT,
                 font=('Segoe UI', 16, 'bold')).pack(side='left')

        card = tk.Frame(self, bg=CARD_BG, highlightthickness=1,
                        highlightbackground=BORDER, padx=22, pady=18)
        card.pack(fill='both', expand=True, padx=22, pady=(6, 0))

        for row, (column, label, secret) in enumerate(EDITABLE_FIELDS):
            tk.Label(card, text=label, bg=CARD_BG, fg=MUTED,
                     font=('Segoe UI', 10, 'bold'), anchor='w').grid(
                row=row, column=0, sticky='w', pady=(0, 4))
            entry = tk.Entry(card, bg=FIELD_BG, fg=TEXT, insertbackground=TEXT,
                             relief='flat', font=('Segoe UI', 11), width=34)
            if secret:
                entry.configure(show='*')
            entry.insert(0, str(self.user.get(column) or ''))
            entry.grid(row=row, column=1, sticky='ew', padx=(16, 0), pady=(0, 14), ipady=5)
            self.entries[column] = entry
        card.grid_columnconfigure(1, weight=1)

        actions = tk.Frame(self, bg=DIALOG_BG)
        actions.pack(fill='x', padx=22, pady=18)
        tk.Button(actions, text='Cancel', command=self.destroy, relief='flat', bd=0,
                  bg=FIELD_BG, fg=TEXT, activebackground=BORDER, activeforeground=TEXT,
                  font=('Segoe UI', 10, 'bold'), padx=18, pady=9,
                  cursor='hand2').pack(side='right')
        tk.Button(actions, text='Save Changes', command=self._save, relief='flat', bd=0,
                  bg=ACCENT, fg='#ffffff', activebackground=ACCENT_DARK,
                  activeforeground='#ffffff', font=('Segoe UI', 10, 'bold'),
                  padx=18, pady=9, cursor='hand2').pack(side='right', padx=(0, 10))

    def _centre_on(self, master):
        self.update_idletasks()
        try:
            root_x = master.winfo_rootx()
            root_y = master.winfo_rooty()
            root_w = master.winfo_width()
            root_h = master.winfo_height()
        except tk.TclError:
            root_x = root_y = root_w = root_h = 0
        width = self.winfo_width()
        height = self.winfo_height()
        x = root_x + max(0, (root_w - width) // 2)
        y = root_y + max(0, (root_h - height) // 3)
        self.geometry(f'+{int(x)}+{int(y)}')

    def _save(self):
        columns = list(self.entries.keys())
        values = [self.entries[column].get().strip() for column in columns]
        try:
            updated = Update_User(
                self.link, self.user, columns, values,
                ['User_id'], [self.user.get('User_id')],
            )
        except Exception as error:  # pragma: no cover - surfaced to the operator
            tkmessagebox.showerror('Edit Profile', f'Could not save changes:\n{error}',
                                   parent=self)
            return

        merged = dict(self.user)
        merged.update(dict(zip(columns, values)))
        if isinstance(updated, dict):
            merged.update(updated)
        if self.on_saved:
            self.on_saved(merged)
        tkmessagebox.showinfo('Edit Profile', 'Your profile has been updated.', parent=self)
        self.destroy()
