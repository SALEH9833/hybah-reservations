# hybah/urls.py (Version Finale et Propre)

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from comptes import views as comptes_views

urlpatterns = [
    path('', comptes_views.page_accueil, name='accueil'),
    path('admin/', admin.site.urls),
    path('comptes/', include('comptes.urls')),
    path('salles/', include('salles.urls')),
    path('gateaux/', include('gateaux.urls')),
]

# Pour servir les images en développement
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)