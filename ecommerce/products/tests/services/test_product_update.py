from unittest.mock import patch

from django.core.exceptions import ValidationError
from django.test import TestCase
from ecommerce.core.test_utils import fake
from ecommerce.products.services import (category_create, product_create,
                                         product_update)


class ProductUpdateTest(TestCase):
    def setUp(self):
        self.category = category_create(
            title=fake.bothify(text='Category Number: ????-###'))
        self.product = product_create(
            title=fake.bothify(text='Product Number: ????-###'),
            description=fake.bothify(text='Description Number: ????-###'),
            category=self.category.id,
            price=130,
            price_discount=120,
            is_active=True,
        )
        self.service = product_update

    @patch('ecommerce.products.services.product_update')
    def test_product_without_price_discount_higher_price(self, product_create_mock):
        with self.assertRaises(ValidationError):
            data = dict()
            data['price_discount'] = 150
            self.service(
                product_id=self.product.id,
                data=data
            )
