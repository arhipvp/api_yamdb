from typing import Any

from django.http import HttpRequest
from rest_framework import permissions, viewsets


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        if (
            request.method in permissions.SAFE_METHODS
            or obj.owner == request.user
        ):

            return True


class IsSuperUserOrReadOnly(permissions.BasePermission):
    """
    Права SuperUser или только на чтение
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_superuser


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Права админа или только на чтение
    """
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return (
                request.method in permissions.SAFE_METHODS
                or request.user.is_admin
            )
        return request.method in permissions.SAFE_METHODS

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


class IsAuthorOrModeratorOrAdminOrSuperuser(permissions.BasePermission):
    def has_permission(
        self,
        request: HttpRequest,
        unused: viewsets,
    ) -> bool:
        del unused
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(
        self,
        request: HttpRequest,
        unused: viewsets,
        obj: Any,
    ) -> bool:
        del unused
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
            or request.user.is_admin
            or request.user.is_superuser
            or request.user.is_moderator
        )
