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

    def to_representation(self, instance):
        if self.context.get("is_limited"):
            if instance.level > 2:
                return []
        return super().to_representation(instance)

class CommentInputSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        exclude = ["post", "level", "tree_id", "lft", "rght"]
    