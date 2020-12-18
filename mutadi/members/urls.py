"""members URL Configuration
"""
from django.urls import include, path

from .views import user_register_view, user_edit_view

urlpatterns = [
    path("register/", user_register_view, name="register"),
    path("", include("django.contrib.auth.urls")),
    path("edit_profile/", user_edit_view, name="edit_profile"),
]
