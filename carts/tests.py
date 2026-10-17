from django.test import TestCase


class EmptyCartViewTests(TestCase):
    def test_cart_page_renders_when_cart_does_not_exist(self):
        response = self.client.get('/cart/')

        self.assertEqual(response.status_code, 200)
        self.assertQuerySetEqual(response.context['cart_items'], [])
        self.assertEqual(response.context['total'], 0)
        self.assertEqual(response.context['quantity'], 0)
        self.assertEqual(response.context['tax'], 0)
        self.assertEqual(response.context['grand_total'], 0)

    def test_checkout_page_renders_when_cart_does_not_exist(self):
        response = self.client.get('/cart/checkout/')

        self.assertEqual(response.status_code, 200)
        self.assertQuerySetEqual(response.context['cart_items'], [])
        self.assertEqual(response.context['total'], 0)
        self.assertEqual(response.context['quantity'], 0)
        self.assertEqual(response.context['tax'], 0)
        self.assertEqual(response.context['grand_total'], 0)
