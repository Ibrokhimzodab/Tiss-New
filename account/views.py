from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .forms import UserRegistrationForm
from django.contrib.auth import views as auth_view


# Create your views here.
@login_required
def dashboard(request):
    return render(request, 'index.html')


class CustomLogin(auth_view.LoginView):
    template_name = 'pages/samples/login.html'


class CustomLogout(auth_view.LogoutView):
    template_name = 'pages/samples/login.html'


@login_required
def settings(request):
    return render(request, 'pages/forms/settings.html')


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            return render(request, 'pages/samples/register.html', {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'pages/samples/register.html', {'user_form': user_form})
