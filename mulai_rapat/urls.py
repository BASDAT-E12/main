from django.urls import path
from mulai_rapat.views import *

app_name = 'mulai_rapat'

urlpatterns = [
    path('', choose_match, name='choose_match'),
    path('rapat/', meeting, name='meeting'),
]