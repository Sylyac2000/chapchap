from django.urls import path

from frontend.controller.LoginPage import LoginPageView
from frontend.views import accueil

app_name = 'frontend'
urlpatterns = [
    path('',accueil, name='index'),
    path('login/',LoginPageView.as_view(), name='login'),
]