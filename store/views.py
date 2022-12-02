""" views function and class"""
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin

from django.urls import reverse
from django.views.generic import CreateView, ListView, DetailView, UpdateView

from frontend.models import Utilisateur
from store.forms import StoreForm
from store.models import Store


class StoreListView(ListView, LoginRequiredMixin):
    template_name = 'store/list-store.html'
    #queryset = Store.objects.all()
    model = Store

    context_object_name = 'stores'


class StoreCreateView(CreateView, LoginRequiredMixin, SuccessMessageMixin):
    template_name = 'store/add-store.html'
    model = Store
    form_class = StoreForm
    context_object_name = 'store'

    success_message = 'Store created successfully'

    def get_success_url(self):
        return reverse('store:list-store')

    def get_form_kwargs(self):
        kwargs = super(StoreCreateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        objStore = form.save(commit=False)
        objStore.proprietary = Utilisateur.objects.get(email=self.request.user.email)
        objStore.save()
        return super(StoreCreateView, self).form_valid(form)

class StoreUpdateView(UpdateView, SuccessMessageMixin, LoginRequiredMixin):
    template_name = 'store/edit-store.html'
    model = Store
    form_class = StoreForm
    context_object_name = 'store'

    success_message = 'Store edited successfully'

    def get_success_url(self):
        return reverse('store:list-store')

    def get_object(self, queryset=None):
        """ Hook to ensure object. """
        obj = super(StoreUpdateView, self).get_object()
        return obj

    def get_form_kwargs(self):
        kwargs = super(StoreUpdateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        objStore = form.save(commit=False)
        #objStore.proprietary = Utilisateur.objects.get(email=self.request.user.email)
        objStore.save()

        return super(StoreUpdateView, self).form_valid(form)



class StoreDetailsView(DetailView, LoginRequiredMixin):
    template_name = 'store/detail-store.html'
    model = Store
    context_object_name = 'store'

