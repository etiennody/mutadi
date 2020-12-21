"""Unit tests for members app urls
"""
import pytest
from django.contrib.auth import get_user_model
from django.urls import resolve, reverse
from model_bakery import baker
from mutadi.posts.models import Profile

pytestmark = pytest.mark.django_db

User = get_user_model()


class TestMembersUrls:
    """Group multiple tests for Members urls"""

    @pytest.fixture
    def proto_profile(self):
        """Fixture for baked User model."""
        proto_user = baker.make(User)
        self.proto_profile = baker.make(Profile, user=proto_user)
        return self.proto_profile

    def test_register_reverse(self):
        """register should reverse to /members/register/."""
        assert reverse("register") == "/members/register/"

    def test_register_resolve(self):
        """/members/register/ should resolve to register."""
        assert resolve("/members/register/").view_name == "register"

    def test_login_reverse(self):
        """login should reverse to /members/login/."""
        assert reverse("login") == "/members/login/"

    def test_login_resolve(self):
        """/members/login/ should resolve to login."""
        assert resolve("/members/login/").view_name == "login"

    def test_logout_reverse(self):
        """logout should reverse to /members/logout/."""
        assert reverse("logout") == "/members/logout/"

    def test_logout_resolve(self):
        """/members/logout/ should resolve to logout."""
        assert resolve("/members/logout/").view_name == "logout"

    def test_edit_user_settings_reverse(self):
        """edit_user_settings should reverse to /members/edit_user_settings/."""
        assert reverse("edit_user_settings") == "/members/edit_user_settings/"

    def test_edit_user_settings_resolve(self):
        """/members/edit_user_settings/ should resolve to edit_user_settings."""
        assert (
            resolve("/members/edit_user_settings/").view_name
            == "edit_user_settings"
        )

    def test_change_password_reverse(self):
        """change_password should reverse to /members/password/."""
        assert reverse("change_password") == "/members/password/"

    def test_change_password_resolve(self):
        """/members/change_password/ should resolve to change_password."""
        assert resolve("/members/password/").view_name == "change_password"

    def test_change_password_success_reverse(self):
        """change_password_success should reverse to /members/password/."""
        assert (
            reverse("change_password_success")
            == "/members/change_password_success/"
        )

    def test_change_password_success_resolve(self):
        """/members/change_password_success/ should resolve to change_password_success."""
        assert (
            resolve("/members/change_password_success/").view_name
            == "change_password_success"
        )

    def test_show_profile_page_reverse(self, proto_profile):
        """show_profile_page should reverse to /members/{profile.pk}/profile/."""
        assert (
            reverse(
                "show_profile_page",
                args=[
                    f"{proto_profile.pk}",
                ],
            )
            == f"/members/{proto_profile.pk}/profile/"
        )

    def test_show_profile_page_resolve(self, proto_profile):
        """/members/{profile.pk}/profile/ should resolve to show_profile_page."""
        assert (
            resolve(f"/members/{proto_profile.pk}/profile/").view_name
            == "show_profile_page"
        )

    def test_edit_user_profile_reverse(self, proto_profile):
        """edit_user_profile should reverse to /members/{profile.pk}/edit_user_profile/."""
        assert (
            reverse(
                "edit_user_profile",
                args=[
                    f"{proto_profile.pk}",
                ],
            )
            == f"/members/{proto_profile.pk}/edit_user_profile/"
        )

    def test_edit_user_profile_resolve(self, proto_profile):
        """/members/{profile.pk}/edit_user_profile/ should resolve to edit_user_profile."""
        assert (
            resolve(
                f"/members/{proto_profile.pk}/edit_user_profile/"
            ).view_name
            == "edit_user_profile"
        )
