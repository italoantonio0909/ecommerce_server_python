from unittest.mock import patch

from django.core.exceptions import ValidationError
from django.test import TestCase
from ecommerce.core.test_utils import fake
from ecommerce.users.models import BaseUser
from ecommerce.users.services import user_create, user_update_profile


class UserUpdateProfileTest(TestCase):
    def setUp(self):
        self.service = user_update_profile

    @patch('ecommerce.users.services.user_update_profile')
    def test_user_not_match_id(self, user_update_profile_mock):
        user = user_create(
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            password=fake.password(),
            email=fake.email()
        )
        user_new = user_create(
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            password=fake.password(),
            email=fake.email()
        )
        with self.assertRaises(ValidationError):
            data = dict()
            data['first_name'] = fake.first_name()
            self.service(
                user_session=user.id,
                user_id=user_new.id,
                data=data
            )

    @patch('ecommerce.users.services.user_update_profile_notify')
    def test_user_update_return_data_user_and_call_event(self, user_update_profile_notify_mock):
        # Create a user test
        user = user_create(
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            password=fake.password(),
            email=fake.email()
        )
        # Data with new data
        data = dict()
        data['first_name'] = fake.first_name()
        data['last_name'] = fake.last_name()

        user = self.service(
            user_session=user.id,
            user_id=user.id,
            data=data
        )

        # Match database with quantity 1
        self.assertEqual(1, BaseUser.objects.count())

        # Transform database data to array
        expect = [BaseUser.objects.first()]
        result = [user]

        # Match database and user updated
        self.assertEqual(expect, result)

        # Invoque event
        user_update_profile_notify_mock.assert_called()
