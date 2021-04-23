from unittest.mock import patch

from django.core.exceptions import ValidationError
from django.test import TestCase
from ecommerce.carts.models import Cart
from ecommerce.carts.services import cart_product_create
from ecommerce.core.test_utils import fake
from ecommerce.products.services import category_create, product_create
from ecommerce.users.services import user_create


class CartProductCreate(TestCase):
    def setUp(self):
        # Create user custom
        self.user = user_create(
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            email=fake.email(),
            password=fake.password(),
        )

        # Category create
        self.category = category_create(
            title=fake.bothify(text='Category Number: ????-###'))

        # Product based in category
        self.product = product_create(
            title=fake.bothify(text='Product Number: ????-###'),
            description=fake.bothify(text='Description Number: ????-###'),
            price=100,
            price_discount=90,
            category=self.category.id
        )

        # Invoque service test
        self.service = cart_product_create

    @patch('ecommerce.carts.services.cart_product_create')
    def test_cart_not_exists(self, cart_product_create_mock):
        cart = self.service(
            user_id=self.user.id,
            product_id=self.product.id
        )

        # Total objects carts
        self.assertEqual(1, Cart.objects.count())

        # Cart match with first cart saved
        self.assertEqual(cart, Cart.objects.first())

    @patch('ecommerce.carts.services.cart_product_create')
    def test_cart_exists(self, cart_product_create_mock):

        # Create product
        product_new = product_create(
            title=fake.bothify(text='Product Number: ????-###'),
            description=fake.bothify(text='Description Number: ????-###'),
            price=100,
            price_discount=90,
            category=self.category.id
        )

        # Create cart session user
        cart = self.service(
            user_id=self.user.id,
            product_id=self.product.id
        )

        # Match total objects with carts quantity
        self.assertEqual(1, Cart.objects.count())

        # Add product to cart with new product
        self.service(
            user_id=self.user.id,
            product_id=product_new.id
        )

        self.assertEqual(1, Cart.objects.count())

    @patch('ecommerce.carts.services.cart_product_create')
    def test_cart_product_already_exists(self, cart_product_create_mock):

        # Create cart session user
        cart = self.service(
            user_id=self.user.id,
            product_id=self.product.id
        )

        self.assertEqual(1, Cart.objects.count())

        with self.assertRaises(ValidationError):
            # Add same product to cart
            self.service(
                user_id=self.user.id,
                product_id=self.product.id
            )
