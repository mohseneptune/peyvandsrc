from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls', namespace='main')),
    path('', include('account.urls', namespace='account')),
    path('', include('adminpanel.urls', namespace='adminpanel')),
    path('', include('chat.urls', namespace='chat')),
]
