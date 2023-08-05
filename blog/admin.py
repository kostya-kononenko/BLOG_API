from django.contrib import admin

from blog.models import (Category, UserFollowing, Post, Like, Comment)

admin.site.register(Category)


@admin.register(UserFollowing)
class UserFollowingAdmin(admin.ModelAdmin):
    list_display = [
        "user_id",
        "following_user_id",
        "created",
    ]


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "author",
        "content",
    ]
    search_fields = ("title",)
    list_filter = ("title",)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = [
        "content",
        "date_posted",
    ]
    search_fields = ("content",)
    list_filter = ("content",)


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = [
        "created_by",
        "post",
    ]
    search_fields = ("created_by",)
    list_filter = ("created_by",)
