from django.shortcuts import render
from .permissions import *
from .serializers import *
from rest_framework import viewsets, mixins
from rest_framework.decorators import action


class PageViewSet(viewsets.ModelViewSet):
    """ViewSet for all Page objects"""
    queryset = Page.objects.all()
    permission_classes = []
    permissions_dict = {
        'partial_update': (permissions.IsAuthenticated, IsPageOwnerOrModeratorOrAdmin, PageIsntBlocked),
        'update': (permissions.IsAuthenticated, IsPageOwnerOrModeratorOrAdmin, PageIsntBlocked),
        'destroy': (permissions.IsAuthenticated, IsPageOwner),
        'create': (permissions.IsAuthenticated,),
        'list': (permissions.IsAuthenticated,),
        'retrieve': (permissions.IsAuthenticated, PageIsPublicOrOwner, PageIsntBlocked),
        'follow_requests': (permissions.IsAuthenticated, IsPageOwnerOrModeratorOrAdmin),
        'followers': (permissions.IsAuthenticated, IsPageOwnerOrModeratorOrAdmin, PageIsntBlocked),
        'follow': (permissions.IsAuthenticated, PageIsntBlocked)
    }

    # a method that set permissions depending on http request methods
    def get_permissions(self):
        if self.action in self.permissions_dict:
            perms = self.permissions_dict[self.action]
        else:
            perms = []
        return [permission() for permission in perms]

    def get_serializer_class(self):
        if self.request.user.role in (User.Roles.ADMIN, User.Roles.MODERATOR):
            self.serializer_class = PageAdminOrModerSerializer
        else:
            self.serializer_class = PageUserSerializer
        return self.serializer_class

    @action(detail=True, methods=('get', 'post'))
    def follow_requests(self, request, pk=None):
        # 'get' returns list of requests
        # 'post' updates list of requests (maybe should be 'patch')
        pass

    @action(detail=True, methods=('get',))
    def followers(self, request, pk=None):
        # 'get' return a list of followers
        pass

    @action(detail=True, methods=('post',))
    def follow(self, request, pk=None):
        # 'post' adding current user to the list of request of followers(in case of public page)
        pass


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
