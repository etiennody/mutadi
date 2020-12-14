"""posts Views Configuration"""
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import (
    CreateView,
    DetailView,
    ListView,
    UpdateView,
    DeleteView,
)
from django.urls import reverse_lazy
from .forms import EditForm, PostForm
from .models import Post


class PostListView(ListView):
    """Post list view"""

    queryset = Post.objects.filter(status=1).order_by("-created_on")
    template_name = "post_list.html"


post_list_view = PostListView.as_view()


class PostDetailView(DetailView):
    """Post detail view"""

    model = Post
    template_name = "post_detail.html"


post_detail_view = PostDetailView.as_view()


class AddPostView(SuccessMessageMixin, CreateView):
    """Add post view"""

    model = Post
    form_class = PostForm
    template_name = "add_post.html"
    success_message = "La publication a été créée avec succès !"


add_post_view = AddPostView.as_view()


class UpdatePostView(SuccessMessageMixin, UpdateView):
    """Update post view"""

    model = Post
    form_class = EditForm
    template_name = "update_post.html"
    success_message = "La publication a été mise à jour avec succès !"


update_post_view = UpdatePostView.as_view()


class DeletePostView(SuccessMessageMixin, DeleteView):
    """Delete post view"""

    model = Post
    template_name = "delete_post.html"
    success_url = reverse_lazy("home")
    success_message = "La publication a été supprimée avec succès !"


delete_post_view = DeletePostView.as_view()
