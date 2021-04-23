from unittest.mock import patch

from django.core.exceptions import ValidationError
from django.test import TestCase
from ecommerce.core.test_utils import fake
from ecommerce.users.models import BaseUser
from ecommerce.users.services import user_create, user_password_change


class UserPasswordChangeTest(TestCase):
    def setUp(self):
        # Use password to change
        self.password = fake.password()
        self.user = user_create(
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            password=self.password,
            email=fake.email()
        )
        self.service = user_password_change

    @patch('ecommerce.users.services.user_password_change')
    def test_user_invalid_old_password(self, user_password_change_mock):
        with self.assertRaises(ValidationError):
            password_new = fake.password()
            self.service(
                user_id=self.user.id,
                password1=password_new,
                password2=password_new,
                old_password=fake.password()
            )

    @patch('ecommerce.users.services.user_password_change')
    def test_user_not_match_passwords(self, user_password_change_mock):
        with self.assertRaises(ValidationError):
            self.service(
                user_id=self.user.id,
                password1=fake.password(),
                password2=fake.password(),
                old_password=self.password
            )

    @patch('ecommerce.users.services.user_password_change')
    def test_user_common_password(self, user_password_change_mock):
        with self.assertRaises(ValidationError):
            password_vulnerable = fake.password(length=5, digits=False)
            self.service(
                user_id=self.user.id,
                password1=password_vulnerable,
                password2=password_vulnerable,
                old_password=self.password
            )

    @patch('ecommerce.users.services.user_password_change_notify')
    def test_service_success_and_call_event(self, user_password_change_notify_mock):
        password_new = fake.password()
        self.service(
            user_id=self.user.id,
            password1=password_new,
            password2=password_new,
            old_password=self.password
        )

        user_password_change_notify_mock.assert_called()
