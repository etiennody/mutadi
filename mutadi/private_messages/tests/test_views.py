"""Unit tests for private_messgaes app views
"""
import pytest
from django.contrib.auth import get_user_model
from django.test import RequestFactory
from django.urls import reverse
from model_bakery import baker
from mutadi.private_messages.models import PrivateMessage
from pytest_django.asserts import assertRedirects, assertTemplateUsed

from mutadi.private_messages.views import compose_message_view

pytestmark = pytest.mark.django_db

User = get_user_model()

factory = RequestFactory()


class TestInboxViews:
    """Group multiple tests in Inbox views"""

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

    @pytest.fixture
    def proto_user_c(self):
        """Fixture for baked User model."""
        self.proto_user_c = baker.make(User)
        self.proto_user_c.set_password("BJw_KkB&asjX_#B3")
        self.proto_user_c.save()
        return self.proto_user_c

    @pytest.fixture
    def proto_private_message(self, proto_user_a, proto_user_b):
        """Fixture for baked PrivateMessage model."""
        return baker.make(
            PrivateMessage,
            sender=proto_user_a,
            recipient=proto_user_b,
            content=(
                "Proident nisi cillum sit tempor "
                "reprehenderit proident in non fugiat ex id."
            ),
            _quantity=26,
        )

    def test_view_url_inbox_page_exists_at_desired_location(
        self, client, proto_user_a
    ):
        """Inbox page should exist at desired location."""
        client.login(
            username=f"{proto_user_a.username}",
            password="m=9UaK^C,Tbq9N=T",
        )
        response = client.get("/messages/inbox/")
        assert response.status_code == 200

    def test_view_url_accessible_by_name(self, client, proto_user_a):
        """Inbox page should be accessible by name."""
        client.login(
            username=f"{proto_user_a.username}",
            password="m=9UaK^C,Tbq9N=T",
        )
        url = reverse("inbox")
        response = client.get(url)
        assert response.status_code == 200

    def test_valid_inbox_page_title_with_client(self, client, proto_user_a):
        """Inbox page should contain "Mes messages"."""
        client.login(
            username=f"{proto_user_a.username}",
            password="m=9UaK^C,Tbq9N=T",
        )
        url = reverse("inbox")
        response = client.get(url)
        assert b"Mes messages re\xc3\xa7us" in response.content

    def test_view_inbox_page_uses_correct_template(self, client, proto_user_a):
        """Inbox page should use inbox.html template."""
        client.login(
            username=f"{proto_user_a.username}",
            password="m=9UaK^C,Tbq9N=T",
        )
        response = client.get(reverse("inbox"))
        assert response.status_code == 200
        assertTemplateUsed(response, "inbox.html")

    def test_view_message_list_context_inbox_is_ok(
        self, client, proto_private_message, proto_user_b
    ):
        """Inbox should have a message."""
        client.login(
            username=f"{proto_user_b.username}",
            password="3$0aF/gxFsinR'6k",
        )
        response = client.get(reverse("inbox"))
        assert response.context["message_list"].count() == 26

    def test_view_message_list_context_is_ko(
        self, client, proto_private_message, proto_user_c
    ):
        """Inbox should have no messages."""
        client.login(
            username=f"{proto_user_c.username}",
            password="BJw_KkB&asjX_#B3",
        )
        response = client.get(reverse("inbox"))
        assert response.context_data["message_list"].count() == 0

    def test_valid_private_massage_inbox_pagination_is_25(
        self, client, proto_private_message, proto_user_b
    ):
        """Valid if inbox page pagination have 25 messages on page"""
        client.login(
            username=f"{proto_user_b.username}",
            password="3$0aF/gxFsinR'6k",
        )
        response = client.get(reverse("inbox"))
        assert response.status_code == 200
        assert "is_paginated" in response.context
        assert (len(response.context["page_obj"])) == 25


class TestOutboxViews:
    """Group multiple tests in Outbox views"""

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

    @pytest.fixture
    def proto_user_c(self):
        """Fixture for baked User model."""
        self.proto_user_c = baker.make(User)
        self.proto_user_c.set_password("BJw_KkB&asjX_#B3")
        self.proto_user_c.save()
        return self.proto_user_c

    @pytest.fixture
    def proto_user_d(self):
        """Fixture for baked User model."""
        self.proto_user_d = baker.make(User)
        self.proto_user_d.set_password("BJw_KkB&asjX_#B3")
        self.proto_user_d.save()
        return self.proto_user_d

    @pytest.fixture
    def proto_private_message(self, proto_user_a, proto_user_b):
        """Fixture for baked PrivateMessage model."""
        return baker.make(
            PrivateMessage,
            sender=proto_user_a,
            recipient=proto_user_b,
            content=(
                "Proident nisi cillum sit tempor "
                "reprehenderit proident in non fugiat ex id."
            ),
        )

    @pytest.fixture
    def proto_private_message_bis(self, proto_user_d, proto_user_a):
        """Fixture for baked PrivateMessage model."""
        return baker.make(
            PrivateMessage,
            sender=proto_user_d,
            recipient=proto_user_a,
            content=(
                "Proident nisi cillum sit tempor "
                "reprehenderit proident in non fugiat ex id."
            ),
            _quantity=26,
        )

    def test_view_url_outbox_page_exists_at_desired_location(
        self, client, proto_user_a
    ):
        """Outbox page should exist at desired location."""
        client.login(
            username=f"{proto_user_a.username}",
            password="m=9UaK^C,Tbq9N=T",
        )
        response = client.get("/messages/outbox/")
        assert response.status_code == 200

    def test_view_url_accessible_by_name(self, client, proto_user_a):
        """Outbox page should be accessible by name."""
        client.login(
            username=f"{proto_user_a.username}",
            password="m=9UaK^C,Tbq9N=T",
        )
        url = reverse("outbox")
        response = client.get(url)
        assert response.status_code == 200

    def test_valid_outbox_page_title_with_client(self, client, proto_user_a):
        """Outbox page should contain "Mes messages"."""
        client.login(
            username=f"{proto_user_a.username}",
            password="m=9UaK^C,Tbq9N=T",
        )
        url = reverse("outbox")
        response = client.get(url)
        assert b"Mes messages envoy\xc3\xa9s" in response.content

    def test_view_outbox_page_uses_correct_template(
        self, client, proto_user_a
    ):
        """Outbox page should use outbox.html template."""
        client.login(
            username=f"{proto_user_a.username}",
            password="m=9UaK^C,Tbq9N=T",
        )
        response = client.get(reverse("outbox"))
        assert response.status_code == 200
        assertTemplateUsed(response, "outbox.html")

    def test_view_message_list_context_outbox_is_ok(
        self, client, proto_private_message, proto_user_a
    ):
        """Outbox should have a message."""
        client.login(
            username=f"{proto_user_a.username}",
            password="m=9UaK^C,Tbq9N=T",
        )
        response = client.get(reverse("outbox"))
        assert response.context["message_list"].count() == 1

    def test_view_message_list_context_is_ko(self, client, proto_user_c):
        """Outbox should have no messages."""
        client.login(
            username=f"{proto_user_c.username}",
            password="BJw_KkB&asjX_#B3",
        )
        response = client.get(reverse("outbox"))
        assert response.context_data["message_list"].count() == 0

    def test_valid_private_massage_outbox_pagination_is_25(
        self, client, proto_private_message_bis, proto_user_d
    ):
        """Valid if outbox page pagination have 25 messages on single page"""
        client.login(
            username=f"{proto_user_d.username}",
            password="BJw_KkB&asjX_#B3",
        )
        response = client.get(reverse("outbox"))
        assert response.status_code == 200
        assert "is_paginated" in response.context
        assert (len(response.context["page_obj"])) == 25


class TestDeleteMessageViews:
    """Group multiple tests in DeleteMessage views"""

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

    @pytest.fixture
    def proto_user_c(self):
        """Fixture for baked User model."""
        self.proto_user_c = baker.make(User)
        self.proto_user_c.set_password("BJw_KkB&asjX_#B3")
        self.proto_user_c.save()
        return self.proto_user_c

    @pytest.fixture
    def proto_private_message(self, proto_user_a, proto_user_b):
        """Fixture for baked PrivateMessage model."""
        return baker.make(
            PrivateMessage,
            sender=proto_user_a,
            recipient=proto_user_b,
            content=(
                "Proident nisi cillum sit tempor "
                "reprehenderit proident in non fugiat ex id."
            ),
        )

    def test_view_url_delete_message_page_exists_at_desired_location(
        self, client, proto_user_a, proto_private_message
    ):
        """delete_message page should exist at desired location."""
        client.login(
            username=f"{proto_user_a.username}",
            password="m=9UaK^C,Tbq9N=T",
        )
        response = client.get(
            f"/messages/message_detail/{proto_private_message.id}/delete"
        )
        assert response.status_code == 200

    def test_view_url_accessible_by_name(
        self, client, proto_user_a, proto_private_message
    ):
        """delete_message page should be accessible by name."""
        client.login(
            username=f"{proto_user_a.username}",
            password="m=9UaK^C,Tbq9N=T",
        )
        url = reverse(
            "delete_message",
            args=[
                f"{proto_private_message.pk}",
            ],
        )
        response = client.get(url)
        assert response.status_code == 200

    def test_valid_delete_message_page_with_correct_user(
        self, client, proto_user_a, proto_private_message
    ):
        """delete_message page should contain the subject of the message."""
        client.login(
            username=f"{proto_user_a.username}",
            password="m=9UaK^C,Tbq9N=T",
        )
        url = reverse(
            "delete_message",
            args=[
                f"{proto_private_message.pk}",
            ],
        )
        response = client.get(url)
        assert (
            b"Message supprim\xc3\xa9 avec succ\xc3\xa8s !" in response.content
        )

    def test_invalid_delete_message_page_with_wrong_user(
        self, client, proto_user_c, proto_private_message
    ):
        """delete_message page should contain the title of the message."""
        client.login(
            username=f"{proto_user_c.username}",
            password="BJw_KkB&asjX_#B3",
        )
        url = reverse(
            "delete_message",
            args=[
                f"{proto_private_message.pk}",
            ],
        )
        response = client.get(url)
        assert (
            b"Message supprim\xc3\xa9 avec succ\xc3\xa8s !"
            not in response.content
        )


class TestMessageDetailViews:
    """Group multiple tests in MessageDetail views"""

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
        self.proto_user_b.set_password("m=9UaK^C,Tbq9N=T")
        self.proto_user_b.save()
        return self.proto_user_b

    @pytest.fixture
    def proto_private_message(self, proto_user_a, proto_user_b):
        """Fixture for baked PrivateMessage model."""
        return baker.make(
            PrivateMessage,
            sender=proto_user_a,
            recipient=proto_user_b,
            content=(
                "Proident nisi cillum sit tempor "
                "reprehenderit proident in non fugiat ex id."
            ),
        )

    def test_view_url_message_detail_page_exists_at_desired_location(
        self, client, proto_private_message, proto_user_a
    ):
        """message_detail page should exist at desired location."""
        client.login(
            username=f"{proto_user_a.username}",
            password="m=9UaK^C,Tbq9N=T",
        )
        response = client.get(
            f"/messages/message_detail/{proto_private_message.pk}"
        )
        assert response.status_code == 200

    def test_view_url_accessible_by_name(
        self, client, proto_private_message, proto_user_a
    ):
        """message_detail page should be accessible by name."""
        client.login(
            username=f"{proto_user_a.username}",
            password="m=9UaK^C,Tbq9N=T",
        )
        url = reverse(
            "message_detail",
            args=[
                f"{proto_private_message.pk}",
            ],
        )
        response = client.get(url)
        assert response.status_code == 200

    def test_valid_message_detail_page_subject_with_client(
        self, client, proto_private_message, proto_user_a
    ):
        """message_detail page should contain the subject of the message."""
        client.login(
            username=f"{proto_user_a.username}",
            password="m=9UaK^C,Tbq9N=T",
        )
        url = reverse(
            "message_detail",
            args=[
                f"{proto_private_message.pk}",
            ],
        )
        response = client.get(url)
        assert proto_private_message.subject in str(response.content)

    def test_view_message_detail_page_uses_correct_template(
        self, client, proto_private_message, proto_user_a
    ):
        """message_detail page should use message_detail.html template."""
        client.login(
            username=f"{proto_user_a.username}",
            password="m=9UaK^C,Tbq9N=T",
        )
        url = reverse(
            "message_detail",
            args=[
                f"{proto_private_message.pk}",
            ],
        )
        response = client.get(url)
        assert response.status_code == 200
        assertTemplateUsed(response, "message_detail.html")

    class TestComposeMessageViews:
        """Group multiple tests in ComposeMessage views"""

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

        @pytest.fixture
        def proto_private_message(self, proto_user_a, proto_user_b):
            """Fixture for baked PrivateMessage model."""
            return baker.make(
                PrivateMessage,
                sender=proto_user_a,
                recipient=proto_user_b,
                content=(
                    "Proident nisi cillum sit tempor "
                    "reprehenderit proident in non fugiat ex id."
                ),
            )

        def test_view_url_compose_message_page_exists_at_desired_location(
            self, client, proto_user_a
        ):
            """compose_message page should exist at desired location."""
            client.login(
                username=f"{proto_user_a.username}",
                password="m=9UaK^C,Tbq9N=T",
            )
            response = client.get("/messages/compose_message/")
            assert response.status_code == 200

        def test_view_url_accessible_by_name(self, client, proto_user_a):
            """compose_message page should be accessible by name."""
            client.login(
                username=f"{proto_user_a.username}",
                password="m=9UaK^C,Tbq9N=T",
            )
            url = reverse("compose_message")
            response = client.get(url)
            assert response.status_code == 200

        def test_valid_compose_message_page_with_correct_user(
            self, client, proto_user_a, proto_private_message
        ):
            """compose_message page should contain the subject of the message."""
            client.login(
                username=f"{proto_user_a.username}",
                password="m=9UaK^C,Tbq9N=T",
            )
            url = reverse("compose_message")
            response = client.get(url)
            assert "Envoyer" in str(response.content)

        def test_invalid_compose_message_page_with_anonymous_user(
            self, client, proto_private_message
        ):
            """compose_message page should contain the title of the message."""
            url = reverse("compose_message")
            response = client.get(url)
            assert proto_private_message.subject not in str(response.content)
            assert response.status_code == 302
            assert (
                response.url
                == "/members/login/?next=/messages/compose_message/"
            )

        def test_view_compose_message_page_uses_correct_template(
            self, client, proto_user_a
        ):
            """compose_message page should use compose_message.html template."""
            client.login(
                username=f"{proto_user_a.username}",
                password="m=9UaK^C,Tbq9N=T",
            )
            url = reverse("compose_message")
            response = client.get(url)
            assert response.status_code == 200
            assertTemplateUsed(response, "compose_message.html")

        def test_compose_message_valid_compose_message_view(
            self, client, proto_user_a, proto_user_b
        ):
            """compose_message page should valid compose_message_view."""
            client.login(
                username=f"{proto_user_a.username}",
                password="m=9UaK^C,Tbq9N=T",
            )
            data = {
                "subject": "This is the subject",
                "recipient": proto_user_b,
                "content": (
                    "Culpa est et aliquip non tempor "
                    "mollit exercitation cillum et."
                ),
            }
            user = proto_user_a
            request = factory.post("/messages/compose/", data=data)
            request.user = user
            response = compose_message_view(request)
            assert response
            assert response.status_code == 200
