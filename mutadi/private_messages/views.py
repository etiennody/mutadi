"""Private Messages Views Configuration"""
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import DeleteView, ListView

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


class DeleteMessageView(SuccessMessageMixin, DeleteView):
    """Delete message view"""

    model = PrivateMessage
    template_name = "delete_message.html"
    context_object_name = "message"
    success_url = reverse_lazy("inbox")
    success_message = "Le message a été supprimé avec succès !"

    def delete(self, request, *args, **kwargs):
        messages.warning(self.request, self.success_message)
        return super(DeleteMessageView, self).delete(request, *args, **kwargs)


delete_message_view = DeleteMessageView.as_view()
