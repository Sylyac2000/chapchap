#!/usr/bin/env python3
"""This module is about : forms.py
"""
from django import forms
from .models import Order


class OrderCreateForm(forms.ModelForm):

    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'phone', 'email', 'address', 'city']

    def clean_first_name(self):
        """validate first_name"""
        first_name = self.cleaned_data['first_name']
        if not first_name:
            raise forms.ValidationError('This field is required.')

        return first_name

    def clean_last_name(self):
        """validate last_name"""
        last_name = self.cleaned_data['last_name']
        if not last_name:
            raise forms.ValidationError('This field is required.')

        return last_name

    def clean_phone(self):
        """validate phone"""
        phone = self.cleaned_data['phone']
        if not phone:
            raise forms.ValidationError('This field is required.')
        else:
            if not phone.isdigit():
                raise forms.ValidationError('Phone must be digits')

        return phone
