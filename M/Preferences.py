import re
import tkinter as tk
from tkinter import ttk


COUNTRY_CURRENCIES = {
    'Argentina': 'ARS',
    'Australia': 'AUD',
    'Brazil': 'BRL',
    'Canada': 'CAD',
    'China': 'CNY',
    'Egypt': 'EGP',
    'Ethiopia': 'ETB',
    'France': 'EUR',
    'Germany': 'EUR',
    'India': 'INR',
    'Indonesia': 'IDR',
    'Italy': 'EUR',
    'Japan': 'JPY',
    'Kenya': 'KES',
    'Kuwait': 'KWD',
    'Malaysia': 'MYR',
    'Mexico': 'MXN',
    'Morocco': 'MAD',
    'Netherlands': 'EUR',
    'New Zealand': 'NZD',
    'Nigeria': 'NGN',
    'Norway': 'NOK',
    'Pakistan': 'PKR',
    'Qatar': 'QAR',
    'Saudi Arabia': 'SAR',
    'Singapore': 'SGD',
    'South Africa': 'ZAR',
    'South Korea': 'KRW',
    'Spain': 'EUR',
    'Sweden': 'SEK',
    'Turkey': 'TRY',
    'United Arab Emirates': 'AED',
    'United Kingdom': 'GBP',
    'United States': 'USD',
}

SUPPORTED_CURRENCIES = tuple(sorted(set(COUNTRY_CURRENCIES.values())))
THEME_NAMES = ('Blue', 'Dark', 'Green', 'Light')
THEME_LABELS = {
    'Blue': ('Dark Blue Accent', 'Professional dark mode with blue and green accents.'),
    'Dark': ('Cyberpunk Energy', 'High-contrast dark mode with energy red and bright highlights.'),
    'Green': ('Emerald Wealth', 'Financial success theme with emerald green and dark slate.'),
    'Light': ('Modern Light Surface', 'Clean bright theme for well-lit retail environments.'),
}

THEME_PALETTES = {
    'Blue': {
        'background': '#0d47a1',
        'surface': '#1565c0',
        'accent': '#1976d2',
        'accent_dark': '#0a3d91',
        'button': '#1976d2',
        'button_text': '#ffffff',
        'selected': '#22c55e',
        'text': '#ffffff',
        'panel': '#ffffff',
        'panel_text': '#111827',
    },
    'Light': {
        'background': '#f1f5f9',
        'surface': '#e2e8f0',
        'accent': '#2563eb',
        'accent_dark': '#1e40af',
        'button': '#ffffff',
        'button_text': '#0f172a',
        'selected': '#2563eb',
        'text': '#0f172a',
        'panel': '#ffffff',
        'panel_text': '#111827',
    },
    'Dark': {
        'background': '#111827',
        'surface': '#1f2937',
        'accent': '#0f766e',
        'accent_dark': '#115e59',
        'button': '#0f766e',
        'button_text': '#f9fafb',
        'selected': '#facc15',
        'text': '#f9fafb',
        'panel': '#1f2937',
        'panel_text': '#f9fafb',
    },
    'Green': {
        'background': '#064e3b',
        'surface': '#047857',
        'accent': '#10b981',
        'accent_dark': '#065f46',
        'button': '#047857',
        'button_text': '#ffffff',
        'selected': '#2563eb',
        'text': '#ffffff',
        'panel': '#ffffff',
        'panel_text': '#111827',
    },
}


def ensure_preference_columns(connection):
    required_columns = {
        'Shops': ('Shop_currency',),
        'setting': ('Theme', 'Language'),
    }
    for table_name, column_names in required_columns.items():
        existing = {row[1] for row in connection.execute(f'PRAGMA table_info({table_name})')}
        for column_name in column_names:
            if column_name not in existing:
                connection.execute(f'ALTER TABLE {table_name} ADD COLUMN {column_name} TEXT')


def currency_for_country(country):
    return COUNTRY_CURRENCIES.get(str(country or '').strip())


def resolve_shop_currency(country, currency=''):
    requested = str(currency or '').strip().upper()
    if requested:
        if not re.fullmatch(r'[A-Z]{3}', requested):
            raise ValueError('Currency must be a three-letter ISO code.')
        return requested
    return currency_for_country(country)


def format_currency(amount, currency):
    code = str(currency or '').strip().upper()
    if not re.fullmatch(r'[A-Z]{3}', code):
        return f'{float(amount):,.2f}'
    return f'{code} {float(amount):,.2f}'


def _recolor_mapped_toplevel(event, app_root):
    try:
        window = event.widget.winfo_toplevel()
        if window is app_root or not isinstance(window, tk.Toplevel):
            return
    except (tk.TclError, AttributeError):
        return

    window_key = str(window)
    pending = getattr(app_root, '_app_theme_pending_toplevels', set())
    if window_key in pending:
        return
    pending.add(window_key)
    app_root._app_theme_pending_toplevels = pending

    def apply_to_window():
        pending.discard(window_key)
        try:
            if window.winfo_exists():
                recolor = getattr(app_root, '_app_theme_recolor', None)
                if recolor:
                    recolor(window)
        except tk.TclError:
            pass

    try:
        app_root.after_idle(apply_to_window)
    except tk.TclError:
        pending.discard(window_key)


def apply_app_theme(root, theme_name):
    palette = THEME_PALETTES.get(theme_name, THEME_PALETTES['Blue'])
    style = ttk.Style(root)
    style.configure('TFrame', background=palette['background'])
    style.configure('TLabel', background=palette['background'], foreground=palette['text'])
    style.configure('TButton', background=palette['button'], foreground=palette['button_text'])
    style.map('TButton', background=[('active', palette['accent_dark'])])
    style.configure('TNotebook', background=palette['background'])
    style.configure('TNotebook.Tab', background=palette['surface'], foreground=palette['text'])
    style.map('TNotebook.Tab', background=[('selected', palette['selected'])])
    style.configure('TLabelframe', background=palette['background'], foreground=palette['text'])
    style.configure('TLabelframe.Label', background=palette['background'], foreground=palette['text'])
    style.configure('TEntry', fieldbackground=palette['panel'], foreground=palette['panel_text'])
    style.configure('TCombobox', fieldbackground=palette['panel'], foreground=palette['panel_text'])
    style.map('TCombobox', fieldbackground=[('readonly', palette['panel'])], foreground=[('readonly', palette['panel_text'])])
    style.configure('TSpinbox', fieldbackground=palette['panel'], foreground=palette['panel_text'])
    style.configure('TCheckbutton', background=palette['background'], foreground=palette['text'])
    style.configure('TRadiobutton', background=palette['background'], foreground=palette['text'])
    style.configure('Treeview', background=palette['panel'], fieldbackground=palette['panel'], foreground=palette['panel_text'])
    style.map('Treeview', background=[('selected', palette['selected'])], foreground=[('selected', palette['text'])])
    style.configure('TScrollbar', background=palette['surface'], troughcolor=palette['background'], arrowcolor=palette['text'])

    def is_light_color(color):
        try:
            value = str(color).lstrip('#')[:6]
            if len(value) != 6:
                return False
            red, green, blue = (
                int(value[index:index + 2], 16) / 255
                for index in (0, 2, 4)
            )
            return (red * 299 + green * 587 + blue * 114) / 1000 > 0.56
        except (TypeError, ValueError):
            return False

    def set_widget_colors(widget, options):
        for option, value in options.items():
            try:
                widget.configure(**{option: value})
            except (tk.TclError, TypeError):
                pass

    def recolor(widget, depth=0):
        if getattr(widget, '_preserve_app_theme_preview', False):
            return

        for attribute, value in (
            ('bg_dark', palette['background']),
            ('bg_light', palette['surface']),
            ('accent_blue', palette['accent']),
            ('bg_darker', palette['accent_dark']),
            ('text_light', palette['text']),
        ):
            if hasattr(widget, attribute):
                setattr(widget, attribute, value)

        widget_class = widget.winfo_class()
        original_background = getattr(widget, '_app_theme_original_background', None)
        if original_background is None:
            try:
                original_background = widget.cget('background')
                widget._app_theme_original_background = original_background
            except (tk.TclError, TypeError):
                original_background = ''

        background_key = str(original_background).lower()
        is_danger = background_key in ('red', '#b42318', '#912018', '#991b1b', '#dc2626')
        is_success = background_key in ('green', '#059669', '#047857', '#16a34a')
        if widget is root:
            set_widget_colors(widget, {'background': palette['background'], 'foreground': palette['text']})
        elif widget_class in ('Frame', 'TFrame', 'Labelframe', 'TLabelframe'):
            container_color = palette['background'] if depth <= 2 else palette['surface']
            set_widget_colors(widget, {'background': container_color, 'foreground': palette['text']})
        elif widget_class in ('Entry', 'TEntry', 'Text', 'Spinbox', 'TSpinbox', 'Listbox', 'Treeview', 'TCombobox'):
            set_widget_colors(widget, {
                'background': palette['panel'],
                'foreground': palette['panel_text'],
                'insertbackground': palette['panel_text'],
                'selectbackground': palette['accent'],
                'selectforeground': palette['text'],
            })
        elif widget_class in ('Button', 'TButton'):
            button_background = '#b42318' if is_danger else '#059669' if is_success else palette['button']
            button_foreground = palette['text'] if (is_danger or is_success) else palette['button_text']
            set_widget_colors(widget, {
                'background': button_background,
                'foreground': button_foreground,
                'activebackground': palette['accent_dark'] if not (is_danger or is_success) else button_background,
                'activeforeground': button_foreground,
            })
        elif widget_class in ('Scrollbar', 'TScrollbar'):
            set_widget_colors(widget, {
                'background': palette['surface'],
                'activebackground': palette['accent'],
                'troughcolor': palette['background'],
            })
        elif widget_class == 'Canvas':
            set_widget_colors(widget, {'background': palette['background']})
        elif widget_class in ('Label', 'TLabel', 'Checkbutton', 'Radiobutton', 'TCheckbutton', 'TRadiobutton'):
            parent_background = palette['background']
            try:
                parent_background = widget.master.cget('background')
            except (tk.TclError, TypeError):
                pass
            foreground = palette['panel_text'] if is_light_color(parent_background) else palette['text']
            set_widget_colors(widget, {
                'background': parent_background,
                'foreground': foreground,
                'activebackground': parent_background,
                'activeforeground': foreground,
                'selectcolor': palette['surface'],
            })
        else:
            set_widget_colors(widget, {'background': palette['surface'], 'foreground': palette['text']})

        for child in widget.winfo_children():
            recolor(child, depth + 1)

    root._app_theme_recolor = recolor
    if not getattr(root, '_app_theme_map_binding', None):
        root._app_theme_map_binding = root.bind_all(
            '<Map>',
            lambda event, app_root=root: _recolor_mapped_toplevel(event, app_root),
            add='+',
        )
    recolor(root)
    return palette