from django.urls import path, include
from rest_framework import routers

from user.views import CreateUserView, ListUserView

router = routers.DefaultRouter()
router.register("all_users", ListUserView)


urlpatterns = [
    path("", ListUserView.as_view(), name="user-all"),
    path("register/", CreateUserView.as_view(), name="user-register"),
]
app_name = "user"
