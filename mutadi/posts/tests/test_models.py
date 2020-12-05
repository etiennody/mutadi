"""Unit tests for posts app models
"""
import pytest
from django.contrib.auth.models import User
from mutadi.posts.models import Category, Comment, Post

pytestmark = pytest.mark.django_db


class TestCategoryClass:
    """Group multiple tests in Category class"""

    def test___str__category_model(self):
        """Test __str__() method in Category model"""
        category = Category.objects.create(title="Bricolage")
        assert category.__str__() == "Bricolage"
        assert str(category) == "Bricolage"

    def test_verbose_name_plural_categories(self):
        """Test verbose_name_plural for categories"""
        assert Category._meta.verbose_name_plural == "categories"


class TestCommentClass:
    """Group multiple tests in Comment class"""

    def test___str__comment_model(self):
        """Test __str__() method in Category model"""
        user = User.objects.create(username="Bob")
        post = Post.objects.create(
            title="Post1",
            overview="This an overview1",
            content="This a content1",
            featured=True,
            author=user,
        )
        comment = Comment.objects.create(
            content="This a content", user=user, post=post
        )
        assert comment.__str__() == "Bob"
        assert str(comment) == "Bob"


class TestPostClass:
    """Group multiple tests in Post class"""

    def test___str__post_model(self):
        """Test __str__() method in Category model"""
        user = User.objects.create(username="Bob")
        post = Post.objects.create(
            title="Post2",
            overview="This an overview2",
            content="This a content2",
            featured=True,
            author=user,
        )
        assert post.__str__() == "Post2 | Bob"
        assert str(post) == "Post2 | Bob"
