import tkinter as tk
import unittest

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

    def test_pos_panels_stack_on_narrow_windows_and_split_on_wide(self):
        layout = type('PosLayout', (), {})()
        layout.main_frame = tk.Frame(self.root)
        layout.midel_frame = tk.Frame(layout.main_frame)
        layout.buttons_frame = tk.Frame(layout.main_frame)
        layout.total_frame = tk.Frame(layout.main_frame)
        layout._pos_layout_is_narrow = None

        DisplayFrame._apply_pos_layout(layout, 900, 600)

        self.assertEqual(layout.buttons_frame.grid_info()['row'], 1)
        self.assertEqual(layout.midel_frame.grid_info()['row'], 2)
        self.assertEqual(layout.total_frame.grid_info()['row'], 3)

        DisplayFrame._apply_pos_layout(layout, 1400, 900)

        self.assertEqual(layout.midel_frame.grid_info()['column'], 0)
        self.assertEqual(layout.midel_frame.grid_info()['rowspan'], 2)
        self.assertEqual(layout.buttons_frame.grid_info()['row'], 1)
        self.assertEqual(layout.total_frame.grid_info()['row'], 2)

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
