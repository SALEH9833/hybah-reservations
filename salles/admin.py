# salles/admin.py

from django.contrib import admin # type: ignore
from .models import Salle 
admin.site.register(Salle)