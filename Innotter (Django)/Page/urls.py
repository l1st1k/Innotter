from .views import *
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'', PageViewSet, basename='page')
router.register(r'tag', TagViewSet, basename='tag')
urlpatterns = router.urls
