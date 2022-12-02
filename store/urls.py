from django.urls import path

from store.views import StoreListView, StoreCreateView, StoreUpdateView

app_name = 'store'

urlpatterns = [
    path('list-store/', StoreListView.as_view(), name='list-store'),
    path('add-store/', StoreCreateView.as_view(), name='add-store'),
    path('edit-store/<int:pk>', StoreUpdateView.as_view(), name='edit-store'),
]