import tkinter as tk
import unittest

from M.Display import BottomTabs


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
        self.assertGreater(tabs.bar.winfo_height(), 1)
        self.assertTrue(all(item['btn'].winfo_height() > 1 for item in tabs._tabs))


if __name__ == '__main__':
    unittest.main()
