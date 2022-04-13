from rest_framework import serializers

from .models import Post, Comment

class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ["id", "text"]


class SubCommentSerializer(serializers.ModelSerializer):

    def to_representation(self, value):
            serializer = self.parent.parent.__class__(value, context=self.context)
            return serializer.data

class CommentOutputSerializer(serializers.ModelSerializer):
    children = SubCommentSerializer(many=True)

    class Meta:
        model = Comment
        exclude = ["post", "level", "tree_id", "lft", "rght"]



class CommentInputSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        exclude = ["post", "level", "tree_id", "lft", "rght"]
