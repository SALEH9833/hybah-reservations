# reservations/models.py

from django.db import models # type: ignore
from django.conf import settings # type: ignore
from salles.models import Salle

class Reservation(models.Model):
    EN_ATTENTE = 'ATTENTE'
    CONFIRMEE = 'CONFIRMEE'
    ANNULEE = 'ANNULEE'
    
    STATUT_CHOICES = [
        (EN_ATTENTE, 'En attente'),
        (CONFIRMEE, 'Confirmée'),
        (ANNULEE, 'Annulée'),
    ]

    salle = models.ForeignKey(Salle, on_delete=models.CASCADE)
    utilisateur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    date_reservation = models.DateField()
    duree_heures = models.IntegerField()
    prix_total = models.DecimalField(max_digits=8, decimal_places=2)
    
    statut = models.CharField(
        max_length=10,
        choices=STATUT_CHOICES,
        default=EN_ATTENTE,
    )
    
    horodatage_creation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Réservation de {self.salle.nom} par {self.utilisateur.username} le {self.date_reservation}"