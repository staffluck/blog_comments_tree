from django.db import models
from mptt import models as mptt_models

# Create your models here.


class Post(models.Model):
    text = models.TextField(max_length=255)


class Comment(mptt_models.MPTTModel):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    parent = mptt_models.TreeForeignKey("self", on_delete=models.CASCADE, related_name="children", null=True)
    text = models.TextField("Текст комментария", max_length=144)

    class MPTTMeta:
        order_insertion_by = ['text']