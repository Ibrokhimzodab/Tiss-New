from django.shortcuts import render, redirect
from . import services
from django.contrib.auth.decorators import login_required
from .models import ClickUpUserId
from clickup.clickup_api.errors import ApiRequestError, TeamNotAuthorized, AuthTokenError
from .clickup_api.models import Tasks


@login_required
def click_up_link(request):
    if 'code' in request.GET:
        user = request.user
        auth_succeed = services.click_up_authorize(user=user, code=request.GET['code'])
        if auth_succeed:
            return redirect('clickup:choose_team')
    return services.build_click_up_redirect(request)


@login_required
def choose_team(request):
    user = request.user
    if request.method == 'POST' and request.POST['team_id']:
        try:
            services.set_team_id(user, team_id=request.POST['team_id'])
            redirect(request, '')
        except ClickUpUserId.DoesNotExist:
            return redirect('clickup:click_up_link')
    else:
        try:
            teams = services.get_teams(user)
            return render(request, '', {'teams': teams})
        except (ClickUpUserId.DoesNotExist, ApiRequestError, AuthTokenError):
            return services.build_click_up_redirect(request)


@login_required
def tasks_list(request):
    user = request.user
    try:
        tasks = services.get_tasks(user)
        return render(request, '', {'tasks': tasks})
    except TeamNotAuthorized:
        return redirect('clickup:choose_team')
    except (AuthTokenError, ApiRequestError, ClickUpUserId.DoesNotExist):
        return services.build_click_up_redirect(request)


@login_required
def click_up_unlink(request):
    try:
        services.deauthorize(request.user.username)
        return render(request, '')
    except ClickUpUserId.DoesNotExist:
        return render(request, '')
