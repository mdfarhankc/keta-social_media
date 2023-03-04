from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.

user = get_user_model()

class Profile(models.Model):
    user = models.ForeignKey(user,on_delete=models.CASCADE)

    prof_id = models.BigAutoField(primary_key=True)
    
    profilepic = models.ImageField(
        upload_to='Upload/ProfilePicture',
        default='Upload/ProfilePicture/defaultprofile.png',
    )

    bio = models.CharField(
        max_length=200,
        blank=True
    )

    location = models.CharField(
        max_length=200,
        blank=True
    )

    def __str__(self) -> str:
        return self.user.username