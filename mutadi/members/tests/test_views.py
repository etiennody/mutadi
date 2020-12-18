"""Unit tests for members views
"""
import pytest
from django.contrib.auth.models import User
from django.test import RequestFactory
from django.urls import reverse
from model_bakery import baker
from mutadi.members.views import user_edit_view
from pytest_django.asserts import assertRedirects, assertTemplateUsed

pytestmark = pytest.mark.django_db

factory = RequestFactory()


class TestRegisterViews:
    """Group multiple tests for register views"""

    @pytest.fixture
    def proto_user(self):
        """Fixture for baked User model."""
        return baker.make(User)

    def test_view_url_register_page_exists_at_desired_location(self, client):
        """Register page should exist at desired location."""
        response = client.get("/members/register/")
        assert response.status_code == 200

    def test_view_url_register_accessible_by_name(self, client):
        """Register page should be accessible by name."""
        response = client.get(reverse("register"))
        assert response.status_code == 200

    def test_view_register_page_uses_correct_template(self, client):
        """Home page should use registration/register.html template."""
        response = client.get(reverse("register"))
        assert response.status_code == 200
        assertTemplateUsed(response, "registration/register.html")

    def test_valid_user_exists_after_registration(self, client, proto_user):
        """Register if prototype user is in db after registration."""
        response = client.post(
            reverse("register"),
            {
                "username": proto_user.username,
                "first_name": proto_user.first_name,
                "last_name": proto_user.last_name,
                "email": proto_user.email,
                "password1": "dhjO0iZxt}!;",
                "password2": "dhjO0iZxt}!;",
                "robot": True,
            },
            follow=True,
        )
        assert response.status_code == 200
        assert User.objects.filter(username=proto_user.username).exists()


class TestLoginViews:
    """Group multiple tests for login views"""

    @pytest.fixture
    def proto_user(self):
        """Fixture for baked User model."""
        self.proto_user = baker.make(User)
        self.proto_user.set_password("m=9UaK^C,Tbq9N=T")
        self.proto_user.save()
        return self.proto_user

    def test_view_url_login_page_exists_at_desired_location(self, client):
        """Login page should exist at desired location."""
        response = client.get("/members/login/")
        assert response.status_code == 200

    def test_view_url_login_accessible_by_name(self, client):
        """Login page should be accessible by name."""
        response = client.get(reverse("login"))
        assert response.status_code == 200

    def test_view_login_page_uses_correct_template(self, client):
        """Login page should use registration/login.html template."""
        response = client.get(reverse("login"))
        assert response.status_code == 200
        assertTemplateUsed(response, "registration/login.html")

    def test_valid_user_login(self, client, proto_user):
        """Valid if user can be authenticated."""

        response = client.post(
            reverse("login"),
            {
                "username": proto_user.username,
                "password": "m=9UaK^C,Tbq9N=T",
                "robot": True,
            },
            follow=True,
        )
        assert response.context["user"].is_authenticated

    def test_invalid_user_login_with_wrong_password(self, client, proto_user):
        """Unvalid user login if user doesn't exist in database."""
        response = client.post(
            reverse("login"),
            {
                "username": proto_user.username,
                "password": "anonymous",
                "robot": True,
            },
            follow=True,
        )
        assert not response.context["user"].is_authenticated

    def test_invalid_user_login_with_wrong_username(self, client, proto_user):
        """Unvalid user login if user type a wrong username."""
        response = client.post(
            reverse("login"),
            {"username": "anonymous", "password": proto_user.password},
            follow=True,
        )
        assert not response.context["user"].is_authenticated

    def test_valid_redirect_user_logged_to_home_page(self, client, proto_user):
        """After login process, user should be redirect to home page."""

        response = client.post(
            reverse("login"),
            {
                "username": proto_user.username,
                "password": "m=9UaK^C,Tbq9N=T",
                "robot": True,
            },
            follow=True,
        )
        assert response.context["user"].is_authenticated
        assertRedirects(response, "/")


class TestLogoutViews:
    """Group multiple tests for login views"""

    def test_view_url_logout_accessible_by_name(self, client):
        """Logout page should be accessible by name."""
        response = client.get(reverse("logout"))
        print(response.content)
        assert response.status_code == 302

    def test_valid_logout_page_view(self, client):
        """Test logout view using reverse url."""
        response = client.get(reverse("logout"))
        assert response.status_code == 302
        assertRedirects(response, "/")


class TestUserEditViews:
    """Group multiple tests for user edit views"""

    @pytest.fixture
    def proto_user(self):
        """Fixture for baked User model."""
        self.proto_user = baker.make(User)
        self.proto_user.set_password("m=9UaK^C,Tbq9N=T")
        self.proto_user.save()
        return self.proto_user

    def test_view_url_edit_profile_page_exists_at_desired_location(
        self, client, proto_user
    ):
        """edit_profile page should exist at desired location."""
        client.login(
            username=f"{proto_user.username}",
            password="m=9UaK^C,Tbq9N=T",
        )
        response = client.get("/members/edit_profile/")
        assert response.status_code == 200

    def test_view_url_edit_profile_accessible_by_name(
        self, client, proto_user
    ):
        """edit_profile page should be accessible by name."""
        client.login(
            username=f"{proto_user.username}",
            password="m=9UaK^C,Tbq9N=T",
        )
        response = client.get(reverse("edit_profile"))
        assert response.status_code == 200

    def test_view_edit_profile_page_uses_correct_template(
        self, client, proto_user
    ):
        """Home page should use registration/edit_profile.html template."""
        client.login(
            username=f"{proto_user.username}",
            password="m=9UaK^C,Tbq9N=T",
        )
        response = client.get(reverse("edit_profile"))
        assert response.status_code == 200
        assertTemplateUsed(response, "registration/edit_profile.html")

    def test_valid_form_on_edit_profile_view(self, proto_user):
        """form_valid function should be valid the edit profile view"""
        data = {
            "username": "UsernameModified",
            "first_name": proto_user.first_name,
            "last_name": proto_user.last_name,
            "email": proto_user.email,
        }
        user = proto_user
        request = factory.post("/edit_profile/", data=data)
        request.user = user
        response = user_edit_view(request)
        assert response
        assert str(proto_user.username) == "UsernameModified"
        assert User.objects.all().count() == 1
