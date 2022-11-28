"""routes of myaccount application"""
from django.contrib.auth.views import LogoutView
from django.urls import path

import myaccount
from myaccount.views import dashboard
app_name = 'myaccount'

urlpatterns = [
    path('dashboard/',dashboard, name='dashboard'),
    path('logout/', LogoutView.as_view(), name='logout'),  # extending  Django built in logout
]