# comptes/views.py (Version Finale et Corrigée)

from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views import generic
from django.http import JsonResponse
from reservations.models import Reservation
# On importe nos DEUX formulaires personnalisés
from .forms import CustomUserCreationForm, EmailAuthenticationForm 

# --- Vue pour l'inscription ---
class InscriptionView(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('connexion')
    template_name = 'comptes/inscription.html'

# --- Vue pour l'accueil ---
def page_accueil(request):
    return render(request, 'accueil.html')

# --- Vue pour la connexion (utilisant notre formulaire par e-mail) ---
def page_connexion_personnalisee(request):
    if request.user.is_authenticated:
        return redirect('accueil')
        
    if request.method == 'POST':
        # CETTE LIGNE EST LA PLUS IMPORTANTE
        # Elle doit utiliser EmailAuthenticationForm
        form = EmailAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            
            if not request.POST.get('remember_me', None):
                request.session.set_expiry(0)
            else:
                request.session.set_expiry(None)
            
            if user.is_staff:
                return redirect('/admin/')
            else:
                return redirect('accueil')
    else:
        # CETTE LIGNE AUSSI EST IMPORTANTE
        form = EmailAuthenticationForm()
        
    return render(request, 'comptes/connexion.html', {'form': form})

# --- Vue pour l'historique ---
@login_required
def historique_reservations(request):
    reservations_utilisateur = Reservation.objects.filter(utilisateur=request.user).order_by('-horodatage_creation')
    context = {
        'reservations': reservations_utilisateur
    }
    return render(request, 'comptes/historique.html', context)
@login_required
def supprimer_reservation(request, reservation_id):
    # On s'assure que c'est une requête POST pour la sécurité
    if request.method == 'POST':
        try:
            # On cherche la réservation à supprimer
            # ET on s'assure qu'elle appartient bien à l'utilisateur connecté
            # (pour l'empêcher de supprimer les réservations des autres)
            reservation = Reservation.objects.get(pk=reservation_id, utilisateur=request.user)
            
            # On la supprime
            reservation.delete()
            
            # On renvoie un message de succès
            return JsonResponse({'status': 'succes', 'message': 'Réservation supprimée.'})
        except Reservation.DoesNotExist:
            return JsonResponse({'status': 'erreur', 'message': 'Réservation non trouvée ou vous n\'avez pas la permission.'})
    
    return JsonResponse({'status': 'erreur', 'message': 'Méthode non autorisée.'})