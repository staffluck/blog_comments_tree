from rest_framework.generics import ListCreateAPIView, GenericAPIView, get_object_or_404
from rest_framework.exceptions import NotFound

from .models import Post, Comment
from .serializers import PostSerializer, CommentOutputSerializer, CommentInputSerializer


class PostListCreateAPIView(ListCreateAPIView):
    serializer_class = PostSerializer
    queryset = Post.objects.all()


class CommentListCreateAPIView(ListCreateAPIView):

    def get_serializer_context(self):
        context =  super().get_serializer_context()
        context["is_limited"] = True
        return context

    def get_serializer_class(self):
        if self.request.method == "GET":
            return CommentOutputSerializer
        if self.request.method == "POST":
            return CommentInputSerializer

    def perform_create(self, serializer):
        if not Post.objects.filter(id=self.kwargs["post_id"]):
            raise NotFound()
        serializer.validated_data["post_id"] = self.kwargs["post_id"]
        return super().perform_create(serializer)

    def get_queryset(self):
        post_id = self.kwargs["post_id"]
        if not Comment.objects.filter(post_id=post_id).exists():
            raise NotFound()
        else:
            base_q = Comment.objects.filter(post=post_id)
            comments = base_q.filter(level=0)
            if not comments.exists():
                comments = base_q.filter(level=1)
                if not comments.exists():
                    comments = base_q.filter(level=2)

        return comments


class CommentDeepListAPIView(GenericAPIView):
    serializer_class = CommentOutputSerializer

    def get(self, requst, post_id, comment_id):
        comment = get_object_or_404(id=comment_id, post_id=post_id)
        
        serializer = self.get_serializer(instance=comment)
        return serializer.data