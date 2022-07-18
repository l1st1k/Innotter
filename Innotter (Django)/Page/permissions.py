from rest_framework import permissions
from User.models import *
from django.contrib.auth.models import AnonymousUser
from .models import *


class IsAdminOrModerator(permissions.BasePermission):
    def has_permission(self, request, view):
        if isinstance(request.user, AnonymousUser):
            return False
        return request.user.role == User.Roles.ADMIN or request.user.role == User.Roles.MODERATOR
