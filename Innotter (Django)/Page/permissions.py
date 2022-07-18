from rest_framework import permissions
from User.models import *
from django.contrib.auth.models import AnonymousUser
from .services import is_page_unblocked


class PageIsPublic(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return not obj.is_private


class IsAdminOrModerator(permissions.BasePermission):
    def has_permission(self, request, view):
        if isinstance(request.user, AnonymousUser):
            return False
        return request.user.role == User.Roles.ADMIN or request.user.role == User.Roles.MODERATOR


class PageIsPublicOrOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return PageIsPublic.has_object_permission(self, request, view, obj)\
               or IsPageOwner.has_object_permission(self, request, view, obj)


class IsPageOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user


class IsPageOwnerOrModeratorOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return IsAdminOrModerator.has_permission(self, request, view)\
               or IsPageOwner.has_object_permission(self, request, view, obj)


class PageIsntBlocked(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj.unblock_date:
            return is_page_unblocked(obj.unblock_date)
        return IsAdminOrModerator.has_permission(self, request, view)
