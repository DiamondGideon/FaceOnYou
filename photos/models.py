from django.contrib.auth.models import Permission, User
from django.db import models


class Post(models.Model):
    user = models.ForeignKey(User, default=1)
    post_title = models.CharField(max_length=500)
    hashtag = models.CharField(max_length=100)
    photo = models.FileField()
    is_favorite = models.BooleanField(default=False)

    def __str__(self):
        return self.post_title + ' - ' + self.hashtag


class Coment(models.Model):
    user = models.ForeignKey(User, default=1)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    text = models.CharField(max_length = 500)

    def __str__(self):
        return self.text

class Mask(models.Model):
    name = models.CharField(max_length=255)
    thumbnail = models.FileField(default= None)

    def __str__(self):
        return 'mask'