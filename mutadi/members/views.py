"""members Views Configuration"""
from django.contrib.auth.forms import UserCreationForm
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views import generic


class UserRegisterView(SuccessMessageMixin, generic.CreateView):
    """User registration view"""

    form_class = UserCreationForm
    template_name = "registration/register.html"
    success_url = reverse_lazy("login")
    success_message = "Le compte de %(username)s a été créé avec succès !"


user_register_view = UserRegisterView.as_view()
