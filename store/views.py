#!/usr/bin/env python
"""views function and class to manage store and is contents(products)
"""
import base64
import io
from io import BytesIO

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect, get_object_or_404
from django.template.loader import get_template

from django.urls import reverse
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView

from chapchap import settings
from frontend.models import Utilisateur
from store.forms import StoreForm, ProductForm
from store.models import Store, Product
from django.views.generic import View
from django.http import HttpResponse
from xhtml2pdf import pisa
import qrcode


class StoreListView(LoginRequiredMixin, ListView):
    template_name = 'store/list-store.html'
    # queryset = Store.objects.all()
    model = Store

    # context_object_name = 'stores'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        utilisateur = Utilisateur.objects.get(email=self.request.user.email)

        if (self.request.user.is_authenticated and utilisateur.is_admin):
            stores = Store.objects.all()

        else:
            stores = Store.objects.filter(proprietary=utilisateur)
            # stores = Store.objects.all()

        print('utilisateur', utilisateur.id)
        print('store', stores)
        context['stores'] = stores
        return context


from django.views.generic import View
from django.shortcuts import render
import qrcode


class QRcodeView(View):
    def get(self, request, *args, **kwargs):
        # Generate the QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data('This is the data for the QR code')
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")

        # Create an in-memory buffer containing the image data
        buffer = io.BytesIO()
        img.save(buffer, format='PNG')
        buffer.seek(0)

        base64_image = base64.b64encode(buffer.read()).decode('utf-8')

        print(base64_image)

        # Render the template and pass the image data to the template
        return render(request, 'store/mytemplateqrcode.html', {'base64_image': base64_image})


class MyView(View):
    def get(self, request, *args, **kwargs):
        # Generate the QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data('This is the data for the QR code')
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")

        # Create an HttpResponse and set the appropriate headers
        response = HttpResponse(content_type='image/png')
        response['Content-Disposition'] = 'inline; filename=qrcode.png'

        # Write the QR code image to the response
        img.save(response, 'PNG')
        return response


class MyViewPdf(View):
    def get(self, request, *args, **kwargs):
        """Render qrcode"""
        template = get_template('store/mytemplate.html')
        code = kwargs.get('code')
        print('kwargs', str(code))
        store = None
        if str(code):
            store = get_object_or_404(Store, code=code)
        else:
            return HttpResponse('Error generating PDF, no valid store code', status=400)
        # from settings.py, BASE_URL is configured
        BASE_URL = settings.BASE_URL

        store_relative_url = store.get_absolute_url()
        store_absolute_url = BASE_URL + reverse('frontend:detail-store', args=[code])


        # print(store_relative_url, store_absolute_url)

        # Generate the QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=20,
            border=4,
        )
        qr.add_data(store_absolute_url)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")

        # Create an in-memory buffer containing the image data
        buffer = io.BytesIO()
        img.save(buffer, format='PNG')
        buffer.seek(0)

        base64_image = base64.b64encode(buffer.read()).decode('utf-8')

        context = {
            'data': store_absolute_url,
            'base64_image': base64_image
        }
        html = template.render(context)

        # Create a PDF from the HTML
        result = BytesIO()
        pdf = pisa.pisaDocument(BytesIO(html.encode('UTF-8')), result)
        if not pdf.err:
            response = HttpResponse(result.getvalue(), content_type='application/pdf')
            # response['Content-Disposition'] = 'attachment; filename=mypdf.pdf' # is download
            response['Content-Disposition'] = 'inline; filename=qrcode.pdf'
            return response
        return HttpResponse('Error generating PDF', status=400)


class StoreListQrcodeView(LoginRequiredMixin, ListView):
    template_name = 'store/list-store-qrcode.html'
    # queryset = Store.objects.all()
    model = Store

    # context_object_name = 'stores'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        utilisateur = Utilisateur.objects.get(email=self.request.user.email)

        if (self.request.user.is_authenticated and utilisateur.is_admin):
            stores = Store.objects.all()

        else:
            stores = Store.objects.filter(proprietary=utilisateur)
            # stores = Store.objects.all()

        print('utilisateur', utilisateur.id)
        print('store', stores)
        context['stores'] = stores
        return context


class StoreCreateView(LoginRequiredMixin, CreateView, SuccessMessageMixin):
    """Class based view to create a store"""
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


class StoreUpdateView(LoginRequiredMixin, UpdateView, SuccessMessageMixin):
    """Class based view to update a store"""
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
        # objStore.proprietary = Utilisateur.objects.get(email=self.request.user.email)
        objStore.save()

        return super(StoreUpdateView, self).form_valid(form)


class StoreDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    """Class based view to delete a store"""
    model = Store
    template_name = "store/delete-store.html"
    context_object_name = "store"

    success_message = "Store deleted successfully."

    def get_success_url(self):
        return reverse("store:list-store")


class StoreDetailsView(LoginRequiredMixin, DetailView):
    template_name = 'store/detail-store.html'
    model = Store
    context_object_name = 'store'


class ProductListView(LoginRequiredMixin, ListView):
    template_name = 'product/list-product.html'
    # queryset = Store.objects.all()
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


class ProductCreateView(LoginRequiredMixin, CreateView):
    template_name = 'product/add-product.html'
    # queryset = Store.objects.all()
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


class ProductUpdateView(LoginRequiredMixin, UpdateView, SuccessMessageMixin):
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
        # objStore.proprietary = Utilisateur.objects.get(email=self.request.user.email)
        objStore.save()

        return super(ProductUpdateView, self).form_valid(form)


class ProductDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Product
    template_name = "product/delete-product.html"
    context_object_name = "product"

    success_message = "Product deleted successfully."

    def get_success_url(self):
        return reverse("store:list-product")
