import os
import uuid

from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify

User = get_user_model()


def blog_image_file_path(instance, filename):
    _, extension = os.path.splitext(filename)
    filename = f"{slugify(instance)}-{uuid.uuid4()}{extension}"

    return os.path.join("uploads/blogs/", filename)

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=150, blank=True)
    content = models.TextField()
    post_image = models.ImageField(null=True, upload_to=blog_image_file_path)
    author = models.ForeignKey('user.User', related_name='posts', on_delete=models.SET_NULL, null=True)
    is_hidden = models.BooleanField(default=False)
    is_edited = models.BooleanField(default=False)
    date_posted = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField(Category, related_name="posts")
    hashtag = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        ordering = ['-date_posted']


class Like(models.Model):
    created_by = models.ForeignKey("user.User", on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="likes")

    def __str__(self):
        return "{0} liked by {1}".format(self.post, self.created_by)


class Comment(models.Model):
    content = models.TextField()
    comment_image = models.ImageField(null=True, upload_to=blog_image_file_path)
    author = models.ForeignKey('user.User', on_delete=models.SET_NULL, null=True)
    date_posted = models.DateTimeField(auto_now_add=True)
    parent_post = models.ForeignKey('Post', on_delete=models.CASCADE,  related_name="comments")
