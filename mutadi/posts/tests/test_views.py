"""Unit tests for posts app views"""
import pytest
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import RequestFactory
from django.urls import reverse
from model_bakery import baker
from mutadi.posts.models import Category, Post
from mutadi.posts.views import add_post_view
from pytest_django.asserts import assertRedirects, assertTemplateUsed

pytestmark = pytest.mark.django_db

User = get_user_model()

factory = RequestFactory()


class TestPostlistViews:
    """Group multiple tests in Postlist views."""

    @pytest.fixture
    def proto_user(self):
        """Fixture for baked User model."""
        return baker.make(User)

    @pytest.fixture
    def proto_post(self, proto_user):
        """Fixture for baked Post model."""
        return baker.make(
            Post,
            author=proto_user,
            content=(
                "Ipsum nulla aute irure sint consequat "
                "consequat proident irure voluptate."
            ),
            make_m2m=True,
            _create_files=True,
            _quantity=6,
        )

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

    def test_valid_search_pagination_is_four(self, client, proto_post):
        """Valid if search results pagination have six products on page."""
        response = client.get(reverse("post_list"))
        assert response.status_code == 200
        assert "is_paginated" in response.context
        assert (len(response.context_data["object_list"])) == 4


class TestPostDetailViews:
    """Group multiple tests in PostDetail views."""

    @pytest.fixture
    def proto_user(self):
        """Fixture for baked User model."""
        return baker.make(User)

    @pytest.fixture
    def proto_post(self, proto_user):
        """Fixture for baked Post model."""
        return baker.make(
            Post,
            author=proto_user,
            content=(
                "Ipsum nulla aute irure sint consequat "
                "consequat proident irure voluptate."
            ),
            _create_files=True,
        )

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


class TestAddPostViews:
    """Group multiple tests in AddPost views."""

    @pytest.fixture
    def proto_user(self):
        """Fixture for baked User model."""
        self.proto_user = baker.make(User)
        self.proto_user.set_password("m=9UaK^C,Tbq9N=T")
        self.proto_user.save()
        return self.proto_user

    def test_view_url_add_post_page_exists_at_desired_location(
        self, client, proto_user
    ):
        """add_post page should exist at desired location."""
        client.login(
            username=f"{proto_user.username}",
            password="m=9UaK^C,Tbq9N=T",
        )
        response = client.get("/posts/add_post/")
        assert response.status_code == 200

    def test_view_url_accessible_by_name(self, client, proto_user):
        """add_post page should be accessible by name."""
        client.login(
            username=f"{proto_user.username}",
            password="m=9UaK^C,Tbq9N=T",
        )
        url = reverse("add_post")
        response = client.get(url)
        assert response.status_code == 200

    def test_valid_add_post_page_with_title_in_html(self, client, proto_user):
        """add_post page should contain the title of the creation post."""
        client.login(
            username=f"{proto_user.username}",
            password="m=9UaK^C,Tbq9N=T",
        )
        url = reverse("add_post")
        response = client.get(url)
        assert "Ajouter une publication" in str(response.content)

    def test_view_add_post_page_uses_correct_template(
        self, client, proto_user
    ):
        """add_post page should use add_post.html template."""
        client.login(
            username=f"{proto_user.username}",
            password="m=9UaK^C,Tbq9N=T",
        )
        url = reverse("add_post")
        response = client.get(url)
        assert response.status_code == 200
        assertTemplateUsed(response, "add_post.html")

    def test_form_valid_on_add_post_view(self, proto_user):
        """form_valid function should be valid the add post view."""
        testfile = (
            b"\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x00\x00\x00\x21\xf9\x04"
            b"\x01\x0a\x00\x01\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02"
            b"\x02\x4c\x01\x00\x3b"
        )
        data = {
            "title": "This is the title",
            "categories": [1, 2],
            "overview": "This is the overview",
            "content": (
                "Culpa est et aliquip non tempor "
                "mollit exercitation cillum et."
            ),
            "featured": False,
            "status": 1,
            "thumbnail": SimpleUploadedFile(
                "small.gif",
                testfile,
                content_type="image/gif",
            ),
        }
        user = proto_user
        request = factory.post("/add_post/", data=data)
        request.user = user
        response = add_post_view(request)
        assert response


class TestUpdatePostViews:
    """Group multiple tests in UpdatePost views."""

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
            content="Ex anim do nostrud cupidatat id nostrud ad.",
            _create_files=True,
        )

    def test_view_url_update_post_page_exists_at_desired_location(
        self, client, proto_post
    ):
        """update_post page should exist at desired location."""
        response = client.get(f"/posts/post_detail/edit/{proto_post.pk}")
        assert response.status_code == 200

    def test_view_url_accessible_by_name(self, client, proto_post):
        """update_post page should be accessible by name."""
        url = reverse(
            "update_post",
            args=[
                f"{proto_post.pk}",
            ],
        )
        response = client.get(url)
        assert response.status_code == 200

    def test_valid_update_post_page_with_correct_user(
        self, client, proto_post, proto_user
    ):
        """update_post page should contain the title of the post."""
        proto_post_a = baker.make(
            Post, content="Eiusmod eu ipsum id pariatur.", author=proto_user
        )
        client.login(
            username=f"{proto_user.username}",
            password="m=9UaK^C,Tbq9N=T",
        )
        url = reverse(
            "update_post",
            args=[
                f"{proto_post_a.pk}",
            ],
        )
        response = client.get(url)
        print(response.content)
        assert proto_post_a.title in str(response.content)

    def test_invalid_update_post_page_with_wrong_user(
        self, client, proto_post, proto_user
    ):
        """update_post page should contain the title of the post."""
        proto_user_a = baker.make(User)
        proto_post_b = baker.make(
            Post,
            content=(
                "Qui do anim tempor aliqua dolor non voluptate "
                "fugiat exercitation veniam nulla reprehenderit."
            ),
            author=proto_user_a,
        )
        client.login(
            username=f"{proto_user.username}",
            password="m=9UaK^C,Tbq9N=T",
        )
        url = reverse(
            "update_post",
            args=[
                f"{proto_post_b.pk}",
            ],
        )
        response = client.get(url)
        assert proto_post_b.title not in str(response.content)

    def test_view_update_post_page_uses_correct_template(
        self, client, proto_post
    ):
        """post_detail page should use post_detail.html template."""
        url = reverse(
            "update_post",
            args=[
                f"{proto_post.pk}",
            ],
        )
        response = client.get(url)
        assert response.status_code == 200
        assertTemplateUsed(response, "update_post.html")


class TestDeletePostViews:
    """Group multiple tests in DeletePost."""

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
            content="Consequat aliqua non qui veniam sit voluptate.",
            _create_files=True,
        )

    def test_view_url_delete_post_page_exists_at_desired_location(
        self, client, proto_post
    ):
        """delete_post page should exist at desired location."""
        response = client.get(f"/posts/post_detail/{proto_post.pk}/remove")
        assert response.status_code == 200

    def test_view_url_accessible_by_name(self, client, proto_post):
        """delete_post page should be accessible by name."""
        url = reverse(
            "delete_post",
            args=[
                f"{proto_post.pk}",
            ],
        )
        response = client.get(url)
        assert response.status_code == 200

    def test_valid_delete_post_page_with_correct_user(
        self, client, proto_post, proto_user
    ):
        """delete_post page should contain the title of the post."""
        proto_post_a = baker.make(
            Post, content="Cupidatat ex eu excepteur magna.", author=proto_user
        )
        client.login(
            username=f"{proto_user.username}",
            password="m=9UaK^C,Tbq9N=T",
        )
        url = reverse(
            "delete_post",
            args=[
                f"{proto_post_a.pk}",
            ],
        )
        response = client.get(url)
        assert proto_post_a.title in str(response.content)

    def test_invalid_delete_post_page_with_wrong_user(
        self, client, proto_post, proto_user
    ):
        """delete_post page should contain the title of the post."""
        proto_user_a = baker.make(User)
        proto_post_c = baker.make(
            Post,
            content=(
                "Cillum fugiat consequat est non sunt "
                "excepteur reprehenderit minim non nisi."
            ),
            author=proto_user_a,
        )
        client.login(
            username=f"{proto_user.username}",
            password="m=9UaK^C,Tbq9N=T",
        )
        url = reverse(
            "delete_post",
            args=[
                f"{proto_post_c.pk}",
            ],
        )
        response = client.get(url)
        assert proto_post_c.title not in str(response.content)

    def test_view_delete_post_page_uses_correct_template(
        self, client, proto_post
    ):
        """delete_post page should use delete_post.html template."""
        url = reverse(
            "delete_post",
            args=[
                f"{proto_post.pk}",
            ],
        )
        response = client.get(url)
        assert response.status_code == 200
        assertTemplateUsed(response, "delete_post.html")

    def test_delete_post_success_url(self, client, proto_post):
        """delete_post page should redirect to home page template."""
        response = client.post(f"/posts/post_detail/{proto_post.pk}/remove")
        assert response.status_code == 302
        assertRedirects(response, "/")


class TestCategoryViews:
    """Group multiple tests in Category views."""

    @pytest.fixture
    def proto_category(self):
        """Fixture for baked Category model."""
        return baker.prepare(Category, title="Test")

    @pytest.fixture
    def proto_post(self, proto_category):
        """Fixture for baked Post model."""
        return baker.make(
            Post,
            categories__title=proto_category.title,
            content="Consequat aliqua non qui veniam sit voluptate.",
            _create_files=True,
        )

    def test_view_url_category_page_exists_at_desired_location(
        self, client, proto_category
    ):
        """category page should exist at desired location."""
        response = client.get(f"/posts/category/{proto_category.title}/")
        assert response.status_code == 200

    def test_view_url_accessible_by_name(self, client, proto_category):
        """category page should be accessible by name."""
        url = reverse(
            "category",
            args=[
                f"{proto_category.title}",
            ],
        )
        response = client.get(url)
        assert response.status_code == 200

    def test_valid_categories_page_with_post_category_title(
        self, client, proto_category, proto_post
    ):
        """category page should contain the title of post category."""
        url = reverse(
            "category",
            args=[
                f"{proto_category.title}",
            ],
        )
        response = client.get(url)
        assert response.status_code == 200
        assert b"Test" in response.content
        assert proto_post.categories.all().count() == 5

    def test_view_categories_page_uses_correct_template(
        self, client, proto_category
    ):
        """category page should use categories.html template."""
        url = reverse(
            "category",
            args=[
                f"{proto_category.title}",
            ],
        )
        response = client.get(url)
        assert response.status_code == 200
        assertTemplateUsed(response, "categories.html")

    def test_valid_search_pagination_is_four(self, client, proto_category):
        """Valid if search results pagination have six products on page."""
        response = client.get(
            reverse(
                "category",
                args=[
                    f"{proto_category.title}",
                ],
            )
        )
        assert response.status_code == 200
        assert (len(response.context["cats"])) == 4


class TestSearchResultsViews:
    """Group multiple tests in search results views."""

    @pytest.fixture
    def proto_post(self):
        """Fixture for baked Post model."""
        return baker.make(
            Post,
            title=baker.seq("Post-"),
            content="Consequat aliqua non qui veniam sit voluptate.",
            _create_files=True,
            _quantity=6,
        )

    def test_view_url_search_results_page_exists_at_desired_location(
        self, client, proto_post
    ):
        """search_results page should exist at desired location."""
        response = client.get(f"/posts/search/?q={proto_post[1].title}")
        assert response.status_code == 200

    def test_view_url_accessible_by_name(self, client, proto_post):
        """search_results page should be accessible by name."""
        url = reverse("search_results")
        response = client.get(url, {"q": f"{proto_post[1].title}"})
        assert response.status_code == 200

    def test_valid_search_results_page_title_with_client(
        self, client, proto_post
    ):
        """search_results page should contain "Résultats de recherche"."""
        url = reverse("search_results")
        response = client.get(url, {"q": f"{proto_post[1].title}"})
        print(response.content)
        assert proto_post[1].title in str(response.content)

    def test_view_search_results_page_uses_correct_template(
        self, client, proto_post
    ):
        """search_results page should use search_results.html template."""
        response = client.get(
            reverse("search_results"), {"q": f"{proto_post[1].title}"}
        )
        assert response.status_code == 200
        assertTemplateUsed(response, "search_results.html")

    def test_search_results_product_is_ko(self, client):
        """Valid if search results can be down."""
        response = client.get(reverse("search_results"), {"q": "Moutarde"})
        assert response.context_data["post_searches"].count() == 0

    def test_valid_search_pagination_is_four(self, client, proto_post):
        """Valid if search results pagination have six products on page."""
        response = client.get(reverse("search_results"), {"q": "Post"})
        assert response.status_code == 200
        assert "is_paginated" in response.context
        assert (len(response.context_data["post_searches"])) == 4
