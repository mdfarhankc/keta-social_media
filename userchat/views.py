from datetime import datetime
from django.shortcuts import render, redirect
from .models import Chat
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from accounts.models import Profile

# Create your views here.


@login_required(login_url='login')
def chat_home(request):
    profiles = Profile.objects.exclude(user_id=request.user.id)
    chatusers = []
    chats = []
    newchat = []
    chatsfilter = Chat.objects.filter(sender=request.user) | Chat.objects.filter(receiver=request.user)
    for chat in chatsfilter:
        if chat.sender not in chats:
            chats.append(chat.sender)
        if chat.receiver not in chats:
            chats.append(chat.receiver)
    for user in profiles:
        if user.user in chats:
            chatusers.append(user)
    for user in profiles:
        if user.user not in chats:
            newchat.append(user)
        
    
    context = {
        'profile':Profile.objects.get(user_id=request.user.id),
        'lenchat':len(chatusers),
        'lenusers':len(newchat),
        'chatusers':chatusers,
        'newchat':newchat
    }
    return render(request,'chathome.html',context)


@login_required(login_url='login')
def chat(request, username):
    user = request.user
    other_user = User.objects.get(username=username)
    other_user_profile = Profile.objects.get(user_id=other_user.id)
    chats = Chat.objects.filter(sender=user, receiver=other_user) | Chat.objects.filter(sender=other_user, receiver=user)
    chats = chats.order_by('timestamp')

    if request.method == 'POST':
        message = request.POST.get('message')
        if message != "":
            chat = Chat.objects.create(sender=user, receiver=other_user, message=message)
            print(chat.message)

            response_data = {
                'success': True,
                'message': chat.message,
                'sender_username': user.username,
                'timestamp': datetime.now().strftime("%b. %d, %Y, %I:%M %p")
            }
            return JsonResponse(response_data,safe=False)

    context = {
        'other_user': other_user,
        'chats': chats,
        'profile':Profile.objects.get(user_id=request.user.id),
        'other_user_profile':other_user_profile,
        }
    return render(request, 'chat.html', context)


# @login_required(login_url='login')
# def chat(request, username):
#     user = request.user
#     other_user = User.objects.get(username=username)
#     other_user_profile = Profile.objects.get(user_id=other_user.id)
#     chats = Chat.objects.filter(sender=user, receiver=other_user) | Chat.objects.filter(sender=other_user, receiver=user)

#     context = {
#         'other_user': other_user,
#         'chats': chats,
#         'profile': Profile.objects.get(user_id=request.user.id),
#         'other_user_profile': other_user_profile,
#     }
#     return render(request, 'chat.html', context)

# @login_required(login_url='login')
# def send_message(request,username):
#     if request.method == 'POST':
#         message = request.POST.get('message')
#         sender = request.user
#         receiver_username = username
#         receiver = User.objects.get(username=receiver_username)

#         chat = Chat.objects.create(sender=sender, receiver=receiver, message=message)
#         response_data = {
#             'success': True,
#             'message': chat.message,
#             'sender_username': sender.username,
#         }
#         return JsonResponse(response_data)

#     # return JsonResponse({'success': False, 'error': 'Invalid request method'})
#     return render(request, 'chat.html')