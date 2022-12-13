#!/usr/bin/env python

""" Store creation Form"""
from django.utils.safestring import mark_safe
from django import forms
from django.forms import ModelForm
from django_summernote.widgets import SummernoteWidget

from store.models import Store, Product, Category


class ProductForm(ModelForm):

    class Meta:
        model = Product

        fields = ('name', 'description',  'category', 'store', 'price', 'productimage')

        labels = {
            "name": mark_safe('Name<span class="text-danger">*</span>'),
            "description": mark_safe('Description<span class="text-danger">*</span>'),
            "category": mark_safe('Category<span class="text-danger">*</span>'),
            "store": mark_safe('Store<span class="text-danger">*</span>'),
            "price": mark_safe('Price<span class="text-danger">*</span>'),
            "photo": mark_safe('Photo<span class="text-danger">*</span>'),
        }

        widgets = {
            "name": forms.TextInput(attrs={'class': 'form-control'}),
            "description": SummernoteWidget(attrs={'class': 'form-control'}),
            "category": forms.Select(attrs={'class': 'form-control'}),
            "store": forms.Select(attrs={'class': 'form-control'}),
            "price": forms.TextInput(attrs={'class': 'form-control'}),
            "photo": forms.FileInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, user, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        self.request = kwargs.pop('request', None)
        self.user = user
        print("Proprio", user)

        self.fields['store'].queryset = Store.objects.filter(proprietary=self.user)
        self.fields['category'].queryset = Category.objects.all()

        print("store", self.fields['store'].queryset)




class StoreForm(ModelForm):
    class Meta:
        model = Store

        fields = ("name", "phone", "description", "photo")

        labels = {
            "name": mark_safe('Name<span class="text-danger">*</span>'),
            "phone": mark_safe('Phone<span class="text-danger">*</span>'),
            "description": mark_safe('Description<span class="text-danger">*</span>'),
            "photo": mark_safe('Photo<span class="text-danger">*</span>'),
        }

        widgets = {
            "name": forms.TextInput(attrs={'class': 'form-control'}),
            "phone": forms.TextInput(attrs={'class': 'form-control'}),
            "description": SummernoteWidget(attrs={'class': 'form-control'}),
            "photo": forms.FileInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, user, *args, **kwargs):
        super(StoreForm, self).__init__(*args, **kwargs)
        self.request = kwargs.pop('request', None)
        self.user = user

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if not phone:
            raise forms.ValidationError('Ce champ est requis')
        else:
            if not phone.isdigit():
                raise forms.ValidationError('Phone must be digits')

        return phone

    def clean_name(self):
        name = self.cleaned_data['name']
        if not name:
            raise forms.ValidationError('Ce champ est requis')
        return name

    def clean_photo(self):
        photo = self.cleaned_data['photo']
        if not photo:
            raise forms.ValidationError('Ce champ est requis')
        return photo
