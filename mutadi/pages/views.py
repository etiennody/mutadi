"""pages Views Configuration"""
from django.views.generic import TemplateView


class HomeView(TemplateView):
    """Home page view"""

    template_name = "pages/home.html"


home_view = HomeView.as_view()
