"""Unit tests for posts app models
"""
import pytest
from model_bakery import baker

from mutadi.posts.models import Category, Comment, Post

pytestmark = pytest.mark.django_db


class TestCategoryModel:
    """Group multiple tests in Category model"""

    @pytest.fixture
    def category(self):
        """Fixture for baked Category model."""
        return baker.make(Category)

    def test_using_category(self, category):
        """Function should be using fixture of Category baked model."""
        assert isinstance(category, Category)

    def test___str__category_model(self, category):
        """__str__() method should be the category title."""
        assert category.__str__() == category.title
        assert str(category) == category.title

    def test_verbose_name_plural_categories(self):
        """verbose_name_plural should be categories."""
        assert Category._meta.verbose_name_plural == "categories"

    def test_title_label(self, category):
        """Title label name should be title."""
        field_label = category._meta.get_field("title").verbose_name
        assert field_label == "title"

    def test_title_max_length(self, category):
        """Max length for title field should be 20."""
        max_length = category._meta.get_field("title").max_length
        assert max_length == 20


class TestCommentModel:
    """Group multiple tests in Comment Model"""

    @pytest.fixture
    def comment(self):
        """Fixture for baked Category model."""
        return baker.make(Comment)

    def test_using_comment(self, comment):
        """Function should be using fixture of Comment baked model."""
        assert isinstance(comment, Comment)

    def test___str__comment_model(self, comment):
        """__str__() should be the username of user."""
        assert comment.__str__() == comment.user.username
        assert str(comment) == comment.user.username

    def test_content_label(self, comment):
        """Content label name should be content."""
        field_label = comment._meta.get_field("content").verbose_name
        assert field_label == "content"


class TestPostModel:
    """Group multiple tests in Post Model"""

    @pytest.fixture
    def post(self):
        """Fixture for baked Post model."""
        return baker.make(Post, make_m2m=True)

    def test_using_post(self, post):
        """Function should be using fixture of Post baked model."""
        assert isinstance(post, Post)

    def test__str__post_model(self, post):
        """__str__() method should be title and author of a post."""
        assert post.__str__() == post.title + " | " + str(post.author)
        assert str(post) == post.title + " | " + str(post.author)

    def test_title_label(self, post):
        """Title label name should be title."""
        field_label = post._meta.get_field("title").verbose_name
        assert field_label == "title"

    def test_title_max_length(self, post):
        """Max length for title field should be 100."""
        max_length = post._meta.get_field("title").max_length
        assert max_length == 100
