"""Unit tests for posts app views
"""
import pytest
from django.urls import reverse
from pytest_django.asserts import assertTemplateUsed

pytestmark = pytest.mark.django_db


class TestPagesViews:
    """Group multiple tests in Pages views"""

    def test_view_url_home_page_exists_at_desired_location(self, client):
        """Home page should exist at desired location."""
        response = client.get("/")
        assert response.status_code == 200

    def test_view_url_accessible_by_name(self, client):
        """Home page should be accessible by name."""
        url = reverse("home")
        response = client.get(url)
        assert response.status_code == 200

    def test_valid_home_page_title_with_client(self, client):
        """Home page should contain Accueil."""
        url = reverse("home")
        response = client.get(url)
        assert "Accueil" in str(response.content)

    def test_view_home_page_uses_correct_template(self, client):
        """Home page should use pages/home.html template."""
        response = client.get(reverse("home"))
        assert response.status_code == 200
        assertTemplateUsed(response, "pages/home.html")
