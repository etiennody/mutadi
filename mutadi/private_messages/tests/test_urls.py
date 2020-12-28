"""Unit tests for posts app urls
"""
import pytest
from django.urls import resolve, reverse

pytestmark = pytest.mark.django_db


class TestPrivateMessageUrls:
    """Group multiple tests for Private Message urls"""

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
