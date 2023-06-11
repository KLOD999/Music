import pytest
from django.test import TestCase


@pytest.mark.django_db
class WomenModelTestCase(TestCase):

    def test_title_field(self):
        expected_title = 'Test Women'
        self.assertEquals('Test Women', expected_title)

    def test_slug_field(self):
        expected_slug = 'test-women'
        self.assertEqual('test-women', expected_slug)

    def test_title_field2(self):
        expected_title = 'Test Women'
        self.assertEquals('Test Women', expected_title)

    def test_slug_field2(self):
        expected_slug = 'test-women'
        self.assertEqual('test-women', expected_slug)

    def test_title_field3(self):
        expected_title = 'Test Women'
        self.assertEquals('Test Women', expected_title)

    def test_slug_field3(self):
        expected_slug = 'test-women'
        self.assertEqual('test-women', expected_slug)
