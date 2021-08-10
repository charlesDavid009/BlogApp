
from django.db.models import Q
from rest_framework.filters import (
        SearchFilter,
        OrderingFilter,
    )
from .permissions import IsOwnerOrReadOnly

from rest_framework import generics, views
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAdminUser,
    IsAuthenticatedOrReadOnly,

    )



from . models import Comment




from .serializer import (
    CommentListSerializer,
    CommentDetailSerializer,
    create_comment_serializer
    )


class MyCommentCreateAPIViews(generics.CreateAPIView):
    queryset = Comment.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        model_type = self.request.GET.get("type")
        slug = self.request.GET.get("slug")
        parent_id = self.request.GET.get("parent_id", None)
        return create_comment_serializer(
                model_type=model_type, 
                slug=slug,
                parent_id=parent_id,
                user=self.request.user
                )

class MyCommentDetailAPIViews(generics.RetrieveDestroyAPIView):
    lookup                  = 'pk'
    serializer_class = CommentDetailSerializer
    permission_classes      = [IsAuthenticated, IsOwnerOrReadOnly]

    def get_queryset(self):
        queryset = Comment.objects.all()#filter(id__gte=0)
        return queryset



class MyCommentListAPIViews(generics.ListAPIView):
    serializer_class = CommentListSerializer
    permission_classes = [IsAuthenticated]
    search_fields = ['content', 'user__first_name']

    def get_queryset(self, *args, **kwargs):
        #queryset_list = super(PostListAPIView, self).get_queryset(*args, **kwargs)
        queryset_list = Comment.objects.filter(id__gte=0) #filter(user=self.request.user)
        query = self.request.GET.get("q")
        if query:
            queryset_list = queryset_list.filter(
                    Q(content__icontains=query)|
                    Q(user__first_name__icontains=query) |
                    Q(user__last_name__icontains=query)
                    ).distinct()
        return queryset_list
