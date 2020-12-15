"""Unit tests for posts app views
"""
import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from model_bakery import baker
from mutadi.posts.models import Post
from pytest_django.asserts import assertRedirects, assertTemplateUsed

pytestmark = pytest.mark.django_db


class TestPostlistViews:
    """Group multiple tests in Postlist views"""

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


class TestPostDetailViews:
    """Group multiple tests in PostDetail views"""

    @pytest.fixture
    def proto_post(self):
        """Fixture for baked Post model."""
        return baker.make(Post, _create_files=True)

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
    """Group multiple tests in AddPost views"""

    @pytest.fixture
    def proto_user(self):
        """Fixture for baked User model."""
        self.proto_user = baker.make(User)
        self.proto_user.set_password("m=9UaK^C,Tbq9N=T")
        self.proto_user.save()
        return self.proto_user

    def test_view_url_add_post_page_exists_at_desired_location(self, client):
        """add_post page should exist at desired location."""
        response = client.get("/posts/add_post/")
        assert response.status_code == 200

    def test_view_url_accessible_by_name(self, client):
        """add_post page should be accessible by name."""
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

    def test_view_add_post_page_uses_correct_template(self, client):
        """add_post page should use add_post.html template."""
        url = reverse("add_post")
        response = client.get(url)
        assert response.status_code == 200
        assertTemplateUsed(response, "add_post.html")


class TestUpdatePostViews:
    """Group multiple tests in UpdatePost views"""

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
        return baker.make(Post, _create_files=True)

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

    def test_valid_update_post_page_with_post_title_as_reminder(
        self, client, proto_post, proto_user
    ):
        """update_post page should contain the title of the post."""
        client.login(
            username=f"{proto_user.username}",
            password="m=9UaK^C,Tbq9N=T",
        )
        url = reverse(
            "update_post",
            args=[
                f"{proto_post.pk}",
            ],
        )
        response = client.get(url)
        print(response.content)
        assert proto_post.title in str(response.content)

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
    """Group multiple tests in DeletePost views"""

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
        return baker.make(Post, _create_files=True)

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

    def test_valid_delete_post_page_with_post_title_as_reminder(
        self, client, proto_post, proto_user
    ):
        """delete_post page should contain the title of the post."""
        client.login(
            username=f"{proto_user.username}",
            password="m=9UaK^C,Tbq9N=T",
        )
        url = reverse(
            "delete_post",
            args=[
                f"{proto_post.pk}",
            ],
        )
        response = client.get(url)
        assert proto_post.title in str(response.content)

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
        response = client.post(f"/posts/post_detail/{proto_post.pk}/remove")
        assert response.status_code == 302
        assertRedirects(response, "/")
