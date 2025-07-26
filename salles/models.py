# salles/models.py
from django.db import models # type: ignore

class Salle(models.Model):
    # Constantes pour les choix de catégorie
    HOMMES = 'H'
    FEMMES = 'F'
    CATEGORIE_CHOICES = [
        (HOMMES, 'Salle pour Hommes'),
        (FEMMES, 'Salle pour Femmes'),
    ]

    nom = models.CharField(max_length=100)
    description = models.TextField()
    capacite = models.IntegerField()
    
    categorie = models.CharField(
        max_length=1,
        choices=CATEGORIE_CHOICES,
    )
    
    prix_par_heure = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        # Cette fonction est très utile pour que le nom de la salle s'affiche clairement dans l'admin
        return self.nom
