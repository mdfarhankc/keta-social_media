from itertools import chain
from django.shortcuts import render,redirect,HttpResponse
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Post,PostLike,Followers
from django.contrib.auth.models import User
from accounts.models import Profile
from django.contrib import messages
import os
from django.conf import settings



@login_required(login_url='login')
def user_home(request):
    if request.method == 'GET':
        posts = Post.objects.all().exclude(user=request.user.username)
        users = User.objects.exclude(username=request.user.username).exclude(username='admin')
        users_list = []
        usersuggestion = []
        followfilter = Followers.objects.filter(following=request.user.username)
        followlist= []
        for followers in followfilter:
            followlist.append(followers.follower)
        for user in users:
            users_iter = User.objects.get(username=user.username)
            users_list.append(users_iter)
        for user in users_list:
            if (user.username not in followlist):
                usersuggestion.append(Profile.objects.get(user_id=user.id))
        usersuglen = len(usersuggestion)
        context = {
            'name': request.user,
            'posts': posts,
            'lenpost':len(posts),
            'profile':Profile.objects.get(user_id=request.user.id),
            'usersuggestion':usersuggestion,
            'usersuglen':usersuglen,
        }
        return render(request,'userhome.html',context)
    elif request.method == 'POST':
        username = request.POST['susername']
        if username != "":
            users = User.objects.filter(username__icontains=username).exclude(username=request.user.username)
            profile = []
            for user in users:
                profile.append(Profile.objects.filter(user_id=user.id))
            print(profile)
            profile = list(chain(*profile))
            context = {
                'profiles':profile,
                'lenprof':len(profile),
                'username':username,
                'profile':Profile.objects.get(user_id=request.user.id),
                }
            return render(request,'search.html',context)
        else:
            return redirect('user_home')



@login_required(login_url='login')
def updateprofile(request):
    profile = Profile.objects.get(user_id=request.user.id)
    user = User.objects.get(id=request.user.id)
    if request.method == 'GET':
        context = {
            'profile':profile
        }
        return render(request,'updateprofile.html',context)
    elif request.method == 'POST':
        fname = request.POST['firstname']
        lname = request.POST['lastname']
        uname = request.POST['username']
        email = request.POST['email']
        loc = request.POST.get('location')
        bio = request.POST.get('bio')
        if (User.objects.filter(email=email).exists()) and (email != request.user.email):
            messages.info(request,"Email already exists!")
            return redirect('updateprofile')
        elif (User.objects.filter(username=uname).exists()) and (uname != request.user.username):
            messages.info(request,"Username already exists!")
            return redirect('updateprofile')
        else:
            profile.bio = bio
            profile.location = loc
            user.first_name = fname
            user.last_name = lname
            user.username = uname
            user.email = email
            profile.save()
            user.save()
            return redirect('my_profile')
        

@login_required(login_url='login')
def updateprofilepic(request):
    profile = Profile.objects.get(user_id=request.user.id)
    if request.method == 'GET':
        return render(request,'updateprofilepic.html',{'profilepic':profile.profilepic})
    elif request.method == 'POST':
        pic = request.FILES.get('pic')
        profile.profilepic = pic
        profile.save()
        return redirect('my_profile')
    


@login_required(login_url='login')
def post_text(request):
    profile = Profile.objects.get(user_id=request.user.id)
    if request.method == 'GET':
        return render(request,'posttext.html',{'profile':profile})
    elif request.method == 'POST':
        user = User.objects.get(id=request.user.id)
        text = request.POST.get('post')
        if text == '':
            messages.info(request,"Dont submit without any post content!")
            return redirect('post_text')
        else:
            print(profile)
            post = Post(user=request.user.username,text=text,userid_id=user.id,profile_id=profile.prof_id)
            post.save()
            return redirect('user_home')
        



@login_required(login_url='login')
def post_image(request):
    profile = Profile.objects.get(user_id=request.user.id)
    if request.method == 'GET':
        return render(request,'postimage.html',{'profile':profile})
    elif request.method == 'POST':
        user = User.objects.get(id=request.user.id)
        text = request.POST.get('post')
        image = request.FILES.get('image')
        if image == None:
            messages.info(request,"Dont submit without any post content!")
            return redirect('post_image')
        else:
            print(profile)
            post = Post(user=request.user.username,text=text,image=image,userid_id=user.id,profile_id=profile.prof_id)
            post.save()
            return redirect('user_home')
    


@login_required(login_url='login')
def deletepost(request,id):
    post = Post.objects.get(id=id)
    url = str(post.image)
    post.delete()
    paths = os.path.join(settings.MEDIA_ROOT,url)
    os.remove(paths)
    return redirect('my_profile')

@login_required(login_url='login')
def remove_profilepic(request):
    profile = Profile.objects.get(user_id=request.user.id)
    profilepic = str(profile.profilepic)
    profile.profilepic = None
    profile.save()
    print(profile)
    paths = os.path.join(settings.MEDIA_ROOT,profilepic)
    os.remove(paths)
    messages.info(request,"Profile Picture Has Been Removed!")
    return redirect('my_profile')



# @login_required(login_url='login')
# def post_like(request,id):
#     post = Post.objects.get(id=id)
#     username = request.user.username
#     postlike = PostLike.objects.filter(post_id=id,username=username).first()
#     print(postlike)
#     if postlike == None:
#         newlike = PostLike(post_id=id,username=username)
#         newlike.save()
#         post.no_of_likes = post.no_of_likes+1
#         post.save()
#         return redirect('user_home')
#     else:
#         postlike.delete()
#         post.no_of_likes = post.no_of_likes-1
#         post.save()
#         return redirect('user_home')

@login_required(login_url='login')
def post_likes(request,id):
    if request.method == 'POST':
        post = Post.objects.get(id=id)
        username = request.user.username
        postlike = PostLike.objects.filter(post_id=id,username=username).first()
        if postlike == None:
            newlike = PostLike(post_id=id,username=username)
            newlike.save()
            post.no_of_likes = post.no_of_likes+1
            post.save()
        else:
            postlike.delete()
            post.no_of_likes = post.no_of_likes-1
            post.save()
        data = {
            'no_of_likes':post.no_of_likes
        }
        return JsonResponse(data)
    return HttpResponse("Request method is not POST")


@login_required(login_url='login')
def my_profile(request):
    user = User.objects.get(id=request.user.id)
    profile = Profile.objects.get(user_id=request.user.id)
    posts = Post.objects.filter(user=request.user.username)
    followingfilter = Followers.objects.filter(following=request.user.username)
    following = len(followingfilter)
    followerfilter = Followers.objects.filter(follower=request.user.username)
    follower = len(followerfilter)
    context = {
        'user':user,
        'profile':profile,
        'posts':posts,
        'no_of_posts':len(posts),
        'follower':follower,
        'following':following,
    }
    return render(request,'myprofile.html',context)


@login_required(login_url='login')
def user_profile(request,username):
    if username == request.user.username:
        return redirect('my_profile')
    else:
        followingfilter = Followers.objects.filter(following=username)
        following = len(followingfilter)
        followerfilter = Followers.objects.filter(follower=username)
        follower = len(followerfilter)
        followfilter = Followers.objects.filter(follower=username,following=request.user.username).first()
        user = User.objects.get(username=username)
        profile = Profile.objects.get(user_id=user.id)
        posts = Post.objects.filter(user=username)
        context = {
            'user':user,
            'profiles':profile,
            'posts':posts,
            'no_of_posts':len(posts),
            'follower':follower,
            'following':following,
            'followfilter':followfilter,
            'profile':Profile.objects.get(user_id=request.user.id)
        }
        return render(request,'userprofile.html',context)


# @login_required(login_url='login')
# def search_username(request):
#     if request.method == 'GET':
#         return render(request,'userhome.html')
#     elif request.method == 'POST':
#         username = request.POST['susername']
#         users = User.objects.filter(username__icontains=username)
#         profile = []
#         for user in users:
#             profile.append(Profile.objects.filter(user_id=user.id))
#         print(profile)
#         profile = list(chain(*profile))
#         context = {
#             'profiles':profile,
#             'username':username,
#             'profile':Profile.objects.get(user_id=request.user.id),
#             }
#         return render(request,'search.html',context)
    



@login_required(login_url='login')
def homefollower(request,username):
    follower = username
    following = request.user.username
    followerfilter = Followers.objects.filter(follower=follower,following=following).first()
    if followerfilter == None:
        follow = Followers(follower=follower,following=following)
        follow.save()
    else:
        followerfilter.delete()
    return redirect('user_home')
        


@login_required(login_url='login')
def followers(request,username):
    if request.method == 'POST':
        follower = username
        following = request.user.username
        followerfilter = Followers.objects.filter(follower=follower,following=following).first()
        if followerfilter == None:
            follow = Followers(follower=follower,following=following)
            follow.save()
            f = False
        else:
            followerfilter.delete()
            f = True
        data = {
            'follow':f,
            'followers':len(Followers.objects.filter(follower=follower))
        }
        return JsonResponse(data)
    return HttpResponse("Not GET")


