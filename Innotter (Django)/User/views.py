import django_filters.rest_framework
from django.contrib.auth import get_user_model
from rest_framework import mixins, parsers, renderers, status, viewsets
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.decorators import action
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from User.permissions import *
from User.serializers import UserSerializer

from .services import *

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
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
        'image': (permissions.IsAuthenticated, IsUserOwnerOrAdmin,)
    }

    # a method that set permissions depending on http request methods
    def get_permissions(self):
        if self.action in self.permissions_dict:
            perms = self.permissions_dict[self.action]
        else:
            perms = []
        return [permission() for permission in perms]

    @action(detail=True, methods=('post', 'get'))
    def image(self, request, pk=None):
        """
        'POST' uploads new user's image, 'GET' returns link for the image

        No parameters there, only file with avatar. Image should be in 'jpg' or 'png' format.
        """
        user = self.get_object()
        if request.method == "POST":
            image = request.data['upload']
            ALLOWABLE_IMAGE_FORMATS = ('png', 'jpeg', 'jpg')
            img_format = image.name.split('.')[-1]
            if img_format in ALLOWABLE_IMAGE_FORMATS:
                image.name = f'user_{user.pk}_{datetime.datetime.now().date()}.{img_format}'
                s3_url = upload_image_to_s3(image)
                user.image_s3_path = s3_url
                user.save()
                response = Response({"message": "Successfully uploaded!", "S3 URL": s3_url}, status.HTTP_200_OK)
            else:
                response = Response({"message": "Image should be in ('.png', '.jpeg', '.jpg') format!"},
                                    status.HTTP_400_BAD_REQUEST)
        elif request.method == 'GET':
            if user.image_s3_path:
                response = Response({"message": "Success!", "S3 URL": user.image_s3_path}, status.HTTP_200_OK)
            else:
                response = Response({"message": "There is no image for this user :("}, status.HTTP_400_BAD_REQUEST)
        return response


class CreateTokenView(GenericAPIView):
    throttle_classes = ()
    permission_classes = (permissions.AllowAny,)
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.JSONParser,)
    renderer_classes = (renderers.JSONRenderer,)
    serializer_class = AuthTokenSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            token = generate_access_token(user)
            refresh_token = generate_refresh_token()
            set_refresh_token(refresh_token=refresh_token, user=user)
            response = Response({'access_token': token, 'refresh_token': refresh_token})
            response.set_cookie(
                key=settings.CUSTOM_JWT['AUTH_COOKIE'],
                value=token,
                expires=settings.CUSTOM_JWT['ACCESS_TOKEN_LIFETIME'],
                secure=settings.CUSTOM_JWT['AUTH_COOKIE_SECURE'],
                httponly=settings.CUSTOM_JWT['AUTH_COOKIE_HTTP_ONLY'],
                samesite=settings.CUSTOM_JWT['AUTH_COOKIE_SAMESITE']
            )
            response.set_cookie(
                key=settings.CUSTOM_JWT['AUTH_COOKIE_REFRESH'],
                value=refresh_token,
                expires=settings.CUSTOM_JWT['REFRESH_TOKEN_LIFETIME'],
                secure=settings.CUSTOM_JWT['AUTH_COOKIE_SECURE'],
                httponly=settings.CUSTOM_JWT['AUTH_COOKIE_HTTP_ONLY'],
                samesite=settings.CUSTOM_JWT['AUTH_COOKIE_SAMESITE']
            )

            return response
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RefreshTokenView(GenericAPIView):
    throttle_classes = ()
    permission_classes = (permissions.AllowAny,)
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.JSONParser,)
    renderer_classes = (renderers.JSONRenderer,)
    serializer_class = AuthTokenSerializer

    def post(self, request):
        refresh_token = request.COOKIES.get(settings.CUSTOM_JWT['AUTH_COOKIE_REFRESH'])
        new_tokens = check_and_update_refresh_token(refresh_token)
        if refresh_token and new_tokens:
            response = Response(new_tokens)
            response.set_cookie(
                key=settings.CUSTOM_JWT['AUTH_COOKIE'],
                value=new_tokens[settings.CUSTOM_JWT['AUTH_COOKIE']],
                expires=settings.CUSTOM_JWT['ACCESS_TOKEN_LIFETIME'],
                secure=settings.CUSTOM_JWT['AUTH_COOKIE_SECURE'],
                httponly=settings.CUSTOM_JWT['AUTH_COOKIE_HTTP_ONLY'],
                samesite=settings.CUSTOM_JWT['AUTH_COOKIE_SAMESITE']
            )
            response.set_cookie(
                key=settings.CUSTOM_JWT['AUTH_COOKIE_REFRESH'],
                value=new_tokens[settings.CUSTOM_JWT['AUTH_COOKIE_REFRESH']],
                expires=settings.CUSTOM_JWT['REFRESH_TOKEN_LIFETIME'],
                secure=settings.CUSTOM_JWT['AUTH_COOKIE_SECURE'],
                httponly=settings.CUSTOM_JWT['AUTH_COOKIE_HTTP_ONLY'],
                samesite=settings.CUSTOM_JWT['AUTH_COOKIE_SAMESITE']
            )
            return response
        return Response({'message': "Your token isn't valid"})


class SearchUserViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = User.objects.all()
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filterset_fields = ('username', 'email')
