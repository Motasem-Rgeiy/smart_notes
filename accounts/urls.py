from django.urls import path , include
from django.contrib.auth.views import LoginView
from accounts import forms
from . import views

urlpatterns = [
    path('login/' , LoginView.as_view(authentication_form = forms.UserLoginForm) , name = 'login'),
    path('register/' , views.UserRegisterView.as_view() , name='register'),
    path('profile' , views.UserChangeView.as_view() , name= 'profile'),
    path('' , include('django.contrib.auth.urls')),

]
