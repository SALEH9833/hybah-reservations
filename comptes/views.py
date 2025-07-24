# comptes/views.py

from django.shortcuts import render, redirect # type: ignore
from django.contrib.auth import login # type: ignore
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm # type: ignore
from django.urls import reverse_lazy # type: ignore
from django.views import generic # type: ignore

# Vue pour la page d'inscription
class InscriptionView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('connexion')
    template_name = 'comptes/inscription.html'

# Vue pour la page d'accueil
def page_accueil(request):
    return render(request, 'accueil.html')

# LA FONCTION QUI MANQUAIT EST ICI :
def page_connexion_personnalisee(request):
    if request.user.is_authenticated:
        return redirect('accueil')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            
            if user.is_staff:
                return redirect('/admin/') # Redirection pour l'admin
            else:
                return redirect('accueil') # Redirection pour les autres
    else:
        form = AuthenticationForm()
        
    return render(request, 'comptes/connexion.html', {'form': form})