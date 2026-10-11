import json
import unittest
from unittest.mock import patch

from C import slipe


class SaleSlipPreviewSectionsTests(unittest.TestCase):
    def setUp(self):
        self.user = {"User_name": "cashier", "User_phone_num": "555"}
        self.shop = {
            "Shop_Slip_Settings": json.dumps([
                [32, 0],
                [[18], [7], [15], [17]],
            ]),
            "Shop_name": "Test Shop",
            "Shop_rules": "Sale only",
            "Shop_Adress_Information": "",
            "Shop_about": "",
            "Shop_SocLinks": "",
        }
        self.doc = {
            "doc_barcode": "PREVIEW",
            "extension_barcode": "extension_barcode",
            "At_Shop_Id": "1",
            "user_id": "1",
            "Seller_id": "",
            "customer_id": "",
            "item": json.dumps([
                [1, "C1", "B1", "Test item", "", "", "", 2, 5, 0, 0, 1],
            ]),
            "qty": 2,
            "price": 10,
            "discount": 0,
            "tax": 0,
            "payments": json.dumps([
                ["Cash", "Cash", "10", "", "", "cashier", 1, ""],
            ]),
            "pid": 10,
            "doc_created_date": "2026-10-11 17:00",
            "doc_expire_date": "2026-10-11 17:00",
            "doc_updated_date": "2026-10-11 17:00",
        }
        self.user_lookup = patch.object(
            slipe, "find_user", return_value=self.user,
        )
        self.shop_lookup = patch.object(slipe, "find_shop", return_value=None)
        self.user_lookup.start()
        self.shop_lookup.start()
        self.addCleanup(self.user_lookup.stop)
        self.addCleanup(self.shop_lookup.stop)

    def test_preview_sections_are_rendered_in_order_with_occurrence_key_overrides(self):
        sections = {
            "20:0": "Social edit\nSecond social line\n",
            "21:0": "Location edit\n",
            "22:0": "Phone Number: 555123\n",
            "15:0": "User edit\n",
            "17:0": "Customer edit\n",
            "23:0": "Cash: 10\n",
            "24:0": "10.00 EUR\n",
        }

        slip = slipe.load_slip(
            None, self.doc, 0, shop_override=self.shop,
            receipt_sections=sections,
        )

        labels = [
            "Social edit\nSecond social line",
            "Location edit",
            "Phone Number: 555123",
            "User edit",
            "Customer edit",
            "Cash: 10",
            "10.00 EUR",
        ]
        positions = [slip.index(label) for label in labels]
        self.assertEqual(positions, sorted(positions))
        self.assertIn("Social edit\nSecond social line\n", slip)
        self.assertIn("Due Date :  2026-10-11 17:00", slip)
        self.assertNotIn("User : cashier", slip)
        self.assertIn("TOTAL", slip)
        self.assertNotIn("_preview_receipt_sections", self.doc)
        self.assertIn("[[18], [7], [15], [17]]", self.shop["Shop_Slip_Settings"])

    def test_unchecked_or_empty_preview_sections_are_omitted(self):
        slip = slipe.load_slip(
            None, self.doc, 0, shop_override=self.shop,
            receipt_sections={
                "20:0": "",
                "21:0": "Only this\n",
                "23:0": "",
                "24:0": "",
            },
        )

        self.assertIn("Only this", slip)
        self.assertNotIn("Social:", slip)
        self.assertNotIn("Phone Number:", slip)
        self.assertNotIn("Total Payment:", slip)

    def test_preview_with_unconfigured_shop_uses_generated_slip_sections(self):
        self.shop["Shop_Slip_Settings"] = ""

        slip = slipe.load_slip(
            None, self.doc, 0, shop_override=self.shop,
            receipt_sections={"21:0": "Only this\n"},
        )

        self.assertIn("Test ite", slip)
        self.assertIn("Only this", slip)
        self.assertNotIn("MAMS MALL", slip)

    def test_missing_social_location_and_phone_sections_are_inserted_before_sale_sections(self):
        self.shop["Shop_Slip_Settings"] = json.dumps([
            [42, 0],
            [["6"], ["18"], ["15"]],
        ])

        slip = slipe.load_slip(
            None, self.doc, 0, shop_override=self.shop,
            receipt_sections={}, capture_sections=(captured := []),
        )

        keys = [section["key"] for section in captured]
        self.assertLess(keys.index("20:0"), keys.index("18:0"))
        self.assertLess(keys.index("21:0"), keys.index("18:0"))
        self.assertLess(keys.index("22:0"), keys.index("18:0"))
        self.assertLess(slip.index("Test ite"), slip.index("User : cashier"))

    def test_preview_keeps_item_total_payments_tax_received_balance_and_rules(self):
        self.shop["Shop_Slip_Settings"] = json.dumps([
            [42, 0],
            [["18"], ["23"], ["24"], ["19"]],
        ])
        receipt = dict(
            self.doc,
            price=20,
            discount=3,
            tax=2,
            pid=9,
        )
        receipt["payments"] = json.dumps([
            ["Cash", "Cash", "9", "", "", "cashier", 1, ""],
        ])

        slip = slipe.load_slip(
            None, receipt, 0, shop_override=self.shop, receipt_sections={},
        )

        self.assertIn("TOTAL", slip)
        self.assertIn("Test ite", slip)
        self.assertIn("Cash Cash: 9", slip)
        self.assertIn("Total: 20.00", slip)
        payment_summary_row = next(
            line for line in slip.splitlines() if "Cash Cash: 9" in line
        )
        self.assertIn("|", payment_summary_row)
        self.assertIn("Total: 20.00", payment_summary_row)
        self.assertIn("Tax: 2.00", slip)
        self.assertIn("Discount: 3.00", slip)
        self.assertIn("Received: 9.00", slip)
        self.assertIn("Balance: 10.00", slip)
        self.assertIn("Sale only", slip)

    def test_rule_formatter_keeps_checked_rows_numbered_and_omits_unchecked(self):
        self.assertEqual(
            slipe.format_slip_rules(["No returns", "Exchange in 7 days"]),
            "1. No returns\n2. Exchange in 7 days\n",
        )
        self.assertEqual(slipe.format_slip_rules(["No returns"]), "No returns\n")
        self.assertEqual(slipe.format_slip_rules([]), "")

    def test_regular_slip_keeps_legacy_item_payment_and_tax_summary(self):
        self.shop["Shop_Slip_Settings"] = json.dumps([
            [42, 0],
            [["18"]],
        ])

        slip = slipe.load_slip(
            None, self.doc, 0, shop_override=self.shop,
        )

        self.assertIn("Test ite", slip)
        self.assertIn("TOTAL", slip)
        self.assertIn("TOTAL Price", slip)
        self.assertIn("TOTAL Tax", slip)
        self.assertIn("cashier", slip)

    def test_social_links_and_location_are_read_as_individual_shop_values(self):
        self.shop["Shop_SocLinks"] = "instagram.example+facebook.example+tiktok.example"
        self.shop["Shop_Adress_Information"] = (
            "Phone Number=555-100=555-200=+Location=Market Street=City Center="
        )

        self.assertEqual(
            slipe.parse_social_links(self.shop["Shop_SocLinks"]),
            ["instagram.example", "facebook.example", "tiktok.example"],
        )
        self.assertEqual(
            slipe.get_shop_information_values(self.shop, "Location"),
            ["Market Street", "City Center"],
        )
        self.assertEqual(
            slipe.get_shop_information_values(self.shop, "Phone Number"),
            ["555-100", "555-200"],
        )
        self.assertEqual(
            slipe.get_Location(None, self.doc, 32, [], self.user, self.shop)[0],
            "* Market Street\n* City Center\n",
        )
        self.assertEqual(
            slipe.get_Social(None, self.doc, 32, [], self.user, self.shop)[0],
            "instagram.example\nfacebook.example\ntiktok.example\n",
        )

        self.shop["Shop_Slip_Settings"] = json.dumps([
            [32, 0],
            [["20"], ["21"], ["22"]],
        ])
        slip = slipe.load_slip(
            None, self.doc, 0, shop_override=self.shop, receipt_sections={},
        )
        self.assertIn(
            "instagram.example\nfacebook.example\ntiktok.example\n", slip,
        )
        self.assertIn("* Market Street\n* City Center\n", slip)
        self.assertIn(
            "Phone Number: 555-100\nPhone Number: 555-200\n", slip,
        )

    def test_duplicate_sections_get_distinct_override_keys_and_remain_ordered(self):
        self.shop["Shop_Slip_Settings"] = json.dumps([
            [32, 0],
            [["6"], ["20"], ["20"], ["18"]],
        ])
        captured = []

        slip = slipe.load_slip(
            None,
            self.doc,
            0,
            shop_override=self.shop,
            receipt_sections={"20:0": "First\nLine\n", "20:1": "Second\nLine\n"},
            capture_sections=captured,
        )

        self.assertLess(slip.index("First\nLine"), slip.index("Second\nLine"))
        self.assertEqual(
            [section["key"] for section in captured[:3]],
            ["6:0", "20:0", "20:1"],
        )
        self.assertEqual(captured[1]["text"], "First\nLine\n")
        self.assertEqual(captured[2]["text"], "Second\nLine\n")
        self.assertEqual(captured[-1]["key"], "_footer")

    def test_edited_footer_uses_final_receipt_barcode(self):
        receipt = dict(self.doc, doc_barcode="SALE-123")

        slip = slipe.load_slip(
            None,
            receipt,
            0,
            shop_override=self.shop,
            receipt_sections={"_footer": "Thank you - PREVIEW\n"},
        )

        self.assertIn("Thank you - SALE-123\n", slip)
        self.assertNotIn("Thank you - PREVIEW", slip)


if __name__ == "__main__":
    unittest.main()
