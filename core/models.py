# core/models.py
from django.db import models

class Service(models.Model):
    titre = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='photos_services/')
    ordre = models.IntegerField(default=0, help_text="Permet de trier les services (le plus petit en premier)")

    class Meta:
        ordering = ['ordre'] # Trie les services par le champ 'ordre'

    def __str__(self):
        return self.titre