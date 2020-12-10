"""members URL Configuration
"""
from django.urls import path, include
from .views import user_register_view

urlpatterns = [
    path("register/", user_register_view, name="register"),
    path("", include("django.contrib.auth.urls")),
]
