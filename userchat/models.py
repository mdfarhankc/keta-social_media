from django.db import models
from django.contrib.auth.models import User

class Chat(models.Model):

    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiver')
    message = models.TextField(max_length=2000)
    timestamp = models.DateTimeField(auto_now_add=True)