# core/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('politique/', views.page_statique_view, {'template_name': 'core/politique.html'}, name='politique'),
    path('conditions/', views.page_statique_view, {'template_name': 'core/conditions.html'}, name='conditions'),
    path('contact/', views.page_statique_view, {'template_name': 'core/contact.html'}, name='contact'),
]