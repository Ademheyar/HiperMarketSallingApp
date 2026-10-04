import unittest

from M.Display import DisplayFrame


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


if __name__ == '__main__':
    unittest.main()
