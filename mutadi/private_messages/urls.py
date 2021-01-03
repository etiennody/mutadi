"""private_messages URL configuration"""
from django.urls import path

from .views import (
    compose_message_view,
    delete_message,
    inbox_view,
    message_detail_view,
    outbox_view,
)

urlpatterns = [
    path("inbox/", inbox_view, name="inbox"),
    path("outbox/", outbox_view, name="outbox"),
    path(
        "message_detail/<int:pk>/delete",
        delete_message,
        name="delete_message",
    ),
    path(
        "message_detail/<int:pk>",
        message_detail_view,
        name="message_detail",
    ),
    path(
        "compose_message/",
        compose_message_view,
        name="compose_message",
    ),
]
