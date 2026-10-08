import tkinter as tk
from tkinter import ttk

PROFILE_THEME = {
    'bg': '#0b1726',
    'card_bg': '#132238',
    'card_border': '#22344f',
    'row_bg': '#182942',
    'text': '#f8fafc',
    'muted': '#8fa3bd',
    'accent': '#2f80ed',
    'accent_dark': '#1c65c9',
    'danger': '#e23b4e',
    'danger_dark': '#b91c2c',
}

_BACKGROUND_COLORS = {
    '#0d47a1': PROFILE_THEME['bg'],
    '#0a3d91': PROFILE_THEME['bg'],
    '#0b1726': PROFILE_THEME['bg'],
    '#0f172a': PROFILE_THEME['bg'],
    '#f3f4f6': PROFILE_THEME['bg'],
    '#1565c0': PROFILE_THEME['card_bg'],
    '#132238': PROFILE_THEME['card_bg'],
    '#ffffff': PROFILE_THEME['card_bg'],
    '#fff': PROFILE_THEME['card_bg'],
    '#f9fafb': PROFILE_THEME['card_bg'],
    '#f1f5f9': PROFILE_THEME['card_bg'],
    '#f8fafc': PROFILE_THEME['card_bg'],
    '#1976d2': PROFILE_THEME['accent'],
    '#2f80ed': PROFILE_THEME['accent'],
    '#1d4ed8': PROFILE_THEME['accent'],
    '#2563eb': PROFILE_THEME['accent'],
    '#047857': PROFILE_THEME['accent'],
    '#0f766e': PROFILE_THEME['accent'],
    '#115e59': PROFILE_THEME['accent'],
    '#e5e7eb': PROFILE_THEME['row_bg'],
    '#e2e8f0': PROFILE_THEME['row_bg'],
    '#182942': PROFILE_THEME['row_bg'],
    '#991b1b': PROFILE_THEME['danger_dark'],
    '#b91c1c': PROFILE_THEME['danger'],
    '#fee2e2': PROFILE_THEME['danger_dark'],
}

_FOREGROUND_COLORS = {
    '#000000': PROFILE_THEME['text'],
    '#000': PROFILE_THEME['text'],
    '#111827': PROFILE_THEME['text'],
    '#1f2937': PROFILE_THEME['text'],
    '#374151': PROFILE_THEME['text'],
    '#0f172a': PROFILE_THEME['text'],
    '#1d4ed8': PROFILE_THEME['text'],
    '#2563eb': PROFILE_THEME['text'],
    '#991b1b': PROFILE_THEME['text'],
    '#b91c1c': PROFILE_THEME['text'],
    '#e2e8f0': PROFILE_THEME['text'],
    '#f8fafc': PROFILE_THEME['text'],
    '#0f766e': PROFILE_THEME['text'],
    '#115e59': PROFILE_THEME['text'],
    '#ffffff': PROFILE_THEME['text'],
    '#fff': PROFILE_THEME['text'],
    '#0b1726': PROFILE_THEME['text'],
    '#132238': PROFILE_THEME['text'],
    '#182942': PROFILE_THEME['text'],
    '#6b7280': PROFILE_THEME['muted'],
    '#64748b': PROFILE_THEME['muted'],
    '#9ca3af': PROFILE_THEME['muted'],
}


def apply_profile_theme(widget):
    """Apply the shared dark profile-card theme to a Tk widget tree."""
    try:
        if hasattr(widget.winfo_toplevel(), '_app_theme_name'):
            return
    except tk.TclError:
        pass

    try:
        style = ttk.Style(widget.winfo_toplevel())
    except Exception:
        style = ttk.Style()

    style.theme_use('clam')
    style.configure('.', background=PROFILE_THEME['bg'], foreground=PROFILE_THEME['text'], borderwidth=0)
    style.configure('Profile.TFrame', background=PROFILE_THEME['card_bg'])
    style.configure('Profile.Card.TFrame', background=PROFILE_THEME['card_bg'], borderwidth=1, relief='flat')
    style.configure('Profile.TLabel', background=PROFILE_THEME['card_bg'], foreground=PROFILE_THEME['text'])
    style.configure('Profile.Primary.TButton', background=PROFILE_THEME['accent'], foreground=PROFILE_THEME['text'], borderwidth=0, relief='flat', padding=(12, 8))
    style.map('Profile.Primary.TButton', background=[('active', PROFILE_THEME['accent_dark'])], foreground=[('active', PROFILE_THEME['text'])])
    style.configure('Profile.Secondary.TButton', background=PROFILE_THEME['row_bg'], foreground=PROFILE_THEME['text'], borderwidth=0, relief='flat', padding=(12, 8))
    style.map('Profile.Secondary.TButton', background=[('active', PROFILE_THEME['card_border'])], foreground=[('active', PROFILE_THEME['text'])])
    style.configure('Profile.Danger.TButton', background=PROFILE_THEME['danger'], foreground=PROFILE_THEME['text'], borderwidth=0, relief='flat', padding=(12, 8))
    style.map('Profile.Danger.TButton', background=[('active', PROFILE_THEME['danger_dark'])], foreground=[('active', PROFILE_THEME['text'])])
    style.configure('TEntry', fieldbackground=PROFILE_THEME['row_bg'], foreground=PROFILE_THEME['text'], insertcolor=PROFILE_THEME['text'])
    style.configure('TCombobox', fieldbackground=PROFILE_THEME['row_bg'], foreground=PROFILE_THEME['text'], arrowcolor=PROFILE_THEME['text'])
    style.map('TCombobox', fieldbackground=[('readonly', PROFILE_THEME['row_bg'])], foreground=[('readonly', PROFILE_THEME['text'])])
    style.configure('TSpinbox', fieldbackground=PROFILE_THEME['row_bg'], foreground=PROFILE_THEME['text'], arrowcolor=PROFILE_THEME['text'])
    style.configure('TCheckbutton', background=PROFILE_THEME['bg'], foreground=PROFILE_THEME['text'])
    style.map('TCheckbutton', background=[('active', PROFILE_THEME['bg'])], foreground=[('active', PROFILE_THEME['text'])])
    style.configure('TRadiobutton', background=PROFILE_THEME['bg'], foreground=PROFILE_THEME['text'])
    style.map('TRadiobutton', background=[('active', PROFILE_THEME['bg'])], foreground=[('active', PROFILE_THEME['text'])])
    style.configure('TLabelFrame', background=PROFILE_THEME['card_bg'], foreground=PROFILE_THEME['text'])
    style.configure('TLabelFrame.Label', background=PROFILE_THEME['card_bg'], foreground=PROFILE_THEME['text'])
    style.configure('Treeview', background=PROFILE_THEME['card_bg'], fieldbackground=PROFILE_THEME['card_bg'], foreground=PROFILE_THEME['text'], rowheight=28)
    style.map('Treeview', background=[('selected', PROFILE_THEME['accent'])], foreground=[('selected', PROFILE_THEME['text'])])
    style.configure('Treeview.Heading', background=PROFILE_THEME['row_bg'], foreground=PROFILE_THEME['text'], relief='flat')
    style.map('Treeview.Heading', background=[('active', PROFILE_THEME['card_border'])])


def apply_profile_widget_theme(widget, recursive=False):
    """Translate legacy light/blue widget colors into the shared profile palette."""
    try:
        background = str(widget.cget('background')).lower()
    except tk.TclError:
        background = ''

    themed_background = _BACKGROUND_COLORS.get(background)
    if themed_background:
        widget.configure(background=themed_background)
        background = themed_background

    try:
        foreground = str(widget.cget('foreground')).lower()
    except tk.TclError:
        foreground = ''

    if background in PROFILE_THEME.values():
        themed_foreground = _FOREGROUND_COLORS.get(foreground)
        if themed_foreground:
            widget.configure(foreground=themed_foreground)

    for option in ('activebackground', 'highlightbackground', 'selectcolor', 'selectbackground'):
        try:
            color = str(widget.cget(option)).lower()
        except tk.TclError:
            continue
        themed_color = _BACKGROUND_COLORS.get(color)
        if themed_color:
            widget.configure(**{option: themed_color})

    for option in ('activeforeground', 'disabledforeground', 'insertbackground'):
        try:
            color = str(widget.cget(option)).lower()
        except tk.TclError:
            continue
        themed_color = _FOREGROUND_COLORS.get(color)
        if themed_color:
            widget.configure(**{option: themed_color})

    if recursive:
        for child in widget.winfo_children():
            apply_profile_widget_theme(child, recursive=True)
