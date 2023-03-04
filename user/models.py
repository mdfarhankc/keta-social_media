from django.db import models
from django.contrib.auth.models import User
from accounts.models import Profile
from datetime import datetime

# Create your models here.

class Post(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.CharField(
        max_length=100
    )

    image = models.FileField(
        max_length=2000,
        upload_to='Upload/Posted_Images',
        blank=True
    )

    text = models.CharField(
        max_length=500,
        blank=True
    )

    no_of_likes = models.BigIntegerField(
        default=0
    )

    created_at = models.DateTimeField(default=datetime.now)

    userid = models.ForeignKey(User,on_delete=models.DO_NOTHING)

    profile = models.ForeignKey(Profile,on_delete=models.DO_NOTHING)

    def __str__(self) -> str:
        return self.user
    


class PostLike(models.Model):
    
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    username = models.CharField(max_length=200)

    def __str__(self) -> str:
        return self.username
    


class Followers(models.Model):
    follower = models.CharField(max_length=200)

    following = models.CharField(max_length=200)

    