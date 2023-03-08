from django.urls import path
from account import views


app_name = 'account'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('register_verify/', views.register_verify, name='register_verify'),
    path('user_dashboard/', views.user_dashboard, name='user_dashboard'),
    path('login/', views.login_, name='login'),
    path('login_verify/', views.login_verify, name='login_verify'),
    path('logout/', views.logout_, name='logout'),
]