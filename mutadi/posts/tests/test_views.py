"""Unit tests for posts app views
"""
import pytest
from django.urls import reverse
from model_bakery import baker
from mutadi.posts.models import Post
from pytest_django.asserts import assertTemplateUsed

pytestmark = pytest.mark.django_db


class TestPostlistViews:
    """Group multiple tests in Postlist views"""

    def test_view_url_post_list_page_exists_at_desired_location(self, client):
        """post_list page should exist at desired location."""
        response = client.get("/posts/post_list/")
        assert response.status_code == 200

    def test_view_url_accessible_by_name(self, client):
        """post_list page should be accessible by name."""
        url = reverse("post_list")
        response = client.get(url)
        assert response.status_code == 200

    def test_valid_post_list_page_title_with_client(self, client):
        """post_list page should contain "Publications"."""
        url = reverse("post_list")
        response = client.get(url)
        assert "Publications" in str(response.content)

    def test_view_post_list_page_uses_correct_template(self, client):
        """post_list page should use post_list.html template."""
        response = client.get(reverse("post_list"))
        assert response.status_code == 200
        assertTemplateUsed(response, "post_list.html")


class TestPostDetailViews:
    """Group multiple tests in PostDetail views"""

    @pytest.fixture
    def proto_post(self):
        """Fixture for baked User model."""
        return baker.make(Post, _create_files=True)

    def test_view_url_post_detail_page_exists_at_desired_location(
        self, client, proto_post
    ):
        """post_detail page should exist at desired location."""
        response = client.get(f"/posts/post_detail/{proto_post.pk}")
        assert response.status_code == 200

    def test_view_url_accessible_by_name(self, client, proto_post):
        """post_detail page should be accessible by name."""
        url = reverse(
            "post_detail",
            args=[
                f"{proto_post.pk}",
            ],
        )
        response = client.get(url)
        assert response.status_code == 200

    def test_valid_post_detail_page_title_with_client(
        self, client, proto_post
    ):
        """post_detail page should contain the title of the post."""
        url = reverse(
            "post_detail",
            args=[
                f"{proto_post.pk}",
            ],
        )
        response = client.get(url)
        assert proto_post.title in str(response.content)

    def test_view_post_detail_page_uses_correct_template(
        self, client, proto_post
    ):
        """post_detail page should use post_detail.html template."""
        url = reverse(
            "post_detail",
            args=[
                f"{proto_post.pk}",
            ],
        )
        response = client.get(url)
        assert response.status_code == 200
        assertTemplateUsed(response, "post_detail.html")
