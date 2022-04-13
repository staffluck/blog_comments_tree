from rest_framework import serializers

from .models import Post, Comment

class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ["id", "text"]


class SubCommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        exclude = ["post", "level", "tree_id", "lft", "rght"]

class CommentSerializer(serializers.ModelSerializer):
    parent = SubCommentSerializer(many=False)

    class Meta:
        model = Comment
        exclude = ["post", "level", "tree_id", "lft", "rght"]
