from rest_framework import permissions
from .models import Profiles

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    This permission only allows owner to edit posts
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.owner == request.user


class IsOwners(permissions.BasePermission):
    """
    This permission only allows owner to View posts
    """

    def has_permission(self, request, view):
        user = request.user
        not_owner = Group.objects.filter(user= user)
        return not not_owner