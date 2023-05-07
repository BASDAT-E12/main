from django.urls import path
from manage_pertandingan.views import *

app_name = 'manage_pertandingan'

urlpatterns = [
    path('', grupstageabis, name='grupstageabis'),
    path('listpertandingan_update/', listpertandingan_update, name='listpertandingan_update'),
    path('listpertandingan/', listpertandingan, name='listpertandingan'),
    path('next_belumlengkap/', next_belumlengkap, name='next_belumlengkap'),
    path('next_pertandinganbaru/', next_pertandinganbaru, name='next_pertandinganbaru'),
    path('peristiwatim/', peristiwatim, name='peristiwatim'),
]