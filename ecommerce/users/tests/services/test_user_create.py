from unittest.mock import patch

from django.core.exceptions import ValidationError
from django.test import TestCase, override_settings
from ecommerce.core.test_utils import fake
from ecommerce.users.models import BaseUser
from ecommerce.users.services import user_create


class UserCreateTest(TestCase):
    def setUp(self):
        self.service = user_create

    @patch('ecommerce.users.services.user_create')
    def test_user_with_unusable_password(self, user_create_mock):
        user = self.service(
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            password=None,
            email=fake.email()
        )

        self.assertFalse(user.has_usable_password())

    @patch('ecommerce.users.services.user_create')
    def test_user_with_vulnerable_password(self, user_create_mock):
        """Validate password with common cases:
           UserAttributeSimilarityValidator
           MinimumLengthValidator
           CommonPasswordValidator
           NumericPasswordValidator

        """
        with self.assertRaises(ValidationError):
            user = self.service(
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                password=fake.password(length=5, digits=False),
                email=fake.email()
            )

    @patch('ecommerce.users.services.user_create')
    def test_user_with_capitalize_email_cannot_created(self, user_create_mock):
        # Generate email and apply upper joseph76@torres.biz -> JOSEPH76@TORRES.BIZ
        email = fake.email()
        email_upper = email.upper()

        self.service(
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            password=fake.password(),
            email=email
        )

        with self.assertRaises(ValidationError):
            self.service(
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                password=fake.password(),
                email=email_upper
            )

        self.assertEqual(1, BaseUser.objects.count())

    @patch('ecommerce.users.services.user_create_notify')
    def test_user_create_and_call_event(self, user_create_notify_mock):
        self.service(
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            password=fake.password(),
            email=fake.email()
        )

        user_create_notify_mock.assert_called()
