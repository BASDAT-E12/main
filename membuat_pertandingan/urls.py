from django.urls import path
from membuat_pertandingan.views import *

app_name = 'membuat_pertandingan'

urlpatterns = [
    path('', show_list_pertandingan, name='show_list_pertandingan'),
    path('memilihstadium/', choose_stadium, name='choose_stadium'),
    path('choose_time/<str:stadium_name>/', choose_time, name='choose_time'),
    path('membuatpertandingan/', create_match, name='create_match'),
    path('delete_pertandingan/<uuid:id_pertandingan>/', delete_pertandingan, name='delete_pertandingan'),
    path('submit_match/', submit_match, name='submit_match'),
    path('choose_date/', choose_date, name='choose_date'),
    path('update_choose_stadium/<id_pertandingan>/', update_choose_stadium, name='update_choose_stadium'),
    path('update_pertandingan/<uuid:id_pertandingan>/', update_pertandingan, name='update_pertandingan'),
    path('update_choose_date/<uuid:id_pertandingan>/', update_choose_date, name='update_choose_date'),
]
