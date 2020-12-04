from django.db import models
from django.contrib.auth.models import User


class ClickUpUserId(models.Model):
    user = models.OneToOneField(User, related_name='click_up', on_delete=models.CASCADE)
    auth_token = models.CharField(verbose_name='Authorization token', max_length=64, blank=True)
    click_up_user_id = models.CharField(verbose_name='ClickUp User unique id', null=True, blank=True, max_length=64)
    team_id = models.CharField(verbose_name='ClickUp Team unique id', null=True, blank=True, max_length=64)

    class Meta:
        db_table = 'clickup_user_ids'
