"""members URL Configuration
"""
from django.urls import include, path

from .views import (
    change_password_success,
    change_password_view,
    # create_user_profile_view,
    show_profile_page_view,
    user_profile_edit_view,
    user_register_view,
    user_settings_edit_view,
)

urlpatterns = [
    path("register/", user_register_view, name="register"),
    path("", include("django.contrib.auth.urls")),
    path(
        "edit_user_settings/",
        user_settings_edit_view,
        name="edit_user_settings",
    ),
    path("password/", change_password_view, name="change_password"),
    path(
        "change_password_success/",
        change_password_success,
        name="change_password_success",
    ),
    path(
        "<int:pk>/profile/",
        show_profile_page_view,
        name="show_profile_page",
    ),
    path(
        "<int:pk>/edit_user_profile/",
        user_profile_edit_view,
        name="edit_user_profile",
    ),
]
