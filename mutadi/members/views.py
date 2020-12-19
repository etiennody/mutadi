"""members Views Configuration"""
from django.contrib.auth.views import PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from .forms import EditProfileForm, PasswordChangingForm, SignUpForm


class UserRegisterView(SuccessMessageMixin, generic.CreateView):
    """User registration view"""

    form_class = SignUpForm
    template_name = "registration/register.html"
    success_url = reverse_lazy("login")
    success_message = "Le compte de %(username)s a été créé avec succès !"


user_register_view = UserRegisterView.as_view()


class UserEditView(SuccessMessageMixin, generic.UpdateView):
    """User registration view"""

    form_class = EditProfileForm
    template_name = "registration/edit_profile.html"
    success_url = reverse_lazy("home")
    success_message = "Le profil a été modifié avec succès !"

    def get_object(self):
        return self.request.user


user_edit_view = UserEditView.as_view()


class ChangePasswordView(PasswordChangeView):
    """Password change view"""

    form_class = PasswordChangingForm
    template_name = "registration/change_password.html"
    success_url = reverse_lazy("change_password_success")


change_password_view = ChangePasswordView.as_view()


def change_password_success(request):
    return render(request, "registration/change_password_success.html", {})
