from django.urls import path

from chat import views


app_name = 'chat'

urlpatterns = [
    path('room/<int:room_id>/', views.room_view, name='room'),
    path('room_create/<int:relation_id>/', views.room_create_view, name='room_create')
]