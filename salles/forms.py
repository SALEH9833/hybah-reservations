# salles/forms.py
from django import forms # type: ignore

class ReservationForm(forms.Form):
    date_reservation = forms.DateField(
        label="Date de la réservation",
        widget=forms.DateInput(attrs={'type': 'date'}) # Pour avoir un calendrier
    )
    
    duree_heures = forms.IntegerField(
        label="Durée de la location (en heures)",
        min_value=1, # On ne peut pas réserver pour moins d'une heure
        initial=1    # La valeur par défaut sera 1
    )