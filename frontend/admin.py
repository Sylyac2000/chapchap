from django.contrib import admin
from django.contrib.admin.forms import AdminPasswordChangeForm

from frontend.models import Utilisateur
from frontend.forms import CustomUtilisateurChangeForm

class UtilisateurAdmin(admin.ModelAdmin):
    """model Utilisateur in django admin"""
    list_display = ['email', 'nom', 'prenom',  'telephone']
    list_filter = ['email', 'nom', 'prenom', 'telephone']
    list_editable = ['nom', 'prenom', 'telephone']

    # form = CustomUtilisateurChangeForm
    # change_password_form = AdminPasswordChangeForm

admin.site.register(Utilisateur, UtilisateurAdmin)