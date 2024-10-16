from datetime import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import models
from django.db.models import Count
from .models import User
from django.views.generic import (
    ListView,
    CreateView,
    DetailView,
    DeleteView,
    UpdateView,
    FormView,
)
from django.urls import reverse
from django.shortcuts import get_object_or_404, redirect
from django.core.paginator import Paginator

from blog.models import Category, Post, Comments

from .forms import PostForm, CommentForm, ProfilForm

from .constant import COUNT_POSTS_ON_FRAME


class CommentSyccessMixin:
    """Миксин удачного выполнения."""

    def get_success_url(self):
        """функция перенаправления при удачном выполнении."""
        return reverse(
            "blog:post_detail", kwargs={"post_id": self.kwargs["post_id"]})


def page_counter(self, model):
    """Функция подсчета страниц."""
    paginator = Paginator(model, COUNT_POSTS_ON_FRAME)
    page_number = self.request.GET.get("page")
    return paginator.get_page(page_number)


class ProfileListView(ListView):
    """CBV класс для отоброжанеия профиля."""

    template_name = "blog/profile.html"

    def get_queryset(self):
        """фунция выборпи постов с сортировкой по автору."""
        self.author = get_object_or_404(User, username=self.kwargs["username"])
        return (
            Post.objects.filter(author=self.author)
            .annotate(comment_count=Count("comments"))
            .order_by("-pub_date")
        )

    def get_context_data(self, **kwargs):
        """модификация контекста."""
        context = super().get_context_data(**kwargs)
        context["profile"] = self.author
        model = context["page_obj"] = (
            Post.objects.filter(author=self.author)
            .annotate(comment_count=Count("comments"))
            .order_by("-pub_date")
        )
        context["page_obj"] = page_counter(self, model)
        return context


class ProfileSuccessMixin:
    """Миксин успешного выполнения."""

    def get_success_url(self):
        """функция перенаправления при удачном выполнении."""
        return reverse(
            "blog:profile", kwargs={"username": self.request.user.username}
        )


class ProfileUpdateView(LoginRequiredMixin, ProfileSuccessMixin, FormView):
    """CBV класс для редактирования профиля."""

    template_name = "blog/user.html"
    form_class = ProfilForm

    def form_valid(self, form):
        """функция для проверки валидации формы."""
        form.instance.id = self.request.user.id
        form.instance.password = self.request.user.password
        form.instance.username = self.request.user.username

        form.save()
        return super().form_valid(form)


class PostQuerySet(models.QuerySet):
    """класс для выборки данныех из моделей."""

    def with_related_data(self):
        """Обедитенения запроса у БД."""
        return self.select_related(
            "author",
            "category",
            "location",
            "comments"
        )

    def published(self):
        """Фильтр для выборки по актуальности поста."""
        return self.filter(
            is_published=True,
            category__is_published=True,
            pub_date__lt=datetime.now()
        )

    def annotates(self):
        """Метод для подсчёта комментария к посту."""
        return self.annotate(comment_count=Count("comments"))


class PostListView(ListView):
    """CBV класс для отоброжанеия списка постов."""

    model = Post
    template_name = "blog/index.html"
    paginate_by = COUNT_POSTS_ON_FRAME

    def get_queryset(self):
        """функция выборки актуальных постов."""
        return PostQuerySet(Post).published().annotates().order_by("-pub_date")


class PostCreateView(LoginRequiredMixin, CreateView):
    """CBV класс для создания постов."""

    model = Post
    template_name = "blog/create.html"
    form_class = PostForm

    def get_queryset(self):
        """функция выборки актуальной информации для формирования постов."""
        return Post.objects.select_related("category").filter()

    def form_valid(self, form):
        """функция проверки заполнения данных."""
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        """функция перенаправления при удачном выполнении."""
        return reverse(
            "blog:profile", kwargs={"username": self.request.user.username}
        )


class PostUpdateView(LoginRequiredMixin, UpdateView):
    """CBV класс для редактирования постов."""

    model = Post
    template_name = "blog/create.html"
    pk_url_kwarg = "post_id"
    form_class = PostForm

    def get_context_data(self, **kwargs):
        """функция модификации контектса."""
        context = super().get_context_data(**kwargs)
        context["form"] = PostForm(
            instance=get_object_or_404(Post, pk=self.kwargs.get("post_id"))
        )
        context["comments"] = self.object.comments.select_related("author")
        return context

    def dispatch(self, request, *args, **kwargs):
        """функция проверки нахождения обьекта в базе."""
        post = get_object_or_404(Post, id=self.kwargs["post_id"])
        if self.request.user != post.author:
            return redirect("blog:post_detail", post_id=self.kwargs["post_id"])
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        """функция перенаправления при удачном выполнении."""
        return reverse("blog:post_detail", kwargs={"post_id": self.object.id})


class PostDeleteView(LoginRequiredMixin, ProfileSuccessMixin, DeleteView):
    """CBV класс для удаления постов."""

    model = Post
    template_name = "blog/create.html"
    pk_url_kwarg = "post_id"

    def dispatch(self, request, *args, **kwargs):
        """функция проверки нахождения обьекта в базе."""
        post = get_object_or_404(
            Post,
            id=kwargs["post_id"],
        )
        if post.author != request.user:
            return redirect("blog:post_detail", post_id=self.kwargs["post_id"])
        return super().dispatch(request, *args, **kwargs)


class PostDetailView(DetailView):
    """CBV класс для отображения подробной информации поста."""

    model = Post
    template_name = "blog/detail.html"
    pk_url_kwarg = "post_id"

    def get_context_data(self, **kwargs):
        """функция модификации контектса."""
        context = super().get_context_data(**kwargs)
        context["form"] = CommentForm()
        context["comments"] = self.object.comments.select_related("author")
        return context

    def get_queryset(self):
        """функция выборки постов по его ID."""
        queryset = Post.objects.select_related(
            "author",
            "category",
            "location"
        ).filter(
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
    """CBV класс для отображения постов по категории."""

    template_name = "blog/category.html"
    model = Category
    paginate_by = COUNT_POSTS_ON_FRAME

    def get_context_data(self, **kwargs):
        """функция модификации контектса."""
        context = super().get_context_data(**kwargs)
        context["category"] = get_object_or_404(
            Category, slug=self.kwargs["category_slug"], is_published=True
        )
        return context

    def get_queryset(self):
        """функция выборки постов по определйнной категории."""
        return Post.objects.select_related("author", "category", "location"
                                           ).filter(
            is_published=True,
            category__is_published=True,
            pub_date__lt=datetime.now(),
            category__slug=self.kwargs.get("category_slug"),
        ).order_by("-pub_date")


class AddCommentView(LoginRequiredMixin, CreateView):
    """CBV класс для добавления комментария."""

    posts = None
    form_class = CommentForm
    model = Comments
    template_name = "blog/comment.html"
    pk_url_kwarg = "commet_id"

    def dispatch(self, request, *args, **kwargs):
        """функция проверки нахождения обьекта в базе."""
        self.posts = get_object_or_404(Post, pk=kwargs["post_id"])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        """функция для проверки валидации формы."""
        form.instance.author = self.request.user
        form.instance.post = self.posts
        return super().form_valid(form)

    def get_success_url(self):
        """функция перенаправления при удачном выполнении."""
        return reverse("blog:post_detail", kwargs={"post_id": self.posts.pk})


class CommentUpdateView(LoginRequiredMixin, CommentSyccessMixin, UpdateView):
    """CBV класс для редактирования постов."""

    model = Comments
    template_name = "blog/comment.html"
    pk_url_kwarg = "comment_id"
    form_class = CommentForm

    def dispatch(self, request, *args, **kwargs):
        """функция проверки нахождения обьекта в базе."""
        comment = get_object_or_404(
            Comments,
            id=kwargs["comment_id"],
        )

        if comment.author != request.user:
            return redirect("blog:post_detail", post_id=self.kwargs["post_id"])
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """функция модификации контектса."""
        context = super().get_context_data(**kwargs)
        context["comment"] = get_object_or_404(
            Comments,
            id=self.kwargs["comment_id"],
        )
        return context


class DeleteCommentView(LoginRequiredMixin, CommentSyccessMixin, DeleteView):
    """CBV класс для удаления комменатрия."""

    model = Comments
    template_name = "blog/comment.html"
    pk_url_kwarg = "comment_id"

    def dispatch(self, request, *args, **kwargs):
        """функция проверки нахождения обьекта в базе."""
        comment = get_object_or_404(
            Comments,
            id=kwargs["comment_id"],
        )
        if comment.author != request.user:
            return redirect("blog:post_detail", post_id=self.kwargs["post_id"])
        return super().dispatch(request, *args, **kwargs)
