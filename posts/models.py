from django.db import models

# Create your models here.


class Post(models.Model):
    text = models.TextField(max_length=255)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    parent = models.ForeignKey("self", on_delete=models.CASCADE, related_name="children")
    text = models.TextField("Текст комментария", max_length=144)