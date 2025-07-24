# salles/admin.py

from django.contrib import admin # type: ignore
from .models import Salle  # 1. On importe le modèle "Salle" que nous avons créé dans models.py

# 2. On enregistre ce modèle pour qu'il soit gérable via l'interface d'administration.
admin.site.register(Salle)