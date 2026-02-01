from django.test import TestCase
from moba_ai_analysis.utils import validate_username

# Unit tests for validator classes or methods
class ValidatorsTests(TestCase):
    def setUp(self):
        print("Set up validators")
    
    def test_validate_username_happy_case(self):
        result = validate_username("validUsername")
        self.assertTrue(result)

    def test_validate_username_negative_case(self):
        result = validate_username("invalid#Username")
        self.assertFalse(result)