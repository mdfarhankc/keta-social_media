from django.urls import path
from .views import *
from django.contrib.auth.views import PasswordResetView,PasswordResetDoneView,PasswordChangeDoneView,PasswordChangeView,PasswordResetCompleteView,PasswordResetConfirmView

urlpatterns = [
    path('',home,name='home'),
    path('login/',account_login,name='login'),
    path('register/',account_register,name='register'),
    path('logout/',account_logout,name='logout'),
    path('change_password/',change_password,name='change_password'),
    path('password-reset/',PasswordResetView.as_view(template_name='passwordreset.html'),name='password_reset'),
    path('password-reset/done/',PasswordResetDoneView.as_view(template_name='passwordresetdone.html'),name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',PasswordResetConfirmView.as_view(template_name='passwordresetconfirm.html'),name='password_reset_confirm'),
    path('password-reset-complete/',PasswordResetCompleteView.as_view(template_name='passwordresetcomplete.html'),name='password_reset_complete'),
    path('deactivate/',account_deactivate,name='deactivate'),

]