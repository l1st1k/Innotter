"""Innotter_Django URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from Page.views import SearchPageViewSet
from Post.views import FeedViewSet
from User.views import CreateTokenView, RefreshTokenView, SearchUserViewSet

schema_view = get_schema_view(
   openapi.Info(
      title="Snippets API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/user/', include('User.urls')),
    path('api/v1/page/', include('Page.urls')),
    path('api/v1/post/', include('Post.urls')),
    path('api/v1/feed/', FeedViewSet.as_view({'get': 'list'}), name='feed'),
    path('api/v1/search/user/', SearchUserViewSet.as_view({'get': 'list'}), name='search-user'),
    path('api/v1/search/page/', SearchPageViewSet.as_view({'get': 'list'}), name='search-page'),

    # JWT token urls
    path('api/v1/token/create/', CreateTokenView.as_view(), name='token_create'),
    path('api/v1/token/refresh/', RefreshTokenView.as_view(), name='token_refresh'),

    # Swagger urls
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
