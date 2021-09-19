from django.urls import path
from post.views import (
    PostAPIView,
    PostDetailAPIView,
    CommentAPIView,
    CommentDetailAPIView,
    VoteView,
)

app_name = "post"

urlpatterns = [
    path("posts/", PostAPIView.as_view(), name="posts"),
    path("post/<int:pk>", PostDetailAPIView.as_view(), name="post_detail"),
    path("comments/", CommentAPIView.as_view(), name="comments"),
    path("comment/<int:pk>", CommentDetailAPIView.as_view(), name="comment_detail"),
    path("vote/", VoteView.as_view(), name="vote"),
]
