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

    def test_tos_reverse(self):
        """Terms of service should reverse to /."""
        assert reverse("tos") == "/tos/"

    def test_tos_resolve(self):
        """/ should resolve to Terms of service."""
        assert resolve("/tos/").view_name == "tos"
