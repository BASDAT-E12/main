from django.urls import path
from login_logout.views import *

app_name = ''

urlpatterns = [
    path('', login, name='login'),
    path('formlogin/', formlogin, name='formlogin'),
    path('login/', login, name='login'),
    path('authenticate/', authenticate, name='authenticate'),
    path('logout/', logout, name='logout')
]
