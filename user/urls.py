from django.urls import path
from .views import *


urlpatterns = [
    path('',user_home,name='user_home'),
    path('post_text/',post_text,name='post_text'),
    path('post_image/',post_image,name='post_image'),
    path('remove_profilepic/',remove_profilepic,name='remove_profilepic'),
    path('deletepost/<int:id>',deletepost,name='delete_post'),
    path('post_likes/<int:id>/',post_likes,name='post_likes'),
    path('my_profile/',my_profile,name='my_profile'),
    path('updateprofile/',updateprofile,name='updateprofile'),
    path('updateprofilepic/',updateprofilepic,name='update_profilepic'),
    path('profile/<username>/',user_profile,name='user_profile'),
    # path('search_username/',search_username,name='search_username'),
    path('followers/<username>/',followers,name='followers'),
    path('homefollower/<username>/',homefollower,name='homefollower'),
]