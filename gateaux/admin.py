# gateaux/admin.py
from django.contrib import admin # type: ignore
from .models import Gateau

admin.site.register(Gateau)