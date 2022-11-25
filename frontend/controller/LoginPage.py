from django.contrib.auth.views import LoginView

from frontend.forms import LoginForm


class LoginPageView(LoginView):
    template_name = 'registration/login.html'

    #form_class = AuthenticationForm
    form_class = LoginForm
    context_object_name = "context"
    #success_url = reverse_lazy('dashboard') #url from settings.LOGIN_REDIRECT_URL

    redirect_authenticated_user = True