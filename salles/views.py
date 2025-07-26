# salles/views.py

from django.shortcuts import render, get_object_or_404, redirect # type: ignore
from .models import Salle
from .forms import ReservationForm
from reservations.models import Reservation
from datetime import date, datetime, time, timedelta

# FONCTION N°1 : LISTE DES SALLES (Celle qui manquait)
def liste_salles(request):
    categorie_filtre = request.GET.get('categorie')
    if categorie_filtre:
        salles = Salle.objects.filter(categorie=categorie_filtre)
    else:
        salles = Salle.objects.all()
    return render(request, 'salles/liste_salles.html', {'salles': salles})

# FONCTION N°2 : DÉTAIL D'UNE SALLE ET RÉSERVATION (La version avec l'heure)
def detail_salle(request, salle_id):
    salle = get_object_or_404(Salle, pk=salle_id)
    
    reservations_confirmees = Reservation.objects.filter(
        salle=salle,
        statut=Reservation.CONFIRMEE,
        date_reservation__gte=date.today()
    )
    
    creneaux_reserves = {}
    for resa in reservations_confirmees:
        date_str = resa.date_reservation.strftime('%Y-%m-%d')
        if date_str not in creneaux_reserves:
            creneaux_reserves[date_str] = []
        
        heure_debut_resa = resa.heure_debut
        for i in range(resa.duree_heures):
            creneau = (datetime.combine(date.today(), heure_debut_resa) + timedelta(hours=i)).time()
            creneaux_reserves[date_str].append(creneau.strftime('%H:%M'))
    
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            if not request.user.is_authenticated:
                return redirect('connexion')

            date_demandee = form.cleaned_data['date_reservation']
            heure_demandee_str = form.cleaned_data['heure_debut']
            heure_demandee = datetime.strptime(heure_demandee_str, '%H:%M').time()
            duree = form.cleaned_data['duree_heures']

            conflit = False
            for i in range(duree):
                creneau_a_verifier = (datetime.combine(date.today(), heure_demandee) + timedelta(hours=i)).time()
                creneau_a_verifier_str = creneau_a_verifier.strftime('%H:%M')
                date_demandee_str = date_demandee.strftime('%Y-%m-%d')
                if creneaux_reserves.get(date_demandee_str) and creneau_a_verifier_str in creneaux_reserves[date_demandee_str]:
                    conflit = True
                    break

            if conflit:
                form.add_error('heure_debut', f"Le créneau commençant à {heure_demandee_str} est déjà pris ou en conflit.")
            else:
                prix_total_calcule = salle.prix_par_heure * duree
                Reservation.objects.create(
                    salle=salle,
                    utilisateur=request.user,
                    date_reservation=date_demandee,
                    heure_debut=heure_demandee,
                    duree_heures=duree,
                    prix_total=prix_total_calcule,
                    type_reservation=Reservation.TYPE_SALLE,
                )
                context_confirmation = {'salle': salle, 'date': date_demandee, 'duree': duree, 'heure': heure_demandee_str}
                return render(request, 'salles/confirmation_reservation.html', context_confirmation)
    
    else:
        form = ReservationForm()

    context = {
            'salle': salle,
            'form': form,
            'creneaux_reserves': creneaux_reserves, 
        }
    return render(request, 'salles/detail_salle.html', context)