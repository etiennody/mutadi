"""Unit tests for posts app urls
"""
import pytest
from django.contrib.auth import get_user_model
from django.urls import resolve, reverse
from model_bakery import baker
from mutadi.private_messages.models import PrivateMessage

pytestmark = pytest.mark.django_db

User = get_user_model()


class TestPrivateMessageUrls:
    """Group multiple tests for Private Message urls"""

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

    def test_inbox_reverse(self):
        """inbox should reverse to /messages/inbox/."""
        assert reverse("inbox") == "/messages/inbox/"

    def test_inbox_resolve(self):
        """/messages/inbox/ should resolve to inbox."""
        assert resolve("/messages/inbox/").view_name == "inbox"

    def test_outbox_reverse(self):
        """outbox should reverse to /messages/outbox/."""
        assert reverse("outbox") == "/messages/outbox/"

    def test_outbox_resolve(self):
        """/messages/outbox/ should resolve to outbox."""
        assert resolve("/messages/outbox/").view_name == "outbox"

    def test_delete_message_reverse(self, proto_private_message):
        """
        delete_message should reverse to
        /messages/message_detail/{proto_private_message.pk}/delete.
        """
        assert (
            reverse(
                "delete_message",
                args=[
                    f"{proto_private_message.pk}",
                ],
            )
            == f"/messages/message_detail/{proto_private_message.pk}/delete"
        )

    def test_delete_message_resolve(self, proto_private_message):
        """
        /messages/message_detail/{proto_private_message.pk}/delete
        should resolve to delete_message.
        """
        assert (
            resolve(
                f"/messages/message_detail/{proto_private_message.pk}/delete"
            ).view_name
            == "delete_message"
        )

    def test_message_detail_reverse(self, proto_private_message):
        """
        message_detail should reverse to
        /messages/message_detail/{proto_private_message.pk}.
        """
        assert (
            reverse(
                "message_detail",
                args=[
                    f"{proto_private_message.pk}",
                ],
            )
            == f"/messages/message_detail/{proto_private_message.pk}"
        )

    def test_message_detail_resolve(self, proto_private_message):
        """
        /messages/message_detail/{proto_private_message.pk}
        should resolve to message_detail.
        """
        assert (
            resolve(
                f"/messages/message_detail/{proto_private_message.pk}"
            ).view_name
            == "message_detail"
        )
