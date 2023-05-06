from django.urls import path
from kelola_tim.views import *

app_name = 'kelola_tim'

urlpatterns = [
    path('', show_register_tim, name='show_register_tim'),
    path('list_tim/', show_list_tim, name='show_list_tim'),
    path('pilih_pelatih/', show_pilih_pelatih, name='show_pilih_pelatih'),
    path('pilih_pemain/', show_pilih_pemain, name='show_pilih_pemain'),
]