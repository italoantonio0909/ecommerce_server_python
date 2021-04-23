from unittest.mock import patch

from django.core.exceptions import ValidationError
from django.test import TestCase
from ecommerce.billing.selectors import billing_profile_by_user_id
from ecommerce.billing.services import billing_profile_create
from ecommerce.core.test_utils import fake
from ecommerce.users.services import user_create


class BillingProfileByIdTest(TestCase):
    def setUp(self):
        self.selector = billing_profile_by_user_id

    @patch('ecommerce.billing.selectors.billing_profile_by_user_id')
    def test_selector_return_nothing_with_invalid_param(self, billing_profile_by_user_id_mock):
        result = self.selector(user_id=fake.random_digit())
        self.assertIsNone(result)

    @patch('ecommerce.billing.selectors.billing_profile_by_user_id')
    def test_selector_return_billing_profile_for_user_id_param(self, billing_profile_by_user_id_mock):
        # Create user
        user = user_create(
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            password=fake.password(),
            email=fake.email()
        )
        # Create billing profile
        billing_profile = billing_profile_create(user_id=user.id)

        result_selector = self.selector(user_id=user.id)
        # Transform data <QuerySet[BillingProfile]> to array -> []
        result = [result_selector]
        expect = [billing_profile]
        self.assertEqual(result, expect)
