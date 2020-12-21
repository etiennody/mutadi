"""Unit tests for members form
"""
import pytest
from django.contrib.auth.models import User
from model_bakery import baker
from mutadi.members.forms import EditUserSettingsForm, SignUpForm

pytestmark = pytest.mark.django_db


class TestSignUpForm:
    """Group multiple tests for SignUpForm"""

    @pytest.fixture
    def proto_user(self):
        """Fixture for baked User model."""
        self.proto_user = baker.make(User)
        self.proto_user.set_password("m=9UaK^C,Tbq9N=T")
        self.proto_user.save()
        return self.proto_user

    def test_registration_form_for_new_user(self):
        """Registration form should be valid for new user."""

        form = SignUpForm(
            {
                "username": "Bob123",
                "first_name": "Bob",
                "last_name": "Robert",
                "email": "bobrobert@test.fr",
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

        form = SignUpForm(
            {
                "username": proto_user.username,
                "first_name": proto_user.first_name,
                "last_name": proto_user.last_name,
                "email": proto_user.email,
                "password1": proto_user.password,
                "password2": proto_user.password,
            }
        )
        assert not form.is_valid()
        assert len(form.errors) == 4
        assert "username" in form.errors

    def test_invalid_registration_form_with_personal_informations(self):
        """
        Registration form should inform for personal informations entries
        and user cannot be created twice.
        """

        form = SignUpForm(
            {
                "username": "Alice123",
                "first_name": "Alice",
                "last_name": "Robert",
                "email": "alicerobert@test.fr",
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

        form = SignUpForm(
            {
                "username": "Alice",
                "first_name": "Alice",
                "last_name": "Robert",
                "email": "alicerobert@test.fr",
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

        form = SignUpForm(
            {
                "username": "Alice",
                "first_name": "Alice",
                "last_name": "Robert",
                "email": "alicerobert@test.fr",
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

        form = SignUpForm(
            {
                "username": "Alice",
                "first_name": "Alice",
                "last_name": "Robert",
                "email": "alicerobert@test.fr",
                "password1": "1234567890",
                "password2": "1234567890",
            }
        )
        assert not form.is_valid()
        assert len(form.errors) == 1
        assert "password2" in form.errors


class TestEditUserSettingsForm:
    """Group multiple tests for EditUserSettingsForm"""

    @pytest.fixture
    def proto_user(self):
        """Fixture for baked User model."""
        self.proto_user = baker.make(User)
        self.proto_user.set_password("m=9UaK^C,Tbq9N=T")
        self.proto_user.save()
        return self.proto_user

    def test_edit_user_settings_form_for_new_user(self):
        """edit_user_settings form should be valid for new user."""

        form = EditUserSettingsForm(
            {
                "username": "Bob123",
                "first_name": "Bob",
                "last_name": "Robert",
                "email": "bobrobert@test.fr",
            }
        )
        assert form.is_valid()

    def test_invalid_edit_user_settings_form_for_existing_user(
        self, proto_user
    ):
        """
        edit_user_settings form should inform in existing user
        and user cannot be created twice.
        """

        form = EditUserSettingsForm(
            {
                "username": proto_user.username,
                "first_name": proto_user.first_name,
                "last_name": proto_user.last_name,
                "email": proto_user.email,
            }
        )
        assert not form.is_valid()
        assert len(form.errors) == 4
        assert "username" in form.errors

    def test_invalid_edit_user_settings_form_for_wrong_email(self):
        """
        edit_user_settings form should inform for different passwords
        and user cannot be created.
        """

        form = EditUserSettingsForm(
            {
                "username": "Alice",
                "first_name": "Alice",
                "last_name": "Robert",
                "email": "alicerobert@",
            }
        )
        assert not form.is_valid()
        assert len(form.errors) == 1
        assert "email" in form.errors
