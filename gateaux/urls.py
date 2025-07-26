# gateaux/urls.py

from django.urls import path  # type: ignore
from . import views

urlpatterns = [
    path('', views.liste_gateaux, name='liste_gateaux'),
    
    path('<int:gateau_id>/', views.detail_gateau, name='detail_gateau'),
    
    path('ajouter-au-panier/<int:gateau_id>/', views.ajouter_au_panier, name='ajouter_au_panier'),

    path('panier/', views.vue_panier, name='vue_panier'),
    path('recapitulatif-commande/', views.recapitulatif_commande, name='recapitulatif_commande'),
    path('retirer-du-panier/<int:gateau_id>/', views.retirer_du_panier, name='retirer_du_panier'),
]