"""Unit tests for posts app views
"""
import pytest
from django.urls import reverse

pytestmark = pytest.mark.django_db


class TestPagesViews:
    """Group multiple tests in Pages views"""

    def test_valid_home_page_status_code_views(self, client):
        """Test if the status code for home page is 200 and exists."""
        url = reverse("home")
        response = client.get(url)
        assert response.status_code == 200