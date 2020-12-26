"""posts Views Configuration"""
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, redirect, render, reverse
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from .forms import CommentForm, EditForm, PostForm
from .models import Post


def get_category_count():
    queryset = Post.objects.values("categories__title").annotate(
        Count("categories__title")
    )
    return queryset


class PostListView(ListView):
    """Post list view"""

    model = Post
    template_name = "post_list.html"
    context_object_name = "queryset"

    def get_context_data(self, **kwargs):
        category_count = get_category_count()
        most_recent = Post.objects.order_by("-created_on")
        context = super().get_context_data(**kwargs)
        context["most_recent"] = most_recent
        context["category_count"] = category_count
        return context


post_list_view = PostListView.as_view()


class PostDetailView(DetailView):
    """Post detail view"""

    model = Post
    template_name = "post_detail.html"
    context_object_name = "post"
    form_class = CommentForm

    def get_context_data(self, **kwargs):
        category_count = get_category_count()
        most_recent = Post.objects.order_by("-created_on")[:3]
        context = super().get_context_data(**kwargs)
        context["most_recent"] = most_recent
        context["category_count"] = category_count
        context["form"] = self.form_class
        return context

    def post(self, request, pk, *args, **kwargs):
        form = CommentForm(request.POST)
        if form.is_valid():
            post = get_object_or_404(Post, pk=pk)
            form.instance.user = request.user
            form.instance.post = post
            form.save()
            return redirect(reverse("post_detail", kwargs={"pk": post.pk}))


post_detail_view = PostDetailView.as_view()


class AddPostView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    """Add post view"""

    model = Post
    form_class = PostForm
    template_name = "add_post.html"
    success_message = "La publication a été créée avec succès !"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


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

    def delete(self, request, *args, **kwargs):
        messages.warning(self.request, self.success_message)
        return super(DeletePostView, self).delete(request, *args, **kwargs)


delete_post_view = DeletePostView.as_view()


def category_view(request, cats):
    category_posts = Post.objects.filter(categories__title=cats)
    return render(
        request,
        "categories.html",
        {"cats": cats, "category_posts": category_posts},
    )


class SearchResultsView(ListView):
    """Limit the search results page to filter the results outputted based upon a search query
    Args:
        ListView (generic class-based views): render some list of objects
    Returns:
        list: return the list of items for search results view
    """

    model = Post
    template_name = "search_results.html"
    context_object_name = "post_searches"
    paginate_by = 4

    def get_queryset(self):
        """Retrieving specific objects with icontains filters
        Returns:
            list: objects by products name
        """
        query = self.request.GET.get("q")
        if query:
            object_list = (
                Post.objects.filter(
                    Q(title__icontains=query) | Q(overview__icontains=query)
                )
                .distinct()
                .order_by("-created_on")
            )
        return object_list


search_results_view = SearchResultsView.as_view()
