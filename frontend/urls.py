from django.urls import path

from frontend.controller.LoginPage import LoginPageView
from frontend.controller.SignupPage import SignUpView
from frontend.views import accueil, resetpassword

app_name = 'frontend'
urlpatterns = [
    path('',accueil, name='index'),
    path('login/',LoginPageView.as_view(), name='login'),
    path('reset-password/',resetpassword, name='reset-password'),
    #path('signup/',LoginPageView.as_view(), name='signup'),
    path('signup/',SignUpView.as_view(), name='signup'),
]