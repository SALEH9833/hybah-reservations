# comptes/forms.py (Version Finale, Propre et Corrigée)

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Profile

# --- FORMULAIRE D'INSCRIPTION PERSONNALISÉ ---
class CustomUserCreationForm(UserCreationForm):
    nom = forms.CharField(max_length=100, required=True, label="Nom de famille")
    prenom = forms.CharField(max_length=100, required=True, label="Prénom")
    email = forms.EmailField(required=True, label="Adresse e-mail")
    telephone = forms.CharField(max_length=20, required=False, label="Numéro de téléphone (Optionnel)")

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("nom", "prenom", "email", "telephone", "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit=False)
        
        base_username = f"{self.cleaned_data['prenom']}{self.cleaned_data['nom']}".lower().replace(' ', '')
        username = base_username
        num = 1
        while User.objects.filter(username=username).exists():
            username = f"{base_username}{num}"
            num += 1
        user.username = username
        user.email = self.cleaned_data['email']
        
        if commit:
            user.save()
            Profile.objects.create(
                user=user,
                nom=self.cleaned_data['nom'],
                prenom=self.cleaned_data['prenom'],
                telephone=self.cleaned_data['telephone'],
            )
        return user


# --- FORMULAIRE DE CONNEXION PAR E-MAIL ---
class EmailAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = "Adresse e-mail"
        self.fields['username'].help_text = ''

    def clean(self):
        # Le code ici est bien indenté
        email = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if email and password:
            user_by_email = User.objects.filter(email__iexact=email).first()
            
            if user_by_email:
                self.cleaned_data['username'] = user_by_email.username
        
        return super().clean()