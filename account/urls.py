from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('login/', views.CustomLogin.as_view(), name='login'),
    path('logout/', views.CustomLogout.as_view(), name='logout'),
    path('', views.dashboard, name='dashboard'),
    path('settings/', views.settings, name='settings'),
    path('register/', views.register, name='register')
]
