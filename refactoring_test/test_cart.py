import unittest
from cart_module import calc_ord

class TestCartModule(unittest.TestCase):
    def setUp(self):
        self.valid_user = {
            'age': 25,
            'reg_days': 100,
            'is_blocked': False
        }
        self.items = [
            {'id': '1', 'name': 'Ноутбук', 'price': 50000.0, 'qty': 1, 'cat': 'tech'},
            {'id': '2', 'name': 'Мышь', 'price': 1000.0, 'qty': 2, 'cat': 'accessories'}
        ]

    def test_successful_calculation_without_discounts(self):
        res = calc_ord(self.valid_user, self.items, d_code="")
        self.assertIsNotNone(res)
        self.assertEqual(res['subtotal'], 52000.0)
        self.assertEqual(res['discount'], 0.0)
        self.assertEqual(res['tax'], 10400.0)  # 20%
        self.assertEqual(res['total'], 62400.0)

    def test_sale10_promo_code(self):
        res = calc_ord(self.valid_user, self.items, d_code="SALE10")
        self.assertIsNotNone(res)
        self.assertEqual(res['subtotal'], 52000.0)
        self.assertEqual(res['discount'], 5200.0)  # 10%
        self.assertEqual(res['total'], 56160.0)

    def test_spring5_promo_code(self):
        res = calc_ord(self.valid_user, self.items, d_code="SPRING5")
        self.assertIsNotNone(res)
        self.assertEqual(res['discount'], 2600.0)  # 5%

    def test_promo_items_prevent_promo_code(self):
        items_with_promo = self.items + [
            {'id': '3', 'name': 'Акционный коврик', 'price': 500.0, 'qty': 1, 'cat': 'promo'}
        ]
        res = calc_ord(self.valid_user, items_with_promo, d_code="SALE10")
        # Скидка по промокоду не должна примениться
        self.assertEqual(res['discount'], 0.0)

    def test_vip_and_loyalty_discount(self):
        loyal_user = {
            'age': 30,
            'reg_days': 500,  # > 365 -> +100 руб
            'is_blocked': False
        }
        res = calc_ord(loyal_user, self.items, d_code="", vip=True)
        # VIP: 52000 * 0.07 = 3640. Лояльность: +100 -> 3740.0
        self.assertEqual(res['discount'], 3740.0)

    def test_blocked_user_returns_none(self):
        blocked_user = {'age': 25, 'reg_days': 50, 'is_blocked': True}
        res = calc_ord(blocked_user, self.items, d_code="")
        self.assertIsNone(res)

    def test_underage_user_returns_none(self):
        kid_user = {'age': 16, 'reg_days': 10, 'is_blocked': False}
        res = calc_ord(kid_user, self.items, d_code="")
        self.assertIsNone(res)

    def test_empty_cart_returns_none(self):
        res = calc_ord(self.valid_user, [], d_code="")
        self.assertIsNone(res)

    def test_invalid_item_price_returns_none(self):
        bad_items = [{'id': '1', 'name': 'Флешка', 'price': -100.0, 'qty': 1, 'cat': 'tech'}]
        res = calc_ord(self.valid_user, bad_items, d_code="")
        self.assertIsNone(res)

if __name__ == '__main__':
    unittest.main()
