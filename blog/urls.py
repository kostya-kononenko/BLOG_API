from django.urls import path, include
from rest_framework import routers

from blog.views import PostViewSet, CommentViewSet, CategoryViewSet

router = routers.DefaultRouter()
router.register("posts", PostViewSet)
router.register("comments", CommentViewSet)
router.register("category", CategoryViewSet)


urlpatterns = [
    path("", include(router.urls)),
    path("<int:pk>/like/", PostViewSet.as_view({"post": "like"}), name="like"),
    path("<int:pk>/unlike/", PostViewSet.as_view({"post": "unlike"}), name="unlike"),

]

app_name = "blog"
