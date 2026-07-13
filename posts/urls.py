from rest_framework.routers import DefaultRouter
from .viewsets import PostViewSet


router = DefaultRouter()
router.register("posts", PostViewSet)


urlpatterns = router.urls
