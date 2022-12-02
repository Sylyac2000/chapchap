""" Store creation Form"""
from django.utils.safestring import mark_safe
from django import forms
from django.forms import ModelForm

from store.models import Store


class StoreForm(ModelForm):
    class Meta:
        model = Store

        fields = ("name", "photo")

        labels = {
            "name": mark_safe('Name<span class="text-danger">*</span>'),
            "photo": mark_safe('Photo<span class="text-danger">*</span>'),
        }

        widgets = {
            "name": forms.TextInput(attrs={'class': 'form-control'}),
            "photo": forms.FileInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, user, *args, **kwargs):
        super(StoreForm, self).__init__(*args, **kwargs)
        self.request = kwargs.pop('request', None)
        self.user = user

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
