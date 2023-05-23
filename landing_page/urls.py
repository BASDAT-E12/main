from django.urls import path
from landing_page.views import *

app_name = 'landing_page'

urlpatterns = [
    path('manajer/', show_landing_page_manajer, name='show_landing_page_manajer'),
    path('penonton/', show_landing_page_penonton, name='show_landing_page_penonton'),
    path('panitia/', show_landing_page_panitia, name='show_landing_page_panitia'),
    path('', get_role, name='index'),
    path('back_landing_page_manajer/', back_landing_page_manajer, name='back_landing_page_manajer')
]