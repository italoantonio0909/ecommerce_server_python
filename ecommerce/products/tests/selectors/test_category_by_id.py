from django.test import TestCase
from django.core.exceptions import ValidationError

from unittest.mock import patch
from ecommerce.products.selectors import category_by_id
from ecommerce.products.services import category_create
from ecommerce.core.test_utils import fake


class ProductByIdTest(TestCase):
    def setUp(self):
        self.selector = category_by_id

    @patch('ecommerce.products.selectors.category_by_id')
    def test_selector_return_nothing(self, category_by_id_mock):
        with self.assertRaises(ValidationError):
            self.selector(category_id=fake.random_digit())

    @patch('ecommerce.products.selectors.category_by_id')
    def test_selector_return_category(self, product_by_id_mock):
        category = category_create(title=fake.bothify(
            text='Category Number: ????-###'))

        # Product data to array
        expect = [category]

        # Tranform result to array -> Category.objects.get(category_id=number)
        result = [self.selector(category_id=category.id)]

        # Match data
        self.assertEqual(expect, result)

    @patch('ecommerce.products.selectors.category_by_id')
    def test_selector_return_nothing_is_active_false(self, product_by_id_mock):
        category = category_create(title=fake.bothify(
            text='Category Number: ????-###'), is_active=False)
        with self.assertRaises(ValidationError):
            self.selector(category_id=category.id)
