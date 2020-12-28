"""Private Messages Views Configuration"""
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

from .models import PrivateMessage


class InboxView(LoginRequiredMixin, ListView):
    """Returns all messages that were received by the given user"""

    model = PrivateMessage
    template_name = "inbox.html"
    object_context_name = "message_list"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        message_list = PrivateMessage.objects.filter(
            recipient=self.request.user
        )
        context["message_list"] = message_list
        return context


inbox_view = InboxView.as_view()


class OutboxView(LoginRequiredMixin, ListView):
    """Returns all messages that were sent by the given user"""

    model = PrivateMessage
    template_name = "outbox.html"
    object_context_name = "message_list"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        message_list = PrivateMessage.objects.filter(sender=self.request.user)
        context["message_list"] = message_list
        return context


outbox_view = OutboxView.as_view()
