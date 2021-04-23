from collections import OrderedDict
from unittest.mock import patch

from django.core.exceptions import ValidationError
from django.test import TestCase
from ecommerce.carts.services import (billing_profile_create,
                                      cart_product_create)
from ecommerce.core.test_utils import fake
from ecommerce.orders.selectors import order_list
from ecommerce.orders.services import order_create
from ecommerce.products.services import category_create, product_create
from ecommerce.users.services import user_create


class OrderByIdTest(TestCase):
    def setUp(self):
        # Create user
        self.user = user_create(
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            password=fake.password(),
            email=fake.email()
        )
        # Create category
        self.category = category_create(
            title=fake.bothify(text='Category Number: ????-###'))
        # Create product
        self.product = product_create(
            title=fake.bothify(text='Product Number: ????-###'),
            description=fake.bothify(text='Description Number: ????-###'),
            price=100,
            price_discount=90,
            category=self.category.id
        )
        # Create order
        self.cart = cart_product_create(
            user_id=self.user.id,
            product_id=self.product.id
        )
        # Create billing profile
        self.billing = billing_profile_create(user_id=self.user.id)
        # Create order
        self.order = order_create(
            shipping_total=0.00,
            billing_profile_id=self.billing.id,
            shipping_address_id=None,
            billing_address_id=None,
            shipping_address_final=None,
            billing_address_final=None,
            cart_id=self.cart.id,
            total=0.00,
            status='created',
            is_active=True
        )

        self.selector = order_list

    @patch('ecommerce.orders.selectors.order_list')
    def test_return_all_order_when_filter_empty(self, order_list_mock):
        result = list(self.selector(filters=None))
        self.assertNotEqual([], result)

    @patch('ecommerce.orders.selectors.order_list')
    def test_return_order_with_param(self, order_list_mock):

        # Filter data
        # Fields avaibles id, is_active, cart_id
        filter = OrderedDict()
        filter['id'] = self.order.id
        filter['cart_id'] = self.cart.id
        filter['is_active'] = True

        result = list(self.selector(filters=filter))
        self.assertEqual(1, len(result))

    @patch('ecommerce.orders.selectors.order_list')
    def test_return_nothing_with_invalid_param(self, order_list_mock):

        # Filter data
        # Fields avaibles id, is_active, cart_id
        filter = OrderedDict()
        filter['id'] = fake.random_digit()

        result = list(self.selector(filters=filter))
        self.assertEqual([], result)
