# reservations/models.py

from django.db import models # type: ignore
from django.conf import settings # type: ignore
from salles.models import Salle
from gateaux.models import Gateau
import json

class Reservation(models.Model):
    EN_ATTENTE = 'ATTENTE'
    CONFIRMEE = 'CONFIRMEE'
    ANNULEE = 'ANNULEE'
    STATUT_CHOICES = [
        (EN_ATTENTE, 'En attente'),
        (CONFIRMEE, 'Confirmée'),
        (ANNULEE, 'Annulée'),
    ]

    TYPE_SALLE = 'SALLE'
    TYPE_GATEAU = 'GATEAU'
    TYPE_CHOICES = [
        (TYPE_SALLE, 'Réservation de Salle'),
        (TYPE_GATEAU, 'Commande de Gâteau'),
    ]

    salle = models.ForeignKey(Salle, on_delete=models.SET_NULL, null=True, blank=True)
    type_reservation = models.CharField(max_length=10, choices=TYPE_CHOICES, default=TYPE_SALLE)
    gateau_details = models.JSONField(null=True, blank=True)
    utilisateur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_reservation = models.DateField(null=True, blank=True)
    heure_debut = models.TimeField(null=True, blank=True)
    duree_heures = models.IntegerField(default=0)
    prix_total = models.DecimalField(max_digits=8, decimal_places=2)
    statut = models.CharField(max_length=10, choices=STATUT_CHOICES, default=EN_ATTENTE)
    horodatage_creation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.type_reservation == self.TYPE_SALLE and self.salle:
            return f"Réservation Salle: {self.salle.nom} par {self.utilisateur.username} le {self.date_reservation}"
        elif self.type_reservation == self.TYPE_GATEAU and self.gateau_details:
            try:
                noms_gateaux = ", ".join([item['nom'] for item in self.gateau_details])
                return f"Commande Gâteau: {noms_gateaux} par {self.utilisateur.username}"
            except (TypeError, KeyError):
                return f"Commande Gâteau #{self.id} par {self.utilisateur.username}"
        return f"Réservation #{self.id} par {self.utilisateur.username}"