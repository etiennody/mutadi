"""Unit tests for posts app models
"""
import pytest
from mutadi.posts.models import Category, Comment, Post
from django.contrib.auth.models import User


pytestmark = pytest.mark.django_db


def test___str__category_model():
    """Test __str__() method in Category model"""
    category = Category.objects.create(title="Bricolage")
    assert category.__str__() == "Bricolage"
    assert str(category) == "Bricolage"


def test___str__comment_model():
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


def test___str__post_model():
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
