#!/usr/bin/env python3
"""This module is about urls of frontend app
"""
from django.urls import path

from frontend.controller.LoginPage import LoginPageView
from frontend.controller.SignupPage import SignUpView
from frontend.views import accueil, resetpassword, listofstore,\
                        storedetails, productdetails, StoreListView, ShopListView

app_name = 'frontend'
urlpatterns = [
    path('', accueil, name='index'),
    path('login/', LoginPageView.as_view(), name='login'),
    path('reset-password/', resetpassword, name='reset-password'),
    # path('stores/', listofstore, name='stores'),
    path('stores/', StoreListView.as_view(), name='stores'),
    path('shop/', ShopListView.as_view(), name='shop'),
    #path('detail-store/<int:pk>',storedetails, name='detail-store'),
    path('detail-store/<uuid:pk>', storedetails, name='detail-store'),
    path('detail-product/<int:pk>', productdetails, name='detail-product'),
    path('signup/', SignUpView.as_view(), name='signup'),
]