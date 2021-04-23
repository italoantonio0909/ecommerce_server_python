from unittest.mock import patch

from django.core.exceptions import ValidationError
from django.test import TestCase
from ecommerce.core.test_utils import fake
from ecommerce.products.services import category_create, product_create


class ProductCreateTest(TestCase):

    def setUp(self):
        self.category = category_create(title=fake.random_uppercase_letter())
        self.service = product_create

    @patch('ecommerce.products.services.product_create')
    def test_product_without_price_discount_higher_price(self, product_create_mock):
        with self.assertRaises(ValidationError):
            self.service(
                title=fake.bothify(text='Product Number: ????-###'),
                description=fake.bothify(text='Description Number: ????-###'),
                category=self.category.id,
                price=120,
                price_discount=150,
                is_active=True,
            )
