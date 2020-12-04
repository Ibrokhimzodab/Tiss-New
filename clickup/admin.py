from django.contrib import admin
from .models import ClickUpUserId


@admin.register(ClickUpUserId)
class ClickUpIdAdmin(admin.ModelAdmin):
    list_display = ('user', 'auth_token')
