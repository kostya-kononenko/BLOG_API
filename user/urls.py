from django.urls import path
from rest_framework.authtoken import views

from user.views import CreateUserView, ListUserView, CreateTokenView

urlpatterns = [
    path("", ListUserView.as_view(), name="user-all"),
    path("register/", CreateUserView.as_view(), name="user-register"),
    path('token/', CreateTokenView.as_view(), name="user-token")
]
app_name = "user"
