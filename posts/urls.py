from django.urls import path

from .views import PostListCreateAPIView, CommentListCreateAPIView, CommentDeepListAPIView

urlpatterns = [
    path("", PostListCreateAPIView.as_view() ),
    path("<int:post_id>/comments/", CommentListCreateAPIView.as_view() ),
    path("<int:post_id>/<int:comment_id>/get_full_tree/", CommentDeepListAPIView.as_view() )
]