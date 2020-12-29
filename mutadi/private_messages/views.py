"""Private Messages Views Configuration"""
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView

from .forms import ComposeForm, ReplyForm
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
        ).order_by("-sent_at")
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
        message_list = PrivateMessage.objects.filter(
            sender=self.request.user
        ).order_by("-sent_at")
        context["message_list"] = message_list
        return context


outbox_view = OutboxView.as_view()


class DeleteMessageView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
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


class MessageDetailView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = PrivateMessage
    template_name = "message_detail.html"
    form_class = ReplyForm
    success_message = "La réponse a été envoyé avec succès !"

    def dispatch(self, request, pk, *args, **kwargs):
        self.message = PrivateMessage.objects.get(pk=pk)
        return super().dispatch(request, *args, **kwargs)

    def get_initial(self):
        return {"subject": f"Re: {self.message.subject}"}

    def form_valid(self, form):
        form.instance.sender = self.request.user
        form.instance.recipient = self.message.sender
        return super().form_valid(form)

    def get_context_data(self):
        context = super().get_context_data()
        context["private_message"] = self.message
        return context


message_detail_view = MessageDetailView.as_view()


class ComposeMessageView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    """Compose message view"""

    model = PrivateMessage
    template_name = "compose_message.html"
    form_class = ComposeForm
    success_url = reverse_lazy("inbox")
    success_message = "Le message a été envoyé avec succès !"

    def form_valid(self, form):
        form.instance.sender = self.request.user
        return super().form_valid(form)


compose_message_view = ComposeMessageView.as_view()
