from django.urls import path
from membuat_pertandingan.views import *

app_name = 'mulai_pertandingan'

urlpatterns = [
    path('', show_list_pertandingan, name='show_list_pertandingan'),
]