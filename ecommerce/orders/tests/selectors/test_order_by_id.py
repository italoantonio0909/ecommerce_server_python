from unittest.mock import patch

from django.core.exceptions import ValidationError
from django.test import TestCase
from ecommerce.carts.services import (billing_profile_create,
                                      cart_product_create)
from ecommerce.core.test_utils import fake
from ecommerce.orders.selectors import order_by_id
from ecommerce.orders.services import order_create
from ecommerce.products.services import category_create, product_create
from ecommerce.users.services import user_create


class OrderByIdTest(TestCase):
    def setUp(self):
        self.selector = order_by_id

    @patch('ecommerce.orders.selectors.order_by_id')
    def test_selector_return_nothing(self, order_by_id_mock):
        with self.assertRaises(ValidationError):
            self.selector(order_id=None)

    @patch('ecommerce.orders.selectors.order_by_id')
    def test_selector_return_order(self, order_by_id_mock):
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
        # Create order
        cart = cart_product_create(
            user_id=user.id,
            product_id=product.id
        )
        # Create billing profile
        billing = billing_profile_create(user_id=user.id)
        # Create order
        order = order_create(
            shipping_total=0.00,
            billing_profile_id=billing.id,
            shipping_address_id=None,
            billing_address_id=None,
            shipping_address_final=None,
            billing_address_final=None,
            cart_id=cart.id,
            total=0.00,
            status='created',
            is_active=True
        )
        result = [self.selector(order_id=order.id)]
        expect = [order]

        self.assertEqual(result, expect)
