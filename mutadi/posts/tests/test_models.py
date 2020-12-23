"""Unit tests for posts app models
"""
import pytest
from model_bakery import baker
from mutadi.posts.models import Category, Comment, Post, Profile
from django.contrib.auth import get_user_model

pytestmark = pytest.mark.django_db

User = get_user_model()


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
    def post(self):
        """Fixture for baked Category model."""
        return baker.make(
            Post, content="Reprehenderit tempor laboris incididunt occaecat."
        )

    @pytest.fixture
    def comment(self, post):
        """Fixture for baked Category model."""
        return baker.make(Comment, post=post)

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
    def proto_user(self):
        """Fixture for baked User model."""
        self.proto_user = baker.make(User)
        self.proto_user.set_password("m=9UaK^C,Tbq9N=T")
        self.proto_user.save()
        return self.proto_user

    @pytest.fixture
    def proto_post(self):
        """Fixture for baked Post model."""
        return baker.make(
            Post,
            make_m2m=True,
            content="Amet amet ea excepteur veniam et do elit irure.",
        )

    @pytest.fixture
    def proto_comment(self, proto_post, proto_user):
        """Fixture for baked Category model."""
        return baker.make(Comment, post=proto_post, user=proto_user)

    def test_using_post(self, proto_post):
        """Function should be using fixture of Post baked model."""
        assert isinstance(proto_post, Post)

    def test__str__post_model(self, proto_post):
        """__str__() method should be title and author of a post."""
        assert proto_post.__str__() == proto_post.title + " | " + str(
            proto_post.author
        )
        assert str(proto_post) == proto_post.title + " | " + str(
            proto_post.author
        )

    def test_title_label(self, proto_post):
        """Title label name should be title."""
        field_label = proto_post._meta.get_field("title").verbose_name
        assert field_label == "title"

    def test_title_max_length(self, proto_post):
        """Max length for title field should be 100."""
        max_length = proto_post._meta.get_field("title").max_length
        assert max_length == 100

    def test_get_absolute_url(self, proto_post):
        """get_absolute_url() should be redirected to home page."""
        assert proto_post.get_absolute_url() == "/"

    def test_get_comments(self, proto_post, proto_comment):
        """get_comments method should return all comments for a post."""
        assert proto_post.get_comments
        assert Post.objects.count() == 1
        assert Comment.objects.count() == 1

    def test_comment_count(self, proto_post, proto_comment):
        """comment_count method should all comments counted for a post."""
        assert proto_post.comment_count
        assert Post.objects.count() == 1
        assert Comment.objects.count() == 1


class TestProfileModel:
    """Group multiple tests in Category model"""

    @pytest.fixture
    def profile(self):
        """Fixture for baked Category model."""
        return baker.make(Profile)

    def test_using_profile(self, profile):
        """Function should be using fixture of profile baked model."""
        assert isinstance(profile, Profile)

    def test___str__profile_model(self, profile):
        """__str__() method should be the profile title."""
        assert profile.__str__() == str(profile.user)
        assert str(profile) == str(profile.user)

    def test_get_absolute_url(self, profile):
        """get_absolute_url() should be reirected to home page."""
        assert profile.get_absolute_url() == "/"

    def test_verbose_name_plural_profiles(self, profile):
        """verbose_name_plural should be categories."""
        assert profile._meta.verbose_name_plural == "profiles"

    def test_profile_picture_label(self, profile):
        """Title label profile picture should be profile_pic."""
        field_label = profile._meta.get_field("profile_pic").verbose_name
        assert field_label == "profile pic"

    def test_profile_pic_blank(self, profile):
        """Blank for profile picture field should be True."""
        blank = profile._meta.get_field("profile_pic").blank
        assert blank

    def test_profile_pic_null(self, profile):
        """Nullable for profile picture field should be True."""
        null = profile._meta.get_field("profile_pic").null
        assert null

    def test_profile_exists(self, profile):
        """Profile should exists with baked Profile model."""
        assert Profile.objects.count() == 1
