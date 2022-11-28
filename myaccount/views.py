"""controller actions, """
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

# Create your views here.
@login_required(login_url='/login')
def dashboard(request):
    """Show dashboard after a successful login"""

    return render(request, 'myaccount/dashboard.html')
