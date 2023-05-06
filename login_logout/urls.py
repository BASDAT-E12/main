from django.urls import path
from login_logout.views import *

app_name = 'login_logout'

urlpatterns = [
    path('', login, name='login'),
    path('formlogin/', formlogin, name='formlogin'),
    path('login/', login, name='login'),
]