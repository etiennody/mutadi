"""Unit tests for members views
"""
import pytest
from django.contrib.auth import get_user_model
from django.test import RequestFactory
from django.urls import reverse
from model_bakery import baker
from mutadi.members.views import change_password_view, user_settings_edit_view
from pytest_django.asserts import assertRedirects, assertTemplateUsed

pytestmark = pytest.mark.django_db

User = get_user_model()

factory = RequestFactory()


class TestRegisterViews:
    """Group multiple tests for register views"""

    @pytest.fixture
    def proto_user(self):
        """Fixture for baked User model."""
        return baker.make(User)

    def test_view_url_create_user_profile_exists_at_desired_location(
        self, client
    ):
        """Register page should exist at desired location."""
        response = client.get("/members/register/")
        assert response.status_code == 200

    def test_view_url_register_accessible_by_name(self, client):
        """Register page should be accessible by name."""
        response = client.get(reverse("register"))
        assert response.status_code == 200

    def test_view_create_user_profile_uses_correct_template(self, client):
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


class TestUserSettingsEditViews:
    """Group multiple tests for user settings edit views"""

    @pytest.fixture
    def proto_user(self):
        """Fixture for baked User model."""
        self.proto_user = baker.make(User)
        self.proto_user.set_password("m=9UaK^C,Tbq9N=T")
        self.proto_user.save()
        return self.proto_user

    def test_view_url_edit_user_settings_page_exists_at_desired_location(
        self, client, proto_user
    ):
        """edit_user_settings page should exist at desired location."""
        client.login(
            username=f"{proto_user.username}",
            password="m=9UaK^C,Tbq9N=T",
        )
        response = client.get("/members/edit_user_settings/")
        assert response.status_code == 200

    def test_view_url_edit_user_settings_accessible_by_name(
        self, client, proto_user
    ):
        """edit_user_settings page should be accessible by name."""
        client.login(
            username=f"{proto_user.username}",
            password="m=9UaK^C,Tbq9N=T",
        )
        response = client.get(reverse("edit_user_settings"))
        assert response.status_code == 200

    def test_view_edit_user_settings_page_uses_correct_template(
        self, client, proto_user
    ):
        """Home page should use registration/edit_user_settings.html template."""
        client.login(
            username=f"{proto_user.username}",
            password="m=9UaK^C,Tbq9N=T",
        )
        response = client.get(reverse("edit_user_settings"))
        assert response.status_code == 200
        assertTemplateUsed(response, "registration/edit_user_settings.html")

    def test_valid_form_on_edit_user_settings_view(self, proto_user):
        """form_valid function should be valid the edit user_settings view"""
        data = {
            "username": "UsernameModified",
            "first_name": proto_user.first_name,
            "last_name": proto_user.last_name,
            "email": proto_user.email,
        }
        user = proto_user
        request = factory.post("/edit_user_settings/", data=data)
        request.user = user
        response = user_settings_edit_view(request)
        assert response
        assert str(proto_user.username) == "UsernameModified"
        assert User.objects.all().count() == 1


class TestChangePassword:
    """Change Password Test view"""

    @pytest.fixture
    def proto_user(self):
        """Fixture for baked User model."""
        self.proto_user = baker.make(User)
        self.proto_user.set_password("m=9UaK^C,Tbq9N=T")
        self.proto_user.save()
        return self.proto_user

    def test_root_url_resolves_to_change_password_view(
        self, client, proto_user
    ):
        """Valid the status code 200 and the template used to change password"""
        client.login(
            username=f"{proto_user.username}",
            password="m=9UaK^C,Tbq9N=T",
        )
        response = client.get(reverse("change_password"))
        assert response.status_code == 200
        assertTemplateUsed(response, "registration/change_password.html")

    def test_change_password_returns_correct_html(self, client, proto_user):
        """Valid html document and the html title in change password page"""
        client.login(
            username=f"{proto_user.username}",
            password="m=9UaK^C,Tbq9N=T",
        )
        response = client.get(reverse("change_password"))
        html = response.content.decode("utf8")
        assert html.startswith("\n\n<!DOCTYPE html>")
        assert "<title>Changer de mot de passe :: Mutadi</title>" in html
        assert html.endswith("</html>")

    def test_valid_form_on_change_password_view(self, proto_user):
        """It should be valid change password view"""
        data = {
            "old_password": "m=9UaK^C,Tbq9N=T",
            "new_password1": "/GiLnni.9H{^A?3+",
            "new_password2": "/GiLnni.9H{^A?3+",
        }
        user = proto_user
        request = factory.post("/password/", data=data)
        request.user = user
        response = change_password_view(request)
        assert response


class TestShowProfilePageViews:
    """Group multiple tests in Show Profile Page views"""

    @pytest.fixture
    def proto_user(self):
        """Fixture for baked User model."""
        return baker.make(User)

    def test_view_url_show_profile_page_exists_at_desired_location(
        self, client, proto_user
    ):
        """Show Profile Page should exist at desired location."""
        response = client.get(f"/members/{proto_user.pk}/profile/")
        assert response.status_code == 200

    def test_view_url_accessible_by_name(self, client, proto_user):
        """Show Profile Page should be accessible by name."""
        url = reverse(
            "show_profile_page",
            args=[
                f"{proto_user.pk}",
            ],
        )
        response = client.get(url)
        assert response.status_code == 200

    def test_valid_show_profile_page_title_with_client(
        self, client, proto_user
    ):
        """Show Profile Page should contain Mon Profil."""
        url = reverse(
            "show_profile_page",
            args=[
                f"{proto_user.pk}",
            ],
        )
        response = client.get(url)
        assert "Mon profil" in str(response.content)

    def test_view_show_profile_page_uses_correct_template(
        self, client, proto_user
    ):
        """Show Profile Page should use registration/user_profile.html template."""
        response = client.get(
            reverse(
                "show_profile_page",
                args=[
                    f"{proto_user.pk}",
                ],
            )
        )
        assert response.status_code == 200
        assertTemplateUsed(response, "registration/user_profile.html")


class TestEditUserProfileViews:
    """Group multiple tests for editing user profile views"""

    @pytest.fixture
    def proto_user(self):
        """Fixture for baked User model."""
        return baker.make(User)

    def test_view_url_edit_user_profile_exists_at_desired_location(
        self, client, proto_user
    ):
        """edit_user_profile page should exist at desired location."""
        client.login(
            username=f"{proto_user.username}",
            password="m=9UaK^C,Tbq9N=T",
        )
        response = client.get(f"/members/{proto_user.pk}/edit_user_profile/")
        assert response.status_code == 200

    def test_view_url_edit_user_profile_accessible_by_name(
        self, client, proto_user
    ):
        """edit_user_profile should be accessible by name."""
        client.login(
            username=f"{proto_user.username}",
            password="m=9UaK^C,Tbq9N=T",
        )
        response = client.get(
            reverse(
                "edit_user_profile",
                args=[
                    f"{proto_user.pk}",
                ],
            )
        )
        assert response.status_code == 200

    def test_view_edit_user_profile_page_uses_correct_template(
        self, client, proto_user
    ):
        """Home page should use registration/edit_user_profile.html template."""
        client.login(
            username=f"{proto_user.username}",
            password="m=9UaK^C,Tbq9N=T",
        )
        response = client.get(
            reverse(
                "edit_user_profile",
                args=[
                    f"{proto_user.pk}",
                ],
            )
        )
        assert response.status_code == 200
        assertTemplateUsed(response, "registration/edit_user_profile.html")
