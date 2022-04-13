from django.urls import path

from .views import PostListCreateAPIView, CommentListCreateAPIView

urlpatterns = [
    path("", PostListCreateAPIView.as_view() ),
    path("<int:post_id>/comments/", CommentListCreateAPIView.as_view() )
]