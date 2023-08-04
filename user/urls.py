from django.urls import path
from rest_framework.authtoken import views

from user.views import (
    CreateUserView,
    ListUserView,
    CreateTokenView,
    UpdateUserView
)

urlpatterns = [
    path("", ListUserView.as_view(), name="user-all"),
    path("register/", CreateUserView.as_view(), name="user-register"),
    path("update/", UpdateUserView.as_view(), name="user-update"),
    path('token/', CreateTokenView.as_view(), name="user-token")
]
app_name = "user"
