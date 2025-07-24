# gateaux/urls.py
from django.urls import path # type: ignore
from . import views

urlpatterns = [
    path('', views.liste_gateaux, name='liste_gateaux'),
]