from unittest.mock import patch

from django.core.exceptions import ValidationError
from django.test import TestCase
from ecommerce.core.test_utils import fake
from ecommerce.products.selectors import product_by_id
from ecommerce.products.services import category_create, product_create


class ProductByIdTest(TestCase):
    def setUp(self):

        self.selector = product_by_id

    @patch('ecommerce.products.selectors.product_by_id')
    def test_selector_return_nothing(self, product_by_id_mock):
        with self.assertRaises(ValidationError):
            self.selector(product_id=fake.random_digit())

    @patch('ecommerce.products.selectors.product_by_id')
    def test_selector_return_product(self, product_by_id_mock):
        category = category_create(
            title=fake.bothify(text='Category Number: ????-###'))

        product = product_create(
            title=fake.bothify(text='Product Number: ????-###'),
            description=fake.bothify(text='Description Number: ????-###'),
            price=100,
            price_discount=90,
            category=category.id
        )

        # Product data to array
        expect = [product]

        # Tranform result to array -> Product.objects.get(product_id=number)
        result = [self.selector(product_id=product.id)]

        # Match data
        self.assertEqual(expect, result)

    @patch('ecommerce.products.selectors.product_by_id')
    def test_selector_return_nothing_is_active_false(self, product_by_id_mock):
        category = category_create(
            title=fake.bothify(text='Category Number: ????-###'))

        product = product_create(
            title=fake.bothify(text='Product Number: ????-###'),
            description=fake.bothify(text='Description Number: ????-###'),
            price=100,
            price_discount=90,
            category=category.id,
            is_active=False
        )

        with self.assertRaises(ValidationError):
            self.selector(product_id=product.id)
