from django.urls import path
from kelola_tim.views import *

app_name = 'kelola_tim'

urlpatterns = [
    path('', show_register_tim, name='show_register_tim'),
    path('list_tim/', show_list_tim, name='show_list_tim'),
    path('pilih_pelatih/', show_pilih_pelatih, name='show_pilih_pelatih'),
    path('pilih_pemain/', show_pilih_pemain, name='show_pilih_pemain'),
    path('manager_check_team/', manager_check_team, name='manager_check_team'),
    path('register_tim/', show_register_tim, name='register_tim'), 
    path('pilih_pemain_available/', pilih_pemain_available, name='pilih_pemain_available'),
    path('pilih_pelatih_available/', pilih_pelatih_available, name='pilih_pelatih_available'),
    path('daftar_pelatih/', daftar_pelatih, name='daftar_pelatih'),
    path('daftar_pemain/', daftar_pemain, name='daftar_pemain'), 
    path('delete_pelatih/<str:id>/', delete_pelatih, name='delete_pelatih'),
    path('delete_pemain/<str:id>/', delete_pemain, name='delete_pemain'),
    path('make_captain/<str:id>/', make_captain, name='make_captain'),
    path('create_tim/', create_tim, name='create_tim'),
]