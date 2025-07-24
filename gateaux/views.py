# gateaux/views.py
from django.shortcuts import render # type: ignore
from .models import Gateau

def liste_gateaux(request):
    tous_les_gateaux = Gateau.objects.all()
    context = {
        'gateaux': tous_les_gateaux,
    }
    return render(request, 'gateaux/liste_gateaux.html', context)