from django.urls import path, include
from rest_framework import routers

from blog.views import PostViewSet, CommentViewSet, CategoryViewSet

router = routers.DefaultRouter()
router.register("posts", PostViewSet)
router.register("comments", CommentViewSet)
router.register("category", CategoryViewSet)


urlpatterns = router.urls

app_name = "blog"
