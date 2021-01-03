"""Private messages views configuration"""
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import get_object_or_404, render
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.views.generic import CreateView, ListView

from .forms import ComposeForm, ReplyForm
from .models import PrivateMessage


class InboxView(LoginRequiredMixin, ListView):
    """
    Returns all messages that were received
    by the given user.
    """

    template_name = "inbox.html"
    paginate_by = 25

    def get_queryset(self):
        self.message_list = PrivateMessage.objects.filter(
            recipient=self.request.user,
            recipient_deleted_at__isnull=True,
        ).order_by("-sent_at")
        return self.message_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["message_list"] = self.message_list
        return context


inbox_view = InboxView.as_view()


class OutboxView(LoginRequiredMixin, ListView):
    """
    Returns all messages that were sent
    by the given user.
    """

    template_name = "outbox.html"
    paginate_by = 25

    def get_queryset(self):
        self.message_list = PrivateMessage.objects.filter(
            sender=self.request.user,
            sender_deleted_at__isnull=True,
        ).order_by("-sent_at")
        return self.message_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["message_list"] = self.message_list
        return context


outbox_view = OutboxView.as_view()


@login_required(login_url="/members/login/")
def delete_message(request, pk, success_url=None):
    """
    Marks a message as deleted by sender or recipient. The message is not
    really removed from the database, because two users must delete a message
    before it's save to remove it completely.
    """
    user = request.user
    now = timezone.now()
    message = get_object_or_404(PrivateMessage, pk=pk)
    deleted = False
    if success_url is None:
        success_url = reverse("inbox")
    if message.sender == user:
        message.sender_deleted_at = now
        deleted = True
    if message.recipient == user:
        message.recipient_deleted_at = now
        deleted = True
    if deleted:
        message.save()
        messages.warning(request, ("Message supprimé avec succès !"))
    return render(request, "inbox.html", {"deleted": deleted})


class MessageDetailView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    """Message detail view and processing reply."""

    model = PrivateMessage
    template_name = "message_detail.html"
    form_class = ReplyForm
    success_message = "La réponse a été envoyé avec succès !"

    def dispatch(self, request, pk, *args, **kwargs):
        self.message = PrivateMessage.objects.get(pk=pk)
        return super().dispatch(request, *args, **kwargs)

    def get_initial(self):
        return {
            "subject": f"Re: {self.message.subject}",
            "content": f"-- {self.message.sender} : {self.message.content}",
        }

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
    """Compose message view."""

    model = PrivateMessage
    template_name = "compose_message.html"
    form_class = ComposeForm
    success_url = reverse_lazy("inbox")
    success_message = "Le message a été envoyé avec succès !"

    def form_valid(self, form):
        form.instance.sender = self.request.user
        return super().form_valid(form)


compose_message_view = ComposeMessageView.as_view()
