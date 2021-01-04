"""Unit tests for posts app urls"""
import pytest
from django.urls import resolve, reverse
from model_bakery import baker
from mutadi.posts.models import Category, Post

pytestmark = pytest.mark.django_db


class TestPostsUrls:
    """Group multiple tests for Posts urls."""

    @pytest.fixture
    def proto_category(self):
        """Fixture for baked Category model."""
        return baker.make(Category)

    @pytest.fixture
    def proto_post(self):
        """Fixture for baked Post model."""
        return baker.make(
            Post,
            content=(
                "Cupidatat duis commodo aliqua adipisicing "
                "mollit consequat mollit cupidatat ad adipisicing."
            ),
        )

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

    def test_delete_post_reverse(self, proto_post):
        """delete_post should reverse to /posts/delete_post/post.pk."""
        assert (
            reverse(
                "delete_post",
                args=[
                    f"{proto_post.pk}",
                ],
            )
            == f"/posts/post_detail/{proto_post.pk}/remove"
        )

    def test_delete_post_resolve(self, proto_post):
        """/posts/delete_post/post.pk should resolve to delete_post."""
        assert (
            resolve(f"/posts/post_detail/{proto_post.pk}/remove").view_name
            == "delete_post"
        )

    def test_category_posts_reverse(self, proto_category):
        """
        category should reverse to
        /posts/category/proto_post.categories__title.
        """
        assert (
            reverse(
                "category",
                args=[
                    f"{proto_category.title}",
                ],
            )
            == f"/posts/category/{proto_category.title}/"
        )

    def test_category_posts_resolve(self, proto_category):
        """
        /posts/category/proto_post.categories__title
        should resolve to category.
        """
        assert (
            resolve(f"/posts/category/{proto_category.title}/").view_name
            == "category"
        )

    def test_search_results_posts_reverse(self):
        """
        search_results should reverse to /posts/search/.
        """
        assert (reverse("search_results")) == "/posts/search/"

    def test_search_posts_resolve(self):
        """
        /posts/search/ should resolve to search_results.
        """
        assert resolve("/posts/search/").view_name == "search_results"
