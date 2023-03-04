from django.shortcuts import redirect, render,HttpResponse
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from .models import Profile
from user.models import Post,Followers,PostLike
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Create your views here.

def home(request):
    return render(request,'home.html')

def account_register(request):
    if request.method == 'GET':
        return render(request,'register.html')
    elif request.method == 'POST':
        fname = request.POST['firstname']
        lname = request.POST['lastname']
        uname = request.POST['username']
        email = request.POST['email']
        pic = request.FILES.get('profile')
        loc = request.POST.get('location')
        bio = request.POST.get('bio')
        password = request.POST['password']
        cpassword = request.POST['cpassword']
        if len(password) < 8:
            messages.info(request,"Password must contain atleast 8 characters!")
            return redirect('register')
        if password == cpassword:
            if User.objects.filter(email=email).exists():
                messages.info(request,"Email already exists!")
                return redirect('register')
            elif User.objects.filter(username=uname).exists():
                messages.info(request,"Username already exists!")
                return redirect('register')
            else:
                user = User(first_name=fname,last_name=lname,username=uname,email=email)
                user.set_password(password)
                user.save()
                profile = Profile(profilepic=pic,location=loc,bio=bio,user_id=user.id)
                profile.save()
                return redirect('login')
        else:
            messages.info(request,"Password and Confirm Password Doesnt match")
            return redirect('register')

def account_login(request):
    if request.method == 'GET':
        return render(request,'login.html')
    elif request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            if user.is_superuser == True:
                return redirect('/admin/')
            else:
                return redirect('user_home')
        else:
            messages.info(request,"Username or Password is Incorrect!!")
            return redirect('login')
        

def account_logout(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def account_deactivate(request):
    user = User.objects.get(id=request.user.id)
    profile = Profile.objects.get(user_id=request.user.id)
    posts = Post.objects.filter(user=request.user.username)
    followers = Followers.objects.filter(following=request.user.username)
    postslike = PostLike.objects.filter(username=request.user.username)
    postslike.delete()
    posts.delete()
    followers.delete()
    profile.delete()
    user.delete()
    logout(request)
    return render(request,'deactivate.html')

@login_required(login_url='login')
def change_password(request):
    if request.method == 'GET':
        form = PasswordChangeForm(request.user)
        context = {
            'form':form,
            'profile':Profile.objects.get(user_id=request.user.id)
        }
        return render(request,"changepassword.html",context)
    elif request.method == 'POST':
        form = PasswordChangeForm(request.user,request.POST)
        if form.is_valid():
            user = form.save()
            print(user)
            update_session_auth_hash(request,user) 
            messages.success(request,"Your Password Has Been Changed Successfully!")
            return redirect('my_profile')
        else:
            return render(request,"changepassword.html",{'form':form})

        