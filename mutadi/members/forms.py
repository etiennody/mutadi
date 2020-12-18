"""members Foms Configuration"""
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django import forms


class SignUpForm(UserCreationForm):
    """Sign Up form"""

    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={"class": "form-control"},
        ),
        label="E-mail",
    )
    first_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={"class": "form-control"}),
        label="Prénom",
    )
    last_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={"class": "form-control"}),
        label="Nom",
    )

    class Meta:
        model = User
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
        )

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        self.fields["username"].widget.attrs["class"] = "form-control"
        self.fields["password1"].widget.attrs["class"] = "form-control"
        self.fields["password2"].widget.attrs["class"] = "form-control"
        self.fields["username"].label = "Nom d'utilisateur"
        self.fields["password1"].label = "Mot de passe"
        self.fields["password2"].label = "Confirmation du mot de passe"


class EditProfileForm(UserChangeForm):
    """Edit profile form"""

    username = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={"class": "form-control"}),
        label="Nom d'utilisateur",
    )
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={"class": "form-control"},
        ),
        label="E-mail",
    )
    first_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={"class": "form-control"}),
        label="Prénom",
    )
    last_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={"class": "form-control"}),
        label="Nom",
    )
    # is_actif = forms.CharField(
    #     max_length=100,
    #     widget=forms.CheckboxInput(attrs={"class": "form-check"}),
    #     label="Actif",
    # )

    class Meta:
        model = User
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "password",
            # "is_actif",
        )
