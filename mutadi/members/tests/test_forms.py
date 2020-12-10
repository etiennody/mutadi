"""Unit tests for members form
"""
import pytest
from django.contrib.auth.models import User
from model_bakery import baker
from mutadi.members.views import UserCreationForm

pytestmark = pytest.mark.django_db


class TestUserCreationForm:
    """Group multiple tests for UserCreationForm"""

    @pytest.fixture
    def proto_user(self):
        """Fixture for baked User model."""
        self.proto_user = baker.make(User)
        self.proto_user.set_password("m=9UaK^C,Tbq9N=T")
        self.proto_user.save()
        return self.proto_user

    def test_registration_form_for_new_user(self):
        """Registration form should be valid for new user."""

        form = UserCreationForm(
            {
                "username": "Bob",
                "password1": "W:rZsT.eI9o__Tf%",
                "password2": "W:rZsT.eI9o__Tf%",
            }
        )
        assert form.is_valid()

    def test_invalid_registration_form_for_existing_user(self, proto_user):
        """
        Registration form should inform in existing user
        and user cannot be created twice.
        """

        form = UserCreationForm(
            {
                "username": proto_user.username,
                "password1": proto_user.password,
                "password2": proto_user.password,
            }
        )
        assert not form.is_valid()
        assert len(form.errors) == 1
        assert "username" in form.errors

    def test_invalid_registration_form_with_personal_informations(self):
        """
        Registration form should inform for personal informations entries
        and user cannot be created twice.
        """

        form = UserCreationForm(
            {
                "username": "Alice",
                "password1": "Alice",
                "password2": "Alice",
            }
        )
        assert not form.is_valid()
        assert len(form.errors) == 1
        assert "password2" in form.errors

    def test_invalid_registration_form_for_different_passwords(self):
        """
        Registration form should inform for different passwords
        and user cannot be created.
        """

        form = UserCreationForm(
            {
                "username": "Alice",
                "password1": "o4zX(N#4Yztl*G@|",
                "password2": "o4zX(N#4Yztl0000",
            }
        )
        assert not form.is_valid()
        assert len(form.errors) == 1
        assert "password2" in form.errors

    def test_invalid_registration_form_for_password_too_short(self):
        """
        Registration form should inform for too short passwords
        and user cannot be created.
        """

        form = UserCreationForm(
            {
                "username": "Alice",
                "password1": "o4zX",
                "password2": "o4zX",
            }
        )
        assert not form.is_valid()
        assert len(form.errors) == 1
        assert "password2" in form.errors

    def test_invalid_registration_form_for_password_with_only_number(self):
        """
        Registration form should inform for password with only number
        and user cannot be created twice.
        """

        form = UserCreationForm(
            {
                "username": "Alice",
                "password1": "1234567890",
                "password2": "1234567890",
            }
        )
        assert not form.is_valid()
        assert len(form.errors) == 1
        assert "password2" in form.errors
