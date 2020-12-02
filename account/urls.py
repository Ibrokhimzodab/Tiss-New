from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('login/', views.CustomLogin.as_view(), name='login'),
    path('logout/', views.CustomLogout.as_view(), name='logout'),
    path('', views.dashboard, name='dashboard'),
    path('settings/', views.settings, name='settings'),
    path('register/', views.register, name='register'),
    path('password_reset/', views.CustomPasswordResetView, name='password_reset'),
    path('password_reset/done', views.CustomPasswordResetDoneView, name='password_reset_done'),
    path('reset/<uidb64>/<token>/', views.CustomPasswordResetConfirmView, name='password_reset_confirm'),
    path('reset/done/', views.CustomPasswordResetConfirmView, name='password_reset_complete'),
]
