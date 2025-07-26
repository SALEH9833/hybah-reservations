# reservations/management/commands/annuler_reservations.py

from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from reservations.models import Reservation

class Command(BaseCommand):
    help = "Annule les réservations 'En attente' depuis plus de 30 minutes."

    def handle(self, *args, **kwargs):
        # self.stdout.write est la bonne façon d'afficher du texte dans une commande
        self.stdout.write(self.style.NOTICE("Début du script d'annulation..."))

        # 1. Calculer le moment "il y a 30 minutes"
        temps_limite = timezone.now() - timedelta(minutes=30)
        
        # 2. Trouver toutes les réservations à annuler
        # On cherche les réservations qui sont 'EN_ATTENTE' ET dont la date de création
        # est PLUS ANCIENNE que notre temps limite.
        reservations_a_annuler = Reservation.objects.filter(
            statut=Reservation.EN_ATTENTE,
            horodatage_creation__lt=temps_limite # __lt signifie "less than" (inférieur à)
        )
        
        # 3. Compter combien on en a trouvé
        nombre_reservations = reservations_a_annuler.count()

        if nombre_reservations > 0:
            # 4. On les met toutes à jour d'un seul coup (c'est plus efficace)
            reservations_a_annuler.update(statut=Reservation.ANNULEE)
            self.stdout.write(self.style.SUCCESS(f"{nombre_reservations} réservation(s) ont été annulée(s)."))
        else:
            self.stdout.write(self.style.SUCCESS("Aucune réservation à annuler."))

        self.stdout.write(self.style.NOTICE("Script d'annulation terminé."))