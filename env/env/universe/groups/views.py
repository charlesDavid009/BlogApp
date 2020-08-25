from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from django.http import HttpResponse, JsonResponse
from rest_framework import status
from rest_framework.response import Response
from .serializers import (
    GroupSerializer,
    CreateGroupSerializer,
    CreateBlogSerializer,
    BlogSerializer,
    MessageSerializer,
    CreateMessageSerializer,
    ActionBlogSerializer,
    CommentSerializer,
    CreateCommentSerializer,
    RequestSerializer,
    FollowsSerializer,
    UsesSerializer,
    MyBlogLikesSerializer,
    MessageLikesSerializer,
    CommentLikesSerializer,
    AdminSerializer,
    ReportSerializer,
    ReportListSerializer
)
from .models import (
    Group,
    MyBlog,
    Message,
    MyComment,
    Request,
    Follows,
    Uses,
    CommentsLikes,
    MessageLikes,
    MyBlogLikes,
    Admins,
    Reports
)
from rest_framework.views import APIView
from rest_framework import mixins
from rest_framework import generics
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.conf import settings
from .permissions import IsFollower, IsOwnerOrReadOnly, MyAdmin, IsOwners

User = get_user_model()

ACTIONS = settings.ACTIONS

# Create your views here.

class GroupCreateView(generics.CreateAPIView):
    """
    Create Group
    """
    serializer_class = CreateGroupSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Group.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = CreateGroupSerializer(data= request.data)
        if serializer.is_valid():
            obj = serializer.save(owner = self.request.user)
            vs = obj.id
            qs = Group.objects.filter(id = vs)
            if not qs.exists():
                return Response({}, status=status.HTTP_404_NOT_FOUND)
            objs = qs.first()
            objs.follower.add(self.request.user)
            objs.users.add(self.request.user)
            objs.admin.add(self.request.user)
            serializers = objs.save()
            return Response(serializers, status=status.HTTP_201_CREATED)
        return Response({}, status=status.HTTP_400_BAD_REQUEST)

class GroupListView(generics.ListAPIView):
    """
    Display Group List
    """
    lookup                  = 'pk'
    serializer_class        = GroupSerializer
    permission_classes      = [IsAuthenticated]

    def get_queryset(self):
        """
        To use search features, always put this before the url
        in the browser--> ?q=(the word you want to search for)
        """
        qs = Group.objects.all()
        query = self.request.GET.get("q")
        if query is not None:
            qs = qs.filter(
                Q(title__icontains=query) |
                Q(content__icontains=query)).distinct()
        return qs

class GroupRUdView(generics.RetrieveDestroyAPIView):
    """
    View And Delete Group Associated To Owner
    """
    lookup = 'pk'
    serializer_class = GroupSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get_queryset(self):
        return Group.objects.all()

class GroupFollowerView(generics.ListAPIView):
    """
    Display Follow User
    """
    lookup = 'id'
    serializer_class = FollowsSerializer
    permission_classes = [IsAuthenticated, IsFollower]

    def get_queryset(self):
        blog_id = self.kwargs.get('id')
        qs = Follows.objects.filter(groups=blog_id)
        return qs

class GroupRequestView(generics.ListAPIView):
    """
    Display Follow User
    """
    lookup = 'id'
    serializer_class = RequestSerializer
    permission_classes = [IsAuthenticated, IsFollower]

    def get_queryset(self):
        blog_id = self.kwargs.get('id')
        qs = Request.objects.filter(group=blog_id)
        return qs

class GroupAdminUserView(generics.ListAPIView):
    """
    Display Group Admin
    """
    lookup = 'id'
    serializer_class = AdminSerializer
    permission_classes = [IsAuthenticated, IsFollower]

    def get_queryset(self):
        blog_id = self.kwargs.get('id')
        qs = Admins.objects.filter(container=blog_id)
        return qs


class GroupUserView(generics.ListAPIView):
    """
    Display Group User
    """
    lookup = 'id'
    serializer_class = UsesSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get_queryset(self):
        blog_id = self.kwargs.get('id')
        qs = Uses.objects.filter(members=blog_id)
        return qs


class GroupActionView(generics.CreateAPIView):
    """
    Actions On Groups
    """
    queryset = Group.objects.all()
    serializer_class = ActionBlogSerializer
    permission_classes = [IsAuthenticated]

    # - Returns a serializer instance.
    def create(self, request, *args, **kwargs):
        serializer = ActionBlogSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            blog_id = data.get("id_")
            action = data.get("action")
            qs = Group.objects.filter(id=blog_id)
            if not qs.exists():
                return Response({}, status=status.HTTP_401_UNAUTHORIZED)
            obj = qs.first()
            if action == "follow":
                obj.follower.add(request.user)
                serializer = GroupSerializer(obj)
                return Response(serializer.data)
            elif action == "unfollow":
                obj.follower.remove(request.user)
                serializer = GroupSerializer(obj)
                return Response(serializer.data)
            elif action == "exit":
                obj.users.remove(request.user)
                serializer = GroupSerializer(obj)
                return Response(serializer.data)
            elif action == "join":
                obj.request.add(request.user)
                serializer = GroupSerializer(obj)
                return Response(serializer.data)
            elif action == "invite":
                obj.like.remove(request.user)
                serializer = GroupSerializer(obj)
                return Response(serializer.data)
            return Response({}, status=status.HTTP_400_BAD_REQUEST)


class GroupAdminActionView(generics.CreateAPIView):
    """
    Actions By Group Admin
    """
    queryset = Group.objects.all()
    serializer_class = ActionBlogSerializer
    permission_classes = [IsAuthenticated, MyAdmin]

    # - Returns a serializer instance.
    def create(self, request, *args, **kwargs):
        serializer = ActionBlogSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            group_id = data.get("id_")
            action = data.get("action")
            qs = Request.objects.filter(id=group_id)
            if not qs.exists():
                return Response(status=status.HTTP_404_NOT_FOUND)
            vd = qs.first()
            user = vd.user
            obj = vd.group
            if action == "confirm":
                obj.users.add(user)
                vd = Group.objects.filter(follower=user)
                if not vd.exists():
                    obj.follower.add(user)
                    serializer = GroupSerializer(obj)
                    return Response(serializer.data)
                serializer = GroupSerializer(obj)
                return Response(serializer.data)
            elif action == "reject":
                obj.request.remove(user)
                serializer = GroupSerializer(obj)
                return Response(serializer.data)
            elif action == "remove":
                obj.users.remove(user)
                vs = Group.objects.filter(follower=user)
                if vs.exists():
                    obj.follower.remove(user)
                    serializer = GroupSerializer(obj)
                    return Response(serializer.data)
                serializer = GroupSerializer(obj)
                return Response(serializer.data)
            return Response({}, status=status.HTTP_400_BAD_REQUEST)


class GroupOwnerActionView(generics.CreateAPIView):
    """
    Actions By Group Admin
    """
    queryset = Group.objects.all()
    serializer_class = ActionBlogSerializer
    permission_classes = [IsAuthenticated, IsOwners]

    # - Returns a serializer instance.
    def create(self, request, *args, **kwargs):
        serializer = ActionBlogSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            users_id = data.get("id_")
            action = data.get("action")
            qs = Uses.objects.filter(id=users_id)
            if not qs.exists():
                return Response({}, status=status.HTTP_404_NOT_FOUND)
            ms = qs.first()
            md = ms.user
            obj = ms.members
            if action == "add":
                obj.admin.add(md)
                vs = Group.objects.filter(follower=ms)
                if not vs.exists():
                    obj.follower.add(ms)
                    serializer = GroupSerializer(obj)
                    return Response(serializer.data)
                serializer = GroupSerializer(obj)
                return Response(serializer.data)
            elif action == "remove":
                obj.admin.remove(md)
                serializer = GroupSerializer(obj)
                return Response(serializer.data)
            return Response({}, status=status.HTTP_400_BAD_REQUEST)
