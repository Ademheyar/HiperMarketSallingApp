"""Construction test for :class:`M.UserProfilePanel`.

Runs headless: it builds the panel against a small stub application object,
switches between the three sub-sections and asserts the summary values the
panel derives from a user row.
"""
import os
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

import tkinter as tk

from M.ProfileData import build_summary, count_items
from M.UserProfile import UserProfilePanel


class StubApp:
    def __init__(self):
        self.user = {
            'User_id': 7,
            'User_name': 'AH Adem',
            'User_fname': 'Adem',
            'User_Lname': 'Heyar',
            'User_type': 'Cashier',
            'User_country': 'South Africa',
            'User_address': 'Johannesburg',
            'User_email': 'adem@example.com',
            'User_likes': 'a|b|c',
            'User_following_shop': '[1, 2, 3]',
            'User_favoraite_items': 'x,y',
        }
        self.Shops = [{
            'Shop_Id': 1,
            'Shop_name': 'Hiper Mart',
            'Shop_brand_name': 'Hiper Mart',
            'Shop_country': 'South Africa',
        }]
        self.on_Shop = 0
        self.Link = ''
        self.can_manage = True
        self.pos_calls = 0
        self.manager_calls = 0

    def go_to_pos(self):
        self.pos_calls += 1

    def go_to_manager(self):
        self.manager_calls += 1

    def sign_out(self):
        pass


def test_count_items():
    assert count_items('[1, 2, 3]') == 3
    assert count_items('a|b|c') == 3
    assert count_items('x,y') == 2
    assert count_items('') == 0
    assert count_items(None) == 0


def test_build_summary():
    app = StubApp()
    summary = build_summary(app.user, app.Shops, app.on_Shop)
    assert summary['handle'] == '@AH Adem'
    assert summary['full_name'] == 'Adem Heyar'
    assert summary['role'] == 'Cashier'
    assert summary['shop_name'] == 'Hiper Mart'
    assert summary['following'] == 3
    assert summary['likes'] == 3
    assert summary['saved'] == 2


def test_panel_constructs_and_switches():
    try:
        root = tk.Tk()
    except tk.TclError:
        print('SKIP: no display available for Tk')
        return
    root.withdraw()
    app = StubApp()
    panel = UserProfilePanel(root, app)
    panel.pack()
    root.update_idletasks()
    assert 'Messages' in panel.sections
    assert 'Notif' in panel.sections
    assert 'History' in panel.sections
    panel._select_section('Notif')
    assert panel.active_section == 'Notif'
    panel._select_section('History')
    assert panel.active_section == 'History'
    panel.refresh()
    root.update_idletasks()
    root.destroy()
    print('OK: profile panel constructed and section switching works')


if __name__ == '__main__':
    test_count_items()
    test_build_summary()
    test_panel_constructs_and_switches()
    print('All profile data tests passed')
