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
    path('profile/', views.profile, name='profile'),
    path('profile_change/', views.profile_change, name='profile_change'),
    path('phone_change/', views.phone_change, name='phone_change'),
    path('phone_change_verify/', views.phone_change_verify, name='phone_change_verify'),
    path('khosousiaat_change/', views.khosousiaat_change, name='khosousiaat_change'),
    path('entezaaraat_change/', views.entezaaraat_change, name='entezaaraat_change'),
    path('partner_search/', views.partner_search, name='partner_search'),
    path('user_detail/<int:pk>/', views.user_detail, name='user_detail'),

    path("relation_request/<int:sender>/<int:reciver>/<str:action>/", views.relation_request, name="rr"),
    path("sending_requests/", views.sending_requests, name="sending_requests"),
    path("reciving_requests/", views.reciving_requests, name="reciving_requests"),
]