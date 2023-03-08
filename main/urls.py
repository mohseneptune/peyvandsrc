from django.urls import path
from django.views.generic import RedirectView
from main import views


app_name = 'main'

urlpatterns = [
    path('', RedirectView.as_view(pattern_name='main:home')),
    path('home/', views.home, name='home'),
]