from django.urls import path
from .views import *

urlpatterns = [
    path('<str:username>/',chat,name='chat'),
    # path('send_message/<str:username>/',send_message,name='send_message'),
]