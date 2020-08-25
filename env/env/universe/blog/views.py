from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response

from .serializers import(
    CreateBlogSerializer,
    BlogSerializer,
    CreateCommentSerializer,
    CommentSerializer,
    CreateSubCommentSerializer,
    SubCommentSerializer,
    ActionBlogSerializer,
    BlogLikesSerializer,
    CommentLikesSerializer,
    SubCommentLikesSerializer
)
from .models import (
    Blog,
    Comment,
    SubComment,
    BlogLikes,
    CommentLikes,
    SubCommentLikes
)
from rest_framework.views import APIView
from rest_framework import mixins
from rest_framework import generics
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes
)
from rest_framework.permissions import IsAuthenticated
from rest_framework import permissions
from .permissions import IsOwnerOrReadOnly, IsOwner
from django.conf import settings
from django.db.models import Q


ACTIONS = settings.ACTIONS


# Create your views here.

# All About Blog Posts
class BlogPostRUDView(generics.RetrieveDestroyAPIView):
    lookup                  = 'pk'
    serializer_class        = BlogSerializer
    permission_classes      = [IsAuthenticated, IsOwnerOrReadOnly]

    def get_queryset(self):
        return Blog.objects.all()


class BlogCreatePostView(generics.CreateAPIView):
    lookup                  = 'pk'
    serializer_class        = CreateBlogSerializer
    permission_classes      = [IsAuthenticated]

    def get_queryset(self):
        return Blog.objects.all()

    def perform_create(self, serializer):
        serializer.save(user = self.request.user)


class BlogPostListView(generics.ListAPIView):
    """
    Get All Blogs And Search for Blog Titles Or Contents
    """
    lookup                   = 'pk'
    serializer_class         = BlogSerializer
    permission_classes       = [IsAuthenticated]

    def get_queryset(self):
        qs = Blog.objects.all()
        query = self.request.GET.get("q")
        if query is not None:
            qs = qs.filter(
                Q(title_icontains = query)|
                Q(content_icontains = query)).distinct()
        return qs

class BlogUsersPostsView(generics.ListAPIView):
    """
    Displays Only Users Posts
    """
    lookup                  = 'pk'
    serializer_class        = BlogSerializer
    permission_classes      = [IsAuthenticated]

    def get_queryset(self):
        qs = Blog.objects.all()
        user  = self.request.user
        obj = qs.filter(user= user)
        return obj


class BlogFeedsView(generics.ListAPIView):
    """
    Displays Only Users Posts
    """
    serializer_class         = BlogSerializer
    permission_classes       = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        qs = Blog.objects.feed(user)
        return qs


class BlogLikeListView(generics.ListAPIView):
    """
    Displays Only Users Posts
    """
    lookup                   = 'id'
    serializer_class         = BlogLikesSerializer
    permission_classes       = [IsAuthenticated, IsOwnerOrReadOnly]

    def get_queryset(self):
        blog_id = self.kwargs.get('id')
        qs = BlogLikes.objects.filter(blog=blog_id)
        return qs

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def actions(request, *args, **kwargs):
    """
    IF ACTION PASSED IS VALID RUN ACTIONS API
    ID IS REQUIRED
    ACTIONS = LIKE, UNLIKE, RE_BLOG
    """
    if request.method == 'POST':
        serializer = ActionBlogSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            blog_id = data.get("id")
            action = data.get("action")
            details = data.get("add")
            qs = Blog.objects.filter(id=blog_id)
            if not qs.exists():
                return Response({}, status=status.HTTP_404_NOT_FOUND)
            obj = qs.first()
            if action == "like":
                obj.likes.add(request.user)
                serializer = BlogSerializer(obj)
                return Response(serializer.data)
            elif action == "unlike":
                obj.likes.remove(request.user)
                serializer = BlogSerializer(obj)
                return Response(serializer.data)
            elif action == "report":
                obj.reports.add(request.user)
                serializer = BlogSerializer(obj)
                return Response(serializer.data)
            elif action == "reblog":
                new_blog = Blog.objects.create(
                    user=request.user,
                    parent=obj,
                    content=details
                )
                serializer = BlogSerializer(new_blog)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response({}, status=status.HTTP_400_BAD_REQUEST)


# ALL ABOUT COMMENTS POSTS

