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
        """/posts/post_list/ should resolve to post_list."""
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

    def test_add_post_reverse(self):
        """add_post should reverse to /posts/add_post/."""
        assert reverse("add_post") == "/posts/add_post/"

    def test_add_post_resolve(self):
        """/posts/add_post/ should resolve to add_post."""
        assert resolve("/posts/add_post/").view_name == "add_post"

    def test_update_post_reverse(self, proto_post):
        """update_post should reverse to /posts/update_post/post.pk."""
        assert (
            reverse(
                "update_post",
                args=[
                    f"{proto_post.pk}",
                ],
            )
            == f"/posts/post_detail/edit/{proto_post.pk}"
        )

    def test_update_post_resolve(self, proto_post):
        """/posts/update_post/post.pk should resolve to update_post."""
        assert (
            resolve(f"/posts/post_detail/edit/{proto_post.pk}").view_name
            == "update_post"
        )
