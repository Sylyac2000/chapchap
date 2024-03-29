#!/usr/bin/python3
from decimal import Decimal
from django.conf import settings
from store.models import Product


class Cart:
    """Class to manage cart"""

    def __init__(self, request):
        """
        Initialize the cart.
        """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # save an empty cart in the session
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def __iter__(self):
        """Iterate over items in the cart and get the products from database
        """
        product_ids = self.cart.keys()
        # get products and add them to the cart
        products = Product.objects.filter(id__in=product_ids)
        cart = self.cart.copy()

        for product in products:
            cart[str(product.id)]['product'] = product
        # Le mot-clé yield à l'intérieur d'une fonction génératrice
        # est utilisé pour retourner une valeur de la fonction et mettre
        # en pause son exécution.

        for item in cart.values():
            item['price'] = int(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item # return and resume execution

    def add(self, product, quantity=1, override_quantity=False):
        """Add a product to the cart, or update its quantity and quantity
        """
        product_id = str(product.id)
        print('product_id', product_id)
        print('self.cart', self.cart)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0, 'price': str(product.price)}

        if override_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity

        self.save()
        print('self.cart', self.cart)

    def save(self):
        """Save the cart, by setting modified to True
        """
        self.session.modified = True

    def remove(self, product):
        """Remove a product from the cart.
        """
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.save()

    def __len__(self):
        """Counts the number of items in the cart
        """
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        return sum(int(item['price']) * item['quantity'] for item in self.cart.values())



