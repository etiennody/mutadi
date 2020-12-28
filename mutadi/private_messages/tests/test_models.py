"""Unit tests for posts app models
"""
import pytest
from django.contrib.auth import get_user_model
from model_bakery import baker
from mutadi.private_messages.models import PrivateMessage

pytestmark = pytest.mark.django_db

User = get_user_model()


class TestPrivateMessageModel:
    """Group multiple tests in PrivateMessage model"""

    @pytest.fixture
    def proto_user(self):
        """Fixture for baked User model."""
        return baker.make(
            User,
            username=baker.seq("User-"),
            _quantity=3,
        )

    @pytest.fixture
    def proto_private_message(self, proto_user):
        """Fixture for baked PrivateMessage model."""
        return baker.make(
            PrivateMessage,
            sender=proto_user[0],
            recipient=proto_user[1],
            content=(
                "Proident nisi cillum sit tempor "
                "reprehenderit proident in non fugiat ex id."
            ),
        )

    def test_using_private_message(self, proto_private_message):
        """Function should be using fixture of private_message baked model."""
        assert isinstance(proto_private_message, PrivateMessage)

    def test___str__private_message_model(self, proto_private_message):
        """__str__() method should be the private_message subject."""
        assert (
            proto_private_message.__str__()
            == f"{proto_private_message.sender} to "
            f"{proto_private_message.recipient} : "
            f"{proto_private_message.content}"
        )
        assert (
            str(proto_private_message) == f"{proto_private_message.sender} to "
            f"{proto_private_message.recipient} : "
            f"{proto_private_message.content}"
        )

    def test_sender_label(self, proto_private_message):
        """Sender label name should be sender."""
        field_label = proto_private_message._meta.get_field(
            "sender"
        ).verbose_name
        assert field_label == "sender"

    def test_subject_max_length(self, proto_private_message):
        """Max length for subject field should be 20."""
        max_length = proto_private_message._meta.get_field(
            "subject"
        ).max_length
        assert max_length == 150

    def test_get_absolute_url(self, proto_private_message):
        """get_absolute_url() should be redirected to home page."""
        assert proto_private_message.get_absolute_url() == "/messages/inbox/"
