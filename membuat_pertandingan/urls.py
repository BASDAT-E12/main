from django.urls import path
from membuat_pertandingan.views import *

app_name = 'membuat_pertandingan'

urlpatterns = [
    path('', show_list_pertandingan, name='show_list_pertandingan'),
    path('memilihstadium/', choose_stadium, name='choose_stadium'),
    path('memilihwaktu/', choose_time, name='choose_time'),
    path('membuatpertandingan/', create_match, name='create_match'),
]