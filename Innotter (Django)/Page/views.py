from .permissions import *
from .serializers import *
from .services import add_follow_requests_to_request_data, user_is_in_page_follow_requests_or_followers,\
                        add_user_to_page_follow_requests, add_user_to_page_followers
from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response
from Post.serializers import PostModelSerializer
from Post.models import Post


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
        'follow': (permissions.IsAuthenticated, PageIsntBlocked),
        'posts': (permissions.IsAuthenticated, PageIsntBlocked, PageIsPublicOrFollowerOrOwnerOrModeratorOrAdmin)
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
        """
        'GET' returns list of requests 'POST' updates list of requests (according to accepted or denied requests)

        Send one of 2 parameters: {"accept_ids": [0,1,2,3]} or {"deny_ids": [0,1,2,3]}
        """
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
        """
        'GET' returns list of followers for chosen page

        No parameters there
        """
        page = self.get_object()
        self.check_permissions(request)
        self.check_object_permissions(request, page)
        serializer = PageModelFollowRequestsSerializer(page)
        return Response({'followers': serializer.data['followers']}, status.HTTP_200_OK)

    @action(detail=True, methods=('post',))
    def follow(self, request, pk=None):
        """
        'POST' following or sending a follow_request

        No data required there. Just send {}
        """
        # 'post' adding current user to the list of request of followers(in case of public page)
        page = self.get_object()
        self.check_permissions(request)
        self.check_object_permissions(request, self.get_object())
        # 'already sent' case
        if user_is_in_page_follow_requests_or_followers(request.user, page):
            return Response({"message": "You are already sent follow request"}, status.HTTP_400_BAD_REQUEST)
        # 'new follow_request' case
        if page.is_private:
            add_user_to_page_follow_requests(request.user, page)
            page.save()
            return Response({'message': 'Your follow request successfully sent!'}, status.HTTP_200_OK)
        else:
            add_user_to_page_followers(request.user, page)
            page.save()
            return Response({'message': 'Successfully followed!'}, status.HTTP_200_OK)

    @action(detail=True, methods=('get',))
    def posts(self, request, pk=None):
        """
        'GET' returns list of posts for chosen page

        No parameters there
        """
        page = self.get_object()
        self.check_permissions(request)
        self.check_object_permissions(request, page)
        query = Post.objects.filter(page=page)
        post_serializer = PostModelSerializer(query, many=True)
        return Response({'posts': post_serializer.data}, status.HTTP_200_OK)


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
