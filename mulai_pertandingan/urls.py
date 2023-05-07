from django.urls import path
from mulai_pertandingan.views import *

app_name = 'mulai_pertandingan'

urlpatterns = [
    path('', start_match, name='start_match'),
    path('pilihperistiwa/', choose_episode, name='choose_episode'),
]