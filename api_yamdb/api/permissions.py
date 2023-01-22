from rest_framework import permissions
from reviews.models import ADMIN


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the snippet.
        return obj.owner == request.user


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Права админа или только на чтение
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return request.user.is_admin


class IsAdminOrSuperUser(permissions.BasePermission):
    """
    Права админа или суперюзера системы
    """

    def has_permission(self, request, view):
        return (
            request.user.is_admin
            or request.user.is_superuser
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.user.is_admin
            or request.user.is_superuser
        )
