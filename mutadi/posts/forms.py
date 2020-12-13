"""posts Forms Configuration"""
from django import forms
from .models import Post


class PostForm(forms.ModelForm):
    """Add post form"""

    class Meta:
        model = Post
        fields = "__all__"
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "author": forms.Select(attrs={"class": "form-control"}),
            "categories": forms.CheckboxSelectMultiple,
            "overview": forms.TextInput(attrs={"class": "form-control"}),
            "content": forms.Textarea(attrs={"class": "form-control"}),
            "featured": forms.CheckboxInput,
            "status": forms.Select(attrs={"class": "form-control"}),
        }
        labels = {
            "title": "Titre",
            "author": "Auteur",
            "categories": "Catégories",
            "overview": "Présentation",
            "content": "Contenu",
            "thumbnail": "Image",
            "featured": "Mise en avant",
            "status": "Statut",
        }