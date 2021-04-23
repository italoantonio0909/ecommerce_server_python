from collections import OrderedDict
from unittest.mock import patch

from django.core.exceptions import ValidationError
from django.test import TestCase
from ecommerce.carts.models import Cart
from ecommerce.carts.selectors import cart_product_all
from ecommerce.carts.services import cart_product_create
from ecommerce.core.test_utils import fake
from ecommerce.products.models import Product
from ecommerce.products.services import category_create, product_create
from ecommerce.users.services import user_create


class CartByUserIdTests(TestCase):
    def setUp(self):
        self.selector = cart_product_all

    @patch('ecommerce.carts.selectors.cart_product_all')
    def test_selector_return_nothing_with_no_souch_found(self, cart_product_all_mock):
        result = self.selector(cart_id=1)
        self.assertIsNone(result)

    @patch('ecommerce.carts.selectors.cart_product_all')
    def test_selector_return_products_for_user_with_that_cart(self, cart_product_all_mock):
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
        for e in range(4):
            product_create(
                title=fake.bothify(text='Product Number: ????-###'),
                description=fake.bothify(text='Description Number: ????-###'),
                price=100,
                price_discount=90,
                category=category.id

            )
        # Get all products and save ids
        products_ids = [x.id for x in Product.objects.all()]

        # Create cart
        for e in products_ids:
            cart_product_create(
                user_id=user.id,
                product_id=e
            )

        cart_id = Cart.objects.first().id
        result_selector = self.selector = cart_product_all(cart_id=cart_id)
        self.assertEqual(len(products_ids), len(result_selector))
