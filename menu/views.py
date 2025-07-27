# menu/views.py
from django.shortcuts import render
from .models import Produit

def menu_view(request):
    # On récupère la catégorie sélectionnée, ou 'BOISSON_CHAUDE' par défaut
    categorie_filtre = request.GET.get('categorie', 'BOISSON_CHAUDE')
    
    # On filtre les produits par cette catégorie
    produits_filtres = Produit.objects.filter(categorie=categorie_filtre)
    
    context = {
        'produits': produits_filtres,
        'categories': Produit.CATEGORIE_CHOICES,
        'categorie_active': categorie_filtre,
    }
    return render(request, 'menu/menu_page.html', context)