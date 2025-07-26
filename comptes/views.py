# comptes/views.py

from django.shortcuts import render, redirect # type: ignore
from django.contrib.auth import login # type: ignore
from django.contrib.auth.decorators import login_required # type: ignore
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm # type: ignore
from django.urls import reverse_lazy # type: ignore
from django.views import generic # type: ignore
from reservations.models import Reservation # Important pour l'historique

# --- Vue pour l'inscription ---
class InscriptionView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('connexion')
    template_name = 'comptes/inscription.html'

# --- Vue pour l'accueil ---
def page_accueil(request):
    return render(request, 'accueil.html')

# --- Vue pour la connexion personnalisée ---
def page_connexion_personnalisee(request):
    if request.user.is_authenticated:
        return redirect('accueil')
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if user.is_staff:
                return redirect('/admin/')
            else:
                return redirect('accueil')
    else:
        form = AuthenticationForm()
    return render(request, 'comptes/connexion.html', {'form': form})

# --- Vue pour l'historique des réservations ---
@login_required
def historique_reservations(request):
    reservations_utilisateur = Reservation.objects.filter(utilisateur=request.user).order_by('-horodatage_creation')
    context = {
        'reservations': reservations_utilisateur
    }
    return render(request, 'comptes/historique.html', context)
def debug_static_css(request):
    # On construit le chemin absolu vers le fichier style.css
    file_path = os.path.join(settings.BASE_DIR, 'static', 'style.css') # type: ignore
    
    try:
        # On essaie d'ouvrir et de lire le fichier
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        # On renvoie le contenu avec le bon type MIME pour le CSS
        return HttpResponse(content, content_type='text/css') # type: ignore
    except FileNotFoundError:
        # Si le fichier n'est pas trouvé, on renvoie une erreur 404 claire
        return HttpResponse("Le fichier style.css n'a pas été trouvé à l'emplacement attendu.", status=404) # type: ignore