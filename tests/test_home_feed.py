import json
import unittest

from M.Display import DisplayFrame
from M.Preferences import (
    THEME_PALETTES,
    ensure_preference_columns,
    format_currency,
    load_saved_theme,
    resolve_shop_currency,
    save_app_preferences,
)


class HomeFeedTests(unittest.TestCase):
    def test_normalize_home_product(self):
        product = {
            'id': 42,
            'name': 'Urban Windbreaker',
            'code': 'UW-100',
            'barcode': '123456789',
            'price': 249.99,
            'description': 'Lightweight windbreaker for everyday use',
            'images': '[]',
            'quantity': 12,
            'at_shop': 'Main Store',
        }

        data = DisplayFrame.normalize_home_product(product)

        self.assertEqual(data['id'], 42)
        self.assertEqual(data['name'], 'Urban Windbreaker')
        self.assertEqual(data['shop'], 'Main Store')
        self.assertEqual(data['price'], 249.99)
        self.assertGreaterEqual(data['likes'], 0)
        self.assertGreaterEqual(data['comment_count'], 0)

    def test_get_home_product_variants_uses_available_stock(self):
        more_info = [
            [
                'Main Store',
                [
                    [
                        'TJ-7',
                        [
                            ['Blue', [
                                ['M', [['TJ-7-M', '["WOMANS"]', 80, 4, 3, '', '[]', '', '']]],
                            ]],
                            ['Red', [
                                ['S', [['TJ-7-S', '[]', 80, 2, 0, '', '[]', '', '']]],
                            ]],
                        ],
                    ],
                ],
            ],
        ]
        product = {
            'id': 7,
            'name': 'Trail Jacket',
            'code': 'TJ-7',
            'barcode': 'TJ-7',
            'price': 80,
            'more_info': json.dumps(more_info),
        }

        variants = DisplayFrame.get_home_product_variants(product)

        self.assertEqual(len(variants), 1)
        self.assertEqual(variants[0]['color'], 'Blue')
        self.assertEqual(variants[0]['size'], 'M')
        self.assertEqual(variants[0]['stock'], 3)
        self.assertEqual(variants[0]['barcode'], 'TJ-7-M')
        self.assertEqual(variants[0]['type_label'], 'WOMANS')

    def test_guest_cart_items_keep_variant_and_total(self):
        product = {
            'id': 7,
            'name': 'Trail Jacket',
            'price': 80,
            '_source': {'name': 'Trail Jacket'},
        }
        variant = {
            'code': 'TJ-7',
            'barcode': 'TJ-7-M',
            'shop': 'Main Store',
            'color': 'Blue',
            'size': 'M',
            'type_value': '["WOMANS"]',
            'stock': 3,
            'price': 82,
        }

        cart_item = DisplayFrame.make_guest_cart_item(product, variant, 2)

        self.assertEqual(cart_item['color'], 'Blue')
        self.assertEqual(cart_item['size'], 'M')
        self.assertEqual(cart_item['quantity'], 2)
        self.assertEqual(DisplayFrame.guest_cart_total([cart_item]), 164)

    def test_guest_cart_merges_variant_and_respects_stock(self):
        product = {
            'id': 7,
            'name': 'Trail Jacket',
            'price': 80,
        }
        variant = {
            'code': 'TJ-7',
            'barcode': 'TJ-7-M',
            'shop': 'Main Store',
            'color': 'Blue',
            'size': 'M',
            'type_value': '',
            'stock': 3,
            'price': 80,
        }
        cart = [DisplayFrame.make_guest_cart_item(product, variant, 2)]
        another = DisplayFrame.make_guest_cart_item(product, variant, 2)

        DisplayFrame.add_guest_cart_item(cart, another)

        self.assertEqual(len(cart), 1)
        self.assertEqual(cart[0]['quantity'], 3)
        self.assertEqual(DisplayFrame.guest_cart_total(cart), 240)

    def test_shop_currency_defaults_to_country_and_formats_iso_code(self):
        self.assertEqual(resolve_shop_currency('South Africa'), 'ZAR')
        self.assertEqual(resolve_shop_currency('South Africa', 'eur'), 'EUR')
        self.assertIsNone(resolve_shop_currency('Unknown Country'))
        self.assertEqual(format_currency(1234.5, 'ZAR'), 'ZAR 1,234.50')

    def test_preference_schema_migration_is_idempotent(self):
        import sqlite3

        with sqlite3.connect(':memory:') as connection:
            connection.execute('CREATE TABLE Shops (Id INTEGER PRIMARY KEY, Shop_country TEXT)')
            connection.execute('CREATE TABLE setting (Id INTEGER PRIMARY KEY, User_id INTEGER)')

            ensure_preference_columns(connection)
            ensure_preference_columns(connection)

            shop_columns = {row[1] for row in connection.execute('PRAGMA table_info(Shops)')}
            setting_columns = {row[1] for row in connection.execute('PRAGMA table_info(setting)')}
            self.assertIn('Shop_currency', shop_columns)
            self.assertIn('Theme', setting_columns)
            self.assertIn('Language', setting_columns)

    def test_light_theme_uses_white_buttons_and_blue_selection(self):
        light = THEME_PALETTES['Light']

        self.assertEqual(light['button'], '#ffffff')
        self.assertEqual(light['button_text'], '#0f172a')
        self.assertEqual(light['selected'], '#2563eb')

    def test_theme_preference_persists_for_launch_and_user(self):
        import sqlite3

        with sqlite3.connect(':memory:') as connection:
            connection.execute('CREATE TABLE Shops (Id INTEGER PRIMARY KEY)')
            connection.execute('CREATE TABLE setting (Id INTEGER PRIMARY KEY, User_id INTEGER)')
            ensure_preference_columns(connection)

            save_app_preferences(connection, 'Dark', 'English', user_id=7)
            self.assertEqual(load_saved_theme(connection), 'Dark')
            self.assertEqual(load_saved_theme(connection, 7), 'Dark')

            save_app_preferences(connection, 'Green', 'English', user_id=8)
            self.assertEqual(load_saved_theme(connection), 'Green')
            self.assertEqual(load_saved_theme(connection, 7), 'Dark')
            self.assertEqual(load_saved_theme(connection, 8), 'Green')


if __name__ == '__main__':
    unittest.main()
