from django.urls import path
from . import views
from django.views.defaults import page_not_found

app_name = 'clickup'
urlpatterns = [
    path('authorize/', views.click_up_link, name='click_up_link'),
    path('authorize', views.click_up_link, name='click_up_link2'),
    path('link-team/', views.choose_team, name='choose_team'),
    # path('test/', views.test_view, name='test'),
    path('tasks/', views.tasks_list, name='tasks')
]
