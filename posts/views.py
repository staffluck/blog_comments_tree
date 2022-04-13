from rest_framework.generics import ListCreateAPIView, CreateAPIView, GenericAPIView, get_object_or_404
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from mptt.templatetags.mptt_tags import cache_tree_children
from drf_spectacular.utils import extend_schema

from .models import Post, Comment
from .serializers import PostSerializer, CommentInputSerializer, CommentOutputSerializer

def recursive_build_json_from_tree(instance):
    response = {
        "id": instance.id,
        "text": instance.text,
        "children": [recursive_build_json_from_tree(child) for child in instance._cached_children]
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
        comments = Comment.objects.filter(post_id=post_id, level=0)
        response = []
        for comment in comments:
            comment = cache_tree_children(comment.get_descendants(include_self=True))
            response.append(recursive_build_json_from_tree(comment[0]))

        return Response(response, 200)


class CommentGetFullTreeAPIView(GenericAPIView):

    @extend_schema(
        responses={200: CommentOutputSerializer()}
    )
    def get(self, request, post_id, comment_id):
        comment = get_object_or_404(Comment.objects.all(), id=comment_id, post_id=post_id)
        
        comment = cache_tree_children(comment.get_descendants(include_self=True))
        tree = recursive_build_json_from_tree(comment[0])
        return Response(tree, 200)