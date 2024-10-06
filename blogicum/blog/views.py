from datetime import datetime
from django.db import models
from django.db.models import Count
from django.forms import BaseModelForm
from django.http import HttpRequest, HttpResponse
from django.views.generic import (
    ListView,
    CreateView,
    DetailView,
    DeleteView,
    UpdateView,
    FormView,
)
from django.urls import reverse_lazy

from django.shortcuts import get_object_or_404, render, redirect
from django.core.paginator import Paginator
from blog.models import Category, Post, Comments

from .constant import POST_OUTPUT_LIM
from .forms import PostForm, CommentForm, ProfilForm

from .models import User
from django.urls import reverse


from django.contrib.auth.mixins import LoginRequiredMixin





class ProfileDetailView(ListView):

    template_name = "blog/profile.html"

    def get_queryset(self):
        self.author = get_object_or_404(User, username=self.kwargs["username"])
        return (
            Post.objects.filter(author=self.author)
            .annotate(comment_count=Count("comments"))
            .order_by("-pub_date")
        )

    def get_context_data(self, **kwargs: reverse_lazy):
        context = super().get_context_data(**kwargs)
        context["profile"] = self.author
        model = context["page_obj"] = (
            Post.objects.filter(author=self.author)
            .annotate(comment_count=Count("comments"))
            .order_by("-pub_date")
        )
        paginator = Paginator(model, 10)
        page_number = self.request.GET.get("page")
        context["page_obj"] = paginator.get_page(page_number)
        return context


class ProfileUpdateView(LoginRequiredMixin, FormView):
    template_name = "blog/user.html"
    form_class = ProfilForm

    def form_valid(self, form):

        form.instance.id = self.request.user.id
        form.instance.password = self.request.user.password
        form.instance.username = self.request.user.username

        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy(
            "blog:profile", kwargs={"username": self.request.user.username}
        )


def edit_profile():
    pass


class PostQuerySet(models.QuerySet):

    def with_related_data(self):
        return self.select_related("author", "category", "location", "comments")

    def published(self):
        return self.filter(
            is_published=True, category__is_published=True, pub_date__lt=datetime.now()
        )

    def annotates(self):
        return self.annotate(comment_count=Count("comments"))


class PostListView(ListView):
    model = Post
    template_name = "blog/index.html"
    paginate_by = 10

    def get_queryset(self):
        return PostQuerySet(Post).published().annotates().order_by("-pub_date")


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = "blog/create.html"
    form_class = PostForm

    def get_queryset(self):
        return Post.objects.select_related("category").filter()

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy(
            "blog:profile", kwargs={"username": self.request.user.username}
        )


class PostUpdateView(LoginRequiredMixin, UpdateView):

    model = Post
    template_name = "blog/create.html"
    pk_url_kwarg = "post_id"
    form_class = PostForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = PostForm(
            instance=get_object_or_404(Post, pk=self.kwargs.get("post_id"))
        )
        context["comments"] = self.object.comments.select_related("author")
        return context

    def dispatch(self, request, *args, **kwargs):
        post = get_object_or_404(Post, id=self.kwargs["post_id"])
        if self.request.user != post.author:
            return redirect("blog:post_detail", post_id=self.kwargs["post_id"])
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse("blog:post_detail", kwargs={"post_id": self.object.id})


class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = "blog/create.html"
    pk_url_kwarg = "post_id"

    def dispatch(self, request, *args, **kwargs):
        post = get_object_or_404(
            Post,
            id=kwargs["post_id"],
        )
        if post.author != request.user:
            return redirect("blog:post_detail", post_id=self.kwargs["post_id"])
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy(
            "blog:profile", kwargs={"username": self.request.user.username}
        )


class PostDetailView(DetailView):
    model = Post
    template_name = "blog/detail.html"
    pk_url_kwarg = "post_id"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = CommentForm()
        context["comments"] = self.object.comments.select_related("author")
        return context

    def get_queryset(self):
        queryset = Post.objects.select_related("author", "category", "location").filter(
            id=self.kwargs.get("post_id")
        )
        user = queryset.values_list("author__username", flat=True).first()

        if not self.request.user.username == user:
            queryset = queryset.filter(
                is_published=True,
                category__is_published=True,
                pub_date__lt=datetime.now(),
            )

        return queryset


class CategoryListView(ListView):
    template_name = "blog/category.html"
    model = Category
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["category"] = get_object_or_404(
            Category, slug=self.kwargs["category_slug"], is_published=True
        )
        return context

    def get_queryset(self):
        queryset = (
            Post.objects.select_related("author", "category", "location")
            .filter(
                is_published=True,
                category__is_published=True,
                pub_date__lt=datetime.now(),
                category__slug=self.kwargs.get("category_slug"),
            )
            .order_by("-pub_date")
        )
        return queryset

class AddCommentView(LoginRequiredMixin, CreateView):
    posts = None
    form_class = CommentForm
    model = Comments
    template_name = "blog/comment.html"
    pk_url_kwarg = "commet_id"

    def dispatch(self, request, *args, **kwargs):
        self.posts = get_object_or_404(Post, pk=kwargs["post_id"])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = self.posts
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("blog:post_detail", kwargs={"post_id": self.posts.pk})


class CommentUpdateView(LoginRequiredMixin, UpdateView):
    model = Comments
    template_name = "blog/comment.html"
    pk_url_kwarg = "comment_id"
    form_class = CommentForm

    def dispatch(self, request, *args, **kwargs):
        comment = get_object_or_404(
            Comments,
            id=kwargs["comment_id"],
        )

        if comment.author != request.user:
            return redirect("blog:post_detail", post_id=self.kwargs["post_id"])
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["comment"] = get_object_or_404(
            Comments,
            id=self.kwargs["comment_id"],
        )
        return context

    def get_success_url(self):
        return reverse_lazy(
            "blog:post_detail", kwargs={"post_id": self.kwargs["post_id"]}
        )


class DeleteCommentView(LoginRequiredMixin, DeleteView):
    model = Comments
    template_name = "blog/comment.html"
    pk_url_kwarg = "comment_id"

    def dispatch(self, request, *args, **kwargs):
        comment = get_object_or_404(
            Comments,
            id=kwargs["comment_id"],
        )
        if comment.author != request.user:
            return redirect("blog:post_detail", post_id=self.kwargs["post_id"])
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy(
            "blog:post_detail", kwargs={"post_id": self.kwargs["post_id"]}
        )
