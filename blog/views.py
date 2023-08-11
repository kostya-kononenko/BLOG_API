from django.db.models import Q
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from blog.models import Post, Comment, Category, Like
from blog.permissions import IsOwnerOrReadOnly
from blog.serializers import (
    PostSerializer,
    CommentSerializer,
    CategorySerializer,
    LikeSerializer,
    PostDetailSerializer,
    PostCreateSerializer,
)


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.select_related("author")
    permission_classes = (IsOwnerOrReadOnly,)

    def get_queryset(self):
        title = self.request.query_params.get("title")
        hashtag = self.request.query_params.get("hashtag")

        queryset = self.queryset.filter(
            Q(author=self.request.user)
            | Q(author__in=self.request.user.following.values("following_user_id"))
        )
        if title:
            queryset = queryset.filter(title__icontains=title)

        if hashtag:
            queryset = queryset.filter(hashtag__icontains=hashtag)

        return queryset

    def get_serializer_class(self):
        if self.action == "retrieve":
            return PostDetailSerializer
        if self.action == "create":
            return PostCreateSerializer
        if self.action == "like":
            return LikeSerializer
        return PostSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=True, methods=["post"], url_path="like")
    def like(self, request, pk):
        post = get_object_or_404(Post, id=pk)
        created_by = request.user
        serializer = LikeSerializer(data={"post": post.id, "created_by": created_by.id})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        response_serializer = PostDetailSerializer(post)
        return Response(response_serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["post"], url_path="unlike")
    def unlike(self, request, pk):
        post = get_object_or_404(Post, id=pk)
        created_by = request.user
        like = Like.objects.filter(post=post.id, created_by=created_by.id)
        if not like:
            raise ValidationError("You hadn't liked this post yet")
        like.delete()
        response_serializer = PostDetailSerializer(post)
        return Response(response_serializer.data, status=status.HTTP_200_OK)

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.select_related("author", "parent_post")
    serializer_class = CommentSerializer
    permission_classes = (IsOwnerOrReadOnly,)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

