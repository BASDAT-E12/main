from django.urls import path
from cru_peminjaman_stadium.views import *

app_name = 'cru_peminjaman_stadium'

urlpatterns = [
    path('', listpemesanan, name='listpemesanan'),
    path('listwaktustadium/', listwaktustadium, name='listwaktustadium'),
    path('peminjamanstadium/', peminjamanstadium, name='peminjamanstadium'),
]