from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from user.views import CreateUserView, ListUserView, UpdateUserView

urlpatterns = [
    path("", ListUserView.as_view(), name="user-all"),
    path("register/", CreateUserView.as_view(), name="user-register"),
    path("update/", UpdateUserView.as_view(), name="user-update"),
    path("token/", TokenObtainPairView.as_view(), name="token-obtain-pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token-refresh"),  #  use in all endpoint authentication_classes = (JWTAuthentication,)
    path('token/verify/', TokenVerifyView.as_view(), name='token-verify'),

]
app_name = "user"
