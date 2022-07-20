from rest_framework import viewsets, status
from .serializers import PostModelSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from .services import *
from Page.permissions import *
from .models import Post
from Page.models import Page


class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostModelSerializer
    permission_classes = ()
    queryset = Post.objects.all()
    permissions_dict = {
        'list': (permissions.IsAuthenticated,),  # also got some permit checks in get_query
        'create': (permissions.IsAuthenticated,),  # overloaded below
        'partial_update': (permissions.IsAuthenticated, IsPageOwnerOrModeratorOrAdmin, PageIsntBlocked),
        'update': (permissions.IsAuthenticated, IsPageOwnerOrModeratorOrAdmin, PageIsntBlocked),
        'destroy': (permissions.IsAuthenticated, IsPageOwnerOrModeratorOrAdmin),
        'retrieve': (permissions.IsAuthenticated, PageIsPublicOrFollowerOrOwnerOrModeratorOrAdmin, PageIsntBlocked),
        'like': (permissions.IsAuthenticated, PageIsPublicOrFollowerOrOwnerOrModeratorOrAdmin, PageIsntBlocked)
    }

    # a method that set permissions depending on http request methods
    def get_permissions(self):
        if self.action in self.permissions_dict:
            perms = self.permissions_dict[self.action]
        else:
            perms = []
        return [permission() for permission in perms]

    def check_permissions(self, request):
        """
        Checking all the permissions according to the parent Page
        """
        if self.kwargs.get('pk', False):
            post = self.get_object()
            parent_page = Page.objects.get(id=post.page.id)
            self.check_object_permissions(request, parent_page)
        return super().check_permissions(request)

    def get_object(self):
        return Post.objects.get(pk=self.kwargs['pk'])

    def get_queryset(self):
        query = Post.objects.all()
        if self.action == 'list':
            return [post for post in query if user_is_able_to_see_the_post(self.request.user, post)]
        return query

    def create(self, request, *args, **kwargs):
        post_data = request.data
        if user_is_page_owner(request.user, post_data['page']):
            page = Page.objects.get(pk=post_data['page'])
            replied_post = None
            if post_data.get('reply_to', False):
                replied_post = Post.objects.get(pk=post_data['reply_to'])
            new_post = Post.objects.create(page=page, content=post_data['content'], reply_to=replied_post)
            new_post.save()
            serializer = PostModelSerializer(new_post)
            return Response(serializer.data)
        return Response({'message': 'You are not the owning this page!'}, status.HTTP_405_METHOD_NOT_ALLOWED)

    @action(detail=True, methods=('post',))
    def like(self, request):
        post = self.get_object()
        self.check_permissions(request)
        add_like_to_post(request, post)
        return Response({'message': 'Successfully liked!'}, status.HTTP_200_OK)
