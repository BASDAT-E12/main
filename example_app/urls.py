from django.urls import path
from login_logout.views import index

app_name = 'example_app'

urlpatterns = [
    path('', index, name='index'),
]