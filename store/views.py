#!/usr/bin/env python
""" views function and class"""
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect

from django.urls import reverse
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView

from frontend.models import Utilisateur
from store.forms import StoreForm, ProductForm
from store.models import Store, Product


class StoreListView(LoginRequiredMixin, ListView ):
    template_name = 'store/list-store.html'
    #queryset = Store.objects.all()
    model = Store

    #context_object_name = 'stores'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        utilisateur = Utilisateur.objects.get(email=self.request.user.email)

        if (self.request.user.is_authenticated and utilisateur.is_admin):
            stores = Store.objects.all()

        else:
            stores = Store.objects.filter(proprietary=utilisateur)
            #stores = Store.objects.all()


        print('utilisateur', utilisateur.id)
        print('store', stores)
        context['stores'] = stores
        return context


class StoreCreateView(LoginRequiredMixin, CreateView, SuccessMessageMixin):
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

class StoreUpdateView(LoginRequiredMixin, UpdateView, SuccessMessageMixin ):
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

class StoreDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
  model = Store
  template_name = "store/delete-store.html"
  context_object_name = "store"

  success_message = "Store deleted successfully."

  def get_success_url(self):
    return reverse("store:list-store")


class StoreDetailsView(LoginRequiredMixin, DetailView ):
    template_name = 'store/detail-store.html'
    model = Store
    context_object_name = 'store'


class ProductListView(LoginRequiredMixin, ListView ):
    template_name = 'product/list-product.html'
    #queryset = Store.objects.all()
    model = Product

    context_object_name = 'products'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        products = None


        utilisateur = Utilisateur.objects.get(email=self.request.user.email)

        thestores = Store.objects.filter(proprietary=utilisateur)
        nbre = len(thestores)

        context['has_stores'] = True if nbre > 0 else False

        if (self.request.user.is_authenticated and utilisateur.is_admin):
            products = Product.objects.all()

        else:

            products = Product.objects.select_related('store__proprietary').filter(store__proprietary_id=utilisateur.id)


        context['products'] = products
        return context


class ProductCreateView(LoginRequiredMixin, CreateView ):
    template_name = 'product/add-product.html'
    #queryset = Store.objects.all()
    model = Product
    form_class = ProductForm

    context_object_name = 'product'

    def get_success_url(self):
        return reverse('store:list-product')

    """def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        proprietary = Utilisateur.objects.get(telephone=self.request.user.telephone)

        store = Store.objects.filter(proprietary= proprietary)
        print(type(store))

        context['store'] = store[1]

        return context

        print('proprietary', proprietary)"""

    def get_form_kwargs(self):
        kwargs = super(ProductCreateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user

        return kwargs


class ProductUpdateView(LoginRequiredMixin, UpdateView, SuccessMessageMixin ):
    template_name = 'product/edit-product.html'
    model = Product
    form_class = ProductForm
    context_object_name = 'product'

    success_message = 'Product edited successfully'

    def get_success_url(self):
        return reverse('store:list-product')

    def get_object(self, queryset=None):
        """ Hook to ensure object. """
        obj = super(ProductUpdateView, self).get_object()
        return obj

    def get_form_kwargs(self):
        kwargs = super(ProductUpdateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        objStore = form.save(commit=False)
        #objStore.proprietary = Utilisateur.objects.get(email=self.request.user.email)
        objStore.save()

        return super(ProductUpdateView, self).form_valid(form)

class ProductDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
  model = Product
  template_name = "product/delete-product.html"
  context_object_name = "product"

  success_message = "Product deleted successfully."

  def get_success_url(self):
    return reverse("store:list-product")