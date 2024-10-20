from datetime import datetime

from django.core.paginator import Paginator

from django.db import models
from django.db.models import Count

from .constant import COUNT_POSTS_ON_FRAME


def page_counter(self, model):
    """Функция подсчета страниц."""
    paginator = Paginator(model, COUNT_POSTS_ON_FRAME)
    page_number = self.request.GET.get("page")
    return paginator.get_page(page_number)


class PostQuerySet(models.QuerySet):
    """Выборка данных из моделей."""

    def with_related_data(self):
        """Объединения запроса к БД c комментариями."""
        return self.select_related(
            "author",
            "category",
            "location",
            "comments"
        )

    def with_related_data_no_comments(self):
        """Объединения запроса к БД без комментариев."""
        return self.select_related(
            "author",
            "category",
            "location",

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
