from unittest.mock import patch

from django.core.exceptions import ValidationError
from django.test import TestCase
from ecommerce.carts.models import Cart
from ecommerce.carts.services import cart_product_create, cart_product_delete
from ecommerce.core.test_utils import fake
from ecommerce.products.models import Product
from ecommerce.products.services import category_create, product_create
from ecommerce.users.services import user_create


class CartProductDelete(TestCase):
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
            title=fake.bothify(text='Category Number: ????-########'))

        self.product = product_create(
            title=fake.bothify(text='Product Number: ????-########'),
            description=fake.bothify(text='Description Number: ????-########'),
            price=100,
            price_discount=90,
            category=self.category.id
        )

        self.product_new = product_create(
            title=fake.bothify(text='Product Number: ????-########'),
            description=fake.bothify(text='Description Number: ????-########'),
            price=100,
            price_discount=90,
            category=self.category.id
        )

        self.service = cart_product_delete

    @patch('ecommerce.carts.services.cart_product_delete')
    def test_product_not_exists_in_cart(self, cart_product_delete_mock):

        # Create cart
        cart = cart_product_create(
            user_id=self.user.id,
            product_id=self.product.id
        )

        with self.assertRaises(ValidationError):
            # Delete product not exists in cart
            self.service(
                user_id=self.user.id,
                product_id=self.product_new.id,
                cart_id=cart.id,
            )

    @patch('ecommerce.carts.services.cart_product_delete')
    def test_product_remove_in_cart(self, cart_product_delete_mock):
        # List comprehension ids products -> [1,2...]
        products = [x.id for x in Product.objects.all()]

        # Iterator in products and create order
        for e in products:
            cart_product_create(
                user_id=self.user.id,
                product_id=e
            )

        self.assertEqual(1, Cart.objects.count())

        # Delete first product cart
        card_id = Cart.objects.first().id
        result_service = self.service(
            user_id=self.user.id,
            product_id=products[0],
            cart_id=card_id
        )

        result = result_service.products.all()
        self.assertEqual(1, len(result))
