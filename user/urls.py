from .views import *

from django.contrib import admin
from django.urls import path,include



urlpatterns = [

path('login/',LoginUser.as_view() ,name="user-login"),
path('signup/',UserRegister.as_view() ,name="user-signup"),
path('changepassword/',ChangePassword.as_view() ,name="change-password"),
path('delete/',UserView.as_view() ,name="user-delete"),
path('get/',UserView.as_view() ,name="retrieve-user"),
path('update/',UserView.as_view() ,name="user-update"),
path('all/',UserRegister.as_view() ,name="users-list"),
path('forgetpassword/',UserForgetPassword.as_view(),name="forget-password"),
path('setpassword/<str:uidb64>/<str:token>/', SetNewPasswordAPIView.as_view(),
         name='password-reset-complete'),


]
