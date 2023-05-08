from django.urls import path
from pengguna.views import *

app_name = 'pengguna'

urlpatterns = [
    path('', register, name='register'),
    path('register_manager_penonton/', register_manager_penonton, name='register_manager_penonton'),
    path('register_panitia/', register_panitia, name='register_panitia'),
]