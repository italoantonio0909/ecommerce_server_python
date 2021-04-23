from unittest.mock import patch

from django.core.exceptions import ValidationError
from django.test import TestCase
from ecommerce.core.test_utils import fake
from ecommerce.users.services import user_create, user_password_reset


class UserPasswordResetTest(TestCase):
    def setUp(self):
        self.service = user_password_reset

    @patch('ecommerce.users.services.user_password_reset')
    def test_service_with_account_no_active(self, user_password_reset_mock):
        with self.assertRaises(ValidationError):
            email = fake.email()
            self.service(email=email)

    @patch('ecommerce.users.services.user_password_reset_notify')
    def test_service_return_token_user_and_call_event(self, user_password_reset_notify_mock):
        user = user_create(
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            password=fake.password(),
            email=fake.email()
        )

        user_profile = self.service(email=user.email)

        # Data to array list -> [<BaseUser: developer1999@gmail.com>,
        # 'alcr3d-93e02ecaf523d3332a99462eb93989fb_NQ']
        result = list(user_profile)

        # Match length result -> BaseUser -Token
        self.assertEqual(2, len(result))

        user_password_reset_notify_mock.assert_called()
