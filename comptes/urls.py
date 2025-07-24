# comptes/urls.py (version finale et correcte)
from django.urls import path # type: ignore
from django.contrib.auth import views as auth_views # type: ignore
from . import views # <-- CET IMPORT EST CORRECT ICI !

urlpatterns = [
    # Le chemin pour la page d'inscription
    path('inscription/', views.InscriptionView.as_view(), name='inscription'),

    # Le chemin pour la page de connexion
    path('connexion/', views.page_connexion_personnalisee, name='connexion'),

    # Le chemin pour la déconnexion
    path('deconnexion/', auth_views.LogoutView.as_view(), name='deconnexion'),
]