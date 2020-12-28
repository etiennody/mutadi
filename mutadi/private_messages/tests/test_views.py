"""Unit tests for private_messgaes app views
"""
import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from model_bakery import baker
from pytest_django.asserts import assertTemplateUsed

from mutadi.private_messages.models import PrivateMessage

pytestmark = pytest.mark.django_db

User = get_user_model()


class TestInboxViews:
    """Group multiple tests in Inbox views"""

    @pytest.fixture
    def proto_user(self):
        """Fixture for baked User model."""
        self.proto_user = baker.make(User)
        self.proto_user.set_password("m=9UaK^C,Tbq9N=T")
        self.proto_user.save()
        return self.proto_user

    def test_view_url_inbox_page_exists_at_desired_location(
        self, client, proto_user
    ):
        """Inbox page should exist at desired location."""
        client.login(
            username=f"{proto_user.username}",
            password="m=9UaK^C,Tbq9N=T",
        )
        response = client.get("/messages/inbox/")
        assert response.status_code == 200

    def test_view_url_accessible_by_name(self, client, proto_user):
        """Inbox page should be accessible by name."""
        client.login(
            username=f"{proto_user.username}",
            password="m=9UaK^C,Tbq9N=T",
        )
        url = reverse("inbox")
        response = client.get(url)
        assert response.status_code == 200

    def test_valid_inbox_page_title_with_client(self, client, proto_user):
        """Inbox page should contain "Mes messages"."""
        client.login(
            username=f"{proto_user.username}",
            password="m=9UaK^C,Tbq9N=T",
        )
        url = reverse("inbox")
        response = client.get(url)
        assert "Mes messages" in str(response.content)

    def test_view_inbox_page_uses_correct_template(self, client, proto_user):
        """Inbox page should use inbox.html template."""
        client.login(
            username=f"{proto_user.username}",
            password="m=9UaK^C,Tbq9N=T",
        )
        response = client.get(reverse("inbox"))
        assert response.status_code == 200
        assertTemplateUsed(response, "inbox.html")

    def test_view_message_list_context_is_ko(self, client, proto_user):
        """Inbox should have no messages."""
        client.login(
            username=f"{proto_user.username}",
            password="m=9UaK^C,Tbq9N=T",
        )
        response = client.get(reverse("inbox"))
        assert response.context_data["message_list"].count() == 0


class TestOutboxViews:
    """Group multiple tests in Outbox views"""

    @pytest.fixture
    def proto_user(self):
        """Fixture for baked User model."""
        self.proto_user = baker.make(User)
        self.proto_user.set_password("m=9UaK^C,Tbq9N=T")
        self.proto_user.save()
        return self.proto_user

    def test_view_url_outbox_page_exists_at_desired_location(
        self, client, proto_user
    ):
        """Outbox page should exist at desired location."""
        client.login(
            username=f"{proto_user.username}",
            password="m=9UaK^C,Tbq9N=T",
        )
        response = client.get("/messages/outbox/")
        assert response.status_code == 200

    def test_view_url_accessible_by_name(self, client, proto_user):
        """Outbox page should be accessible by name."""
        client.login(
            username=f"{proto_user.username}",
            password="m=9UaK^C,Tbq9N=T",
        )
        url = reverse("outbox")
        response = client.get(url)
        assert response.status_code == 200

    def test_valid_outbox_page_title_with_client(self, client, proto_user):
        """Outbox page should contain "Mes messages"."""
        client.login(
            username=f"{proto_user.username}",
            password="m=9UaK^C,Tbq9N=T",
        )
        url = reverse("outbox")
        response = client.get(url)
        assert "Mes messages" in str(response.content)

    def test_view_outbox_page_uses_correct_template(self, client, proto_user):
        """Outbox page should use outbox.html template."""
        client.login(
            username=f"{proto_user.username}",
            password="m=9UaK^C,Tbq9N=T",
        )
        response = client.get(reverse("outbox"))
        assert response.status_code == 200
        assertTemplateUsed(response, "outbox.html")

    def test_view_message_list_context_is_ko(self, client, proto_user):
        """Outbox should have no messages."""
        client.login(
            username=f"{proto_user.username}",
            password="m=9UaK^C,Tbq9N=T",
        )
        response = client.get(reverse("outbox"))
        assert response.context_data["message_list"].count() == 0


class TestDeleteMessageViews:
    """Group multiple tests in DeleteMessage views"""

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
            PrivateMessage, sender=proto_user[0], recipient=proto_user[1]
        )

    def test_view_url_delete_message_page_exists_at_desired_location(
        self, client, proto_private_message
    ):
        """delete_message page should exist at desired location."""
        response = client.get(
            f"/messages/message_detail/{proto_private_message.id}/delete"
        )
        assert response.status_code == 200

    def test_view_url_accessible_by_name(self, client, proto_private_message):
        """delete_message page should be accessible by name."""
        url = reverse(
            "delete_message",
            args=[
                f"{proto_private_message.pk}",
            ],
        )
        response = client.get(url)
        assert response.status_code == 200

    def test_invalid_delete_message_page_with_wrong_user(
        self, client, proto_user
    ):
        """delete_message page should contain the title of the message."""
        proto_user_a = baker.make(User)
        proto_private_message_c = baker.make(
            PrivateMessage,
            sender=proto_user_a,
        )
        client.login(
            username=f"{proto_user[2].username}",
            password="m=9UaK^C,Tbq9N=T",
        )
        url = reverse(
            "delete_message",
            args=[
                f"{proto_private_message_c.pk}",
            ],
        )
        response = client.get(url)
        assert proto_private_message_c.subject not in str(response.content)

    def test_view_delete_message_page_uses_correct_template(
        self, client, proto_private_message
    ):
        """delete_message page should use delete_message.html template."""
        url = reverse(
            "delete_message",
            args=[
                f"{proto_private_message.pk}",
            ],
        )
        response = client.get(url)
        assert response.status_code == 200
        assertTemplateUsed(response, "delete_message.html")

    def test_delete_message_success_url(self, client, proto_private_message):
        """delete_message page should redirect to home page template."""
        response = client.post(
            f"/messages/message_detail/{proto_private_message.pk}/delete"
        )
        assert response.status_code == 302
        assert response.url == "/messages/inbox/"
