"""posts Views Configuration"""
from django.views.generic import DetailView, ListView

from .models import Post


class PostListView(ListView):
    """Post list view"""

    queryset = Post.objects.filter(status=1).order_by("-created_on")
    template_name = "posts/post_list.html"


post_list_view = PostListView.as_view()


class PostDetailView(DetailView):
    """Post detail view"""

    model = Post
    template_name = "posts/post_detail.html"


post_detail_view = PostDetailView.as_view()
