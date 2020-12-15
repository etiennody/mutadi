"""pages Views Configuration"""
from django.views.generic import ListView, TemplateView
from mutadi.posts.models import Post


class HomeView(ListView):
    """Home page view"""

    template_name = "pages/home.html"
    queryset = Post.objects.filter(featured=True)


home_view = HomeView.as_view()
