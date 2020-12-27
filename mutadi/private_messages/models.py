"""private_messages Models Configuration"""
from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone

User = get_user_model()


class Conversation(models.Model):
    subject = models.CharField(max_length=150)
    participants = models.ManyToManyField(User)


class PrivateMessage(models.Model):
    sender = models.ForeignKey(
        User, related_name="sent_messages", on_delete=models.CASCADE
    )
    recipient = models.ManyToManyField(User, related_name="received_messages")
    sent_at = models.DateTimeField(default=timezone.now)
    content = models.TextField()
    conversation = models.ForeignKey(
        Conversation, blank=False, null=False, on_delete=models.CASCADE
    )

    class Meta:
        ordering = ["sent_at"]

    def __str__(self):
        return f"{self.sender} to {self.receiver} : {self.content}"