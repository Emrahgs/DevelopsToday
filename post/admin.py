from django.contrib import admin
from .models import Post, Comment, Upvote

admin.site.register(Post)
admin.site.register(Upvote)
admin.site.register(Comment)
