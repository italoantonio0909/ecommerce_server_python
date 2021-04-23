from unittest.mock import patch

from django.core.exceptions import ValidationError
from django.test import TestCase
from ecommerce.core.test_utils import fake
from ecommerce.users.models import BaseUser
from ecommerce.users.selectors import user_by_email
from ecommerce.users.services import user_create


class UserByEmailTest(TestCase):
    def setUp(self):
        self.selector = user_by_email

    @patch('ecommerce.users.selectors.user_by_email')
    def test_selector_return_nothing(self, user_by_email_mock):
        with self.assertRaises(ValidationError):
            email_default = fake.email()
            self.selector(email=email_default)

    @patch('ecommerce.users.selectors.user_by_email')
    def test_selector_return_user(self, user_by_email):

        # Create user
        user = user_create(
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            password=fake.password(),
            email=fake.email()
        )
        self.assertEqual(1, BaseUser.objects.count())

        result_selector = self.selector(email=user.email)

        # Transform data to array -> []
        result = [result_selector]
        expect = [user]
        self.assertEqual(result, expect)
