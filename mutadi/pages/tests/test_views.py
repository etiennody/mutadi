"""Unit tests for pages app views
"""
import pytest
from django.urls import reverse
from model_bakery import baker
from mutadi.posts.models import Post
from pytest_django.asserts import assertTemplateUsed

pytestmark = pytest.mark.django_db


class TestPagesViews:
    """Group multiple tests in Pages views"""

    @pytest.fixture
    def proto_post(self):
        """Fixture for baked Post model."""
        return baker.make(
            Post,
            title=baker.seq("Post-"),
            content="Consequat aliqua non qui veniam sit voluptate.",
            featured=True,
            _create_files=True,
            _quantity=6,
        )

    # Home page section
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

    def test_display_posts_on_homepage_is_three(self, client, proto_post):
        """Homepage shoud display only three featured_posts nor latest_posts"""
        response = client.get(reverse("home"))
        assert response.status_code == 200
        assert (len(response.context_data["featured_posts"])) == 3
        assert (len(response.context_data["latest_posts"])) == 3

    # Terms of service section
    def test_tos_view_url_accessible_by_name(self, client):
        """Terms of service should be accessible by name."""
        url = reverse("tos")
        response = client.get(url)
        assert response.status_code == 200

    def test_valid_tos_page_title_with_client(self, client):
        """Terms of service should contain Conditions générales."""
        url = reverse("tos")
        response = client.get(url)
        assert b"Mentions l\xc3\xa9gales" in response.content

    def test_view_tos_page_uses_correct_template(self, client):
        """Terms of service should use pages/tos.html template."""
        response = client.get(reverse("tos"))
        assert response.status_code == 200
        assertTemplateUsed(response, "pages/tos.html")

    # How it works section
    def test_how_view_url_accessible_by_name(self, client):
        """How it works should be accessible by name."""
        url = reverse("how")
        response = client.get(url)
        assert response.status_code == 200

    def test_valid_how_page_title_with_client(self, client):
        """How it works should contain Conditions générales."""
        url = reverse("how")
        response = client.get(url)
        print(response.content)
        assert b"Comment \xc3\xa7a marche ?" in response.content

    def test_view_how_page_uses_correct_template(self, client):
        """How it works should use pages/how.html template."""
        response = client.get(reverse("how"))
        assert response.status_code == 200
        assertTemplateUsed(response, "pages/how.html")
