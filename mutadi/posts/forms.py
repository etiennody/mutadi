"""posts Forms Configuration"""
from django import forms
from .models import Comment, Post


class PostForm(forms.ModelForm):
    """Add post form"""

    class Meta:
        model = Post
        fields = (
            "title",
            "categories",
            "overview",
            "content",
            "thumbnail",
            "featured",
            "status",
        )
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "categories": forms.CheckboxSelectMultiple(
                attrs={"class": "list-unstyled"}
            ),
            "overview": forms.TextInput(attrs={"class": "form-control"}),
            "content": forms.Textarea(attrs={"class": "form-control"}),
            "featured": forms.CheckboxInput,
            "status": forms.Select(attrs={"class": "form-control"}),
        }
        labels = {
            "title": "Titre",
            "categories": "Catégories",
            "overview": "Présentation",
            "content": "Contenu",
            "thumbnail": "Image",
            "featured": "Mise en avant",
            "status": "Statut",
        }


class EditForm(forms.ModelForm):
    """Update post form"""

    class Meta:
        model = Post
        fields = (
            "title",
            "categories",
            "overview",
            "content",
            "thumbnail",
            "featured",
            "status",
        )
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "categories": forms.CheckboxSelectMultiple(
                attrs={"class": "list-unstyled"}
            ),
            "overview": forms.TextInput(attrs={"class": "form-control"}),
            "content": forms.Textarea(attrs={"class": "form-control"}),
            "featured": forms.CheckboxInput,
            "status": forms.Select(attrs={"class": "form-control"}),
        }
        labels = {
            "title": "Titre",
            "categories": "Catégories",
            "overview": "Présentation",
            "content": "Contenu",
            "thumbnail": "Image",
            "featured": "Mise en avant",
            "status": "Statut",
        }


class CommentForm(forms.ModelForm):
    """Comment form"""

    class Meta:
        model = Comment
        fields = ("content",)
        widgets = {
            "content": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Ajouter un commentaire",
                    "id": "usercomment",
                    "rows": "4",
                }
            ),
        }
        labels = {
            "content": "Contenu",
        }
