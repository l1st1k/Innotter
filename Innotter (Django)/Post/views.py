from rest_framework import viewsets, status
from .serializers import PostModelSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from .services import *
from Page.permissions import *
from .models import Post


class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostModelSerializer
    permission_classes = ()
    queryset = Post.objects.all()
    permissions_dict = {
        'list': (permissions.IsAuthenticated, PageIsPublic, PageIsntBlocked),
        'create': (permissions.IsAuthenticated, IsPageOwner),
        'partial_update': (permissions.IsAuthenticated, IsPageOwnerOrModeratorOrAdmin, PageIsntBlocked),
        'update': (permissions.IsAuthenticated, IsPageOwnerOrModeratorOrAdmin, PageIsntBlocked),
        'destroy': (permissions.IsAuthenticated, IsPageOwnerOrModeratorOrAdmin),
        'retrieve': (permissions.IsAuthenticated, PageIsPublicOrFollowerOrOwnerOrModeratorOrAdmin, PageIsntBlocked),
        'like': (permissions.IsAuthenticated, PageIsPublicOrFollowerOrOwnerOrModeratorOrAdmin, PageIsntBlocked),
    }

    # a method that set permissions depending on http request methods
    def get_permissions(self):
        if self.action in self.permissions_dict:
            perms = self.permissions_dict[self.action]
        else:
            perms = []
        return [permission() for permission in perms]

    # def check_permissions(self, request):
    #     obj = Page.objects.get(id=self.kwargs.get('parent_lookup_page_id'))
    #     self.check_object_permissions(request, obj)
    #     return super().check_permissions(request)

    # def get_object(self):
    #     return Post.objects.get(pk=self.kwargs['pk'])

    @action(detail=True, methods=('post',))
    def like(self, request):
        post = self.get_object()
        self.check_permissions(request)
        add_like_to_post(request, post)
        return Response({'message': 'Successfully liked!'}, status.HTTP_200_OK)
