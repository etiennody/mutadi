"""Unit tests for posts app models
"""
import pytest
from django.contrib.auth.models import User
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
        """Test function using fixture of baked model."""
        assert isinstance(category, Category)

    def test___str__category_model(self, category):
        """Test __str__() method in Category model."""
        assert category.__str__() == category.title
        assert str(category) == category.title

    def test_verbose_name_plural_categories(self):
        """Test verbose_name_plural for categories."""
        assert Category._meta.verbose_name_plural == "categories"


class TestCommentModel:
    """Group multiple tests in Comment Model"""

    @pytest.fixture
    def comment(self):
        """Fixture for baked Category model."""
        return baker.make(Comment)

    def test_using_comment(self, comment):
        """Test function using fixture of baked model."""
        assert isinstance(comment, Comment)

    def test___str__comment_model(self, comment):
        """Test __str__() method in Comment model."""
        assert comment.__str__() == comment.user.username
        assert str(comment) == comment.user.username


class TestPostModel:
    """Group multiple tests in Post Model"""

    @pytest.fixture
    def post(self):
        """Fixture for baked Post model."""
        return baker.make(Post, make_m2m=True)

    def test_using_post(self, post):
        """Test function using fixture of baked model."""
        assert isinstance(post, Post)

    def test__str__post_model(self, post):
        """Test __str__() method in Post model."""
        assert post.__str__() == post.title + " | " + str(post.author)
        assert str(post) == post.title + " | " + str(post.author)
