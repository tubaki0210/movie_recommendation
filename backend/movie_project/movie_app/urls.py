from django.urls import path
from . import main_system

urlpatterns = [
    path('', main_system.SystemUtt.as_view(), name='index'),
]