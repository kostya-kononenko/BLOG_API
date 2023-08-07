from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=150, blank=True)
    content = models.TextField()
    category = models.ManyToManyField(Category, related_name="posts")
    post_image = models.CharField(max_length=32, blank=True)
    author = models.ForeignKey(
        "user.User", related_name="posts", on_delete=models.SET_NULL, null=True
    )
    is_hidden = models.BooleanField(default=False)
    is_edited = models.BooleanField(default=False)
    date_posted = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-date_posted"]


class Like(models.Model):
    created_by = models.ForeignKey("user.User", on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)


class Comment(models.Model):
    content = models.TextField()
    comment_image = models.CharField(max_length=32, blank=True)
    author = models.ForeignKey("user.User", on_delete=models.SET_NULL, null=True)
    is_edited = models.BooleanField(default=False)
    date_posted = models.DateTimeField(auto_now_add=True)
    parent_post = models.ForeignKey("Post", on_delete=models.CASCADE)
