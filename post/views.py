import json
from django.db.utils import IntegrityError
from rest_framework.response import Response
from rest_framework import status
from .models import Post, Comment
from rest_framework.exceptions import NotFound
from rest_framework.views import APIView
from post.serializers import (
    PostSerializer,
    PostCreateSerializer,
    PostCommentSerializer,
    PostCommentCreateSerializer,
    UpvoteSerializer,
)


# --------------------- Post -----------------------------------


class PostAPIView(APIView):
    def get(self, request, *args, **kwargs):
        post = Post.objects.all()
        filter_by = json.loads(json.dumps(request.GET))
        if filter_by:
            post = post.filter(**filter_by)
        serializer = PostSerializer(post, many=True, context={"request": request})
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        post_data = request.data
        serializer = PostCreateSerializer(data=post_data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class PostDetailAPIView(APIView):
    def get(self, request, *args, **kwargs):
        post_id = kwargs.get("pk")
        post = Post.objects.filter(pk=post_id).first()
        if not post:
            raise NotFound
        serializer = PostSerializer(post, context={"request": request})
        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        post_data = request.data
        post_id = kwargs.get("pk")
        post = Post.objects.filter(pk=post_id).first()
        if not post:
            raise NotFound
        serializer = PostCreateSerializer(
            data=post_data, instance=post, partial=True, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, *args, **kwargs):
        post_data = request.data
        post_id = kwargs.get("pk")
        post = Post.objects.filter(pk=post_id).first()
        if not post:
            raise NotFound
        serializer = PostCreateSerializer(
            data=post_data, instance=post, partial=True, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        post_id = kwargs.get("pk")
        post = Post.objects.filter(pk=post_id)
        if not post:
            raise NotFound
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# --------------------- Comment -----------------------------------


class CommentAPIView(APIView):
    def get(self, request, *args, **kwargs):
        comment = Comment.objects.all()
        filter_by = json.loads(json.dumps(request.GET))
        if filter_by:
            comment = comment.filter(**filter_by)
        serializer = PostCommentSerializer(
            comment, many=True, context={"request": request}
        )
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        comment_data = request.data
        serializer = PostCommentCreateSerializer(
            data=comment_data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CommentDetailAPIView(APIView):
    def get(self, request, *args, **kwargs):
        comment_id = kwargs.get("pk")
        comment = Comment.objects.filter(pk=comment_id).first()
        if not comment:
            raise NotFound
        serializer = PostCommentSerializer(comment, context={"request": request})
        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        comment_data = request.data
        comment_id = kwargs.get("pk")
        comment = Comment.objects.filter(pk=comment_id).first()
        if not comment:
            raise NotFound
        serializer = PostCommentCreateSerializer(
            data=comment_data,
            instance=comment,
            partial=True,
            context={"request": request},
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, *args, **kwargs):
        comment_data = request.data
        comment_id = kwargs.get("pk")
        comment = Comment.objects.filter(pk=comment_id).first()
        if not comment:
            raise NotFound
        serializer = PostCommentCreateSerializer(
            data=comment_data,
            instance=comment,
            partial=True,
            context={"request": request},
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        comment_id = kwargs.get("pk")
        comment = Comment.objects.filter(pk=comment_id)
        if not comment:
            raise NotFound
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# ---------------- Vote -------------------------------


class VoteView(APIView):
    def post(self, request):
        serializer = UpvoteSerializer(data=request.data)
        if serializer.is_valid(raise_exception=ValueError):
            created_instance = serializer.create(validated_data=request.data)

            try:
                created_instance.save()

            except IntegrityError:
                return Response(
                    {"message": "Already voted"}, status=status.HTTP_400_BAD_REQUEST
                )

            return Response(
                {"message": "Vote cast successful"}, status=status.HTTP_200_OK
            )
