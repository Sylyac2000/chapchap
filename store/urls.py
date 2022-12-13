from django.urls import path

from store.views import (StoreListView, StoreCreateView, StoreUpdateView,
                         ProductListView, ProductCreateView,
                         ProductUpdateView, StoreDeleteView, ProductDeleteView)

app_name = 'store'

urlpatterns = [
    path('list-store/', StoreListView.as_view(), name='list-store'),
    path('add-store/', StoreCreateView.as_view(), name='add-store'),
    path('edit-store/<int:pk>', StoreUpdateView.as_view(), name='edit-store'),
    path('delete-store/<int:pk>', StoreDeleteView.as_view(), name='del-store'),
    path('list-product/', ProductListView.as_view(), name='list-product'),
    path('add-product/', ProductCreateView.as_view(), name='add-product'),
    path('edit-product/<int:pk>', ProductUpdateView.as_view(),
         name='edit-product'),
    path('delete-product/<int:pk>', ProductDeleteView.as_view(),
         name='del-product'),

]