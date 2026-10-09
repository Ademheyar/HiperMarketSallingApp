"""Rich profile panel for a signed-in staff member.

The panel reproduces the account screen used across the app: handle and
verification badge, avatar with a coloured ring, follower/like/saved counters,
name and role details, the POS / Manage / Edit Profile actions, a sign-out
button and the Messages / Notif / History tabs, all rendered in the dark blue
theme the rest of the desktop UI uses.
"""
import os
import tkinter as tk
from tkinter import ttk

from PIL import Image, ImageDraw, ImageTk

from C.API.Get import fetch_as_dict_list
from M.UITheme import PROFILE_THEME, apply_profile_theme
from M.ProfileData import (
    build_messages,
    build_summary,
    format_history_rows,
)
from D.Veaw_Notifications import Veaw_Notifications
from M.ProfileEdit import ProfileEditDialog
from M.ProfileIcons import draw_icon, icon_label

MAIN_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

BG = '#0b1726'
CARD_BG = '#132238'
CARD_BORDER = '#22344f'
ROW_BG = '#182942'
TEXT = '#f8fafc'
MUTED = '#8fa3bd'
ACCENT = '#2f80ed'
ACCENT_DARK = '#1c65c9'
DANGER = '#e23b4e'
DANGER_DARK = '#b91c2c'

AVATAR_SIZE = 116
RING_WIDTH = 6
RING_STOPS = ((0.0, '#3fb950'), (0.45, '#2f80ed'), (0.8, '#2f80ed'), (1.0, '#f0883e'))

SECTIONS = (
    ('Messages', 'chat'),
    ('Notif', 'bell'),
    ('History', 'clock'),
)


def _hex_to_rgb(color):
    value = color.lstrip('#')
    return tuple(int(value[index:index + 2], 16) for index in (0, 2, 4))


def _rgb_to_hex(rgb):
    return '#%02x%02x%02x' % tuple(rgb)


def _gradient_color(position, stops):
    position = min(max(position, 0.0), 1.0)
    for index in range(len(stops) - 1):
        start_pos, start_color = stops[index]
        end_pos, end_color = stops[index + 1]
        if start_pos <= position <= end_pos:
            if end_pos == start_pos:
                return start_color
            ratio = (position - start_pos) / (end_pos - start_pos)
            start_rgb = _hex_to_rgb(start_color)
            end_rgb = _hex_to_rgb(end_color)
            return _rgb_to_hex([
                int(start_rgb[channel] + (end_rgb[channel] - start_rgb[channel]) * ratio)
                for channel in range(3)
            ])
    return stops[-1][1]


class UserProfilePanel(tk.Frame):
    """Account panel for the user currently signed in."""

    def __init__(self, parent, app):
        tk.Frame.__init__(self, parent, bg=BG)
        apply_profile_theme(self)
        self.app = app
        self.summary = build_summary(
            getattr(app, 'user', None) or {},
            getattr(app, 'Shops', None) or [],
            getattr(app, 'on_Shop', 0),
        )
        self.sections = {}
        self.section_tabs = {}
        self.active_section = SECTIONS[0][0]
        self._avatar_photo = None
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.build()
        self._apply_app_theme_palette()

    # ------------------------------------------------------------------ build
    def build(self):
        root = tk.Frame(self, bg=BG)
        root.pack(fill='both', expand=True, padx=20, pady=18)
        root.columnconfigure(0, weight=1)
        root.rowconfigure(1, weight=1)

        card = tk.Frame(root, bg=CARD_BG, highlightthickness=1,
                        highlightbackground=CARD_BORDER, padx=26, pady=24)
        card.grid(row=0, column=0, sticky='ew')
        card.columnconfigure(0, weight=1)

        self._build_identity(card)
        self._build_counters(card)
        self._build_details(card)
        self._build_actions(card)
        self._build_sign_out(card)

        content = tk.Frame(root, bg=BG)
        content.grid(row=1, column=0, sticky='nsew', pady=(18, 0))
        content.columnconfigure(0, weight=1)
        self.content = content
        self._build_sections(content)
        self._select_section(self.active_section)

        self.section_navigation = tk.Frame(root, bg=BG)
        self.section_navigation.grid(row=2, column=0, sticky='ew', pady=(12, 0))
        self._build_section_tabs(self.section_navigation)

    def _build_identity(self, card):
        header = tk.Frame(card, bg=CARD_BG)
        header.grid(row=0, column=0, sticky='ew')
        tk.Label(header, text=self.summary['handle'], bg=CARD_BG, fg=TEXT,
                 font=('Segoe UI', 20, 'bold')).pack(side='left')
        icon_label(header, 'verified', 20, ACCENT, CARD_BG).pack(side='left', padx=(9, 0))

    def _build_counters(self, card):
        body = tk.Frame(card, bg=CARD_BG)
        body.grid(row=1, column=0, sticky='ew', pady=(16, 0))

        avatar_holder = tk.Frame(body, bg=CARD_BG)
        avatar_holder.pack(side='left')
        self._render_avatar(avatar_holder)

        stats = tk.Frame(body, bg=CARD_BG)
        stats.pack(side='left', fill='x', expand=True, padx=(28, 0))
        counters = (
            (self.summary['following'], 'Following'),
            (self.summary['likes'], 'Likes'),
            (self.summary['saved'], 'Saved'),
        )
        for column, (value, label) in enumerate(counters):
            cell = tk.Frame(stats, bg=CARD_BG)
            cell.grid(row=0, column=column, sticky='nsew', padx=(0, 24))
            tk.Label(cell, text=str(value), bg=CARD_BG, fg=TEXT,
                     font=('Segoe UI', 18, 'bold')).pack()
            tk.Label(cell, text=label, bg=CARD_BG, fg=MUTED,
                     font=('Segoe UI', 10)).pack(pady=(2, 0))
            stats.columnconfigure(column, weight=1)

    def _build_details(self, card):
        tk.Label(card, text=self.summary['full_name'], bg=CARD_BG, fg=TEXT,
                 font=('Segoe UI', 15, 'bold'), anchor='w').grid(
            row=2, column=0, sticky='w', pady=(20, 10))

        details = tk.Frame(card, bg=CARD_BG)
        details.grid(row=3, column=0, sticky='ew')

        top_row = tk.Frame(details, bg=CARD_BG)
        top_row.pack(fill='x', pady=3)
        self._icon_text(top_row, 'briefcase', 'Role: ' + self.summary['role'])
        tk.Label(top_row, text=' | ', bg=CARD_BG, fg=CARD_BORDER,
                 font=('Segoe UI', 11)).pack(side='left')
        shop_holder = tk.Frame(top_row, bg=CARD_BG)
        shop_holder.pack(side='left')
        icon_label(shop_holder, 'store', 16, MUTED, CARD_BG).pack(side='left', padx=(0, 8))
        shop_names = [shop.get('Shop_name', '') for shop in getattr(self.app, 'Shops', [])]
        self.shop_selector = ttk.Combobox(
            shop_holder,
            values=shop_names,
            state='readonly',
            width=18,
        )
        self.shop_selector.pack(side='left')
        selected_shop = getattr(self.app, 'on_Shop', 0)
        if shop_names:
            if not isinstance(selected_shop, int) or not 0 <= selected_shop < len(shop_names):
                selected_shop = 0
            self.shop_selector.current(selected_shop)
        self.shop_selector.bind('<<ComboboxSelected>>', self._on_shop_selected)

        bottom_row = tk.Frame(details, bg=CARD_BG)
        bottom_row.pack(fill='x', pady=3)
        self._icon_text(bottom_row, 'pin', 'Location: ' + self.summary['location'])
        tk.Label(bottom_row, text=' | ', bg=CARD_BG, fg=CARD_BORDER,
                 font=('Segoe UI', 11)).pack(side='left')
        self._icon_text(bottom_row, 'mail', self.summary['email'])

        if self.summary['about']:
            tk.Label(card, text=self.summary['about'], bg=CARD_BG, fg=MUTED,
                     font=('Segoe UI', 10), anchor='w', justify='left',
                     wraplength=560).grid(row=4, column=0, sticky='w', pady=(8, 0))

    def _icon_text(self, parent, kind, text):
        holder = tk.Frame(parent, bg=CARD_BG)
        holder.pack(side='left')
        icon_label(holder, kind, 16, MUTED, CARD_BG).pack(side='left', padx=(0, 8))
        tk.Label(holder, text=text, bg=CARD_BG, fg=TEXT,
                 font=('Segoe UI', 11)).pack(side='left')
        return holder

    def _build_actions(self, card):
        row = tk.Frame(card, bg=CARD_BG)
        row.grid(row=5, column=0, sticky='ew', pady=(20, 0))
        row.columnconfigure((0, 1, 2), weight=1, uniform='actions')

        pos = self._pill_button(row, 'pos', 'POS', ACCENT, ACCENT_DARK, '#ffffff',
                                self.app.go_to_pos)
        pos.grid(row=0, column=0, sticky='ew', padx=(0, 10))

        manage = self._pill_button(row, 'shield', 'Manage', ROW_BG, '#2c4262', TEXT,
                                   self.app.go_to_manager)
        manage.grid(row=0, column=1, sticky='ew', padx=(0, 10))
        self.manage_action = manage

        edit = self._pill_button(row, 'edit', 'Edit Profile', ROW_BG, '#2c4262', TEXT,
                                 self.open_edit_dialog)
        edit.grid(row=0, column=2, sticky='ew')

    def _on_shop_selected(self, _event=None):
        index = self.shop_selector.current()
        if index < 0:
            return
        select_shop = getattr(self.app, 'select_shop', None)
        if callable(select_shop):
            select_shop(index)
        else:
            self.app.on_Shop = index

    def _build_sign_out(self, card):
        row = tk.Frame(card, bg=CARD_BG)
        row.grid(row=6, column=0, sticky='ew', pady=(12, 0))
        row.columnconfigure(0, weight=1)
        button = self._pill_button(row, 'logout', 'Sign Out / Log Out',
                                   DANGER, DANGER_DARK, '#ffffff', self.app.sign_out)
        button.grid(row=0, column=0, sticky='ew')

    def _build_section_tabs(self, card):
        self.section_separator = tk.Frame(card, bg=CARD_BORDER, height=1)
        self.section_separator.pack(fill='x', pady=(0, 12))
        tabs = tk.Frame(card, bg=BG)
        tabs.pack(fill='x')
        self.section_tabs_frame = tabs
        for column, (name, kind) in enumerate(SECTIONS):
            tabs.columnconfigure(column, weight=1)
            self.section_tabs[name] = self._section_tab(tabs, column, name, kind)

    def _pill_button(self, parent, kind, text, bg, hover_bg, fg, command, enabled=True):
        frame = tk.Frame(parent, bg=bg, padx=12, pady=11,
                         cursor='hand2' if enabled else 'arrow')
        inner = tk.Frame(frame, bg=bg)
        inner.pack()
        icon = icon_label(inner, kind, 16, fg, bg)
        icon.pack(side='left', padx=(0, 9))
        label = tk.Label(inner, text=text, bg=bg, fg=fg,
                         font=('Segoe UI', 11, 'bold'))
        label.pack(side='left')

        widgets = (frame, inner, icon, label)

        def colors(hover=False):
            palette = getattr(self.winfo_toplevel(), '_app_theme_palette', None)
            if not palette:
                return (hover_bg if hover else bg), fg
            if kind == 'logout':
                return (DANGER_DARK if hover else DANGER), '#ffffff'
            if kind == 'pos':
                return (
                    palette['accent_dark'] if hover else palette['button'],
                    palette['button_text'],
                )
            return (
                palette['accent_dark'] if hover else palette['surface'],
                palette['text'] if enabled else ('#64748b' if palette['background'] == '#f1f5f9' else MUTED),
            )

        def paint(hover=False):
            color, foreground = colors(hover)
            frame.configure(bg=color)
            inner.configure(bg=color)
            icon.configure(bg=color)
            icon.delete('all')
            draw_icon(
                icon, kind, 16, foreground,
                icon.winfo_reqwidth() / 2,
                icon.winfo_reqheight() / 2,
            )
            label.configure(bg=color, fg=foreground)

        def on_enter(_event):
            if enabled:
                paint(hover=True)

        def on_leave(_event):
            if enabled:
                paint()

        def on_click(_event):
            if enabled:
                command()

        for widget in widgets:
            widget.bind('<Enter>', on_enter)
            widget.bind('<Leave>', on_leave)
            widget.bind('<Button-1>', on_click)
        frame._apply_app_theme_palette = lambda palette: paint()
        paint()
        return frame

    def _section_tab(self, parent, column, name, kind):
        tab = tk.Frame(parent, bg=CARD_BG, cursor='hand2')
        tab.grid(row=0, column=column, sticky='nsew')
        icon = icon_label(tab, kind, 22, MUTED, CARD_BG)
        icon.pack()
        label = tk.Label(tab, text=name, bg=CARD_BG, fg=MUTED,
                         font=('Segoe UI', 10, 'bold'))
        label.pack(pady=(6, 0))

        def on_click(_event):
            self._select_section(name)

        for widget in (tab, icon, label):
            widget.bind('<Button-1>', on_click)
        return {'frame': tab, 'icon': icon, 'label': label, 'kind': kind}

    # --------------------------------------------------------------- sections
    def _build_sections(self, parent):
        self.sections['Messages'] = self._build_messages(parent)
        self.sections['Notif'] = self._build_notifications(parent)
        self.sections['History'] = self._build_history(parent)
        for frame in self.sections.values():
            frame.pack_forget()

    def _select_section(self, name):
        if name not in self.sections:
            return
        self.active_section = name
        palette = getattr(self.winfo_toplevel(), '_app_theme_palette', None)
        accent = palette['accent'] if palette else ACCENT
        muted = '#64748b' if palette and palette['background'] == '#f1f5f9' else MUTED
        for frame in self.sections.values():
            frame.pack_forget()
        self.sections[name].pack(fill='both', expand=True)
        for section_name, tab in self.section_tabs.items():
            color = accent if section_name == name else muted
            tab['icon'].delete('all')
            draw_icon(tab['icon'], tab['kind'], 22, color,
                      tab['icon'].winfo_reqwidth() / 2,
                      tab['icon'].winfo_reqheight() / 2)
            tab['label'].configure(fg=color)

    def _apply_app_theme_palette(self, palette=None):
        if palette is None:
            palette = getattr(self.winfo_toplevel(), '_app_theme_palette', None)
        if not palette or not hasattr(self, 'section_navigation'):
            return

        background = palette['background']
        text = palette['text']
        muted = '#64748b' if background == '#f1f5f9' else MUTED
        self.configure(bg=background)
        self.section_navigation.configure(bg=background)
        self.section_tabs_frame.configure(bg=background)
        self.section_separator.configure(bg=palette['surface'])
        for name, tab in self.section_tabs.items():
            tab['frame'].configure(bg=background)
            tab['icon'].configure(bg=background)
            tab['label'].configure(
                bg=background,
                fg=palette['accent'] if name == self.active_section else muted,
            )
            tab['icon'].delete('all')
            draw_icon(
                tab['icon'], tab['kind'], 22,
                palette['accent'] if name == self.active_section else muted,
                tab['icon'].winfo_reqwidth() / 2,
                tab['icon'].winfo_reqheight() / 2,
            )

    def open_edit_dialog(self):
        ProfileEditDialog(
            self, getattr(self.app, 'user', None) or {},
            getattr(self.app, 'Link', '') or '',
            on_saved=self._on_profile_saved,
        )

    def _on_profile_saved(self, updated_user):
        self.app.user = updated_user
        self.refresh()

    def refresh(self):
        self.summary = build_summary(
            getattr(self.app, 'user', None) or {},
            getattr(self.app, 'Shops', None) or [],
            getattr(self.app, 'on_Shop', 0),
        )
        for child in self.winfo_children():
            child.destroy()
        self.sections = {}
        self.section_tabs = {}
        self.build()
        self._apply_app_theme_palette()

    def _section_heading(self, parent, kind, title):
        heading = tk.Frame(parent, bg=BG)
        heading.pack(fill='x', pady=(0, 10))
        icon_label(heading, kind, 20, ACCENT, BG).pack(side='left', padx=(0, 10))
        tk.Label(heading, text=title, bg=BG, fg=TEXT,
                 font=('Segoe UI', 14, 'bold')).pack(side='left')

    def _empty_state(self, parent, text):
        tk.Label(parent, text=text, bg=BG, fg=MUTED,
                 font=('Segoe UI', 11), anchor='w', justify='left').pack(fill='x', pady=8)

    def _person_badge(self, parent, size=42):
        canvas = tk.Canvas(parent, width=size, height=size, bg=BG,
                           highlightthickness=0, bd=0)
        canvas.create_oval(1, 1, size - 1, size - 1, fill=ACCENT, outline='')
        head = size * 0.22
        canvas.create_oval(size / 2 - head / 2, size * 0.24,
                           size / 2 + head / 2, size * 0.24 + head,
                           fill='#ffffff', outline='')
        canvas.create_arc(size * 0.24, size * 0.56, size * 0.76, size * 1.02,
                          start=0, extent=180, fill='#ffffff', outline='')
        return canvas

    def _chat_row(self, parent, sender, preview):
        card = tk.Frame(parent, bg=CARD_BG, highlightthickness=1,
                        highlightbackground=CARD_BORDER, padx=14, pady=12)
        card.pack(fill='x', pady=6)
        self._person_badge(card, 42).pack(side='left', padx=(0, 12))
        text_holder = tk.Frame(card, bg=CARD_BG)
        text_holder.pack(side='left', fill='x', expand=True)
        tk.Label(text_holder, text=sender, bg=CARD_BG, fg=ACCENT,
                 font=('Segoe UI', 11, 'bold'), anchor='w').pack(fill='x')
        tk.Label(text_holder, text=preview, bg=CARD_BG, fg=TEXT,
                 font=('Segoe UI', 10), anchor='w', justify='left',
                 wraplength=520).pack(fill='x', pady=(3, 0))

    def _build_messages(self, parent):
        frame = tk.Frame(parent, bg=BG)
        self._section_heading(frame, 'chat', 'Messages & Chats')
        shop_rows = getattr(self.app, 'Shops', None) or []
        for message in build_messages(self.summary, shop_rows):
            self._chat_row(frame, message['sender'], message['preview'])
        return frame

    def _build_notifications(self, parent):
        frame = tk.Frame(parent, bg=BG)
        shop_rows = getattr(self.app, 'Shops', None) or []
        self.notifications_viewer = Veaw_Notifications(
            frame,
            getattr(self.app, 'user', None) or {},
            shop_rows,
            app=self.app,
        )
        self.notifications_viewer.pack(fill='both', expand=True)
        return frame

    def _load_history_rows(self):
        user_id = self.summary.get('user_id')
        if user_id in (None, ''):
            return []
        try:
            rows = fetch_as_dict_list(
                getattr(self.app, 'Link', '') or '',
                'SELECT * FROM doc_table WHERE user_id=? OR Seller_id=? ORDER BY id DESC LIMIT 25',
                (user_id, user_id),
            )
        except Exception:
            rows = []
        return rows or []

    def _build_history(self, parent):
        frame = tk.Frame(parent, bg=BG)
        self._section_heading(frame, 'clock', 'History')
        shop_rows = getattr(self.app, 'Shops', None) or []
        history = format_history_rows(
            self._load_history_rows(), shop_rows, getattr(self.app, 'on_Shop', 0),
        )
        if not history:
            self._empty_state(frame, 'No recorded orders for this account yet.')
            return frame
        for entry in history:
            card = tk.Frame(frame, bg=CARD_BG, highlightthickness=1,
                            highlightbackground=CARD_BORDER, padx=14, pady=12)
            card.pack(fill='x', pady=6)
            top = tk.Frame(card, bg=CARD_BG)
            top.pack(fill='x')
            tk.Label(top, text='Receipt ' + entry['barcode'], bg=CARD_BG, fg=TEXT,
                     font=('Segoe UI', 11, 'bold'), anchor='w').pack(side='left')
            tk.Label(top, text=entry['amount'], bg=CARD_BG, fg=ACCENT,
                     font=('Segoe UI', 11, 'bold'), anchor='e').pack(side='right')
            tk.Label(card, text=entry['date'], bg=CARD_BG, fg=MUTED,
                     font=('Segoe UI', 9), anchor='w').pack(fill='x', pady=(3, 0))
        return frame

    # ------------------------------------------------------------------ avatar
    def _avatar_image_path(self):
        name = str(self.summary.get('user_name') or '').strip()
        if name:
            candidate = os.path.join(MAIN_dir, 'data', 'Users', name, 'ProfileImage.jpg')
            if os.path.exists(candidate):
                return candidate
        return os.path.join(MAIN_dir, 'data', 'Icon', 'no_Profile_image.jpg')

    def _render_avatar(self, parent):
        outer = AVATAR_SIZE + RING_WIDTH * 2
        canvas = tk.Canvas(parent, width=outer, height=outer, bg=CARD_BG,
                           highlightthickness=0, bd=0)
        canvas.pack()

        centre = outer / 2
        radius = AVATAR_SIZE / 2
        steps = 72
        segment = 360 / steps
        for index in range(steps):
            color = _gradient_color(index / steps, RING_STOPS)
            canvas.create_arc(
                centre - radius, centre - radius, centre + radius, centre + radius,
                start=90 - index * segment, extent=-segment,
                style='arc', outline=color, width=RING_WIDTH,
            )

        image = self._load_circular_avatar(AVATAR_SIZE)
        self._avatar_photo = image
        canvas.create_image(centre, centre, image=image)

    def _load_circular_avatar(self, size):
        try:
            portrait = Image.open(self._avatar_image_path()).convert('RGBA')
            portrait = portrait.resize((size, size), Image.Resampling.LANCZOS)
        except Exception:
            portrait = Image.new('RGBA', (size, size), (28, 47, 74, 255))
        mask = Image.new('L', (size, size), 0)
        ImageDraw.Draw(mask).ellipse((0, 0, size - 1, size - 1), fill=255)
        portrait.putalpha(mask)
        return ImageTk.PhotoImage(portrait)
