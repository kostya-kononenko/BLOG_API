from rest_framework import serializers
from .models import Post, Comment, Like, Category


class LikeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Like
        fields = (
            "id",
            "created_by",
            "post",
        )

    def validate(self, data):
        like = Like.objects.filter(post_id=data["post"], created_by_id=data["created_by"])
        if like:
            raise serializers.ValidationError("You had already liked this post")
        return data


class LikeDetailSerializer(serializers.ModelSerializer):
    first_name = serializers.ReadOnlyField(source='created_by.first_name')
    last_name = serializers.ReadOnlyField(source='created_by.last_name')

    class Meta:
        model = Like
        fields = (
            "id",
            "first_name",
            "last_name"
        )


class LikeListSerializer(serializers.ModelSerializer):
    post = serializers.CharField(source="post.title", read_only=True)

    class Meta:
        model = Like
        fields = (
            "id",
            "post",
        )


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = (
            "id",
            "content",
            "comment_image",
            "date_posted",
            "parent_post"
        )


class CommentDetailSerializer(serializers.ModelSerializer):
    first_name = serializers.ReadOnlyField(source='author.first_name')
    last_name = serializers.ReadOnlyField(source='author.last_name')

    class Meta:
        model = Comment
        fields = (
            "id",
            "first_name",
            "last_name",
            "content",
            "date_posted",
        )


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = (
            "id",
            "name",
        )


class PostSerializer(serializers.ModelSerializer):
    first_name = serializers.ReadOnlyField(source='author.first_name')
    last_name = serializers.ReadOnlyField(source='author.last_name')
    comments_count = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()
    category_count = serializers.SerializerMethodField()

    def get_comments_count(self, obj):
        return obj.comments.count()

    def get_likes_count(self, obj):
        return obj.likes.count()

    def get_category_count(self, obj):
        return obj.category.count()

    class Meta:
        model = Post
        fields = (
            "id",
            "title",
            "content",
            "post_image",
            "first_name",
            "last_name",
            "date_posted",
            "hashtag",
            "comments_count",
            "likes_count",
            "category_count",
        )


class PostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = (
            "title",
            "content",
            "post_image",
            "category",
            "hashtag"
        )


class PostDetailSerializer(serializers.ModelSerializer):
    first_name = serializers.ReadOnlyField(source='author.first_name')
    last_name = serializers.ReadOnlyField(source='author.last_name')
    likes = LikeDetailSerializer(many=True, read_only=True)
    comments = CommentDetailSerializer(many=True, read_only=True)
    category = CategorySerializer(many=True)
    # category = serializers.StringRelatedField(many=True)

    class Meta:
        model = Post
        fields = (
            "id",
            "first_name",
            "last_name",
            "title",
            "content",
            "post_image",
            "hashtag",
            "likes",
            "comments",
            "category",
        )
