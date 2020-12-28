"""private_messages URL Configuration
"""
from django.urls import path

from .views import inbox_view, outbox_view

urlpatterns = [
    path("inbox/", inbox_view, name="inbox"),
    path("outbox/", outbox_view, name="outbox"),
]
