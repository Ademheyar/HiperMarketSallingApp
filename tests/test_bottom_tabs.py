import tkinter as tk
import unittest
from unittest.mock import patch

from M.Display import BottomTabs, DisplayFrame


class BottomTabsLayoutTests(unittest.TestCase):
    def setUp(self):
        try:
            self.root = tk.Tk()
        except tk.TclError as error:
            self.skipTest(f'Tk display is unavailable: {error}')
        self.root.geometry('800x600')

    def tearDown(self):
        if hasattr(self, 'root'):
            self.root.destroy()

    def test_main_navigation_bar_remains_visible(self):
        tabs = BottomTabs(self.root)
        tabs.pack(fill='both', expand=True)
        frames = [tk.Frame(tabs.content_area) for _ in range(3)]
        for frame, title in zip(frames, ('Home', 'User Profile', 'POS Terminal')):
            tabs.add(frame, title)

        self.root.update()

        self.assertEqual(
            [item['btn'].cget('text') for item in tabs._tabs],
            ['Home', 'User Profile', 'POS Terminal'],
        )
        self.assertTrue(all(item['icon_label'].cget('text') for item in tabs._tabs))
        self.assertGreater(tabs.bar.winfo_height(), 1)
        self.assertTrue(all(item['btn'].winfo_height() > 1 for item in tabs._tabs))

    def test_selected_tab_uses_current_theme_palette(self):
        tabs = BottomTabs(self.root)
        tabs.pack(fill='both', expand=True)
        frame = tk.Frame(tabs.content_area)
        tabs.add(frame, 'Home')
        palette = {
            'background': '#101010',
            'surface': '#202020',
            'selected': '#f0f0f0',
            'accent_dark': '#303030',
            'text': '#ffffff',
            'panel_text': '#111827',
        }
        self.root._app_theme_palette = palette

        tabs._apply_app_theme_palette()

        self.assertEqual(tabs._tabs[0]['btn'].cget('bg'), palette['selected'])
        self.assertEqual(tabs._tabs[0]['btn'].cget('fg'), palette['panel_text'])

    def test_login_tab_preserves_current_content_panel(self):
        tabs = BottomTabs(self.root)
        tabs.pack(fill='both', expand=True)
        current_frame = tk.Frame(tabs.content_area)
        login_frame = tk.Frame(tabs.content_area)
        tabs.add(current_frame, 'Home')
        tabs.add(login_frame, 'Login', preserve_panel=True)
        changed_tabs = []
        tabs.on_tab_changed(lambda text, _tab_id, _frame: changed_tabs.append(text))

        tabs.select(login_frame)

        self.assertIs(tabs._current, current_frame)
        self.assertTrue(current_frame.winfo_manager())
        self.assertFalse(login_frame.winfo_manager())
        self.assertEqual(changed_tabs, ['Login'])

    def test_login_tab_does_not_open_on_startup(self):
        tabs = BottomTabs(self.root)
        tabs.pack(fill='both', expand=True)
        login_frame = tk.Frame(tabs.content_area)
        changed_tabs = []
        tabs.on_tab_changed(lambda text, _tab_id, _frame: changed_tabs.append(text))

        tabs.add(login_frame, 'Login', preserve_panel=True)

        self.assertEqual(changed_tabs, [])
        self.assertIsNone(tabs._current)

    def test_display_cleanup_removes_root_shortcut_binding(self):
        binding_owner = type('BindingOwner', (), {})()
        binding_owner.master = self.root
        binding_owner._master_binding_ids = []
        binding_owner._master_bindings_cleaned = False

        DisplayFrame._bind_master(binding_owner, '<F4>', lambda _event: None)

        self.assertTrue(self.root.bind('<F4>'))
        DisplayFrame._cleanup_master_bindings(binding_owner)

        self.assertFalse(self.root.bind('<F4>'))

    def test_pos_payment_panel_moves_below_toolbar_or_uses_quick_pay(self):
        layout = type('PosLayout', (), {})()
        layout.main_frame = tk.Frame(self.root)
        layout.top_frame = tk.Frame(layout.main_frame)
        layout.top_frame.grid(row=0, column=0, columnspan=3, sticky='nsew')
        layout.midel_frame = tk.Frame(layout.main_frame)
        layout.buttons_frame = tk.Frame(layout.top_frame)
        layout.action_buttons_frame = tk.Frame(layout.top_frame)
        layout.total_frame = tk.Frame(layout.main_frame)
        layout.buttons_frame.grid(row=1, column=0, columnspan=2, sticky='ew')
        layout.action_buttons_frame.grid(row=1, column=2, columnspan=6, sticky='ew')
        layout.quick_pay_button = tk.Button(layout.top_frame, text='Quick Pay')
        layout.main_Notebook = type('NotebookStub', (), {})()
        layout.main_Notebook.bar = tk.Frame(layout.main_frame, height=40)
        layout.main_Notebook.bar.pack_propagate(False)
        layout._pos_layout_is_narrow = None

        DisplayFrame._apply_pos_layout(layout, 899, 560)

        self.assertFalse(layout.buttons_frame.winfo_manager())
        self.assertEqual(layout.quick_pay_button.grid_info()['row'], 1)
        self.assertEqual(layout.quick_pay_button.grid_info()['column'], 0)
        self.assertEqual(layout.quick_pay_button.grid_info()['columnspan'], 2)
        self.assertEqual(layout.action_buttons_frame.grid_info()['row'], 1)
        self.assertEqual(layout.action_buttons_frame.grid_info()['column'], 2)
        self.assertEqual(layout.top_frame.grid_info()['row'], 0)
        self.assertEqual(layout.top_frame.grid_info()['column'], 0)
        self.assertEqual(layout.midel_frame.grid_info()['row'], 1)
        self.assertEqual(layout.midel_frame.grid_info()['sticky'], 'nesw')
        self.assertEqual(layout.total_frame.grid_info()['row'], 2)

        DisplayFrame._apply_pos_layout(layout, 900, 560)

        self.assertFalse(layout.quick_pay_button.winfo_manager())
        self.assertEqual(layout.buttons_frame.grid_info()['row'], 1)
        self.assertEqual(layout.buttons_frame.grid_info()['column'], 0)
        self.assertEqual(layout.buttons_frame.grid_info()['columnspan'], 2)
        self.assertEqual(layout.action_buttons_frame.grid_info()['row'], 1)
        self.assertEqual(layout.action_buttons_frame.grid_info()['column'], 2)
        self.assertEqual(layout.top_frame.grid_info()['row'], 0)
        self.assertEqual(layout.top_frame.grid_info()['column'], 0)
        self.assertEqual(layout.top_frame.grid_info()['columnspan'], 3)
        self.assertEqual(layout.total_frame.grid_info()['row'], 1)
        self.assertEqual(layout.total_frame.grid_info()['sticky'], 'nesw')
        self.assertEqual(layout.midel_frame.grid_info()['row'], 1)
        self.assertEqual(layout.midel_frame.grid_info()['column'], 0)
        self.assertEqual(layout.midel_frame.grid_info()['columnspan'], 2)
        self.assertEqual(layout.midel_frame.grid_info()['sticky'], 'nesw')
        self.assertEqual(layout.total_frame.grid_info()['column'], 2)
        self.assertEqual(
            int(layout.main_frame.grid_rowconfigure(1)['weight']),
            1,
        )
        self.assertEqual(
            int(layout.main_frame.grid_rowconfigure(2)['weight']),
            0,
        )

    def test_pos_layout_uses_available_size_not_tk_scaling(self):
        layout = type('PosLayout', (), {})()
        layout.main_frame = tk.Frame(self.root)
        layout.top_frame = tk.Frame(layout.main_frame)
        layout.top_frame.grid(row=0, column=0, columnspan=3, sticky='nsew')
        layout.midel_frame = tk.Frame(layout.main_frame)
        layout.buttons_frame = tk.Frame(layout.top_frame)
        layout.action_buttons_frame = tk.Frame(layout.top_frame)
        layout.total_frame = tk.Frame(layout.main_frame)
        layout.buttons_frame.grid(row=1, column=0, columnspan=2, sticky='ew')
        layout.action_buttons_frame.grid(row=1, column=2, columnspan=6, sticky='ew')
        layout.quick_pay_button = tk.Button(layout.top_frame, text='Quick Pay')
        layout.main_Notebook = type('NotebookStub', (), {})()
        layout.main_Notebook.bar = tk.Frame(layout.main_frame, height=40)
        layout.main_Notebook.bar.pack_propagate(False)
        layout._pos_layout_is_narrow = None

        DisplayFrame._apply_pos_layout(layout, 900, 560)

        self.assertEqual(layout.total_frame.grid_info()['column'], 2)
        self.assertEqual(layout.buttons_frame.grid_info()['column'], 0)
        self.assertEqual(layout.action_buttons_frame.grid_info()['column'], 2)
        self.assertEqual(layout.buttons_frame.grid_info()['row'], 1)
        self.assertEqual(layout.top_frame.grid_info()['column'], 0)
        self.assertFalse(layout.quick_pay_button.winfo_manager())

    def test_payment_buttons_use_one_horizontally_scrollable_row(self):
        panel = tk.Frame(
            self.root,
            width=320,
            height=60,
            bd=0,
            highlightthickness=0,
        )
        panel.pack_propagate(False)
        panel.pack()
        canvas = tk.Canvas(panel, width=320, height=46, highlightthickness=0, bd=0)
        scrollbar = tk.Scrollbar(panel, orient='horizontal', command=canvas.xview)
        canvas.configure(xscrollcommand=scrollbar.set)
        canvas.pack(side='top', fill='both', expand=True)
        inner = tk.Frame(canvas)
        canvas.create_window((0, 0), window=inner, anchor='nw')

        payment_tools = type('PaymentToolsStub', (), {
            'Shop_Payment_Tools': [
                [f'Method {index}', 'OTHER', '', str(index)]
                for index in range(6)
            ],
            'user': {},
            'Shops': [{}],
            'on_Shop': 0,
            'button_style': {
                'font': ('Arial', 10),
                'bg': '#1976d2',
                'fg': '#ffffff',
            },
            '_bind_master': lambda *_args: None,
            'payment_buttons_canvas': canvas,
            'payment_buttons_inner': inner,
            'payment_buttons_scrollbar': scrollbar,
        })()

        with patch('M.Display.Chacke_Security', return_value=True):
            buttons = DisplayFrame._populate_payment_buttons(payment_tools, inner)
        self.root.update_idletasks()
        DisplayFrame._update_payment_scrollbar(payment_tools)

        self.assertEqual(len(buttons), 6)
        self.assertTrue(all(button.grid_info()['row'] == 0 for button in buttons))
        self.assertEqual(
            [button.grid_info()['column'] for button in buttons],
            list(range(6)),
        )
        self.assertTrue(scrollbar.winfo_manager())
        self.assertEqual(panel.cget('bd'), 0)
        self.assertEqual(panel.cget('highlightthickness'), 0)

        for button in buttons[1:]:
            button.destroy()
        self.root.update_idletasks()
        DisplayFrame._update_payment_scrollbar(payment_tools)

        self.assertFalse(scrollbar.winfo_manager())

    def test_quick_pay_opens_payment_tools_dialog(self):
        host = tk.Frame(self.root, bg='#101010')
        host.pack()
        host._quick_pay_dialog = None
        host.bg_dark = '#101010'
        host.bg_light = '#202020'
        host.text_light = '#ffffff'
        host._populate_payment_buttons = lambda parent: [tk.Button(parent, text='Cash')]

        DisplayFrame.open_quick_pay(host)
        self.root.update_idletasks()

        dialog = host._quick_pay_dialog
        self.assertEqual(dialog.title(), 'Quick Pay')
        payment_panel = dialog.winfo_children()[0]
        self.assertEqual(payment_panel.cget('text'), 'Payment Tools')
        self.assertEqual(payment_panel.winfo_children()[0].cget('text'), 'Cash')

    def test_barcode_toggle_collapses_and_restores_totals(self):
        class PanelStub:
            def __init__(self):
                self.total_frame = type('FrameStub', (), {
                    'height': 250,
                    'configure': lambda frame, **options: setattr(frame, 'height', options['height']),
                    'winfo_height': lambda frame: frame.height,
                })()
                self.totals_details_frame = type('DetailsStub', (), {
                    'visible': True,
                    'grid': lambda frame: setattr(frame, 'visible', True),
                    'grid_remove': lambda frame: setattr(frame, 'visible', False),
                })()
                self._totals_full_height = 250
                self._totals_collapsed_height = 68
                self._totals_expanded = True
                self._totals_animation_id = None
                self._next_after_id = 0
                self._scheduled = {}

            def after(self, _delay, callback, *args):
                self._next_after_id += 1
                self._scheduled[self._next_after_id] = (callback, args)
                return self._next_after_id

            def after_cancel(self, after_id):
                self._scheduled.pop(after_id, None)

            def run_animation(self):
                while self._scheduled:
                    after_id = next(iter(self._scheduled))
                    callback, args = self._scheduled.pop(after_id)
                    callback(*args)

        panel = PanelStub()

        DisplayFrame.toggle_totals_panel(panel)
        panel.run_animation()

        self.assertFalse(panel._totals_expanded)
        self.assertFalse(panel.totals_details_frame.visible)
        self.assertEqual(panel.total_frame.height, 68)

        DisplayFrame.toggle_totals_panel(panel)
        panel.run_animation()

        self.assertTrue(panel._totals_expanded)
        self.assertTrue(panel.totals_details_frame.visible)
        self.assertEqual(panel.total_frame.height, 250)


if __name__ == '__main__':
    unittest.main()
