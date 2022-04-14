from rest_framework.generics import ListCreateAPIView, CreateAPIView, GenericAPIView, get_object_or_404
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from mptt.templatetags.mptt_tags import cache_tree_children
from drf_spectacular.utils import extend_schema
from mptt.models import MPTTModel

from .models import Post, Comment
from .serializers import PostSerializer, CommentInputSerializer, CommentOutputSerializer

def recursive_build_json_from_tree(instance: MPTTModel, max_level=2) -> dict:  # уровень вложенности дерева начинается с 0. max_level=2 означает что вернёт вплоть до правнука
    response = {
        "id": instance.id,
        "text": instance.text,
        "children": [recursive_build_json_from_tree(child, max_level) if instance.level <= max_level else ["..."] for child in instance._cached_children]
    }
    return response


class PostListCreateAPIView(ListCreateAPIView):
    serializer_class = PostSerializer
    queryset = Post.objects.all()


class CommentListCreateAPIView(CreateAPIView):
    serializer_class = CommentInputSerializer

    def perform_create(self, serializer):
        if not Post.objects.filter(id=self.kwargs["post_id"]).exists():
            raise NotFound()
        serializer.validated_data["post_id"] = self.kwargs["post_id"]
        return super().perform_create(serializer)

    @extend_schema(
        responses={200: CommentOutputSerializer(many=True)}
    )
    def get(self, request, post_id):
        # Если у комментария нет детей, то незачем использовать метод get_descendants, который делает ещё один запрос к бд.
        comments_with_children = Comment.objects.filter(post_id=post_id, level=0, children__isnull=False).distinct()
        comments_without_children = Comment.objects.filter(post_id=post_id, level=0, children__isnull=True).distinct()

        response = []
        for comment in comments_with_children:
            comment = cache_tree_children(comment.get_descendants(include_self=True))
            response.append(recursive_build_json_from_tree(comment[0]))
        for comment in comments_without_children:
            comment._cached_children = []
            response.append(recursive_build_json_from_tree(comment))
        return Response(response, 200)


class CommentGetFullTreeAPIView(GenericAPIView):

    @extend_schema(
        responses={200: CommentOutputSerializer()}
    )
    def get(self, request, post_id, comment_id):
        comment = get_object_or_404(Comment.objects.all(), id=comment_id, post_id=post_id)
        
        comment = cache_tree_children(comment.get_descendants(include_self=True))
        tree = recursive_build_json_from_tree(comment[0], max_level=100)
        return Response(tree, 200)