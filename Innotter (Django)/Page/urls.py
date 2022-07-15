from .views import PageViewSet
from rest_framework.routers import DefaultRouter
# from rest_framework_extensions.routers import ExtendedSimpleRouter


router = DefaultRouter()
router.register(r'', PageViewSet, basename='page')
urlpatterns = router.urls
