from django.db import models

# Create your models here.
# menu/models.py
from django.db import models

class Produit(models.Model):
    CATEGORIE_CHOICES = [
        ('BOISSON_CHAUDE', 'Boissons chaudes'),
        ('BOISSON_FROIDE', 'Boissons froides'),
        ('PATISSERIE', 'Pâtisseries'),
        ('SALE', 'Plats salés'),
        ('AUTRE', 'Autres'),
    ]

    nom = models.CharField(max_length=100)
    description = models.TextField()
    prix = models.DecimalField(max_digits=6, decimal_places=2)
    photo = models.ImageField(upload_to='photos_produits/')
    categorie = models.CharField(max_length=20, choices=CATEGORIE_CHOICES)

    class Meta:
        verbose_name = "produit du menu"
        verbose_name_plural = "produits du menu"

    def __str__(self):
        return self.nom