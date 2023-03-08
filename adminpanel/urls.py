from django.urls import path

from adminpanel import views


app_name = 'adminpanel'

urlpatterns = [
    path('admin_dashboard', views.admin_dashboard, name='admin_dashboard'),
    path('requests_list', views.requests_list, name='requests_list'),
]