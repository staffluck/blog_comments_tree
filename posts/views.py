from rest_framework.generics import GenericAPIView, ListCreateAPIView

from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer

class PostListCreateAPIView(ListCreateAPIView):
    serializer_class = PostSerializer
    queryset = Post.objects.all()


class CommentListCreateAPIView(ListCreateAPIView):
    serializer_class = CommentSerializer

    def perform_create(self, serializer):
        serializer.data["post"] = self.kwargs["post_id"]
        return super().perform_create(serializer)

    def get_queryset(self):
        return Comment.objects.filter(post=self.kwargs["post_id"], level__gte=0, level__lt=3)