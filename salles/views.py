# salles/views.py

from django.shortcuts import render, get_object_or_404, redirect # type: ignore
from .models import Salle
from .forms import ReservationForm
from reservations.models import Reservation
from datetime import date

# FONCTION N°1 : LISTE DES SALLES
def liste_salles(request):
    categorie_filtre = request.GET.get('categorie')
    if categorie_filtre:
        salles = Salle.objects.filter(categorie=categorie_filtre)
    else:
        salles = Salle.objects.all()
    return render(request, 'salles/liste_salles.html', {'salles': salles})

# FONCTION N°2 : DÉTAIL D'UNE SALLE ET RÉSERVATION
def detail_salle(request, salle_id):
    salle = get_object_or_404(Salle, pk=salle_id)
    
    reservations_confirmees = Reservation.objects.filter(
        salle=salle,
        statut=Reservation.CONFIRMEE,
        date_reservation__gte=date.today()
    )
    dates_reservees = [reservation.date_reservation for reservation in reservations_confirmees]

    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            if not request.user.is_authenticated:
                return redirect('connexion')

            date_demandee = form.cleaned_data['date_reservation']
            duree = form.cleaned_data['duree_heures']

            if date_demandee in dates_reservees:
                form.add_error('date_reservation', 'Cette salle est déjà réservée pour cette date.')
            else:
                prix_total_calcule = salle.prix_par_heure * duree
                Reservation.objects.create(
                    salle=salle,
                    utilisateur=request.user,
                    date_reservation=date_demandee,
                    duree_heures=duree,
                    prix_total=prix_total_calcule,
                )
                context_confirmation = {'salle': salle, 'date': date_demandee, 'duree': duree}
                return render(request, 'salles/confirmation_reservation.html', context_confirmation)
    
    else:
        form = ReservationForm()

    context = {
        'salle': salle,
        'form': form,
        'dates_reservees': dates_reservees,
    }
    return render(request, 'salles/detail_salle.html', context)