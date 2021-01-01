"""pages Views Configuration"""
from django.shortcuts import render
from django.views.generic import ListView
from mutadi.posts.models import Post


class HomeView(ListView):
    """Home page view"""

    model = Post
    template_name = "pages/home.html"

    def get_context_data(self, **kwargs):
        featured_posts = Post.objects.filter(featured=True).order_by(
            "-created_on"
        )[:3]
        latest_posts = Post.objects.order_by("-created_on")[:3]
        context = super().get_context_data(**kwargs)
        context["featured_posts"] = featured_posts
        context["latest_posts"] = latest_posts
        return context


home_view = HomeView.as_view()


def tos(request):
    """
    Here’s a view that returns the current terms of service,
    as an HTML document
    """
    context = {}
    return render(request, "pages/tos.html", context)
