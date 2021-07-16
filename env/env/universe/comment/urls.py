from django.urls import path
from .views import *


urlpatterns = [
    path('Comment/create', MyCommentCreateAPIViews.as_view()),
    path('Comment/<int:pk>/detail', MyCommentDetailAPIViews.as_view(), name = 'thread'),
    #path('Blog/Comment/<int:id>/likes', views.CommentLikeListView.as_view()),
    path('Comment/', MyCommentListAPIViews.as_view()),
]