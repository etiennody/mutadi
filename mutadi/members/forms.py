"""members Foms Configuration"""
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import (
    PasswordChangeForm,
    UserChangeForm,
    UserCreationForm,
)

User = get_user_model()


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


class EditUserSettingsForm(UserChangeForm):
    """Edit user settings form"""

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

    class Meta:
        model = User
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "password",
        )


class PasswordChangingForm(PasswordChangeForm):
    """Password changing form"""

    old_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "type": "password"}
        ),
        label="Ancien mot de passe",
    )
    new_password1 = forms.CharField(
        max_length=128,
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "type": "password"}
        ),
        label="Nouveau mot de passe",
    )
    new_password2 = forms.CharField(
        max_length=128,
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "type": "password"}
        ),
        label="Confirmation du nouveau mot de passe",
    )

    class Meta:
        model = User
        fields = ("old_password", "new_password1", "new_password2")
