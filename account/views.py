from django.shortcuts import render
from django.contrib.auth import views as auth_view


# Create your views here.
class CustomLogin(auth_view.LoginView):
    template_name = 'pages/samples/login.html'
