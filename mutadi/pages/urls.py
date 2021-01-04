"""pages URL Configuration
"""
from django.urls import path

from .views import home_view, how, tos

urlpatterns = [
    path("", home_view, name="home"),
    path("tos/", tos, name="tos"),
    path("how/", how, name="how"),
]
