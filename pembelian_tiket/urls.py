from django.urls import path
from pembelian_tiket.views import *

app_name = 'pembelian_tiket'

urlpatterns = [
    path('', pilih_stadium, name='pilih_stadium'),
    path('memilihwaktu/', list_waktu_stadium_tiket, name='list_waktu_stadium_tiket'),
    path('listpertandingan/', list_pertandingan_tiket, name='list_pertandingan_tiket'),
    path('belitiket/', beli_tiket, name='beli_tiket'),
]