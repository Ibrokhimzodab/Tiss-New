from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from .forms import UserRegistrationForm, UserEditForm, ProfileEditForm
from django.contrib.auth import views as auth_view
from .models import Profile
from django.contrib import messages
from django.views.defaults import page_not_found, server_error
from django.http import Http404, HttpResponse


# Create your views here.
@login_required
def dashboard(request):
    if request.user.is_superuser and request.user.is_staff:
        users = User.objects.filter(is_superuser=False)
        return render(request, 'admin_dashboard.html', {'users': users})
    return render(request, 'user_dashboard.html')


class CustomLogin(auth_view.LoginView):
    template_name = 'pages/samples/login.html'
    redirect_authenticated_user = True


class CustomLogout(auth_view.LogoutView):
    template_name = 'pages/samples/login.html'


class CustomPasswordResetView(auth_view.PasswordResetView):
    template_name = 'pages/samples/password_reset_form.html'


class CustomPasswordResetDoneView(auth_view.PasswordResetDoneView):
    template_name = 'pages/samples/password_reset_done.html'


class CustomPasswordResetConfirmView(auth_view.PasswordResetConfirmView):
    template_name = 'pages/samples/password_reset_confirm.html'


class CustomPasswordResetCompleteView(auth_view.PasswordResetCompleteView):
    template_name = 'pages/samples/password_reset_complete.html'


@login_required
def settings(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile, data=request.POST, files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            print(request.FILES)
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


def custom_404(request, exception=None):
    return page_not_found(request, exception, template_name='pages/samples/error-404.html')


def custom_500(request, exception=None):
    return server_error(request, exception, template_name='pages/samples/error-505.html')


@login_required()
def test(request):
    if request.method == 'POST':
        form = ProfileEditForm(instance=request.user.profile, data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            print(request.FILES)
            return HttpResponse('Done')
        else:
            return Http404
    else:
        form = ProfileEditForm()
        return render(request, 'test.html', {'form': form})
