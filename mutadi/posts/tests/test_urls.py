"""Unit tests for posts app urls
"""
import pytest
from django.urls import resolve, reverse
from model_bakery import baker
from mutadi.posts.models import Post

pytestmark = pytest.mark.django_db


class TestPostsUrls:
    """Group multiple tests for Posts urls"""

    @pytest.fixture
    def proto_post(self):
        """Fixture for baked User model."""
        return baker.make(Post)

    def test_post_list_reverse(self):
        """post_list should reverse to /posts/post_list/."""
        assert reverse("post_list") == "/posts/post_list/"

    def test_post_list_resolve(self):
        """/posts/register/ should resolve to post_list."""
        assert resolve("/posts/post_list/").view_name == "post_list"

    def test_post_detail_reverse(self, proto_post):
        """post_detail should reverse to /posts/post_detail/post.pk."""
        assert (
            reverse(
                "post_detail",
                args=[
                    f"{proto_post.pk}",
                ],
            )
            == f"/posts/post_detail/{proto_post.pk}"
        )

    def test_post_detail_resolve(self, proto_post):
        """/posts/post_detail/post.pk should resolve to post_detail."""
        assert (
            resolve(f"/posts/post_detail/{proto_post.pk}").view_name
            == "post_detail"
        )
