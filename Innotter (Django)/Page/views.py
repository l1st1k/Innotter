from django.shortcuts import render
from .permissions import *
from .serializers import *
from .services import add_follow_requests_to_request_data
from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response


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

    def check_permissions(self, request):
        try:
            obj = Page.objects.get(id=self.kwargs.get('pk'))
        except Page.DoesNotExist:  # exception when 'get' request on /pages/
            return Response({'message': 'Not found'}, status.HTTP_404_NOT_FOUND)
        else:
            self.check_object_permissions(request, obj)
        finally:
            return super().check_permissions(request)

    def get_serializer_class(self):
        if self.action in ('followers', 'follow_requests', 'follow'):
            self.serializer_class = PageModelFollowRequestsSerializer
            return self.serializer_class
        if self.request.user.role in (User.Roles.ADMIN, User.Roles.MODERATOR):
            self.serializer_class = PageAdminOrModerSerializer
        else:
            self.serializer_class = PageUserSerializer
        return self.serializer_class

    @action(detail=True, methods=('get', 'post'))
    def follow_requests(self, request, pk=None):
        # 'get' returns list of requests
        # 'post' updates list of requests (maybe should be 'patch')
        page = self.get_object()
        self.check_permissions(request)
        self.check_object_permissions(request, page)
        if page.is_private:
            if request.method == "GET":
                serializer = PageModelFollowRequestsSerializer(page)
                return Response({'follow_requests': serializer.data['follow_requests']}, status.HTTP_200_OK)
            elif request.method == 'POST':
                # there we're adding ids of already requested users
                # that allow user write only new follow_requests in request.data
                add_follow_requests_to_request_data(request.data, page.follow_requests)
                serializer = PageModelFollowRequestsSerializer(data=request.data)
                if serializer.is_valid():
                    serializer.update(page, request.data)
                    return Response({'message': 'Ok'}, status.HTTP_200_OK)
                return Response({'message': 'Your data is not valid'}, status.HTTP_400_BAD_REQUEST)
        return Response({"message": "Your page isn't private"}, status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=('get',))
    def followers(self, request, pk=None):
        # 'get' returns list of followers
        page = self.get_object()
        self.check_permissions(request)
        self.check_object_permissions(request, page)
        serializer = PageModelFollowRequestsSerializer(page)
        return Response({'followers': serializer.data['followers']}, status.HTTP_200_OK)


    # @action(detail=True, methods=('post',))
    # def follow(self, request, pk=None):
    #     # 'post' adding current user to the list of request of followers(in case of public page)
    #     pass


class TagViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin, mixins.DestroyModelMixin, mixins.RetrieveModelMixin,
                 mixins.ListModelMixin):
    """ViewSet for all Tag objects"""
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
