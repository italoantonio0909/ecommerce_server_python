from unittest.mock import patch

from django.core.exceptions import ValidationError
from django.test import TestCase
from ecommerce.carts.selectors import cart_get
from ecommerce.carts.services import cart_product_create
from ecommerce.core.test_utils import fake
from ecommerce.products.services import category_create, product_create
from ecommerce.users.services import user_create


class CartGetTests(TestCase):
    def setUp(self):
        self.selector = cart_get

    @patch('ecommerce.carts.selectors.cart_get')
    def test_selector_return_nothing_with_invalid_params(self, cart_get_mock):
        with self.assertRaises(ValidationError):
            self.selector(cart_id=1, user_id=1)

    @patch('ecommerce.carts.selectors.cart_get')
    def test_selector_return_cart(self, cart_get_mock):
        # Create user
        user = user_create(
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            password=fake.password(),
            email=fake.email()

        )
        # Create category
        category = category_create(title=fake.bothify(
            text='Category Number: ????-###'))

        # Create product
        product = product_create(
            title=fake.bothify(text='Product Number: ????-###'),
            description=fake.bothify(text='Description Number: ????-###'),
            price=100,
            price_discount=90,
            category=category.id
        )
        # Create cart
        cart = cart_product_create(
            user_id=user.id,
            product_id=product.id,
        )

        result = [self.selector(cart_id=cart.id, user_id=user.id)]
        expect = [cart]
        self.assertEqual(result, expect)
