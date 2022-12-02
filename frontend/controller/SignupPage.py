from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic import CreateView

from frontend.forms import SignupForm
from frontend.models import Utilisateur


def inscription(request):

    return render(request, 'registration/signup.html')

class SignUpView(generic.CreateView):
    form_class = SignupForm
    success_url = reverse_lazy('frontend:login')
    template_name = 'registration/signup.html'

class UtilisateurCreatePageView(LoginRequiredMixin, CreateView):
    model = Utilisateur
    form_class = SignupForm
    template_name = "frontend/test.html"
    """context_object_name = "utilisateur"

    success_url = reverse_lazy('login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        utilisateur = Utilisateur.objects.get(username=self.request.user)
        context["utilisateur"] = Utilisateur.objects.get(username=self.request.user)

        return context

    def form_valid(self, form):
        anutilisateur = form.save(commit=False)
        anutilisateur.username = form.cleaned_data.get("email")
        anutilisateur.save()

        messages.success(self.request, "Compte utilisateur créé avec succès!")

        return super(UtilisateurCreatePageView,self).form_valid(form)"""
