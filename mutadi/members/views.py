"""members Views Configuration"""
from django.contrib.auth.views import PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views import generic

from .forms import EditUserSettingsForm, PasswordChangingForm, SignUpForm
from .models import Profile


class UserRegisterView(SuccessMessageMixin, generic.CreateView):
    """User registration view"""

    form_class = SignUpForm
    template_name = "registration/register.html"
    success_url = reverse_lazy("login")
    success_message = "Le compte de %(username)s a été créé avec succès !"


user_register_view = UserRegisterView.as_view()


class UserSettingsEditView(SuccessMessageMixin, generic.UpdateView):
    """User settings edit view"""

    form_class = EditUserSettingsForm
    template_name = "registration/edit_user_settings.html"
    success_url = reverse_lazy("home")
    success_message = "Les réglages utilisateur ont été modifiés avec succès !"

    def get_object(self):
        return self.request.user


user_settings_edit_view = UserSettingsEditView.as_view()


class ChangePasswordView(PasswordChangeView):
    """Password change view"""

    form_class = PasswordChangingForm
    template_name = "registration/change_password.html"
    success_url = reverse_lazy("change_password_success")


change_password_view = ChangePasswordView.as_view()


def change_password_success(request):
    return render(request, "registration/change_password_success.html", {})


class ShowProfilePageView(generic.DetailView):
    """Show profile page view"""

    model = Profile
    template_name = "registration/user_profile.html"

    def get_context_data(self, *args, **kwargs):
        context = super(ShowProfilePageView, self).get_context_data(
            *args, **kwargs
        )
        page_user = get_object_or_404(Profile, id=self.kwargs["pk"])
        context["page_user"] = page_user
        return context


show_profile_page_view = ShowProfilePageView.as_view()


class UserProfileEditView(SuccessMessageMixin, generic.UpdateView):
    """User settings edit view"""

    model = Profile
    template_name = "registration/edit_user_profile.html"
    fields = ["bio", "profile_pic"]
    success_url = reverse_lazy("home")
    success_message = "Le profil utilisateur a été modifié avec succès !"


user_profile_edit_view = UserProfileEditView.as_view()
