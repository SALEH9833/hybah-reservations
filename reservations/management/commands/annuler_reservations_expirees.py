# reservations/management/commands/annuler_reservations_expirees.py

from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from reservations.models import Reservation

class Command(BaseCommand):
    # Message d'aide qui s'affiche si on tape 'python manage.py help annuler_reservations_expirees'
    help = "Annule les réservations 'En attente' créées depuis plus de 30 minutes."

    def handle(self, *args, **kwargs):
        # stdout.write est la bonne manière d'afficher du texte dans une commande
        self.stdout.write(f"[{timezone.now():%Y-%m-%d %H:%M}] Début du script d'annulation...")

        # 1. On calcule le moment exact "il y a 30 minutes"
        temps_limite = timezone.now() - timedelta(minutes=30)
        
        # 2. On trouve toutes les réservations à annuler :
        #    - Celles qui ont le statut "EN_ATTENTE"
        #    - ET dont l'horodatage de création est plus ancien que notre temps limite.
        reservations_a_annuler = Reservation.objects.filter(
            statut=Reservation.EN_ATTENTE,
            horodatage_creation__lt=temps_limite # __lt = "less than" (inférieur à)
        )
        
        # 3. On compte combien on en a trouvé
        nombre_a_annuler = reservations_a_annuler.count()

        if nombre_a_annuler > 0:
            # 4. On met à jour leur statut en "ANNULEE" en une seule requête
            reservations_a_annuler.update(statut=Reservation.ANNULEE)
            
            # On affiche un message de succès clair
            self.stdout.write(self.style.SUCCESS(f"{nombre_a_annuler} réservation(s) ont été automatiquement annulée(s)."))
        else:
            # S'il n'y en a aucune, on le dit aussi
            self.stdout.write(self.style.SUCCESS("Aucune réservation expirée à annuler."))

        self.stdout.write(f"[{timezone.now():%Y-%m-%d %H:%M}] Script terminé.")