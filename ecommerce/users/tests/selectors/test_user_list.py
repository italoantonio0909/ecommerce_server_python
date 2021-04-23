from collections import OrderedDict
from unittest.mock import patch

from django.core.exceptions import ValidationError
from django.test import TestCase
from ecommerce.core.test_utils import fake
from ecommerce.users.models import BaseUser
from ecommerce.users.selectors import user_list
from ecommerce.users.services import user_create


class UserAllTest(TestCase):
    def setUp(self):
        self.selector = user_list

    @patch('ecommerce.users.selectors.user_list')
    def test_selector_return_all_user_with_empty_list_params(self, user_list_mock):
        for e in range(5):
            user_create(
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                password=fake.password(),
                email=fake.email()
            )
        # By default, the empty list contain active=True
        # Should extract all user with active=True
        result_selector = self.selector(filters={})
        self.assertNotEqual([], result_selector)

    @patch('ecommerce.users.selectors.user_list')
    def test_selector_return_data_for_user_param(self, user_list_mock):
        for e in range(3):
            user_create(
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                password=fake.password(),
                email=fake.email()
            )

        filters = OrderedDict()
        filters['id'] = BaseUser.objects.first().id
        filters['is_active'] = True
        result = self.selector(filters=filters)
        self.assertNotEqual([], list(result))
