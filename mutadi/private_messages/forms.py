"""Private messages Forms Configuration"""
from django import forms
from .models import PrivateMessage


class ComposeForm(forms.ModelForm):
    """Compose message form"""

    class Meta:
        model = PrivateMessage
        fields = (
            "subject",
            "recipient",
            "content",
        )
        widgets = {
            "subject": forms.TextInput(attrs={"class": "form-control"}),
            "recipient": forms.Select(attrs={"class": "form-control"}),
            "content": forms.Textarea(attrs={"class": "form-control"}),
        }
        labels = {
            "subject": "Sujet",
            "recipient": "Destinataire",
            "content": "Contenu",
        }
