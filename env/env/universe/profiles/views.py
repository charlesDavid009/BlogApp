from django.shortcuts import render
from .serializers import (
    ProfileSerializer,
    CreateProfileSerializer,
    ActionProfileSerializer,
    FollowSerializer)
from .models import Profile, Follow
from rest_framework import generics, mixins
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.conf import settings
from .permissions import IsOwnerOrReadOnly
from django.shortcuts import render
from rest_framework import status
from django.db.models import Q
from rest_framework.response import Response

ACTIONS = settings.ACTIONS

# Create your views here.

class CraeteProfileView(generics.CreateAPIView):
    """
    Create your Profile
    """
    serializer_class    = CreateProfileSerializer
    permission_classes  = [IsAuthenticated]

    def get_queryset(self):
        Profile.objects.all()

    def perform_create(self, serializer):
        serializer.save(user =self.request.user)

class UpdateProfileView(generics.RetrieveUpdateDestroyAPIView):
    """
    Updates and Delete Uses Profiles
    """
    lookup                      = 'pk'
    serializer_class            = ProfileSerializer
    permission_classes          = [IsAuthenticated, IsOwnerOrReadOnly]

    def get_queryset(self):
        return Profile.objects.all()

class MyProfileView(generics.ListAPIView):
    """
    Gets Users Profile
    """
    Lookup                      = 'pk'
    serializer_class            = ProfileSerializer
    permission_classes          = [IsAuthenticated]

    def get_queryset(self):
        users = self.request.user
        qs = Profile.objects.filter(user = users)
        return qs

class GetUserView(generics.ListAPIView):
    """
    Search And Displays Profiles According to User Id Provided
    """
    Lookup                      = 'slug'
    serializer_class            = ProfileSerializer
    permission_classes          = [IsAuthenticated]

    def get_queryset(self):
        query = self.request.GET.get("q")
        if query is not None:
            qs = Profile.objects.all()
            qs = qs.filter(
                Q(user__username__icontains = query)|
                Q(first_name__icontains = query)).distinct()
        return qs


class UserFollowersView(generics.ListAPIView):
    """
    DIsplays Followers
    """
    lookup                     = 'pk'
    serializer_class           = FollowSerializer
    permission_classes         = [IsAuthenticated]

    def get_queryset(self):
        user = self.kwargs.get('pk')
        obj = Profile.objects.filter(user__id = user)
        obj = obj.first()
        qs = Follow.objects.filter(profiles = obj).order_by('alphabet')
        return qs

class UsersFollowingView(generics.ListAPIView):
    """
    Displays Users is Following
    """
    lookup                     = 'pk'
    serializers_class          = FollowSerializer
    permission_classes         = [IsAuthenticated]

    def get_queryset(self):
        users = self.kwargs.get('pk')
        obj = Profile.objects.filter(user__id = users)
        qs = Profile.objects.following_feed(obj)
        return qs

class ProfileActionView(generics.CreateAPIView):
    """
    Performs Action on Profiles
    """
    queryset                    = Profile.objects.all()
    serializer_class            = ActionProfileSerializer
    permission_classes          = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = ActionProfileSerializer(data=request.data)
        me = request.user
        if serializer.is_valid():
            data = serializer.validated_data
            profile = data.get("id")
            qs = self.queryset.filter(user__id = profile)
            if not qs.exists():
                return Response({}, status=status.HTTP_404_NOT_FOUND)
            obj = qs.first()
            if me == obj.user:
                vs = obj.user
                qs = vs.my_followings.all()
                serializer = FollowSerializer(qs)
                return Response(serializer.data)
            action = data.get("action")
            if action == "follow":
                obj.followers.add(me)
                serializer = ProfileSerializer(obj)
                return Response(serializer.data)
            elif action == "unfollow":
                obj.followers.remove(me)
                serializer = ProfileSerializer(obj)
                return Response(serializer.data)
            else:
                pass
