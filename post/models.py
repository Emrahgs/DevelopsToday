from django.db import models
from django.db import IntegrityError
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()


class Post(models.Model):
    """
    In this table we can store Post info
    """

    title = models.CharField("Title", max_length=127)
    link = models.URLField("URL")
    votes = models.IntegerField(default=0)
    creation_date = models.DateTimeField(default=timezone.now)

    author = models.ForeignKey(
        User,
        verbose_name="Author",
        on_delete=models.CASCADE,
        db_index=True,
        related_name="posts",
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.title


class Upvote(models.Model):

    post = models.ForeignKey(
        Post,
        related_name="upvotes",
        on_delete=models.CASCADE,
        db_index=True,
        null=True,
        blank=True,
    )
    author = models.ForeignKey(
        User,
        verbose_name="Author",
        on_delete=models.CASCADE,
        db_index=True,
        related_name="upvotes",
        null=True,
        blank=True,
    )

    def save(self, commit=True, *args, **kwargs):

        if commit:
            try:
                self.post.votes += 1
                self.post.save()
                super(Upvote, self).save(*args, **kwargs)

            except IntegrityError:
                self.post.votes -= 1
                self.post.save()
                raise IntegrityError

        else:
            raise IntegrityError

    def __str__(self):
        if self.post:
            return self.post.title

        return "Okeyy"


class Comment(models.Model):
    """
    In this table we can store Comment info
    """

    content = models.TextField("Content")

    post = models.ForeignKey(
        Post,
        verbose_name="Post",
        on_delete=models.CASCADE,
        db_index=True,
        related_name="comments",
        null=True,
        blank=True,
    )

    author = models.ForeignKey(
        User,
        verbose_name="Author",
        on_delete=models.CASCADE,
        db_index=True,
        related_name="comments",
        null=True,
        blank=True,
    )

    creation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.author}'s comment"
