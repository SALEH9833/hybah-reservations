# salles/forms.py (Version Corrigée)

from django import forms # type: ignore

# On définit une liste de choix pour les heures, de 9h à 21h
HEURE_CHOICES = [
    (f"{h:02d}:00", f"{h:02d}:00") for h in range(9, 22)
]

class ReservationForm(forms.Form):
    date_reservation = forms.DateField(
        label="Date de la réservation",
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    
   
    heure_debut = forms.ChoiceField(
        label="Heure de début",
        choices=HEURE_CHOICES, 
        widget=forms.Select()  
    )
    
    duree_heures = forms.IntegerField(
        label="Durée de la location (en heures)",
        min_value=1,
        initial=1
    )