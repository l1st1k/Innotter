from django.shortcuts import render
from User.models import User
from User.permissions import *
from User.serializers import UserSerializer
from rest_framework import viewsets
from Page.models import Tag
from rest_framework.decorators import action


class UserAPIViewSet(viewsets.ModelViewSet):
    """ViewSet for all User objects"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = []
    permissions_dict = {
                        'partial_update': (permissions.IsAuthenticated, IsUserOwnerOrAdmin),
                        'update': (permissions.IsAuthenticated, IsUserOwnerOrAdmin),
                        'destroy': (permissions.IsAuthenticated, IsUserOwnerOrAdmin),
                        'create': (permissions.AllowAny,),
                        'list': (permissions.IsAuthenticated, IsAdmin,),
                        'retrieve': (permissions.IsAuthenticated,),
                        }

    # a method that set permissions depending on http request methods
    def get_permissions(self):
        if self.action in self.permissions_dict:
            perms = self.permissions_dict[self.action]
        else:
            perms = []
        return [permission() for permission in perms]
