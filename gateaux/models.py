# gateaux/models.py
from django.db import models # type: ignore

class Gateau(models.Model):
    nom = models.CharField(max_length=100)
    description = models.TextField()
    prix = models.DecimalField(max_digits=6, decimal_places=2)
    
    # Ce champ permettra de lier une image plus tard
    photo = models.ImageField(upload_to='photos_gateaux/', null=True, blank=True)

    def __str__(self):
        return self.nom