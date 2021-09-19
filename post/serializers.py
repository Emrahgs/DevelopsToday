from rest_framework import serializers
from .models import Post, Comment, Upvote
from account.serializers import UserSerializer
from django.shortcuts import get_object_or_404
from django.db import IntegrityError


class UpvoteSerializer(serializers.ModelSerializer):
    post = serializers.CharField()

    def create(self, validated_data):
        post = get_object_or_404(Post, id=validated_data["post"])
        vote = Upvote()
        vote.post = post
        try:
            vote.save(commit=False)
        except IntegrityError:
            return vote
        return vote

    class Meta:
        model = Upvote
        fields = ("id", "post", "author")


class PostSerializer(serializers.ModelSerializer):
    votes = serializers.ReadOnlyField()
    author = UserSerializer()
    comment = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = (
            "id",
            "title",
            "link",
            "author",
            "votes",
            "comment",
            "creation_date",
        )

    def get_votes(self, obj):
        votes = obj.upvotes.all()
        return UpvoteSerializer(votes, many=True).data

    def get_comment(self, obj):
        comment = obj.comments.all()
        return PostCommentSerializer(comment, many=True).data


class PostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = (
            "id",
            "title",
            "link",
            "author",
            "creation_date",
        )


class PostCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = (
            "id",
            "content",
            "creation_date",
            "post",
            "author",
        )


class PostCommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = (
            "id",
            "content",
            "creation_date",
            "post",
            "author",
        )
