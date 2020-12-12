"""posts URL Configuration
"""
from django.urls import path

from .views import add_post_view, post_detail_view, post_list_view

urlpatterns = [
    path("post_list/", post_list_view, name="post_list"),
    path("post_detail/<int:pk>", post_detail_view, name="post_detail"),
    path("add_post/", add_post_view, name="add_post"),
]
