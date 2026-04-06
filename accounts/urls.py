from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .viewsets import RegisterViewSet, LoginViewSet, MeViewSet

router = DefaultRouter()
router.register("register", RegisterViewSet, basename="register")

urlpatterns = [
    path("", include(router.urls)),
    path("login/", LoginViewSet.as_view(), name="login"),
    path("me/", MeViewSet.as_view(), name="me"),
]
