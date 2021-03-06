from rest_framework import serializers

from .models import Post, Comment

class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ["id", "text"]


class CommentOutputSerializer(serializers.ModelSerializer):
    children = serializers.ListField()

    class Meta:
        model = Comment
        exclude = ["post", "parent", "level", "tree_id", "lft", "rght"]


class CommentInputSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        exclude = ["post", "level", "tree_id", "lft", "rght"]
    