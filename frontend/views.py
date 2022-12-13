""" frontend view
"""
from django.shortcuts import render

# Create your views here.
from store.models import Category, Store


def accueil(request):
    categories = Category.objects.all()
    stores = Store.objects.all()
    print('categories', categories)

    context = {
        'categories': categories,
        'stores': stores,
    }
    return render(request, 'frontend/home.html', context)


def resetpassword(request):
    return render(request, 'frontend/forgot-password.html')


"""
class ResetPasswordView(SuccessMessageMixin):
        model = Utilisateur
        form_class = ResetPasswordForm

        template_name = 'myaccount/forgot-password.html'

        context_object_name = "utilisateur"

        success_url = reverse_lazy('motdepasse-edit')

        success_message = "We sent you some instructions by email, to reset your password!"  # not to forget the mixin SuccessMessageMixin
"""
