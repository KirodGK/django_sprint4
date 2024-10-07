from django import forms
from .models import Comments, Post, User


class PostForm(forms.ModelForm):
    """Класс для формирования CBV формы поста."""

    class Meta:
        """Класс для формирования CBV формы поста, вывод полей."""

        model = Post
        fields = (
            'title',
            'category',
            'location',
            'pub_date',
            'text',
            'is_published',
            'image',
        )


class CommentForm(forms.ModelForm):
    """Класс для формирования CBV формы комментария."""

    class Meta:
        """Класс для формирования CBV формы комментария, вывод полей."""

        model = Comments
        fields = ('text',)


class ProfilForm(forms.ModelForm):
    """Класс для формирования CBV формы профиля."""

    class Meta:
        """Класс для формирования CBV формы профиля, вывод полей."""

        model = User
        fields = (
            'last_name',
            'first_name')
