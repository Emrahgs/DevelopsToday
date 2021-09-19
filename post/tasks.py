from celery import shared_task
from .models import Post
from datetime import timedelta, datetime


@shared_task
def reset_post():
    reset_posts = Post.objects.all()
    for i in reset_posts:
        i.votes = 0
        i.save()
