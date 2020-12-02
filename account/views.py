from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import UserRegistrationForm, UserEditForm, ProfileEditForm
from django.contrib.auth import views as auth_view
from .models import Profile
from django.contrib import messages


# Create your views here.
@login_required
def dashboard(request):
    if request.user.is_superuser and request.user.is_staff:
        return render(request, 'admin_dashboard.html')
    return render(request, 'user_dashboard.html')


class CustomLogin(auth_view.LoginView):
    template_name = 'pages/samples/login.html'


class CustomLogout(auth_view.LogoutView):
    template_name = 'pages/samples/login.html'


class CustomPasswordResetView(auth_view.PasswordResetView):
    template_name = 'pages/samples/password_reset_form.html'


class CustomPasswordResetDoneView(auth_view.PasswordResetDoneView):
    template_name = 'pages/samples/password_reset_email.html'


class CustomPasswordResetConfirmView(auth_view.PasswordResetConfirmView):
    template_name = 'pages/samples/password_reset_form.html'


class CustomPasswordResetCompleteView(auth_view.PasswordResetCompleteView):
    template_name = 'pages/samples/password_reset_form.html'


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
    if request.user.is_superuser and request.user.is_staff:
        return render(request, 'pages/forms/admin_settings.html')
    return render(request, 'pages/forms/user_settings.html')


@login_required()
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
