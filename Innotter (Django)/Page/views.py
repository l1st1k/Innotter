from django.shortcuts import render

from .permissions import *
from .serializers import *
from rest_framework import viewsets, mixins


class PageViewSet(viewsets.ModelViewSet):
    """ViewSet for all Page and Tokens objects"""
    queryset = Page.objects.all()
    # serializer_class = PageSerializer
    permission_classes = []
    permissions_dict = {
        # 'partial_update': (permissions.IsAuthenticated, IsUserOwnerOrAdmin),
        # 'update': (permissions.IsAuthenticated, IsUserOwnerOrAdmin),
        # 'destroy': (permissions.IsAuthenticated, IsUserOwnerOrAdmin),
        # 'create': (permissions.AllowAny,),
        # 'list': (permissions.IsAuthenticated, IsAdmin,),
        # 'retrieve': (permissions.IsAuthenticated,),
    }

    # a method that set permissions depending on http request methods
    def get_permissions(self):
        if self.action in self.permissions_dict:
            perms = self.permissions_dict[self.action]
        else:
            perms = []
        return [permission() for permission in perms]


class TagViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin, mixins.DestroyModelMixin, mixins.RetrieveModelMixin,
                 mixins.ListModelMixin):
    queryset = Tag.objects.all()
    serializer_class = TagModelSerializer
    permission_classes = ()
    permissions_dict = {
        'destroy': (permissions.IsAuthenticated, IsAdminOrModerator),
        'create': (permissions.IsAuthenticated, IsAdminOrModerator),
        'list': (permissions.IsAuthenticated,),
        'retrieve': (permissions.IsAuthenticated,),
    }

    # a method that set permissions depending on http request methods
    def get_permissions(self):
        if self.action in self.permissions_dict:
            perms = self.permissions_dict[self.action]
        else:
            perms = []
        return [permission() for permission in perms]
