#!/usr/bin/env python3
"""This module is about : views.py
"""
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import OrderItem
from .forms import OrderCreateForm
# from .tasks import order_created
from cart.cart import Cart

# @login_required(login_url='/login/')
def order_create(request):
    """order creation"""
    cart = Cart(request)
    print('cart', len(cart))
    if len(cart) == 0:
        return redirect('frontend:stores')
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity'])
            # clear the cart
            cart.clear()
            # launch asynchronous task
            # order_created.delay(order.id)
            return render(request,
                          'orders/order-created.html',
                          {'order': order})
    else:
        form = OrderCreateForm()
    return render(request,
                  'orders/checkout.html',
                  {'cart': cart, 'form': form})

def order_created(request):
    # launch asynchronous task
    return render(request, 'orders/order-created.html')
