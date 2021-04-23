from collections import OrderedDict
from unittest.mock import patch

from django.core.exceptions import ValidationError
from django.test import TestCase
from ecommerce.carts.selectors import cart_list
from ecommerce.carts.services import cart_product_create
from ecommerce.core.test_utils import fake
from ecommerce.products.services import category_create, product_create
from ecommerce.users.services import user_create


class CartByUserIdTests(TestCase):
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
        # Create cart
        self.cart = cart_product_create(
            user_id=self.user.id,
            product_id=self.product.id,
        )
        self.selector = cart_list

    @patch('ecommerce.carts.selectors.cart_list')
    def test_selector_return_all_carts_when_list_params_empty(self, cart_list_mock):
        result_selector = self.selector(filters={})
        result = list(result_selector)
        self.assertNotEqual([], result)

    @patch('ecommerce.carts.selectors.cart_list')
    def test_selector_return_data_with_params_valid(self, cart_list_mock):
        filters = OrderedDict()
        filters['user'] = self.user.id
        filters['is_active'] = True
        result_selector = self.selector(filters=filters)
        result = list(result_selector)
        expect = [self.cart]
        self.assertEqual(result, expect)
