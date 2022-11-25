from django.urls import path


from frontend.views import accueil


urlpatterns = [
    path('',accueil, name='index'),
    #path('login/',LoginPageView.as_view(), name='login'),
]