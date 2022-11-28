"""Forms in frontend app """
from django import forms
from django.contrib.auth.forms import AuthenticationForm, UsernameField
from django.core.validators import validate_email

from frontend.models import Utilisateur


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



class SignupForm(forms.Form):
    pass
