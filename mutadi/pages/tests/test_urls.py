"""Unit tests for posts app urls
"""
import pytest
from django.urls import resolve, reverse

pytestmark = pytest.mark.django_db


class TestPagesUrls:
    """Group multiple tests in Pages urls"""

    def test_home_reverse(self):
        """home should reverse to /."""
        assert reverse("home") == "/"

    def test_home_resolve(self):
        """/ should resolve to home."""
        assert resolve("/").view_name == "home"
