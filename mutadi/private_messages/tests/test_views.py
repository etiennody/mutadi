"""Unit tests for private_messgaes app views
"""
import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from model_bakery import baker
from pytest_django.asserts import assertTemplateUsed

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
        """inbox page should exist at desired location."""
        client.login(
            username=f"{proto_user.username}",
            password="m=9UaK^C,Tbq9N=T",
        )
        response = client.get("/messages/inbox/")
        assert response.status_code == 200

    def test_view_url_accessible_by_name(self, client, proto_user):
        """inbox page should be accessible by name."""
        client.login(
            username=f"{proto_user.username}",
            password="m=9UaK^C,Tbq9N=T",
        )
        url = reverse("inbox")
        response = client.get(url)
        assert response.status_code == 200

    def test_valid_inbox_page_title_with_client(self, client, proto_user):
        """inbox page should contain "Publications"."""
        client.login(
            username=f"{proto_user.username}",
            password="m=9UaK^C,Tbq9N=T",
        )
        url = reverse("inbox")
        response = client.get(url)
        assert "Publications" in str(response.content)

    def test_view_inbox_page_uses_correct_template(self, client, proto_user):
        """inbox page should use inbox.html template."""
        client.login(
            username=f"{proto_user.username}",
            password="m=9UaK^C,Tbq9N=T",
        )
        response = client.get(reverse("inbox"))
        assert response.status_code == 200
        assertTemplateUsed(response, "inbox.html")

    def test_view_message_list_context_is_ko(self, client, proto_user):
        """Inbow should have no messages"""
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
        """outbox page should exist at desired location."""
        client.login(
            username=f"{proto_user.username}",
            password="m=9UaK^C,Tbq9N=T",
        )
        response = client.get("/messages/outbox/")
        assert response.status_code == 200

    def test_view_url_accessible_by_name(self, client, proto_user):
        """outbox page should be accessible by name."""
        client.login(
            username=f"{proto_user.username}",
            password="m=9UaK^C,Tbq9N=T",
        )
        url = reverse("outbox")
        response = client.get(url)
        assert response.status_code == 200

    def test_valid_outbox_page_title_with_client(self, client, proto_user):
        """outbox page should contain "Publications"."""
        client.login(
            username=f"{proto_user.username}",
            password="m=9UaK^C,Tbq9N=T",
        )
        url = reverse("outbox")
        response = client.get(url)
        assert "Publications" in str(response.content)

    def test_view_outbox_page_uses_correct_template(self, client, proto_user):
        """outbox page should use outbox.html template."""
        client.login(
            username=f"{proto_user.username}",
            password="m=9UaK^C,Tbq9N=T",
        )
        response = client.get(reverse("outbox"))
        assert response.status_code == 200
        assertTemplateUsed(response, "outbox.html")

    def test_view_message_list_context_is_ko(self, client, proto_user):
        """Inbow should have no messages"""
        client.login(
            username=f"{proto_user.username}",
            password="m=9UaK^C,Tbq9N=T",
        )
        response = client.get(reverse("outbox"))
        assert response.context_data["message_list"].count() == 0
