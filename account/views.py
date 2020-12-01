from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import UserRegistrationForm, UserEditForm, ProfileEditForm
from django.contrib.auth import views as auth_view
from .models import Profile
from django.contrib import messages


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
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile, data=request.POST, files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated successfully')
        else:
            messages.error(request, 'Error updating profile')
    return render(request, 'pages/forms/settings.html')


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            Profile.objects.create(user=new_user)
            new_user.save()
            return redirect('dashboard')
    else:
        user_form = UserRegistrationForm()
    return render(request, 'pages/samples/register.html')
