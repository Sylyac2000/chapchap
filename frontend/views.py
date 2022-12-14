""" frontend view
"""


from django.shortcuts import render, get_object_or_404

# Create your views here.
from store.models import Category, Store, Product


def page_not_found_view(request, exception):
    context = {}
    return render(request, 'frontend/404.html', context)


def accueil(request):
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
    product = get_object_or_404(Product, code=pk)
    if product is not None:
        otherproducts = Product.objects.filter(store=product.store)
        print('otherproducts', otherproducts)


    context = {
        'product': product,
        'otherproducts': otherproducts,

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
