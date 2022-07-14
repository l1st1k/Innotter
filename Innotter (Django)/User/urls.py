from .views import UserViewSet, JSONWebTokenAuthViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'', UserViewSet, basename='user')
router.register(r'token', JSONWebTokenAuthViewSet, basename='token')
urlpatterns = router.urls
