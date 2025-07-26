# gateaux/views.py

from django.shortcuts import render, get_object_or_404, redirect  # type: ignore
from django.db import transaction # type: ignore
from .models import Gateau
from django.http import JsonResponse # type: ignore
from reservations.models import Reservation
from django.contrib import messages  # type: ignore
def liste_gateaux(request):
    tous_les_gateaux = Gateau.objects.all()
    context = { 'gateaux': tous_les_gateaux,
               'show_panier': True,}
    return render(request, 'gateaux/liste_gateaux.html', context)

def detail_gateau(request, gateau_id):
    gateau = get_object_or_404(Gateau, pk=gateau_id)
    context = { 'gateau': gateau,
               'show_panier': True,}
    return render(request, 'gateaux/detail_gateau.html', context)

def ajouter_au_panier(request, gateau_id):
    if request.method == 'POST':
        panier = request.session.get('panier', {})
        gateau_id_str = str(gateau_id)
        panier[gateau_id_str] = panier.get(gateau_id_str, 0) + 1
        request.session['panier'] = panier
        return JsonResponse({'status': 'succes', 'message': 'Gâteau ajouté au panier !'})
    return redirect('liste_gateaux')

def vue_panier(request):
    panier = request.session.get('panier', {})
    gateaux_ids = panier.keys()
    gateaux_objets = Gateau.objects.filter(id__in=gateaux_ids)
    items_panier = []
    total_prix = 0
    total_items = 0
    for gateau in gateaux_objets:
        quantite = panier.get(str(gateau.id), 0)
        prix_total_item = gateau.prix * quantite
        items_panier.append({
            'id': gateau.id, 'nom': gateau.nom, 'quantite': quantite,
            'prix_unitaire': float(gateau.prix), 'prix_total': float(prix_total_item),
        })
        total_prix += prix_total_item
        total_items += quantite
    return JsonResponse({
        'items': items_panier, 'total_prix': float(total_prix), 'total_items': total_items,
    })

def recapitulatif_commande(request):
    if not request.user.is_authenticated:
        return redirect('connexion')

    panier = request.session.get('panier', {})
    gateaux_ids = panier.keys()
    gateaux_objets = Gateau.objects.filter(id__in=gateaux_ids)
    
    items_panier = []
    total_prix = 0
    for gateau in gateaux_objets:
        quantite = panier.get(str(gateau.id), 0)
        if quantite > 0:
            prix_total_item = gateau.prix * quantite
            items_panier.append({
                'gateau_id': gateau.id, 'nom': gateau.nom, 'quantite': quantite,
                'prix_unitaire': float(gateau.prix), 'prix_total': float(prix_total_item),
                'photo_url': gateau.photo.url if gateau.photo else ''
            })
            total_prix += prix_total_item
    
    if request.method == 'POST':
        if not items_panier:
            return redirect('liste_gateaux')
        try:
            with transaction.atomic():
                Reservation.objects.create(
                    utilisateur=request.user,
                    type_reservation=Reservation.TYPE_GATEAU,
                    gateau_details=items_panier,
                    prix_total=total_prix,
                    statut=Reservation.EN_ATTENTE,
                )
                request.session['panier'] = {}
                request.session.modified = True
                
            messages.success(request, "Votre commande de gâteau a bien été enregistrée !") # type: ignore
            return redirect('liste_gateaux')

        except Exception as e:
            messages.error(request, f"Une erreur est survenue: {e}") # type: ignore
            context = {
                'items': items_panier, 'total_prix': total_prix,
                'error_message': 'Une erreur est survenue lors de la confirmation.'
            }
            return render(request, 'gateaux/recapitulatif_commande.html', context)

    context = {
        'items': items_panier, 'total_prix': total_prix,'show_panier': True,
        'total_items': sum(item['quantite'] for item in items_panier),
    }
    return render(request, 'gateaux/recapitulatif_commande.html', context)
def retirer_du_panier(request, gateau_id):
    if request.method == 'POST':
        panier = request.session.get('panier', {})
        gateau_id_str = str(gateau_id)

        if gateau_id_str in panier:
            if panier[gateau_id_str] > 1:
                panier[gateau_id_str] -= 1
            
            else:
                del panier[gateau_id_str]

            request.session['panier'] = panier
            request.session.modified = True
            return JsonResponse({'status': 'succes', 'message': 'Article mis à jour.'})

    return redirect('liste_gateaux')