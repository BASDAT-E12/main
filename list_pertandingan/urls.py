from django.urls import path
from list_pertandingan.views import *

app_name = 'list_pertandingan'

urlpatterns = [
<<<<<<< HEAD
    path('manajer/', list_pertandingan_manager, name='list_pertandingan_manager'),
    path('penonton/', list_pertandingan_penonton, name='list_pertandingan_penonton'),
=======
    path('penonton/', list_pertandingan_penonton, name='list_pertandingan_penonton'),
    path('manajer/', list_pertandingan_manager, name='list_pertandingan_manajer'),
>>>>>>> 3d8f74a49d196fa18e718fda8403587dd6921851
]