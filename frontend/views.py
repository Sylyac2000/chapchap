#!/usr/bin/env python3
"""This module is about : views.py
"""
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from el_pagination.views import AjaxListView
from store.models import Category, Store, Product
from cart.forms import CartAddProductForm


def page_not_found_view(request, exception):
    """page not found function
    """
    context = {}
    return render(request, 'frontend/404.html', context)


def accueil(request):
    """Home page function"""
    categories = Category.objects.all()
    stores = Store.objects.all()
    print('categories', categories)

    context = {
        'categories': categories,
        'stores': stores,
    }
    return render(request, 'frontend/home.html', context)


def listofstore(request):
    stores = Store.objects.all()
    print("stores", stores)
    context = {
        'stores': stores,
    }
    return render(request, 'frontend/store.html', context)


def productdetails(request, pk):
    otherproducts = None
    product = get_object_or_404(Product, pk=pk)
    if product is not None:
        otherproducts = Product.objects.filter(Q(store_id=product.store.id) & ~Q(id__in=[product.pk,]))
        print('otherproducts', otherproducts)

    cart_form = CartAddProductForm()

    context = {
        'product': product,
        'otherproducts': otherproducts,
        'cart_form': cart_form,

    }
    return render(request, 'frontend/detail-product.html', context)


def storedetails(request, pk):
    products = None
    store = get_object_or_404(Store, code=pk)
    if store is not None:
        products = Product.objects.filter(store=store)
        print('products', products)

    context = {
        'products': products,
        'store': store,
    }
    return render(request, 'frontend/detail-store.html', context)


def resetpassword(request):
    return render(request, 'frontend/forgot-password.html')


class StoreListView(AjaxListView):
    """Class for pagination of store list"""
    context_object_name = 'stores'
    template_name = 'frontend/store.html'
    page_template = 'frontend/store-list-ajax.html'

    def get_queryset(self):
        return Store.objects.all()
