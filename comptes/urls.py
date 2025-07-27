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
      path('historique/', views.historique_reservations, name='historique'),
       path('password_reset/', auth_views.PasswordResetView.as_view(template_name='comptes/password_reset.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='comptes/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='comptes/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='comptes/password_reset_complete.html'), name='password_reset_complete'),
    path('historique/supprimer/<int:reservation_id>/', views.supprimer_reservation, name='supprimer_reservation'),
]