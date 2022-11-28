from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy

from frontend.forms import LoginForm


class LoginPageView(LoginView):
    template_name = 'registration/login.html'

    #form_class = AuthenticationForm
    form_class = LoginForm
    context_object_name = "context"
    #success_url = reverse_lazy('dashboard') #url from settings.LOGIN_REDIRECT_URL

    redirect_authenticated_user = True


    def dispatch(self, request, *args, **kwargs):

        '''if self.request.user.is_authenticated:
            # Redirect them to the home page if not
            return redirect('dashboard')'''


        return super().dispatch(request,*args, **kwargs)

