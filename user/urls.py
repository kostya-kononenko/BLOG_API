from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from user.views import (
    CreateUserView,
    ListUserView,
    UpdateUserView,
    DetailUserView,
    UserFollowingView,
    UserFollow
)

router = routers.DefaultRouter()
router.register("following", UserFollowingView)


urlpatterns = [
    path("", ListUserView.as_view(), name="user-all"),
    path("", include(router.urls)),
    path("<int:pk>/", DetailUserView.as_view(), name="user-detail"),
    path("register/", CreateUserView.as_view(), name="user-register"),
    path("update/", UpdateUserView.as_view(), name="user-update"),
    path('follow/<int:pk>/', UserFollow.as_view(), name='user-follow'),
    path("token/", TokenObtainPairView.as_view(), name="token-obtain-pair"),
    path(
        "token/refresh/", TokenRefreshView.as_view(), name="token-refresh"
    ),  #  TODO use in all endpoint authentication_classes = (JWTAuthentication,)
    path("token/verify/", TokenVerifyView.as_view(), name="token-verify"),
]
app_name = "user"
