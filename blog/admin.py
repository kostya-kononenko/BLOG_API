from django.contrib import admin

from blog.models import (Category, UserFollowing, Post, Like, Comment)

admin.site.register(Category)
admin.site.register(UserFollowing)
admin.site.register(Post)
admin.site.register(Like)
admin.site.register(Comment)
