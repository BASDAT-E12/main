from django.urls import path
from pengguna.views import *

app_name = 'pengguna'

urlpatterns = [
    path('', register, name='register'),
    path('register_manager/', register_manager, name='register_manager'),
    path('register_penonton/', register_penonton, name='register_penonton'),
    path('register_panitia/', register_panitia, name='register_panitia'),
    path('register_roles/', register_all_roles, name ='register_all_roles')
]