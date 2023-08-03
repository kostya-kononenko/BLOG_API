from django.urls import path, include
from rest_framework import routers


router = routers.DefaultRouter()
# router.register("posts", PostViewSet)
# router.register("authors", AuthorViewSet)
# router.register("category`s", CategoryViewSet)
# router.register("comments", CommentViewSet)


urlpatterns = [
    path("", include(router.urls)),
]
app_name = "blog"
