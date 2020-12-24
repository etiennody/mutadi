"""posts Models Configuration"""
from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import post_save
from django.urls import reverse

User = get_user_model()


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(default="Plaisir d'aider ou de se faire aider !!")
    profile_pic = models.ImageField(
        default="default_profile_picture.jpg", upload_to="images/profile/"
    )

    def __str__(self):
        return str(self.user)

    def get_absolute_url(self):
        """get_absolute_url function allows to redirect to the home page."""
        return reverse("home")


def create_user_profile(sender, **kwargs):
    user = kwargs["instance"]
    if kwargs["created"]:
        user_profile = Profile(user=user)
        user_profile.save()


post_save.connect(create_user_profile, sender=User)
