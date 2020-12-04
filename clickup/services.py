from .models import ClickUpUserId
from requests import request
from tiss_main.settings import CLICK_UP_CLIENT_ID, CLICK_UP_CLIENT_SECRET
from .clickup_api.models import Teams, AuthorizedUser, Tasks
from django.shortcuts import redirect


def click_up_authorize(code, user):
    req = request(method='POST', url='https://api.clickup.com/api/v2/oauth/token', params={
        'client_id': CLICK_UP_CLIENT_ID,
        'client_secret': CLICK_UP_CLIENT_SECRET,
        'code': code
    }).json()
    try:
        token = req['access_token']
        click_up_user = AuthorizedUser(user.click_up.auth_token)
    except (KeyError, ClickUpUserId.DoesNotExist):
        return False
    ClickUpUserId.objects.update_or_create(user=user, auth_token=token, click_up_user_id=click_up_user.id, team_id=None)
    return True


def deauthorize(username):
    ClickUpUserId.objects.get(user__username=username).delete()


def set_team_id(user, team_id):
    to_update = ClickUpUserId.objects.get(user=user)
    to_update.team_id = team_id
    to_update.save()


def get_teams(user):
    click_up_ids = ClickUpUserId.objects.get(user=user)
    teams = Teams(click_up_ids.auth_token)
    return teams


def get_tasks(user):
    return Tasks(token=user.click_up.auth_token, user_id=user.click_up.user_id)


def build_click_up_redirect(request):
    return redirect('https://app.clickup.com/api?client_id={client_id}&redirect_uri={redirect_uri}'
                    .format(client_id=CLICK_UP_CLIENT_ID,
                            redirect_uri=request.build_absolute_uri(location='/clickup/authorize')))
