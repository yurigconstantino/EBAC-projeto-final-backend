from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .viewsets import (
    RegisterViewSet,
    LoginViewSet,
    MeViewSet,
    FollowToggleView,
    FollowStatusView,
    FollowingListView,
    UpdateProfileView,
)

router = DefaultRouter()
router.register("register", RegisterViewSet, basename="register")

urlpatterns = [
    path("", include(router.urls)),
    path("login/", LoginViewSet.as_view(), name="login"),
    path("me/", MeViewSet.as_view(), name="me"),
    path("follow/<int:user_id>/", FollowToggleView.as_view(), name="follow-toggle"),
    path("follow/<int:user_id>/", FollowStatusView.as_view(), name="follow-status"),
    path("following/", FollowingListView.as_view(), name="following-list"),
    path("me/update/", UpdateProfileView.as_view(), name="update-profile"),
]
