# reservations/admin.py

from django.contrib import admin, messages # type: ignore
from django.utils.html import format_html # type: ignore
from .models import Reservation
import json

@admin.action(description="Marquer les réservations sélectionnées comme CONFIRMÉES")
def marquer_comme_confirmee(modeladmin, request, queryset):
    queryset.update(statut=Reservation.CONFIRMEE)
    messages.success(request, "Les réservations sélectionnées ont été marquées comme confirmées.")

@admin.action(description="Marquer les réservations sélectionnées comme ANNULÉES")
def marquer_comme_annulee(modeladmin, request, queryset):
    queryset.update(statut=Reservation.ANNULEE)
    messages.success(request, "Les réservations sélectionnées ont été annulées.")

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    actions = [marquer_comme_confirmee, marquer_comme_annulee]

    list_display = (
        'id', 
        'utilisateur', 
        'type_reservation', 
        'statut', 
        'prix_total', 
        'date_creation_formatee', # <-- CORRIGÉ : On n'utilise que le nom de la fonction
    )
    
    list_filter = ('statut', 'type_reservation', 'date_reservation')
    search_fields = ('utilisateur__username', 'salle__nom')
    
    fieldsets = (
        ('Informations Générales', {'fields': ('utilisateur', 'statut', 'type_reservation', 'prix_total')}),
        ('Détails Salle', {'fields': ('salle', 'date_reservation', 'heure_debut', 'duree_heures')}),
        ('Détails Gâteau', {'fields': ('formatted_gateau_details',)}),
        ('Dates', {'fields': ('horodatage_creation',)}),
    )
    
    readonly_fields = ('horodatage_creation', 'formatted_gateau_details')

    # --- Les fonctions doivent être indentées DANS la classe ---
    def date_creation_formatee(self, obj):
        if obj.horodatage_creation:
            return obj.horodatage_creation.strftime("%d %B %Y à %H:%M")
        return "N/A"
    date_creation_formatee.short_description = "Date de Création"
    date_creation_formatee.admin_order_field = 'horodatage_creation'

    def formatted_gateau_details(self, obj):
        if obj.gateau_details:
            details = json.dumps(obj.gateau_details, indent=4, ensure_ascii=False)
            return format_html("<pre>{}</pre>", details)
        return "N/A"
    formatted_gateau_details.short_description = 'Contenu de la Commande Gâteau'