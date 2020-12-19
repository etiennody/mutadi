"""members URL Configuration
"""
from django.urls import include, path

from .views import (
    change_password_success,
    change_password_view,
    user_edit_view,
    user_register_view,
)

urlpatterns = [
    path("register/", user_register_view, name="register"),
    path("", include("django.contrib.auth.urls")),
    path("edit_profile/", user_edit_view, name="edit_profile"),
    path("password/", change_password_view, name="change_password"),
    path(
        "change_password_success/",
        change_password_success,
        name="change_password_success",
    ),
]
