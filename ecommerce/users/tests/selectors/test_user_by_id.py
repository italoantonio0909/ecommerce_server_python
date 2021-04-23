from unittest.mock import patch

from django.core.exceptions import ValidationError
from django.test import TestCase
from ecommerce.users.models import BaseUser
from ecommerce.users.selectors import user_by_id
from ecommerce.users.services import user_create
from ecommerce.core.test_utils import fake


class UserByIdTest(TestCase):
    def setUp(self):
        self.selector = user_by_id

    @patch('ecommerce.users.selectors.user_by_id')
    def test_selector_return_nothing(self, user_by_id_mock):
        with self.assertRaises(ValidationError):
            self.selector(user_id=fake.random_digit())

    @patch('ecommerce.users.selectors.user_by_id')
    def test_selector_return_user(self, user_by_id):

        # Create user
        user = user_create(
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            password=fake.password(),
            email=fake.email()
        )
        self.assertEqual(1, BaseUser.objects.count())

        result_selector = self.selector(user_id=user.id)

        # Transform data to array -> []
        result = [result_selector]
        expect = [user]
        self.assertEqual(result, expect)
