"""posts Views Configuration"""
from django.views.generic import ListView
from .models import Post


class PostListView(ListView):
    """Post list view"""

    model = Post
    template_name = "posts/post_list.html"


post_list_view = PostListView.as_view()
