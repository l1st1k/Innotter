from .views import UserAPIViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'', UserAPIViewSet, basename='users')
urlpatterns = router.urls
