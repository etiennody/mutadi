"""private_messages Models Configuration"""
from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from django.utils import timezone

User = get_user_model()


class PrivateMessage(models.Model):
    subject = models.CharField(max_length=150)
    sender = models.ForeignKey(
        User, related_name="sent_messages", on_delete=models.CASCADE
    )
    recipient = models.ForeignKey(
        User, related_name="received_messages", on_delete=models.CASCADE
    )
    sent_at = models.DateTimeField(default=timezone.now)
    content = models.TextField()

    class Meta:
        ordering = ["sent_at"]

    def __str__(self):
        return f"{self.sender} to {self.recipient} : {self.content}"

    def get_absolute_url(self):
        return reverse("inbox")
