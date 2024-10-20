from django.urls import reverse


class CommentSuccessMixin:
    """Миксин удачного выполнения для комментария."""

    def get_success_url(self):
        """Перенаправление при удачном выполнении."""
        return reverse(
            "blog:post_detail", kwargs={"post_id": self.kwargs["post_id"]})


class ProfileSuccessMixin:
    """Миксин успешного выполнения для профиля."""

    def get_success_url(self):
        """Перенаправление при удачном выполнении."""
        return reverse(
            "blog:profile", kwargs={"username": self.request.user.username}
        )
