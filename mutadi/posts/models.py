"""posts Models Configuration"""
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from ckeditor.fields import RichTextField


class Category(models.Model):
    title = models.CharField(max_length=20)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "categories"


class Comment(models.Model):
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(
        "Post", related_name="comments", on_delete=models.CASCADE
    )

    def __str__(self):
        return self.user.username


STATUS = ((0, "Non publié"), (1, "Publié"))


class Post(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    categories = models.ManyToManyField(Category)
    updated_on = models.DateTimeField(auto_now=True)
    overview = models.CharField(max_length=255)
    content = RichTextField()
    created_on = models.DateTimeField(auto_now_add=True)
    thumbnail = models.ImageField()
    featured = models.BooleanField()
    status = models.IntegerField(choices=STATUS, default=0)

    def __str__(self):
        return self.title + " | " + str(self.author)

    def get_absolute_url(self):
        """get_absolute_url function allows to redirect to the home page."""
        return reverse("home")
