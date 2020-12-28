"""private_messages URL Configuration
"""
from django.urls import path

from .views import delete_message_view, inbox_view, outbox_view

urlpatterns = [
    path("inbox/", inbox_view, name="inbox"),
    path("outbox/", outbox_view, name="outbox"),
    path(
        "message_detail/<int:pk>/delete",
        delete_message_view,
        name="delete_message",
    ),
]
