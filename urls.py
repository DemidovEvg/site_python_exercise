from django.urls import path
from .views import *

app_name = 'test_app'

urlpatterns = [
    path('',
         test_view,
         name='home'),
]
