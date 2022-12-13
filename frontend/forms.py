"""Forms in frontend app """
from django import forms
from django.contrib.auth.forms import AuthenticationForm, UsernameField, UserCreationForm
from django.core.validators import validate_email
from django.utils.safestring import mark_safe

from frontend.models import Utilisateur

"""
class ResetPasswordForm(AuthenticationForm):

"""

class LoginForm(AuthenticationForm):

    username = UsernameField(widget=forms.TextInput(attrs={'autofocus': True}))
    password = forms.CharField(
        label="Mot de passe",
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password'}),
    )

    class Meta:
        model = Utilisateur
        fields = (
            'email',
            'password',
        )

    error_messages = {}

    def clean_email(self):
        username = self.cleaned_data['email']
        if username is None:
            raise forms.ValidationError(f"Username {username} est requis")
        try:
            username = validate_email(username)
        except:
            raise forms.ValidationError(f"{username} n'est pas un email valide")


        return username

    def clean_password(self):
        password = self.cleaned_data['password']
        if len(password) < 8 :
            raise forms.ValidationError(f"Au moins 8 caractères pour le mot de passe")
        return password

    def get_invalid_login_error(self):
        raise forms.ValidationError("Login et/ou mot de passe incorrecte")



class SignupForm(UserCreationForm):
    password1 = forms.CharField(max_length=200, label=mark_safe('Password<span class="text-danger">*</span>'),
                                widget=forms.PasswordInput(
                                    attrs={'class': 'form-control', 'placeholder': 'Password'}))
    password2 = forms.CharField(max_length=200,
                                label=mark_safe('Password confirmation<span class="text-danger">*</span>'),
                                widget=forms.PasswordInput(
                                    attrs={'class': 'form-control', 'placeholder': 'Password confirmation'}))


    class Meta:
        model = Utilisateur
        fields = ('nom', 'prenom','telephone','email','password1','password2')
        widgets = {
            "nom": forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
            "prenom": forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last name'}),
            "telephone": forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone'}),
            "email": forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),

        }
        labels = {
            "nom": mark_safe('First name<span class="text-danger">*</span>'),
            "prenom": mark_safe('Lastname<span class="text-danger">*</span>'),
            "telephone": mark_safe('Phone<span class="text-danger">*</span>'),
            "email": mark_safe('Email<span class="text-danger">*</span>'),
        }

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                "Les mots de passes ne sont pas égaux"
            )
        return password2

    def clean_username(self):
        username = self.cleaned_data['username']
        isuserexist = Utilisateur.objects.filter(username=username).exists()

        if isuserexist:
            raise forms.ValidationError(f"Username {username} est déja utilisé")

        return username
