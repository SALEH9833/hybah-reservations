# hybah/urls.py (version finale et correcte)
from django.contrib import admin # type: ignore
from django.urls import path, include # type: ignore
from comptes import views as comptes_views
from django.conf import settings              # type: ignore # <-- 1. Ajoutez cet import
from django.conf.urls.static import static # type: ignore
urlpatterns = [
    path('', comptes_views.page_accueil, name='accueil'),
    # Si l'URL est /admin/, va voir l'admin de Django.
    path('admin/', admin.site.urls),

    # Si l'URL commence par /comptes/, passe le relais au fichier urls.py de l'app comptes.
    path('comptes/', include('comptes.urls')),
    path('salles/', include('salles.urls')), 
    path('gateaux/', include('gateaux.urls')),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)