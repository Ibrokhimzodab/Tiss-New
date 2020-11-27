from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib.auth import views as auth_view


# Create your views here.
@login_required
def dashboard(request):
    return render(request, 'index.html')


class CustomLogin(auth_view.LoginView):
    template_name = 'pages/samples/login.html'


class CustomLogout(auth_view.LoginView):
    template_name = 'pages/samples/login.html'
