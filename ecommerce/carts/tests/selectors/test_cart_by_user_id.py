from unittest.mock import patch

from django.core.exceptions import ValidationError
from django.test import TestCase
from ecommerce.carts.selectors import cart_by_user_id
from ecommerce.carts.services import cart_product_create
from ecommerce.core.test_utils import fake
from ecommerce.products.services import category_create, product_create
from ecommerce.users.services import user_create
from ecommerce.core.test_utils import fake


class CartByUserIdTests(TestCase):
    def setUp(self):
        self.selector = cart_by_user_id

    @patch('ecommerce.carts.selectors.cart_by_user_id')
    def test_selector_return_nothing_with_invalid_params(self, cart_by_user_id_mock):
        # Selector return None when cart is no souch found
        result = self.selector(user_id=1)
        self.assertIsNone(result)

    @patch('ecommerce.carts.selectors.cart_by_user_id')
    def test_selector_return_cart(self, cart_by_user_id_mock):
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

        result = [self.selector(user_id=user.id)]
        expect = [cart]
        self.assertEqual(result, expect)
