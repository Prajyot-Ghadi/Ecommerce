from django.test import TestCase

from accounts.models import Account
from carts.models import Cart, CartItem
from category.models import Category
from store.models import Product


class LoginCartTests(TestCase):
    def test_guest_cart_items_remain_visible_after_login(self):
        user = Account.objects.create_user(
            first_name='Test',
            last_name='User',
            username='testuser',
            email='test@example.com',
            password='test-password',
        )
        user.is_active = True
        user.save(update_fields=['is_active'])

        category = Category.objects.create(
            category_name='Test category',
            slug='test-category',
        )
        product = Product.objects.create(
            product_name='Test product',
            slug='test-product',
            price=100,
            images='test-product.jpg',
            stock=10,
            category=category,
        )

        self.client.get('/cart/')
        session = self.client.session
        guest_cart = Cart.objects.create(cart_id=session.session_key)
        cart_item = CartItem.objects.create(
            cart=guest_cart,
            product=product,
            quantity=2,
        )

        response = self.client.post(
            '/accounts/login/',
            {'email': user.email, 'password': 'test-password'},
        )

        self.assertRedirects(response, '/accounts/')
        self.assertNotEqual(self.client.session.session_key, guest_cart.cart_id)

        response = self.client.get('/cart/')

        self.assertEqual(response.status_code, 200)
        self.assertQuerySetEqual(
            response.context['cart_items'],
            [cart_item],
        )
        cart_item.refresh_from_db()
        guest_cart.refresh_from_db()
        self.assertEqual(cart_item.user, user)
        self.assertEqual(guest_cart.cart_id, self.client.session.session_key)
