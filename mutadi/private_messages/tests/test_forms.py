"""Unit tests for private messages form
"""
import pytest
from django.contrib.auth import get_user_model
from model_bakery import baker
from mutadi.private_messages.forms import ComposeForm, ReplyForm

pytestmark = pytest.mark.django_db

User = get_user_model()


class TestComposeForm:
    """Group multiple tests for ComposeForm"""

    @pytest.fixture
    def proto_user_a(self):
        """Fixture for baked User model."""
        self.proto_user_a = baker.make(User)
        self.proto_user_a.set_password("m=9UaK^C,Tbq9N=T")
        self.proto_user_a.save()
        return self.proto_user_a

    @pytest.fixture
    def proto_user_b(self):
        """Fixture for baked User model."""
        self.proto_user_b = baker.make(User)
        self.proto_user_b.set_password("3$0aF/gxFsinR'6k")
        self.proto_user_b.save()
        return self.proto_user_b

    def test_valid_compose_message_form(self, proto_user_b):
        """Compose message form should be valid for a member."""
        data = {
            "subject": "This is the subject",
            "recipient": proto_user_b,
            "content": (
                "Culpa est et aliquip non tempor "
                "mollit exercitation cillum et."
            ),
        }
        form = ComposeForm(data)
        assert form.is_valid()

    def test_invalid_compose_message_form_wit_subject_missing(
        self, proto_user_b
    ):
        """Compose message form should be refused with subject missing."""
        data = {
            "subject": "",
            "recipient": proto_user_b,
            "content": (
                "Culpa est et aliquip non tempor "
                "mollit exercitation cillum et."
            ),
        }
        form = ComposeForm(data)
        assert not form.is_valid()
        assert len(form.errors) == 1
        assert "subject" in form.errors

    def test_invalid_compose_message_form_wit_recipient_missing(self):
        """Compose message form should be refused with recipient missing."""
        data = {
            "subject": "This is the subject",
            "recipient": "",
            "content": (
                "Culpa est et aliquip non tempor "
                "mollit exercitation cillum et."
            ),
        }
        form = ComposeForm(data)
        assert not form.is_valid()
        assert len(form.errors) == 1
        assert "recipient" in form.errors

    def test_invalid_compose_message_form_wit_content_missing(
        self, proto_user_a
    ):
        """Compose message form should be refused with content missing."""
        data = {
            "subject": "This is the subject",
            "recipient": proto_user_a,
            "content": "",
        }
        form = ComposeForm(data)
        assert not form.is_valid()
        assert len(form.errors) == 1
        assert "content" in form.errors


class TestReplyForm:
    """Group multiple tests for ReplyForm"""

    def test_valid_reply_message_form(self):
        """Reply message form should be valid for a member."""
        data = {
            "subject": "This is the subject",
            "content": (
                "Culpa est et aliquip non tempor "
                "mollit exercitation cillum et."
            ),
        }
        form = ReplyForm(data)
        assert form.is_valid()

    def test_invalid_reply_message_form_wit_subject_missing(self):
        """Reply message form should be refused with subject missing."""
        data = {
            "subject": "",
            "content": (
                "Culpa est et aliquip non tempor "
                "mollit exercitation cillum et."
            ),
        }
        form = ReplyForm(data)
        assert not form.is_valid()
        assert len(form.errors) == 1
        assert "subject" in form.errors

    def test_invalid_reply_message_form_with_content_missing(self):
        """Reply message form should be refused with content missing."""
        data = {
            "subject": "This is the subject",
            "content": "",
        }
        form = ReplyForm(data)
        assert not form.is_valid()
        assert len(form.errors) == 1
        assert "content" in form.errors
