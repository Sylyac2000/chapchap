"""controller actions, """
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

# Create your views here.
from frontend.models import Utilisateur


@login_required(login_url='/login')
def dashboard(request):
    """Show dashboard after a successful login"""

    utilisateur = Utilisateur.objects.get(email=request.user.email)
    context = {
        'request': request
    }
    return render(request, 'myaccount/dashboard.html', context)
