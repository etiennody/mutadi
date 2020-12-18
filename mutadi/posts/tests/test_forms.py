"""Unit tests for posts form
"""
import pytest
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from model_bakery import baker
from mutadi.posts.forms import EditForm, PostForm
from mutadi.posts.models import Category, Post

pytestmark = pytest.mark.django_db


class TestPostForm:
    """Group multiple tests for PostForm"""

    @pytest.fixture()
    def proto_user(self):
        """Fixture for baked User model."""
        return baker.make(User)

    @pytest.fixture()
    def proto_category(self):
        """Fixture for baked Category model."""
        categories_set = baker.prepare(Category, _quantity=5)
        return categories_set

    @pytest.fixture()
    def proto_post(self, proto_category):
        """Fixture for baked Post model."""
        return baker.make(
            Post,
            content="Aute non ex nostrud amet ipsum.",
            categories=proto_category,
            make_m2m=True,
            _create_files=True,
        )

    def test_valid_add_post_form(self, proto_post, proto_user):
        """Add post form should be valid for new user."""
        testfile = (
            b"\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x00\x00\x00\x21\xf9\x04"
            b"\x01\x0a\x00\x01\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02"
            b"\x02\x4c\x01\x00\x3b"
        )
        data = {
            "title": "This is the added title",
            "author": proto_user,
            "categories": [1, 2],
            "overview": "This is the added overview",
            "content": "This is the added content",
            "featured": True,
            "status": 1,
        }
        form = PostForm(
            data,
            {
                "thumbnail": SimpleUploadedFile(
                    "small.gif",
                    testfile,
                    content_type="image/gif",
                )
            },
        )
        assert form.is_valid()

    def test_valid_add_post_form_with_unpublish_article(
        self, proto_post, proto_user
    ):
        """Add post form should be valid with an unpublish article."""
        testfile = (
            b"\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x00\x00\x00\x21\xf9\x04"
            b"\x01\x0a\x00\x01\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02"
            b"\x02\x4c\x01\x00\x3b"
        )
        data = {
            "title": "This is the added title",
            "author": proto_user,
            "categories": [6, 7],
            "overview": "This is the added overview",
            "content": "This is the added content",
            "featured": True,
            "status": 0,
        }
        form = PostForm(
            data,
            {
                "thumbnail": SimpleUploadedFile(
                    "small.gif",
                    testfile,
                    content_type="image/gif",
                )
            },
        )
        assert form.is_valid()

    def test_invalid_add_post_form_with_title_missing(
        self, proto_post, proto_user
    ):
        """Add post form should be refused with title missing."""

        testfile = (
            b"\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x00\x00\x00\x21\xf9\x04"
            b"\x01\x0a\x00\x01\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02"
            b"\x02\x4c\x01\x00\x3b"
        )
        data = {
            "title": "",
            "author": proto_user,
            "categories": [11, 12],
            "overview": "This is the added overview",
            "content": "This is the added content",
            "featured": True,
            "status": 1,
        }
        form = PostForm(
            data,
            {
                "thumbnail": SimpleUploadedFile(
                    "small.gif",
                    testfile,
                    content_type="image/gif",
                )
            },
        )
        assert not form.is_valid()
        assert len(form.errors) == 1
        assert "title" in form.errors

    def test_invalid_add_post_form_with_categorie_missing(
        self, proto_post, proto_user
    ):
        """Add post form should be refused with categories missing."""

        testfile = (
            b"\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x00\x00\x00\x21\xf9\x04"
            b"\x01\x0a\x00\x01\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02"
            b"\x02\x4c\x01\x00\x3b"
        )
        data = {
            "title": "This is the added title",
            "author": proto_user,
            "categories": [],
            "overview": "This is the added overview",
            "content": "This is the added content",
            "featured": True,
            "status": 1,
        }
        form = PostForm(
            data,
            {
                "thumbnail": SimpleUploadedFile(
                    "small.gif",
                    testfile,
                    content_type="image/gif",
                )
            },
        )
        assert not form.is_valid()
        assert len(form.errors) == 1
        assert "categories" in form.errors

    def test_invalid_add_post_form_with_image_missing(
        self, proto_post, proto_user
    ):
        """Add post form should be refused with image missing."""

        data = {
            "title": "This is the added title",
            "author": proto_user,
            "categories": [21, 22],
            "overview": "This is the added overview",
            "content": "This is the added content",
            "featured": True,
            "status": 1,
        }
        form = PostForm(data)
        assert not form.is_valid()
        assert len(form.errors) == 1
        assert "thumbnail" in form.errors

    def test_valid_add_post_form_with_featured_not_checked(
        self, proto_post, proto_user
    ):
        """Add post form should be valid with an unchecked featured."""

        testfile = (
            b"\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x00\x00\x00\x21\xf9\x04"
            b"\x01\x0a\x00\x01\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02"
            b"\x02\x4c\x01\x00\x3b"
        )
        data = {
            "title": "This is the added title",
            "author": proto_user,
            "categories": [26, 27],
            "overview": "This is the added overview",
            "content": "This is the added content",
            "featured": False,
            "status": 1,
        }
        form = PostForm(
            data,
            {
                "thumbnail": SimpleUploadedFile(
                    "small.gif",
                    testfile,
                    content_type="image/gif",
                )
            },
        )
        assert form.is_valid()


class TestUpdatePostForm:
    """Group multiple tests for UpdatePostForm"""

    @pytest.fixture()
    def proto_user(self):
        """Fixture for baked User model."""
        return baker.make(User)

    @pytest.fixture()
    def proto_category(self):
        """Fixture for baked Category model."""
        categories_set = baker.prepare(Category, _quantity=5)
        return categories_set

    @pytest.fixture()
    def proto_post(self, proto_category):
        return baker.make(
            Post,
            content=(
                "Aliquip excepteur qui mollit labore nulla et culpa "
                "minim et commodo reprehenderit consequat sint."
            ),
            categories=proto_category,
            make_m2m=True,
            _create_files=True,
        )

    def test_valid_update_post_form(self, proto_post, proto_user):
        """Update post form should be valid for new user."""
        testfile = (
            b"\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x00\x00\x00\x21\xf9\x04"
            b"\x01\x0a\x00\x01\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02"
            b"\x02\x4c\x01\x00\x3b"
        )
        data = {
            "title": "This is the modified title",
            "categories": [31, 32],
            "overview": "This is the modified overview",
            "content": "This is the modified content",
            "featured": True,
            "status": 1,
        }
        form = EditForm(
            data,
            {
                "thumbnail": SimpleUploadedFile(
                    "small.gif",
                    testfile,
                    content_type="image/gif",
                )
            },
        )
        print(form.errors)
        assert form.is_valid()

    def test_valid_update_post_form_with_unpublish_article(
        self, proto_post, proto_user
    ):
        """Update post form should be valid with an unpublish article."""
        testfile = (
            b"\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x00\x00\x00\x21\xf9\x04"
            b"\x01\x0a\x00\x01\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02"
            b"\x02\x4c\x01\x00\x3b"
        )
        data = {
            "title": "This is the modified title",
            "categories": [36, 37],
            "overview": "This is the modified overview",
            "content": "This is the modified content",
            "featured": True,
            "status": 0,
        }
        form = EditForm(
            data,
            {
                "thumbnail": SimpleUploadedFile(
                    "small.gif",
                    testfile,
                    content_type="image/gif",
                )
            },
        )
        assert form.is_valid()

    def test_invalid_update_post_form_with_title_missing(
        self, proto_post, proto_user
    ):
        """Update post form should be refused with title missing."""

        testfile = (
            b"\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x00\x00\x00\x21\xf9\x04"
            b"\x01\x0a\x00\x01\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02"
            b"\x02\x4c\x01\x00\x3b"
        )
        data = {
            "title": "",
            "categories": [41, 42],
            "overview": "This is the modified overview",
            "content": "This is the modified content",
            "featured": True,
            "status": 1,
        }
        form = EditForm(
            data,
            {
                "thumbnail": SimpleUploadedFile(
                    "small.gif",
                    testfile,
                    content_type="image/gif",
                )
            },
        )
        assert not form.is_valid()
        assert len(form.errors) == 1
        assert "title" in form.errors

    def test_invalid_update_post_form_with_categorie_missing(
        self, proto_post, proto_user
    ):
        """Update post form should be refused with categories missing."""

        testfile = (
            b"\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x00\x00\x00\x21\xf9\x04"
            b"\x01\x0a\x00\x01\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02"
            b"\x02\x4c\x01\x00\x3b"
        )
        data = {
            "title": "This is the modified title",
            "categories": [],
            "overview": "This is the modified overview",
            "content": "This is the modified content",
            "featured": True,
            "status": 1,
        }
        form = EditForm(
            data,
            {
                "thumbnail": SimpleUploadedFile(
                    "small.gif",
                    testfile,
                    content_type="image/gif",
                )
            },
        )
        assert not form.is_valid()
        assert len(form.errors) == 1
        assert "categories" in form.errors

    def test_invalid_update_post_form_with_image_missing(
        self, proto_post, proto_user
    ):
        """Update post form should be refused with image missing."""

        data = {
            "title": "This is the modified title",
            "categories": [51, 52],
            "overview": "This is the modified overview",
            "content": "This is the modified content",
            "featured": True,
            "status": 1,
        }
        form = EditForm(data)
        assert not form.is_valid()
        assert len(form.errors) == 1
        assert "thumbnail" in form.errors

    def test_valid_update_post_form_with_featured_not_checked(
        self, proto_post, proto_user
    ):
        """Update post form should be valid with an unchecked featured."""

        testfile = (
            b"\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x00\x00\x00\x21\xf9\x04"
            b"\x01\x0a\x00\x01\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02"
            b"\x02\x4c\x01\x00\x3b"
        )
        data = {
            "title": "This is the modified title",
            "categories": [56, 57],
            "overview": "This is the modified overview",
            "content": "This is the modified content",
            "featured": False,
            "status": 1,
        }
        form = EditForm(
            data,
            {
                "thumbnail": SimpleUploadedFile(
                    "small.gif",
                    testfile,
                    content_type="image/gif",
                )
            },
        )
        assert form.is_valid()
