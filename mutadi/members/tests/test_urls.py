"""Unit tests for members app urls
"""
import pytest
from django.urls import resolve, reverse

pytestmark = pytest.mark.django_db


class TestMembersUrls:
    """Group multiple tests for Members urls"""

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

    def test_edit_profile_reverse(self):
        """edit_profile should reverse to /members/edit_profile/."""
        assert reverse("edit_profile") == "/members/edit_profile/"

    def test_edit_profile_resolve(self):
        """/members/edit_profile/ should resolve to edit_profile."""
        assert resolve("/members/edit_profile/").view_name == "edit_profile"

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
